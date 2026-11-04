# m_matchpo — 구매 주문 대사

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_matchpo` |
| 한국어 논리명(문서용 해석) | 구매 주문 대사 |
| 원본 논리명 | Match PO |
| 원본 사전 ID | 473 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 37 |
| 물리 열 수 | 27 |
| 나가는 FK / 들어오는 FK | 7 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

구매 주문을 출하·입고 및 송장 내역과 대응시킨다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Match Purchase Order to Shipment/Receipt and Invoice
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_matchpo_pkey` | `m_matchpo_id` |
| UNIQUE | `m_matchpo_uu_idx` | `m_matchpo_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_matchpo_id` | Match PO | numeric(10,0) | 불가 | 예 | — | Match Purchase Order to Shipment/Receipt and Invoice |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_orderline_id` | Sales Order Line | numeric(10,0) | 불가 | — | — | Sales Order Line |
| 10 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 11 | `m_inoutline_id` | Shipment/Receipt Line | numeric(10,0) | 허용 | — | — | Line on Shipment or Receipt document |
| 12 | `c_invoiceline_id` | Invoice Line | numeric(10,0) | 허용 | — | — | Invoice Detail Line |
| 13 | `datetrx` | Transaction Date | timestamp without time zone | 불가 | — | — | Transaction Date |
| 14 | `qty` | Quantity | numeric | 불가 | — | 0 | Quantity |
| 15 | `processing` | Process Now | character(1) | 불가 | — | — | — |
| 16 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 17 | `posted` | Posted | character(1) | 불가 | — | 'N'::bpchar | Posting status |
| 18 | `documentno` | Document No | character varying(30) | 허용 | — | — | Document sequence number of the document |
| 19 | `dateacct` | Account Date | timestamp without time zone | 허용 | — | — | Accounting Date |
| 20 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 허용 | — | — | Product Attribute Set Instance |
| 21 | `pricematchdifference` | Price Match Difference | numeric | 허용 | — | — | Difference between Purchase and Invoice Price per matched line |
| 22 | `isapproved` | Approved | character(1) | 허용 | — | 'Y'::bpchar | Indicates if this document requires approval |
| 23 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 24 | `processedon` | Processed On | numeric | 허용 | — | — | The date+time (expressed in decimal format) when the document has been processed |
| 25 | `m_matchpo_uu` | M_MatchPO_UU | uuid | 허용 | — | — | — |
| 26 | `reversal_id` | Reversal ID | numeric(10,0) | 허용 | — | NULL::numeric | ID of document reversal |
| 27 | `ref_matchpo_id` | Referenced Match PO | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_invoiceline"]
    n1["c_orderline"]
    n2["m_attributesetinstance"]
    n3["m_inoutline"]
    n4["m_matchpo"]
    n5["m_product"]
    n4 -->|"c_invoiceline_id → c_invoiceline_id"| n0
    n4 -->|"c_orderline_id → c_orderline_id"| n1
    n4 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n2
    n4 -->|"m_inoutline_id → m_inoutline_id"| n3
    n4 -->|"m_product_id → m_product_id"| n5
    n4 -->|"ref_matchpo_id → m_matchpo_id"| n4
    n4 -->|"reversal_id → m_matchpo_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cinvoiceline_mmatchpo` <!-- FK_OUT: adempiere.m_matchpo.cinvoiceline_mmatchpo --> | [`m_matchpo`](m_matchpo.md) | `c_invoiceline_id` | [`c_invoiceline`](../c/c_invoiceline.md) | `c_invoiceline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `corderline_mmatchpo` <!-- FK_OUT: adempiere.m_matchpo.corderline_mmatchpo --> | [`m_matchpo`](m_matchpo.md) | `c_orderline_id` | [`c_orderline`](../c/c_orderline.md) | `c_orderline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattributesetinstance_mmatchpo` <!-- FK_OUT: adempiere.m_matchpo.mattributesetinstance_mmatchpo --> | [`m_matchpo`](m_matchpo.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minoutline_mmatchpo` <!-- FK_OUT: adempiere.m_matchpo.minoutline_mmatchpo --> | [`m_matchpo`](m_matchpo.md) | `m_inoutline_id` | [`m_inoutline`](m_inoutline.md) | `m_inoutline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mmatchpo` <!-- FK_OUT: adempiere.m_matchpo.mproduct_mmatchpo --> | [`m_matchpo`](m_matchpo.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `refmatchpo_mmatchpo` <!-- FK_OUT: adempiere.m_matchpo.refmatchpo_mmatchpo --> | [`m_matchpo`](m_matchpo.md) | `ref_matchpo_id` | [`m_matchpo`](m_matchpo.md) | `m_matchpo_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversal_mmatchpo` <!-- FK_OUT: adempiere.m_matchpo.reversal_mmatchpo --> | [`m_matchpo`](m_matchpo.md) | `reversal_id` | [`m_matchpo`](m_matchpo.md) | `m_matchpo_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `refmatchpo_mmatchpo` <!-- FK_IN: adempiere.m_matchpo.refmatchpo_mmatchpo --> | [`m_matchpo`](m_matchpo.md) | `ref_matchpo_id` | [`m_matchpo`](m_matchpo.md) | `m_matchpo_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversal_mmatchpo` <!-- FK_IN: adempiere.m_matchpo.reversal_mmatchpo --> | [`m_matchpo`](m_matchpo.md) | `reversal_id` | [`m_matchpo`](m_matchpo.md) | `m_matchpo_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
