"""문서 overlay 전용: 사전 의미와 독립적인 열/FK 근거를 함께 요구한다.

실제 테이블 접두어는 분류 점수에 사용하지 않는다. 업무 공식 분류/사람 승인을 뜻하지 않는다.
"""
from collections import Counter, defaultdict
import re


# id, Korean label, dictionary semantic pattern, corroborating physical-column pattern, scope
RULES = (
    ("data-exchange", "데이터 연계·가져오기·내보내기", r"\b(import|imported|export|replication|edi|web service|migration script|uuid mapping)\b", r"(i_isimported|i_errormsg|processing|processed|import|export|replication|webservice|impformat|exp_format|edi)", "원본 사전이 명시하는 적재 준비·교환 형식·전송 처리기와 그 실행 기록을 탐색합니다."),
    ("manufacturing", "제조·BOM·소요 계획", r"\b(manufacturing|production|bom|bill of material|material requirement|mrp|product planning|product operation)\b", r"(pp_order|pp_mrp|pp_product|m_bom|m_production|m_product_planning|qtyrequired|qtybatch|qtybom|iscritical|bomtype|workflow_id)", "제조 지시·제품 구성·생산 행·소요 계획의 문서 및 구성 참조를 탐색합니다."),
    ("assets", "자산·감가상각", r"\b(asset|depreciation|funding mode)\b", r"(a_asset|a_depreciation|a_funding|a_registration|asset|depreciat|useperiod|uselif|salvage|disposal|reval)", "자산 식별·취득/처분·감가상각 설정과 관련 금액/기간 기록을 탐색합니다."),
    ("workflow", "워크플로 정의·실행", r"\b(workflow|transition condition|node transition)\b", r"(ad_wf_|ad_workflow|wfstate|wfresponsible|action|docaction|transition|priority|iscentrallymaintained)", "사전에서 workflow로 설명한 노드·전이·책임·실행 활동의 참조를 탐색합니다."),
    ("payroll", "인사·급여", r"\b(payroll|employee attribute|paycheck)\b", r"(hr_concept|hr_employee|hr_department|hr_job|hr_payroll|hr_contract|hr_period|hr_process|hr_list|hr_year|payroll|employee|validfrom|validto|amount|qty|salary|concept|department|paydate)", "급여 계약·사원·개념·기간·이동/계산 기록의 연결을 탐색합니다."),
    ("promotion", "프로모션·마케팅", r"\b(promotion|campaign|marketing|sales channel)\b", r"(promotion|campaign|channel|reward|discount|c_bpartner|m_product|startdate|enddate)", "프로모션 조건/보상·상품 그룹·캠페인의 설정 참조를 탐색합니다. 실제 할인 적용 여부를 보장하지 않습니다."),
    ("quality", "품질 시험·규격", r"\b(quality|specification)\b", r"(quality|specification|m_product|testtype|testvalue|result|validfrom)", "상품의 품질 시험·시험 결과·규격 조건 참조를 탐색합니다."),
    ("invoice", "청구·대변 문서", r"\b(invoice|invoiced|invoicing)\b", r"(c_invoice|dateinvoiced|invoiceline|grandtotal|totallines|invoiced|qtyinvoiced)", "청구 헤더·상세·세금·문서 유형의 연결을 탐색합니다. 금액의 세금 처리나 집계식은 별도 업무 규칙입니다."),
    ("order", "주문·수주·발주", r"\b(order|orders|purchase order|requisition)\b", r"(c_order|dateordered|orderline|qtyordered|m_requisition|m_pricelist|issotrx|c_bpartner)", "주문/발주·요청 헤더와 상세의 거래처·상품·일자 참조를 탐색합니다. 판매/구매 방향은 별도 필드를 확인합니다."),
    ("payment", "입출금·은행·결제 배분", r"\b(payment|cash|bank|allocation|dunning|cheque|check book|credit card|remittance)\b", r"(c_payment|c_cash|c_bank|c_allocation|c_dunning|c_pay|payment|payamt|statement|iban|routing|accountno|tendertype|creditcard)", "입출금·은행 명세·현금·수금/지급 배분의 참조를 탐색합니다. 청구액과 입금액을 동일시하지 않습니다."),
    ("tax", "세금·원천징수", r"\b(tax|taxation|withholding|1099)\b", r"(c_tax|c_withholding|taxamt|taxbase|taxrate|rate|istaxincluded|withholding|1099)", "세율·세금 구분·원천징수 및 문서 세금 항목의 참조를 탐색합니다."),
    ("accounting", "회계·원장·예산", r"\b(accounting|acct|account schema|general ledger|gl|journal|budget|account reconciliation|trial balance|account combination|account element)\b", r"(c_acct|account|acct|gl_journal|gl_budget|gl_distribution|gl_fund|fact_acct|amtsource|amtacct|posting|dateacct|c_element|c_validcombination|budget)", "회계 스키마·계정/차원·분개·예산·회계 사실의 참조를 탐색합니다. 전기 실행이나 잔액 정확성을 검증한 분류는 아닙니다."),
    ("inventory", "재고·창고·로케이터", r"\b(inventory|storage|warehouse|locator|stock|replenish|reservation|material demand|material forecast|lot|serial no)\b", r"(m_inventory|m_storage|m_warehouse|m_locator|m_lot|qtyonhand|qtyreserved|qtycount|qtybook|movementqty|m_replenish|datematerial|serno)", "창고/보관 위치·실사·재고 수량·예약·로트/일련번호의 참조를 탐색합니다."),
    ("logistics", "출하·입고·반품·배송", r"\b(shipment|receipt|ship receipt|distribution|shipping|shipper|freight|rma|return material|package|inventory move|move confirm|move line)\b", r"(m_inout|m_movement|m_ship|m_rma|m_package|dd_order|dd_networkdistribution|m_distribution|movementdate|movementqty|qty|freight|tracking|shipment|locator)", "출하/입고·이동·반품·배송/분배의 헤더/상세 참조를 탐색합니다. 물리 FK 화살표를 시간 순서로 해석하지 않습니다."),
    ("product", "상품·속성·가격·단위", r"\b(product|price|discount|uom|unit of measure|product attribute|attribute set|attribute value|substitute)\b", r"(m_product|m_price|m_attribute|m_discount|c_uom|pricelist|pricestd|pricelimit|producttype|sku|upc|value|uomsymbol|multiplyrate)", "상품/서비스 기준·속성·가격표·단위의 참조를 탐색합니다. 상품 행이 매출 실적을 뜻하지는 않습니다."),
    ("partner", "거래처·연락처·주소", r"\b(business partner|partner relation|partner location|customer|vendor|contact|address|location)\b", r"(c_bpartner|c_bp_group|c_bp_relation|c_location|address|postal|contact|phone|email|iscustomer|isvendor|salesrep|country|region)", "거래처·고객/공급자 역할·주소/연락처의 기준 참조를 탐색합니다."),
    ("project", "프로젝트·활동·작업", r"\b(project|project phase|project task|project issue|business activity|activity trl)\b", r"(c_project|c_phase|c_task|c_activity|project|planned|committed|contract|qty|startdate|finishdate)", "프로젝트/단계/작업·업무 활동과 예산/수량의 참조를 탐색합니다."),
    ("time-resource", "자원·시간·경비·교육", r"\b(resource|training|time and expense|expense report|expense line|expense type|time type)\b", r"(s_resource|s_training|s_time|s_expense|resource|datefrom|dateto|qty|hours|time|c_bpartner)", "자원 배정/가용성·시간/경비 보고·교육 일정의 참조를 탐색합니다."),
    ("request-support", "요청·지원·이슈", r"\b(request|known issue|issue recommendation|issue status|issue system|issue user|request resolution|request category|standard response|interest area)\b", r"(r_request|r_issue|r_status|r_group|r_category|r_resolution|r_interest|request|summary|result|c_bpartner|confidential)", "요청 유형/상태·지원 기록·관련 통지/이슈 참조를 탐색합니다."),
    ("reporting", "보고서·성과·대시보드", r"\b(report|reporting|performance|dashboard|measure|ratio|benchmark|goal|achievement|chart|graph)\b", r"(pa_goal|pa_measure|pa_ratio|pa_report|pa_dashboard|pa_benchmark|pa_colorschema|ad_chart|ad_report|ad_pinstance_id|report|measure|goal|ratio|benchmark|chart|selectclause|whereclause|sql|printformat|color|calculation)", "보고서 정의·성과 측정·차트/대시보드 구성의 참조를 탐색합니다. 표시 결과의 정확성 검증은 별도입니다."),
    ("user-contact", "공통 사용자·거래처 연락처", r"\b(user contact)\b", r"(c_bpartner|password|email|phone|ad_user|islocked|login)", "사전에서 시스템 사용자와 거래처 연락처를 함께 표현한 공통 객체를 탐색합니다."),
    ("identity", "사용자·인증·접근 권한", r"\b(role|roles|access|authorization|credential|password|ldap|mfa|multi factor|sso|user session|user substitute|user contact)\b", r"(ad_role|ad_user|ad_authorization|ad_session|mfa_method|mfa_registereddevice|mfa_registration|mfa_rule|sso_principal|password|access|permission|principal|token|credential|record_id|tablename)", "사용자/역할·인증 자격·기록/조직 접근 제한의 참조를 탐색합니다. 현재 계정 권한이 안전하다는 인증은 아닙니다."),
    ("workflow-configuration", "프로세스·스케줄·시스템 운영", r"\b(process|scheduler|schedule|system configurator|system definition|house keeping|smtp|alert|system issue|processor log|storage provider|notice)\b", r"(ad_process|ad_pinstance|ad_schedule|ad_alert|ad_system|ad_sysconfig|ad_smtp|ad_issue|ad_storage|processing|classname|cron|frequency|notification|event|errormsg|name|value)", "프로세스 실행 정의·스케줄·시스템 설정·알림/오류 기록의 참조를 탐색합니다."),
    ("application-metadata", "애플리케이션 사전·화면·서식", r"\b(table|column|field|window|tab|form|menu|reference|validation|element|print|font|color|style|theme|toolbar|workbench|desktop|wizard|tree|label|context help|system attribute|entity type|model validator|model generator|preference|user query|search definition)\b", r"(ad_table|ad_column|ad_field|ad_window|ad_tab|ad_form|ad_menu|ad_reference|ad_element|ad_print|ad_color|ad_style|ad_tree|ad_label|ad_ctx|tablename|columnname|displaytype|seqno|selectclause|isdisplayed|html|css|font)", "애플리케이션 사전의 테이블/열·화면/필드·선택값·출력 서식 정의를 탐색합니다."),
    ("common-master", "테넌트·조직·통화·지역·달력 기준", r"\b(tenant|organization|currency|country|region|city|calendar|period|conversion|document type|document sequence|payment term|unit precision)\b", r"(ad_client|ad_org|c_currency|c_country|c_region|c_city|c_calendar|c_period|c_year|c_conversion|c_doctype|c_paymentterm|iso_code|cursymbol|countrycode|startdate|enddate|periodno|docbasetype|currentnext)", "테넌트/조직·통화/환산·지리·달력·문서 유형 등 여러 업무에서 공유하는 기준 참조를 탐색합니다."),
    ("web-content", "웹 콘텐츠·미디어", r"\b(content|container|media|news|web project|webproject|template|advertising|wiki)\b", r"(cm_container|cm_cstage|cm_template|cm_webproject|cm_media|cm_advertising|cm_access|cm_news|content|template|media|container|webproject|url|html|xml|rss|ad_cat|news|wiki)", "콘텐츠 컨테이너·스테이지·템플릿·미디어 배포/뉴스의 참조를 탐색합니다."),
    ("web-store", "웹 상점·POS·웹 접점", r"\b(web store|pos|basket|web click|click count|web counter|counter count|web properties|web menu|web advertisement)\b", r"(w_store|w_basket|w_click|w_counter|w_ad|u_pos|u_web|url|web|m_pricelist|c_bpartner|terminal|counter)", "웹 상점/장바구니·POS·접점 카운터/메뉴의 참조를 탐색합니다."),
    ("knowledge", "지식·분류·문서", r"\b(knowledge|knowledge entry|knowledge category|knowledge source|knowledge synonym|knowledge topic)\b", r"(k_entry|k_category|k_source|k_topic|k_type|k_index|keyword|text|content|source)", "지식 항목·출처·키워드/분류·연관 항목의 참조를 탐색합니다."),
    ("auction", "경매·입찰·판매 제안", r"\b(auction|bid|bids|offer|buyer funds|seller funds)\b", r"(b_topic|b_bid|b_offer|b_buyer|b_seller|bid|offer|fund|price|qty|c_bpartner)", "사전이 명시한 경매 토픽·입찰/판매 제안·참여자 자금의 참조를 탐색합니다."),
    ("audit-attachment", "변경 기록·첨부·보관", r"\b(change log|access log|archive|attachment|audit|document archive)\b", r"(ad_changelog|ad_archive|ad_attachment|ad_accesslog|record_id|oldvalue|newvalue|binarydata|content|filename|data|table_id)", "문서 첨부/보관·변경 전후 값·시스템 접근 기록의 참조를 탐색합니다."),
)

COMMON_COLUMNS = {"ad_client_id", "ad_org_id", "created", "createdby", "updated", "updatedby", "isactive", "name", "description", "help", "value"}
DOMAINS = {r[0]: {"name": r[1], "scope": r[4], "dictionary_pattern": r[2], "column_pattern": r[3]} for r in RULES}
PURPOSE_QUALIFIERS = (
    (r"\b(import|imported|export|replication|web service|migration script)\b", "data-exchange"),
    (r"\b(report|reporting|dashboard)\b", "reporting"),
    (r"\b(manufacturing|production|bom|material requirement|mrp|product planning)\b", "manufacturing"),
    (r"\b(payroll)\b", "payroll"),
    (r"\b(quality|specification)\b", "quality"),
    (r"\b(promotion|campaign|marketing)\b", "promotion"),
    (r"\b(user contact)\b", "user-contact"),
    (r"\b(workflow)\b", "workflow"),
    (r"\b(access|authorization|credential|password|mfa|sso|ldap)\b", "identity"),
    (r"\b(web store|pos|basket|web click|web counter)\b", "web-store"),
)


def normalized(value):
    value = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(value or ""))
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def classify(snapshot):
    tables = {t["physical_name"]: t for t in snapshot["tables"]}
    columns, edges, primary = defaultdict(list), defaultdict(list), defaultdict(set)
    for c in snapshot["columns"]:
        columns[c["table_name"]].append(c)
    for fk in snapshot["constraints"]:
        if fk["kind"] == "p":
            primary[fk["source_table"]].update(fk["source_columns"])
        if fk["kind"] != "f" or not fk.get("validated") or set(fk["source_columns"]) <= {"ad_client_id", "ad_org_id", "createdby", "updatedby"}:
            continue
        if fk["source_table"] in tables and fk["target_table"] in tables:
            edges[fk["source_table"]].append(("outgoing", fk, fk["target_table"]))
            if fk["source_table"] != fk["target_table"]:
                edges[fk["target_table"]].append(("incoming", fk, fk["source_table"]))
    result = {}
    for name, table in sorted(tables.items()):
        candidates = []
        dictionary_name = normalized(table.get("logical_name"))
        dictionary_description = normalized(table.get("description"))
        for slug, label, semantic, structural, _ in RULES:
            regex = re.compile(semantic, re.I)
            name_hits = sorted({m.group(0) for m in regex.finditer(dictionary_name)})
            description_hits = sorted({m.group(0) for m in regex.finditer(dictionary_description)})
            if not name_hits and not description_hits:
                continue
            key_columns = [c for c in columns[name] if c["physical_name"] not in COMMON_COLUMNS | primary[name] and not c["physical_name"].endswith("_uu")
                           and re.search(structural, c["physical_name"], re.I)]
            related = []
            for direction, fk, other in edges[name]:
                other_table = tables[other]
                # The adjacent table's own dictionary semantics must corroborate;
                # its prefix alone and common audit/tenant links never suffice.
                if regex.search(normalized(other_table.get("logical_name"))) or regex.search(normalized(other_table.get("description"))):
                    related.append({"direction": direction, "constraint": fk["name"], "source_table": fk["source_table"],
                        "source_columns": fk["source_columns"], "target_table": fk["target_table"], "target_columns": fk["target_columns"],
                        "other_table": other, "other_dictionary_name": other_table.get("logical_name"), "other_dictionary_description": other_table.get("description")})
            if not key_columns and not related:
                continue
            # Multiple compatible words/relations reinforce a proposal; unresolved
            # ties remain review-required. No physical table name participates.
            score = (6 if name_hits else 0) + min(len(name_hits), 2) + (2 if description_hits else 0) + min(len(key_columns), 2) + min(len(related), 2) * 2
            candidates.append({"domain": slug, "domain_label": label, "score": score, "name_hits": name_hits,
                "description_hits": description_hits, "key_columns": [{k: c.get(k) for k in ("physical_name", "logical_name", "description", "data_type")} for c in key_columns[:6]],
                "foreign_keys": sorted(related, key=lambda e: (e["direction"], e["constraint"]))[:4]})
        candidates.sort(key=lambda c: (-c["score"], c["domain"]))
        winner = candidates[0] if candidates and (len(candidates) == 1 or candidates[0]["score"] > candidates[1]["score"]) else None
        qualifier = None
        # Explicit purpose words distinguish e.g. Import Invoice from operational
        # Invoice and Manufacturing Order from generic Order. The selected rule
        # must already have its own column/FK corroboration; this is not a prefix override.
        for field, value in (("Name", dictionary_name), ("Description", dictionary_description)):
            for pattern, domain in PURPOSE_QUALIFIERS:
                match = re.search(pattern, value)
                candidate = next((c for c in candidates if c["domain"] == domain), None)
                if match and candidate:
                    winner, qualifier = candidate, {"field": field, "word": match[0], "domain": domain}
                    break
            if qualifier:
                break
        # Missing dictionary Name cannot become a proposal from structural naming alone.
        if winner and not table.get("logical_name"):
            winner = None
        status = "근거 기반 분류안(공식 분류 아님)" if winner else "확인 필요"
        observed_columns = [c for c in columns[name] if c["physical_name"] not in COMMON_COLUMNS | primary[name] and not c["physical_name"].endswith("_uu")]
        observed_fks = [{"direction": direction, "constraint": fk["name"], "source_table": fk["source_table"],
            "source_columns": fk["source_columns"], "target_table": fk["target_table"], "target_columns": fk["target_columns"],
            "other_table": other, "other_dictionary_name": tables[other].get("logical_name")}
            for direction, fk, other in edges[name]][:4]
        result[name] = {"table": name, "status": status, "domain": winner["domain"] if winner else "needs-review",
            "domain_label": winner["domain_label"] if winner else "업무영역 확인 필요",
            "dictionary_name": table.get("logical_name"), "dictionary_description": table.get("description"),
            "selected_evidence": winner, "candidates": candidates,
            "explicit_purpose_qualifier": qualifier,
            "observed_columns": [{k: c.get(k) for k in ("physical_name", "logical_name", "description", "data_type")} for c in observed_columns[:6]],
            "observed_foreign_keys": observed_fks,
            "unresolved_reason": None if winner else "사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음",
            "method": "자동 사전 의미 + 주요 열/FK 교차대조", "human_domain_approval": False}
    return result


def validate(snapshot, records):
    expected = {t["physical_name"] for t in snapshot["tables"]}
    assert set(records) == expected and len(records) == 912
    assert records == classify(snapshot), "overlay 근거/규칙 재계산 불일치"
    for record in records.values():
        if record["status"] != "확인 필요":
            evidence = record["selected_evidence"]
            assert record["dictionary_name"] and evidence and (evidence["name_hits"] or evidence["description_hits"])
            assert evidence["key_columns"] or evidence["foreign_keys"]
        assert record["human_domain_approval"] is False
    return {"total": len(records), "evidence_based_proposals": sum(r["status"] != "확인 필요" for r in records.values()),
        "review_required": sum(r["status"] == "확인 필요" for r in records.values()),
        "dictionary_and_columns_and_fk": sum(bool(r["selected_evidence"] and r["selected_evidence"]["key_columns"] and r["selected_evidence"]["foreign_keys"]) for r in records.values()),
        "dictionary_and_columns": sum(bool(r["selected_evidence"] and r["selected_evidence"]["key_columns"] and not r["selected_evidence"]["foreign_keys"]) for r in records.values()),
        "dictionary_and_fk": sum(bool(r["selected_evidence"] and not r["selected_evidence"]["key_columns"] and r["selected_evidence"]["foreign_keys"]) for r in records.values()),
        "automatic_records": len(records), "human_domain_approvals": 0,
        "proposal_dictionary_description_present": sum(bool(r["selected_evidence"] and r["dictionary_description"]) for r in records.values()),
        "domains": dict(sorted(Counter(r["domain"] for r in records.values()).items()))}
