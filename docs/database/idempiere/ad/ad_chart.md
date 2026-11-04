# ad_chart — 차트 정의

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_chart` |
| 한국어 논리명(문서용 해석) | 차트 정의 |
| 원본 논리명 | Chart |
| 원본 사전 ID | 53284 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 4 |
| 물리 열 수 | 21 |
| 나가는 FK / 들어오는 FK | 1 / 6 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

정보를 그래프로 표시하기 위한 차트를 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Chart definition
- 원본 도움말: Charts are for the graphical display of information
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_chart_key` | `ad_chart_id` |
| UNIQUE | `ad_chart_uu_idx` | `ad_chart_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_chart_id` | Chart | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `charttype` | Chart Type | character varying(2) | 불가 | — | — | Type of chart to render |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 8 | `isactive` | Active | character(1) | 허용 | — | NULL::bpchar | The record is active in the system |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 11 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 12 | `winheight` | Window Height | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 13 | `isdisplaylegend` | Display Legend | character(1) | 불가 | — | 'Y'::bpchar | Display chart legend |
| 14 | `chartorientation` | Orientation | character(1) | 불가 | — | 'V'::bpchar | The orientation of the chart. |
| 15 | `istimeseries` | Time Series | character(1) | 불가 | — | 'N'::bpchar | The domain data for the chart is organised by time. |
| 16 | `timeunit` | Time Unit | character(1) | 허용 | — | NULL::bpchar | The unit of time for grouping chart data. |
| 17 | `timescope` | Time Scope | numeric(10,0) | 허용 | — | — | The number of time units to include the chart result. |
| 18 | `domainlabel` | Domain Label | character varying(60) | 허용 | — | NULL::character varying | Label for the domain axis. |
| 19 | `rangelabel` | Range Label | character varying(60) | 허용 | — | NULL::character varying | Label for the range axis. |
| 20 | `ad_chart_uu` | AD_Chart_UU | uuid | 허용 | — | — | — |
| 21 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_chart"]
    n1["ad_chart_trl"]
    n2["ad_chartdatasource"]
    n3["ad_column"]
    n4["ad_entitytype"]
    n5["ad_field"]
    n6["ad_userdef_field"]
    n7["pa_dashboardcontent"]
    n0 -->|"entitytype → entitytype"| n4
    n1 -->|"ad_chart_id → ad_chart_id"| n0
    n2 -->|"ad_chart_id → ad_chart_id"| n0
    n3 -->|"ad_chart_id → ad_chart_id"| n0
    n5 -->|"ad_chart_id → ad_chart_id"| n0
    n6 -->|"ad_chart_id → ad_chart_id"| n0
    n7 -->|"ad_chart_id → ad_chart_id"| n0
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `entityt_adchart` <!-- FK_OUT: adempiere.ad_chart.entityt_adchart --> | [`ad_chart`](ad_chart.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adchart_adcharttrl` <!-- FK_IN: adempiere.ad_chart_trl.adchart_adcharttrl --> | [`ad_chart_trl`](ad_chart_trl.md) | `ad_chart_id` | [`ad_chart`](ad_chart.md) | `ad_chart_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adchart_adchartdatasource` <!-- FK_IN: adempiere.ad_chartdatasource.adchart_adchartdatasource --> | [`ad_chartdatasource`](ad_chartdatasource.md) | `ad_chart_id` | [`ad_chart`](ad_chart.md) | `ad_chart_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adchart_adcolumn` <!-- FK_IN: adempiere.ad_column.adchart_adcolumn --> | [`ad_column`](ad_column.md) | `ad_chart_id` | [`ad_chart`](ad_chart.md) | `ad_chart_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adchart_adfield` <!-- FK_IN: adempiere.ad_field.adchart_adfield --> | [`ad_field`](ad_field.md) | `ad_chart_id` | [`ad_chart`](ad_chart.md) | `ad_chart_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adchart_aduserdeffield` <!-- FK_IN: adempiere.ad_userdef_field.adchart_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_chart_id` | [`ad_chart`](ad_chart.md) | `ad_chart_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adchart_padashboardcontent` <!-- FK_IN: adempiere.pa_dashboardcontent.adchart_padashboardcontent --> | [`pa_dashboardcontent`](../pa/pa_dashboardcontent.md) | `ad_chart_id` | [`ad_chart`](ad_chart.md) | `ad_chart_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
