# a_asset_transfer — 자산 이동

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.a_asset_transfer` |
| 한국어 논리명(문서용 해석) | 자산 이동 |
| 원본 논리명 | A_Asset_Transfer_ID |
| 원본 사전 ID | 53128 |
| 분류 | `a` — 자산·감가상각 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 54 |
| 나가는 FK / 들어오는 FK | 15 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

자산 이동과 이에 따른 회계 항목 생성에 필요한 정보를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: This table holds all necessary information to process asset transfers and create the appropriate entry
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `a_asset_transfer_key` | `a_asset_transfer_id` |
| UNIQUE | `a_asset_transfer_uu_idx` | `a_asset_transfer_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `a_asset_acct_id` | A_Asset_Acct_ID | numeric(10,0) | 허용 | — | — | — |
| 2 | `a_asset_transfer_id` | A_Asset_Transfer_ID | numeric(10,0) | 불가 | 예 | — | — |
| 3 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 4 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 5 | `a_accumdepreciation_acct` | Accumulated Depreciation Account | numeric(10,0) | 허용 | — | — | — |
| 6 | `a_asset_acct_new` | New Asset Cost Acct | character varying(22) | 허용 | — | — | — |
| 7 | `a_depreciation_acct` | Depreciation Account | numeric(10,0) | 허용 | — | — | — |
| 8 | `a_depreciation_acct_str` | A_Depreciation_Acct_Str | character varying(40) | 허용 | — | — | — |
| 9 | `a_disposal_loss_new` | New Disposal Loss | character varying(22) | 허용 | — | — | — |
| 10 | `a_transfer_balance_is` | A_Transfer_Balance_IS | character(1) | 불가 | — | — | — |
| 11 | `a_transfer_balance` | A_Transfer_Balance | character(1) | 불가 | — | 'Y'::bpchar | — |
| 12 | `a_split_percent` | Split Percent | numeric | 불가 | — | (1)::numeric | — |
| 13 | `a_period_start` | A_Period_Start | numeric(10,0) | 불가 | — | — | — |
| 14 | `a_period_end` | A_Period_End | numeric(10,0) | 불가 | — | — | — |
| 15 | `a_disposal_revenue_str` | Disposal Revenue Str | character varying(40) | 허용 | — | — | — |
| 16 | `a_disposal_revenue_new` | New Disposal Revenue | character varying(22) | 허용 | — | — | — |
| 17 | `a_disposal_revenue` | Disposal Revenue | numeric(10,0) | 허용 | — | — | — |
| 18 | `a_disposal_loss_str` | Disposal Loss Str | character varying(40) | 허용 | — | — | — |
| 19 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 20 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 21 | `processing` | Process Now | character(1) | 불가 | — | 'N'::bpchar | — |
| 22 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 23 | `postingtype` | Posting Type | character(1) | 불가 | — | 'A'::bpchar | The type of posted amount for the transaction |
| 24 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 25 | `dateacct` | Account Date | timestamp without time zone | 불가 | — | — | Accounting Date |
| 26 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 27 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 28 | `c_period_id` | Period | numeric(10,0) | 허용 | — | — | Period of the Calendar |
| 29 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 불가 | — | — | Rules for accounting |
| 30 | `a_disposal_loss` | Loss on Disposal | numeric(10,0) | 허용 | — | — | — |
| 31 | `a_depreciation_acct_new` | New Depreciation Exp Acct | character varying(22) | 허용 | — | — | — |
| 32 | `a_asset_id` | Asset | numeric(10,0) | 불가 | — | — | Asset used internally or by customers |
| 33 | `a_asset_acct_str` | A_Asset_Acct_Str | character varying(40) | 허용 | — | — | — |
| 34 | `a_accumdepreciation_acct_new` | New Accum Depreciation Acct | character varying(22) | 허용 | — | — | — |
| 35 | `a_accumdepreciation_acct_str` | Old Asset Cost Acct | character varying(40) | 허용 | — | — | — |
| 36 | `a_asset_acct` | Asset Acct | numeric(10,0) | 허용 | — | — | — |
| 37 | `a_asset_transfer_uu` | A_Asset_Transfer_UU | uuid | 허용 | — | — | — |
| 38 | `a_accumdepreciation_new_acct` | Accumulated Depreciation Account (new) | numeric(10,0) | 불가 | — | — | — |
| 39 | `a_depreciation_new_acct` | Depreciation Acct (new) | numeric(10,0) | 불가 | — | — | — |
| 40 | `a_disposal_loss_acct` | Disposal Loss Acct | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 41 | `a_disposal_revenue_new_acct` | Disposal Revenue Acct (new) | numeric(10,0) | 불가 | — | — | — |
| 42 | `a_disposal_revenue_acct` | Disposal Revenue Acct | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 43 | `a_disposal_loss_new_acct` | Disposal Loss Acct (new) | numeric(10,0) | 불가 | — | — | — |
| 44 | `a_asset_new_acct` | Asset Acct (new) | numeric(10,0) | 불가 | — | — | — |
| 45 | `docaction` | Document Action | character(2) | 불가 | — | 'CO'::bpchar | The targeted status of the document |
| 46 | `docstatus` | Document Status | character varying(2) | 불가 | — | 'DR'::character varying | The current status of the document |
| 47 | `posted` | Posted | character(1) | 허용 | — | NULL::bpchar | Posting status |
| 48 | `a_capvsexp` | Capital/Expense | character varying(3) | 불가 | — | 'Cap'::character varying | — |
| 49 | `a_accumulated_depr_f` | Accumulated Depreciation (fiscal) | numeric | 허용 | — | — | — |
| 50 | `documentno` | Document No | character varying(30) | 허용 | — | NULL::character varying | Document sequence number of the document |
| 51 | `datedoc` | Document Date | timestamp without time zone | 허용 | — | — | Date of the Document |
| 52 | `processedon` | Processed On | numeric | 허용 | — | — | The date+time (expressed in decimal format) when the document has been processed |
| 53 | `c_costcenter_id` | Cost Center | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 54 | `c_department_id` | Department | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 15개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset"]
    n1["a_asset_transfer"]
    n2["c_validcombination"]
    n1 -->|"a_accumdepreciation_acct → c_validcombination_id"| n2
    n1 -->|"a_accumdepreciation_new_acct → c_validcombination_id"| n2
    n1 -->|"a_asset_id → a_asset_id"| n0
    n1 -->|"a_asset_new_acct → c_validcombination_id"| n2
    n1 -->|"a_asset_acct → c_validcombination_id"| n2
    n1 -->|"a_depreciation_acct → c_validcombination_id"| n2
    n1 -->|"a_depreciation_new_acct → c_validcombination_id"| n2
    n1 -->|"a_disposal_loss_acct → c_validcombination_id"| n2
    n1 -->|"a_disposal_loss_new_acct → c_validcombination_id"| n2
    n1 -->|"a_disposal_revenue_acct → c_validcombination_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aaccumdepreciation_aassettrans` <!-- FK_OUT: adempiere.a_asset_transfer.aaccumdepreciation_aassettrans --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_accumdepreciation_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aaccumdepreciationnew_aassettr` <!-- FK_OUT: adempiere.a_asset_transfer.aaccumdepreciationnew_aassettr --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_accumdepreciation_new_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aasset_aassettransfer` <!-- FK_OUT: adempiere.a_asset_transfer.aasset_aassettransfer --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_asset_id` | [`a_asset`](a_asset.md) | `a_asset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aassetnew_aassettransfer` <!-- FK_OUT: adempiere.a_asset_transfer.aassetnew_aassettransfer --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_asset_new_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aassetvc_aassettransfer` <!-- FK_OUT: adempiere.a_asset_transfer.aassetvc_aassettransfer --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_asset_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adepreciation_aassettransfer` <!-- FK_OUT: adempiere.a_asset_transfer.adepreciation_aassettransfer --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_depreciation_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adepreciationnew_aassettransfe` <!-- FK_OUT: adempiere.a_asset_transfer.adepreciationnew_aassettransfe --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_depreciation_new_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adisposalloss_aassettransfer` <!-- FK_OUT: adempiere.a_asset_transfer.adisposalloss_aassettransfer --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_disposal_loss_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adisposallossnew_aassettransfe` <!-- FK_OUT: adempiere.a_asset_transfer.adisposallossnew_aassettransfe --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_disposal_loss_new_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adisposalrevenue_aassettransfe` <!-- FK_OUT: adempiere.a_asset_transfer.adisposalrevenue_aassettransfe --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_disposal_revenue_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adisposalrevenuenew_aassettran` <!-- FK_OUT: adempiere.a_asset_transfer.adisposalrevenuenew_aassettran --> | [`a_asset_transfer`](a_asset_transfer.md) | `a_disposal_revenue_new_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cacctschema_aassettransfer` <!-- FK_OUT: adempiere.a_asset_transfer.cacctschema_aassettransfer --> | [`a_asset_transfer`](a_asset_transfer.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccostcenter_aassettransfer` <!-- FK_OUT: adempiere.a_asset_transfer.ccostcenter_aassettransfer --> | [`a_asset_transfer`](a_asset_transfer.md) | `c_costcenter_id` | [`c_costcenter`](../c/c_costcenter.md) | `c_costcenter_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdepartment_aassettransfer` <!-- FK_OUT: adempiere.a_asset_transfer.cdepartment_aassettransfer --> | [`a_asset_transfer`](a_asset_transfer.md) | `c_department_id` | [`c_department`](../c/c_department.md) | `c_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_aassettransfer` <!-- FK_OUT: adempiere.a_asset_transfer.cperiod_aassettransfer --> | [`a_asset_transfer`](a_asset_transfer.md) | `c_period_id` | [`c_period`](../c/c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
