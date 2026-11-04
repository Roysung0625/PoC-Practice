# m_inventory — 실사 재고 문서

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_inventory` |
| 한국어 논리명(문서용 해석) | 실사 재고 문서 |
| 원본 논리명 | Phys.Inventory |
| 원본 사전 ID | 321 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 3 |
| 물리 열 수 | 37 |
| 나가는 FK / 들어오는 FK | 15 / 5 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

실물 재고 실사를 위한 문서 및 매개변수를 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Parameters for a Physical Inventory
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_inventory_pkey` | `m_inventory_id` |
| UNIQUE | `m_inventory_uu_idx` | `m_inventory_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_inventory_id` | Phys.Inventory | numeric(10,0) | 불가 | 예 | — | Parameters for a Physical Inventory |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `documentno` | Document No | character varying(30) | 불가 | — | — | Document sequence number of the document |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `m_warehouse_id` | Warehouse | numeric(10,0) | 허용 | — | — | Storage Warehouse and Service Point |
| 12 | `movementdate` | Movement Date | timestamp without time zone | 불가 | — | — | Date a product was moved in or out of inventory |
| 13 | `posted` | Posted | character(1) | 불가 | — | 'N'::bpchar | Posting status |
| 14 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 15 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 16 | `updateqty` | Update Quantities | character(1) | 허용 | — | 'N'::bpchar | — |
| 17 | `generatelist` | Generate List | character(1) | 허용 | — | 'Y'::bpchar | Generate List |
| 18 | `m_perpetualinv_id` | Perpetual Inventory | numeric(10,0) | 허용 | — | — | Rules for generating physical inventory |
| 19 | `ad_orgtrx_id` | Trx Organization | numeric(10,0) | 허용 | — | — | Performing or initiating organization |
| 20 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 21 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | — | Marketing Campaign |
| 22 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 23 | `user1_id` | User Element List 1 | numeric(10,0) | 허용 | — | — | User defined list element #1 |
| 24 | `user2_id` | User Element List 2 | numeric(10,0) | 허용 | — | — | User defined list element #2 |
| 25 | `isapproved` | Approved | character(1) | 불가 | — | 'N'::bpchar | Indicates if this document requires approval |
| 26 | `docstatus` | Document Status | character(2) | 불가 | — | — | The current status of the document |
| 27 | `docaction` | Document Action | character(2) | 불가 | — | — | The targeted status of the document |
| 28 | `approvalamt` | Approval Amount | numeric | 허용 | — | — | Document Approval Amount |
| 29 | `c_doctype_id` | Document Type | numeric(10,0) | 불가 | — | — | Document type or rules |
| 30 | `reversal_id` | Reversal ID | numeric(10,0) | 허용 | — | — | ID of document reversal |
| 31 | `processedon` | Processed On | numeric | 허용 | — | — | The date+time (expressed in decimal format) when the document has been processed |
| 32 | `m_inventory_uu` | M_Inventory_UU | uuid | 허용 | — | — | — |
| 33 | `costingmethod` | Costing Method | character(1) | 허용 | — | NULL::bpchar | Indicates how Costs will be calculated |
| 34 | `c_conversiontype_id` | Currency Type | numeric(10,0) | 허용 | — | NULL::numeric | Currency Conversion Rate Type |
| 35 | `c_currency_id` | Currency | numeric(10,0) | 허용 | — | NULL::numeric | The Currency for this record |
| 36 | `c_costcenter_id` | Cost Center | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 37 | `c_department_id` | Department | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 19개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_org"]
    n1["c_activity"]
    n2["c_campaign"]
    n3["c_conversiontype"]
    n4["c_costcenter"]
    n5["c_currency"]
    n6["c_department"]
    n7["c_doctype"]
    n8["c_elementvalue"]
    n9["m_inventory"]
    n9 -->|"ad_org_id → ad_org_id"| n0
    n9 -->|"ad_orgtrx_id → ad_org_id"| n0
    n9 -->|"c_activity_id → c_activity_id"| n1
    n9 -->|"c_campaign_id → c_campaign_id"| n2
    n9 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n9 -->|"c_costcenter_id → c_costcenter_id"| n4
    n9 -->|"c_currency_id → c_currency_id"| n5
    n9 -->|"c_department_id → c_department_id"| n6
    n9 -->|"c_doctype_id → c_doctype_id"| n7
    n9 -->|"user1_id → c_elementvalue_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adorg_minventory` <!-- FK_OUT: adempiere.m_inventory.adorg_minventory --> | [`m_inventory`](m_inventory.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorgtrx_minventory` <!-- FK_OUT: adempiere.m_inventory.adorgtrx_minventory --> | [`m_inventory`](m_inventory.md) | `ad_orgtrx_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_minventory` <!-- FK_OUT: adempiere.m_inventory.cactivity_minventory --> | [`m_inventory`](m_inventory.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccampaign_minventory` <!-- FK_OUT: adempiere.m_inventory.ccampaign_minventory --> | [`m_inventory`](m_inventory.md) | `c_campaign_id` | [`c_campaign`](../c/c_campaign.md) | `c_campaign_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_minventory` <!-- FK_OUT: adempiere.m_inventory.cconversiontype_minventory --> | [`m_inventory`](m_inventory.md) | `c_conversiontype_id` | [`c_conversiontype`](../c/c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccostcenter_minventory` <!-- FK_OUT: adempiere.m_inventory.ccostcenter_minventory --> | [`m_inventory`](m_inventory.md) | `c_costcenter_id` | [`c_costcenter`](../c/c_costcenter.md) | `c_costcenter_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_minventory` <!-- FK_OUT: adempiere.m_inventory.ccurrency_minventory --> | [`m_inventory`](m_inventory.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdepartment_minventory` <!-- FK_OUT: adempiere.m_inventory.cdepartment_minventory --> | [`m_inventory`](m_inventory.md) | `c_department_id` | [`c_department`](../c/c_department.md) | `c_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_minventory` <!-- FK_OUT: adempiere.m_inventory.cdoctype_minventory --> | [`m_inventory`](m_inventory.md) | `c_doctype_id` | [`c_doctype`](../c/c_doctype.md) | `c_doctype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalueuser1_minvent` <!-- FK_OUT: adempiere.m_inventory.celementvalueuser1_minvent --> | [`m_inventory`](m_inventory.md) | `user1_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalueuser2_minvent` <!-- FK_OUT: adempiere.m_inventory.celementvalueuser2_minvent --> | [`m_inventory`](m_inventory.md) | `user2_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_minventory` <!-- FK_OUT: adempiere.m_inventory.cproject_minventory --> | [`m_inventory`](m_inventory.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mperpetualinv_minventory` <!-- FK_OUT: adempiere.m_inventory.mperpetualinv_minventory --> | [`m_inventory`](m_inventory.md) | `m_perpetualinv_id` | [`m_perpetualinv`](m_perpetualinv.md) | `m_perpetualinv_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_minventory` <!-- FK_OUT: adempiere.m_inventory.mwarehouse_minventory --> | [`m_inventory`](m_inventory.md) | `m_warehouse_id` | [`m_warehouse`](m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversal_minventory` <!-- FK_OUT: adempiere.m_inventory.reversal_minventory --> | [`m_inventory`](m_inventory.md) | `reversal_id` | [`m_inventory`](m_inventory.md) | `m_inventory_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `minventory_iinventory` <!-- FK_IN: adempiere.i_inventory.minventory_iinventory --> | [`i_inventory`](../i/i_inventory.md) | `m_inventory_id` | [`m_inventory`](m_inventory.md) | `m_inventory_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventory_minoutconfirm` <!-- FK_IN: adempiere.m_inoutconfirm.minventory_minoutconfirm --> | [`m_inoutconfirm`](m_inoutconfirm.md) | `m_inventory_id` | [`m_inventory`](m_inventory.md) | `m_inventory_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversal_minventory` <!-- FK_IN: adempiere.m_inventory.reversal_minventory --> | [`m_inventory`](m_inventory.md) | `reversal_id` | [`m_inventory`](m_inventory.md) | `m_inventory_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventory_minventoryline` <!-- FK_IN: adempiere.m_inventoryline.minventory_minventoryline --> | [`m_inventoryline`](m_inventoryline.md) | `m_inventory_id` | [`m_inventory`](m_inventory.md) | `m_inventory_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventory_mmovconfirm` <!-- FK_IN: adempiere.m_movementconfirm.minventory_mmovconfirm --> | [`m_movementconfirm`](m_movementconfirm.md) | `m_inventory_id` | [`m_inventory`](m_inventory.md) | `m_inventory_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
