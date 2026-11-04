# c_allocationline — 입출금 소거 명세

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_allocationline` |
| 한국어 논리명(문서용 해석) | 입출금 소거 명세 |
| 원본 논리명 | Allocation Line |
| 원본 사전 ID | 390 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 2 |
| 물리 열 수 | 24 |
| 나가는 FK / 들어오는 FK | 8 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

입출금 소거 전표에서 청구서·입출금·현금 명세를 연결하고 배분 금액·할인·상각·과부족 금액을 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Allocation Line
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_allocationline_pkey` | `c_allocationline_id` |
| UNIQUE | `c_allocationline_uu_idx` | `c_allocationline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_allocationline_id` | Allocation Line | numeric(10,0) | 불가 | 예 | — | Allocation Line |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `allocationno` | — | numeric(10,0) | 허용 | — | — | — |
| 10 | `datetrx` | Transaction Date | timestamp without time zone | 허용 | — | — | Transaction Date |
| 11 | `ismanual` | Manual | character(1) | 허용 | — | 'N'::bpchar | This is a manual process |
| 12 | `c_invoice_id` | Invoice | numeric(10,0) | 허용 | — | — | Invoice Identifier |
| 13 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 14 | `c_order_id` | Order | numeric(10,0) | 허용 | — | — | Order |
| 15 | `c_payment_id` | Payment | numeric(10,0) | 허용 | — | — | Payment identifier |
| 16 | `c_cashline_id` | Cash Journal Line | numeric(10,0) | 허용 | — | — | Cash Journal Line |
| 17 | `amount` | Amount | numeric | 불가 | — | 0 | Amount in a defined currency |
| 18 | `discountamt` | Discount Amount | numeric | 불가 | — | 0 | Calculated amount of discount |
| 19 | `writeoffamt` | Write-off Amount | numeric | 불가 | — | 0 | Amount to write-off |
| 20 | `overunderamt` | Over/Under Payment | numeric | 허용 | — | 0 | Over-Payment (unallocated) or Under-Payment (partial payment) Amount |
| 21 | `c_allocationhdr_id` | Allocation | numeric(10,0) | 불가 | — | — | Payment allocation |
| 22 | `c_allocationline_uu` | C_AllocationLine_UU | uuid | 허용 | — | — | — |
| 23 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | NULL::numeric | Additional document charges |
| 24 | `c_banktransfer_id` | Bank Transfer | numeric(10,0) | 허용 | — | NULL::numeric | Bank Transfer |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 10개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_allocationhdr"]
    n1["c_allocationline"]
    n2["c_banktransfer"]
    n3["c_bpartner"]
    n4["c_cashline"]
    n5["c_charge"]
    n6["c_invoice"]
    n7["c_order"]
    n8["c_payment"]
    n9["c_paymentallocate"]
    n10["c_taxdeclarationline"]
    n1 -->|"c_allocationhdr_id → c_allocationhdr_id"| n0
    n1 -->|"c_banktransfer_id → c_banktransfer_id"| n2
    n1 -->|"c_bpartner_id → c_bpartner_id"| n3
    n1 -->|"c_cashline_id → c_cashline_id"| n4
    n1 -->|"c_charge_id → c_charge_id"| n5
    n1 -->|"c_invoice_id → c_invoice_id"| n6
    n1 -->|"c_order_id → c_order_id"| n7
    n1 -->|"c_payment_id → c_payment_id"| n8
    n9 -->|"c_allocationline_id → c_allocationline_id"| n1
    n10 -->|"c_allocationline_id → c_allocationline_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `callocation_callocationline` <!-- FK_OUT: adempiere.c_allocationline.callocation_callocationline --> | [`c_allocationline`](c_allocationline.md) | `c_allocationhdr_id` | [`c_allocationhdr`](c_allocationhdr.md) | `c_allocationhdr_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbanktransfer_callocationline` <!-- FK_OUT: adempiere.c_allocationline.cbanktransfer_callocationline --> | [`c_allocationline`](c_allocationline.md) | `c_banktransfer_id` | [`c_banktransfer`](c_banktransfer.md) | `c_banktransfer_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_callocationline` <!-- FK_OUT: adempiere.c_allocationline.cbpartner_callocationline --> | [`c_allocationline`](c_allocationline.md) | `c_bpartner_id` | [`c_bpartner`](c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccashline_callocationline` <!-- FK_OUT: adempiere.c_allocationline.ccashline_callocationline --> | [`c_allocationline`](c_allocationline.md) | `c_cashline_id` | [`c_cashline`](c_cashline.md) | `c_cashline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccharge_callocationline` <!-- FK_OUT: adempiere.c_allocationline.ccharge_callocationline --> | [`c_allocationline`](c_allocationline.md) | `c_charge_id` | [`c_charge`](c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoice_callocationline` <!-- FK_OUT: adempiere.c_allocationline.cinvoice_callocationline --> | [`c_allocationline`](c_allocationline.md) | `c_invoice_id` | [`c_invoice`](c_invoice.md) | `c_invoice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `corder_callocation` <!-- FK_OUT: adempiere.c_allocationline.corder_callocation --> | [`c_allocationline`](c_allocationline.md) | `c_order_id` | [`c_order`](c_order.md) | `c_order_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpayment_callocationline` <!-- FK_OUT: adempiere.c_allocationline.cpayment_callocationline --> | [`c_allocationline`](c_allocationline.md) | `c_payment_id` | [`c_payment`](c_payment.md) | `c_payment_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cpaymtallocate_callocationline` <!-- FK_IN: adempiere.c_paymentallocate.cpaymtallocate_callocationline --> | [`c_paymentallocate`](c_paymentallocate.md) | `c_allocationline_id` | [`c_allocationline`](c_allocationline.md) | `c_allocationline_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `callocationline_ctaxdeclline` <!-- FK_IN: adempiere.c_taxdeclarationline.callocationline_ctaxdeclline --> | [`c_taxdeclarationline`](c_taxdeclarationline.md) | `c_allocationline_id` | [`c_allocationline`](c_allocationline.md) | `c_allocationline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
