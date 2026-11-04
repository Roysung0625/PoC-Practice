# ad_val_rule — 동적 검증 규칙

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_val_rule` |
| 한국어 논리명(문서용 해석) | 동적 검증 규칙 |
| 원본 논리명 | Dynamic Validation |
| 원본 사전 ID | 108 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 332 |
| 물리 열 수 | 14 |
| 나가는 FK / 들어오는 FK | 3 / 14 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

동적으로 적용하는 검증 규칙을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Dynamic Validation Rule
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_val_rule_pkey` | `ad_val_rule_id` |
| UNIQUE | `ad_val_rule_uu_idx` | `ad_val_rule_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_val_rule_id` | Dynamic Validation | numeric(10,0) | 불가 | 예 | — | Dynamic Validation Rule |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `type` | Type | character(1) | 허용 | — | — | Type of Validation (SQL, Java Script, Java Language) |
| 12 | `code` | Validation code | character varying(4000) | 허용 | — | — | Validation Code |
| 13 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 14 | `ad_val_rule_uu` | AD_Val_Rule_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 17개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_attribute"]
    n1["ad_client"]
    n2["ad_column"]
    n3["ad_entitytype"]
    n4["ad_field"]
    n5["ad_infocolumn"]
    n6["ad_org"]
    n7["ad_package_exp_detail"]
    n8["ad_val_rule"]
    n8 -->|"entitytype → entitytype"| n3
    n8 -->|"ad_client_id → ad_client_id"| n1
    n8 -->|"ad_org_id → ad_org_id"| n6
    n0 -->|"ad_val_rule_id → ad_val_rule_id"| n8
    n2 -->|"ad_val_rule_id → ad_val_rule_id"| n8
    n2 -->|"ad_val_rule_lookup_id → ad_val_rule_id"| n8
    n4 -->|"ad_val_rule_id → ad_val_rule_id"| n8
    n4 -->|"ad_val_rule_lookup_id → ad_val_rule_id"| n8
    n5 -->|"ad_val_rule_id → ad_val_rule_id"| n8
    n7 -->|"ad_val_rule_id → ad_val_rule_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `entityt_advalrule` <!-- FK_OUT: adempiere.ad_val_rule.entityt_advalrule --> | [`ad_val_rule`](ad_val_rule.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `val_ruleclient` <!-- FK_OUT: adempiere.ad_val_rule.val_ruleclient --> | [`ad_val_rule`](ad_val_rule.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `val_ruleorg` <!-- FK_OUT: adempiere.ad_val_rule.val_ruleorg --> | [`ad_val_rule`](ad_val_rule.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `advalrule_adattribute` <!-- FK_IN: adempiere.ad_attribute.advalrule_adattribute --> | [`ad_attribute`](ad_attribute.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_valrule_column` <!-- FK_IN: adempiere.ad_column.ad_valrule_column --> | [`ad_column`](ad_column.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrulelookup_adcolumn` <!-- FK_IN: adempiere.ad_column.advalrulelookup_adcolumn --> | [`ad_column`](ad_column.md) | `ad_val_rule_lookup_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_adfield` <!-- FK_IN: adempiere.ad_field.advalrule_adfield --> | [`ad_field`](ad_field.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrulelookup_adfield` <!-- FK_IN: adempiere.ad_field.advalrulelookup_adfield --> | [`ad_field`](ad_field.md) | `ad_val_rule_lookup_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_adinfocolumn` <!-- FK_IN: adempiere.ad_infocolumn.advalrule_adinfocolumn --> | [`ad_infocolumn`](ad_infocolumn.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_adpackageexpdetail` <!-- FK_IN: adempiere.ad_package_exp_detail.advalrule_adpackageexpdetail --> | [`ad_package_exp_detail`](ad_package_exp_detail.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_ad_processpara` <!-- FK_IN: adempiere.ad_process_para.advalrule_ad_processpara --> | [`ad_process_para`](ad_process_para.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_valrule_table` <!-- FK_IN: adempiere.ad_table.ad_valrule_table --> | [`ad_table`](ad_table.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_aduserdeffield` <!-- FK_IN: adempiere.ad_userdef_field.advalrule_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrulelookup_aduserdeffield` <!-- FK_IN: adempiere.ad_userdef_field.advalrulelookup_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_val_rule_lookup_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_aduserdefinfocolumn` <!-- FK_IN: adempiere.ad_userdef_info_column.advalrule_aduserdefinfocolumn --> | [`ad_userdef_info_column`](ad_userdef_info_column.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_aduserdefprocparamet` <!-- FK_IN: adempiere.ad_userdef_proc_parameter.advalrule_aduserdefprocparamet --> | [`ad_userdef_proc_parameter`](ad_userdef_proc_parameter.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_mattribute` <!-- FK_IN: adempiere.m_attribute.advalrule_mattribute --> | [`m_attribute`](../m/m_attribute.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
