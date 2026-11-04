# c_cashbook — 소액현금 출납장

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_cashbook` |
| 한국어 논리명(문서용 해석) | 소액현금 출납장 |
| 원본 논리명 | Cash Book |
| 원본 사전 ID | 408 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 2 |
| 물리 열 수 | 13 |
| 나가는 FK / 들어오는 FK | 1 / 10 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

소액현금 거래를 기록하는 출납장의 기준정보를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Cash Book for recording petty cash transactions
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_cashbook_pkey` | `c_cashbook_id` |
| UNIQUE | `c_cashbook_uu_idx` | `c_cashbook_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_cashbook_id` | Cash Book | numeric(10,0) | 불가 | 예 | — | Cash Book for recording petty cash transactions |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `isdefault` | Default | character(1) | 불가 | — | 'N'::bpchar | Default value |
| 12 | `c_currency_id` | Currency | numeric(10,0) | 불가 | — | — | The Currency for this record |
| 13 | `c_cashbook_uu` | C_CashBook_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 11개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_orginfo"]
    n1["c_cash"]
    n2["c_cashbook"]
    n3["c_cashbook_acct"]
    n4["c_currency"]
    n5["c_payment"]
    n6["c_paymenttransaction"]
    n7["c_pos"]
    n8["u_posterminal"]
    n2 -->|"c_currency_id → c_currency_id"| n4
    n0 -->|"transfercashbook_id → c_cashbook_id"| n2
    n1 -->|"c_cashbook_id → c_cashbook_id"| n2
    n3 -->|"c_cashbook_id → c_cashbook_id"| n2
    n5 -->|"c_cashbook_id → c_cashbook_id"| n2
    n6 -->|"c_cashbook_id → c_cashbook_id"| n2
    n7 -->|"c_cashbook_id → c_cashbook_id"| n2
    n8 -->|"cardtransfercashbook_id → c_cashbook_id"| n2
    n8 -->|"cashtransfercashbook_id → c_cashbook_id"| n2
    n8 -->|"c_cashbook_id → c_cashbook_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccurrency_ccashbook` <!-- FK_OUT: adempiere.c_cashbook.ccurrency_ccashbook --> | [`c_cashbook`](c_cashbook.md) | `c_currency_id` | [`c_currency`](c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccashbook_adorginfo` <!-- FK_IN: adempiere.ad_orginfo.ccashbook_adorginfo --> | [`ad_orginfo`](../ad/ad_orginfo.md) | `transfercashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccashbook_ccash` <!-- FK_IN: adempiere.c_cash.ccashbook_ccash --> | [`c_cash`](c_cash.md) | `c_cashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccashbook_ccashbookacct` <!-- FK_IN: adempiere.c_cashbook_acct.ccashbook_ccashbookacct --> | [`c_cashbook_acct`](c_cashbook_acct.md) | `c_cashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_payment__c_cashbo_c_cashbook` <!-- FK_IN: adempiere.c_payment.c_payment__c_cashbo_c_cashbook --> | [`c_payment`](c_payment.md) | `c_cashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccashbook_cpaymenttransaction` <!-- FK_IN: adempiere.c_paymenttransaction.ccashbook_cpaymenttransaction --> | [`c_paymenttransaction`](c_paymenttransaction.md) | `c_cashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccashbook_cpos` <!-- FK_IN: adempiere.c_pos.ccashbook_cpos --> | [`c_pos`](c_pos.md) | `c_cashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cardtransfercashbook_upostermi` <!-- FK_IN: adempiere.u_posterminal.cardtransfercashbook_upostermi --> | [`u_posterminal`](../u/u_posterminal.md) | `cardtransfercashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cashtransfercashbook_upostermi` <!-- FK_IN: adempiere.u_posterminal.cashtransfercashbook_upostermi --> | [`u_posterminal`](../u/u_posterminal.md) | `cashtransfercashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccashbook_uposterminal` <!-- FK_IN: adempiere.u_posterminal.ccashbook_uposterminal --> | [`u_posterminal`](../u/u_posterminal.md) | `c_cashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `checktransfercashbook_uposterm` <!-- FK_IN: adempiere.u_posterminal.checktransfercashbook_uposterm --> | [`u_posterminal`](../u/u_posterminal.md) | `checktransfercashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
