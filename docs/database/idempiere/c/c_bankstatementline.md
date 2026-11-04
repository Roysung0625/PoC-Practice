# c_bankstatementline — 은행거래 명세 행

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_bankstatementline` |
| 한국어 논리명(문서용 해석) | 은행거래 명세 행 |
| 원본 논리명 | Bank statement line |
| 원본 사전 ID | 393 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 2 |
| 물리 열 수 | 43 |
| 나가는 FK / 들어오는 FK | 7 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

은행거래 명세서에 포함된 개별 계좌 거래를 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Line on a statement from this Bank
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_bankstatementline_pkey` | `c_bankstatementline_id` |
| UNIQUE | `c_bankstatementline_uu_idx` | `c_bankstatementline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_bankstatementline_id` | Bank statement line | numeric(10,0) | 불가 | 예 | — | Line on a statement from this Bank |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_bankstatement_id` | Bank Statement | numeric(10,0) | 불가 | — | — | Bank Statement of account |
| 10 | `line` | Line No | numeric(10,0) | 불가 | — | — | Unique line for this document |
| 11 | `description` | Description | character varying(1000) | 허용 | — | — | Optional short description of the record |
| 12 | `isreversal` | Reversal | character(1) | 불가 | — | 'N'::bpchar | This is a reversing transaction |
| 13 | `c_payment_id` | Payment | numeric(10,0) | 허용 | — | — | Payment identifier |
| 14 | `valutadate` | Effective date | timestamp without time zone | 불가 | — | — | Date when money is available |
| 15 | `dateacct` | Account Date | timestamp without time zone | 불가 | — | — | Accounting Date |
| 16 | `c_currency_id` | Currency | numeric(10,0) | 불가 | — | — | The Currency for this record |
| 17 | `trxamt` | Transaction Amount | numeric | 불가 | — | 0 | Amount of a transaction |
| 18 | `stmtamt` | Statement amount | numeric | 불가 | — | 0 | Statement Amount |
| 19 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | — | Additional document charges |
| 20 | `chargeamt` | Charge amount | numeric | 불가 | — | 0 | Charge Amount |
| 21 | `interestamt` | Interest Amount | numeric | 불가 | — | 0 | Interest Amount |
| 22 | `memo` | Memo | character varying(4000) | 허용 | — | — | Memo Text |
| 23 | `referenceno` | Reference No | character varying(255) | 허용 | — | — | Your customer or vendor number at the Business Partner's site |
| 24 | `ismanual` | Manual | character(1) | 불가 | — | 'N'::bpchar | This is a manual process |
| 25 | `efttrxid` | EFT Trx ID | character varying(40) | 허용 | — | — | Electronic Funds Transfer Transaction ID |
| 26 | `efttrxtype` | EFT Trx Type | character varying(255) | 허용 | — | — | Electronic Funds Transfer Transaction Type |
| 27 | `eftmemo` | EFT Memo | character varying(4000) | 허용 | — | — | Electronic Funds Transfer Memo |
| 28 | `eftpayee` | EFT Payee | character varying(255) | 허용 | — | — | Electronic Funds Transfer Payee information |
| 29 | `eftpayeeaccount` | EFT Payee Account | character varying(40) | 허용 | — | — | Electronic Funds Transfer Payee Account Information |
| 30 | `createpayment` | Create Payment | character(1) | 허용 | — | — | — |
| 31 | `statementlinedate` | Statement Line Date | timestamp without time zone | 불가 | — | — | Date of the Statement Line |
| 32 | `eftstatementlinedate` | EFT Statement Line Date | timestamp without time zone | 허용 | — | — | Electronic Funds Transfer Statement Line Date |
| 33 | `eftvalutadate` | EFT Effective Date | timestamp without time zone | 허용 | — | — | Electronic Funds Transfer Valuta (effective) Date |
| 34 | `eftreference` | EFT Reference | character varying(255) | 허용 | — | — | Electronic Funds Transfer Reference |
| 35 | `eftcurrency` | EFT Currency | character varying(20) | 허용 | — | — | Electronic Funds Transfer Currency |
| 36 | `eftamt` | EFT Amount | numeric | 허용 | — | 0 | Electronic Funds Transfer Amount |
| 37 | `eftcheckno` | EFT Check No | character varying(20) | 허용 | — | — | Electronic Funds Transfer Check No |
| 38 | `matchstatement` | Match Statement | character(1) | 허용 | — | — | — |
| 39 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 40 | `c_invoice_id` | Invoice | numeric(10,0) | 허용 | — | — | Invoice Identifier |
| 41 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 42 | `c_bankstatementline_uu` | C_BankStatementLine_UU | uuid | 허용 | — | — | — |
| 43 | `c_depositbatch_id` | Deposit Batch | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_bankstatement"]
    n1["c_bankstatementline"]
    n2["c_bpartner"]
    n3["c_charge"]
    n4["c_currency"]
    n5["c_depositbatch"]
    n6["c_invoice"]
    n7["c_payment"]
    n8["i_bankstatement"]
    n1 -->|"c_bpartner_id → c_bpartner_id"| n2
    n1 -->|"c_bankstatement_id → c_bankstatement_id"| n0
    n1 -->|"c_charge_id → c_charge_id"| n3
    n1 -->|"c_currency_id → c_currency_id"| n4
    n1 -->|"c_depositbatch_id → c_depositbatch_id"| n5
    n1 -->|"c_invoice_id → c_invoice_id"| n6
    n1 -->|"c_payment_id → c_payment_id"| n7
    n8 -->|"c_bankstatementline_id → c_bankstatementline_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cbpartner_cbankstatementline` <!-- FK_OUT: adempiere.c_bankstatementline.cbpartner_cbankstatementline --> | [`c_bankstatementline`](c_bankstatementline.md) | `c_bpartner_id` | [`c_bpartner`](c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbstatement_cbstatementline` <!-- FK_OUT: adempiere.c_bankstatementline.cbstatement_cbstatementline --> | [`c_bankstatementline`](c_bankstatementline.md) | `c_bankstatement_id` | [`c_bankstatement`](c_bankstatement.md) | `c_bankstatement_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccharge_cbankstmtlime` <!-- FK_OUT: adempiere.c_bankstatementline.ccharge_cbankstmtlime --> | [`c_bankstatementline`](c_bankstatementline.md) | `c_charge_id` | [`c_charge`](c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_cbankstmtline` <!-- FK_OUT: adempiere.c_bankstatementline.ccurrency_cbankstmtline --> | [`c_bankstatementline`](c_bankstatementline.md) | `c_currency_id` | [`c_currency`](c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdepositbatch_cbankstatementli` <!-- FK_OUT: adempiere.c_bankstatementline.cdepositbatch_cbankstatementli --> | [`c_bankstatementline`](c_bankstatementline.md) | `c_depositbatch_id` | [`c_depositbatch`](c_depositbatch.md) | `c_depositbatch_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoice_cbankstatementline` <!-- FK_OUT: adempiere.c_bankstatementline.cinvoice_cbankstatementline --> | [`c_bankstatementline`](c_bankstatementline.md) | `c_invoice_id` | [`c_invoice`](c_invoice.md) | `c_invoice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpayment_cbankstmtline` <!-- FK_OUT: adempiere.c_bankstatementline.cpayment_cbankstmtline --> | [`c_bankstatementline`](c_bankstatementline.md) | `c_payment_id` | [`c_payment`](c_payment.md) | `c_payment_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cbankstmtline_ibankstmt` <!-- FK_IN: adempiere.i_bankstatement.cbankstmtline_ibankstmt --> | [`i_bankstatement`](../i/i_bankstatement.md) | `c_bankstatementline_id` | [`c_bankstatementline`](c_bankstatementline.md) | `c_bankstatementline_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
