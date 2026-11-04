# c_projectline — 프로젝트 명세

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_projectline` |
| 한국어 논리명(문서용 해석) | 프로젝트 명세 |
| 원본 논리명 | Project Line |
| 원본 사전 ID | 434 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 31 |
| 나가는 FK / 들어오는 FK | 9 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

프로젝트의 과업 또는 수행 단계를 명세 행으로 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Task or step in a project
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_projectline_pkey` | `c_projectline_id` |
| UNIQUE | `c_projectline_uu_idx` | `c_projectline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_projectline_id` | Project Line | numeric(10,0) | 불가 | 예 | — | Task or step in a project |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_project_id` | Project | numeric(10,0) | 불가 | — | — | Financial Project |
| 10 | `line` | Line No | numeric(10,0) | 불가 | — | — | Unique line for this document |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `plannedqty` | Planned Quantity | numeric | 불가 | — | 0 | Planned quantity for this project |
| 13 | `plannedprice` | Planned Price | numeric | 불가 | — | 0 | Planned price for this project line |
| 14 | `plannedamt` | Planned Amount | numeric | 불가 | — | 0 | Planned amount for this project |
| 15 | `plannedmarginamt` | Planned Margin | numeric | 불가 | — | 0 | Project's planned margin amount |
| 16 | `committedamt` | Committed Amount | numeric | 허용 | — | 0 | The (legal) commitment amount |
| 17 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 18 | `m_product_category_id` | Product Category | numeric(10,0) | 허용 | — | — | Category of a Product |
| 19 | `invoicedamt` | Invoiced Amount | numeric | 불가 | — | 0 | The amount invoiced |
| 20 | `invoicedqty` | Quantity Invoiced | numeric | 불가 | — | 0 | The quantity invoiced |
| 21 | `committedqty` | Committed Quantity | numeric | 허용 | — | 0 | The (legal) commitment Quantity |
| 22 | `c_projectissue_id` | Project Issue | numeric(10,0) | 허용 | — | — | Project Issues (Material, Labor) |
| 23 | `c_order_id` | Order | numeric(10,0) | 허용 | — | — | Order |
| 24 | `c_orderpo_id` | Purchase Order | numeric(10,0) | 허용 | — | — | Purchase Order |
| 25 | `isprinted` | Printed | character(1) | 불가 | — | 'Y'::bpchar | Indicates if this document / line is printed |
| 26 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 27 | `dopricing` | Pricing | character(1) | 허용 | — | 'Y'::bpchar | — |
| 28 | `c_projectphase_id` | Project Phase | numeric(10,0) | 허용 | — | — | Phase of a Project |
| 29 | `c_projecttask_id` | Project Task | numeric(10,0) | 허용 | — | — | Actual Project Task in a Phase |
| 30 | `c_projectline_uu` | C_ProjectLine_UU | uuid | 허용 | — | — | — |
| 31 | `m_production_id` | Production | numeric(10,0) | 허용 | — | NULL::numeric | Plan for producing a product |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 9개 중 9개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_order"]
    n1["c_project"]
    n2["c_projectissue"]
    n3["c_projectline"]
    n4["c_projectphase"]
    n5["c_projecttask"]
    n6["m_product"]
    n7["m_product_category"]
    n8["m_production"]
    n3 -->|"c_order_id → c_order_id"| n0
    n3 -->|"c_orderpo_id → c_order_id"| n0
    n3 -->|"c_project_id → c_project_id"| n1
    n3 -->|"c_projectissue_id → c_projectissue_id"| n2
    n3 -->|"c_projectphase_id → c_projectphase_id"| n4
    n3 -->|"c_projecttask_id → c_projecttask_id"| n5
    n3 -->|"m_product_id → m_product_id"| n6
    n3 -->|"m_product_category_id → m_product_category_id"| n7
    n3 -->|"m_production_id → m_production_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `corder_cprojectline` <!-- FK_OUT: adempiere.c_projectline.corder_cprojectline --> | [`c_projectline`](c_projectline.md) | `c_order_id` | [`c_order`](c_order.md) | `c_order_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `corderpo_cprojectline` <!-- FK_OUT: adempiere.c_projectline.corderpo_cprojectline --> | [`c_projectline`](c_projectline.md) | `c_orderpo_id` | [`c_order`](c_order.md) | `c_order_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_cprojectline` <!-- FK_OUT: adempiere.c_projectline.cproject_cprojectline --> | [`c_projectline`](c_projectline.md) | `c_project_id` | [`c_project`](c_project.md) | `c_project_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectissue_cprojectline` <!-- FK_OUT: adempiere.c_projectline.cprojectissue_cprojectline --> | [`c_projectline`](c_projectline.md) | `c_projectissue_id` | [`c_projectissue`](c_projectissue.md) | `c_projectissue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_cprojectline` <!-- FK_OUT: adempiere.c_projectline.cprojectphase_cprojectline --> | [`c_projectline`](c_projectline.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojecttask_cprojectline` <!-- FK_OUT: adempiere.c_projectline.cprojecttask_cprojectline --> | [`c_projectline`](c_projectline.md) | `c_projecttask_id` | [`c_projecttask`](c_projecttask.md) | `c_projecttask_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_cprojectline` <!-- FK_OUT: adempiere.c_projectline.mproduct_cprojectline --> | [`c_projectline`](c_projectline.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductcat_cprojectline` <!-- FK_OUT: adempiere.c_projectline.mproductcat_cprojectline --> | [`c_projectline`](c_projectline.md) | `m_product_category_id` | [`m_product_category`](../m/m_product_category.md) | `m_product_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduction_cprojectline` <!-- FK_OUT: adempiere.c_projectline.mproduction_cprojectline --> | [`c_projectline`](c_projectline.md) | `m_production_id` | [`m_production`](../m/m_production.md) | `m_production_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
