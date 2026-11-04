# ad_ref_table — 테이블 기반 참조

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_ref_table` |
| 한국어 논리명(문서용 해석) | 테이블 기반 참조 |
| 원본 논리명 | AD_Ref_Table |
| 원본 사전 ID | 103 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 234 |
| 물리 열 수 | 20 |
| 나가는 FK / 들어오는 FK | 9 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

테이블을 이용한 참조 정의를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Reference Table Definitions
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_ref_table_pkey` | `ad_reference_id` |
| UNIQUE | `ad_ref_table_uu_idx` | `ad_ref_table_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_reference_id` | Reference | numeric(10,0) | 불가 | 예 | — | System Reference and Validation |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 10 | `ad_key` | Key column | numeric(10,0) | 불가 | — | — | Unique identifier of a record |
| 11 | `ad_display` | Display column | numeric(10,0) | 불가 | — | — | Column that will display |
| 12 | `isvaluedisplayed` | Display Value | character(1) | 불가 | — | 'N'::bpchar | Displays Value column with the Display column |
| 13 | `whereclause` | Sql WHERE | character varying(2000) | 허용 | — | — | Fully qualified SQL WHERE clause |
| 14 | `orderbyclause` | Sql ORDER BY | character varying(2000) | 허용 | — | — | Fully qualified ORDER BY clause |
| 15 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 16 | `ad_window_id` | Window | numeric(10,0) | 허용 | — | — | Data entry or display window |
| 17 | `ad_ref_table_uu` | AD_Ref_Table_UU | uuid | 허용 | — | — | — |
| 18 | `ad_infowindow_id` | Info Window | numeric(10,0) | 허용 | — | NULL::numeric | Info and search/select Window |
| 19 | `isdisplayidentifier` | Display Identifier | character(1) | 불가 | — | 'N'::bpchar | Display the record identifier |
| 20 | `displaysql` | Display SQL | character varying(4000) | 허용 | — | NULL::character varying | SQL for display of lookup value |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 9개 중 9개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_column"]
    n2["ad_entitytype"]
    n3["ad_infowindow"]
    n4["ad_org"]
    n5["ad_ref_table"]
    n6["ad_reference"]
    n7["ad_table"]
    n8["ad_window"]
    n5 -->|"ad_display → ad_column_id"| n1
    n5 -->|"ad_key → ad_column_id"| n1
    n5 -->|"ad_reference_id → ad_reference_id"| n6
    n5 -->|"ad_table_id → ad_table_id"| n7
    n5 -->|"ad_infowindow_id → ad_infowindow_id"| n3
    n5 -->|"ad_window_id → ad_window_id"| n8
    n5 -->|"entitytype → entitytype"| n2
    n5 -->|"ad_client_id → ad_client_id"| n0
    n5 -->|"ad_org_id → ad_org_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ad_column_reftable_display` <!-- FK_OUT: adempiere.ad_ref_table.ad_column_reftable_display --> | [`ad_ref_table`](ad_ref_table.md) | `ad_display` | [`ad_column`](ad_column.md) | `ad_column_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_column_reftable_id` <!-- FK_OUT: adempiere.ad_ref_table.ad_column_reftable_id --> | [`ad_ref_table`](ad_ref_table.md) | `ad_key` | [`ad_column`](ad_column.md) | `ad_column_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_reference_reftable` <!-- FK_OUT: adempiere.ad_ref_table.ad_reference_reftable --> | [`ad_ref_table`](ad_ref_table.md) | `ad_reference_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `add_table_reftable` <!-- FK_OUT: adempiere.ad_ref_table.add_table_reftable --> | [`ad_ref_table`](ad_ref_table.md) | `ad_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adinfowindow_adreftable` <!-- FK_OUT: adempiere.ad_ref_table.adinfowindow_adreftable --> | [`ad_ref_table`](ad_ref_table.md) | `ad_infowindow_id` | [`ad_infowindow`](ad_infowindow.md) | `ad_infowindow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwindow_adreftable` <!-- FK_OUT: adempiere.ad_ref_table.adwindow_adreftable --> | [`ad_ref_table`](ad_ref_table.md) | `ad_window_id` | [`ad_window`](ad_window.md) | `ad_window_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adreftable` <!-- FK_OUT: adempiere.ad_ref_table.entityt_adreftable --> | [`ad_ref_table`](ad_ref_table.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ref_tableclient` <!-- FK_OUT: adempiere.ad_ref_table.ref_tableclient --> | [`ad_ref_table`](ad_ref_table.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ref_tableorg` <!-- FK_OUT: adempiere.ad_ref_table.ref_tableorg --> | [`ad_ref_table`](ad_ref_table.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
