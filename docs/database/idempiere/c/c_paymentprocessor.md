# c_paymentprocessor — 전자결제 처리기

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_paymentprocessor` |
| 한국어 논리명(문서용 해석) | 전자결제 처리기 |
| 원본 논리명 | Payment Processor |
| 원본 사전 ID | 398 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 2 |
| 물리 열 수 | 36 |
| 나가는 FK / 들어오는 FK | 3 / 5 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

전자결제를 처리하는 서비스 또는 처리기의 설정을 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Payment processor for electronic payments
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_paymentprocessor_pkey` | `c_paymentprocessor_id` |
| UNIQUE | `c_paymentprocessor_uu_idx` | `c_paymentprocessor_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_paymentprocessor_id` | Payment Processor | numeric(10,0) | 불가 | 예 | — | Payment processor for electronic payments |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `c_bankaccount_id` | Bank Account | numeric(10,0) | 허용 | — | — | Account at the Bank |
| 12 | `ad_sequence_id` | Sequence | numeric(10,0) | 허용 | — | — | Document Sequence |
| 13 | `payprocessorclass` | Payment Processor Class | character varying(60) | 허용 | — | — | Payment Processor Java Class |
| 14 | `hostaddress` | Host Address | character varying(60) | 허용 | — | — | Host Address URL or DNS |
| 15 | `hostport` | Host port | numeric(10,0) | 허용 | — | — | Host Communication Port |
| 16 | `proxyaddress` | Proxy address | character varying(60) | 허용 | — | — |  Address of your proxy server |
| 17 | `proxyport` | Proxy port | numeric(10,0) | 허용 | — | — | Port of your proxy server |
| 18 | `proxylogon` | Proxy logon | character varying(60) | 허용 | — | — | Logon of your proxy server |
| 19 | `proxypassword` | Proxy password | character varying(60) | 허용 | — | — | Password of your proxy server |
| 20 | `acceptvisa` | Accept Visa | character(1) | 불가 | — | 'Y'::bpchar | Accept Visa Cards |
| 21 | `acceptmc` | Accept MasterCard | character(1) | 불가 | — | 'Y'::bpchar | Accept Master Card |
| 22 | `acceptamex` | Accept AMEX | character(1) | 불가 | — | 'Y'::bpchar | Accept American Express Card |
| 23 | `acceptdiners` | Accept Diners | character(1) | 불가 | — | 'Y'::bpchar | Accept Diner's Club |
| 24 | `acceptdiscover` | Accept Discover | character(1) | 불가 | — | 'Y'::bpchar | Accept Discover Card |
| 25 | `acceptcorporate` | Accept Corporate | character(1) | 불가 | — | 'Y'::bpchar | Accept Corporate Purchase Cards |
| 26 | `acceptcheck` | Accept Electronic Check | character(1) | 불가 | — | 'Y'::bpchar | Accept ECheck (Electronic Checks) |
| 27 | `acceptatm` | Accept ATM | character(1) | 불가 | — | 'Y'::bpchar | Accept Bank ATM Card |
| 28 | `requirevv` | Require Credit Card Verification Code | character(1) | 불가 | — | 'N'::bpchar | Require 3/4 digit Credit Verification Code |
| 29 | `c_currency_id` | Currency | numeric(10,0) | 허용 | — | — | The Currency for this record |
| 30 | `costpertrx` | Cost per transaction | numeric | 불가 | — | 0 | Fixed cost per transaction |
| 31 | `commission` | Commission % | numeric | 불가 | — | — | Commission stated as a percentage |
| 32 | `minimumamt` | Minimum Amt | numeric | 허용 | — | 0 | Minimum Amount in Document Currency |
| 33 | `acceptdirectdebit` | Accept Direct Debit | character(1) | 불가 | — | 'N'::bpchar | Accept Direct Debits (vendor initiated) |
| 34 | `acceptdirectdeposit` | Accept Direct Deposit | character(1) | 불가 | — | 'N'::bpchar | Accept Direct Deposit (payee initiated) |
| 35 | `c_paymentprocessor_uu` | C_PaymentProcessor_UU | uuid | 허용 | — | — | — |
| 36 | `trxtype` | Transaction Type | character(1) | 허용 | — | NULL::bpchar | Type of credit card transaction |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_sequence"]
    n1["c_bankaccount"]
    n2["c_bankaccount_processor"]
    n3["c_bp_bankaccount"]
    n4["c_currency"]
    n5["c_payment"]
    n6["c_paymentbatch"]
    n7["c_paymentprocessor"]
    n8["c_paymenttransaction"]
    n7 -->|"ad_sequence_id → ad_sequence_id"| n0
    n7 -->|"c_bankaccount_id → c_bankaccount_id"| n1
    n7 -->|"c_currency_id → c_currency_id"| n4
    n2 -->|"c_paymentprocessor_id → c_paymentprocessor_id"| n7
    n3 -->|"c_paymentprocessor_id → c_paymentprocessor_id"| n7
    n5 -->|"c_paymentprocessor_id → c_paymentprocessor_id"| n7
    n6 -->|"c_paymentprocessor_id → c_paymentprocessor_id"| n7
    n8 -->|"c_paymentprocessor_id → c_paymentprocessor_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adsequence_cpaymentprocessor` <!-- FK_OUT: adempiere.c_paymentprocessor.adsequence_cpaymentprocessor --> | [`c_paymentprocessor`](c_paymentprocessor.md) | `ad_sequence_id` | [`ad_sequence`](../ad/ad_sequence.md) | `ad_sequence_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbankaccount_cpaymtprocessor` <!-- FK_OUT: adempiere.c_paymentprocessor.cbankaccount_cpaymtprocessor --> | [`c_paymentprocessor`](c_paymentprocessor.md) | `c_bankaccount_id` | [`c_bankaccount`](c_bankaccount.md) | `c_bankaccount_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_cpaymentprocessor` <!-- FK_OUT: adempiere.c_paymentprocessor.ccurrency_cpaymentprocessor --> | [`c_paymentprocessor`](c_paymentprocessor.md) | `c_currency_id` | [`c_currency`](c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cpaymentprocessor_cbankaccount` <!-- FK_IN: adempiere.c_bankaccount_processor.cpaymentprocessor_cbankaccount --> | [`c_bankaccount_processor`](c_bankaccount_processor.md) | `c_paymentprocessor_id` | [`c_paymentprocessor`](c_paymentprocessor.md) | `c_paymentprocessor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentprocessor_cbpbankaccou` <!-- FK_IN: adempiere.c_bp_bankaccount.cpaymentprocessor_cbpbankaccou --> | [`c_bp_bankaccount`](c_bp_bankaccount.md) | `c_paymentprocessor_id` | [`c_paymentprocessor`](c_paymentprocessor.md) | `c_paymentprocessor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentprocessor_cpayment` <!-- FK_IN: adempiere.c_payment.cpaymentprocessor_cpayment --> | [`c_payment`](c_payment.md) | `c_paymentprocessor_id` | [`c_paymentprocessor`](c_paymentprocessor.md) | `c_paymentprocessor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymtprocessor_cpaymtbatch` <!-- FK_IN: adempiere.c_paymentbatch.cpaymtprocessor_cpaymtbatch --> | [`c_paymentbatch`](c_paymentbatch.md) | `c_paymentprocessor_id` | [`c_paymentprocessor`](c_paymentprocessor.md) | `c_paymentprocessor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentprocessor_cpaymenttran` <!-- FK_IN: adempiere.c_paymenttransaction.cpaymentprocessor_cpaymenttran --> | [`c_paymenttransaction`](c_paymenttransaction.md) | `c_paymentprocessor_id` | [`c_paymentprocessor`](c_paymentprocessor.md) | `c_paymentprocessor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
