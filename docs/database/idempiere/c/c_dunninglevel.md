# c_dunninglevel — 연체 독촉 단계

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_dunninglevel` |
| 한국어 논리명(문서용 해석) | 연체 독촉 단계 |
| 원본 논리명 | Dunning Level |
| 원본 사전 ID | 331 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 2 |
| 물리 열 수 | 28 |
| 나가는 FK / 들어오는 FK | 3 / 4 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

독촉 규칙별 연체 일수·독촉 간격·이자·수수료·인쇄 문구와 신용 중지 조건 등을 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_dunninglevel_pkey` | `c_dunninglevel_id` |
| UNIQUE | `c_dunninglevel_uu_idx` | `c_dunninglevel_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_dunninglevel_id` | Dunning Level | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_dunning_id` | Dunning | numeric(10,0) | 불가 | — | — | Dunning Rules for overdue invoices |
| 10 | `printname` | Print Text | character varying(60) | 불가 | — | — | The label text to be printed on a document or correspondence. |
| 11 | `daysafterdue` | Days after due date | numeric(10,0) | 불가 | — | — | Days after due date to dun (if negative days until due) |
| 12 | `daysbetweendunning` | Days between dunning | numeric(10,0) | 불가 | — | — | Days between sending dunning notices |
| 13 | `note` | Note | character varying(2000) | 허용 | — | — | Optional additional user defined information |
| 14 | `chargeinterest` | Charge Interest | character(1) | 불가 | — | 'Y'::bpchar | Indicates if interest will be charged on overdue invoices |
| 15 | `interestpercent` | Interest in percent | numeric | 허용 | — | 0 | Percentage interest to charge on overdue invoices |
| 16 | `chargefee` | Charge fee | character(1) | 불가 | — | 'Y'::bpchar | Indicates if fees will be charged for overdue invoices |
| 17 | `feeamt` | Fee Amount | numeric | 허용 | — | 0 | Fee amount in invoice currency |
| 18 | `dunning_printformat_id` | Dunning Print Format | numeric(10,0) | 허용 | — | — | Print Format for printing Dunning Letters |
| 19 | `name` | Name | character varying(60) | 불가 | — | 'x'::character varying | Alphanumeric identifier of the entity |
| 20 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 21 | `isshowalldue` | Show All Due | character(1) | 불가 | — | 'N'::bpchar | Show/print all due invoices |
| 22 | `isshownotdue` | Show Not Due | character(1) | 불가 | — | 'N'::bpchar | Show/print all invoices which are not due (yet). |
| 23 | `issetcreditstop` | Credit Stop | character(1) | 불가 | — | 'N'::bpchar | Set the business partner to credit stop |
| 24 | `issetpaymentterm` | Set Payment Term | character(1) | 불가 | — | 'N'::bpchar | Set the payment term of the Business Partner |
| 25 | `c_paymentterm_id` | Payment Term | numeric(10,0) | 허용 | — | — | The terms of Payment (timing, discount) |
| 26 | `invoicecollectiontype` | Collection Status | character(1) | 허용 | — | NULL::bpchar | Invoice Collection Status |
| 27 | `isstatement` | Is Statement | character(1) | 불가 | — | 'N'::bpchar | Dunning Level is a definition of a statement |
| 28 | `c_dunninglevel_uu` | C_DunningLevel_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_printformat"]
    n1["c_dunning"]
    n2["c_dunninglevel"]
    n3["c_dunninglevel_trl"]
    n4["c_dunningrun"]
    n5["c_dunningrunentry"]
    n6["c_invoice"]
    n7["c_paymentterm"]
    n2 -->|"dunning_printformat_id → ad_printformat_id"| n0
    n2 -->|"c_dunning_id → c_dunning_id"| n1
    n2 -->|"c_paymentterm_id → c_paymentterm_id"| n7
    n3 -->|"c_dunninglevel_id → c_dunninglevel_id"| n2
    n4 -->|"c_dunninglevel_id → c_dunninglevel_id"| n2
    n5 -->|"c_dunninglevel_id → c_dunninglevel_id"| n2
    n6 -->|"c_dunninglevel_id → c_dunninglevel_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adprintformat_cdunninglevel` <!-- FK_OUT: adempiere.c_dunninglevel.adprintformat_cdunninglevel --> | [`c_dunninglevel`](c_dunninglevel.md) | `dunning_printformat_id` | [`ad_printformat`](../ad/ad_printformat.md) | `ad_printformat_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdunning_cdunninglevel` <!-- FK_OUT: adempiere.c_dunninglevel.cdunning_cdunninglevel --> | [`c_dunninglevel`](c_dunninglevel.md) | `c_dunning_id` | [`c_dunning`](c_dunning.md) | `c_dunning_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_cdunninglevel` <!-- FK_OUT: adempiere.c_dunninglevel.cpaymentterm_cdunninglevel --> | [`c_dunninglevel`](c_dunninglevel.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cdunninglevel_cdltrl` <!-- FK_IN: adempiere.c_dunninglevel_trl.cdunninglevel_cdltrl --> | [`c_dunninglevel_trl`](c_dunninglevel_trl.md) | `c_dunninglevel_id` | [`c_dunninglevel`](c_dunninglevel.md) | `c_dunninglevel_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdunninglevel_cdunningrun` <!-- FK_IN: adempiere.c_dunningrun.cdunninglevel_cdunningrun --> | [`c_dunningrun`](c_dunningrun.md) | `c_dunninglevel_id` | [`c_dunninglevel`](c_dunninglevel.md) | `c_dunninglevel_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdunninglevel_cdunningrunentry` <!-- FK_IN: adempiere.c_dunningrunentry.cdunninglevel_cdunningrunentry --> | [`c_dunningrunentry`](c_dunningrunentry.md) | `c_dunninglevel_id` | [`c_dunninglevel`](c_dunninglevel.md) | `c_dunninglevel_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdunninglevel_cinvoice` <!-- FK_IN: adempiere.c_invoice.cdunninglevel_cinvoice --> | [`c_invoice`](c_invoice.md) | `c_dunninglevel_id` | [`c_dunninglevel`](c_dunninglevel.md) | `c_dunninglevel_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
