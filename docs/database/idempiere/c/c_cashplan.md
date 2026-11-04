# c_cashplan — 자금 계획

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_cashplan` |
| 한국어 논리명(문서용 해석) | 자금 계획 |
| 원본 논리명 | Cash Plan |
| 원본 사전 ID | 53297 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 26 |
| 나가는 FK / 들어오는 FK | 7 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

예상 자금 흐름을 계획 단위로 묶어 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Cash Plan
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_cashplan_key` | `c_cashplan_id` |
| UNIQUE | `c_cashplan_uu_idx` | `c_cashplan_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_orgtrx_id` | Trx Organization | numeric(10,0) | 허용 | — | NULL::numeric | Performing or initiating organization |
| 4 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 5 | `cashflowtype` | Cash Flow Type | character(1) | 허용 | — | NULL::bpchar | — |
| 6 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | NULL::numeric | Identifies a Business Partner |
| 7 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | NULL::numeric | Marketing Campaign |
| 8 | `c_cashplan_id` | Cash Plan | numeric(10,0) | 불가 | 예 | — | — |
| 9 | `copyfrom` | Copy From | character(1) | 허용 | — | NULL::bpchar | Copy From Record |
| 10 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 11 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 12 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 13 | `datedoc` | Document Date | timestamp without time zone | 불가 | — | — | Date of the Document |
| 14 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 15 | `documentno` | Document No | character varying(30) | 불가 | — | — | Document sequence number of the document |
| 16 | `generateperiodic` | Generate Periodic Plan | character(1) | 허용 | — | NULL::bpchar | — |
| 17 | `grandtotal` | Grand Total | numeric | 불가 | — | — | Total amount of document |
| 18 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 19 | `isapproved` | Approved | character(1) | 불가 | — | 'N'::bpchar | Indicates if this document requires approval |
| 20 | `issotrx` | Sales Transaction | character(1) | 불가 | — | — | This is a Sales Transaction |
| 21 | `processed` | Processed | character(1) | 불가 | — | — | The document has been processed |
| 22 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 23 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 24 | `user1_id` | User Element List 1 | numeric(10,0) | 허용 | — | NULL::numeric | User defined list element #1 |
| 25 | `user2_id` | User Element List 2 | numeric(10,0) | 허용 | — | NULL::numeric | User defined list element #2 |
| 26 | `c_cashplan_uu` | C_CashPlan_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_org"]
    n1["c_activity"]
    n2["c_bpartner"]
    n3["c_campaign"]
    n4["c_cashplan"]
    n5["c_cashplanline"]
    n6["c_elementvalue"]
    n7["c_project"]
    n4 -->|"ad_orgtrx_id → ad_org_id"| n0
    n4 -->|"c_activity_id → c_activity_id"| n1
    n4 -->|"c_bpartner_id → c_bpartner_id"| n2
    n4 -->|"c_campaign_id → c_campaign_id"| n3
    n4 -->|"c_project_id → c_project_id"| n7
    n4 -->|"user1_id → c_elementvalue_id"| n6
    n4 -->|"user2_id → c_elementvalue_id"| n6
    n5 -->|"c_cashplan_id → c_cashplan_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adorgtrx_ccashplan` <!-- FK_OUT: adempiere.c_cashplan.adorgtrx_ccashplan --> | [`c_cashplan`](c_cashplan.md) | `ad_orgtrx_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_ccashplan` <!-- FK_OUT: adempiere.c_cashplan.cactivity_ccashplan --> | [`c_cashplan`](c_cashplan.md) | `c_activity_id` | [`c_activity`](c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_ccashplan` <!-- FK_OUT: adempiere.c_cashplan.cbpartner_ccashplan --> | [`c_cashplan`](c_cashplan.md) | `c_bpartner_id` | [`c_bpartner`](c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccampaign_ccashplan` <!-- FK_OUT: adempiere.c_cashplan.ccampaign_ccashplan --> | [`c_cashplan`](c_cashplan.md) | `c_campaign_id` | [`c_campaign`](c_campaign.md) | `c_campaign_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_ccashplan` <!-- FK_OUT: adempiere.c_cashplan.cproject_ccashplan --> | [`c_cashplan`](c_cashplan.md) | `c_project_id` | [`c_project`](c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `user1_ccashplan` <!-- FK_OUT: adempiere.c_cashplan.user1_ccashplan --> | [`c_cashplan`](c_cashplan.md) | `user1_id` | [`c_elementvalue`](c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `user2_ccashplan` <!-- FK_OUT: adempiere.c_cashplan.user2_ccashplan --> | [`c_cashplan`](c_cashplan.md) | `user2_id` | [`c_elementvalue`](c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccashplan_ccashplanline` <!-- FK_IN: adempiere.c_cashplanline.ccashplan_ccashplanline --> | [`c_cashplanline`](c_cashplanline.md) | `c_cashplan_id` | [`c_cashplan`](c_cashplan.md) | `c_cashplan_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `issotrx`가 있습니다. 판매(`Y`)와 구매(`N`)를 구분해서 분석합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
