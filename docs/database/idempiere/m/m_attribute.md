# m_attribute — 제품 속성

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_attribute` |
| 한국어 논리명(문서용 해석) | 제품 속성 |
| 원본 논리명 | Attribute |
| 원본 사전 ID | 562 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 4 |
| 물리 열 수 | 21 |
| 나가는 FK / 들어오는 FK | 5 / 5 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제품의 특성을 표현하는 속성을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Product Attribute
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_attribute_pkey` | `m_attribute_id` |
| UNIQUE | `m_attribute_uu_idx` | `m_attribute_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_attribute_id` | Attribute | numeric(10,0) | 불가 | 예 | — | Product Attribute |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `ismandatory` | Mandatory | character(1) | 불가 | — | 'N'::bpchar | Data entry is required in this column |
| 12 | `isinstanceattribute` | Instance Attribute | character(1) | 불가 | — | 'N'::bpchar | The product attribute is specific to the instance (like Serial No, Lot or Guarantee Date) |
| 13 | `m_attributesearch_id` | Attribute Search | numeric(10,0) | 허용 | — | — | Common Search Attribute  |
| 14 | `attributevaluetype` | Attribute Value Type | character(1) | 불가 | — | 'S'::bpchar | Type of Attribute Value |
| 15 | `m_attribute_uu` | M_Attribute_UU | uuid | 허용 | — | — | — |
| 16 | `dateformat` | Date Format | character varying(20) | 허용 | — | NULL::character varying | Date format used in the input format |
| 17 | `ad_reference_id` | Reference | numeric(10,0) | 허용 | — | NULL::numeric | System Reference and Validation |
| 18 | `ad_reference_value_id` | Reference Key | numeric(10,0) | 허용 | — | NULL::numeric | Required to specify, if data type is Table or List |
| 19 | `ad_val_rule_id` | Dynamic Validation | numeric(10,0) | 허용 | — | NULL::numeric | Dynamic Validation Rule |
| 20 | `defaultvalue` | Default Logic | character varying(2000) | 허용 | — | NULL::character varying | Default value hierarchy, separated by ; |
| 21 | `entitytype` | Entity Type | character varying(40) | 허용 | — | NULL::character varying | Dictionary Entity Type; Determines ownership and synchronization |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 10개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_entitytype"]
    n1["ad_reference"]
    n2["ad_tableattribute"]
    n3["ad_val_rule"]
    n4["m_attribute"]
    n5["m_attributeinstance"]
    n6["m_attributesearch"]
    n7["m_attributeuse"]
    n8["m_attributevalue"]
    n9["qm_specificationline"]
    n4 -->|"ad_reference_id → ad_reference_id"| n1
    n4 -->|"ad_reference_value_id → ad_reference_id"| n1
    n4 -->|"ad_val_rule_id → ad_val_rule_id"| n3
    n4 -->|"entitytype → entitytype"| n0
    n4 -->|"m_attributesearch_id → m_attributesearch_id"| n6
    n2 -->|"m_attribute_id → m_attribute_id"| n4
    n5 -->|"m_attribute_id → m_attribute_id"| n4
    n7 -->|"m_attribute_id → m_attribute_id"| n4
    n8 -->|"m_attribute_id → m_attribute_id"| n4
    n9 -->|"m_attribute_id → m_attribute_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adreference_mattribute` <!-- FK_OUT: adempiere.m_attribute.adreference_mattribute --> | [`m_attribute`](m_attribute.md) | `ad_reference_id` | [`ad_reference`](../ad/ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreferencevalue_mattribute` <!-- FK_OUT: adempiere.m_attribute.adreferencevalue_mattribute --> | [`m_attribute`](m_attribute.md) | `ad_reference_value_id` | [`ad_reference`](../ad/ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_mattribute` <!-- FK_OUT: adempiere.m_attribute.advalrule_mattribute --> | [`m_attribute`](m_attribute.md) | `ad_val_rule_id` | [`ad_val_rule`](../ad/ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entitytype_mattribute` <!-- FK_OUT: adempiere.m_attribute.entitytype_mattribute --> | [`m_attribute`](m_attribute.md) | `entitytype` | [`ad_entitytype`](../ad/ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattributesearch_mattribute` <!-- FK_OUT: adempiere.m_attribute.mattributesearch_mattribute --> | [`m_attribute`](m_attribute.md) | `m_attributesearch_id` | [`m_attributesearch`](m_attributesearch.md) | `m_attributesearch_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mattribute_adtableattribute` <!-- FK_IN: adempiere.ad_tableattribute.mattribute_adtableattribute --> | [`ad_tableattribute`](../ad/ad_tableattribute.md) | `m_attribute_id` | [`m_attribute`](m_attribute.md) | `m_attribute_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattribute_mattributeinst` <!-- FK_IN: adempiere.m_attributeinstance.mattribute_mattributeinst --> | [`m_attributeinstance`](m_attributeinstance.md) | `m_attribute_id` | [`m_attribute`](m_attribute.md) | `m_attribute_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattribute_mattributeuse` <!-- FK_IN: adempiere.m_attributeuse.mattribute_mattributeuse --> | [`m_attributeuse`](m_attributeuse.md) | `m_attribute_id` | [`m_attribute`](m_attribute.md) | `m_attribute_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattribute_mattributevalue` <!-- FK_IN: adempiere.m_attributevalue.mattribute_mattributevalue --> | [`m_attributevalue`](m_attributevalue.md) | `m_attribute_id` | [`m_attribute`](m_attribute.md) | `m_attribute_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattribute_qmspecificationline` <!-- FK_IN: adempiere.qm_specificationline.mattribute_qmspecificationline --> | [`qm_specificationline`](../qm/qm_specificationline.md) | `m_attribute_id` | [`m_attribute`](m_attribute.md) | `m_attribute_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
