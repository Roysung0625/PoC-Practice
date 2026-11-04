# m_inout — 출하·입고 문서

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_inout` |
| 한국어 논리명(문서용 해석) | 출하·입고 문서 |
| 원본 논리명 | Shipment/Receipt |
| 원본 사전 ID | 319 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 9 |
| 물리 열 수 | 80 |
| 나가는 FK / 들어오는 FK | 28 / 10 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제품의 고객 출하 또는 공급업체 입고를 기록하는 자재 이동 문서의 헤더다. 출하와 입고를 모두 포함하므로 조회 시 거래 방향을 구분해야 한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Material Shipment Document
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_inout_pkey` | `m_inout_id` |
| UNIQUE | `m_inout_uu_idx` | `m_inout_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_inout_id` | Shipment/Receipt | numeric(10,0) | 불가 | 예 | — | Material Shipment Document |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `issotrx` | Sales Transaction | character(1) | 불가 | — | 'Y'::bpchar | This is a Sales Transaction |
| 10 | `documentno` | Document No | character varying(30) | 불가 | — | — | Document sequence number of the document |
| 11 | `docaction` | Document Action | character(2) | 불가 | — | — | The targeted status of the document |
| 12 | `docstatus` | Document Status | character(2) | 불가 | — | — | The current status of the document |
| 13 | `posted` | Posted | character(1) | 불가 | — | 'N'::bpchar | Posting status |
| 14 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 15 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 16 | `c_doctype_id` | Document Type | numeric(10,0) | 불가 | — | — | Document type or rules |
| 17 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 18 | `c_order_id` | Order | numeric(10,0) | 허용 | — | — | Order |
| 19 | `dateordered` | Date Ordered | timestamp without time zone | 허용 | — | — | Date of Order |
| 20 | `isprinted` | Printed | character(1) | 불가 | — | 'N'::bpchar | Indicates if this document / line is printed |
| 21 | `movementtype` | Movement Type | character(2) | 불가 | — | — | Method of moving the inventory |
| 22 | `movementdate` | Movement Date | timestamp without time zone | 불가 | — | — | Date a product was moved in or out of inventory |
| 23 | `dateacct` | Account Date | timestamp without time zone | 불가 | — | — | Accounting Date |
| 24 | `c_bpartner_id` | Business Partner | numeric(10,0) | 불가 | — | — | Identifies a Business Partner |
| 25 | `c_bpartner_location_id` | Partner Location | numeric(10,0) | 불가 | — | — | Identifies the (ship to) address for this Business Partner |
| 26 | `m_warehouse_id` | Warehouse | numeric(10,0) | 불가 | — | — | Storage Warehouse and Service Point |
| 27 | `poreference` | Order Reference | character varying(20) | 허용 | — | — | Transaction Reference Number (Sales Order, Purchase Order) of your Business Partner |
| 28 | `deliveryrule` | Delivery Rule | character(1) | 불가 | — | — | Defines the timing of Delivery |
| 29 | `freightcostrule` | Freight Cost Rule | character(1) | 불가 | — | — | Method for charging Freight |
| 30 | `freightamt` | Freight Amount | numeric | 허용 | — | 0 | Freight Amount  |
| 31 | `deliveryviarule` | Delivery Via | character(1) | 불가 | — | — | How the order will be delivered |
| 32 | `m_shipper_id` | Shipper | numeric(10,0) | 허용 | — | — | Method or manner of product delivery |
| 33 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | — | Additional document charges |
| 34 | `chargeamt` | Charge amount | numeric | 허용 | — | 0 | Charge Amount |
| 35 | `priorityrule` | Priority | character(1) | 불가 | — | — | Priority of a document |
| 36 | `dateprinted` | Date Printed | timestamp without time zone | 허용 | — | — | Date the document was printed. |
| 37 | `c_invoice_id` | Invoice | numeric(10,0) | 허용 | — | — | Invoice Identifier |
| 38 | `createfrom` | Create lines from | character(1) | 허용 | — | — | Process which will generate a new document lines based on an existing document |
| 39 | `generateto` | Generate To | character(1) | 허용 | — | — | Generate To |
| 40 | `sendemail` | Send EMail | character(1) | 불가 | — | 'N'::bpchar | Enable sending Document EMail |
| 41 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | — | User within the system - Internal or Business Partner Contact |
| 42 | `salesrep_id` | Sales Representative | numeric(10,0) | 허용 | — | — | Sales Representative or Company Agent |
| 43 | `nopackages` | No Packages | numeric(10,0) | 허용 | — | (1)::numeric | Number of packages shipped |
| 44 | `pickdate` | Pick Date | timestamp without time zone | 허용 | — | — | Date/Time when picked for Shipment |
| 45 | `shipdate` | Ship Date | timestamp without time zone | 허용 | — | — | Shipment Date/Time |
| 46 | `trackingno` | Tracking No | character varying(60) | 허용 | — | — | Number to track the shipment |
| 47 | `ad_orgtrx_id` | Trx Organization | numeric(10,0) | 허용 | — | — | Performing or initiating organization |
| 48 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 49 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | — | Marketing Campaign |
| 50 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 51 | `user1_id` | User Element List 1 | numeric(10,0) | 허용 | — | — | User defined list element #1 |
| 52 | `user2_id` | User Element List 2 | numeric(10,0) | 허용 | — | — | User defined list element #2 |
| 53 | `datereceived` | Date Received | timestamp without time zone | 허용 | — | — | Date a product was received |
| 54 | `isintransit` | In Transit | character(1) | 불가 | — | 'N'::bpchar | Movement is in transit |
| 55 | `ref_inout_id` | Referenced Shipment | numeric(10,0) | 허용 | — | — | — |
| 56 | `createconfirm` | Create Confirm | character(1) | 허용 | — | — | — |
| 57 | `createpackage` | Create Package | character(1) | 허용 | — | — | — |
| 58 | `isapproved` | Approved | character(1) | 불가 | — | 'N'::bpchar | Indicates if this document requires approval |
| 59 | `isindispute` | In Dispute | character(1) | 불가 | — | 'N'::bpchar | Document is in dispute |
| 60 | `volume` | Volume | numeric | 허용 | — | — | Volume of a product |
| 61 | `weight` | Weight | numeric | 허용 | — | — | Weight of a product |
| 62 | `m_rma_id` | RMA | numeric(10,0) | 허용 | — | — | Return Material Authorization |
| 63 | `reversal_id` | Reversal ID | numeric(10,0) | 허용 | — | — | ID of document reversal |
| 64 | `isdropship` | Drop Shipment | character(1) | 허용 | — | 'N'::bpchar | Drop Shipments are sent directly to the Drop Shipment Location |
| 65 | `dropship_bpartner_id` | Drop Ship Business Partner | numeric(10,0) | 허용 | — | — | Business Partner to ship to |
| 66 | `dropship_location_id` | Drop Shipment Location | numeric(10,0) | 허용 | — | — | Business Partner Location for shipping to |
| 67 | `dropship_user_id` | Drop Shipment Contact | numeric(10,0) | 허용 | — | — | Business Partner Contact for drop shipment |
| 68 | `processedon` | Processed On | numeric | 허용 | — | — | The date+time (expressed in decimal format) when the document has been processed |
| 69 | `m_inout_uu` | M_InOut_UU | uuid | 허용 | — | — | — |
| 70 | `freightcharges` | Freight Charges | character varying(10) | 허용 | — | NULL::character varying | — |
| 71 | `shipperaccount` | Shipper Account Number | character varying(40) | 허용 | — | NULL::character varying | — |
| 72 | `insurance` | Insurance | character(1) | 허용 | — | NULL::bpchar | — |
| 73 | `fob` | Freight Terms | character varying(10) | 허용 | — | NULL::character varying | — |
| 74 | `isalternatereturnaddress` | Alternate Return Address | character(1) | 불가 | — | 'N'::bpchar | — |
| 75 | `returnbpartner_id` | Return Partner | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 76 | `returnlocation_id` | Return Location | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 77 | `returnuser_id` | Return User/Contact | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 78 | `createlinesfrom` | Create lines from | character(1) | 허용 | — | NULL::bpchar | Process which will generate a new document lines based on an existing document |
| 79 | `c_costcenter_id` | Cost Center | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 80 | `c_department_id` | Department | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 36개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_org"]
    n1["ad_user"]
    n2["c_activity"]
    n3["c_bpartner"]
    n4["c_campaign"]
    n5["c_charge"]
    n6["c_costcenter"]
    n7["c_department"]
    n8["m_inout"]
    n8 -->|"ad_org_id → ad_org_id"| n0
    n8 -->|"ad_orgtrx_id → ad_org_id"| n0
    n8 -->|"ad_user_id → ad_user_id"| n1
    n8 -->|"salesrep_id → ad_user_id"| n1
    n8 -->|"c_activity_id → c_activity_id"| n2
    n8 -->|"c_bpartner_id → c_bpartner_id"| n3
    n8 -->|"c_campaign_id → c_campaign_id"| n4
    n8 -->|"c_charge_id → c_charge_id"| n5
    n8 -->|"c_costcenter_id → c_costcenter_id"| n6
    n8 -->|"c_department_id → c_department_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adorg_minout` <!-- FK_OUT: adempiere.m_inout.adorg_minout --> | [`m_inout`](m_inout.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorgtrx_minout` <!-- FK_OUT: adempiere.m_inout.adorgtrx_minout --> | [`m_inout`](m_inout.md) | `ad_orgtrx_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduser_minout` <!-- FK_OUT: adempiere.m_inout.aduser_minout --> | [`m_inout`](m_inout.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduser_sr_minout` <!-- FK_OUT: adempiere.m_inout.aduser_sr_minout --> | [`m_inout`](m_inout.md) | `salesrep_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_minout` <!-- FK_OUT: adempiere.m_inout.cactivity_minout --> | [`m_inout`](m_inout.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_minout` <!-- FK_OUT: adempiere.m_inout.cbpartner_minout --> | [`m_inout`](m_inout.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccampaign_minout` <!-- FK_OUT: adempiere.m_inout.ccampaign_minout --> | [`m_inout`](m_inout.md) | `c_campaign_id` | [`c_campaign`](../c/c_campaign.md) | `c_campaign_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccharge_minout` <!-- FK_OUT: adempiere.m_inout.ccharge_minout --> | [`m_inout`](m_inout.md) | `c_charge_id` | [`c_charge`](../c/c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccostcenter_minout` <!-- FK_OUT: adempiere.m_inout.ccostcenter_minout --> | [`m_inout`](m_inout.md) | `c_costcenter_id` | [`c_costcenter`](../c/c_costcenter.md) | `c_costcenter_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdepartment_minout` <!-- FK_OUT: adempiere.m_inout.cdepartment_minout --> | [`m_inout`](m_inout.md) | `c_department_id` | [`c_department`](../c/c_department.md) | `c_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_minout` <!-- FK_OUT: adempiere.m_inout.cdoctype_minout --> | [`m_inout`](m_inout.md) | `c_doctype_id` | [`c_doctype`](../c/c_doctype.md) | `c_doctype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalueuser1_minout` <!-- FK_OUT: adempiere.m_inout.celementvalueuser1_minout --> | [`m_inout`](m_inout.md) | `user1_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalueuser2_minout` <!-- FK_OUT: adempiere.m_inout.celementvalueuser2_minout --> | [`m_inout`](m_inout.md) | `user2_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoice_minout` <!-- FK_OUT: adempiere.m_inout.cinvoice_minout --> | [`m_inout`](m_inout.md) | `c_invoice_id` | [`c_invoice`](../c/c_invoice.md) | `c_invoice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `corder_minout` <!-- FK_OUT: adempiere.m_inout.corder_minout --> | [`m_inout`](m_inout.md) | `c_order_id` | [`c_order`](../c/c_order.md) | `c_order_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_minout` <!-- FK_OUT: adempiere.m_inout.cproject_minout --> | [`m_inout`](m_inout.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `dropshipbpartner_minout` <!-- FK_OUT: adempiere.m_inout.dropshipbpartner_minout --> | [`m_inout`](m_inout.md) | `dropship_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `dropshiplocation_minout` <!-- FK_OUT: adempiere.m_inout.dropshiplocation_minout --> | [`m_inout`](m_inout.md) | `dropship_location_id` | [`c_bpartner_location`](../c/c_bpartner_location.md) | `c_bpartner_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `dropshipuser_minout` <!-- FK_OUT: adempiere.m_inout.dropshipuser_minout --> | [`m_inout`](m_inout.md) | `dropship_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_ref` <!-- FK_OUT: adempiere.m_inout.minout_ref --> | [`m_inout`](m_inout.md) | `ref_inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mrma_minout` <!-- FK_OUT: adempiere.m_inout.mrma_minout --> | [`m_inout`](m_inout.md) | `m_rma_id` | [`m_rma`](m_rma.md) | `m_rma_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_minout` <!-- FK_OUT: adempiere.m_inout.mshipper_minout --> | [`m_inout`](m_inout.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_minout` <!-- FK_OUT: adempiere.m_inout.mwarehouse_minout --> | [`m_inout`](m_inout.md) | `m_warehouse_id` | [`m_warehouse`](m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `returnbpartner_minout` <!-- FK_OUT: adempiere.m_inout.returnbpartner_minout --> | [`m_inout`](m_inout.md) | `returnbpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `returnlocation_minout` <!-- FK_OUT: adempiere.m_inout.returnlocation_minout --> | [`m_inout`](m_inout.md) | `returnlocation_id` | [`c_bpartner_location`](../c/c_bpartner_location.md) | `c_bpartner_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `returnuser_minout` <!-- FK_OUT: adempiere.m_inout.returnuser_minout --> | [`m_inout`](m_inout.md) | `returnuser_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversal_minout` <!-- FK_OUT: adempiere.m_inout.reversal_minout --> | [`m_inout`](m_inout.md) | `reversal_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vbplocation_minout` <!-- FK_OUT: adempiere.m_inout.vbplocation_minout --> | [`m_inout`](m_inout.md) | `c_bpartner_location_id` | [`c_bpartner_location`](../c/c_bpartner_location.md) | `c_bpartner_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `minout_clandedcost` <!-- FK_IN: adempiere.c_landedcost.minout_clandedcost --> | [`c_landedcost`](../c/c_landedcost.md) | `m_inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_ref` <!-- FK_IN: adempiere.m_inout.minout_ref --> | [`m_inout`](m_inout.md) | `ref_inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversal_minout` <!-- FK_IN: adempiere.m_inout.reversal_minout --> | [`m_inout`](m_inout.md) | `reversal_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_minoutconfirm` <!-- FK_IN: adempiere.m_inoutconfirm.minout_minoutconfirm --> | [`m_inoutconfirm`](m_inoutconfirm.md) | `m_inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_minoutline` <!-- FK_IN: adempiere.m_inoutline.minout_minoutline --> | [`m_inoutline`](m_inoutline.md) | `m_inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_mpackage` <!-- FK_IN: adempiere.m_package.minout_mpackage --> | [`m_package`](m_package.md) | `m_inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_mrma` <!-- FK_IN: adempiere.m_rma.minout_mrma --> | [`m_rma`](m_rma.md) | `inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_mshippingtransaction` <!-- FK_IN: adempiere.m_shippingtransaction.minout_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_rrequest` <!-- FK_IN: adempiere.r_request.minout_rrequest --> | [`r_request`](../r/r_request.md) | `m_inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_mrequestaction` <!-- FK_IN: adempiere.r_requestaction.minout_mrequestaction --> | [`r_requestaction`](../r/r_requestaction.md) | `m_inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `issotrx`가 있습니다. 판매(`Y`)와 구매(`N`)를 구분해서 분석합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
