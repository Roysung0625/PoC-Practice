# m_shippingtransaction — 배송 거래

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_shippingtransaction` |
| 한국어 논리명(문서용 해석) | 배송 거래 |
| 원본 논리명 | Shipping Transaction |
| 원본 사전 ID | 200051 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 89 |
| 나가는 FK / 들어오는 FK | 23 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

배송 서비스와 처리하는 배송 거래 정보를 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Shipping Transaction
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_shippingtransaction_key` | `m_shippingtransaction_id` |
| UNIQUE | `m_shippingtransaction_uu_idx` | `m_shippingtransaction_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `action` | Action | character varying(2) | 불가 | — | — | Indicates the Action to be performed |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `boxcount` | Box Count | numeric(10,0) | 허용 | — | 1 | — |
| 5 | `c_bp_shippingacct_id` | Business Partner Shipping Account | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 6 | `c_bpartner_location_id` | Partner Location | numeric(10,0) | 허용 | — | NULL::numeric | Identifies the (ship to) address for this Business Partner |
| 7 | `c_currency_id` | Currency | numeric(10,0) | 허용 | — | NULL::numeric | The Currency for this record |
| 8 | `c_order_id` | Order | numeric(10,0) | 허용 | — | NULL::numeric | Order |
| 9 | `c_uom_length_id` | UOM for Length | numeric(10,0) | 허용 | — | NULL::numeric | Standard Unit of Measure for Length |
| 10 | `c_uom_weight_id` | UOM for Weight | numeric(10,0) | 허용 | — | NULL::numeric | Standard Unit of Measure for Weight |
| 11 | `cashondelivery` | COD | character(1) | 불가 | — | 'N'::bpchar | — |
| 12 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 13 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 14 | `datereceived` | Date Received | timestamp without time zone | 허용 | — | — | Date a product was received |
| 15 | `deliveryconfirmation` | Delivery Confirmation | character(1) | 불가 | — | 'N'::bpchar | EMail Delivery confirmation |
| 16 | `deliveryconfirmationtype` | Delivery Confirmation Type | character varying(30) | 허용 | — | NULL::character varying | — |
| 17 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 18 | `dothazardclassordivision` | Dot Hazard Class or Division | character varying(30) | 허용 | — | NULL::character varying | — |
| 19 | `dryiceweight` | Dry Ice Weight | numeric | 허용 | — | — | — |
| 20 | `dutiesshipperaccount` | Duties Shipper Account | character varying(40) | 허용 | — | NULL::character varying | — |
| 21 | `fob` | Freight Terms | character varying(10) | 허용 | — | NULL::character varying | — |
| 22 | `freightcharges` | Freight Charges | character varying(10) | 허용 | — | NULL::character varying | — |
| 23 | `handlingcharge` | Handling Charge | numeric | 허용 | — | — | — |
| 24 | `height` | Height | numeric | 허용 | — | — | — |
| 25 | `homedeliverypremiumdate` | Date | timestamp without time zone | 허용 | — | — | — |
| 26 | `homedeliverypremiumphone` | Phone Number | character varying(30) | 허용 | — | NULL::character varying | — |
| 27 | `homedeliverypremiumtype` | Home Delivery Premium Type | character varying(30) | 허용 | — | NULL::character varying | — |
| 28 | `insurance` | Insurance | character(1) | 허용 | — | NULL::bpchar | — |
| 29 | `insuredamount` | Insured Amount | numeric | 허용 | — | — | — |
| 30 | `isaccessible` | Accessible | character(1) | 불가 | — | 'N'::bpchar | — |
| 31 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 32 | `isaddedhandling` | Added Handling | character(1) | 불가 | — | 'N'::bpchar | — |
| 33 | `iscargoaircraftonly` | Cargo Aircraft Only | character(1) | 불가 | — | 'N'::bpchar | — |
| 34 | `isdryice` | Dry Ice | character(1) | 불가 | — | 'N'::bpchar | — |
| 35 | `isdutiable` | Dutiable | character(1) | 불가 | — | 'N'::bpchar | — |
| 36 | `isfuturedayshipment` | Future Day Shipment | character(1) | 불가 | — | 'N'::bpchar | — |
| 37 | `ishazmat` | Hazardous Materials | character(1) | 불가 | — | 'N'::bpchar | — |
| 38 | `isholdatlocation` | Hold At Location | character(1) | 불가 | — | 'N'::bpchar | — |
| 39 | `isignorezipnotfound` | Ignore Zip Not Found | character(1) | 불가 | — | 'N'::bpchar | — |
| 40 | `isignorezipstatenotmatch` | Ignore Zip State Not Match | character(1) | 불가 | — | 'N'::bpchar | — |
| 41 | `isresidential` | Residential | character(1) | 불가 | — | 'Y'::bpchar | — |
| 42 | `issaturdaydelivery` | Saturday Delivery | character(1) | 불가 | — | 'N'::bpchar | — |
| 43 | `issaturdaypickup` | Saturday Pickup | character(1) | 불가 | — | 'N'::bpchar | — |
| 44 | `isverbalconfirmation` | Verbal Confirmation | character(1) | 불가 | — | 'N'::bpchar | — |
| 45 | `latestpickuptime` | Latest Pickup Time | timestamp without time zone | 허용 | — | — | — |
| 46 | `length` | Length | numeric | 허용 | — | — | — |
| 47 | `m_inout_id` | Shipment/Receipt | numeric(10,0) | 허용 | — | NULL::numeric | Material Shipment Document |
| 48 | `m_package_id` | Package | numeric(10,0) | 허용 | — | NULL::numeric | Shipment Package |
| 49 | `m_shipper_id` | Shipper | numeric(10,0) | 불가 | — | — | Method or manner of product delivery |
| 50 | `m_shipperlabels_id` | Shipper Labels | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 51 | `m_shipperpackaging_id` | Shipper Packaging | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 52 | `m_shipperpickuptypes_id` | Shipper Pickup Types | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 53 | `m_shippingprocessor_id` | Shipping Processor | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 54 | `m_shippingtransaction_id` | Shipping Transaction | numeric(10,0) | 불가 | 예 | — | — |
| 55 | `m_shippingtransaction_uu` | M_ShippingTransaction_UU | uuid | 허용 | — | — | — |
| 56 | `notificationmessage` | Notification Message | character varying(255) | 허용 | — | NULL::character varying | — |
| 57 | `notificationtype` | Notification Type | character varying(2) | 허용 | — | NULL::character varying | Type of Notifications |
| 58 | `paymentrule` | Payment Rule | character(1) | 허용 | — | NULL::bpchar | How you pay the invoice |
| 59 | `price` | Price | numeric | 허용 | — | — | Price |
| 60 | `priceactual` | Unit Price | numeric | 허용 | — | — | Actual Price  |
| 61 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 62 | `rateinquirymessage` | — | character varying(2000) | 허용 | — | NULL::character varying | — |
| 63 | `receivedinfo` | Info Received | character varying(255) | 허용 | — | NULL::character varying | Information of the receipt of the package (acknowledgement) |
| 64 | `shipdate` | Ship Date | timestamp without time zone | 허용 | — | — | Shipment Date/Time |
| 65 | `shipperaccount` | Shipper Account Number | character varying(40) | 허용 | — | NULL::character varying | — |
| 66 | `shippingrespmessage` | Response Message | character varying(2000) | 허용 | — | NULL::character varying | — |
| 67 | `surcharges` | Surcharges | numeric | 허용 | — | — | — |
| 68 | `trackinginfo` | Tracking Info | character varying(255) | 허용 | — | NULL::character varying | — |
| 69 | `trackingno` | Tracking No | character varying(255) | 허용 | — | NULL::character varying | Number to track the shipment |
| 70 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 71 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 72 | `weight` | Weight | numeric | 허용 | — | — | Weight of a product |
| 73 | `width` | Width | numeric | 허용 | — | — | — |
| 74 | `isalternatereturnaddress` | Alternate Return Address | character(1) | 불가 | — | 'N'::bpchar | — |
| 75 | `returnbpartner_id` | Return Partner | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 76 | `returnlocation_id` | Return Location | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 77 | `returnuser_id` | Return User/Contact | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 78 | `codamount` | COD Amount | numeric | 허용 | — | — | — |
| 79 | `customsvalue` | Customs Value | numeric | 허용 | — | — | — |
| 80 | `freightamt` | Freight Amount | numeric | 허용 | — | — | Freight Amount  |
| 81 | `salesrep_id` | Sales Representative | numeric(10,0) | 허용 | — | NULL::numeric | Sales Representative or Company Agent |
| 82 | `m_warehouse_id` | Warehouse | numeric(10,0) | 허용 | — | NULL::numeric | Storage Warehouse and Service Point |
| 83 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | NULL::numeric | Identifies a Business Partner |
| 84 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | NULL::numeric | User within the system - Internal or Business Partner Contact |
| 85 | `poreference` | Order Reference | character varying(30) | 허용 | — | NULL::character varying | Transaction Reference Number (Sales Order, Purchase Order) of your Business Partner |
| 86 | `c_invoice_id` | Invoice | numeric(10,0) | 허용 | — | NULL::numeric | Invoice Identifier |
| 87 | `bill_location_id` | Invoice Location | numeric(10,0) | 허용 | — | NULL::numeric | Business Partner Location for invoicing |
| 88 | `ispriviledgedrate` | Privileged Rate | character(1) | 불가 | — | 'N'::bpchar | — |
| 89 | `holdaddress_id` | Hold Address | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 24개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_user"]
    n1["c_bp_shippingacct"]
    n2["c_bpartner"]
    n3["c_bpartner_location"]
    n4["c_currency"]
    n5["c_invoice"]
    n6["c_order"]
    n7["c_uom"]
    n8["m_shippingtransaction"]
    n8 -->|"ad_user_id → ad_user_id"| n0
    n8 -->|"bill_location_id → c_bpartner_location_id"| n3
    n8 -->|"c_bpartner_id → c_bpartner_id"| n2
    n8 -->|"c_bpartner_location_id → c_bpartner_location_id"| n3
    n8 -->|"c_bp_shippingacct_id → c_bp_shippingacct_id"| n1
    n8 -->|"c_currency_id → c_currency_id"| n4
    n8 -->|"c_invoice_id → c_invoice_id"| n5
    n8 -->|"c_order_id → c_order_id"| n6
    n8 -->|"c_uom_length_id → c_uom_id"| n7
    n8 -->|"c_uom_weight_id → c_uom_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aduser_mshippingtransaction` <!-- FK_OUT: adempiere.m_shippingtransaction.aduser_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `billlocation_mshippingtransact` <!-- FK_OUT: adempiere.m_shippingtransaction.billlocation_mshippingtransact --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `bill_location_id` | [`c_bpartner_location`](../c/c_bpartner_location.md) | `c_bpartner_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_mshippingtransaction` <!-- FK_OUT: adempiere.m_shippingtransaction.cbpartner_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartnerlocation_mshippingtra` <!-- FK_OUT: adempiere.m_shippingtransaction.cbpartnerlocation_mshippingtra --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `c_bpartner_location_id` | [`c_bpartner_location`](../c/c_bpartner_location.md) | `c_bpartner_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpshippingacct_mshippingtrans` <!-- FK_OUT: adempiere.m_shippingtransaction.cbpshippingacct_mshippingtrans --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `c_bp_shippingacct_id` | [`c_bp_shippingacct`](../c/c_bp_shippingacct.md) | `c_bp_shippingacct_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_mshippingtransaction` <!-- FK_OUT: adempiere.m_shippingtransaction.ccurrency_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoice_mshippingtransaction` <!-- FK_OUT: adempiere.m_shippingtransaction.cinvoice_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `c_invoice_id` | [`c_invoice`](../c/c_invoice.md) | `c_invoice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `corder_mshippingtransaction` <!-- FK_OUT: adempiere.m_shippingtransaction.corder_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `c_order_id` | [`c_order`](../c/c_order.md) | `c_order_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cuomlength_mshippingtransactio` <!-- FK_OUT: adempiere.m_shippingtransaction.cuomlength_mshippingtransactio --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `c_uom_length_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cuomweight_mshippingtransactio` <!-- FK_OUT: adempiere.m_shippingtransaction.cuomweight_mshippingtransactio --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `c_uom_weight_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `holdaddress_mshippingtransacti` <!-- FK_OUT: adempiere.m_shippingtransaction.holdaddress_mshippingtransacti --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `holdaddress_id` | [`c_bpartner_location`](../c/c_bpartner_location.md) | `c_bpartner_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minout_mshippingtransaction` <!-- FK_OUT: adempiere.m_shippingtransaction.minout_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_inout_id` | [`m_inout`](m_inout.md) | `m_inout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpackage_mshippingtransaction` <!-- FK_OUT: adempiere.m_shippingtransaction.mpackage_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_package_id` | [`m_package`](m_package.md) | `m_package_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_mshippingtransaction` <!-- FK_OUT: adempiere.m_shippingtransaction.mshipper_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipperlabels_mshippingtransa` <!-- FK_OUT: adempiere.m_shippingtransaction.mshipperlabels_mshippingtransa --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_shipperlabels_id` | [`m_shipperlabels`](m_shipperlabels.md) | `m_shipperlabels_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipperpackaging_mshippingtra` <!-- FK_OUT: adempiere.m_shippingtransaction.mshipperpackaging_mshippingtra --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_shipperpackaging_id` | [`m_shipperpackaging`](m_shipperpackaging.md) | `m_shipperpackaging_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipperpickuptypes_mshippingt` <!-- FK_OUT: adempiere.m_shippingtransaction.mshipperpickuptypes_mshippingt --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_shipperpickuptypes_id` | [`m_shipperpickuptypes`](m_shipperpickuptypes.md) | `m_shipperpickuptypes_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshippingprocessor_mshippingtr` <!-- FK_OUT: adempiere.m_shippingtransaction.mshippingprocessor_mshippingtr --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_shippingprocessor_id` | [`m_shippingprocessor`](m_shippingprocessor.md) | `m_shippingprocessor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_mshippingtransactio` <!-- FK_OUT: adempiere.m_shippingtransaction.mwarehouse_mshippingtransactio --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_warehouse_id` | [`m_warehouse`](m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `returnbpartner_mshippingtransa` <!-- FK_OUT: adempiere.m_shippingtransaction.returnbpartner_mshippingtransa --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `returnbpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `returnlocation_mshippingtransa` <!-- FK_OUT: adempiere.m_shippingtransaction.returnlocation_mshippingtransa --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `returnlocation_id` | [`c_bpartner_location`](../c/c_bpartner_location.md) | `c_bpartner_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `returnuser_mshippingtransactio` <!-- FK_OUT: adempiere.m_shippingtransaction.returnuser_mshippingtransactio --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `returnuser_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `salesrep_mshippingtransaction` <!-- FK_OUT: adempiere.m_shippingtransaction.salesrep_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `salesrep_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mshippingtransaction_mshipping` <!-- FK_IN: adempiere.m_shippingtransactionline.mshippingtransaction_mshipping --> | [`m_shippingtransactionline`](m_shippingtransactionline.md) | `m_shippingtransaction_id` | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_shippingtransaction_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
