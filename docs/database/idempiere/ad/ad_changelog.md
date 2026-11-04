# ad_changelog — 데이터 변경 로그

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_changelog` |
| 한국어 논리명(문서용 해석) | 데이터 변경 로그 |
| 원본 논리명 | Change Log |
| 원본 사전 ID | 580 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 22 |
| 나가는 FK / 들어오는 FK | 3 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

데이터 변경 내역을 기록한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Log of data changes
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_changelog_pkey` | `ad_session_id`, `ad_column_id`, `ad_changelog_id` |
| UNIQUE | `ad_changelog_uu_idx` | `ad_changelog_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_changelog_id` | Change Log | numeric(10,0) | 불가 | 예 | — | Log of data changes |
| 2 | `ad_session_id` | Session | numeric(10,0) | 불가 | 예 | — | User Session Online or Web |
| 3 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 4 | `ad_column_id` | Column | numeric(10,0) | 불가 | 예 | — | Column in the table |
| 5 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 6 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 7 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 8 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 9 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 10 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 11 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 12 | `record_id` | Record ID | numeric(10,0) | 허용 | — | — | Direct internal record ID |
| 13 | `oldvalue` | Old Value | character varying(4000) | 허용 | — | — | The old file data |
| 14 | `newvalue` | New Value | character varying(4000) | 허용 | — | — | New field value |
| 15 | `undo` | Undo | character(1) | 허용 | — | — | — |
| 16 | `redo` | Redo | character(1) | 허용 | — | — | — |
| 17 | `iscustomization` | Customization | character(1) | 불가 | — | 'N'::bpchar | The change is a customization of the data dictionary and can be applied after Migration |
| 18 | `trxname` | Transaction | character varying(1000) | 허용 | — | — | Name of the transaction |
| 19 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 20 | `eventchangelog` | Event Change Log | character(1) | 허용 | — | — | Type of Event in Change Log |
| 21 | `ad_changelog_uu` | AD_ChangeLog_UU | uuid | 허용 | — | — | — |
| 22 | `record_uu` | Record UUID | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 3개 중 3개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_changelog"]
    n1["ad_column"]
    n2["ad_session"]
    n3["ad_table"]
    n0 -->|"ad_column_id → ad_column_id"| n1
    n0 -->|"ad_session_id → ad_session_id"| n2
    n0 -->|"ad_table_id → ad_table_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adcolumn_adchangelog` <!-- FK_OUT: adempiere.ad_changelog.adcolumn_adchangelog --> | [`ad_changelog`](ad_changelog.md) | `ad_column_id` | [`ad_column`](ad_column.md) | `ad_column_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adsession_adchangelog` <!-- FK_OUT: adempiere.ad_changelog.adsession_adchangelog --> | [`ad_changelog`](ad_changelog.md) | `ad_session_id` | [`ad_session`](ad_session.md) | `ad_session_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtable_adchangelog` <!-- FK_OUT: adempiere.ad_changelog.adtable_adchangelog --> | [`ad_changelog`](ad_changelog.md) | `ad_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `record_id`는 가리키는 테이블이 메타데이터에 따라 달라질 수 있습니다. 물리 FK 목록에 없는 대상은 별도 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
