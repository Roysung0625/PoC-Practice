# c_projectphase — 프로젝트 단계

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_projectphase` |
| 한국어 논리명(문서용 해석) | 프로젝트 단계 |
| 원본 논리명 | Project Phase |
| 원본 사전 ID | 576 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 27 |
| 나가는 FK / 들어오는 FK | 4 / 11 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

개별 프로젝트에 실제로 적용되는 단계를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Phase of a Project
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_projectphase_pkey` | `c_projectphase_id` |
| UNIQUE | `c_projectphase_uu_idx` | `c_projectphase_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_project_id` | Project | numeric(10,0) | 불가 | — | — | Financial Project |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 10 | `startdate` | Start Date | timestamp without time zone | 허용 | — | — | First effective day (inclusive) |
| 11 | `enddate` | End Date | timestamp without time zone | 허용 | — | — | Last effective date (inclusive) |
| 12 | `iscomplete` | Complete | character(1) | 불가 | — | 'N'::bpchar | It is complete |
| 13 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 14 | `priceactual` | Unit Price | numeric | 허용 | — | 0 | Actual Price  |
| 15 | `generateorder` | Generate Order | character(1) | 허용 | — | — | Generate Order |
| 16 | `c_order_id` | Order | numeric(10,0) | 허용 | — | — | Order |
| 17 | `c_phase_id` | Standard Phase | numeric(10,0) | 허용 | — | — | Standard Phase of the Project Type |
| 18 | `c_projectphase_id` | Project Phase | numeric(10,0) | 불가 | 예 | — | Phase of a Project |
| 19 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 20 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 21 | `qty` | Quantity | numeric | 허용 | — | 0 | Quantity |
| 22 | `seqno` | Sequence | numeric(10,0) | 불가 | — | — | Method of ordering records; lowest number comes first |
| 23 | `committedamt` | Committed Amount | numeric | 불가 | — | 0 | The (legal) commitment amount |
| 24 | `iscommitceiling` | Commitment is Ceiling | character(1) | 불가 | — | 'N'::bpchar | The commitment amount/quantity is the chargeable ceiling  |
| 25 | `projinvoicerule` | Invoice Rule | character(1) | 허용 | — | — | Invoice Rule for the project |
| 26 | `plannedamt` | Planned Amount | numeric | 불가 | — | 0 | Planned amount for this project |
| 27 | `c_projectphase_uu` | C_ProjectPhase_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 15개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_cashplanline"]
    n1["c_invoiceline"]
    n2["c_order"]
    n3["c_orderline"]
    n4["c_phase"]
    n5["c_project"]
    n6["c_projectline"]
    n7["c_projectphase"]
    n8["c_projecttask"]
    n9["fact_acct"]
    n10["m_product"]
    n7 -->|"c_order_id → c_order_id"| n2
    n7 -->|"c_phase_id → c_phase_id"| n4
    n7 -->|"c_project_id → c_project_id"| n5
    n7 -->|"m_product_id → m_product_id"| n10
    n0 -->|"c_projectphase_id → c_projectphase_id"| n7
    n1 -->|"c_projectphase_id → c_projectphase_id"| n7
    n3 -->|"c_projectphase_id → c_projectphase_id"| n7
    n6 -->|"c_projectphase_id → c_projectphase_id"| n7
    n8 -->|"c_projectphase_id → c_projectphase_id"| n7
    n9 -->|"c_projectphase_id → c_projectphase_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `corder_cprojectphase` <!-- FK_OUT: adempiere.c_projectphase.corder_cprojectphase --> | [`c_projectphase`](c_projectphase.md) | `c_order_id` | [`c_order`](c_order.md) | `c_order_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cphase_cprojectphase` <!-- FK_OUT: adempiere.c_projectphase.cphase_cprojectphase --> | [`c_projectphase`](c_projectphase.md) | `c_phase_id` | [`c_phase`](c_phase.md) | `c_phase_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_cprojectphase` <!-- FK_OUT: adempiere.c_projectphase.cproject_cprojectphase --> | [`c_projectphase`](c_projectphase.md) | `c_project_id` | [`c_project`](c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_cprojectphase` <!-- FK_OUT: adempiere.c_projectphase.mproduct_cprojectphase --> | [`c_projectphase`](c_projectphase.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cprojectphase_ccashplanline` <!-- FK_IN: adempiere.c_cashplanline.cprojectphase_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_cinvoiceline` <!-- FK_IN: adempiere.c_invoiceline.cprojectphase_cinvoiceline --> | [`c_invoiceline`](c_invoiceline.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_corderline` <!-- FK_IN: adempiere.c_orderline.cprojectphase_corderline --> | [`c_orderline`](c_orderline.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_cprojectline` <!-- FK_IN: adempiere.c_projectline.cprojectphase_cprojectline --> | [`c_projectline`](c_projectline.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_cprojecttask` <!-- FK_IN: adempiere.c_projecttask.cprojectphase_cprojecttask --> | [`c_projecttask`](c_projecttask.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_factacct` <!-- FK_IN: adempiere.fact_acct.cprojectphase_factacct --> | [`fact_acct`](../fact/fact_acct.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_factacctsummary` <!-- FK_IN: adempiere.fact_acct_summary.cprojectphase_factacctsummary --> | [`fact_acct_summary`](../fact/fact_acct_summary.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_hrmovement` <!-- FK_IN: adempiere.hr_movement.cprojectphase_hrmovement --> | [`hr_movement`](../hr/hr_movement.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_projectphase_minoutline` <!-- FK_IN: adempiere.m_inoutline.c_projectphase_minoutline --> | [`m_inoutline`](../m/m_inoutline.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_mproduction` <!-- FK_IN: adempiere.m_production.cprojectphase_mproduction --> | [`m_production`](../m/m_production.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_stimeexpenseline` <!-- FK_IN: adempiere.s_timeexpenseline.cprojectphase_stimeexpenseline --> | [`s_timeexpenseline`](../s/s_timeexpenseline.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
