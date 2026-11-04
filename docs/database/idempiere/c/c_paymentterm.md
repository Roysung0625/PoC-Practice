# c_paymentterm — 지급 조건

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_paymentterm` |
| 한국어 논리명(문서용 해석) | 지급 조건 |
| 원본 논리명 | Payment Term |
| 원본 사전 ID | 113 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 5 |
| 물리 열 수 | 30 |
| 나가는 FK / 들어오는 FK | 0 / 12 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

거래에 적용할 지급 시점과 할인 등의 조건을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: The terms for Payment of this transaction
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_paymentterm_pkey` | `c_paymentterm_id` |
| UNIQUE | `c_paymentterm_uu_idx` | `c_paymentterm_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `c_paymentterm_name`: `CREATE UNIQUE INDEX c_paymentterm_name ON adempiere.c_paymentterm USING btree (ad_client_id, name)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_paymentterm_id` | Payment Term | numeric(10,0) | 불가 | 예 | — | The terms of Payment (timing, discount) |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `documentnote` | Document Note | character varying(2000) | 허용 | — | — | Additional information for a Document |
| 12 | `afterdelivery` | After Delivery | character(1) | 불가 | — | 'N'::bpchar | Due after delivery rather than after invoicing |
| 13 | `isduefixed` | Fixed due date | character(1) | 불가 | — | 'N'::bpchar | Payment is due on a fixed date |
| 14 | `netdays` | Net Days | numeric(10,0) | 불가 | — | — | Net Days in which payment is due |
| 15 | `gracedays` | Grace Days | numeric(10,0) | 불가 | — | — | Days after due date to send first dunning letter |
| 16 | `fixmonthcutoff` | Fix month cutoff | numeric(10,0) | 허용 | — | — | Last day to include for next due date |
| 17 | `fixmonthday` | Fix month day | numeric(10,0) | 허용 | — | — | Day of the month of the due date |
| 18 | `fixmonthoffset` | Fix month offset | numeric(10,0) | 허용 | — | — | Number of months (0=same, 1=following) |
| 19 | `discountdays` | Discount Days | numeric(10,0) | 불가 | — | — | Number of days from invoice date to be eligible for discount |
| 20 | `discount` | Discount % | numeric | 불가 | — | — | Discount in percent |
| 21 | `discountdays2` | Discount Days 2 | numeric(10,0) | 불가 | — | — | Number of days from invoice date to be eligible for discount |
| 22 | `discount2` | Discount 2 % | numeric | 불가 | — | — | Discount in percent |
| 23 | `isnextbusinessday` | Next Business Day | character(1) | 허용 | — | 'Y'::bpchar | Payment due on the next business day |
| 24 | `isdefault` | Default | character(1) | 허용 | — | 'N'::bpchar | Default value |
| 25 | `value` | Search Key | character varying(40) | 불가 | — | — | Search key for the record in the format required - must be unique |
| 26 | `netday` | Net Day | character(1) | 허용 | — | — | Day when payment is due net |
| 27 | `isvalid` | Valid | character(1) | 불가 | — | 'N'::bpchar | Element is valid |
| 28 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 29 | `paymenttermusage` | Payment Term Usage | character(1) | 불가 | — | 'B'::bpchar | Payment term usage indicates if this payment term is used for sales, purchases or both. |
| 30 | `c_paymentterm_uu` | C_PaymentTerm_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 12개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_bpartner"]
    n1["c_dunninglevel"]
    n2["c_invoice"]
    n3["c_order"]
    n4["c_paymentterm"]
    n5["c_paymentterm_trl"]
    n6["c_payschedule"]
    n7["c_project"]
    n8["c_withholding"]
    n9["i_invoice"]
    n0 -->|"c_paymentterm_id → c_paymentterm_id"| n4
    n0 -->|"po_paymentterm_id → c_paymentterm_id"| n4
    n1 -->|"c_paymentterm_id → c_paymentterm_id"| n4
    n2 -->|"c_paymentterm_id → c_paymentterm_id"| n4
    n3 -->|"c_paymentterm_id → c_paymentterm_id"| n4
    n5 -->|"c_paymentterm_id → c_paymentterm_id"| n4
    n6 -->|"c_paymentterm_id → c_paymentterm_id"| n4
    n7 -->|"c_paymentterm_id → c_paymentterm_id"| n4
    n8 -->|"c_paymentterm_id → c_paymentterm_id"| n4
    n9 -->|"c_paymentterm_id → c_paymentterm_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cpaymentterm_cbpartner` <!-- FK_IN: adempiere.c_bpartner.cpaymentterm_cbpartner --> | [`c_bpartner`](c_bpartner.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpopaymentterm_cbpartner` <!-- FK_IN: adempiere.c_bpartner.cpopaymentterm_cbpartner --> | [`c_bpartner`](c_bpartner.md) | `po_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_cdunninglevel` <!-- FK_IN: adempiere.c_dunninglevel.cpaymentterm_cdunninglevel --> | [`c_dunninglevel`](c_dunninglevel.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_cinvoice` <!-- FK_IN: adempiere.c_invoice.cpaymentterm_cinvoice --> | [`c_invoice`](c_invoice.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_soheader` <!-- FK_IN: adempiere.c_order.cpaymentterm_soheader --> | [`c_order`](c_order.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_cpaytermtrl` <!-- FK_IN: adempiere.c_paymentterm_trl.cpaymentterm_cpaytermtrl --> | [`c_paymentterm_trl`](c_paymentterm_trl.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_cpayschedule` <!-- FK_IN: adempiere.c_payschedule.cpaymentterm_cpayschedule --> | [`c_payschedule`](c_payschedule.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_cproject` <!-- FK_IN: adempiere.c_project.cpaymentterm_cproject --> | [`c_project`](c_project.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_cwithholding` <!-- FK_IN: adempiere.c_withholding.cpaymentterm_cwithholding --> | [`c_withholding`](c_withholding.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_iinvoice` <!-- FK_IN: adempiere.i_invoice.cpaymentterm_iinvoice --> | [`i_invoice`](../i/i_invoice.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_iorder` <!-- FK_IN: adempiere.i_order.cpaymentterm_iorder --> | [`i_order`](../i/i_order.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_wstore` <!-- FK_IN: adempiere.w_store.cpaymentterm_wstore --> | [`w_store`](../w/w_store.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
