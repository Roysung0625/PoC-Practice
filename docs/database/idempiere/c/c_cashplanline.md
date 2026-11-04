# c_cashplanline — 자금 계획 명세

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_cashplanline` |
| 한국어 논리명(문서용 해석) | 자금 계획 명세 |
| 원본 논리명 | Cash Plan Line |
| 원본 사전 ID | 53298 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 29 |
| 나가는 FK / 들어오는 FK | 12 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

자금 계획의 개별 예상 자금 내역을 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Cash Plan Line
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_cashplanline_key` | `c_cashplanline_id` |
| UNIQUE | `c_cashplanline_uu_idx` | `c_cashplanline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_orgtrx_id` | Trx Organization | numeric(10,0) | 허용 | — | NULL::numeric | Performing or initiating organization |
| 4 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | NULL::numeric | Business Activity |
| 5 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | NULL::numeric | Identifies a Business Partner |
| 6 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | NULL::numeric | Marketing Campaign |
| 7 | `c_cashplan_id` | Cash Plan | numeric(10,0) | 불가 | — | — | — |
| 8 | `c_cashplanline_id` | Cash Plan Line | numeric(10,0) | 불가 | 예 | — | — |
| 9 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | NULL::numeric | Additional document charges |
| 10 | `c_project_id` | Project | numeric(10,0) | 허용 | — | NULL::numeric | Financial Project |
| 11 | `c_projectphase_id` | Project Phase | numeric(10,0) | 허용 | — | NULL::numeric | Phase of a Project |
| 12 | `c_projecttask_id` | Project Task | numeric(10,0) | 허용 | — | NULL::numeric | Actual Project Task in a Phase |
| 13 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 14 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 15 | `datetrx` | Transaction Date | timestamp without time zone | 불가 | — | — | Transaction Date |
| 16 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 17 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 18 | `line` | Line No | numeric(10,0) | 불가 | — | — | Unique line for this document |
| 19 | `linetotalamt` | Line Total | numeric | 허용 | — | — | Total line amount incl. Tax |
| 20 | `m_product_id` | Product | numeric(10,0) | 허용 | — | NULL::numeric | Product, Service, Item |
| 21 | `name` | Name | character varying(60) | 허용 | — | NULL::character varying | Alphanumeric identifier of the entity |
| 22 | `probability` | Probability | numeric | 허용 | — | — | — |
| 23 | `processed` | Processed | character(1) | 불가 | — | — | The document has been processed |
| 24 | `qtyentered` | Quantity | numeric | 불가 | — | 1 | The Quantity Entered is based on the selected UoM |
| 25 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 26 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 27 | `user1_id` | User Element List 1 | numeric(10,0) | 허용 | — | NULL::numeric | User defined list element #1 |
| 28 | `user2_id` | User Element List 2 | numeric(10,0) | 허용 | — | NULL::numeric | User defined list element #2 |
| 29 | `c_cashplanline_uu` | C_CashPlanLine_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 14개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_org"]
    n1["c_activity"]
    n2["c_bpartner"]
    n3["c_campaign"]
    n4["c_cashplan"]
    n5["c_cashplanline"]
    n6["c_charge"]
    n7["c_project"]
    n8["c_projectphase"]
    n9["c_projecttask"]
    n10["m_product"]
    n5 -->|"ad_orgtrx_id → ad_org_id"| n0
    n5 -->|"c_activity_id → c_activity_id"| n1
    n5 -->|"c_bpartner_id → c_bpartner_id"| n2
    n5 -->|"c_campaign_id → c_campaign_id"| n3
    n5 -->|"c_cashplan_id → c_cashplan_id"| n4
    n5 -->|"c_charge_id → c_charge_id"| n6
    n5 -->|"c_project_id → c_project_id"| n7
    n5 -->|"c_projectphase_id → c_projectphase_id"| n8
    n5 -->|"c_projecttask_id → c_projecttask_id"| n9
    n5 -->|"m_product_id → m_product_id"| n10
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adorgtrx_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.adorgtrx_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `ad_orgtrx_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.cactivity_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `c_activity_id` | [`c_activity`](c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.cbpartner_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `c_bpartner_id` | [`c_bpartner`](c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccampaign_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.ccampaign_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `c_campaign_id` | [`c_campaign`](c_campaign.md) | `c_campaign_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccashplan_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.ccashplan_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `c_cashplan_id` | [`c_cashplan`](c_cashplan.md) | `c_cashplan_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccharge_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.ccharge_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `c_charge_id` | [`c_charge`](c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.cproject_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `c_project_id` | [`c_project`](c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.cprojectphase_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `c_projectphase_id` | [`c_projectphase`](c_projectphase.md) | `c_projectphase_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojecttask_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.cprojecttask_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `c_projecttask_id` | [`c_projecttask`](c_projecttask.md) | `c_projecttask_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.mproduct_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `user1_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.user1_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `user1_id` | [`c_elementvalue`](c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `user2_ccashplanline` <!-- FK_OUT: adempiere.c_cashplanline.user2_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `user2_id` | [`c_elementvalue`](c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccashplanline_cinvoice` <!-- FK_IN: adempiere.c_invoice.ccashplanline_cinvoice --> | [`c_invoice`](c_invoice.md) | `c_cashplanline_id` | [`c_cashplanline`](c_cashplanline.md) | `c_cashplanline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccashplanline_corder` <!-- FK_IN: adempiere.c_order.ccashplanline_corder --> | [`c_order`](c_order.md) | `c_cashplanline_id` | [`c_cashplanline`](c_cashplanline.md) | `c_cashplanline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
