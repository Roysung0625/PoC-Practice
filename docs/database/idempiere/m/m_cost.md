# m_cost — 제품 원가

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_cost` |
| 한국어 논리명(문서용 해석) | 제품 원가 |
| 원본 논리명 | Product Cost |
| 원본 사전 ID | 771 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 267 |
| 물리 열 수 | 23 |
| 나가는 FK / 들어오는 FK | 7 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제품·원가 유형·회계 스키마·원가 요소별 현재 원가와 수량 및 누적 금액을 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_cost_pkey` | `ad_client_id`, `ad_org_id`, `m_product_id`, `m_costtype_id`, `c_acctschema_id`, `m_costelement_id`, `m_attributesetinstance_id` |
| UNIQUE | `m_cost_uu_idx` | `m_cost_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | 예 | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | 예 | — | Organizational entity within tenant |
| 3 | `m_product_id` | Product | numeric(10,0) | 불가 | 예 | — | Product, Service, Item |
| 4 | `m_costtype_id` | Cost Type | numeric(10,0) | 불가 | 예 | — | Type of Cost (e.g. Current, Plan, Future) |
| 5 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 불가 | 예 | — | Rules for accounting |
| 6 | `m_costelement_id` | Cost Element | numeric(10,0) | 불가 | 예 | — | Product Cost Element |
| 7 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 불가 | 예 | — | Product Attribute Set Instance |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 10 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 11 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 12 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 13 | `currentcostprice` | Current Cost Price | numeric | 불가 | — | — | The currently used cost price |
| 14 | `currentqty` | Current Quantity | numeric | 불가 | — | 0 | Current Quantity |
| 15 | `cumulatedamt` | Accumulated Amt | numeric | 허용 | — | 0 | Total Amount |
| 16 | `cumulatedqty` | Accumulated Qty | numeric | 허용 | — | 0 | Total Quantity |
| 17 | `futurecostprice` | Future Cost Price | numeric | 허용 | — | — | — |
| 18 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 19 | `percent` | Percent | numeric(10,0) | 허용 | — | 0 | Percentage |
| 20 | `currentcostpricell` | Current Cost Price Lower Level | numeric | 허용 | — | 0 | Current Price Lower Level Is the sum of the costs of the components of this product manufactured for this level. |
| 21 | `futurecostpricell` | Future Cost Price Lower Level | numeric | 허용 | — | — | — |
| 22 | `iscostfrozen` | Cost Frozen | character(1) | 허용 | — | 'N'::bpchar | Indicated that the Standard Cost is frozen |
| 23 | `m_cost_uu` | M_Cost_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_org"]
    n2["c_acctschema"]
    n3["m_attributesetinstance"]
    n4["m_cost"]
    n5["m_costelement"]
    n6["m_costtype"]
    n7["m_product"]
    n4 -->|"ad_client_id → ad_client_id"| n0
    n4 -->|"ad_org_id → ad_org_id"| n1
    n4 -->|"c_acctschema_id → c_acctschema_id"| n2
    n4 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n3
    n4 -->|"m_costelement_id → m_costelement_id"| n5
    n4 -->|"m_costtype_id → m_costtype_id"| n6
    n4 -->|"m_product_id → m_product_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adclient_mcost` <!-- FK_OUT: adempiere.m_cost.adclient_mcost --> | [`m_cost`](m_cost.md) | `ad_client_id` | [`ad_client`](../ad/ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorg_m_cost` <!-- FK_OUT: adempiere.m_cost.adorg_m_cost --> | [`m_cost`](m_cost.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cacctschema_mcost` <!-- FK_OUT: adempiere.m_cost.cacctschema_mcost --> | [`m_cost`](m_cost.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `masi_mcost` <!-- FK_OUT: adempiere.m_cost.masi_mcost --> | [`m_cost`](m_cost.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcostelement_mcost` <!-- FK_OUT: adempiere.m_cost.mcostelement_mcost --> | [`m_cost`](m_cost.md) | `m_costelement_id` | [`m_costelement`](m_costelement.md) | `m_costelement_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcosttype_mcost` <!-- FK_OUT: adempiere.m_cost.mcosttype_mcost --> | [`m_cost`](m_cost.md) | `m_costtype_id` | [`m_costtype`](m_costtype.md) | `m_costtype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mcost` <!-- FK_OUT: adempiere.m_cost.mproduct_mcost --> | [`m_cost`](m_cost.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
