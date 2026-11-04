# m_transactionallocation — 재고 거래 배분

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_transactionallocation` |
| 한국어 논리명(문서용 해석) | 재고 거래 배분 |
| 원본 논리명 | M_TransactionAllocation |
| 원본 사전 ID | 636 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 22 |
| 나가는 FK / 들어오는 FK | 10 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

입고측과 출고측 재고 거래 및 관련 문서행을 배분 수량·전략과 함께 연결한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_transactionallocation_pkey` | `m_transaction_id`, `allocationstrategytype` |
| UNIQUE | `m_transactionallocation_uu_idx` | `m_transactionallocation_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_transaction_id` | Inventory Transaction | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `allocationstrategytype` | Allocation Strategy | character(1) | 불가 | 예 | — | Allocation Strategy |
| 3 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 4 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 5 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 8 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 9 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 10 | `m_product_id` | Product | numeric(10,0) | 불가 | — | — | Product, Service, Item |
| 11 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 불가 | — | 0 | Product Attribute Set Instance |
| 12 | `isallocated` | Allocated | character(1) | 불가 | — | 'N'::bpchar | Indicates if the payment has been allocated |
| 13 | `qty` | Quantity | numeric | 불가 | — | 0 | Quantity |
| 14 | `ismanual` | Manual | character(1) | 불가 | — | 'N'::bpchar | This is a manual process |
| 15 | `m_inoutline_id` | Shipment/Receipt Line | numeric(10,0) | 허용 | — | — | Line on Shipment or Receipt document |
| 16 | `m_productionline_id` | Production Line | numeric(10,0) | 허용 | — | — | Document Line representing a production |
| 17 | `m_inventoryline_id` | Phys.Inventory Line | numeric(10,0) | 허용 | — | — | Unique line in an Inventory document |
| 18 | `out_m_transaction_id` | Out Transaction | numeric(10,0) | 허용 | — | — | Outgoing Transaction |
| 19 | `out_m_inoutline_id` | Out Shipment Line | numeric(10,0) | 허용 | — | — | Outgoing Shipment/Receipt |
| 20 | `out_m_productionline_id` | Out Production Line | numeric(10,0) | 허용 | — | — | Outgoing Production Line |
| 21 | `out_m_inventoryline_id` | Out Inventory Line | numeric(10,0) | 허용 | — | — | Outgoing Inventory Line |
| 22 | `m_transactionallocation_uu` | M_TransactionAllocation_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 10개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["m_attributesetinstance"]
    n1["m_inoutline"]
    n2["m_inventoryline"]
    n3["m_product"]
    n4["m_productionline"]
    n5["m_transaction"]
    n6["m_transactionallocation"]
    n6 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n0
    n6 -->|"m_inoutline_id → m_inoutline_id"| n1
    n6 -->|"out_m_inoutline_id → m_inoutline_id"| n1
    n6 -->|"m_inventoryline_id → m_inventoryline_id"| n2
    n6 -->|"out_m_inventoryline_id → m_inventoryline_id"| n2
    n6 -->|"m_product_id → m_product_id"| n3
    n6 -->|"m_productionline_id → m_productionline_id"| n4
    n6 -->|"out_m_productionline_id → m_productionline_id"| n4
    n6 -->|"out_m_transaction_id → m_transaction_id"| n5
    n6 -->|"m_transaction_id → m_transaction_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mattributesetinst_mtrxalloc` <!-- FK_OUT: adempiere.m_transactionallocation.mattributesetinst_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minoutline_mtrxalloc` <!-- FK_OUT: adempiere.m_transactionallocation.minoutline_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `m_inoutline_id` | [`m_inoutline`](m_inoutline.md) | `m_inoutline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minoutlineout_mtrxalloc` <!-- FK_OUT: adempiere.m_transactionallocation.minoutlineout_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `out_m_inoutline_id` | [`m_inoutline`](m_inoutline.md) | `m_inoutline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventoryline_mtrxalloc` <!-- FK_OUT: adempiere.m_transactionallocation.minventoryline_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventorylineout_mtrxalloc` <!-- FK_OUT: adempiere.m_transactionallocation.minventorylineout_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `out_m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mtrxalloc` <!-- FK_OUT: adempiere.m_transactionallocation.mproduct_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductionline_mtrxalloc` <!-- FK_OUT: adempiere.m_transactionallocation.mproductionline_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `m_productionline_id` | [`m_productionline`](m_productionline.md) | `m_productionline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductionlineout_mtrxalloc` <!-- FK_OUT: adempiere.m_transactionallocation.mproductionlineout_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `out_m_productionline_id` | [`m_productionline`](m_productionline.md) | `m_productionline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mtransactionout_mtrxalloc` <!-- FK_OUT: adempiere.m_transactionallocation.mtransactionout_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `out_m_transaction_id` | [`m_transaction`](m_transaction.md) | `m_transaction_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mttransaction_mtrxalloc` <!-- FK_OUT: adempiere.m_transactionallocation.mttransaction_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `m_transaction_id` | [`m_transaction`](m_transaction.md) | `m_transaction_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
