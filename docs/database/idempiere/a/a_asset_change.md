# a_asset_change — 자산 변경 기록

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.a_asset_change` |
| 한국어 논리명(문서용 해석) | 자산 변경 기록 |
| 원본 논리명 | A_Asset_Change_ID |
| 원본 사전 ID | 53133 |
| 분류 | `a` — 자산·감가상각 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 79 |
| 나가는 FK / 들어오는 FK | 16 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

자산의 변경 유형·일자와 금액·내용연수·회계 설정 등 변경 관련 정보를 기록한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `a_asset_change_pkey` | `a_asset_change_id` |
| UNIQUE | `a_asset_change_uu_idx` | `a_asset_change_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `a_asset_change_id` | A_Asset_Change_ID | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `a_asset_id` | Asset | numeric(10,0) | 불가 | — | — | Asset used internally or by customers |
| 10 | `changetype` | Change Type | character varying(3) | 불가 | — | — | — |
| 11 | `changedate` | Change Date | timestamp without time zone | 허용 | — | — | — |
| 12 | `changeamt` | Change Amt | numeric | 허용 | — | — | — |
| 13 | `uselifeyears` | Usable Life - Years | numeric | 허용 | — | — | Years of the usable life of the asset |
| 14 | `uselifemonths` | Usable Life - Months | numeric(10,0) | 허용 | — | — | Months of the usable life of the asset |
| 15 | `lifeuseunits` | Life use | numeric(10,0) | 허용 | — | — | Units of use until the asset is not usable anymore |
| 16 | `assetdepreciationdate` | Asset Depreciation Date | timestamp without time zone | 허용 | — | — | Date of last depreciation |
| 17 | `a_asset_retirement_id` | Asset Retirement | numeric(10,0) | 허용 | — | — | Internally used asset is not longer used. |
| 18 | `a_asset_addition_id` | Asset Addition | numeric(10,0) | 허용 | — | — | — |
| 19 | `serno` | Serial No | character varying(40) | 허용 | — | — | Product Serial Number  |
| 20 | `lot` | Lot No | character varying(40) | 허용 | — | — | Lot number (alphanumeric) |
| 21 | `versionno` | Version No | character varying(40) | 허용 | — | — | Version Number |
| 22 | `a_accumdepreciation_acct` | Accumulated Depreciation Account | numeric(10,0) | 허용 | — | — | — |
| 23 | `a_asset_createdate` | Create Date | timestamp without time zone | 허용 | — | — | — |
| 24 | `a_asset_spread_type` | Spread Type | character varying(10) | 허용 | — | — | — |
| 25 | `a_depreciation_calc_type` | Calculation Type | character varying(10) | 허용 | — | — | — |
| 26 | `a_depreciation_manual_period` | A_Depreciation_Manual_Period | character varying(2) | 허용 | — | — | — |
| 27 | `a_qty_original` | A_QTY_Original | numeric | 허용 | — | — | — |
| 28 | `a_qty_current` | Current Qty | numeric | 허용 | — | — | — |
| 29 | `a_period_start` | A_Period_Start | numeric(10,0) | 허용 | — | — | — |
| 30 | `a_period_end` | A_Period_End | numeric(10,0) | 허용 | — | — | — |
| 31 | `a_parent_asset_id` | Parent Asset | numeric(10,0) | 허용 | — | — | — |
| 32 | `a_disposal_revenue` | Disposal Revenue | character varying(22) | 허용 | — | — | — |
| 33 | `a_disposal_loss` | Loss on Disposal | character varying(22) | 허용 | — | — | — |
| 34 | `a_depreciation_variable_perc` | Variable Percent | numeric | 허용 | — | — | — |
| 35 | `a_depreciation_table_header_id` | A_Depreciation_Table_Header_ID | numeric(10,0) | 허용 | — | — | — |
| 36 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 허용 | — | — | Rules for accounting |
| 37 | `assetvalueamt` | Asset value | numeric | 불가 | — | (0)::numeric | Book Value of the asset |
| 38 | `assetservicedate` | In Service Date | timestamp without time zone | 허용 | — | — | Date when Asset was put into service |
| 39 | `assetmarketvalueamt` | Market value Amount | numeric | 허용 | — | — | Market value of the asset |
| 40 | `assetdisposaldate` | Asset Disposal Date | timestamp without time zone | 허용 | — | — | Date when the asset is/was disposed |
| 41 | `assetbookvalueamt` | Asset Book Value Amt | numeric | 허용 | — | — | — |
| 42 | `assetaccumdepreciationamt` | Asset Accum Depreciation Amt | numeric | 허용 | — | — | — |
| 43 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | — | User within the system - Internal or Business Partner Contact |
| 44 | `isinposession` | In Possession | character(1) | 허용 | — | — | The asset is in the possession of the organization |
| 45 | `isfullydepreciated` | Fully depreciated | character(1) | 허용 | — | — | The asset is fully depreciated |
| 46 | `isdisposed` | Disposed | character(1) | 허용 | — | — | The asset is disposed |
| 47 | `isdepreciated` | Depreciate | character(1) | 허용 | — | — | The asset will be depreciated |
| 48 | `depreciationtype` | Depreciation Type | character varying(10) | 허용 | — | — | — |
| 49 | `dateacct` | Account Date | timestamp without time zone | 허용 | — | — | Accounting Date |
| 50 | `useunits` | Use units | numeric(10,0) | 허용 | — | — | Currently used units of the assets |
| 51 | `textdetails` | Details | character varying(60) | 불가 | — | — | — |
| 52 | `postingtype` | Posting Type | character varying(10) | 허용 | — | 'A'::character varying | The type of posted amount for the transaction |
| 53 | `isowned` | Owned | character(1) | 허용 | — | — | The asset is owned by the organization |
| 54 | `conventiontype` | Convention Type | character varying(10) | 허용 | — | — | — |
| 55 | `c_validcombination_id` | Combination | numeric(10,0) | 허용 | — | — | Valid Account Combination |
| 56 | `c_location_id` | Address | numeric(10,0) | 허용 | — | — | Location or Address |
| 57 | `c_bpartner_location_id` | Partner Location | numeric(10,0) | 허용 | — | — | Identifies the (ship to) address for this Business Partner |
| 58 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 59 | `a_split_percent` | Split Percent | numeric | 허용 | — | (1)::numeric | — |
| 60 | `a_salvage_value` | Asset Salvage Value | numeric | 허용 | — | — | — |
| 61 | `a_reval_depexp_offset` | Revaluation Expense Offs | numeric(10,0) | 허용 | — | — | — |
| 62 | `a_reval_cost_offset_prior` | Revaluation Cost Offset for Prior Year | numeric(10,0) | 허용 | — | — | — |
| 63 | `a_reval_cost_offset` | Revaluation Cost Offset for Current Year | numeric(10,0) | 허용 | — | — | — |
| 64 | `a_reval_cal_method` | A_Reval_Cal_Method | character varying(3) | 허용 | — | — | — |
| 65 | `a_reval_accumdep_offset_prior` | Revaluation Accumulated Depreciation Offset for Prior Year | numeric(10,0) | 허용 | — | — | — |
| 66 | `a_reval_accumdep_offset_cur` | Revaluation Accumulated Depreciation Offset for Current Year | numeric(10,0) | 허용 | — | — | — |
| 67 | `a_depreciation_manual_amount` | A_Depreciation_Manual_Amount | numeric | 허용 | — | — | — |
| 68 | `a_depreciation_acct` | Depreciation Account | numeric(10,0) | 허용 | — | — | — |
| 69 | `a_asset_revaldate` | Revaluation Date | timestamp without time zone | 허용 | — | — | — |
| 70 | `a_asset_acct` | Asset Acct | numeric(10,0) | 허용 | — | — | — |
| 71 | `a_asset_acct_id` | A_Asset_Acct_ID | numeric(10,0) | 허용 | — | — | — |
| 72 | `a_asset_change_uu` | A_Asset_Change_UU | uuid | 허용 | — | — | — |
| 73 | `a_disposal_revenue_acct` | Disposal Revenue Acct | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 74 | `a_disposal_loss_acct` | Disposal Loss Acct | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 75 | `a_reval_depexp_offset_acct` | Reval Depexp Offset Acct | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 76 | `a_reval_cost_offset_prior_acct` | Reval Cost Offset Prior Acct | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 77 | `a_reval_cost_offset_acct` | Reval Cost Offset Acct | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 78 | `a_reval_adep_offset_prior_acct` | A_Reval_Accumdep_Offset_Prior | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 79 | `a_reval_adep_offset_cur_acct` | A_Reval_Accumdep_Offset_Cur | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 17개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset"]
    n1["a_asset_addition"]
    n2["a_asset_change"]
    n3["a_asset_retirement"]
    n4["a_depreciation_table_header"]
    n5["ad_user"]
    n6["c_validcombination"]
    n2 -->|"a_asset_addition_id → a_asset_addition_id"| n1
    n2 -->|"a_accumdepreciation_acct → c_validcombination_id"| n6
    n2 -->|"a_asset_retirement_id → a_asset_retirement_id"| n3
    n2 -->|"a_asset_id → a_asset_id"| n0
    n2 -->|"a_asset_acct → c_validcombination_id"| n6
    n2 -->|"a_depreciation_acct → c_validcombination_id"| n6
    n2 -->|"a_depreciation_table_header_id → a_depreciation_table_header_id"| n4
    n2 -->|"a_disposal_loss_acct → c_validcombination_id"| n6
    n2 -->|"a_disposal_revenue_acct → c_validcombination_id"| n6
    n2 -->|"ad_user_id → ad_user_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aaaddition_aachange` <!-- FK_OUT: adempiere.a_asset_change.aaaddition_aachange --> | [`a_asset_change`](a_asset_change.md) | `a_asset_addition_id` | [`a_asset_addition`](a_asset_addition.md) | `a_asset_addition_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aaccumdepreciation_aassetchang` <!-- FK_OUT: adempiere.a_asset_change.aaccumdepreciation_aassetchang --> | [`a_asset_change`](a_asset_change.md) | `a_accumdepreciation_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aaretirement_aachange` <!-- FK_OUT: adempiere.a_asset_change.aaretirement_aachange --> | [`a_asset_change`](a_asset_change.md) | `a_asset_retirement_id` | [`a_asset_retirement`](a_asset_retirement.md) | `a_asset_retirement_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aasset_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.aasset_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `a_asset_id` | [`a_asset`](a_asset.md) | `a_asset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aassetvc_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.aassetvc_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `a_asset_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adepreciation_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.adepreciation_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `a_depreciation_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adepreciationtableheader_aass2` <!-- FK_OUT: adempiere.a_asset_change.adepreciationtableheader_aass2 --> | [`a_asset_change`](a_asset_change.md) | `a_depreciation_table_header_id` | [`a_depreciation_table_header`](a_depreciation_table_header.md) | `a_depreciation_table_header_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adisposalloss_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.adisposalloss_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `a_disposal_loss_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adisposalrevenue_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.adisposalrevenue_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `a_disposal_revenue_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduser_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.aduser_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aparentasset_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.aparentasset_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `a_parent_asset_id` | [`a_asset`](a_asset.md) | `a_asset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cacctschema_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.cacctschema_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.cbpartner_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartnerlocation_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.cbpartnerlocation_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `c_bpartner_location_id` | [`c_bpartner_location`](../c/c_bpartner_location.md) | `c_bpartner_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `clocation_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.clocation_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `c_location_id` | [`c_location`](../c/c_location.md) | `c_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cvalidcombinati_aassetchange` <!-- FK_OUT: adempiere.a_asset_change.cvalidcombinati_aassetchange --> | [`a_asset_change`](a_asset_change.md) | `c_validcombination_id` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aassetchange_aassetchangeamt` <!-- FK_IN: adempiere.a_asset_change_amt.aassetchange_aassetchangeamt --> | [`a_asset_change_amt`](a_asset_change_amt.md) | `a_asset_change_id` | [`a_asset_change`](a_asset_change.md) | `a_asset_change_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
