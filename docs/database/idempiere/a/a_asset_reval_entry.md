# a_asset_reval_entry — 자산 재평가 처리 항목

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.a_asset_reval_entry` |
| 한국어 논리명(문서용 해석) | 자산 재평가 처리 항목 |
| 원본 논리명 | Asset Reval. Entry |
| 원본 사전 ID | 53119 |
| 분류 | `a` — 자산·감가상각 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 26 |
| 나가는 FK / 들어오는 FK | 5 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

자산 재평가를 처리하는 데 필요한 정보를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: This table holds all necessary information to process asset revaluations
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `a_asset_reval_entry_key` | `a_asset_reval_entry_id` |
| UNIQUE | `a_asset_reval_entry_uu_idx` | `a_asset_reval_entry_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `a_asset_reval_entry_id` | Asset Reval. Entry | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `a_effective_date` | Effective Date | timestamp without time zone | 불가 | — | — | — |
| 4 | `a_reval_cal_method` | A_Reval_Cal_Method | character varying(3) | 불가 | — | — | — |
| 5 | `a_reval_multiplier` | Reval. Multiplier | character varying(3) | 불가 | — | — | — |
| 6 | `c_currency_id` | Currency | numeric(10,0) | 불가 | — | — | The Currency for this record |
| 7 | `c_period_id` | Period | numeric(10,0) | 허용 | — | — | Period of the Calendar |
| 8 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 9 | `datedoc` | Document Date | timestamp without time zone | 허용 | — | — | Date of the Document |
| 10 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 11 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 12 | `processing` | Process Now | character(1) | 불가 | — | — | — |
| 13 | `processed` | Processed | character(1) | 불가 | — | — | The document has been processed |
| 14 | `postingtype` | Posting Type | character(1) | 불가 | — | — | The type of posted amount for the transaction |
| 15 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 16 | `gl_category_id` | GL Category | numeric(10,0) | 허용 | — | — | General Ledger Category |
| 17 | `documentno` | Document No | character varying(60) | 불가 | — | — | Document sequence number of the document |
| 18 | `description` | Description | character varying(510) | 불가 | — | — | Optional short description of the record |
| 19 | `dateacct` | Account Date | timestamp without time zone | 허용 | — | — | Accounting Date |
| 20 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 21 | `c_doctype_id` | Document Type | numeric(10,0) | 허용 | — | — | Document type or rules |
| 22 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 허용 | — | — | Rules for accounting |
| 23 | `a_reval_effective_date` | Reval. Effective Date | character varying(2) | 불가 | — | — | — |
| 24 | `a_rev_code` | Rev. Code | character varying(3) | 불가 | — | — | — |
| 25 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 26 | `a_asset_reval_entry_uu` | A_Asset_Reval_Entry_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset_reval_entry"]
    n1["c_acctschema"]
    n2["c_currency"]
    n3["c_doctype"]
    n4["c_period"]
    n5["gl_category"]
    n0 -->|"c_acctschema_id → c_acctschema_id"| n1
    n0 -->|"c_currency_id → c_currency_id"| n2
    n0 -->|"c_doctype_id → c_doctype_id"| n3
    n0 -->|"c_period_id → c_period_id"| n4
    n0 -->|"gl_category_id → gl_category_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cacctschema_aassetrevalentry` <!-- FK_OUT: adempiere.a_asset_reval_entry.cacctschema_aassetrevalentry --> | [`a_asset_reval_entry`](a_asset_reval_entry.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_aassetrevalentry` <!-- FK_OUT: adempiere.a_asset_reval_entry.ccurrency_aassetrevalentry --> | [`a_asset_reval_entry`](a_asset_reval_entry.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_aassetrevalentry` <!-- FK_OUT: adempiere.a_asset_reval_entry.cdoctype_aassetrevalentry --> | [`a_asset_reval_entry`](a_asset_reval_entry.md) | `c_doctype_id` | [`c_doctype`](../c/c_doctype.md) | `c_doctype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_aassetrevalentry` <!-- FK_OUT: adempiere.a_asset_reval_entry.cperiod_aassetrevalentry --> | [`a_asset_reval_entry`](a_asset_reval_entry.md) | `c_period_id` | [`c_period`](../c/c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_aassetrevalentry` <!-- FK_OUT: adempiere.a_asset_reval_entry.glcategory_aassetrevalentry --> | [`a_asset_reval_entry`](a_asset_reval_entry.md) | `gl_category_id` | [`gl_category`](../gl/gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
