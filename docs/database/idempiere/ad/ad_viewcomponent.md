# ad_viewcomponent — 데이터베이스 뷰 구성요소

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_viewcomponent` |
| 한국어 논리명(문서용 해석) | 데이터베이스 뷰 구성요소 |
| 원본 논리명 | Database View Component |
| 원본 사전 ID | 200087 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 229 |
| 물리 열 수 | 21 |
| 나가는 FK / 들어오는 FK | 3 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

뷰의 FROM·WHERE 등 SQL 구성과 참조 테이블·결합 옵션을 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_viewcomponent_key` | `ad_viewcomponent_id` |
| UNIQUE | `ad_viewcomponent_uu_idx` | `ad_viewcomponent_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 4 | `ad_viewcomponent_id` | Database View Component | numeric(10,0) | 불가 | 예 | — | — |
| 5 | `ad_viewcomponent_uu` | AD_ViewComponent_UU | uuid | 허용 | — | — | — |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 8 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 9 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 10 | `fromclause` | Sql FROM | character varying(4000) | 불가 | — | NULL::character varying | SQL FROM clause |
| 11 | `help` | Comment/Help | character varying(2000) | 허용 | — | NULL::character varying | Comment or Hint |
| 12 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 13 | `name` | Name | character varying(50) | 불가 | — | — | Alphanumeric identifier of the entity |
| 14 | `otherclause` | Other SQL Clause | character varying(2000) | 허용 | — | NULL::character varying | Other SQL Clause |
| 15 | `referenced_table_id` | Referenced Table | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 16 | `seqno` | Sequence | numeric(10,0) | 허용 | — | NULL::numeric | Method of ordering records; lowest number comes first |
| 17 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 18 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 19 | `whereclause` | Sql WHERE | character varying(2000) | 허용 | — | NULL::character varying | Fully qualified SQL WHERE clause |
| 20 | `isunionall` | Is UNION ALL | character(1) | 불가 | — | 'N'::bpchar | The component view is UNION ALL |
| 21 | `isdistinct` | Distinct | character(1) | 불가 | — | 'N'::bpchar | Select Distinct |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_entitytype"]
    n1["ad_table"]
    n2["ad_viewcolumn"]
    n3["ad_viewcomponent"]
    n3 -->|"ad_table_id → ad_table_id"| n1
    n3 -->|"entitytype → entitytype"| n0
    n3 -->|"referenced_table_id → ad_table_id"| n1
    n2 -->|"ad_viewcomponent_id → ad_viewcomponent_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adtable_adviewcomponent` <!-- FK_OUT: adempiere.ad_viewcomponent.adtable_adviewcomponent --> | [`ad_viewcomponent`](ad_viewcomponent.md) | `ad_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adviewcomponent` <!-- FK_OUT: adempiere.ad_viewcomponent.entityt_adviewcomponent --> | [`ad_viewcomponent`](ad_viewcomponent.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `referencedtable_adviewcomponen` <!-- FK_OUT: adempiere.ad_viewcomponent.referencedtable_adviewcomponen --> | [`ad_viewcomponent`](ad_viewcomponent.md) | `referenced_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adviewcomponent_adviewcolumn` <!-- FK_IN: adempiere.ad_viewcolumn.adviewcomponent_adviewcolumn --> | [`ad_viewcolumn`](ad_viewcolumn.md) | `ad_viewcomponent_id` | [`ad_viewcomponent`](ad_viewcomponent.md) | `ad_viewcomponent_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
