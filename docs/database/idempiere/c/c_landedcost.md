# c_landedcost — 취득 부대원가 배부 설정

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_landedcost` |
| 한국어 논리명(문서용 해석) | 취득 부대원가 배부 설정 |
| 원본 논리명 | Landed Cost |
| 원본 사전 ID | 759 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 17 |
| 나가는 FK / 들어오는 FK | 5 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

청구 명세의 운송비 등 취득 부대원가를 입고·상품에 연결하고 원가 요소와 배부 기준을 지정한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_landedcost_pkey` | `c_landedcost_id` |
| UNIQUE | `c_landedcost_uu_idx` | `c_landedcost_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_landedcost_id` | Landed Cost | numeric(10,0) | 불가 | 예 | — | Landed cost to be allocated to material receipts |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 5 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 6 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 7 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 8 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 9 | `c_invoiceline_id` | Invoice Line | numeric(10,0) | 불가 | — | — | Invoice Detail Line |
| 10 | `m_costelement_id` | Cost Element | numeric(10,0) | 불가 | — | — | Product Cost Element |
| 11 | `m_inoutline_id` | Shipment/Receipt Line | numeric(10,0) | 허용 | — | — | Line on Shipment or Receipt document |
| 12 | `m_inout_id` | Shipment/Receipt | numeric(10,0) | 허용 | — | — | Material Shipment Document |
| 13 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 14 | `landedcostdistribution` | Cost Distribution | character(1) | 불가 | — | — | Landed Cost Distribution |
| 15 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 16 | `c_landedcost_uu` | C_LandedCost_UU | uuid | 허용 | — | — | — |
| 17 | `qty` | Quantity | numeric | 허용 | — | — | Quantity |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_invoiceline"]
    n1["c_landedcost"]
    n2["m_costelement"]
    n3["m_inout"]
    n4["m_inoutline"]
    n5["m_product"]
    n1 -->|"m_costelement_id → m_costelement_id"| n2
    n1 -->|"c_invoiceline_id → c_invoiceline_id"| n0
    n1 -->|"m_inout_id → m_inout_id"| n3
    n1 -->|"m_inoutline_id → m_inoutline_id"| n4
    n1 -->|"m_product_id → m_product_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccostelement_clandedcost` <!-- FK_OUT: adempiere.c_landedcost.ccostelement_clandedcost --> | [`c_landedcost`](c_landedcost.md) | `m_costelement_id` | [`m_costelement`](../m/m_costelement.md) | `m_costelement_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoiceline_clandedcost` <!-- FK_OUT: adempiere.c_landedcost.cinvoiceline_clandedcost --> | [`c_landedcost`](c_landedcost.md) | `c_invoiceline_id` | [`c_invoiceline`](c_invoiceline.md) | `c_invoiceline_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_clandedcost` <!-- FK_OUT: adempiere.c_landedcost.minout_clandedcost --> | [`c_landedcost`](c_landedcost.md) | `m_inout_id` | [`m_inout`](../m/m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minoutline_clandedcost` <!-- FK_OUT: adempiere.c_landedcost.minoutline_clandedcost --> | [`c_landedcost`](c_landedcost.md) | `m_inoutline_id` | [`m_inoutline`](../m/m_inoutline.md) | `m_inoutline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_clandedcost` <!-- FK_OUT: adempiere.c_landedcost.mproduct_clandedcost --> | [`c_landedcost`](c_landedcost.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
