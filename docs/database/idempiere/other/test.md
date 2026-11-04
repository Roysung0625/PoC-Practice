# test — 자료형 시험

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.test` |
| 한국어 논리명(문서용 해석) | 자료형 시험 |
| 원본 논리명 | Test ID |
| 원본 사전 ID | 135 |
| 분류 | `other` — 접두사 공통 분류 없음 |
| 전체 테넌트 행 수 | 2 |
| 물리 열 수 | 36 |
| 나가는 FK / 들어오는 FK | 2 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

문자·숫자·날짜·금액·JSON 및 업무 참조 등 여러 자료형을 시험하는 테이블이다. 업무 원장으로 해석하지 않는다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `test_pkey` | `test_id` |
| UNIQUE | `test_uu_idx` | `test_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `test_id` | Test ID | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 12 | `t_integer` | Integer | numeric(10,0) | 허용 | — | — | — |
| 13 | `t_number` | Number | numeric | 허용 | — | 0 | — |
| 14 | `t_date` | Date | timestamp without time zone | 허용 | — | — | — |
| 15 | `t_datetime` | DateTime | timestamp without time zone | 허용 | — | — | — |
| 16 | `c_uom_id` | UOM | numeric(10,0) | 허용 | — | — | Unit of Measure |
| 17 | `t_qty` | Qty | numeric | 허용 | — | 0 | — |
| 18 | `c_currency_id` | Currency | numeric(10,0) | 허용 | — | — | The Currency for this record |
| 19 | `t_amount` | Amount | numeric | 허용 | — | 0 | — |
| 20 | `c_location_id` | Address | numeric(10,0) | 허용 | — | — | Location or Address |
| 21 | `account_acct` | Account_Acct | numeric(10,0) | 허용 | — | — | — |
| 22 | `c_payment_id` | Payment | numeric(10,0) | 허용 | — | — | Payment identifier |
| 23 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 24 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 25 | `m_locator_id` | Locator | numeric(10,0) | 허용 | — | — | Warehouse Locator |
| 26 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 27 | `binarydata` | Binary Data | bytea | 허용 | — | — | Binary Data |
| 28 | `processed` | Processed | character(1) | 허용 | — | 'N'::bpchar | The document has been processed |
| 29 | `characterdata` | Character Data | text | 허용 | — | — | Long Character Field |
| 30 | `test_uu` | Test_UU | uuid | 허용 | — | — | — |
| 31 | `color` | Color | character varying(7) | 허용 | — | NULL::character varying | — |
| 32 | `t_timestamp` | Timestamp | timestamp with time zone | 허용 | — | — | Timestamp with time zone |
| 33 | `ad_table_id` | Table | numeric(10,0) | 허용 | — | NULL::numeric | Database Table information |
| 34 | `record_id` | Record ID | numeric(10,0) | 허용 | — | NULL::numeric | Direct internal record ID |
| 35 | `record_uu` | Record UUID | uuid | 허용 | — | — | — |
| 36 | `jsondata` | JSON Data | jsonb | 허용 | — | — | The json field stores json data. |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 2개 중 2개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_table"]
    n1["c_validcombination"]
    n2["test"]
    n2 -->|"ad_table_id → ad_table_id"| n0
    n2 -->|"account_acct → c_validcombination_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adtable_test` <!-- FK_OUT: adempiere.test.adtable_test --> | [`test`](test.md) | `ad_table_id` | [`ad_table`](../ad/ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_account_test` <!-- FK_OUT: adempiere.test.vc_account_test --> | [`test`](test.md) | `account_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `record_id`는 가리키는 테이블이 메타데이터에 따라 달라질 수 있습니다. 물리 FK 목록에 없는 대상은 별도 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
