# m_productionline — 생산행

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_productionline` |
| 한국어 논리명(문서용 해석) | 생산행 |
| 원본 논리명 | Production Line |
| 원본 사전 ID | 326 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 23 |
| 나가는 FK / 들어오는 FK | 7 / 6 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

생산 문서에서 발생하는 개별 자재 내역을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Document Line representing a production
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_productionline_pkey` | `m_productionline_id` |
| UNIQUE | `m_productionline_uu_idx` | `m_productionline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_productionline_id` | Production Line | numeric(10,0) | 불가 | 예 | — | Document Line representing a production |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `m_productionplan_id` | Production Plan | numeric(10,0) | 허용 | — | — | Plan for how a product is produced |
| 10 | `line` | Line No | numeric(10,0) | 불가 | — | — | Unique line for this document |
| 11 | `m_product_id` | Product | numeric(10,0) | 불가 | — | — | Product, Service, Item |
| 12 | `movementqty` | Movement Quantity | numeric | 불가 | — | 0 | Quantity of a product moved. |
| 13 | `m_locator_id` | Locator | numeric(10,0) | 불가 | — | — | Warehouse Locator |
| 14 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 15 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 허용 | — | 0 | Product Attribute Set Instance |
| 16 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 17 | `m_productionline_uu` | M_ProductionLine_UU | uuid | 허용 | — | — | — |
| 18 | `m_production_id` | Production | numeric(10,0) | 허용 | — | — | Plan for producing a product |
| 19 | `plannedqty` | Planned Quantity | numeric | 허용 | — | — | Planned quantity for this project |
| 20 | `qtyused` | Quantity Used | numeric | 허용 | — | — | — |
| 21 | `isendproduct` | End Product | character(1) | 허용 | — | NULL::bpchar | End Product of production |
| 22 | `c_costcenter_id` | Cost Center | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 23 | `c_department_id` | Department | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 13개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_costcenter"]
    n1["c_department"]
    n2["m_attributesetinstance"]
    n3["m_costdetail"]
    n4["m_locator"]
    n5["m_product"]
    n6["m_production"]
    n7["m_productionline"]
    n8["m_productionlinema"]
    n9["m_productionplan"]
    n10["m_transaction"]
    n7 -->|"c_costcenter_id → c_costcenter_id"| n0
    n7 -->|"c_department_id → c_department_id"| n1
    n7 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n2
    n7 -->|"m_locator_id → m_locator_id"| n4
    n7 -->|"m_product_id → m_product_id"| n5
    n7 -->|"m_production_id → m_production_id"| n6
    n7 -->|"m_productionplan_id → m_productionplan_id"| n9
    n3 -->|"m_productionline_id → m_productionline_id"| n7
    n8 -->|"m_productionline_id → m_productionline_id"| n7
    n10 -->|"m_productionline_id → m_productionline_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccostcenter_mproductionline` <!-- FK_OUT: adempiere.m_productionline.ccostcenter_mproductionline --> | [`m_productionline`](m_productionline.md) | `c_costcenter_id` | [`c_costcenter`](../c/c_costcenter.md) | `c_costcenter_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdepartment_mproductionline` <!-- FK_OUT: adempiere.m_productionline.cdepartment_mproductionline --> | [`m_productionline`](m_productionline.md) | `c_department_id` | [`c_department`](../c/c_department.md) | `c_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattrsetinst_mproductionline` <!-- FK_OUT: adempiere.m_productionline.mattrsetinst_mproductionline --> | [`m_productionline`](m_productionline.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mlocator_mproductionline` <!-- FK_OUT: adempiere.m_productionline.mlocator_mproductionline --> | [`m_productionline`](m_productionline.md) | `m_locator_id` | [`m_locator`](m_locator.md) | `m_locator_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mproductionline` <!-- FK_OUT: adempiere.m_productionline.mproduct_mproductionline --> | [`m_productionline`](m_productionline.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduction_mproductionline` <!-- FK_OUT: adempiere.m_productionline.mproduction_mproductionline --> | [`m_productionline`](m_productionline.md) | `m_production_id` | [`m_production`](m_production.md) | `m_production_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductionplan_line` <!-- FK_OUT: adempiere.m_productionline.mproductionplan_line --> | [`m_productionline`](m_productionline.md) | `m_productionplan_id` | [`m_productionplan`](m_productionplan.md) | `m_productionplan_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mproductionline_mcostdetail` <!-- FK_IN: adempiere.m_costdetail.mproductionline_mcostdetail --> | [`m_costdetail`](m_costdetail.md) | `m_productionline_id` | [`m_productionline`](m_productionline.md) | `m_productionline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductionline_mplinema` <!-- FK_IN: adempiere.m_productionlinema.mproductionline_mplinema --> | [`m_productionlinema`](m_productionlinema.md) | `m_productionline_id` | [`m_productionline`](m_productionline.md) | `m_productionline_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductionline_mtransaction` <!-- FK_IN: adempiere.m_transaction.mproductionline_mtransaction --> | [`m_transaction`](m_transaction.md) | `m_productionline_id` | [`m_productionline`](m_productionline.md) | `m_productionline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductionline_mtrxalloc` <!-- FK_IN: adempiere.m_transactionallocation.mproductionline_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `m_productionline_id` | [`m_productionline`](m_productionline.md) | `m_productionline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductionlineout_mtrxalloc` <!-- FK_IN: adempiere.m_transactionallocation.mproductionlineout_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `out_m_productionline_id` | [`m_productionline`](m_productionline.md) | `m_productionline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductionline_ttransaction` <!-- FK_IN: adempiere.t_transaction.mproductionline_ttransaction --> | [`t_transaction`](../t/t_transaction.md) | `m_productionline_id` | [`m_productionline`](m_productionline.md) | `m_productionline_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
