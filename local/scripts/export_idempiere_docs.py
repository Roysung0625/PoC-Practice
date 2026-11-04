"""읽기 전용 PostgreSQL 메타데이터를 추출하여 AI용 테이블 문서를 생성한다."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / ".local/datasets/idempiere/documentation-snapshot.json"
OUTPUT = ROOT / "docs/database/idempiere"
OVERVIEWS = ROOT / "local/schema_docs"

GROUPS = {
    "a": "자산·감가상각", "ad": "애플리케이션 사전·화면·권한·시스템",
    "asp": "ASP 구독·기능 제공 설정", "b": "입찰·토픽·구매자/판매자 연결",
    "c": "거래처·주문·청구·결제·회계 기준", "cm": "웹 콘텐츠 관리",
    "dd": "물류 이동·분배 주문", "exp": "데이터 내보내기 형식·처리기",
    "fact": "회계 사실·집계", "gl": "총계정원장·예산·분개",
    "hr": "인사·급여", "i": "데이터 가져오기 준비", "imp": "가져오기·프로세서 설정",
    "k": "지식·분류·문서", "m": "제품·재고·출하/입고·원가",
    "mfa": "다중 인증", "pa": "성과·보고서·대시보드",
    "pp": "제조·생산 계획·제품 구성", "qm": "품질 관리",
    "r": "요청·지원·상태 관리", "s": "자원·시간·비용·교육",
    "sso": "통합 로그인", "t": "작업·보고서용 보조 테이블",
    "u": "POS·수표 제한·웹 메뉴 설정", "w": "웹 상점·카운터",
    "ws": "웹 서비스", "testuu": "시험용 UUID 관련", "other": "접두사 공통 분류 없음",
}
BASIS = {
    "dictionary": "원본 애플리케이션 사전 명칭·설명을 한국어로 해석",
    "structure": "물리명·열·외래키 구조를 근거로 보수적으로 해석",
    "uncertain": "역할을 확정할 사전 정보 부족: 구조에 따른 잠정 해석, 확인 필요",
}
ACTIONS = {"a": "NO ACTION", "r": "RESTRICT", "c": "CASCADE", "n": "SET NULL", "d": "SET DEFAULT"}


def group(name):
    return name.split("_", 1)[0] if "_" in name else "other"


def doc_path(name):
    return Path(group(name)) / f"{name}.md"


def cell(value):
    value = "" if value is None else str(value)
    return html.escape(value, quote=False).replace("|", "&#124;").replace("`", "&#96;").replace("\r", "").replace("\n", "<br>") or "—"


def link(name, directory=Path(".")):
    relative = Path(os.path.relpath(doc_path(name), directory)).as_posix()
    return f"[`{name}`]({relative})"


def code_columns(columns):
    return ", ".join(f"`{c}`" for c in columns)


def load_overviews(names):
    result = {}
    for path in sorted(OVERVIEWS.glob("overviews_*.json")):
        part = json.loads(path.read_text(encoding="utf-8-sig"))
        if result.keys() & part.keys():
            raise ValueError("한국어 개요 중복")
        result.update(part)
    if set(result) != set(names):
        raise ValueError("한국어 개요와 실제 테이블 집합 불일치")
    for entry in result.values():
        if not entry.get("logical_name_ko") or not entry.get("overview_ko") or entry.get("basis") not in BASIS:
            raise ValueError("한국어 개요 필수값 또는 근거 불일치")
    return result


def render(data):
    tables = {t["physical_name"]: t for t in data["tables"]}
    if len(tables) != len(data["tables"]):
        raise ValueError("사전에 물리 테이블 중복")
    if any(not re.fullmatch(r"[a-z0-9_]+", n) for n in tables):
        raise ValueError("문서 경로에 허용되지 않는 테이블명")
    summaries = load_overviews(tables)
    columns, outgoing, incoming, keys = (defaultdict(list) for _ in range(4))
    for c in data["columns"]:
        columns[c["table_name"]].append(c)
    foreign_keys = [c for c in data["constraints"] if c["kind"] == "f"]
    for c in data["constraints"]:
        if c["kind"] == "f":
            if c["source_schema"] != "adempiere" or c["target_schema"] != "adempiere":
                raise ValueError("외부 스키마 FK는 렌더러 확장이 필요합니다")
            if c["source_table"] not in tables or c["target_table"] not in tables:
                raise ValueError("FK 종단 테이블 누락")
            if len(c["source_columns"]) != len(c["target_columns"]):
                raise ValueError("복합 FK 열 순서 불일치")
            for side in ("source", "target"):
                if not set(c[f"{side}_columns"]) <= {col["physical_name"] for col in columns[c[f"{side}_table"]]}:
                    raise ValueError("FK 종단 열 누락")
            outgoing[c["source_table"]].append(c)
            incoming[c["target_table"]].append(c)
        else:
            keys[c["source_table"]].append(c)
    files = {}

    def add(path, content):
        files[Path(path).as_posix()] = content.rstrip() + "\n"

    def index_rows(names, directory=Path(".")):
        result = ["| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |",
                  "|---|---|---|---:|---|"]
        for name in names:
            t, s = tables[name], summaries[name]
            result.append(f"| {link(name, directory)} | {cell(s['logical_name_ko'])} | {cell(t['logical_name'])} | {t['row_count']:,} | {cell(s['overview_ko'])} |")
        return "\n".join(result)

    def fk_rows(relations, direction, directory):
        result = ["| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |",
                  "|---|---|---|---|---|---|---|"]
        for c in relations:
            # 마커는 문서 검증에서 FK 중복·누락과 방향을 독립적으로 확인한다.
            identity = f"{c['source_schema']}.{c['source_table']}.{c['name']}"
            result.append(f"| `{c['name']}` <!-- FK_{direction}: {identity} --> | {link(c['source_table'], directory)} | {code_columns(c['source_columns'])} | {link(c['target_table'], directory)} | {code_columns(c['target_columns'])} | {ACTIONS[c['on_delete']]} / {ACTIONS[c['on_update']]} | {'완료' if c['validated'] else '미검증'} / {'가능 (초기 지연)' if c['initially_deferred'] else '가능 (초기 즉시)' if c['deferrable'] else '불가'} |")
        return "\n".join(result) if relations else "해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다."

    for name, t in tables.items():
        s, directory = summaries[name], Path(group(name))
        primary = [k for k in keys[name] if k["kind"] == "p"]
        primary_columns = {c for k in primary for c in k["source_columns"]}
        text = [f"# {name} — {s['logical_name_ko']}", "",
                "[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)", "",
                "## 기본 정보", "", "| 항목 | 내용 |", "|---|---|",
                f"| 물리명 | `adempiere.{name}` |", f"| 한국어 논리명(문서용 해석) | {cell(s['logical_name_ko'])} |",
                f"| 원본 논리명 | {cell(t['logical_name'])} |", f"| 원본 사전 ID | {t['dictionary_id'] if t['dictionary_id'] is not None else '미등록'} |",
                f"| 분류 | `{group(name)}` — {cell(GROUPS.get(group(name), '해당 접두사 그룹'))} |",
                f"| 전체 테넌트 행 수 | {t['row_count']:,} |", f"| 물리 열 수 | {len(columns[name])} |",
                f"| 나가는 FK / 들어오는 FK | {len(outgoing[name])} / {len(incoming[name])} |",
                f"| 구조·행 수 확인 시점 | {data['captured_at']} |", "",
                "## 의미와 쓰임", "", s["overview_ko"], "", f"- 설명 근거: {BASIS[s['basis']]}.",
                "- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.",
                f"- 원본 설명: {cell(t['description'])}", f"- 원본 도움말: {cell(t['help'])}",
                f"- PostgreSQL 테이블 주석: {cell(t['comment'])}", "",
                "## 키와 열", "", "### 기본키·고유 제약조건", ""]
        if keys[name]:
            text += ["| 종류 | 제약조건 | 열(순서 유지) |", "|---|---|---|"]
            text += [f"| {'PRIMARY KEY' if k['kind']=='p' else 'UNIQUE'} | `{k['name']}` | {code_columns(k['source_columns'])} |" for k in keys[name]]
        else:
            text += ["PostgreSQL에 선언된 PRIMARY KEY·UNIQUE 제약조건이 없습니다. 별도 고유 인덱스 유무는 이 목록의 범위가 아닙니다."]
        unique_indexes = [ix for ix in data.get("unique_indexes", []) if ix["table_name"] == name]
        if unique_indexes:
            text += ["", "### 별도 고유 인덱스", "", "PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.", ""]
            for ix in unique_indexes:
                text += [f"- `{ix['index_name']}`: `{ix['definition']}`"]
        text += ["", "### 열 목록", "", "원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.", "",
                 "| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |", "|---:|---|---|---|---|---|---|---|"]
        for c in columns[name]:
            text.append(f"| {c['position']} | `{c['physical_name']}` | {cell(c['logical_name'])} | {cell(c['data_type'])} | {'허용' if c['nullable'] else '불가'} | {'예' if c['physical_name'] in primary_columns else '—'} | {cell(c.get('column_default'))} | {cell(c['description'])} |")
        text += ["", "## 외래키 흐름", "", "화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.", ""]
        unique_relations = {(c["source_table"], c["name"]): c for c in outgoing[name] + incoming[name]}
        diagram = list(unique_relations.values())[:10]
        if diagram:
            nodes = sorted({c[k] for c in diagram for k in ("source_table", "target_table")})
            ids = {node: f"n{i}" for i, node in enumerate(nodes)}
            text += [f"주변 관계 {len(unique_relations)}개 중 {len(diagram)}개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.", "", "```mermaid", "flowchart LR"]
            text += [f'    {ids[node]}["{node}"]' for node in nodes]
            for c in diagram:
                label = ", ".join(c["source_columns"]) + " → " + ", ".join(c["target_columns"])
                text.append(f'    {ids[c["source_table"]]} -->|"{label}"| {ids[c["target_table"]]}')
            text += ["```", ""]
        text += ["### 이 테이블이 참조하는 부모 — 나가는 FK", "", fk_rows(outgoing[name], "OUT", directory), "",
                 "### 이 테이블을 참조하는 자식 — 들어오는 FK", "", fk_rows(incoming[name], "IN", directory), "",
                 "## 조회 시 주의", "",
                 "- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.",
                 "- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.",
                 "- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다."]
        column_names = {c["physical_name"] for c in columns[name]}
        if "ad_client_id" in column_names:
            text += ["- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다."]
        if "issotrx" in column_names:
            text += ["- `issotrx`가 있습니다. 판매(`Y`)와 구매(`N`)를 구분해서 분석합니다."]
        if "record_id" in column_names:
            text += ["- `record_id`는 가리키는 테이블이 메타데이터에 따라 달라질 수 있습니다. 물리 FK 목록에 없는 대상은 별도 확인합니다."]
        if t["row_count"] == 0:
            text += ["- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다."]
        text += ["- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다."]
        add(doc_path(name), "\n".join(text))

    grouped = defaultdict(list)
    for name in tables:
        grouped[group(name)].append(name)
    counts = Counter(s["basis"] for s in summaries.values())
    add("TABLE_INDEX.md", "\n".join(["# 전체 테이블 일람", "", "[시작 안내](README.md) · [업무별 찾기](BUSINESS_GUIDE.md) · [외래키 안내](RELATIONSHIPS.md)", "",
        f"`{data['database']}.adempiere`의 물리 테이블 {len(tables):,}개입니다. 뷰 {data['excluded_view_count']}개는 제외했습니다. 확인 시점: {data['captured_at']}.", "",
        "한국어 논리명·개요는 원본 사전 또는 구조를 해석한 문서용 설명입니다. 테이블별 문서의 근거 구분을 확인하세요. 행 수는 전체 테넌트 기준이며, 0행도 구조 탐색에 필요하므로 포함합니다.", "", index_rows(tables)]))
    for prefix, names in sorted(grouped.items()):
        add(Path(prefix) / "README.md", "\n".join([f"# {prefix} — {GROUPS.get(prefix, '해당 접두사 그룹')}", "",
            "[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)", "",
            f"물리명 접두사 기준으로 묶은 {len(names)}개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.", "", index_rows(names, Path(prefix))]))
    groups_table = ["| 폴더 | 개요 | 테이블 수 |", "|---|---|---:|"]
    groups_table += [f"| [{p}/]({p}/README.md) | {GROUPS.get(p, '해당 접두사 그룹')} | {len(names)} |" for p,names in sorted(grouped.items())]
    add("README.md", f"""# iDempiere 테이블 사전 — AI 참조용

현재 프로젝트의 `poc_idempiere.adempiere`를 읽기 전용으로 조회해 만든 문서입니다. 물리 테이블 **{len(tables):,}개**, 열 **{len(data['columns']):,}개**, 물리 FK **{len(foreign_keys):,}개**를 포함합니다.

## 읽는 순서

1. [업무별 개요](BUSINESS_GUIDE.md)에서 질문과 관련된 업무·출발 테이블을 찾습니다.
2. [전체 테이블 일람](TABLE_INDEX.md)에서 물리명·한국어 논리명·원본 논리명·간단한 쓰임을 검색합니다.
3. 테이블 문서에서 열·기본키·나가는 FK·들어오는 FK를 읽고 필요한 테이블만 추가로 엽니다.
4. [외래키 안내](RELATIONSHIPS.md)의 방향·복합키·집계 주의사항을 확인한 뒤 SQL을 작성합니다.

## 출처와 범위

- 구조·행 수 수집 시점: **{data['captured_at']}**. 현재 연결된 DB에서 일관된 읽기 전용 스냅샷으로 수집했습니다.
- 물리 구조: PostgreSQL `pg_class`, `pg_attribute`, `pg_constraint`. 제약조건의 열 순서와 삭제·갱신 규칙을 보존합니다.
- 원본 논리명·업무 설명: `adempiere.ad_table`; 열 사전: `adempiere.ad_column`. 원본에 없는 설명은 `—`로 남깁니다.
- 한국어 이름·개요는 문서용 해석입니다. 현재 DB의 테이블 번역 언어는 {', '.join(x['ad_language'] for x in data['table_translation_languages']) or '없음'}이며 공식 한국어 사전을 가져온 것이 아닙니다.
- 설명 근거: 사전 해석 {counts['dictionary']}개 / 구조 해석 {counts['structure']}개 / 확인 필요 {counts['uncertain']}개. 각 문서에 구분을 적었습니다.
- 행 수는 **전체 테넌트** 기준입니다. 업무 데이터 행·개인정보·접속 비밀번호는 내보내지 않았습니다.
- 뷰 {data['excluded_view_count']}개는 이 테이블 문서에서 제외했습니다. 현재 앱의 조회 허용 대상도 물리 테이블입니다.
- UNIQUE 절에는 PostgreSQL 제약조건만 표시합니다. 별도 고유 인덱스·애플리케이션 로직·사전 참조 정의로만 정해진 관계 전체를 보장하지 않습니다.
- 이 문서는 AI에 파일로 제공할 참조 자료입니다. 앱의 기존 JSON 카탈로그나 Agent 입력을 Markdown 자동 로딩으로 변경하지 않았습니다.

## AI가 지켜야 할 해석 기준

- 알려진 물리명만 SQL에 사용하고, 명칭이 비슷하다는 이유로 FK·업무 지표를 만들지 않습니다.
- FK 화살표는 **자식 → 부모**입니다. 업무 처리 순서와 구분합니다. 자기참조와 복합 FK도 일반 FK와 같은 기준으로 읽습니다.
- `createdby`, `updatedby`, `ad_client_id`, `ad_org_id` 등 시스템·감사 관계가 업무 금액의 조인 경로를 대신하지 않습니다.
- 빈 테이블의 실적, 존재하지 않는 판매자 개념·통화·수익 지표를 추정하지 않습니다.
- 주문일·청구일·회계일, 판매/구매, 테넌트, 문서 상태, 통화를 먼저 정의합니다. 부모 합계가 상세 조인으로 중복되지 않게 합니다.

## 폴더별 일람

{chr(10).join(groups_table)}

## 갱신과 검증

프로젝트 루트의 PowerShell에서 실행합니다. 실행 환경은 기존 프로젝트 Python 가상환경이며 AWS 호출이나 DB 변경은 없습니다.

```powershell
.\\.venv\\Scripts\\python.exe .\\local\\scripts\\export_idempiere_docs.py --refresh
.\\.venv\\Scripts\\python.exe .\\local\\scripts\\verify_idempiere_docs.py
```

DB를 다시 읽지 않고 마지막 스냅샷에서 재생성하려면 `--refresh`를 생략합니다. 스냅샷은 Git 제외 경로 `.local/datasets/idempiere/documentation-snapshot.json`, 한국어 설명 원본은 `local/schema_docs/overviews_*.json`입니다. 테이블이 추가·삭제되면 설명 집합과 구조 집합 불일치로 생성을 멈추므로 설명 파일도 갱신해야 합니다. 이전 생성 결과에만 존재하는 파일은 자동 삭제하지 않습니다.

검증 결과는 [검증 기록](VERIFICATION.md), 생성 파일 목록·SHA-256은 [manifest.json](manifest.json)에 있습니다.
""")
    add("RELATIONSHIPS.md", f"""# 외래키 흐름 읽기

[시작 안내](README.md) · [전체 테이블 일람](TABLE_INDEX.md)

물리 FK는 **{len(foreign_keys):,}개**입니다. 각 관계를 자식 문서의 나가는 FK 표와 부모 문서의 들어오는 FK 표 양쪽에서 볼 수 있습니다. 자기참조 {sum(c['source_table']==c['target_table'] for c in foreign_keys)}개, 복합 FK {sum(len(c['source_columns'])>1 for c in foreign_keys)}개입니다.

## 방향과 해석

`자식 테이블(FK 열) → 부모 테이블(참조 열)`로 읽습니다. 예를 들어 `c_orderline.c_order_id → c_order.c_order_id`는 주문 상세가 주문 헤더를 참조한다는 뜻입니다. 물리 FK는 업무 발생 순서가 아니며, 자식 FK에 UNIQUE 제약이 있는지에 따라 대응 건수가 달라지므로 무조건 1:N으로 읽지 않습니다.

테이블별 Mermaid 그림은 주변 FK 최대 10개를 보여주는 요약입니다. **각 테이블 문서의 나가는·들어오는 FK 표는 생략 없는 전체 목록**입니다. 모든 자식·부모 테이블명은 해당 Markdown 문서로 연결됩니다.

## 복합 외래키

{link('ad_registration')}의 `(ad_system_id, ad_client_id)`는 {link('ad_system')}의 `(ad_system_id, ad_client_id)`를 함께 참조합니다. 한 열만으로 조인하면 FK와 다른 의미가 됩니다.

```sql
-- 읽기 예시: 열의 순서를 유지하고 모든 대응을 함께 사용합니다.
SELECT child.ad_system_id, child.ad_client_id
FROM adempiere.ad_registration AS child
JOIN adempiere.ad_system AS parent
  ON child.ad_system_id = parent.ad_system_id
 AND child.ad_client_id = parent.ad_client_id;
```

## 빠뜨리면 안 되는 관계

- 자기참조는 같은 문서의 양쪽 표에 표시합니다. 전역 FK 개수를 셀 때는 제약조건 한 개로 계산합니다.
- `record_id` 같은 동적 참조나 애플리케이션 사전의 참조 설정은 물리 FK가 아닐 수 있습니다. 이 문서에는 실제 `pg_constraint`에 존재하는 FK만 넣었습니다.
- NULL 허용은 열 목록에서 확인합니다. FK가 있다는 사실만으로 필수 입력이라고 가정하지 않습니다.
- CASCADE·SET NULL 등은 **삭제/갱신 시 DB 제약 동작**을 설명합니다. 이 프로젝트의 SQL 조회 계정은 읽기 전용입니다.
- 부모의 총액을 상세와 조인한 후 그대로 합산하지 않습니다. 주문·청구·입출금은 서로 다른 지표입니다.
""")
    add("BUSINESS_GUIDE.md", business_guide(data))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for relative, content in files.items():
        path = OUTPUT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    manifest = {"database": data["database"], "schema": data["schema"], "captured_at": data["captured_at"],
                "snapshot_sha256": hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest(),
                "table_count": len(tables), "column_count": len(data["columns"]), "foreign_key_count": len(foreign_keys),
                "table_paths": {name: doc_path(name).as_posix() for name in tables},
                "overview_sources": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OVERVIEWS.glob('overviews_*.json'))},
                "files": {p: hashlib.sha256(c.encode('utf-8')).hexdigest() for p,c in files.items()}}
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"generated_tables": len(tables), "markdown_files": len(files), "foreign_keys": len(foreign_keys), "output": str(OUTPUT)}, ensure_ascii=False))


def business_guide(data):
    def links(*names):
        return " · ".join(link(name) for name in names)
    fact_rows = next(t['row_count'] for t in data['tables'] if t['physical_name']=='fact_acct')
    date_range = data['invoice_date_range']
    return f"""# 업무별 테이블 안내

[시작 안내](README.md) · [전체 일람](TABLE_INDEX.md) · [외래키 읽는 법](RELATIONSHIPS.md)

## 질문에서 출발 테이블 찾기

| 업무·질문 | 출발 테이블 | 쓰임과 구분 |
|---|---|---|
| 고객·공급업체·거래처 | {links('c_bpartner','c_bpartner_location','ad_user')} | 거래처, 거래처 주소, 사용자/담당자를 구분합니다. 고객을 임의로 판매자 계정으로 바꾸지 않습니다. |
| 판매·구매 주문 | {links('c_order','c_orderline')} | 주문 헤더와 품목 상세. `issotrx`로 판매/구매를 구분하고 주문일 기준을 명시합니다. |
| 청구·매출 분석 | {links('c_invoice','c_invoiceline','c_doctype','c_currency')} | 청구 금액과 상세, 문서 종류, 통화를 함께 확인합니다. 수금액·회계 수익과 동일시하지 않습니다. |
| 수금·지급·상계 | {links('c_payment','c_allocationhdr','c_allocationline')} | 현금 흐름과 청구서 연결을 확인합니다. 결제액을 주문액으로 해석하지 않습니다. |
| 출하·입고 | {links('m_inout','m_inoutline')} | 출입고 헤더/상세와 주문·청구 상세 FK를 확인합니다. 입고와 출하를 구분합니다. |
| 제품·창고·재고 | {links('m_product','m_warehouse','m_locator','m_storageonhand','m_inventory','m_inventoryline')} | 제품 기준, 창고/로케이터, 보유 재고, 실사 문서를 구분합니다. |
| 가격·통화·세금 | {links('m_pricelist','m_pricelist_version','m_productprice','c_currency','c_tax')} | 유효한 가격표·버전·통화와 세금 기준을 확인합니다. 통화 혼합 합산을 피합니다. |
| 회계·원장 | {links('fact_acct','gl_journal','gl_journalline','c_acctschema','c_validcombination')} | 회계 전표·분개와 계정 체계. 수집 시점 `fact_acct`는 {fact_rows:,}행입니다. 행이 없으면 원장 기반 손익의 근거가 없습니다. |
| 프로젝트 | {links('c_project','c_projectphase','c_projecttask','c_projectline')} | 프로젝트와 단계·작업·내역의 연결을 확인합니다. |
| 테넌트·조직·권한 | {links('ad_client','ad_org','ad_user','ad_role','ad_user_roles')} | 업무 소유 범위와 사용자 접근 설정. 실제 거래 실적과 분리합니다. |
| 테이블·열·화면 사전 | {links('ad_table','ad_column','ad_element','ad_window','ad_tab','ad_field')} | 물리 구조의 업무 의미와 화면 연결을 찾습니다. 사전상의 관계가 항상 물리 FK인 것은 아닙니다. |

## 대표적인 관계를 읽는 방법

다음은 DB에 선언된 FK의 일부입니다. 화살표는 자식 → 부모이며 실제 문서 상태 전이를 표시하지 않습니다.

```mermaid
flowchart LR
    c_orderline -->|c_order_id| c_order
    c_order -->|c_bpartner_id| c_bpartner
    c_invoiceline -->|c_invoice_id| c_invoice
    c_invoiceline -->|c_orderline_id| c_orderline
    m_inoutline -->|m_inout_id| m_inout
    m_inoutline -->|c_orderline_id| c_orderline
    c_invoice -->|c_currency_id| c_currency
    c_invoice -->|c_doctype_id| c_doctype
```

## GardenWorld에서 적용할 기준

- 기본 업무 테넌트는 `ad_client_id=11`입니다. 시스템 공통 기준값에는 `0`이 쓰일 수 있어 모든 테이블에 같은 필터를 기계적으로 적용하지 않습니다.
- 판매/구매는 `issotrx='Y'/'N'`로 구분합니다. 확정 거래만 필요하면 문서 상태 `CO`·`CL`을 조건으로 사용한다고 계획에 명시합니다.
- 주문액(`c_order`), 청구액(`c_invoice`), 수금/지급액(`c_payment`)은 다릅니다. 질문의 지표를 먼저 정합니다.
- 청구서 `totallines`는 문서행 합계, `grandtotal`은 총액입니다. 금액의 세금 포함 여부는 `istaxincluded`·가격표·세액과 실제 계산 규칙을 확인해 정의합니다. 상세 집계에는 `c_invoiceline.linenetamt` 등 상세 수준의 값을 사용하고 헤더 합계를 중복하지 않습니다.
- 판매 대변전표는 `c_doctype.docbasetype='ARC'`를 확인해 차감합니다. USD·EUR를 임의 환율로 합치지 않습니다.
- {data['captured_at']} 수집 시 GardenWorld(`ad_client_id=11`)의 청구일 범위는 {date_range['min']} ~ {date_range['max']}입니다. 데모 데이터를 최근 거래나 실제 기업 실적으로 설명하지 않습니다.
- 임베딩 호출 설정과 문서 검색 시스템은 별개입니다. 이 Markdown 문서 생성으로 벡터 검색·RAG가 자동 구성되지는 않습니다.
"""


def extract():
    import psycopg
    from psycopg import sql
    from psycopg.rows import dict_row
    from dotenv import dotenv_values

    env = dotenv_values(ROOT / ".local/app.env")
    with psycopg.connect(env["POC_DB_DSN"], connect_timeout=5, row_factory=dict_row,
                         options="-c default_transaction_read_only=on -c statement_timeout=20000") as conn:
        conn.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        identity = conn.execute("SELECT current_database() AS database, current_setting('transaction_read_only') AS read_only").fetchone()
        if identity["database"] != "poc_idempiere" or identity["read_only"] != "on":
            raise ValueError("대상 DB 또는 읽기 전용 설정 불일치")
        tables = conn.execute("""
            SELECT c.relname AS physical_name, obj_description(c.oid, 'pg_class') AS comment,
                   d.ad_table_id::bigint AS dictionary_id, d.name AS logical_name,
                   d.description, d.help, d.entitytype
            FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
            LEFT JOIN adempiere.ad_table d ON lower(d.tablename)=c.relname
            WHERE n.nspname='adempiere' AND c.relkind IN ('r','p') ORDER BY c.relname
        """).fetchall()
        columns = conn.execute("""
            SELECT c.relname AS table_name, a.attname AS physical_name, a.attnum AS position,
                   format_type(a.atttypid,a.atttypmod) AS data_type, NOT a.attnotnull AS nullable,
                   col_description(c.oid,a.attnum) AS comment,
                   pg_get_expr(def.adbin,def.adrelid) AS column_default,
                   dc.name AS logical_name, dc.description, dc.help,
                   dc.iskey, dc.ad_reference_id::bigint AS reference_type
            FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
            JOIN pg_attribute a ON a.attrelid=c.oid AND a.attnum>0 AND NOT a.attisdropped
            LEFT JOIN pg_attrdef def ON def.adrelid=c.oid AND def.adnum=a.attnum
            LEFT JOIN adempiere.ad_table dt ON lower(dt.tablename)=c.relname
            LEFT JOIN adempiere.ad_column dc ON dc.ad_table_id=dt.ad_table_id AND lower(dc.columnname)=a.attname
            WHERE n.nspname='adempiere' AND c.relkind IN ('r','p') ORDER BY c.relname,a.attnum
        """).fetchall()
        constraints = conn.execute("""
            SELECT co.conname AS name, co.contype AS kind, ns.nspname AS source_schema,
                   src.relname AS source_table, nt.nspname AS target_schema, dst.relname AS target_table,
                   ARRAY(SELECT a.attname FROM unnest(co.conkey) WITH ORDINALITY AS k(attnum,ord)
                         JOIN pg_attribute a ON a.attrelid=co.conrelid AND a.attnum=k.attnum ORDER BY k.ord) AS source_columns,
                   ARRAY(SELECT a.attname FROM unnest(co.confkey) WITH ORDINALITY AS k(attnum,ord)
                         JOIN pg_attribute a ON a.attrelid=co.confrelid AND a.attnum=k.attnum ORDER BY k.ord) AS target_columns,
                   co.confdeltype AS on_delete, co.confupdtype AS on_update,
                   co.convalidated AS validated, co.condeferrable AS deferrable,
                   co.condeferred AS initially_deferred
            FROM pg_constraint co JOIN pg_class src ON src.oid=co.conrelid
            JOIN pg_namespace ns ON ns.oid=src.relnamespace
            LEFT JOIN pg_class dst ON dst.oid=co.confrelid
            LEFT JOIN pg_namespace nt ON nt.oid=dst.relnamespace
            WHERE co.contype IN ('f','p','u') AND (ns.nspname='adempiere' OR nt.nspname='adempiere')
            ORDER BY ns.nspname,src.relname,co.conname
        """).fetchall()
        unique_indexes = conn.execute("""SELECT t.relname AS table_name,i.relname AS index_name,pg_get_indexdef(ix.indexrelid) AS definition
            FROM pg_index ix JOIN pg_class t ON t.oid=ix.indrelid JOIN pg_class i ON i.oid=ix.indexrelid
            JOIN pg_namespace n ON n.oid=t.relnamespace WHERE n.nspname='adempiere' AND ix.indisunique
            AND NOT EXISTS(SELECT 1 FROM pg_constraint co WHERE co.conindid=ix.indexrelid AND co.contype IN ('p','u'))
            ORDER BY t.relname,i.relname""").fetchall()
        for table in tables:
            table["row_count"] = conn.execute(sql.SQL("SELECT count(*) AS n FROM {}.{}").format(
                sql.Identifier("adempiere"), sql.Identifier(table["physical_name"]))).fetchone()["n"]
        translations = conn.execute("SELECT ad_language, count(*) AS n FROM adempiere.ad_table_trl GROUP BY ad_language ORDER BY ad_language").fetchall()
        views = conn.execute("SELECT count(*) AS n FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='adempiere' AND c.relkind='v'").fetchone()["n"]
        date_range = conn.execute("SELECT min(dateinvoiced)::date::text AS min, max(dateinvoiced)::date::text AS max FROM adempiere.c_invoice WHERE ad_client_id=11").fetchone()
        data = {"database": identity["database"], "schema": "adempiere", "read_only": True,
                "captured_at": datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds"),
                "tables": tables, "columns": columns, "constraints": constraints, "unique_indexes": unique_indexes,
                "table_translation_languages": translations, "excluded_view_count": views,
                "invoice_date_range": date_range}
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="현재 DB에서 읽기 전용으로 메타데이터를 수집")
    parser.add_argument("--snapshot-only", action="store_true")
    args = parser.parse_args()
    data = extract() if args.refresh else json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    if args.snapshot_only:
        print(json.dumps({"tables": len(data["tables"]), "columns": len(data["columns"]),
                          "foreign_keys": sum(c["kind"] == "f" for c in data["constraints"]),
                          "translation_languages": data["table_translation_languages"]}, ensure_ascii=False))
        return
    render(data)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # 접속 문자열이나 비밀값을 예외 출력에 포함하지 않는다.
        print(f"문서 처리 실패: {type(exc).__name__}", file=sys.stderr)
        raise SystemExit(1)
