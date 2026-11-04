# pa_report — 재무 보고서

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.pa_report` |
| 한국어 논리명(문서용 해석) | 재무 보고서 |
| 원본 논리명 | Financial Report |
| 원본 사전 ID | 445 |
| 분류 | `pa` — 성과·보고서·대시보드 |
| 전체 테넌트 행 수 | 3 |
| 물리 열 수 | 24 |
| 나가는 FK / 들어오는 FK | 8 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

재무 보고서의 기본 정의를 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Financial Report
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `pa_report_pkey` | `pa_report_id` |
| UNIQUE | `pa_report_uu_idx` | `pa_report_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `pa_report_id` | Financial Report | numeric(10,0) | 불가 | 예 | — | Financial Report |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 허용 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `pa_reportlineset_id` | Report Line Set | numeric(10,0) | 불가 | — | — | — |
| 12 | `pa_reportcolumnset_id` | Report Column Set | numeric(10,0) | 불가 | — | — | Collection of Columns for Report |
| 13 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 불가 | — | — | Rules for accounting |
| 14 | `c_calendar_id` | Calendar | numeric(10,0) | 불가 | — | — | Accounting Calendar Name |
| 15 | `processing` | Process Now | character(1) | 불가 | — | — | — |
| 16 | `ad_printformat_id` | Print Format | numeric(10,0) | 허용 | — | — | Data Print Format |
| 17 | `listsources` | List Sources | character(1) | 불가 | — | 'N'::bpchar | List Report Line Sources |
| 18 | `listtrx` | List Transactions | character(1) | 불가 | — | 'N'::bpchar | List the report transactions |
| 19 | `jasperprocess_id` | Jasper Process | numeric(10,0) | 허용 | — | — | The Jasper Process used by the print engine if any process defined |
| 20 | `jasperprocessing` | Jasper Process Now | character(1) | 허용 | — | — | — |
| 21 | `pa_reportcube_id` | Report Cube | numeric(10,0) | 허용 | — | NULL::numeric | Define reporting cube for pre-calculation of summary accounting data. |
| 22 | `pa_report_uu` | PA_Report_UU | uuid | 허용 | — | — | — |
| 23 | `listsourcesxtrx` | Include source accounts with no transaction | character(1) | 허용 | — | 'N'::bpchar | Include source accounts with no transaction for list report line sources |
| 24 | `excludeadjustmentperiods` | Exclude Adjustment Periods | character(1) | 불가 | — | '1'::bpchar | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_org"]
    n1["ad_printformat"]
    n2["ad_process"]
    n3["c_acctschema"]
    n4["c_calendar"]
    n5["pa_report"]
    n6["pa_reportcolumnset"]
    n7["pa_reportcube"]
    n8["pa_reportlineset"]
    n5 -->|"ad_org_id → ad_org_id"| n0
    n5 -->|"ad_printformat_id → ad_printformat_id"| n1
    n5 -->|"c_acctschema_id → c_acctschema_id"| n3
    n5 -->|"c_calendar_id → c_calendar_id"| n4
    n5 -->|"jasperprocess_id → ad_process_id"| n2
    n5 -->|"pa_reportcolumnset_id → pa_reportcolumnset_id"| n6
    n5 -->|"pa_reportlineset_id → pa_reportlineset_id"| n8
    n5 -->|"pa_reportcube_id → pa_reportcube_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adorg_pareport` <!-- FK_OUT: adempiere.pa_report.adorg_pareport --> | [`pa_report`](pa_report.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintformat_pareport` <!-- FK_OUT: adempiere.pa_report.adprintformat_pareport --> | [`pa_report`](pa_report.md) | `ad_printformat_id` | [`ad_printformat`](../ad/ad_printformat.md) | `ad_printformat_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cacctschema_pareport` <!-- FK_OUT: adempiere.pa_report.cacctschema_pareport --> | [`pa_report`](pa_report.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccalendar_pareport` <!-- FK_OUT: adempiere.pa_report.ccalendar_pareport --> | [`pa_report`](pa_report.md) | `c_calendar_id` | [`c_calendar`](../c/c_calendar.md) | `c_calendar_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `jasperprocess_pareport` <!-- FK_OUT: adempiere.pa_report.jasperprocess_pareport --> | [`pa_report`](pa_report.md) | `jasperprocess_id` | [`ad_process`](../ad/ad_process.md) | `ad_process_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pareport_columnset` <!-- FK_OUT: adempiere.pa_report.pareport_columnset --> | [`pa_report`](pa_report.md) | `pa_reportcolumnset_id` | [`pa_reportcolumnset`](pa_reportcolumnset.md) | `pa_reportcolumnset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pareport_lineset` <!-- FK_OUT: adempiere.pa_report.pareport_lineset --> | [`pa_report`](pa_report.md) | `pa_reportlineset_id` | [`pa_reportlineset`](pa_reportlineset.md) | `pa_reportlineset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pareportcube_pareport` <!-- FK_OUT: adempiere.pa_report.pareportcube_pareport --> | [`pa_report`](pa_report.md) | `pa_reportcube_id` | [`pa_reportcube`](pa_reportcube.md) | `pa_reportcube_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
