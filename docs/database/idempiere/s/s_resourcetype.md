# s_resourcetype — 자원 유형

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.s_resourcetype` |
| 한국어 논리명(문서용 해석) | 자원 유형 |
| 원본 논리명 | Resource Type |
| 원본 사전 ID | 480 |
| 분류 | `s` — 자원·시간·비용·교육 |
| 전체 테넌트 행 수 | 3 |
| 물리 열 수 | 29 |
| 나가는 FK / 들어오는 FK | 3 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

자원 유형별 시간대·요일·단위와 단일 배정 여부 등을 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `s_resourcetype_pkey` | `s_resourcetype_id` |
| UNIQUE | `s_resourcetype_uu_idx` | `s_resourcetype_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `s_resourcetype_id` | Resource Type | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `value` | Search Key | character varying(40) | 불가 | — | — | Search key for the record in the format required - must be unique |
| 10 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `issingleassignment` | Single Assignment only | character(1) | 불가 | — | 'N'::bpchar | Only one assignment at a time (no double-booking or overlapping) |
| 13 | `c_uom_id` | UOM | numeric(10,0) | 불가 | — | — | Unit of Measure |
| 14 | `allowuomfractions` | Allow UoM Fractions | character(1) | 불가 | — | 'N'::bpchar | Allow Unit of Measure Fractions |
| 15 | `timeslotstart` | Slot Start | timestamp without time zone | 허용 | — | — | Time when timeslot starts |
| 16 | `timeslotend` | Slot End | timestamp without time zone | 허용 | — | — | Time when timeslot ends |
| 17 | `istimeslot` | Time Slot | character(1) | 불가 | — | 'N'::bpchar | Resource has time slot availability |
| 18 | `isdateslot` | Day Slot | character(1) | 불가 | — | 'N'::bpchar | Resource has day slot availability |
| 19 | `onsunday` | Sunday | character(1) | 불가 | — | 'N'::bpchar | Available on Sundays |
| 20 | `onmonday` | Monday | character(1) | 불가 | — | 'Y'::bpchar | Available on Mondays |
| 21 | `ontuesday` | Tuesday | character(1) | 불가 | — | 'Y'::bpchar | Available on Tuesdays |
| 22 | `onwednesday` | Wednesday | character(1) | 불가 | — | 'Y'::bpchar | Available on Wednesdays |
| 23 | `onthursday` | Thursday | character(1) | 불가 | — | 'Y'::bpchar | Available on Thursdays |
| 24 | `onfriday` | Friday | character(1) | 불가 | — | 'Y'::bpchar | Available on Fridays |
| 25 | `onsaturday` | Saturday | character(1) | 불가 | — | 'N'::bpchar | Available on Saturday |
| 26 | `m_product_category_id` | Product Category | numeric(10,0) | 불가 | — | — | Category of a Product |
| 27 | `c_taxcategory_id` | Tax Category | numeric(10,0) | 불가 | — | — | Tax Category |
| 28 | `chargeableqty` | Chargeable Quantity | numeric | 허용 | — | 0 | — |
| 29 | `s_resourcetype_uu` | S_ResourceType_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_taxcategory"]
    n1["c_uom"]
    n2["m_product_category"]
    n3["s_resource"]
    n4["s_resourcetype"]
    n4 -->|"c_taxcategory_id → c_taxcategory_id"| n0
    n4 -->|"c_uom_id → c_uom_id"| n1
    n4 -->|"m_product_category_id → m_product_category_id"| n2
    n3 -->|"s_resourcetype_id → s_resourcetype_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ctaxcategory_sresourcetype` <!-- FK_OUT: adempiere.s_resourcetype.ctaxcategory_sresourcetype --> | [`s_resourcetype`](s_resourcetype.md) | `c_taxcategory_id` | [`c_taxcategory`](../c/c_taxcategory.md) | `c_taxcategory_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cuom_sresourcetype` <!-- FK_OUT: adempiere.s_resourcetype.cuom_sresourcetype --> | [`s_resourcetype`](s_resourcetype.md) | `c_uom_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mprodcategory_sresourcetype` <!-- FK_OUT: adempiere.s_resourcetype.mprodcategory_sresourcetype --> | [`s_resourcetype`](s_resourcetype.md) | `m_product_category_id` | [`m_product_category`](../m/m_product_category.md) | `m_product_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `sresourcetype_sresource` <!-- FK_IN: adempiere.s_resource.sresourcetype_sresource --> | [`s_resource`](s_resource.md) | `s_resourcetype_id` | [`s_resourcetype`](s_resourcetype.md) | `s_resourcetype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
