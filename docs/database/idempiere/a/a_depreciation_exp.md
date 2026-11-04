# a_depreciation_exp — 감가상각 작업 항목

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.a_depreciation_exp` |
| 한국어 논리명(문서용 해석) | 감가상각 작업 항목 |
| 원본 논리명 | A_Depreciation_Exp_ID |
| 원본 사전 ID | 53115 |
| 분류 | `a` — 자산·감가상각 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 38 |
| 나가는 FK / 들어오는 FK | 8 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

고정자산 관련 회계 항목과 예상치를 생성하는 작업 데이터를 보관한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: This table is the worktable for generating all fixed asset entries and forecasts
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `a_depreciation_exp_key` | `a_depreciation_exp_id` |
| UNIQUE | `a_depreciation_exp_uu_idx` | `a_depreciation_exp_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `a_depreciation_exp_id` | A_Depreciation_Exp_ID | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `a_entry_type` | Entry Type | character varying(3) | 불가 | — | — | — |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `dateacct` | Account Date | timestamp without time zone | 허용 | — | — | Accounting Date |
| 7 | `expense` | Expense | numeric | 불가 | — | (0)::numeric | — |
| 8 | `isdepreciated` | Depreciate | character(1) | 불가 | — | — | The asset will be depreciated |
| 9 | `processed` | Processed | character(1) | 불가 | — | — | The document has been processed |
| 10 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 11 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 12 | `postingtype` | Posting Type | character(1) | 허용 | — | 'A'::bpchar | The type of posted amount for the transaction |
| 13 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 14 | `description` | Description | character varying(255) | 불가 | — | — | Optional short description of the record |
| 15 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 16 | `a_period` | Asset Period | numeric(10,0) | 불가 | — | — | — |
| 17 | `a_asset_id` | Asset | numeric(10,0) | 불가 | — | — | Asset used internally or by customers |
| 18 | `a_depreciation_exp_uu` | A_Depreciation_Exp_UU | uuid | 허용 | — | — | — |
| 19 | `dr_account_id` | Account (debit) | numeric(10,0) | 허용 | — | NULL::numeric | Account used |
| 20 | `cr_account_id` | Account (credit) | numeric(10,0) | 허용 | — | NULL::numeric | Account used |
| 21 | `expense_f` | Expense (fiscal) | numeric | 불가 | — | (0)::numeric | — |
| 22 | `processing` | Process Now | character(1) | 허용 | — | NULL::bpchar | — |
| 23 | `help` | Comment/Help | character varying(2000) | 허용 | — | NULL::character varying | Comment or Hint |
| 24 | `a_asset_cost` | Asset Cost | numeric | 허용 | — | — | — |
| 25 | `a_accumulated_depr` | Accumulated Depreciation | numeric | 허용 | — | — | — |
| 26 | `a_accumulated_depr_f` | Accumulated Depreciation (fiscal) | numeric | 허용 | — | — | — |
| 27 | `uselifemonths` | Usable Life - Months | numeric(10,0) | 허용 | — | NULL::numeric | Months of the usable life of the asset |
| 28 | `uselifemonths_f` | Use Life - Months (fiscal) | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 29 | `a_asset_remaining` | Remaining Amt | numeric | 허용 | — | — | — |
| 30 | `a_asset_remaining_f` | Remaining Amt (fiscal) | numeric | 허용 | — | — | — |
| 31 | `a_asset_cost_delta` | Delta Asset Cost | numeric | 불가 | — | (0)::numeric | — |
| 32 | `a_accumulated_depr_delta` | Accumulated Depreciation (delta) | numeric | 불가 | — | (0)::numeric | — |
| 33 | `a_accumulated_depr_f_delta` | Accumulated Depreciation - fiscal (delta) | numeric | 불가 | — | (0)::numeric | — |
| 34 | `a_asset_addition_id` | Asset Addition | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 35 | `a_asset_disposed_id` | Asset Disposed | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 36 | `a_depreciation_entry_id` | Depreciation Entry | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 37 | `a_account_number_acct` | A_Account_Number_Acct | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 38 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 허용 | — | NULL::numeric | Rules for accounting |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset"]
    n1["a_asset_addition"]
    n2["a_asset_disposed"]
    n3["a_depreciation_entry"]
    n4["a_depreciation_exp"]
    n5["c_acctschema"]
    n6["c_validcombination"]
    n4 -->|"a_account_number_acct → c_validcombination_id"| n6
    n4 -->|"a_asset_id → a_asset_id"| n0
    n4 -->|"a_asset_addition_id → a_asset_addition_id"| n1
    n4 -->|"a_asset_disposed_id → a_asset_disposed_id"| n2
    n4 -->|"a_depreciation_entry_id → a_depreciation_entry_id"| n3
    n4 -->|"c_acctschema_id → c_acctschema_id"| n5
    n4 -->|"cr_account_id → c_validcombination_id"| n6
    n4 -->|"dr_account_id → c_validcombination_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aaccountnumber_adepreciationex` <!-- FK_OUT: adempiere.a_depreciation_exp.aaccountnumber_adepreciationex --> | [`a_depreciation_exp`](a_depreciation_exp.md) | `a_account_number_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aasset_adepreciationexp` <!-- FK_OUT: adempiere.a_depreciation_exp.aasset_adepreciationexp --> | [`a_depreciation_exp`](a_depreciation_exp.md) | `a_asset_id` | [`a_asset`](a_asset.md) | `a_asset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aassetaddition_adepreciationex` <!-- FK_OUT: adempiere.a_depreciation_exp.aassetaddition_adepreciationex --> | [`a_depreciation_exp`](a_depreciation_exp.md) | `a_asset_addition_id` | [`a_asset_addition`](a_asset_addition.md) | `a_asset_addition_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aassetdisposed_adepreciationex` <!-- FK_OUT: adempiere.a_depreciation_exp.aassetdisposed_adepreciationex --> | [`a_depreciation_exp`](a_depreciation_exp.md) | `a_asset_disposed_id` | [`a_asset_disposed`](a_asset_disposed.md) | `a_asset_disposed_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adepreciationentry_adepreciati` <!-- FK_OUT: adempiere.a_depreciation_exp.adepreciationentry_adepreciati --> | [`a_depreciation_exp`](a_depreciation_exp.md) | `a_depreciation_entry_id` | [`a_depreciation_entry`](a_depreciation_entry.md) | `a_depreciation_entry_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cacctschema_adepreciationexp` <!-- FK_OUT: adempiere.a_depreciation_exp.cacctschema_adepreciationexp --> | [`a_depreciation_exp`](a_depreciation_exp.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `craccou_adepreciationexp` <!-- FK_OUT: adempiere.a_depreciation_exp.craccou_adepreciationexp --> | [`a_depreciation_exp`](a_depreciation_exp.md) | `cr_account_id` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `draccou_adepreciationexp` <!-- FK_OUT: adempiere.a_depreciation_exp.draccou_adepreciationexp --> | [`a_depreciation_exp`](a_depreciation_exp.md) | `dr_account_id` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
