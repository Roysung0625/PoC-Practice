# pa_reportcube — 회계 집계 큐브

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.pa_reportcube` |
| 한국어 논리명(문서용 해석) | 회계 집계 큐브 |
| 원본 논리명 | Report Cube |
| 원본 사전 ID | 53202 |
| 분류 | `pa` — 성과·보고서·대시보드 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 31 |
| 나가는 FK / 들어오는 FK | 1 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

선택한 달력의 기간별로 지정 차원에 따라 회계 자료를 사전 집계하는 큐브를 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Define reporting cube for pre-calculation of summary accounting data.
- 원본 도움말: Summary data will be generated for each period of the selected calendar, grouped by the selected dimensions..
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `pa_reportcube_key` | `pa_reportcube_id` |
| UNIQUE | `pa_reportcube_uu_idx` | `pa_reportcube_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `c_calendar_id` | Calendar | numeric(10,0) | 불가 | — | — | Accounting Calendar Name |
| 4 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 5 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 6 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 7 | `isactive` | Active | character(1) | 허용 | — | NULL::bpchar | The record is active in the system |
| 8 | `isactivitydim` | Activity Dimension | character(1) | 허용 | — | NULL::bpchar | Include Activity as a cube dimension |
| 9 | `isbpartnerdim` | Business Partner Dimension | character(1) | 허용 | — | NULL::bpchar | Include Business Partner as a cube dimension |
| 10 | `iscampaigndim` | Campaign Dimension | character(1) | 허용 | — | NULL::bpchar | Include Campaign as a cube dimension |
| 11 | `isglbudgetdim` | GL Budget Dimension | character(1) | 허용 | — | NULL::bpchar | Include GL Budget as a cube dimension |
| 12 | `islocfromdim` | Location From Dimension | character(1) | 허용 | — | NULL::bpchar | Include Location From as a cube dimension |
| 13 | `isloctodim` | Location To  Dimension | character(1) | 허용 | — | NULL::bpchar | Include Location To as a cube dimension |
| 14 | `isorgtrxdim` | OrgTrx Dimension | character(1) | 허용 | — | NULL::bpchar | Include OrgTrx as a cube dimension |
| 15 | `isproductdim` | Product Dimension | character(1) | 허용 | — | NULL::bpchar | Include Product as a cube dimension |
| 16 | `isprojectdim` | Project Dimension | character(1) | 허용 | — | NULL::bpchar | Include Project as a cube dimension |
| 17 | `isprojectphasedim` | Project Phase  Dimension | character(1) | 허용 | — | NULL::bpchar | Include Project Phase as a cube dimension |
| 18 | `isprojecttaskdim` | Project Task  Dimension | character(1) | 허용 | — | NULL::bpchar | Include Project Task as a cube dimension |
| 19 | `issalesregiondim` | Sales Region Dimension | character(1) | 허용 | — | NULL::bpchar | Include Sales Region as a cube dimension |
| 20 | `issubacctdim` | Sub Acct Dimension | character(1) | 허용 | — | NULL::bpchar | Include Sub Acct as a cube dimension |
| 21 | `isuser1dim` | User Element List 1 Dimension | character(1) | 허용 | — | NULL::bpchar | Include User Element List 1 as a cube dimension |
| 22 | `isuser2dim` | User Element List 2 Dimension | character(1) | 허용 | — | NULL::bpchar | Include User Element List 2 as a cube dimension |
| 23 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 24 | `pa_reportcube_id` | Report Cube | numeric(10,0) | 불가 | 예 | — | Define reporting cube for pre-calculation of summary accounting data. |
| 25 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 26 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 27 | `processing` | Process Now | character(1) | 불가 | — | 'N'::bpchar | — |
| 28 | `lastrecalculated` | Last Recalculated | timestamp without time zone | 허용 | — | — | The time last recalculated. |
| 29 | `isuserelement2dim` | User Column 2 Dimension | character(1) | 허용 | — | NULL::bpchar | Include User Element 2 as a cube dimension |
| 30 | `isuserelement1dim` | User Column 1 Dimension | character(1) | 허용 | — | NULL::bpchar | Include User Element 1 as a cube dimension |
| 31 | `pa_reportcube_uu` | PA_ReportCube_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 3개 중 3개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_calendar"]
    n1["fact_acct_summary"]
    n2["pa_report"]
    n3["pa_reportcube"]
    n3 -->|"c_calendar_id → c_calendar_id"| n0
    n1 -->|"pa_reportcube_id → pa_reportcube_id"| n3
    n2 -->|"pa_reportcube_id → pa_reportcube_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccalendar_pareportcube` <!-- FK_OUT: adempiere.pa_reportcube.ccalendar_pareportcube --> | [`pa_reportcube`](pa_reportcube.md) | `c_calendar_id` | [`c_calendar`](../c/c_calendar.md) | `c_calendar_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `pareportcube_factacctsummary` <!-- FK_IN: adempiere.fact_acct_summary.pareportcube_factacctsummary --> | [`fact_acct_summary`](../fact/fact_acct_summary.md) | `pa_reportcube_id` | [`pa_reportcube`](pa_reportcube.md) | `pa_reportcube_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pareportcube_pareport` <!-- FK_IN: adempiere.pa_report.pareportcube_pareport --> | [`pa_report`](pa_report.md) | `pa_reportcube_id` | [`pa_reportcube`](pa_reportcube.md) | `pa_reportcube_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
