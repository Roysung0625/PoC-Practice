# ad_verifymigration — 마이그레이션 검증 보조

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_verifymigration` |
| 한국어 논리명(문서용 해석) | 마이그레이션 검증 보조 |
| 원본 논리명 | Verify Migration |
| 원본 사전 ID | 200382 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 21 |
| 나가는 FK / 들어오는 FK | 7 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

마이그레이션 검증을 지원하는 정보를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Verify Migration Helper
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_verifymigration_key` | `ad_verifymigration_id` |
| UNIQUE | `ad_verifymigration_uu_idx` | `ad_verifymigration_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_verifymigration_id` | Verify Migration | numeric(10,0) | 불가 | 예 | — | Verify Migration Helper |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `created` | Created | timestamp without time zone | 불가 | — | — | Date this record was created |
| 5 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 6 | `updated` | Updated | timestamp without time zone | 불가 | — | — | Date this record was updated |
| 7 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `ad_verifymigration_uu` | AD_VerifyMigration_UU | uuid | 허용 | — | — | — |
| 10 | `help` | Comment/Help | character varying(2000) | 허용 | — | NULL::character varying | Comment or Hint |
| 11 | `ad_pinstance_id` | Process Instance | numeric(10,0) | 불가 | — | — | Instance of the process |
| 12 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 13 | `record_id` | Record ID | numeric(10,0) | 허용 | — | NULL::numeric | Direct internal record ID |
| 14 | `seqno` | Sequence | numeric(10,0) | 허용 | — | NULL::numeric | Method of ordering records; lowest number comes first |
| 15 | `manualnote` | Note | character varying(4000) | 허용 | — | NULL::character varying | Note for manual entry |
| 16 | `expectedvalue` | Expected Value | character varying(4000) | 허용 | — | NULL::character varying | — |
| 17 | `currentvalue` | Current Value | character varying(4000) | 허용 | — | NULL::character varying | — |
| 18 | `priorityrule` | Priority | character(1) | 허용 | — | NULL::bpchar | Priority of a document |
| 19 | `isignore` | Ignore | character(1) | 불가 | — | 'N'::bpchar | — |
| 20 | `ad_column_id` | Column | numeric(10,0) | 허용 | — | NULL::numeric | Column in the table |
| 21 | `ad_changelog_id` | Change Log | numeric(10,0) | 허용 | — | NULL::numeric | Log of data changes |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_column"]
    n2["ad_org"]
    n3["ad_pinstance"]
    n4["ad_table"]
    n5["ad_user"]
    n6["ad_verifymigration"]
    n6 -->|"ad_client_id → ad_client_id"| n0
    n6 -->|"ad_column_id → ad_column_id"| n1
    n6 -->|"ad_org_id → ad_org_id"| n2
    n6 -->|"ad_pinstance_id → ad_pinstance_id"| n3
    n6 -->|"ad_table_id → ad_table_id"| n4
    n6 -->|"createdby → ad_user_id"| n5
    n6 -->|"updatedby → ad_user_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adclient_adverifymigration` <!-- FK_OUT: adempiere.ad_verifymigration.adclient_adverifymigration --> | [`ad_verifymigration`](ad_verifymigration.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adcolumn_adverifymigration` <!-- FK_OUT: adempiere.ad_verifymigration.adcolumn_adverifymigration --> | [`ad_verifymigration`](ad_verifymigration.md) | `ad_column_id` | [`ad_column`](ad_column.md) | `ad_column_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorg_adverifymigration` <!-- FK_OUT: adempiere.ad_verifymigration.adorg_adverifymigration --> | [`ad_verifymigration`](ad_verifymigration.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adpinstance_adverifymigration` <!-- FK_OUT: adempiere.ad_verifymigration.adpinstance_adverifymigration --> | [`ad_verifymigration`](ad_verifymigration.md) | `ad_pinstance_id` | [`ad_pinstance`](ad_pinstance.md) | `ad_pinstance_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtable_adverifymigration` <!-- FK_OUT: adempiere.ad_verifymigration.adtable_adverifymigration --> | [`ad_verifymigration`](ad_verifymigration.md) | `ad_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `createdby_adverifymigration` <!-- FK_OUT: adempiere.ad_verifymigration.createdby_adverifymigration --> | [`ad_verifymigration`](ad_verifymigration.md) | `createdby` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `updatedby_adverifymigration` <!-- FK_OUT: adempiere.ad_verifymigration.updatedby_adverifymigration --> | [`ad_verifymigration`](ad_verifymigration.md) | `updatedby` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

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
