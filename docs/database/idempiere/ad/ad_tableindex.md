# ad_tableindex — 테이블 인덱스

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_tableindex` |
| 한국어 논리명(문서용 해석) | 테이블 인덱스 |
| 원본 논리명 | Table Index |
| 원본 사전 ID | 200085 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 1,192 |
| 물리 열 수 | 20 |
| 나가는 FK / 들어오는 FK | 3 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

테이블의 인덱스 정의를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Index definition for table
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_tableindex_key` | `ad_tableindex_id` |
| UNIQUE | `ad_tableindex_uu_idx` | `ad_tableindex_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_tableindex_name`: `CREATE UNIQUE INDEX ad_tableindex_name ON adempiere.ad_tableindex USING btree (upper((name)::text))`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 4 | `ad_tableindex_id` | Table Index | numeric(10,0) | 불가 | 예 | — | — |
| 5 | `ad_tableindex_uu` | AD_TableIndex_UU | uuid | 허용 | — | — | — |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 8 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 9 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 10 | `help` | Comment/Help | character varying(2000) | 허용 | — | NULL::character varying | Comment or Hint |
| 11 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 12 | `iscreateconstraint` | Create Constraint | character(1) | 불가 | — | 'N'::bpchar | — |
| 13 | `isunique` | Unique | character(1) | 불가 | — | 'N'::bpchar | — |
| 14 | `name` | Name | character varying(63) | 불가 | — | — | Alphanumeric identifier of the entity |
| 15 | `processing` | Process Now | character(1) | 허용 | — | NULL::bpchar | — |
| 16 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 17 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 18 | `ad_message_id` | Message | numeric(10,0) | 허용 | — | NULL::numeric | System Message |
| 19 | `tableindexdrop` | Drop table index | character(1) | 허용 | — | NULL::bpchar | — |
| 20 | `iskey` | Key column | character(1) | 불가 | — | 'N'::bpchar | This column is the key in this table |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_entitytype"]
    n1["ad_indexcolumn"]
    n2["ad_message"]
    n3["ad_table"]
    n4["ad_tableindex"]
    n4 -->|"ad_message_id → ad_message_id"| n2
    n4 -->|"ad_table_id → ad_table_id"| n3
    n4 -->|"entitytype → entitytype"| n0
    n1 -->|"ad_tableindex_id → ad_tableindex_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `admessage_adtableindex` <!-- FK_OUT: adempiere.ad_tableindex.admessage_adtableindex --> | [`ad_tableindex`](ad_tableindex.md) | `ad_message_id` | [`ad_message`](ad_message.md) | `ad_message_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtable_adtableindex` <!-- FK_OUT: adempiere.ad_tableindex.adtable_adtableindex --> | [`ad_tableindex`](ad_tableindex.md) | `ad_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adtableindex` <!-- FK_OUT: adempiere.ad_tableindex.entityt_adtableindex --> | [`ad_tableindex`](ad_tableindex.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adtableindex_adindexcolumn` <!-- FK_IN: adempiere.ad_indexcolumn.adtableindex_adindexcolumn --> | [`ad_indexcolumn`](ad_indexcolumn.md) | `ad_tableindex_id` | [`ad_tableindex`](ad_tableindex.md) | `ad_tableindex_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
