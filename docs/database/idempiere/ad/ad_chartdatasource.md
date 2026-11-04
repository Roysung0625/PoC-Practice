# ad_chartdatasource — 차트 데이터 원천

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_chartdatasource` |
| 한국어 논리명(문서용 해석) | 차트 데이터 원천 |
| 원본 논리명 | Chart Datasource |
| 원본 사전 ID | 53282 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 6 |
| 물리 열 수 | 22 |
| 나가는 FK / 들어오는 FK | 3 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

차트에 표시할 데이터를 조회하는 쿼리를 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Chart data definition
- 원본 도움말: Query to retrieve data for chart
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_chartdatasource_key` | `ad_chartdatasource_id` |
| UNIQUE | `ad_chartdatasource_uu_idx` | `ad_chartdatasource_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_chartdatasource_id` | Chart Datasource | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_chart_id` | Chart | numeric(10,0) | 불가 | — | — | — |
| 3 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 4 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 5 | `ad_table_id` | Table | numeric(10,0) | 허용 | — | — | Database Table information |
| 6 | `categorycolumn` | Category Column | character varying(124) | 허용 | — | — | Fully qualified data category column |
| 7 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 8 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 9 | `datecolumn` | Date Column | character varying(124) | 허용 | — | — | Fully qualified date column |
| 10 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 11 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 12 | `fromclause` | Sql FROM | character varying(2000) | 불가 | — | — | SQL FROM clause |
| 13 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 14 | `keycolumn` | Key Column | character varying(124) | 허용 | — | — | Key Column for Table |
| 15 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 16 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 17 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 18 | `valuecolumn` | Value Column | character varying(124) | 불가 | — | — | Fully qualified data value column |
| 19 | `whereclause` | Sql WHERE | character varying(2000) | 허용 | — | — | Fully qualified SQL WHERE clause |
| 20 | `timeoffset` | Time Offset | numeric(10,0) | 허용 | — | — | Number of time units to offset displayed chart data from the current date. |
| 21 | `seriescolumn` | Series Column | character varying(124) | 허용 | — | — | — |
| 22 | `ad_chartdatasource_uu` | AD_ChartDatasource_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_chart"]
    n1["ad_chartdatasource"]
    n2["ad_chartdatasource_trl"]
    n3["ad_entitytype"]
    n4["ad_table"]
    n1 -->|"ad_chart_id → ad_chart_id"| n0
    n1 -->|"ad_table_id → ad_table_id"| n4
    n1 -->|"entitytype → entitytype"| n3
    n2 -->|"ad_chartdatasource_id → ad_chartdatasource_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adchart_adchartdatasource` <!-- FK_OUT: adempiere.ad_chartdatasource.adchart_adchartdatasource --> | [`ad_chartdatasource`](ad_chartdatasource.md) | `ad_chart_id` | [`ad_chart`](ad_chart.md) | `ad_chart_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtable_adchartdatasource` <!-- FK_OUT: adempiere.ad_chartdatasource.adtable_adchartdatasource --> | [`ad_chartdatasource`](ad_chartdatasource.md) | `ad_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adchartdatasource` <!-- FK_OUT: adempiere.ad_chartdatasource.entityt_adchartdatasource --> | [`ad_chartdatasource`](ad_chartdatasource.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adchartdatasourceadchartdatas` <!-- FK_IN: adempiere.ad_chartdatasource_trl.adchartdatasourceadchartdatas --> | [`ad_chartdatasource_trl`](ad_chartdatasource_trl.md) | `ad_chartdatasource_id` | [`ad_chartdatasource`](ad_chartdatasource.md) | `ad_chartdatasource_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
