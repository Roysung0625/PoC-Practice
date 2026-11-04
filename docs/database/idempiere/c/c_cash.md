# c_cash — 현금 출납 전표

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_cash` |
| 한국어 논리명(문서용 해석) | 현금 출납 전표 |
| 원본 논리명 | Cash Journal |
| 원본 사전 ID | 407 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 3 |
| 물리 열 수 | 30 |
| 나가는 FK / 들어오는 FK | 8 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

현금 출납 내역을 묶는 현금 일지의 머리글을 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Cash Journal
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_cash_pkey` | `c_cash_id` |
| UNIQUE | `c_cash_uu_idx` | `c_cash_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_cash_id` | Cash Journal | numeric(10,0) | 불가 | 예 | — | Cash Journal |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_cashbook_id` | Cash Book | numeric(10,0) | 불가 | — | — | Cash Book for recording petty cash transactions |
| 10 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `statementdate` | Statement date | timestamp without time zone | 불가 | — | — | Date of the statement |
| 13 | `dateacct` | Account Date | timestamp without time zone | 불가 | — | — | Accounting Date |
| 14 | `beginningbalance` | Beginning Balance | numeric | 불가 | — | 0 | Balance prior to any transactions |
| 15 | `endingbalance` | Ending balance | numeric | 불가 | — | 0 | Ending  or closing balance |
| 16 | `statementdifference` | Statement difference | numeric | 허용 | — | 0 | Difference between statement ending balance and actual ending balance |
| 17 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 18 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 19 | `posted` | Posted | character(1) | 불가 | — | 'N'::bpchar | Posting status |
| 20 | `ad_orgtrx_id` | Trx Organization | numeric(10,0) | 허용 | — | — | Performing or initiating organization |
| 21 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 22 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | — | Marketing Campaign |
| 23 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 24 | `user1_id` | User Element List 1 | numeric(10,0) | 허용 | — | — | User defined list element #1 |
| 25 | `user2_id` | User Element List 2 | numeric(10,0) | 허용 | — | — | User defined list element #2 |
| 26 | `isapproved` | Approved | character(1) | 불가 | — | 'N'::bpchar | Indicates if this document requires approval |
| 27 | `docstatus` | Document Status | character(2) | 불가 | — | — | The current status of the document |
| 28 | `docaction` | Document Action | character(2) | 불가 | — | — | The targeted status of the document |
| 29 | `processedon` | Processed On | numeric | 허용 | — | — | The date+time (expressed in decimal format) when the document has been processed |
| 30 | `c_cash_uu` | C_Cash_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 9개 중 9개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_org"]
    n1["c_activity"]
    n2["c_campaign"]
    n3["c_cash"]
    n4["c_cashbook"]
    n5["c_cashline"]
    n6["c_elementvalue"]
    n7["c_project"]
    n3 -->|"ad_org_id → ad_org_id"| n0
    n3 -->|"ad_orgtrx_id → ad_org_id"| n0
    n3 -->|"c_activity_id → c_activity_id"| n1
    n3 -->|"c_campaign_id → c_campaign_id"| n2
    n3 -->|"c_cashbook_id → c_cashbook_id"| n4
    n3 -->|"user1_id → c_elementvalue_id"| n6
    n3 -->|"user2_id → c_elementvalue_id"| n6
    n3 -->|"c_project_id → c_project_id"| n7
    n5 -->|"c_cash_id → c_cash_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adorg_ccash` <!-- FK_OUT: adempiere.c_cash.adorg_ccash --> | [`c_cash`](c_cash.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorgtrx_ccash` <!-- FK_OUT: adempiere.c_cash.adorgtrx_ccash --> | [`c_cash`](c_cash.md) | `ad_orgtrx_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_ccash` <!-- FK_OUT: adempiere.c_cash.cactivity_ccash --> | [`c_cash`](c_cash.md) | `c_activity_id` | [`c_activity`](c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccampaign_ccash` <!-- FK_OUT: adempiere.c_cash.ccampaign_ccash --> | [`c_cash`](c_cash.md) | `c_campaign_id` | [`c_campaign`](c_campaign.md) | `c_campaign_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccashbook_ccash` <!-- FK_OUT: adempiere.c_cash.ccashbook_ccash --> | [`c_cash`](c_cash.md) | `c_cashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalueuser1_ccash` <!-- FK_OUT: adempiere.c_cash.celementvalueuser1_ccash --> | [`c_cash`](c_cash.md) | `user1_id` | [`c_elementvalue`](c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalueuser2_ccash` <!-- FK_OUT: adempiere.c_cash.celementvalueuser2_ccash --> | [`c_cash`](c_cash.md) | `user2_id` | [`c_elementvalue`](c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_ccash` <!-- FK_OUT: adempiere.c_cash.cproject_ccash --> | [`c_cash`](c_cash.md) | `c_project_id` | [`c_project`](c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccash_ccashline` <!-- FK_IN: adempiere.c_cashline.ccash_ccashline --> | [`c_cashline`](c_cashline.md) | `c_cash_id` | [`c_cash`](c_cash.md) | `c_cash_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
