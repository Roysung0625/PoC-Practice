# t_aging — 채권·채무 연령 분석 자료

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.t_aging` |
| 한국어 논리명(문서용 해석) | 채권·채무 연령 분석 자료 |
| 원본 논리명 | T_Aging |
| 원본 사전 ID | 631 |
| 분류 | `t` — 작업·보고서용 보조 테이블 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 46 |
| 나가는 FK / 들어오는 FK | 7 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

실행 건별 송장 미결 금액을 만기 경과 및 도래 기간 구간으로 나눈 보고용 자료다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `t_aging_pkey` | `ad_pinstance_id`, `c_bpartner_id`, `c_currency_id`, `c_invoice_id`, `c_invoicepayschedule_id` |
| UNIQUE | `t_aging_uu_idx` | `t_aging_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_pinstance_id` | Process Instance | numeric(10,0) | 불가 | 예 | — | Instance of the process |
| 2 | `c_bpartner_id` | Business Partner | numeric(10,0) | 불가 | 예 | — | Identifies a Business Partner |
| 3 | `c_currency_id` | Currency | numeric(10,0) | 불가 | 예 | — | The Currency for this record |
| 4 | `c_invoice_id` | Invoice | numeric(10,0) | 불가 | 예 | — | Invoice Identifier |
| 5 | `c_invoicepayschedule_id` | Invoice Payment Schedule | numeric(10,0) | 불가 | 예 | — | Invoice Payment Schedule |
| 6 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 7 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 10 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 11 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 12 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 13 | `statementdate` | Statement date | timestamp without time zone | 불가 | — | — | Date of the statement |
| 14 | `duedate` | Due Date | timestamp without time zone | 불가 | — | — | Date when the payment is due |
| 15 | `daysdue` | Days due | numeric(10,0) | 허용 | — | 0 | Number of days due (negative: due in number of days) |
| 16 | `islistinvoices` | List Invoices | character(1) | 불가 | — | 'N'::bpchar | Include List of Invoices |
| 17 | `issotrx` | Sales Transaction | character(1) | 불가 | — | 'Y'::bpchar | This is a Sales Transaction |
| 18 | `c_bp_group_id` | Business Partner Group | numeric(10,0) | 불가 | — | — | Business Partner Group |
| 19 | `invoicedamt` | Invoiced Amount | numeric | 불가 | — | 0 | The amount invoiced |
| 20 | `openamt` | Open Amount | numeric | 불가 | — | 0 | Open item amount |
| 21 | `pastdue91_plus` | Past Due &gt; 91 | numeric | 불가 | — | 0 | — |
| 22 | `pastdue61_90` | Past Due 61-90 | numeric | 불가 | — | 0 | — |
| 23 | `pastdue61_plus` | Past Due &gt; 61 | numeric | 불가 | — | 0 | — |
| 24 | `pastdue31_60` | Past Due 31-60 | numeric | 불가 | — | 0 | — |
| 25 | `pastdue31_plus` | Past Due &gt; 31 | numeric | 불가 | — | 0 | — |
| 26 | `pastdue1_30` | Past Due 1-30 | numeric | 불가 | — | 0 | — |
| 27 | `pastdue8_30` | Past Due 8-30 | numeric | 불가 | — | 0 | — |
| 28 | `pastdue1_7` | Past Due 1-7 | numeric | 불가 | — | 0 | — |
| 29 | `pastdueamt` | Past Due | numeric | 불가 | — | 0 | — |
| 30 | `dueamt` | Amount due | numeric | 불가 | — | 0 | Amount of the payment due |
| 31 | `due0` | Due Today | numeric | 불가 | — | 0 | — |
| 32 | `due0_7` | Due Today-7 | numeric | 불가 | — | 0 | — |
| 33 | `due1_7` | Due 1-7 | numeric | 불가 | — | 0 | — |
| 34 | `due8_30` | Due 8-30 | numeric | 불가 | — | 0 | — |
| 35 | `due0_30` | Due Today-30 | numeric | 불가 | — | 0 | — |
| 36 | `due31_plus` | Due &gt; 31 | numeric | 불가 | — | 0 | — |
| 37 | `due31_60` | Due 31-60 | numeric | 불가 | — | 0 | — |
| 38 | `due61_plus` | Due &gt; 61 | numeric | 불가 | — | 0 | — |
| 39 | `due61_90` | Due 61-90 | numeric | 불가 | — | 0 | — |
| 40 | `due91_plus` | Due &gt; 91 | numeric | 불가 | — | 0 | — |
| 41 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 42 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | — | Marketing Campaign |
| 43 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 44 | `dateacct` | Account Date | character(1) | 허용 | — | 'N'::bpchar | Accounting Date |
| 45 | `t_aging_uu` | T_Aging_UU | uuid | 허용 | — | — | — |
| 46 | `convertamountsincurrency_id` | Convert Amounts in Currency | numeric(10,0) | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_pinstance"]
    n1["c_activity"]
    n2["c_bp_group"]
    n3["c_bpartner"]
    n4["c_campaign"]
    n5["c_currency"]
    n6["c_project"]
    n7["t_aging"]
    n7 -->|"ad_pinstance_id → ad_pinstance_id"| n0
    n7 -->|"c_activity_id → c_activity_id"| n1
    n7 -->|"c_bpartner_id → c_bpartner_id"| n3
    n7 -->|"c_bp_group_id → c_bp_group_id"| n2
    n7 -->|"c_campaign_id → c_campaign_id"| n4
    n7 -->|"c_currency_id → c_currency_id"| n5
    n7 -->|"c_project_id → c_project_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adpinstance_taging` <!-- FK_OUT: adempiere.t_aging.adpinstance_taging --> | [`t_aging`](t_aging.md) | `ad_pinstance_id` | [`ad_pinstance`](../ad/ad_pinstance.md) | `ad_pinstance_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_taging` <!-- FK_OUT: adempiere.t_aging.cactivity_taging --> | [`t_aging`](t_aging.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_taging` <!-- FK_OUT: adempiere.t_aging.cbpartner_taging --> | [`t_aging`](t_aging.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpgroup_taging` <!-- FK_OUT: adempiere.t_aging.cbpgroup_taging --> | [`t_aging`](t_aging.md) | `c_bp_group_id` | [`c_bp_group`](../c/c_bp_group.md) | `c_bp_group_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccampaign_taging` <!-- FK_OUT: adempiere.t_aging.ccampaign_taging --> | [`t_aging`](t_aging.md) | `c_campaign_id` | [`c_campaign`](../c/c_campaign.md) | `c_campaign_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_taging` <!-- FK_OUT: adempiere.t_aging.ccurrency_taging --> | [`t_aging`](t_aging.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_taging` <!-- FK_OUT: adempiere.t_aging.cproject_taging --> | [`t_aging`](t_aging.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `issotrx`가 있습니다. 판매(`Y`)와 구매(`N`)를 구분해서 분석합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
