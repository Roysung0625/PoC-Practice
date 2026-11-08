# ERP 업무영역 분류 overlay — 항목별 근거

[전체 일람](index.md) · [분류 규칙](semantic_classification.py) · [기계 판독 근거](semantic-classification.json) · [에이전트 표본 검토](semantic-sample-review.json)

DB 메타데이터 기준 2026-11-08T16:14:17+09:00; 원본 사전/문서 스냅샷 2026-11-03T23:29:01+09:00. 분류 근거는 이 메타데이터와 원본 사전·열·FK의 교차대조이며, 실제 구조 수집 여부와 실행 모드는 정합성 보고에서 별도로 확인합니다.

전체 912개 중 근거 기반 분류안 **730개**, 확인 필요 **182개**입니다. 공식 분류·업무 담당자 승인 0개이며, 원본 MD의 폴더/영역 표시는 기존 생성기의 분류안입니다. 새 overlay와 달라도 원본이 검증된 업무 분류라는 의미가 아닙니다.

## 방법과 한계

- 자동 규칙은 원본 AD_Table의 Name/Description 의미를 먼저 찾고, 일반 감사/테넌트 열과 PK·표준 UUID를 제외한 주요 열 또는 관련 테이블의 사전 의미가 합치하는 검증된 물리 FK를 별도로 요구합니다. 테이블명 접두어는 점수에 쓰지 않습니다.
- 사전 의미와 구조 근거가 모두 없거나 영역 근거 점수가 같으면 확인 필요로 남깁니다. Import/Report/Manufacturing/Payroll/Quality/Workflow처럼 사전에 명시된 용도는 같은 구조 근거를 가진 후보 안에서 세부 목적을 구분합니다. 이러한 의미 규칙도 공식 분류가 아닙니다.
- 숫자 점수는 사전 단어와 근거 개수의 결정적 선택 규칙이며 정확도/확률이 아닙니다. 모호한 테이블을 분류 수에 맞추기 위해 확정하지 않습니다. FK는 참조 관계이고 업무의 실행 순서·계산·권한 동작을 보장하지 않습니다.
- 사전+주요 열+FK 465개, 사전+주요 열 47개, 사전+FK 218개입니다. 제안 중 Description도 있는 것은 458개이며 나머지는 Name과 구조 근거를 사용했습니다.
- 자동 교차대조 912개와 에이전트 메타데이터 표본 검토 24개를 구분합니다. 사람이 공식 검증한 항목은 없습니다. 표본 검토는 전체 ERP 업무 로직 실행 검증을 뜻하지 않습니다.

<a id="t-a_asset"></a>
## `a_asset` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset`
- 사전 Description: Asset used internally or by customers
- 근거 문장: 사전 Name='Asset'; Description='Asset used internally or by customers'; 주요 열 a_asset_group_id, assetservicedate, assetdepreciationdate, uselifeyears; FK aasset_aassetacct, aasset_aassetaddition; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_group_id` | Asset Group | `numeric(10,0)` |
| `assetservicedate` | In Service Date | `timestamp without time zone` |
| `assetdepreciationdate` | Asset Depreciation Date | `timestamp without time zone` |
| `uselifeyears` | Usable Life - Years | `numeric` |
| `uselifemonths` | Usable Life - Months | `numeric(10,0)` |
| `assetdisposaldate` | Asset Disposal Date | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aasset_aassetacct` | `a_asset_acct.(a_asset_id)` → `a_asset.(a_asset_id)` | A_Asset_Acct_ID |
| incoming | `aasset_aassetaddition` | `a_asset_addition.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset Addition |
| incoming | `aasset_aassetchange` | `a_asset_change.(a_asset_id)` → `a_asset.(a_asset_id)` | A_Asset_Change_ID |
| incoming | `aasset_aassetdelivery` | `a_asset_delivery.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset Delivery |

<a id="t-a_asset_acct"></a>
## `a_asset_acct` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Asset_Acct_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Asset_Acct_ID'; 주요 열 a_asset_id, c_acctschema_id, a_depreciation_id, a_depreciation_acct; FK aaccumdepreciation_aassetacct, aasset_aassetacct; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `a_depreciation_id` | Depreciation | `numeric(10,0)` |
| `a_depreciation_acct` | Depreciation Account | `numeric(10,0)` |
| `a_accumdepreciation_acct` | Accumulated Depreciation Account | `numeric(10,0)` |
| `a_disposal_loss` | Loss on Disposal | `character varying(40)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aaccumdepreciation_aassetacct` | `a_asset_acct.(a_accumdepreciation_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `aasset_aassetacct` | `a_asset_acct.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |
| outgoing | `aassetspread_aassetacct` | `a_asset_acct.(a_asset_spread_id)` → `a_asset_spread.(a_asset_spread_id)` | A_Asset_Spread_ID |
| outgoing | `aassetvc_aassetacct` | `a_asset_acct.(a_asset_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

검토 후보: 회계·원장·예산 (규칙 점수 13); 자산·감가상각 (규칙 점수 13).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-a_asset_addition"></a>
## `a_asset_addition` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Addition`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Addition'; 주요 열 a_asset_id, assetvalueamt, a_createasset, assetsourceamt; FK aaaddition_aachange, aassetaddition_adepreciationex; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |
| `assetvalueamt` | Asset value | `numeric` |
| `a_createasset` | Create Asset | `character(1)` |
| `assetsourceamt` | Source Amount | `numeric` |
| `deltauselifeyears` | Delta Use Life Years | `numeric(10,0)` |
| `deltauselifeyears_f` | Delta Use Life Years (fiscal) | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aaaddition_aachange` | `a_asset_change.(a_asset_addition_id)` → `a_asset_addition.(a_asset_addition_id)` | A_Asset_Change_ID |
| incoming | `aassetaddition_adepreciationex` | `a_depreciation_exp.(a_asset_addition_id)` → `a_asset_addition.(a_asset_addition_id)` | A_Depreciation_Exp_ID |
| outgoing | `aasset_aassetaddition` | `a_asset_addition.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |
| outgoing | `ifixedasset_aassetaddition` | `a_asset_addition.(i_fixedasset_id)` → `i_fixedasset.(i_fixedasset_id)` | Imported Fixed Asset |

<a id="t-a_asset_change"></a>
## `a_asset_change` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Asset_Change_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Asset_Change_ID'; 주요 열 a_asset_id, uselifeyears, uselifemonths, assetdepreciationdate; FK aaaddition_aachange, aaretirement_aachange; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |
| `uselifeyears` | Usable Life - Years | `numeric` |
| `uselifemonths` | Usable Life - Months | `numeric(10,0)` |
| `assetdepreciationdate` | Asset Depreciation Date | `timestamp without time zone` |
| `a_asset_retirement_id` | Asset Retirement | `numeric(10,0)` |
| `a_asset_addition_id` | Asset Addition | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aaaddition_aachange` | `a_asset_change.(a_asset_addition_id)` → `a_asset_addition.(a_asset_addition_id)` | Asset Addition |
| outgoing | `aaretirement_aachange` | `a_asset_change.(a_asset_retirement_id)` → `a_asset_retirement.(a_asset_retirement_id)` | Asset Retirement |
| outgoing | `aasset_aassetchange` | `a_asset_change.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |
| outgoing | `adepreciationtableheader_aass2` | `a_asset_change.(a_depreciation_table_header_id)` → `a_depreciation_table_header.(a_depreciation_table_header_id)` | A_Depreciation_Table_Header_ID |

<a id="t-a_asset_change_amt"></a>
## `a_asset_change_amt` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 assetvalueamt, assetmarketvalueamt, assetbookvalueamt, assetaccumdepreciationamt; FK aassetchange_aassetchangeamt, cacctschema_aassetchangeamt; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `assetvalueamt` | 미지정 | `numeric` |
| `assetmarketvalueamt` | 미지정 | `numeric` |
| `assetbookvalueamt` | 미지정 | `numeric` |
| `assetaccumdepreciationamt` | 미지정 | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aassetchange_aassetchangeamt` | `a_asset_change_amt.(a_asset_change_id)` → `a_asset_change.(a_asset_change_id)` | A_Asset_Change_ID |
| outgoing | `cacctschema_aassetchangeamt` | `a_asset_change_amt.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-a_asset_class"></a>
## `a_asset_class` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset class`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset class'; 주요 열 근거 부족; FK aassetclass_aasset, aassetclass_aassetgroup; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aassetclass_aasset` | `a_asset.(a_asset_class_id)` → `a_asset_class.(a_asset_class_id)` | Asset |
| incoming | `aassetclass_aassetgroup` | `a_asset_group.(a_asset_class_id)` → `a_asset_class.(a_asset_class_id)` | Asset Group |
| incoming | `aassetclass_ifixedasset` | `i_fixedasset.(a_asset_class_id)` → `a_asset_class.(a_asset_class_id)` | Imported Fixed Asset |

<a id="t-a_asset_delivery"></a>
## `a_asset_delivery` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Delivery`
- 사전 Description: Delivery of Asset
- 근거 문장: 사전 Name='Asset Delivery'; Description='Delivery of Asset'; 주요 열 a_asset_id; FK aasset_aassetdelivery; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aasset_aassetdelivery` | `a_asset_delivery.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_asset_disposed"></a>
## `a_asset_disposed` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Disposed`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Disposed'; 주요 열 a_asset_id, a_asset_trade_id, a_asset_status, a_disposal_amt; FK aassetdisposed_adepreciationex, aasset_aassetdisposed; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |
| `a_asset_trade_id` | Asset Trade | `numeric(10,0)` |
| `a_asset_status` | Asset Status | `character varying(2)` |
| `a_disposal_amt` | Disposal Amount | `numeric` |
| `a_asset_cost` | Asset Cost | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aassetdisposed_adepreciationex` | `a_depreciation_exp.(a_asset_disposed_id)` → `a_asset_disposed.(a_asset_disposed_id)` | A_Depreciation_Exp_ID |
| outgoing | `aasset_aassetdisposed` | `a_asset_disposed.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |
| outgoing | `aassettrade_aassetdisposed` | `a_asset_disposed.(a_asset_trade_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_asset_group"></a>
## `a_asset_group` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Group`
- 사전 Description: Group of Assets
- 근거 문장: 사전 Name='Asset Group'; Description='Group of Assets'; 주요 열 isdepreciated, isoneassetperuom, a_asset_class_id, a_asset_type_id; FK aassetgroup_aasset, aassetgroup_aassetgroupacct; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isdepreciated` | Depreciate | `character(1)` |
| `isoneassetperuom` | One Asset Per UOM | `character(1)` |
| `a_asset_class_id` | Asset class | `numeric(10,0)` |
| `a_asset_type_id` | Asset Type | `numeric(10,0)` |
| `isfixedasset` | Is Fixed Asset | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aassetgroup_aasset` | `a_asset.(a_asset_group_id)` → `a_asset_group.(a_asset_group_id)` | Asset |
| incoming | `aassetgroup_aassetgroupacct` | `a_asset_group_acct.(a_asset_group_id)` → `a_asset_group.(a_asset_group_id)` | Asset Group Accounting |
| incoming | `aassetgroup_aassetgrouptrl` | `a_asset_group_trl.(a_asset_group_id)` → `a_asset_group.(a_asset_group_id)` | Asset Group Trl |
| incoming | `aassetgroup_iasset` | `i_asset.(a_asset_group_id)` → `a_asset_group.(a_asset_group_id)` | Asset |

<a id="t-a_asset_group_acct"></a>
## `a_asset_group_acct` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Group Accounting`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Group Accounting'; 주요 열 a_asset_group_id, c_acctschema_id, a_asset_acct, a_depreciation_acct; FK aaccumdepreciation_aassetgroup, aasset_aassetgroupacct; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_group_id` | Asset Group | `numeric(10,0)` |
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `a_asset_acct` | Asset Acct | `numeric(10,0)` |
| `a_depreciation_acct` | Depreciation Account | `numeric(10,0)` |
| `a_accumdepreciation_acct` | Accumulated Depreciation Account | `numeric(10,0)` |
| `a_disposal_loss` | Loss on Disposal | `character varying(22)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aaccumdepreciation_aassetgroup` | `a_asset_group_acct.(a_accumdepreciation_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `aasset_aassetgroupacct` | `a_asset_group_acct.(a_asset_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `aassetgroup_aassetgroupacct` | `a_asset_group_acct.(a_asset_group_id)` → `a_asset_group.(a_asset_group_id)` | Asset Group |
| outgoing | `adepreciation_aassetgroupacct` | `a_asset_group_acct.(a_depreciation_id)` → `a_depreciation.(a_depreciation_id)` | Depreciation |

검토 후보: 회계·원장·예산 (규칙 점수 13); 자산·감가상각 (규칙 점수 13).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-a_asset_group_trl"></a>
## `a_asset_group_trl` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Group Trl`
- 사전 Description: Group of Assets
- 근거 문장: 사전 Name='Asset Group Trl'; Description='Group of Assets'; 주요 열 근거 부족; FK aassetgroup_aassetgrouptrl; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aassetgroup_aassetgrouptrl` | `a_asset_group_trl.(a_asset_group_id)` → `a_asset_group.(a_asset_group_id)` | Asset Group |

<a id="t-a_asset_info_fin"></a>
## `a_asset_info_fin` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Info Financial ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Info Financial ID'; 주요 열 a_asset_id; FK aasset_aassetinfofin; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aasset_aassetinfofin` | `a_asset_info_fin.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_asset_info_ins"></a>
## `a_asset_info_ins` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Asset_Info_Ins_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Asset_Info_Ins_ID'; 주요 열 a_asset_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-a_asset_info_lic"></a>
## `a_asset_info_lic` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Asset_Info_Lic_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Asset_Info_Lic_ID'; 주요 열 a_asset_id; FK aasset_aassetinfolic; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aasset_aassetinfolic` | `a_asset_info_lic.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_asset_info_oth"></a>
## `a_asset_info_oth` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Asset_Info_Oth_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Asset_Info_Oth_ID'; 주요 열 a_asset_id, a_asset_info_oth_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |
| `a_asset_info_oth_id` | A_Asset_Info_Oth_ID | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-a_asset_info_tax"></a>
## `a_asset_info_tax` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Info Tax`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Info Tax'; 주요 열 a_asset_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-a_asset_product"></a>
## `a_asset_product` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Product`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Product'; 주요 열 m_product_id, m_attributesetinstance_id; FK mattributesetinstance_aassetpr, mproduct_aassetproduct; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_product_id` | Product | `numeric(10,0)` |
| `m_attributesetinstance_id` | Attribute Set Instance | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mattributesetinstance_aassetpr` | `a_asset_product.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |
| outgoing | `mproduct_aassetproduct` | `a_asset_product.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-a_asset_retirement"></a>
## `a_asset_retirement` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Retirement`
- 사전 Description: Internally used asset is not longer used.
- 근거 문장: 사전 Name='Asset Retirement'; Description='Internally used asset is not longer used.'; 주요 열 a_asset_id, assetvalueamt, assetmarketvalueamt; FK aaretirement_aachange, aasset_aassetretirement; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |
| `assetvalueamt` | Asset value | `numeric` |
| `assetmarketvalueamt` | Market value Amount | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aaretirement_aachange` | `a_asset_change.(a_asset_retirement_id)` → `a_asset_retirement.(a_asset_retirement_id)` | A_Asset_Change_ID |
| outgoing | `aasset_aassetretirement` | `a_asset_retirement.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_asset_reval"></a>
## `a_asset_reval` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Revaluation`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Revaluation'; 주요 열 a_asset_id, a_asset_cost, a_asset_cost_change; FK aasset_aassetreval; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |
| `a_asset_cost` | Asset Cost | `numeric` |
| `a_asset_cost_change` | Asset Cost Change | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aasset_aassetreval` | `a_asset_reval.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_asset_reval_entry"></a>
## `a_asset_reval_entry` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Reval. Entry`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Reval. Entry'; 주요 열 a_reval_cal_method, a_reval_multiplier, a_reval_effective_date; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_reval_cal_method` | A_Reval_Cal_Method | `character varying(3)` |
| `a_reval_multiplier` | Reval. Multiplier | `character varying(3)` |
| `a_reval_effective_date` | Reval. Effective Date | `character varying(2)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-a_asset_reval_index"></a>
## `a_asset_reval_index` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Reval Index`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Reval Index'; 주요 열 a_reval_multiplier, a_reval_rate, a_reval_code; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_reval_multiplier` | Reval. Multiplier | `character varying(3)` |
| `a_reval_rate` | Reval. Rate | `numeric` |
| `a_reval_code` | Reval. Code | `character varying(3)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-a_asset_split"></a>
## `a_asset_split` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Split`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Split'; 주요 열 a_asset_acct_id, a_depreciation_workfile_id, a_asset_cost, a_asset_id; FK aassetid_aassetsplit; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_acct_id` | A_Asset_Acct_ID | `numeric(10,0)` |
| `a_depreciation_workfile_id` | A_Depreciation_Workfile_ID | `numeric(10,0)` |
| `a_asset_cost` | Asset Cost | `numeric` |
| `a_asset_id` | Asset | `numeric(10,0)` |
| `a_asset_id_to` | To Asset ID | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aassetid_aassetsplit` | `a_asset_split.(a_asset_id_to)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_asset_spread"></a>
## `a_asset_spread` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Asset_Spread_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Asset_Spread_ID'; 주요 열 a_asset_spread_type; FK aassetspread_aassetacct; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_spread_type` | Spread Type | `character varying(20)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aassetspread_aassetacct` | `a_asset_acct.(a_asset_spread_id)` → `a_asset_spread.(a_asset_spread_id)` | A_Asset_Acct_ID |

<a id="t-a_asset_transfer"></a>
## `a_asset_transfer` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Asset_Transfer_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Asset_Transfer_ID'; 주요 열 a_asset_acct_id, a_accumdepreciation_acct, a_asset_acct_new, a_depreciation_acct; FK aasset_aassettransfer; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_acct_id` | A_Asset_Acct_ID | `numeric(10,0)` |
| `a_accumdepreciation_acct` | Accumulated Depreciation Account | `numeric(10,0)` |
| `a_asset_acct_new` | New Asset Cost Acct | `character varying(22)` |
| `a_depreciation_acct` | Depreciation Account | `numeric(10,0)` |
| `a_depreciation_acct_str` | A_Depreciation_Acct_Str | `character varying(40)` |
| `a_disposal_loss_new` | New Disposal Loss | `character varying(22)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aasset_aassettransfer` | `a_asset_transfer.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_asset_type"></a>
## `a_asset_type` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Type`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Type'; 주요 열 근거 부족; FK aassettype_aasset, aassettype_aassetgroup; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aassettype_aasset` | `a_asset.(a_asset_type_id)` → `a_asset_type.(a_asset_type_id)` | Asset |
| incoming | `aassettype_aassetgroup` | `a_asset_group.(a_asset_type_id)` → `a_asset_type.(a_asset_type_id)` | Asset Group |
| incoming | `aassettype_ifixedasset` | `i_fixedasset.(a_asset_type_id)` → `a_asset_type.(a_asset_type_id)` | Imported Fixed Asset |

<a id="t-a_asset_use"></a>
## `a_asset_use` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Asset_Use_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Asset_Use_ID'; 주요 열 a_asset_id; FK aasset_aassetuse; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aasset_aassetuse` | `a_asset_use.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_depreciation"></a>
## `a_depreciation` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Depreciation`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Depreciation'; 주요 열 depreciationtype; FK adepreciation_aassetacct, adepreciation_aassetgroupacct; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `depreciationtype` | Depreciation Type | `character varying(10)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adepreciation_aassetacct` | `a_asset_acct.(a_depreciation_id)` → `a_depreciation.(a_depreciation_id)` | A_Asset_Acct_ID |
| incoming | `adepreciation_aassetgroupacct` | `a_asset_group_acct.(a_depreciation_id)` → `a_depreciation.(a_depreciation_id)` | Asset Group Accounting |
| incoming | `adepreciationf_aassetacct` | `a_asset_acct.(a_depreciation_f_id)` → `a_depreciation.(a_depreciation_id)` | A_Asset_Acct_ID |
| incoming | `adepreciationf_aassetgroupacct` | `a_asset_group_acct.(a_depreciation_f_id)` → `a_depreciation.(a_depreciation_id)` | Asset Group Accounting |

<a id="t-a_depreciation_build"></a>
## `a_depreciation_build` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Build Depreciation`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Build Depreciation'; 주요 열 a_end_asset_id, a_start_asset_id; FK aendasset_adepreciationbuild, astartasset_adepreciationbuild; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_end_asset_id` | To Asset | `numeric(10,0)` |
| `a_start_asset_id` | From Asset | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aendasset_adepreciationbuild` | `a_depreciation_build.(a_end_asset_id)` → `a_asset.(a_asset_id)` | Asset |
| outgoing | `astartasset_adepreciationbuild` | `a_depreciation_build.(a_start_asset_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_depreciation_convention"></a>
## `a_depreciation_convention` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Depreciation Convention`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Depreciation Convention'; 주요 열 근거 부족; FK adepreciationconv_aassetacct, adepreciationconv_aassetgroupa; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adepreciationconv_aassetacct` | `a_asset_acct.(a_depreciation_conv_id)` → `a_depreciation_convention.(a_depreciation_convention_id)` | A_Asset_Acct_ID |
| incoming | `adepreciationconv_aassetgroupa` | `a_asset_group_acct.(a_depreciation_conv_id)` → `a_depreciation_convention.(a_depreciation_convention_id)` | Asset Group Accounting |
| incoming | `adepreciationconvf_aassetacct` | `a_asset_acct.(a_depreciation_conv_f_id)` → `a_depreciation_convention.(a_depreciation_convention_id)` | A_Asset_Acct_ID |
| incoming | `adepreciationconvf_aassetgroup` | `a_asset_group_acct.(a_depreciation_conv_f_id)` → `a_depreciation_convention.(a_depreciation_convention_id)` | Asset Group Accounting |

<a id="t-a_depreciation_entry"></a>
## `a_depreciation_entry` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Depreciation Entry`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Depreciation Entry'; 주요 열 근거 부족; FK adepreciationentry_adepreciati; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adepreciationentry_adepreciati` | `a_depreciation_exp.(a_depreciation_entry_id)` → `a_depreciation_entry.(a_depreciation_entry_id)` | A_Depreciation_Exp_ID |

<a id="t-a_depreciation_exp"></a>
## `a_depreciation_exp` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Depreciation_Exp_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Depreciation_Exp_ID'; 주요 열 isdepreciated, a_asset_id, a_asset_cost, uselifemonths; FK aasset_adepreciationexp, aassetaddition_adepreciationex; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isdepreciated` | Depreciate | `character(1)` |
| `a_asset_id` | Asset | `numeric(10,0)` |
| `a_asset_cost` | Asset Cost | `numeric` |
| `uselifemonths` | Usable Life - Months | `numeric(10,0)` |
| `uselifemonths_f` | Use Life - Months (fiscal) | `numeric(10,0)` |
| `a_asset_remaining` | Remaining Amt | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aasset_adepreciationexp` | `a_depreciation_exp.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |
| outgoing | `aassetaddition_adepreciationex` | `a_depreciation_exp.(a_asset_addition_id)` → `a_asset_addition.(a_asset_addition_id)` | Asset Addition |
| outgoing | `aassetdisposed_adepreciationex` | `a_depreciation_exp.(a_asset_disposed_id)` → `a_asset_disposed.(a_asset_disposed_id)` | Asset Disposed |
| outgoing | `adepreciationentry_adepreciati` | `a_depreciation_exp.(a_depreciation_entry_id)` → `a_depreciation_entry.(a_depreciation_entry_id)` | Depreciation Entry |

<a id="t-a_depreciation_forecast"></a>
## `a_depreciation_forecast` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Depreciation Forecast`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Depreciation Forecast'; 주요 열 a_end_asset_id, a_start_asset_id; FK aendasset_adepreciationforecas, astartasset_adepreciationforec; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_end_asset_id` | To Asset | `numeric(10,0)` |
| `a_start_asset_id` | From Asset | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aendasset_adepreciationforecas` | `a_depreciation_forecast.(a_end_asset_id)` → `a_asset.(a_asset_id)` | Asset |
| outgoing | `astartasset_adepreciationforec` | `a_depreciation_forecast.(a_start_asset_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_depreciation_method"></a>
## `a_depreciation_method` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Depreciation Method`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Depreciation Method'; 주요 열 depreciationtype; FK adepreciationmethod_aassetacct, adepreciationmethod_aassetgrou; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `depreciationtype` | Depreciation Type | `character varying(10)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adepreciationmethod_aassetacct` | `a_asset_acct.(a_depreciation_method_id)` → `a_depreciation_method.(a_depreciation_method_id)` | A_Asset_Acct_ID |
| incoming | `adepreciationmethod_aassetgrou` | `a_asset_group_acct.(a_depreciation_method_id)` → `a_depreciation_method.(a_depreciation_method_id)` | Asset Group Accounting |
| incoming | `adepreciationmethodf_aassetacc` | `a_asset_acct.(a_depreciation_method_f_id)` → `a_depreciation_method.(a_depreciation_method_id)` | A_Asset_Acct_ID |
| incoming | `adepreciationmethodf_aassetgro` | `a_asset_group_acct.(a_depreciation_method_f_id)` → `a_depreciation_method.(a_depreciation_method_id)` | Asset Group Accounting |

<a id="t-a_depreciation_table_detail"></a>
## `a_depreciation_table_detail` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Depreciation Table Detail`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Depreciation Table Detail'; 주요 열 a_depreciation_rate, a_depreciation_table_code; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_depreciation_rate` | Rate | `numeric` |
| `a_depreciation_table_code` | Depreciation Code | `character varying(20)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-a_depreciation_table_header"></a>
## `a_depreciation_table_header` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Depreciation_Table_Header_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Depreciation_Table_Header_ID'; 주요 열 a_depreciation_table_code; FK adepreciationtableheader_aass2, adepreciationtableheader_aass3; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_depreciation_table_code` | Depreciation Code | `character varying(20)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adepreciationtableheader_aass2` | `a_asset_change.(a_depreciation_table_header_id)` → `a_depreciation_table_header.(a_depreciation_table_header_id)` | A_Asset_Change_ID |
| incoming | `adepreciationtableheader_aass3` | `a_asset_group_acct.(a_depreciation_table_header_id)` → `a_depreciation_table_header.(a_depreciation_table_header_id)` | Asset Group Accounting |
| incoming | `adepreciationtableheader_aasse` | `a_asset_acct.(a_depreciation_table_header_id)` → `a_depreciation_table_header.(a_depreciation_table_header_id)` | A_Asset_Acct_ID |
| incoming | `adepreciationtableheader_iasse` | `i_asset.(a_depreciation_table_header_id)` → `a_depreciation_table_header.(a_depreciation_table_header_id)` | Asset |

<a id="t-a_depreciation_workfile"></a>
## `a_depreciation_workfile` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_Depreciation_Workfile_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_Depreciation_Workfile_ID'; 주요 열 a_asset_cost, a_asset_id, a_asset_life_current_year, isdepreciated; FK aasset_adepreciationworkfile, afundingmode_adepreciationwork; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_cost` | Asset Cost | `numeric` |
| `a_asset_id` | Asset | `numeric(10,0)` |
| `a_asset_life_current_year` | A_Asset_Life_Current_Year | `numeric` |
| `isdepreciated` | Depreciate | `character(1)` |
| `assetdepreciationdate` | Asset Depreciation Date | `timestamp without time zone` |
| `a_salvage_value` | Asset Salvage Value | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aasset_adepreciationworkfile` | `a_depreciation_workfile.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |
| outgoing | `afundingmode_adepreciationwork` | `a_depreciation_workfile.(a_fundingmode_id)` → `a_fundingmode.(a_fundingmode_id)` | Asset Funding Mode |

<a id="t-a_fundingmode"></a>
## `a_fundingmode` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Funding Mode`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Funding Mode'; 주요 열 근거 부족; FK afundingmode_adepreciationwork, afundingmode_afundingmodeacct; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `afundingmode_adepreciationwork` | `a_depreciation_workfile.(a_fundingmode_id)` → `a_fundingmode.(a_fundingmode_id)` | A_Depreciation_Workfile_ID |
| incoming | `afundingmode_afundingmodeacct` | `a_fundingmode_acct.(a_fundingmode_id)` → `a_fundingmode.(a_fundingmode_id)` | Asset Funding Mode Accounting |

<a id="t-a_fundingmode_acct"></a>
## `a_fundingmode_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset Funding Mode Accounting`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset Funding Mode Accounting'; 주요 열 c_acctschema_id, a_fundingmode_acct; FK afundingmodevc_afundingmodeacc, cacctschema_afundingmodeacct; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `a_fundingmode_acct` | Funding Mode Account | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `afundingmodevc_afundingmodeacc` | `a_fundingmode_acct.(a_fundingmode_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `cacctschema_afundingmodeacct` | `a_fundingmode_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |

<a id="t-a_registration"></a>
## `a_registration` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Registration`
- 사전 Description: User Asset Registration
- 근거 문장: 사전 Name='Registration'; Description='User Asset Registration'; 주요 열 a_asset_id, assetservicedate; FK aasset_aregistration; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_asset_id` | Asset | `numeric(10,0)` |
| `assetservicedate` | In Service Date | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aasset_aregistration` | `a_registration.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |

<a id="t-a_registrationattribute"></a>
## `a_registrationattribute` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Registration Attribute`
- 사전 Description: Asset Registration Attribute
- 근거 문장: 사전 Name='Registration Attribute'; Description='Asset Registration Attribute'; 주요 열 seqno, ad_reference_id, columnname, ad_reference_value_id; FK adreference_aregattribute, adreferencevalue_aregattribute; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_reference_id` | Reference | `numeric(10,0)` |
| `columnname` | DB Column Name | `character varying(63)` |
| `ad_reference_value_id` | Reference Key | `numeric(10,0)` |
| `isselfservice` | Self-Service | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adreference_aregattribute` | `a_registrationattribute.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | Reference |
| outgoing | `adreferencevalue_aregattribute` | `a_registrationattribute.(ad_reference_value_id)` → `ad_reference.(ad_reference_id)` | Reference |
| incoming | `aregattribute_aregproduct` | `a_registrationproduct.(a_registrationattribute_id)` → `a_registrationattribute.(a_registrationattribute_id)` | Registration Product |
| incoming | `aregattribute_aregvalue` | `a_registrationvalue.(a_registrationattribute_id)` → `a_registrationattribute.(a_registrationattribute_id)` | A_RegistrationValue |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-a_registrationproduct"></a>
## `a_registrationproduct` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Registration Product`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Registration Product'; 주요 열 근거 부족; FK mproduct_aregproduct; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mproduct_aregproduct` | `a_registrationproduct.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-a_registrationvalue"></a>
## `a_registrationvalue` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `A_RegistrationValue`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='A_RegistrationValue'; 주요 열 근거 부족; FK aregattribute_aregvalue, aregistration_aregvalue; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aregattribute_aregvalue` | `a_registrationvalue.(a_registrationattribute_id)` → `a_registrationattribute.(a_registrationattribute_id)` | Registration Attribute |
| outgoing | `aregistration_aregvalue` | `a_registrationvalue.(a_registration_id)` → `a_registration.(a_registration_id)` | Registration |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_accesslog"></a>
## `ad_accesslog` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Access Log`
- 사전 Description: Log of Access to the System
- 근거 문장: 사전 Name='Access Log'; Description='Log of Access to the System'; 주요 열 record_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `record_id` | Record ID | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_alert"></a>
## `ad_alert` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Alert`
- 사전 Description: iDempiere Alert
- 근거 문장: 사전 Name='Alert'; Description='iDempiere Alert'; 주요 열 ad_alertprocessor_id; FK adalert_adalertrecipient, adaltert_aralertrule; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_alertprocessor_id` | Alert Processor | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adalert_adalertrecipient` | `ad_alertrecipient.(ad_alert_id)` → `ad_alert.(ad_alert_id)` | Alert Recipient |
| incoming | `adaltert_aralertrule` | `ad_alertrule.(ad_alert_id)` → `ad_alert.(ad_alert_id)` | Alert Rule |
| outgoing | `calertprocessor_adalert` | `ad_alert.(ad_alertprocessor_id)` → `ad_alertprocessor.(ad_alertprocessor_id)` | Alert Processor |

<a id="t-ad_alertprocessor"></a>
## `ad_alertprocessor` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Alert Processor`
- 사전 Description: Alert Processor/Server Parameter
- 근거 문장: 사전 Name='Alert Processor'; Description='Alert Processor/Server Parameter'; 주요 열 frequencytype, frequency, processing, ad_schedule_id; FK calertprocessor_adalert, calertprocessor_log; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `frequencytype` | Frequency Type | `character(1)` |
| `frequency` | Frequency | `numeric(10,0)` |
| `processing` | Process Now | `character(1)` |
| `ad_schedule_id` | Schedule | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `calertprocessor_adalert` | `ad_alert.(ad_alertprocessor_id)` → `ad_alertprocessor.(ad_alertprocessor_id)` | Alert |
| incoming | `calertprocessor_log` | `ad_alertprocessorlog.(ad_alertprocessor_id)` → `ad_alertprocessor.(ad_alertprocessor_id)` | Alert Processor Log |
| outgoing | `adschedule_adalertprocessor` | `ad_alertprocessor.(ad_schedule_id)` → `ad_schedule.(ad_schedule_id)` | Schedule |

<a id="t-ad_alertprocessorlog"></a>
## `ad_alertprocessorlog` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Alert Processor Log`
- 사전 Description: Result of the execution of the Alert Processor
- 근거 문장: 사전 Name='Alert Processor Log'; Description='Result of the execution of the Alert Processor'; 주요 열 근거 부족; FK calertprocessor_log; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `calertprocessor_log` | `ad_alertprocessorlog.(ad_alertprocessor_id)` → `ad_alertprocessor.(ad_alertprocessor_id)` | Alert Processor |

<a id="t-ad_alertrecipient"></a>
## `ad_alertrecipient` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Alert Recipient`
- 사전 Description: Recipient of the Alert Notification
- 근거 문장: 사전 Name='Alert Recipient'; Description='Recipient of the Alert Notification'; 주요 열 ad_alert_id; FK adalert_adalertrecipient; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_alert_id` | Alert | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adalert_adalertrecipient` | `ad_alertrecipient.(ad_alert_id)` → `ad_alert.(ad_alert_id)` | Alert |

<a id="t-ad_alertrule"></a>
## `ad_alertrule` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Alert Rule`
- 사전 Description: Definition of the alert element
- 근거 문장: 사전 Name='Alert Rule'; Description='Definition of the alert element'; 주요 열 ad_alert_id, preprocessing, postprocessing, errormsg; FK adaltert_aralertrule; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_alert_id` | Alert | `numeric(10,0)` |
| `preprocessing` | Pre Processing | `character varying(2000)` |
| `postprocessing` | Post Processing | `character varying(2000)` |
| `errormsg` | Error Msg | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adaltert_aralertrule` | `ad_alertrule.(ad_alert_id)` → `ad_alert.(ad_alert_id)` | Alert |

<a id="t-ad_archive"></a>
## `ad_archive` — 변경 기록·첨부·보관

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Archive`
- 사전 Description: Document Archive
- 근거 문장: 사전 Name='Archive'; Description='Document Archive'; 주요 열 ad_table_id, record_id, binarydata; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `record_id` | Record ID | `numeric(10,0)` |
| `binarydata` | Binary Data | `bytea` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_archive_blob"></a>
## `ad_archive_blob` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 ad_archive_id, binarydata; FK ad_archive_blob_ad_archive_id_fkey; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_archive_id` | 미지정 | `numeric(10,0)` |
| `binarydata` | 미지정 | `oid` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_archive_blob_ad_archive_id_fkey` | `ad_archive_blob.(ad_archive_id)` → `ad_archive.(ad_archive_id)` | Archive |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_attachment"></a>
## `ad_attachment` — 변경 기록·첨부·보관

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Attachment`
- 사전 Description: Attachment for the document
- 근거 문장: 사전 Name='Attachment'; Description='Attachment for the document'; 주요 열 ad_table_id, record_id, binarydata; FK adattachment_adattachmentfile, adattachment_note; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `record_id` | Record ID | `numeric(10,0)` |
| `binarydata` | Binary Data | `bytea` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adattachment_adattachmentfile` | `ad_attachmentfile.(ad_attachment_id)` → `ad_attachment.(ad_attachment_id)` | Attachment File |
| incoming | `adattachment_note` | `ad_attachmentnote.(ad_attachment_id)` → `ad_attachment.(ad_attachment_id)` | Attachment Note |

<a id="t-ad_attachment_entry"></a>
## `ad_attachment_entry` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 ad_attachment_id, seqno, binarydata; FK ad_attachment_entry_ad_attachment_id_fkey; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_attachment_id` | 미지정 | `numeric(10,0)` |
| `seqno` | 미지정 | `numeric(10,0)` |
| `binarydata` | 미지정 | `oid` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_attachment_entry_ad_attachment_id_fkey` | `ad_attachment_entry.(ad_attachment_id)` → `ad_attachment.(ad_attachment_id)` | Attachment |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_attachmentfile"></a>
## `ad_attachmentfile` — 변경 기록·첨부·보관

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Attachment File`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Attachment File'; 주요 열 ad_attachment_id, filename; FK adattachment_adattachmentfile; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_attachment_id` | Attachment | `numeric(10,0)` |
| `filename` | File Name | `character varying(1000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adattachment_adattachmentfile` | `ad_attachmentfile.(ad_attachment_id)` → `ad_attachment.(ad_attachment_id)` | Attachment |

<a id="t-ad_attachmentnote"></a>
## `ad_attachmentnote` — 변경 기록·첨부·보관

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Attachment Note`
- 사전 Description: Personal Attachment Note
- 근거 문장: 사전 Name='Attachment Note'; Description='Personal Attachment Note'; 주요 열 ad_attachment_id; FK adattachment_note; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_attachment_id` | Attachment | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adattachment_note` | `ad_attachmentnote.(ad_attachment_id)` → `ad_attachment.(ad_attachment_id)` | Attachment |

<a id="t-ad_attribute"></a>
## `ad_attribute` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `System Attribute`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='System Attribute'; 주요 열 ad_table_id, ad_reference_id, ad_reference_value_id, seqno; FK adreference_adattribute, adreferencevalue_adattribute; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_reference_id` | Reference | `numeric(10,0)` |
| `ad_reference_value_id` | Reference Key | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adreference_adattribute` | `ad_attribute.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | Reference |
| outgoing | `adreferencevalue_adattribute` | `ad_attribute.(ad_reference_value_id)` → `ad_reference.(ad_reference_id)` | Reference |
| outgoing | `adtable_adattribute` | `ad_attribute.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `advalrule_adattribute` | `ad_attribute.(ad_val_rule_id)` → `ad_val_rule.(ad_val_rule_id)` | Dynamic Validation |

<a id="t-ad_attribute_value"></a>
## `ad_attribute_value` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Attribute_Value`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Attribute_Value'; 주요 열 v_number, v_date, v_string; FK adattribute_adattributevalue; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `v_number` | Number | `numeric` |
| `v_date` | Date | `timestamp without time zone` |
| `v_string` | String | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adattribute_adattributevalue` | `ad_attribute_value.(ad_attribute_id)` → `ad_attribute.(ad_attribute_id)` | System Attribute |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_authorizationaccount"></a>
## `ad_authorizationaccount` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Authorization Account`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Authorization Account'; 주요 열 accesstoken, refreshtoken, ad_authorizationscope, accesstokentimestamp; FK adauthorizationcredential_adau, aduser_adauthorizationaccount; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `authorization`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `accesstoken` | Access Token | `text` |
| `refreshtoken` | Refresh Token | `character varying(4000)` |
| `ad_authorizationscope` | Authorization Scope | `character varying(10)` |
| `accesstokentimestamp` | Access Token Timestamp | `timestamp without time zone` |
| `ad_authorizationcredential_id` | Authorization Credential | `numeric(10,0)` |
| `isaccessrevoked` | Access Revoked | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adauthorizationcredential_adau` | `ad_authorizationaccount.(ad_authorizationcredential_id)` → `ad_authorizationcredential.(ad_authorizationcredential_id)` | Authorization Credential |
| outgoing | `aduser_adauthorizationaccount` | `ad_authorizationaccount.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-ad_authorizationcredential"></a>
## `ad_authorizationcredential` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Authorization Credential`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Authorization Credential'; 주요 열 ad_authorizationprovider_id, ad_authorizationscopelist; FK adauthorizationcredential_adau, adauthorizationprovider_adauth; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `authorization`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_authorizationprovider_id` | Authorization Provider | `numeric(10,0)` |
| `ad_authorizationscopelist` | Scope List | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adauthorizationcredential_adau` | `ad_authorizationaccount.(ad_authorizationcredential_id)` → `ad_authorizationcredential.(ad_authorizationcredential_id)` | Authorization Account |
| outgoing | `adauthorizationprovider_adauth` | `ad_authorizationcredential.(ad_authorizationprovider_id)` → `ad_authorizationprovider.(ad_authorizationprovider_id)` | Authorization Provider |

<a id="t-ad_authorizationprovider"></a>
## `ad_authorizationprovider` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Authorization Provider`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Authorization Provider'; 주요 열 tokenendpoint, ad_authorizationtype; FK adauthorizationprovauthscopepr, adauthorizationprovider_adauth; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `authorization`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `tokenendpoint` | Token Endpoint | `character varying(2000)` |
| `ad_authorizationtype` | Authorization Type | `character varying(10)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adauthorizationprovauthscopepr` | `ad_authorizationscopeprov.(ad_authorizationprovider_id)` → `ad_authorizationprovider.(ad_authorizationprovider_id)` | Authorization Scope Provider |
| incoming | `adauthorizationprovider_adauth` | `ad_authorizationcredential.(ad_authorizationprovider_id)` → `ad_authorizationprovider.(ad_authorizationprovider_id)` | Authorization Credential |

<a id="t-ad_authorizationscopeprov"></a>
## `ad_authorizationscopeprov` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Authorization Scope Provider`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Authorization Scope Provider'; 주요 열 ad_authorizationprovider_id, ad_authorizationscope; FK adauthorizationprovauthscopepr; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `authorization`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_authorizationprovider_id` | Authorization Provider | `numeric(10,0)` |
| `ad_authorizationscope` | Authorization Scope | `character varying(10)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adauthorizationprovauthscopepr` | `ad_authorizationscopeprov.(ad_authorizationprovider_id)` → `ad_authorizationprovider.(ad_authorizationprovider_id)` | Authorization Provider |

<a id="t-ad_broadcastmessage"></a>
## `ad_broadcastmessage` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Broadcast Message`
- 사전 Description: Broadcast Messages for system users
- 근거 문장: 사전 Name='Broadcast Message'; Description='Broadcast Messages for system users'; 주요 열 broadcastfrequency, broadcastmessage, broadcasttype, expiration; FK adrole_adbroadcastmessage, aduser_adbroadcastmessage; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `broadcastfrequency` | Broadcast Frequency | `character varying(60)` |
| `broadcastmessage` | Broadcast Message | `text` |
| `broadcasttype` | Broadcast Type | `character varying(32)` |
| `expiration` | Expire On | `timestamp without time zone` |
| `logacknowledge` | Log Acknowledge | `character(1)` |
| `target` | Target | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adbroadcastmessage` | `ad_broadcastmessage.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |
| outgoing | `aduser_adbroadcastmessage` | `ad_broadcastmessage.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `notificationclient_adbroadcast` | `ad_broadcastmessage.(notification_client_id)` → `ad_client.(ad_client_id)` | Tenant |
| incoming | `adbroadcastmessage_adbroadcast` | `ad_broadcastmessage_trl.(ad_broadcastmessage_id)` → `ad_broadcastmessage.(ad_broadcastmessage_id)` | Broadcast Message Trl |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_broadcastmessage_trl"></a>
## `ad_broadcastmessage_trl` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Broadcast Message Trl`
- 사전 Description: Broadcast Message
- 근거 문장: 사전 Name='Broadcast Message Trl'; Description='Broadcast Message'; 주요 열 broadcastmessage, istranslated, title; FK adbroadcastmessage_adbroadcast, adlanguage_adbroadcastmessaget; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `broadcastmessage` | Broadcast Message | `text` |
| `istranslated` | Translated | `character(1)` |
| `title` | Title | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adbroadcastmessage_adbroadcast` | `ad_broadcastmessage_trl.(ad_broadcastmessage_id)` → `ad_broadcastmessage.(ad_broadcastmessage_id)` | Broadcast Message |
| outgoing | `adlanguage_adbroadcastmessaget` | `ad_broadcastmessage_trl.(ad_language)` → `ad_language.(ad_language)` | Language ID |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_changelog"></a>
## `ad_changelog` — 변경 기록·첨부·보관

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Change Log`
- 사전 Description: Log of data changes
- 근거 문장: 사전 Name='Change Log'; Description='Log of data changes'; 주요 열 ad_table_id, record_id, oldvalue, newvalue; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `record_id` | Record ID | `numeric(10,0)` |
| `oldvalue` | Old Value | `character varying(4000)` |
| `newvalue` | New Value | `character varying(4000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_chart"></a>
## `ad_chart` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Chart`
- 사전 Description: Chart definition
- 근거 문장: 사전 Name='Chart'; Description='Chart definition'; 주요 열 charttype, chartorientation; FK adchart_adchartdatasource, adchart_adcharttrl; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `charttype` | Chart Type | `character varying(2)` |
| `chartorientation` | Orientation | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adchart_adchartdatasource` | `ad_chartdatasource.(ad_chart_id)` → `ad_chart.(ad_chart_id)` | Chart Datasource |
| incoming | `adchart_adcharttrl` | `ad_chart_trl.(ad_chart_id)` → `ad_chart.(ad_chart_id)` | Chart Trl |
| incoming | `adchart_padashboardcontent` | `pa_dashboardcontent.(ad_chart_id)` → `ad_chart.(ad_chart_id)` | Dashboard Content |

<a id="t-ad_chart_trl"></a>
## `ad_chart_trl` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Chart Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Chart Trl'; 주요 열 근거 부족; FK adchart_adcharttrl; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adchart_adcharttrl` | `ad_chart_trl.(ad_chart_id)` → `ad_chart.(ad_chart_id)` | Chart |

<a id="t-ad_chartdatasource"></a>
## `ad_chartdatasource` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Chart Datasource`
- 사전 Description: Chart data definition
- 근거 문장: 사전 Name='Chart Datasource'; Description='Chart data definition'; 주요 열 ad_chart_id, whereclause; FK adchartdatasourceadchartdatas, adchart_adchartdatasource; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_chart_id` | Chart | `numeric(10,0)` |
| `whereclause` | Sql WHERE | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adchartdatasourceadchartdatas` | `ad_chartdatasource_trl.(ad_chartdatasource_id)` → `ad_chartdatasource.(ad_chartdatasource_id)` | Chart Datasource Trl |
| outgoing | `adchart_adchartdatasource` | `ad_chartdatasource.(ad_chart_id)` → `ad_chart.(ad_chart_id)` | Chart |

<a id="t-ad_chartdatasource_trl"></a>
## `ad_chartdatasource_trl` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Chart Datasource Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Chart Datasource Trl'; 주요 열 근거 부족; FK adchartdatasourceadchartdatas; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adchartdatasourceadchartdatas` | `ad_chartdatasource_trl.(ad_chartdatasource_id)` → `ad_chartdatasource.(ad_chartdatasource_id)` | Chart Datasource |

<a id="t-ad_client"></a>
## `ad_client` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tenant`
- 사전 Description: Tenant for this installation.
- 근거 문장: 사전 Name='Tenant'; Description='Tenant for this installation.'; 주요 열 smtphost, requestemail, requestuser, requestuserpw; FK notificationclient_adbroadcast, adlangu_adclient; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `smtphost` | Mail Host | `character varying(60)` |
| `requestemail` | Request EMail | `character varying(60)` |
| `requestuser` | Request User | `character varying(60)` |
| `requestuserpw` | Request User Password | `character varying(255)` |
| `requestfolder` | Request Folder | `character varying(20)` |
| `ad_language` | Language | `character varying(6)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `notificationclient_adbroadcast` | `ad_broadcastmessage.(notification_client_id)` → `ad_client.(ad_client_id)` | Broadcast Message |
| outgoing | `adlangu_adclient` | `ad_client.(ad_language)` → `ad_language.(ad_language)` | Language ID |
| outgoing | `adpasswordrule_adclient` | `ad_client.(ad_passwordrule_id)` → `ad_passwordrule.(ad_passwordrule_id)` | Password Policies |
| outgoing | `adreplicationstrategy_adclient` | `ad_client.(ad_replicationstrategy_id)` → `ad_replicationstrategy.(ad_replicationstrategy_id)` | Replication Strategy |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_clientinfo"></a>
## `ad_clientinfo` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_ClientInfo`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_ClientInfo'; 주요 열 isdiscountlineamt, c_calendar_id, c_acctschema1_id, c_uom_volume_id; FK adstorageprovider_adclientinfo, adtreeactivity_adclientinfo; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isdiscountlineamt` | Discount calculated from Line Amounts | `character(1)` |
| `c_calendar_id` | Calendar | `numeric(10,0)` |
| `c_acctschema1_id` | Primary Accounting Schema | `numeric(10,0)` |
| `c_uom_volume_id` | UOM for Volume | `numeric(10,0)` |
| `c_uom_weight_id` | UOM for Weight | `numeric(10,0)` |
| `c_uom_length_id` | UOM for Length | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adstorageprovider_adclientinfo` | `ad_clientinfo.(ad_storageprovider_id)` → `ad_storageprovider.(ad_storageprovider_id)` | Storage Provider |
| outgoing | `adtreeactivity_adclientinfo` | `ad_clientinfo.(ad_tree_activity_id)` → `ad_tree.(ad_tree_id)` | Tree |
| outgoing | `adtreebpartner_adclientinfo` | `ad_clientinfo.(ad_tree_bpartner_id)` → `ad_tree.(ad_tree_id)` | Tree |
| outgoing | `adtreecampaign_adclientinfo` | `ad_clientinfo.(ad_tree_campaign_id)` → `ad_tree.(ad_tree_id)` | Tree |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_clientshare"></a>
## `ad_clientshare` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tenant Share`
- 사전 Description: Force (not) sharing of tenant/org entities
- 근거 문장: 사전 Name='Tenant Share'; Description='Force (not) sharing of tenant/org entities'; 주요 열 ad_table_id, sharetype; FK adtable_adclientshare; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `sharetype` | Share Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_adclientshare` | `ad_clientshare.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_color"></a>
## `ad_color` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `System Color`
- 사전 Description: Color for backgrounds or indicators
- 근거 문장: 사전 Name='System Color'; Description='Color for backgrounds or indicators'; 주요 열 근거 부족; FK adcolor_adcolortrl, adcolor_addesktop; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adcolor_adcolortrl` | `ad_color_trl.(ad_color_id)` → `ad_color.(ad_color_id)` | System Color Trl |
| incoming | `adcolor_addesktop` | `ad_desktop.(ad_color_id)` → `ad_color.(ad_color_id)` | Desktop |
| incoming | `adcolor_adwindow` | `ad_window.(ad_color_id)` → `ad_color.(ad_color_id)` | Window |
| incoming | `adcolor_adworkbench` | `ad_workbench.(ad_color_id)` → `ad_color.(ad_color_id)` | Workbench |

<a id="t-ad_color_trl"></a>
## `ad_color_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `System Color Trl`
- 사전 Description: Color for backgrounds or indicators
- 근거 문장: 사전 Name='System Color Trl'; Description='Color for backgrounds or indicators'; 주요 열 근거 부족; FK adcolor_adcolortrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adcolor_adcolortrl` | `ad_color_trl.(ad_color_id)` → `ad_color.(ad_color_id)` | System Color |

<a id="t-ad_column"></a>
## `ad_column` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Column`
- 사전 Description: Column in the table
- 근거 문장: 사전 Name='Column'; Description='Column in the table'; 주요 열 columnname, ad_table_id, ad_reference_id, ad_reference_value_id; FK ad_column_ad_tab, ad_column_field; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `columnname` | DB Column Name | `character varying(63)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_reference_id` | Reference | `numeric(10,0)` |
| `ad_reference_value_id` | Reference Key | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_element_id` | System Element | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_column_ad_tab` | `ad_tab.(ad_column_id)` → `ad_column.(ad_column_id)` | Tab |
| incoming | `ad_column_field` | `ad_field.(ad_column_id)` → `ad_column.(ad_column_id)` | Field |
| incoming | `ad_column_reftable_display` | `ad_ref_table.(ad_display)` → `ad_column.(ad_column_id)` | AD_Ref_Table |
| incoming | `ad_column_reftable_id` | `ad_ref_table.(ad_key)` → `ad_column.(ad_column_id)` | AD_Ref_Table |

<a id="t-ad_column_access"></a>
## `ad_column_access` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Column_Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Column_Access'; 주요 열 근거 부족; FK adrole_adcolumnaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adcolumnaccess` | `ad_column_access.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_column_trl"></a>
## `ad_column_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Column Trl`
- 사전 Description: Column in the table
- 근거 문장: 사전 Name='Column Trl'; Description='Column in the table'; 주요 열 근거 부족; FK adcolumn_adcolumntrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adcolumn_adcolumntrl` | `ad_column_trl.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |

<a id="t-ad_ctxhelp"></a>
## `ad_ctxhelp` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Context Help`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Context Help'; 주요 열 ad_form_id, ad_tab_id, ad_table_id; FK adctxhelp_adctxhelpmsg, adctxhelp_adctxhelpsuggestion; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_form_id` | 미지정 | `numeric(10,0)` |
| `ad_tab_id` | 미지정 | `numeric(10,0)` |
| `ad_table_id` | 미지정 | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adctxhelp_adctxhelpmsg` | `ad_ctxhelpmsg.(ad_ctxhelp_id)` → `ad_ctxhelp.(ad_ctxhelp_id)` | Context Help Message |
| incoming | `adctxhelp_adctxhelpsuggestion` | `ad_ctxhelpsuggestion.(ad_ctxhelp_id)` → `ad_ctxhelp.(ad_ctxhelp_id)` | Context Help Suggestion |
| incoming | `adctxhelp_adform` | `ad_form.(ad_ctxhelp_id)` → `ad_ctxhelp.(ad_ctxhelp_id)` | Special Form |
| incoming | `adctxhelp_adinfowindow` | `ad_infowindow.(ad_ctxhelp_id)` → `ad_ctxhelp.(ad_ctxhelp_id)` | Info Window |

<a id="t-ad_ctxhelpmsg"></a>
## `ad_ctxhelpmsg` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Context Help Message`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Context Help Message'; 주요 열 ad_ctxhelp_id; FK adctxhelpmsg_adctxhelpmsgtrl, adctxhelpmsg_adctxhelpsuggesti; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_ctxhelp_id` | Context Help | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adctxhelpmsg_adctxhelpmsgtrl` | `ad_ctxhelpmsg_trl.(ad_ctxhelpmsg_id)` → `ad_ctxhelpmsg.(ad_ctxhelpmsg_id)` | Context Help Message Trl |
| incoming | `adctxhelpmsg_adctxhelpsuggesti` | `ad_ctxhelpsuggestion.(ad_ctxhelpmsg_id)` → `ad_ctxhelpmsg.(ad_ctxhelpmsg_id)` | Context Help Suggestion |
| outgoing | `adctxhelp_adctxhelpmsg` | `ad_ctxhelpmsg.(ad_ctxhelp_id)` → `ad_ctxhelp.(ad_ctxhelp_id)` | Context Help |

<a id="t-ad_ctxhelpmsg_trl"></a>
## `ad_ctxhelpmsg_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Context Help Message Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Context Help Message Trl'; 주요 열 근거 부족; FK adctxhelpmsg_adctxhelpmsgtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adctxhelpmsg_adctxhelpmsgtrl` | `ad_ctxhelpmsg_trl.(ad_ctxhelpmsg_id)` → `ad_ctxhelpmsg.(ad_ctxhelpmsg_id)` | Context Help Message |

<a id="t-ad_ctxhelpsuggestion"></a>
## `ad_ctxhelpsuggestion` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Context Help Suggestion`
- 사전 Description: Suggestion for context help content
- 근거 문장: 사전 Name='Context Help Suggestion'; Description='Suggestion for context help content'; 주요 열 ad_ctxhelp_id, ad_ctxhelpmsg_id; FK adctxhelp_adctxhelpsuggestion, adctxhelpmsg_adctxhelpsuggesti; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_ctxhelp_id` | Context Help | `numeric(10,0)` |
| `ad_ctxhelpmsg_id` | Context Help Message | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adctxhelp_adctxhelpsuggestion` | `ad_ctxhelpsuggestion.(ad_ctxhelp_id)` → `ad_ctxhelp.(ad_ctxhelp_id)` | Context Help |
| outgoing | `adctxhelpmsg_adctxhelpsuggesti` | `ad_ctxhelpsuggestion.(ad_ctxhelpmsg_id)` → `ad_ctxhelpmsg.(ad_ctxhelpmsg_id)` | Context Help Message |

<a id="t-ad_desktop"></a>
## `ad_desktop` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Desktop`
- 사전 Description: Collection of Workbenches
- 근거 문장: 사전 Name='Desktop'; Description='Collection of Workbenches'; 주요 열 ad_color_id; FK addesktop_addesktoptrl, addesktop_addesktopwb; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_color_id` | System Color | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `addesktop_addesktoptrl` | `ad_desktop_trl.(ad_desktop_id)` → `ad_desktop.(ad_desktop_id)` | Desktop Trl |
| incoming | `addesktop_addesktopwb` | `ad_desktopworkbench.(ad_desktop_id)` → `ad_desktop.(ad_desktop_id)` | Desktop Workbench |
| outgoing | `adcolor_addesktop` | `ad_desktop.(ad_color_id)` → `ad_color.(ad_color_id)` | System Color |

<a id="t-ad_desktop_trl"></a>
## `ad_desktop_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Desktop Trl`
- 사전 Description: Collection of Workbenches
- 근거 문장: 사전 Name='Desktop Trl'; Description='Collection of Workbenches'; 주요 열 근거 부족; FK addesktop_addesktoptrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `addesktop_addesktoptrl` | `ad_desktop_trl.(ad_desktop_id)` → `ad_desktop.(ad_desktop_id)` | Desktop |

<a id="t-ad_desktopworkbench"></a>
## `ad_desktopworkbench` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Desktop Workbench`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Desktop Workbench'; 주요 열 seqno; FK addesktop_addesktopwb, adworkbench_addesktopwb; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `addesktop_addesktopwb` | `ad_desktopworkbench.(ad_desktop_id)` → `ad_desktop.(ad_desktop_id)` | Desktop |
| outgoing | `adworkbench_addesktopwb` | `ad_desktopworkbench.(ad_workbench_id)` → `ad_workbench.(ad_workbench_id)` | Workbench |

<a id="t-ad_document_action_access"></a>
## `ad_document_action_access` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Document Action Access`
- 사전 Description: Define access to document type / document action / role combinations.
- 근거 문장: 사전 Name='Document Action Access'; Description='Define access to document type / document action / role combinations.'; 주요 열 근거 부족; FK adrole_addocumentactionaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_addocumentactionaccess` | `ad_document_action_access.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_element"></a>
## `ad_element` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `System Element`
- 사전 Description: System Element enables the central maintenance of column description and help.
- 근거 문장: 사전 Name='System Element'; Description='System Element enables the central maintenance of column description and help.'; 주요 열 columnname; FK ad_element_ad_column, adelement_adelementtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `columnname` | DB Column Name | `character varying(63)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_element_ad_column` | `ad_column.(ad_element_id)` → `ad_element.(ad_element_id)` | Column |
| incoming | `adelement_adelementtrl` | `ad_element_trl.(ad_element_id)` → `ad_element.(ad_element_id)` | System Element Trl |
| incoming | `adelement_adinfocolumn` | `ad_infocolumn.(ad_element_id)` → `ad_element.(ad_element_id)` | Info Column |
| incoming | `adelement_adreference` | `ad_reference.(ad_element_id)` → `ad_element.(ad_element_id)` | Reference |

<a id="t-ad_element_trl"></a>
## `ad_element_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `System Element Trl`
- 사전 Description: System Element enables the central maintenance of column description and help.
- 근거 문장: 사전 Name='System Element Trl'; Description='System Element enables the central maintenance of column description and help.'; 주요 열 근거 부족; FK adelement_adelementtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adelement_adelementtrl` | `ad_element_trl.(ad_element_id)` → `ad_element.(ad_element_id)` | System Element |

<a id="t-ad_entitytype"></a>
## `ad_entitytype` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Entity Type`
- 사전 Description: System Entity Type
- 근거 문장: 사전 Name='Entity Type'; Description='System Entity Type'; 주요 열 근거 부족; FK entityt_adcolumn, entityt_adelement; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `entityt_adcolumn` | `ad_column.(entitytype)` → `ad_entitytype.(entitytype)` | Column |
| incoming | `entityt_adelement` | `ad_element.(entitytype)` → `ad_entitytype.(entitytype)` | System Element |
| incoming | `entityt_adfield` | `ad_field.(entitytype)` → `ad_entitytype.(entitytype)` | Field |
| incoming | `entityt_adfieldgroup` | `ad_fieldgroup.(entitytype)` → `ad_entitytype.(entitytype)` | Field Group |

<a id="t-ad_error"></a>
## `ad_error` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Error`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Error'; 주요 열 code, ad_language; FK adlangu_aderror; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `code` | Validation code | `character varying(2000)` |
| `ad_language` | Language | `character varying(6)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlangu_aderror` | `ad_error.(ad_language)` → `ad_language.(ad_language)` | Language ID |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_field"></a>
## `ad_field` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Field`
- 사전 Description: Field on a database table
- 근거 문장: 사전 Name='Field'; Description='Field on a database table'; 주요 열 ad_tab_id, ad_column_id, ad_fieldgroup_id, isdisplayed; FK ad_fieldtrl, adfield_adfieldsuggestion; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_tab_id` | Tab | `numeric(10,0)` |
| `ad_column_id` | Column | `numeric(10,0)` |
| `ad_fieldgroup_id` | Field Group | `numeric(10,0)` |
| `isdisplayed` | Displayed | `character(1)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_reference_id` | Reference | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_fieldtrl` | `ad_field_trl.(ad_field_id)` → `ad_field.(ad_field_id)` | Field Trl |
| incoming | `adfield_adfieldsuggestion` | `ad_fieldsuggestion.(ad_field_id)` → `ad_field.(ad_field_id)` | Field Suggestions |
| incoming | `adfield_aduserdeffield` | `ad_userdef_field.(ad_field_id)` → `ad_field.(ad_field_id)` | User defined Field |
| incoming | `adfield_aspfield` | `asp_field.(ad_field_id)` → `ad_field.(ad_field_id)` | ASP Field |

<a id="t-ad_field_trl"></a>
## `ad_field_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Field Trl`
- 사전 Description: Field on a database table
- 근거 문장: 사전 Name='Field Trl'; Description='Field on a database table'; 주요 열 근거 부족; FK ad_fieldtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_fieldtrl` | `ad_field_trl.(ad_field_id)` → `ad_field.(ad_field_id)` | Field |

<a id="t-ad_fieldgroup"></a>
## `ad_fieldgroup` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Field Group`
- 사전 Description: Logical grouping of fields
- 근거 문장: 사전 Name='Field Group'; Description='Logical grouping of fields'; 주요 열 근거 부족; FK adfieldgroup_adfield, adfieldgroup_aduserdeffield; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adfieldgroup_adfield` | `ad_field.(ad_fieldgroup_id)` → `ad_fieldgroup.(ad_fieldgroup_id)` | Field |
| incoming | `adfieldgroup_aduserdeffield` | `ad_userdef_field.(ad_fieldgroup_id)` → `ad_fieldgroup.(ad_fieldgroup_id)` | User defined Field |
| incoming | `adfieldgroup_trl` | `ad_fieldgroup_trl.(ad_fieldgroup_id)` → `ad_fieldgroup.(ad_fieldgroup_id)` | Field Group Trl |
| outgoing | `entityt_adfieldgroup` | `ad_fieldgroup.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

<a id="t-ad_fieldgroup_trl"></a>
## `ad_fieldgroup_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Field Group Trl`
- 사전 Description: Logical grouping of fields
- 근거 문장: 사전 Name='Field Group Trl'; Description='Logical grouping of fields'; 주요 열 근거 부족; FK adfieldgroup_trl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adfieldgroup_trl` | `ad_fieldgroup_trl.(ad_fieldgroup_id)` → `ad_fieldgroup.(ad_fieldgroup_id)` | Field Group |

<a id="t-ad_fieldsuggestion"></a>
## `ad_fieldsuggestion` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Field Suggestions`
- 사전 Description: Suggestions for field label, description and help
- 근거 문장: 사전 Name='Field Suggestions'; Description='Suggestions for field label, description and help'; 주요 열 ad_field_id; FK adfield_adfieldsuggestion; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_field_id` | Field | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adfield_adfieldsuggestion` | `ad_fieldsuggestion.(ad_field_id)` → `ad_field.(ad_field_id)` | Field |

<a id="t-ad_find"></a>
## `ad_find` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Find`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Find'; 주요 열 find_id, andor, ad_column_id, operation; FK adcolumn_adfind; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `find_id` | Find | `numeric` |
| `andor` | And/Or | `character(1)` |
| `ad_column_id` | Column | `numeric(10,0)` |
| `operation` | Operation | `character(2)` |
| `value2` | Value To | `character varying(40)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adcolumn_adfind` | `ad_find.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_form"></a>
## `ad_form` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Special Form`
- 사전 Description: Special Form
- 근거 문장: 사전 Name='Special Form'; Description='Special Form'; 주요 열 ad_ctxhelp_id; FK adform_adformaccess, adform_adformtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_ctxhelp_id` | Context Help | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adform_adformaccess` | `ad_form_access.(ad_form_id)` → `ad_form.(ad_form_id)` | AD_Form_Access |
| incoming | `adform_adformtrl` | `ad_form_trl.(ad_form_id)` → `ad_form.(ad_form_id)` | Special Form Trl |
| incoming | `adform_admenu` | `ad_menu.(ad_form_id)` → `ad_form.(ad_form_id)` | Menu |
| incoming | `adform_adpreference` | `ad_preference.(ad_form_id)` → `ad_form.(ad_form_id)` | Preference |

<a id="t-ad_form_access"></a>
## `ad_form_access` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Form_Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Form_Access'; 주요 열 근거 부족; FK adrole_adformaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adformaccess` | `ad_form_access.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_form_trl"></a>
## `ad_form_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Special Form Trl`
- 사전 Description: Special Form
- 근거 문장: 사전 Name='Special Form Trl'; Description='Special Form'; 주요 열 근거 부족; FK adform_adformtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adform_adformtrl` | `ad_form_trl.(ad_form_id)` → `ad_form.(ad_form_id)` | Special Form |

<a id="t-ad_housekeeping"></a>
## `ad_housekeeping` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `House Keeping Configuration`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='House Keeping Configuration'; 주요 열 processing, tablename; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `processing` | Process Now | `character(1)` |
| `tablename` | DB Table Name | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_image"></a>
## `ad_image` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Image`
- 사전 Description: System Image or Icon
- 근거 문장: 사전 Name='Image'; Description='System Image or Icon'; 주요 열 imageurl, binarydata, entitytype, ad_storageprovider_id; FK logo_adclientinfo, logoreport_adclientinfo; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `imageurl` | Image URL | `character varying(120)` |
| `binarydata` | Binary Data | `bytea` |
| `entitytype` | Entity Type | `character varying(40)` |
| `ad_storageprovider_id` | Storage Provider | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `logo_adclientinfo` | `ad_clientinfo.(logo_id)` → `ad_image.(ad_image_id)` | AD_ClientInfo |
| incoming | `logoreport_adclientinfo` | `ad_clientinfo.(logoreport_id)` → `ad_image.(ad_image_id)` | AD_ClientInfo |
| incoming | `logoweb_adclientinfo` | `ad_clientinfo.(logoweb_id)` → `ad_image.(ad_image_id)` | AD_ClientInfo |
| incoming | `adimage_adcolor` | `ad_color.(ad_image_id)` → `ad_image.(ad_image_id)` | System Color |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_image_blob"></a>
## `ad_image_blob` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 ad_image_id, binarydata; FK ad_image_blob_ad_image_id_fkey; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_image_id` | 미지정 | `numeric(10,0)` |
| `binarydata` | 미지정 | `oid` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_image_blob_ad_image_id_fkey` | `ad_image_blob.(ad_image_id)` → `ad_image.(ad_image_id)` | Image |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_impformat"></a>
## `ad_impformat` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Format`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Import Format'; 주요 열 processing; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_impformat_row"></a>
## `ad_impformat_row` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Format Field`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Format Field'; 주요 열 seqno, ad_column_id; FK adcolumn_adimpformatrow; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_column_id` | Column | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adcolumn_adimpformatrow` | `ad_impformat_row.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |

<a id="t-ad_importtemplate"></a>
## `ad_importtemplate` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Template`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Import Template'; 주요 열 importtemplatetype; FK adimporttemplate_adimporttempl; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `importtemplatetype` | Import Template Type | `character varying(4)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adimporttemplate_adimporttempl` | `ad_importtemplateaccess.(ad_importtemplate_id)` → `ad_importtemplate.(ad_importtemplate_id)` | Import Template Access |

<a id="t-ad_importtemplateaccess"></a>
## `ad_importtemplateaccess` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Template Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Import Template Access'; 주요 열 ad_importtemplate_id; FK adimporttemplate_adimporttempl; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_importtemplate_id` | Import Template | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adimporttemplate_adimporttempl` | `ad_importtemplateaccess.(ad_importtemplate_id)` → `ad_importtemplate.(ad_importtemplate_id)` | Import Template |

<a id="t-ad_indexcolumn"></a>
## `ad_indexcolumn` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Table Index Column`
- 사전 Description: Index definition for column
- 근거 문장: 사전 Name='Table Index Column'; Description='Index definition for column'; 주요 열 ad_column_id, ad_tableindex_id, seqno; FK adcolumn_adindexcolumn, adtableindex_adindexcolumn; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_column_id` | Column | `numeric(10,0)` |
| `ad_tableindex_id` | Table Index | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adcolumn_adindexcolumn` | `ad_indexcolumn.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `adtableindex_adindexcolumn` | `ad_indexcolumn.(ad_tableindex_id)` → `ad_tableindex.(ad_tableindex_id)` | Table Index |
| outgoing | `entityt_adindexcolumn` | `ad_indexcolumn.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

<a id="t-ad_infocolumn"></a>
## `ad_infocolumn` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Info Column`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Info Column'; 주요 열 selectclause, seqno, isdisplayed, ad_element_id; FK adinfocolumn_adinfocolumntrl, adinfocolumn_adinfoprocess; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `selectclause` | Sql SELECT | `character varying(2000)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `isdisplayed` | Displayed | `character(1)` |
| `ad_element_id` | System Element | `numeric(10,0)` |
| `ad_reference_id` | Reference | `numeric(10,0)` |
| `ad_reference_value_id` | Reference Key | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adinfocolumn_adinfocolumntrl` | `ad_infocolumn_trl.(ad_infocolumn_id)` → `ad_infocolumn.(ad_infocolumn_id)` | Info Column Trl |
| incoming | `adinfocolumn_adinfoprocess` | `ad_infoprocess.(ad_infocolumn_id)` → `ad_infocolumn.(ad_infocolumn_id)` | Info Process |
| incoming | `adinfocolumn_aduserdefinfocolu` | `ad_userdef_info_column.(ad_infocolumn_id)` → `ad_infocolumn.(ad_infocolumn_id)` | User defined Info Column |
| outgoing | `adelement_adinfocolumn` | `ad_infocolumn.(ad_element_id)` → `ad_element.(ad_element_id)` | System Element |

<a id="t-ad_infocolumn_trl"></a>
## `ad_infocolumn_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Info Column Trl`
- 사전 Description: Info Window Column
- 근거 문장: 사전 Name='Info Column Trl'; Description='Info Window Column'; 주요 열 근거 부족; FK adinfocolumn_adinfocolumntrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adinfocolumn_adinfocolumntrl` | `ad_infocolumn_trl.(ad_infocolumn_id)` → `ad_infocolumn.(ad_infocolumn_id)` | Info Column |

<a id="t-ad_infoprocess"></a>
## `ad_infoprocess` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Info Process`
- 사전 Description: define process for info window
- 근거 문장: 사전 Name='Info Process'; Description='define process for info window'; 주요 열 ad_process_id; FK adprocess_adinfoprocess; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_process_id` | Process | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprocess_adinfoprocess` | `ad_infoprocess.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |

<a id="t-ad_inforelated"></a>
## `ad_inforelated` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Info Related`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Info Related'; 주요 열 ad_infowindow_id, seqno, relatedinfo_id, relatedcolumn_id; FK adinfowindow_adinforelated, entitytype_adinforelated; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_infowindow_id` | Info Window | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `relatedinfo_id` | Related Info Window | `numeric(10,0)` |
| `relatedcolumn_id` | Related Info Column | `numeric(10,0)` |
| `parentrelatedcolumn_id` | Parent Related Column | `numeric(10,0)` |
| `entitytype` | Entity Type | `character varying(40)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adinfowindow_adinforelated` | `ad_inforelated.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Info Window |
| outgoing | `entitytype_adinforelated` | `ad_inforelated.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |
| outgoing | `parentrelatedcolumn_adinforela` | `ad_inforelated.(parentrelatedcolumn_id)` → `ad_infocolumn.(ad_infocolumn_id)` | Info Column |
| outgoing | `relatedcolumn_adinforelated` | `ad_inforelated.(relatedcolumn_id)` → `ad_infocolumn.(ad_infocolumn_id)` | Info Column |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_infowindow"></a>
## `ad_infowindow` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Info Window`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Info Window'; 주요 열 ad_table_id, ad_ctxhelp_id, seqno, ad_window_id; FK ad_infowindow_preference, adinfowindow_adcolumn; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_ctxhelp_id` | Context Help | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_infowindow_preference` | `ad_preference.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Preference |
| incoming | `adinfowindow_adcolumn` | `ad_column.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Column |
| incoming | `adinfowindow_adinfocolumn` | `ad_infocolumn.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Info Column |
| incoming | `adinfowindow_adinfoprocess` | `ad_infoprocess.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Info Process |

<a id="t-ad_infowindow_access"></a>
## `ad_infowindow_access` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Info Window Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Info Window Access'; 주요 열 근거 부족; FK adrole_adinfowindowaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adinfowindowaccess` | `ad_infowindow_access.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_infowindow_trl"></a>
## `ad_infowindow_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Info Window Trl`
- 사전 Description: Info and search/select Window
- 근거 문장: 사전 Name='Info Window Trl'; Description='Info and search/select Window'; 주요 열 근거 부족; FK adinfowindow_adinfowindowtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adinfowindow_adinfowindowtrl` | `ad_infowindow_trl.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Info Window |

<a id="t-ad_issue"></a>
## `ad_issue` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `System Issue`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='System Issue'; 주요 열 username, sourceclassname, sourcemethodname, loggername; FK adprocess_adissue; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `username` | User Name | `character varying(60)` |
| `sourceclassname` | Source Class | `character varying(255)` |
| `sourcemethodname` | Source Method | `character varying(60)` |
| `loggername` | Logger | `character varying(255)` |
| `processing` | Process Now | `character(1)` |
| `ad_process_id` | Process | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprocess_adissue` | `ad_issue.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |

<a id="t-ad_label"></a>
## `ad_label` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Label`
- 사전 Description: Record Label
- 근거 문장: 사전 Name='Label'; Description='Record Label'; 주요 열 ad_labelcategory_id, ad_labelstyle_id; FK adlabel_adlabelassignment, adlabel_adlabeltrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_labelcategory_id` | Label Category | `numeric(10,0)` |
| `ad_labelstyle_id` | Label Style | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adlabel_adlabelassignment` | `ad_labelassignment.(ad_label_id)` → `ad_label.(ad_label_id)` | Label Assignment |
| incoming | `adlabel_adlabeltrl` | `ad_label_trl.(ad_label_id)` → `ad_label.(ad_label_id)` | Label Trl |
| outgoing | `adlabelcategory_adlabel` | `ad_label.(ad_labelcategory_id)` → `ad_labelcategory.(ad_labelcategory_id)` | Label Category |
| outgoing | `adlabelstyle_adlabel` | `ad_label.(ad_labelstyle_id)` → `ad_style.(ad_style_id)` | Style |

<a id="t-ad_label_trl"></a>
## `ad_label_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Label Trl`
- 사전 Description: Record Label
- 근거 문장: 사전 Name='Label Trl'; Description='Record Label'; 주요 열 근거 부족; FK adlabel_adlabeltrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlabel_adlabeltrl` | `ad_label_trl.(ad_label_id)` → `ad_label.(ad_label_id)` | Label |

<a id="t-ad_labelassignment"></a>
## `ad_labelassignment` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Label Assignment`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Label Assignment'; 주요 열 ad_label_id, ad_table_id; FK adlabel_adlabelassignment, adtable_adlabelassignment; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_label_id` | Label | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlabel_adlabelassignment` | `ad_labelassignment.(ad_label_id)` → `ad_label.(ad_label_id)` | Label |
| outgoing | `adtable_adlabelassignment` | `ad_labelassignment.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

<a id="t-ad_labelcategory"></a>
## `ad_labelcategory` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Label Category`
- 사전 Description: Category of a Label
- 근거 문장: 사전 Name='Label Category'; Description='Category of a Label'; 주요 열 ad_labelstyle_id; FK adlabelcategory_adlabcattable, adlabelcategory_adlabel; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_labelstyle_id` | Label Style | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adlabelcategory_adlabcattable` | `ad_labelcategorytable.(ad_labelcategory_id)` → `ad_labelcategory.(ad_labelcategory_id)` | Label Category Table Access |
| incoming | `adlabelcategory_adlabel` | `ad_label.(ad_labelcategory_id)` → `ad_labelcategory.(ad_labelcategory_id)` | Label |
| incoming | `adlabelcategory_adlabelcategor` | `ad_labelcategory_trl.(ad_labelcategory_id)` → `ad_labelcategory.(ad_labelcategory_id)` | Label Category Trl |
| outgoing | `adlabelstyle_clabelcategory` | `ad_labelcategory.(ad_labelstyle_id)` → `ad_style.(ad_style_id)` | Style |

<a id="t-ad_labelcategory_trl"></a>
## `ad_labelcategory_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Label Category Trl`
- 사전 Description: Category of a Label
- 근거 문장: 사전 Name='Label Category Trl'; Description='Category of a Label'; 주요 열 근거 부족; FK adlabelcategory_adlabelcategor; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlabelcategory_adlabelcategor` | `ad_labelcategory_trl.(ad_labelcategory_id)` → `ad_labelcategory.(ad_labelcategory_id)` | Label Category |

<a id="t-ad_labelcategorytable"></a>
## `ad_labelcategorytable` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Label Category Table Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Label Category Table Access'; 주요 열 ad_labelcategory_id, ad_table_id; FK adlabelcategory_adlabcattable, adtable_adlabelcategorytable; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_labelcategory_id` | Label Category | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlabelcategory_adlabcattable` | `ad_labelcategorytable.(ad_labelcategory_id)` → `ad_labelcategory.(ad_labelcategory_id)` | Label Category |
| outgoing | `adtable_adlabelcategorytable` | `ad_labelcategorytable.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

<a id="t-ad_labelprinter"></a>
## `ad_labelprinter` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Label printer`
- 사전 Description: Label Printer Definition
- 근거 문장: 사전 Name='Label printer'; Description='Label Printer Definition'; 주요 열 근거 부족; FK adlabelprinter_function, adlabelprinter_printlabel; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adlabelprinter_function` | `ad_labelprinterfunction.(ad_labelprinter_id)` → `ad_labelprinter.(ad_labelprinter_id)` | Label printer Function |
| incoming | `adlabelprinter_printlabel` | `ad_printlabel.(ad_labelprinter_id)` → `ad_labelprinter.(ad_labelprinter_id)` | Print Label |

<a id="t-ad_labelprinterfunction"></a>
## `ad_labelprinterfunction` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Label printer Function`
- 사전 Description: Function of Label Printer
- 근거 문장: 사전 Name='Label printer Function'; Description='Function of Label Printer'; 주요 열 ad_labelprinter_id; FK adlabelprintfunc_labelline, adlabelprinter_function; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_labelprinter_id` | Label printer | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adlabelprintfunc_labelline` | `ad_printlabelline.(ad_labelprinterfunction_id)` → `ad_labelprinterfunction.(ad_labelprinterfunction_id)` | Print Label Line |
| outgoing | `adlabelprinter_function` | `ad_labelprinterfunction.(ad_labelprinter_id)` → `ad_labelprinter.(ad_labelprinter_id)` | Label printer |

<a id="t-ad_language"></a>
## `ad_language` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Language ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Language ID'; 주요 열 languageiso, countrycode, isbaselanguage, issystemlanguage; FK adlanguage_aassetgrouptrl, adlanguage_adbroadcastmessaget; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `languageiso` | ISO Language Code | `character(2)` |
| `countrycode` | ISO Country Code | `character(2)` |
| `isbaselanguage` | Base Language | `character(1)` |
| `issystemlanguage` | System Language | `character(1)` |
| `processing` | Process Now | `character(1)` |
| `ad_language_id` | Language ID | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adlanguage_aassetgrouptrl` | `a_asset_group_trl.(ad_language)` → `ad_language.(ad_language)` | Asset Group Trl |
| incoming | `adlanguage_adbroadcastmessaget` | `ad_broadcastmessage_trl.(ad_language)` → `ad_language.(ad_language)` | Broadcast Message Trl |
| incoming | `adlanguage_adcharttrl` | `ad_chart_trl.(ad_language)` → `ad_language.(ad_language)` | Chart Trl |
| incoming | `adlanguage_adchartdatasourcetr` | `ad_chartdatasource_trl.(ad_language)` → `ad_language.(ad_language)` | Chart Datasource Trl |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_ldapaccess"></a>
## `ad_ldapaccess` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Ldap Access`
- 사전 Description: Ldap Access Log
- 근거 문장: 사전 Name='Ldap Access'; Description='Ldap Access Log'; 주요 열 ad_user_id; FK adldapprocessor_adldapaccess, aduser_adldapaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `ldap`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adldapprocessor_adldapaccess` | `ad_ldapaccess.(ad_ldapprocessor_id)` → `ad_ldapprocessor.(ad_ldapprocessor_id)` | Ldap Processor |
| outgoing | `aduser_adldapaccess` | `ad_ldapaccess.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-ad_ldapprocessor"></a>
## `ad_ldapprocessor` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Ldap Processor`
- 사전 Description: LDAP Server
- 근거 문장: 사전 Name='Ldap Processor'; Description='LDAP Server'; 주요 열 근거 부족; FK adldapprocessor_adldapaccess, adldapprocessor_adldapproclog; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `ldap`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adldapprocessor_adldapaccess` | `ad_ldapaccess.(ad_ldapprocessor_id)` → `ad_ldapprocessor.(ad_ldapprocessor_id)` | Ldap Access |
| incoming | `adldapprocessor_adldapproclog` | `ad_ldapprocessorlog.(ad_ldapprocessor_id)` → `ad_ldapprocessor.(ad_ldapprocessor_id)` | Ldap Processor Log |
| outgoing | `aduser_adldapprocessor` | `ad_ldapprocessor.(supervisor_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-ad_ldapprocessorlog"></a>
## `ad_ldapprocessorlog` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Ldap Processor Log`
- 사전 Description: LDAP Server Log
- 근거 문장: 사전 Name='Ldap Processor Log'; Description='LDAP Server Log'; 주요 열 근거 부족; FK adldapprocessor_adldapproclog; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `ldap`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adldapprocessor_adldapproclog` | `ad_ldapprocessorlog.(ad_ldapprocessor_id)` → `ad_ldapprocessor.(ad_ldapprocessor_id)` | Ldap Processor |

<a id="t-ad_menu"></a>
## `ad_menu` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Menu`
- 사전 Description: Identifies a Menu
- 근거 문장: 사전 Name='Menu'; Description='Identifies a Menu'; 주요 열 ad_window_id, ad_form_id; FK ad_menutrl, admenu_adtreefavoritenode; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_window_id` | Window | `numeric(10,0)` |
| `ad_form_id` | Special Form | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_menutrl` | `ad_menu_trl.(ad_menu_id)` → `ad_menu.(ad_menu_id)` | Menu Trl |
| incoming | `admenu_adtreefavoritenode` | `ad_tree_favorite_node.(ad_menu_id)` → `ad_menu.(ad_menu_id)` | Favorite Node Tree |
| outgoing | `adform_admenu` | `ad_menu.(ad_form_id)` → `ad_form.(ad_form_id)` | Special Form |
| outgoing | `adinfowindow_admenu` | `ad_menu.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Info Window |

<a id="t-ad_menu_trl"></a>
## `ad_menu_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Menu Trl`
- 사전 Description: Identifies a Menu
- 근거 문장: 사전 Name='Menu Trl'; Description='Identifies a Menu'; 주요 열 근거 부족; FK ad_menutrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_menutrl` | `ad_menu_trl.(ad_menu_id)` → `ad_menu.(ad_menu_id)` | Menu |

<a id="t-ad_message"></a>
## `ad_message` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Message`
- 사전 Description: System Message
- 근거 문장: 사전 Name='Message'; Description='System Message'; 주요 열 msgtext, msgtip, msgtype, entitytype; FK fkconstraintmsg_adcolumn, entityt_admessage; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `msgtext` | Message Text | `character varying(2000)` |
| `msgtip` | Message Tip | `character varying(2000)` |
| `msgtype` | Message Type | `character(1)` |
| `entitytype` | Entity Type | `character varying(40)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `fkconstraintmsg_adcolumn` | `ad_column.(fkconstraintmsg_id)` → `ad_message.(ad_message_id)` | Column |
| outgoing | `entityt_admessage` | `ad_message.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |
| incoming | `ad_messagetrl` | `ad_message_trl.(ad_message_id)` → `ad_message.(ad_message_id)` | Message Trl |
| incoming | `admessage_adnote` | `ad_note.(ad_message_id)` → `ad_message.(ad_message_id)` | Notice |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_message_trl"></a>
## `ad_message_trl` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Message Trl`
- 사전 Description: System Message
- 근거 문장: 사전 Name='Message Trl'; Description='System Message'; 주요 열 msgtext, msgtip, istranslated; FK ad_language_messagetrl, ad_messagetrl; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `msgtext` | Message Text | `character varying(2000)` |
| `msgtip` | Message Tip | `character varying(2000)` |
| `istranslated` | Translated | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_language_messagetrl` | `ad_message_trl.(ad_language)` → `ad_language.(ad_language)` | Language ID |
| outgoing | `ad_messagetrl` | `ad_message_trl.(ad_message_id)` → `ad_message.(ad_message_id)` | Message |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_migrationscript"></a>
## `ad_migrationscript` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Migration Script`
- 사전 Description: Migration Scripts for the System
- 근거 문장: 사전 Name='Migration Script'; Description='Migration Scripts for the System'; 주요 열 developername, projectname, reference, releaseno; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `developername` | Developer Name | `character varying(60)` |
| `projectname` | Project | `character varying(60)` |
| `reference` | Reference | `character varying(2000)` |
| `releaseno` | Release No | `character varying(10)` |
| `scriptroll` | Roll the Script | `character(1)` |
| `status` | Status | `character(2)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_modelgeneratortemplate"></a>
## `ad_modelgeneratortemplate` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Model Generator Template`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Model Generator Template'; 주요 열 tablename; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `tablename` | DB Table Name | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_modelvalidator"></a>
## `ad_modelvalidator` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Model Validator`
- 사전 Description: Global Model Validator
- 근거 문장: 사전 Name='Model Validator'; Description='Global Model Validator'; 주요 열 seqno; FK entityt_admodelvalidator; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `entityt_admodelvalidator` | `ad_modelvalidator.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

<a id="t-ad_modification"></a>
## `ad_modification` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Modification`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Modification'; 주요 열 seqno, entitytype, version; FK adenritytype_admodification; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |
| `entitytype` | Entity Type | `character varying(40)` |
| `version` | Version | `character varying(20)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adenritytype_admodification` | `ad_modification.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_note"></a>
## `ad_note` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Notice`
- 사전 Description: System Notice
- 근거 문장: 사전 Name='Notice'; Description='System Notice'; 주요 열 processing; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_org"></a>
## `ad_org` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Organization`
- 사전 Description: Organizational entity within client
- 근거 문장: 사전 Name='Organization'; Description='Organizational entity within client'; 주요 열 근거 부족; FK adorgparent_adorginfo; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adorgparent_adorginfo` | `ad_orginfo.(parent_org_id)` → `ad_org.(ad_org_id)` | Organization Info |

<a id="t-ad_orginfo"></a>
## `ad_orginfo` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Organization Info`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Organization Info'; 주요 열 ad_orgtype_id, c_calendar_id; FK adorgparent_adorginfo, adorgtype_adorginfo; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_orgtype_id` | Organization Type | `numeric(10,0)` |
| `c_calendar_id` | Calendar | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adorgparent_adorginfo` | `ad_orginfo.(parent_org_id)` → `ad_org.(ad_org_id)` | Organization |
| outgoing | `adorgtype_adorginfo` | `ad_orginfo.(ad_orgtype_id)` → `ad_orgtype.(ad_orgtype_id)` | Organization Type |
| outgoing | `ccalendar_adorginfo` | `ad_orginfo.(c_calendar_id)` → `c_calendar.(c_calendar_id)` | Calendar |

<a id="t-ad_orgtype"></a>
## `ad_orgtype` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Organization Type`
- 사전 Description: Organization Type allows you to categorize your organizations
- 근거 문장: 사전 Name='Organization Type'; Description='Organization Type allows you to categorize your organizations'; 주요 열 근거 부족; FK adorgtype_adorginfo; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adorgtype_adorginfo` | `ad_orginfo.(ad_orgtype_id)` → `ad_orgtype.(ad_orgtype_id)` | Organization Info |

<a id="t-ad_package_exp"></a>
## `ad_package_exp` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Package Exp.`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Package Exp.'; 주요 열 근거 부족; FK adpackageexp_adpackageexpdetai; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adpackageexp_adpackageexpdetai` | `ad_package_exp_detail.(ad_package_exp_id)` → `ad_package_exp.(ad_package_exp_id)` | Package Exp. Detail |

<a id="t-ad_package_exp_common"></a>
## `ad_package_exp_common` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Common Package Exp.`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Common Package Exp.'; 주요 열 ad_form_id, ad_impformat_id, ad_reportview_id, ad_table_id; FK adform_adpackageexpcommon, adimpformat_adpackageexpcommon; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_form_id` | Special Form | `numeric(10,0)` |
| `ad_impformat_id` | Import Format | `numeric(10,0)` |
| `ad_reportview_id` | Report View | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_workbench_id` | Workbench | `numeric(10,0)` |
| `dbtype` | DB Type | `character varying(22)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adform_adpackageexpcommon` | `ad_package_exp_common.(ad_form_id)` → `ad_form.(ad_form_id)` | Special Form |
| outgoing | `adimpformat_adpackageexpcommon` | `ad_package_exp_common.(ad_impformat_id)` → `ad_impformat.(ad_impformat_id)` | Import Format |
| outgoing | `admenu_adpackageexpcommon` | `ad_package_exp_common.(ad_menu_id)` → `ad_menu.(ad_menu_id)` | Menu |
| outgoing | `adprocess_adpackageexpcommon` | `ad_package_exp_common.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_package_exp_detail"></a>
## `ad_package_exp_detail` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Package Exp. Detail`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Package Exp. Detail'; 주요 열 근거 부족; FK adpackageexp_adpackageexpdetai; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adpackageexp_adpackageexpdetai` | `ad_package_exp_detail.(ad_package_exp_id)` → `ad_package_exp.(ad_package_exp_id)` | Package Exp. |

<a id="t-ad_package_imp"></a>
## `ad_package_imp` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Package Imp.`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Package Imp.'; 주요 열 근거 부족; FK adpackageimp_adpackageimpdetai, adpackageimpproc_adpackageimp; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adpackageimp_adpackageimpdetai` | `ad_package_imp_detail.(ad_package_imp_id)` → `ad_package_imp.(ad_package_imp_id)` | Imp. Package Detail |
| outgoing | `adpackageimpproc_adpackageimp` | `ad_package_imp.(ad_package_imp_proc_id)` → `ad_package_imp_proc.(ad_package_imp_proc_id)` | Package Imp. Proc. |

<a id="t-ad_package_imp_backup"></a>
## `ad_package_imp_backup` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Imp. Package Backup`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Imp. Package Backup'; 주요 열 ad_package_imp_id, ad_package_imp_detail_id, ad_table_id, ad_column_id; FK adcolumn_adpackageimpbackup, adreference_adpackageimpbackup; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_package_imp_id` | Package Imp. | `numeric(10,0)` |
| `ad_package_imp_detail_id` | Imp. Package Detail | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_column_id` | Column | `numeric(10,0)` |
| `ad_reference_id` | Reference | `numeric(10,0)` |
| `ad_package_imp_bck_dir` | Package Imp. Bck. Directory | `character varying(255)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adcolumn_adpackageimpbackup` | `ad_package_imp_backup.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `adreference_adpackageimpbackup` | `ad_package_imp_backup.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | Reference |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_package_imp_detail"></a>
## `ad_package_imp_detail` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Imp. Package Detail`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Imp. Package Detail'; 주요 열 근거 부족; FK adpackageimp_adpackageimpdetai; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adpackageimp_adpackageimpdetai` | `ad_package_imp_detail.(ad_package_imp_id)` → `ad_package_imp.(ad_package_imp_id)` | Package Imp. |

<a id="t-ad_package_imp_inst"></a>
## `ad_package_imp_inst` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Package Imp. Inst.`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Package Imp. Inst.'; 주요 열 pk_status, releaseno, pk_version, version; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pk_status` | Package Status | `character varying(44)` |
| `releaseno` | Release No | `character varying(40)` |
| `pk_version` | Package Version | `character varying(40)` |
| `version` | Version | `character varying(40)` |
| `email` | EMail Address | `character varying(120)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_package_imp_proc"></a>
## `ad_package_imp_proc` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Package Imp. Proc.`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Package Imp. Proc.'; 주요 열 근거 부족; FK adpackageimpproc_adpackageimp; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adpackageimpproc_adpackageimp` | `ad_package_imp.(ad_package_imp_proc_id)` → `ad_package_imp_proc.(ad_package_imp_proc_id)` | Package Imp. |

<a id="t-ad_package_uuid_map"></a>
## `ad_package_uuid_map` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `UUID Mapping`
- 사전 Description: UUID Mapping between client
- 근거 문장: 사전 Name='UUID Mapping'; Description='UUID Mapping between client'; 주요 열 ad_table_id, source_uuid, target_uuid; FK adtable_adpackageuuidmap; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `source_uuid` | Source UUID | `character varying(36)` |
| `target_uuid` | Target UUID | `character varying(36)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_adpackageuuidmap` | `ad_package_uuid_map.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_password_history"></a>
## `ad_password_history` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Password History ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Password History ID'; 주요 열 ad_user_id, password, datepasswordchanged; FK aduser_adpasswordhistory; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `password`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `password` | Password | `character varying(1024)` |
| `datepasswordchanged` | Date Password Changed | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_adpasswordhistory` | `ad_password_history.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-ad_passwordrule"></a>
## `ad_passwordrule` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Password Policies`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Password Policies'; 주요 열 days_reuse_password; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `password`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `days_reuse_password` | Days Reuse Password | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_pinstance"></a>
## `ad_pinstance` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Process Instance`
- 사전 Description: Instance of the process
- 근거 문장: 사전 Name='Process Instance'; Description='Instance of the process'; 주요 열 ad_process_id, isprocessing, errormsg, notificationtype; FK adprocess_adpinstance; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_process_id` | Process | `numeric(10,0)` |
| `isprocessing` | Processing | `character(1)` |
| `errormsg` | Error Msg | `character varying(2000)` |
| `notificationtype` | Notification Type | `character varying(2)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprocess_adpinstance` | `ad_pinstance.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |

<a id="t-ad_pinstance_log"></a>
## `ad_pinstance_log` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_PInstance_Log`
- 사전 Description: (Non Standard Table)
- 근거 문장: 사전 Name='AD_PInstance_Log'; Description='(Non Standard Table)'; 주요 열 ad_table_id; FK adtable_adpinstancelog; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_adpinstancelog` | `ad_pinstance_log.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

<a id="t-ad_pinstance_para"></a>
## `ad_pinstance_para` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_PInstance_Para`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_PInstance_Para'; 주요 열 parametername, p_string, p_string_to, p_number; FK adpinstance_adpinstancepara; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `parametername` | Parameter Name | `character varying(60)` |
| `p_string` | Process String | `character varying(4000)` |
| `p_string_to` | Process String To | `character varying(4000)` |
| `p_number` | Process Number | `numeric` |
| `p_number_to` | Process Number To | `numeric` |
| `p_date` | Process Date | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adpinstance_adpinstancepara` | `ad_pinstance_para.(ad_pinstance_id)` → `ad_pinstance.(ad_pinstance_id)` | Process Instance |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_postit"></a>
## `ad_postit` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Post-it`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Post-it'; 주요 열 ad_table_id, text, record_id; FK adtable_adpostit; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `text` | Description | `character varying(2000)` |
| `record_id` | Record ID | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_adpostit` | `ad_postit.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_preference"></a>
## `ad_preference` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Preference`
- 사전 Description: Personal Preference
- 근거 문장: 사전 Name='Preference'; Description='Personal Preference'; 주요 열 ad_window_id, ad_form_id; FK ad_infowindow_preference, ad_window_preference; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_window_id` | Window | `numeric(10,0)` |
| `ad_form_id` | Special Form | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_infowindow_preference` | `ad_preference.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Info Window |
| outgoing | `ad_window_preference` | `ad_preference.(ad_window_id)` → `ad_window.(ad_window_id)` | Window |
| outgoing | `adform_adpreference` | `ad_preference.(ad_form_id)` → `ad_form.(ad_form_id)` | Special Form |

<a id="t-ad_printcolor"></a>
## `ad_printcolor` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Color`
- 사전 Description: Color used for printing and display
- 근거 문장: 사전 Name='Print Color'; Description='Color used for printing and display'; 주요 열 근거 부족; FK adprintcolor1_pacolorschema, adprintcolor2_pacolorschema; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adprintcolor1_pacolorschema` | `pa_colorschema.(ad_printcolor1_id)` → `ad_printcolor.(ad_printcolor_id)` | Color Schema |
| incoming | `adprintcolor2_pacolorschema` | `pa_colorschema.(ad_printcolor2_id)` → `ad_printcolor.(ad_printcolor_id)` | Color Schema |
| incoming | `adprintcolor3_pacolorschema` | `pa_colorschema.(ad_printcolor3_id)` → `ad_printcolor.(ad_printcolor_id)` | Color Schema |
| incoming | `adprintcolor4_pacolorschema` | `pa_colorschema.(ad_printcolor4_id)` → `ad_printcolor.(ad_printcolor_id)` | Color Schema |

<a id="t-ad_printcolor_trl"></a>
## `ad_printcolor_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Color`
- 사전 Description: Color used for printing and display
- 근거 문장: 사전 Name='Print Color'; Description='Color used for printing and display'; 주요 열 근거 부족; FK adprintcolor_adprintcolortrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprintcolor_adprintcolortrl` | `ad_printcolor_trl.(ad_printcolor_id)` → `ad_printcolor.(ad_printcolor_id)` | Print Color |

<a id="t-ad_printfont"></a>
## `ad_printfont` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Font`
- 사전 Description: Maintain Print Font
- 근거 문장: 사전 Name='Print Font'; Description='Maintain Print Font'; 주요 열 근거 부족; FK ad_printfont_adprintformat, adprintfont_adprintformatitem; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_printfont_adprintformat` | `ad_printformat.(ad_printfont_id)` → `ad_printfont.(ad_printfont_id)` | Print Format |
| incoming | `adprintfont_adprintformatitem` | `ad_printformatitem.(ad_printfont_id)` → `ad_printfont.(ad_printfont_id)` | Print Format Item |
| incoming | `adprintfont_tableformatfunc` | `ad_printtableformat.(funct_printfont_id)` → `ad_printfont.(ad_printfont_id)` | Print Table Format |
| incoming | `adprintfont_tablehdr` | `ad_printtableformat.(hdr_printfont_id)` → `ad_printfont.(ad_printfont_id)` | Print Table Format |

<a id="t-ad_printform"></a>
## `ad_printform` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Form`
- 사전 Description: Form
- 근거 문장: 사전 Name='Print Form'; Description='Form'; 주요 열 근거 부족; FK adprintformat_forminvoice, adprintformat_formorder; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprintformat_forminvoice` | `ad_printform.(invoice_printformat_id)` → `ad_printformat.(ad_printformat_id)` | Print Format |
| outgoing | `adprintformat_formorder` | `ad_printform.(order_printformat_id)` → `ad_printformat.(ad_printformat_id)` | Print Format |
| outgoing | `adprintformat_formproject` | `ad_printform.(project_printformat_id)` → `ad_printformat.(ad_printformat_id)` | Print Format |
| outgoing | `adprintformat_formremittance` | `ad_printform.(remittance_printformat_id)` → `ad_printformat.(ad_printformat_id)` | Print Format |

<a id="t-ad_printformat"></a>
## `ad_printformat` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Format`
- 사전 Description: Data Print Format
- 근거 문장: 사전 Name='Print Format'; Description='Data Print Format'; 주요 열 ad_table_id, ad_printpaper_id, ad_printcolor_id, ad_printfont_id; FK adprintformat_forminvoice, adprintformat_formorder; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_printpaper_id` | Print Paper | `numeric(10,0)` |
| `ad_printcolor_id` | Print Color | `numeric(10,0)` |
| `ad_printfont_id` | Print Font | `numeric(10,0)` |
| `ad_printtableformat_id` | Print Table Format | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adprintformat_forminvoice` | `ad_printform.(invoice_printformat_id)` → `ad_printformat.(ad_printformat_id)` | Print Form |
| incoming | `adprintformat_formorder` | `ad_printform.(order_printformat_id)` → `ad_printformat.(ad_printformat_id)` | Print Form |
| incoming | `adprintformat_formproject` | `ad_printform.(project_printformat_id)` → `ad_printformat.(ad_printformat_id)` | Print Form |
| incoming | `adprintformat_formremittance` | `ad_printform.(remittance_printformat_id)` → `ad_printformat.(ad_printformat_id)` | Print Form |

<a id="t-ad_printformat_trl"></a>
## `ad_printformat_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Format Trl`
- 사전 Description: Data Print Format
- 근거 문장: 사전 Name='Print Format Trl'; Description='Data Print Format'; 주요 열 근거 부족; FK adprintformat_trl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprintformat_trl` | `ad_printformat_trl.(ad_printformat_id)` → `ad_printformat.(ad_printformat_id)` | Print Format |

<a id="t-ad_printformatitem"></a>
## `ad_printformatitem` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Format Item`
- 사전 Description: Item/Column in the Print format
- 근거 문장: 사전 Name='Print Format Item'; Description='Item/Column in the Print format'; 주요 열 ad_printformat_id, seqno, ad_column_id, ad_printformatchild_id; FK adprintformatitem_trl, adcolumn_adprintformatitem; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_printformat_id` | Print Format | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_column_id` | Column | `numeric(10,0)` |
| `ad_printformatchild_id` | Included Print Format | `numeric(10,0)` |
| `ad_printcolor_id` | Print Color | `numeric(10,0)` |
| `ad_printfont_id` | Print Font | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adprintformatitem_trl` | `ad_printformatitem_trl.(ad_printformatitem_id)` → `ad_printformatitem.(ad_printformatitem_id)` | Print Format Item Trl |
| outgoing | `adcolumn_adprintformatitem` | `ad_printformatitem.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `adfieldstyle_adprintformatitem` | `ad_printformatitem.(ad_fieldstyle_id)` → `ad_style.(ad_style_id)` | Style |
| outgoing | `adprintcolor_adprintformatitem` | `ad_printformatitem.(ad_printcolor_id)` → `ad_printcolor.(ad_printcolor_id)` | Print Color |

<a id="t-ad_printformatitem_trl"></a>
## `ad_printformatitem_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Format Item Trl`
- 사전 Description: Item/Column in the Print format
- 근거 문장: 사전 Name='Print Format Item Trl'; Description='Item/Column in the Print format'; 주요 열 근거 부족; FK adprintformatitem_trl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprintformatitem_trl` | `ad_printformatitem_trl.(ad_printformatitem_id)` → `ad_printformatitem.(ad_printformatitem_id)` | Print Format Item |

<a id="t-ad_printgraph"></a>
## `ad_printgraph` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Graph`
- 사전 Description: Graph included in Reports
- 근거 문장: 사전 Name='Graph'; Description='Graph included in Reports'; 주요 열 description_printformatitem_id, data_printformatitem_id, data1_printformatitem_id, data2_printformatitem_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `description_printformatitem_id` | Description Column | `numeric(10,0)` |
| `data_printformatitem_id` | Data Column | `numeric(10,0)` |
| `data1_printformatitem_id` | Data Column 2 | `numeric(10,0)` |
| `data2_printformatitem_id` | Data Column 3 | `numeric(10,0)` |
| `data3_printformatitem_id` | Data Column 4 | `numeric(10,0)` |
| `data4_printformatitem_id` | Data Column 5 | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_printheaderfooter"></a>
## `ad_printheaderfooter` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Header/Footer`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Print Header/Footer'; 주요 열 근거 부족; FK adprintheaderfooter_adprintfor; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adprintheaderfooter_adprintfor` | `ad_printformat.(ad_printheaderfooter_id)` → `ad_printheaderfooter.(ad_printheaderfooter_id)` | Print Format |

<a id="t-ad_printlabel"></a>
## `ad_printlabel` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Label`
- 사전 Description: Label Format to print
- 근거 문장: 사전 Name='Print Label'; Description='Label Format to print'; 주요 열 ad_table_id, ad_labelprinter_id; FK adprintlabel_adprintlabelline, adlabelprinter_printlabel; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_labelprinter_id` | Label printer | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adprintlabel_adprintlabelline` | `ad_printlabelline.(ad_printlabel_id)` → `ad_printlabel.(ad_printlabel_id)` | Print Label Line |
| outgoing | `adlabelprinter_printlabel` | `ad_printlabel.(ad_labelprinter_id)` → `ad_labelprinter.(ad_labelprinter_id)` | Label printer |
| outgoing | `adtable_adprintlabel` | `ad_printlabel.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

<a id="t-ad_printlabelline"></a>
## `ad_printlabelline` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Label Line`
- 사전 Description: Print Label Line Format
- 근거 문장: 사전 Name='Print Label Line'; Description='Print Label Line Format'; 주요 열 ad_printlabel_id, seqno, ad_column_id, ad_labelprinterfunction_id; FK adprintlabelline_trl, adcolumn_adprintlabelline; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_printlabel_id` | Print Label | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_column_id` | Column | `numeric(10,0)` |
| `ad_labelprinterfunction_id` | Label printer Function | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adprintlabelline_trl` | `ad_printlabelline_trl.(ad_printlabelline_id)` → `ad_printlabelline.(ad_printlabelline_id)` | Print Label Line Trl |
| outgoing | `adcolumn_adprintlabelline` | `ad_printlabelline.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `adlabelprintfunc_labelline` | `ad_printlabelline.(ad_labelprinterfunction_id)` → `ad_labelprinterfunction.(ad_labelprinterfunction_id)` | Label printer Function |
| outgoing | `adprintlabel_adprintlabelline` | `ad_printlabelline.(ad_printlabel_id)` → `ad_printlabel.(ad_printlabel_id)` | Print Label |

<a id="t-ad_printlabelline_trl"></a>
## `ad_printlabelline_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Label Line Trl`
- 사전 Description: Print Label Line Format
- 근거 문장: 사전 Name='Print Label Line Trl'; Description='Print Label Line Format'; 주요 열 근거 부족; FK adprintlabelline_trl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprintlabelline_trl` | `ad_printlabelline_trl.(ad_printlabelline_id)` → `ad_printlabelline.(ad_printlabelline_id)` | Print Label Line |

<a id="t-ad_printpaper"></a>
## `ad_printpaper` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Paper`
- 사전 Description: Printer paper definition
- 근거 문장: 사전 Name='Print Paper'; Description='Printer paper definition'; 주요 열 근거 부족; FK adprintpaper_adprintformat; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adprintpaper_adprintformat` | `ad_printformat.(ad_printpaper_id)` → `ad_printpaper.(ad_printpaper_id)` | Print Format |

<a id="t-ad_printtableformat"></a>
## `ad_printtableformat` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Print Table Format`
- 사전 Description: Table Format in Reports
- 근거 문장: 사전 Name='Print Table Format'; Description='Table Format in Reports'; 주요 열 hdr_printfont_id, funct_printfont_id; FK adprintformattable_format, adprintcolor_tablefunctbg; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hdr_printfont_id` | Header Row Font | `numeric(10,0)` |
| `funct_printfont_id` | Function Font | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adprintformattable_format` | `ad_printformat.(ad_printtableformat_id)` → `ad_printtableformat.(ad_printtableformat_id)` | Print Format |
| outgoing | `adprintcolor_tablefunctbg` | `ad_printtableformat.(functbg_printcolor_id)` → `ad_printcolor.(ad_printcolor_id)` | Print Color |
| outgoing | `adprintcolor_tablefunctfg` | `ad_printtableformat.(functfg_printcolor_id)` → `ad_printcolor.(ad_printcolor_id)` | Print Color |
| outgoing | `adprintcolor_tablehdrline` | `ad_printtableformat.(hdrline_printcolor_id)` → `ad_printcolor.(ad_printcolor_id)` | Print Color |

<a id="t-ad_private_access"></a>
## `ad_private_access` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Private Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Private Access'; 주요 열 근거 부족; FK aduser_adprivateaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_adprivateaccess` | `ad_private_access.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-ad_process"></a>
## `ad_process` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Process`
- 사전 Description: Process or Report
- 근거 문장: 사전 Name='Process'; Description='Process or Report'; 주요 열 isreport, ad_reportview_id, ad_printformat_id, jasperreport; FK ad_process_ad_process_trl, adprocess_padashboardcontent; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isreport` | Report | `character(1)` |
| `ad_reportview_id` | Report View | `numeric(10,0)` |
| `ad_printformat_id` | Print Format | `numeric(10,0)` |
| `jasperreport` | Jasper Report | `character varying(255)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_process_ad_process_trl` | `ad_process_trl.(ad_process_id)` → `ad_process.(ad_process_id)` | Process Trl |
| incoming | `adprocess_padashboardcontent` | `pa_dashboardcontent.(ad_process_id)` → `ad_process.(ad_process_id)` | Dashboard Content |
| incoming | `jasperprocess_pareport` | `pa_report.(jasperprocess_id)` → `ad_process.(ad_process_id)` | Financial Report |
| outgoing | `adreportview_adprocess` | `ad_process.(ad_reportview_id)` → `ad_reportview.(ad_reportview_id)` | Report View |

<a id="t-ad_process_access"></a>
## `ad_process_access` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Process Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Process Access'; 주요 열 근거 부족; FK adrole_adprocessaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adprocessaccess` | `ad_process_access.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_process_drillrule"></a>
## `ad_process_drillrule` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Drill Rule`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Drill Rule'; 주요 열 showhelp, ad_process_id, ad_table_id, ad_reportview_id; FK adprintformat_addrillrule, adprocess_addrillrule; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `showhelp` | Show Help | `character(1)` |
| `ad_process_id` | Process | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_reportview_id` | Report View | `numeric(10,0)` |
| `ad_printformat_id` | Print Format | `numeric(10,0)` |
| `ad_process_para_id` | Process Parameter | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprintformat_addrillrule` | `ad_process_drillrule.(ad_printformat_id)` → `ad_printformat.(ad_printformat_id)` | Print Format |
| outgoing | `adprocess_addrillrule` | `ad_process_drillrule.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |
| outgoing | `adprocesspara_adprocessdrillru` | `ad_process_drillrule.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | Process Parameter |
| outgoing | `adreportview_adprocessdrillrul` | `ad_process_drillrule.(ad_reportview_id)` → `ad_reportview.(ad_reportview_id)` | Report View |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_process_drillrule_para"></a>
## `ad_process_drillrule_para` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Drill Rule Parameter`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Drill Rule Parameter'; 주요 열 parameterdefault, parametertodefault; FK adprocess_addrillrulepara, adprocesspara_addrillrulepara; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `parameterdefault` | Default Parameter | `character varying(255)` |
| `parametertodefault` | Default To Parameter | `character varying(255)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprocess_addrillrulepara` | `ad_process_drillrule_para.(ad_process_drillrule_id)` → `ad_process_drillrule.(ad_process_drillrule_id)` | Drill Rule |
| outgoing | `adprocesspara_addrillrulepara` | `ad_process_drillrule_para.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | Process Parameter |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_process_drillrule_trl"></a>
## `ad_process_drillrule_trl` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Drill Rule Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Drill Rule Trl'; 주요 열 istranslated; FK adlanguage_adprocessdrillrulet, adprocessdrillrule_trl; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istranslated` | Translated | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlanguage_adprocessdrillrulet` | `ad_process_drillrule_trl.(ad_language)` → `ad_language.(ad_language)` | Language ID |
| outgoing | `adprocessdrillrule_trl` | `ad_process_drillrule_trl.(ad_process_drillrule_id)` → `ad_process_drillrule.(ad_process_drillrule_id)` | Drill Rule |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_process_para"></a>
## `ad_process_para` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Process Parameter`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Process Parameter'; 주요 열 ad_process_id, ad_reference_value_id, columnname, defaultvalue; FK adprocesspara_adschedulerpara, adprocesspara_aduserdefprocpar; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_process_id` | Process | `numeric(10,0)` |
| `ad_reference_value_id` | Reference Key | `numeric(10,0)` |
| `columnname` | DB Column Name | `character varying(63)` |
| `defaultvalue` | Default Logic | `character varying(2000)` |
| `defaultvalue2` | Default Logic 2 | `character varying(2000)` |
| `valuemin` | Min. Value | `character varying(20)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adprocesspara_adschedulerpara` | `ad_scheduler_para.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | AD_Scheduler_Para |
| incoming | `adprocesspara_aduserdefprocpar` | `ad_userdef_proc_parameter.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | AD_UserDef_Proc_Parameter_ID |
| incoming | `adprocesspara_aspprocesspara` | `asp_process_para.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | ASP Process Parameter |
| incoming | `adprocpara_adprocparatrl` | `ad_process_para_trl.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | Process Parameter Trl |

<a id="t-ad_process_para_trl"></a>
## `ad_process_para_trl` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Process Parameter Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Process Parameter Trl'; 주요 열 근거 부족; FK adprocpara_adprocparatrl; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprocpara_adprocparatrl` | `ad_process_para_trl.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | Process Parameter |

<a id="t-ad_process_trl"></a>
## `ad_process_trl` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Process Trl`
- 사전 Description: Process or Report
- 근거 문장: 사전 Name='Process Trl'; Description='Process or Report'; 주요 열 근거 부족; FK ad_process_ad_process_trl; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_process_ad_process_trl` | `ad_process_trl.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |

<a id="t-ad_recentitem"></a>
## `ad_recentitem` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Recent Item`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Recent Item'; 주요 열 ad_role_id, ad_tab_id, ad_table_id, ad_user_id; FK adrole_adrecentitem, adtab_adrecentitem; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_role_id` | Role | `numeric(10,0)` |
| `ad_tab_id` | Tab | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |
| `record_id` | Record ID | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adrecentitem` | `ad_recentitem.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |
| outgoing | `adtab_adrecentitem` | `ad_recentitem.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab |
| outgoing | `adtable_adrecentitem` | `ad_recentitem.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `aduser_adrecentitem` | `ad_recentitem.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_record_access"></a>
## `ad_record_access` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Record_Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Record_Access'; 주요 열 근거 부족; FK adrole_ardecordaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_ardecordaccess` | `ad_record_access.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_ref_list"></a>
## `ad_ref_list` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Reference List`
- 사전 Description: Reference List based on Table
- 근거 문장: 사전 Name='Reference List'; Description='Reference List based on Table'; 주요 열 ad_reference_id; FK ad_reflisttrl, ad_reference_reflist; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_reference_id` | Reference | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_reflisttrl` | `ad_ref_list_trl.(ad_ref_list_id)` → `ad_ref_list.(ad_ref_list_id)` | Reference List Trl |
| outgoing | `ad_reference_reflist` | `ad_ref_list.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | Reference |
| outgoing | `entityt_adreflist` | `ad_ref_list.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

<a id="t-ad_ref_list_trl"></a>
## `ad_ref_list_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Reference List Trl`
- 사전 Description: Reference List based on Table
- 근거 문장: 사전 Name='Reference List Trl'; Description='Reference List based on Table'; 주요 열 근거 부족; FK ad_reflisttrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_reflisttrl` | `ad_ref_list_trl.(ad_ref_list_id)` → `ad_ref_list.(ad_ref_list_id)` | Reference List |

<a id="t-ad_ref_table"></a>
## `ad_ref_table` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Ref_Table`
- 사전 Description: Reference Table Definitions
- 근거 문장: 사전 Name='AD_Ref_Table'; Description='Reference Table Definitions'; 주요 열 ad_table_id, ad_window_id; FK ad_column_reftable_display, ad_column_reftable_id; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_column_reftable_display` | `ad_ref_table.(ad_display)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `ad_column_reftable_id` | `ad_ref_table.(ad_key)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `ad_reference_reftable` | `ad_ref_table.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | Reference |
| outgoing | `add_table_reftable` | `ad_ref_table.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

<a id="t-ad_reference"></a>
## `ad_reference` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Reference`
- 사전 Description: System Reference (Pick List)
- 근거 문장: 사전 Name='Reference'; Description='System Reference (Pick List)'; 주요 열 ad_element_id; FK ad_reference_columndatatype, ad_reference_columnvalue; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_element_id` | System Element | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_reference_columndatatype` | `ad_column.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | Column |
| incoming | `ad_reference_columnvalue` | `ad_column.(ad_reference_value_id)` → `ad_reference.(ad_reference_id)` | Column |
| incoming | `ad_reference_reflist` | `ad_ref_list.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | Reference List |
| incoming | `ad_reference_reftable` | `ad_ref_table.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | AD_Ref_Table |

<a id="t-ad_reference_trl"></a>
## `ad_reference_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Reference Trl`
- 사전 Description: System Reference and Validation
- 근거 문장: 사전 Name='Reference Trl'; Description='System Reference and Validation'; 주요 열 근거 부족; FK ad_referencetrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_referencetrl` | `ad_reference_trl.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | Reference |

<a id="t-ad_registration"></a>
## `ad_registration` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `System Registration`
- 사전 Description: System Registration
- 근거 문장: 사전 Name='System Registration'; Description='System Registration'; 주요 열 isregistered, record_id, c_location_id, isinproduction; FK adsystem_adregistration, ccurrency_adregistration; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isregistered` | Registered | `character(1)` |
| `record_id` | Record ID | `numeric(10,0)` |
| `c_location_id` | Address | `numeric(10,0)` |
| `isinproduction` | In Production | `character(1)` |
| `startproductiondate` | Start Implementation/Production | `timestamp without time zone` |
| `isallowpublish` | Allowed to be Published | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adsystem_adregistration` | `ad_registration.(ad_system_id,ad_client_id)` → `ad_system.(ad_system_id,ad_client_id)` | System |
| outgoing | `ccurrency_adregistration` | `ad_registration.(c_currency_id)` → `c_currency.(c_currency_id)` | Currency |
| outgoing | `clocation_adregistration` | `ad_registration.(c_location_id)` → `c_location.(c_location_id)` | Address |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_relationtype"></a>
## `ad_relationtype` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Relation Type`
- 사전 Description: Defines the sets of record pairs (and the conditions a given pair must fulfill to be part of one)
- 근거 문장: 사전 Name='Relation Type'; Description='Defines the sets of record pairs (and the conditions a given pair must fulfill to be part of one)'; 주요 열 ad_reference_source_id, ad_reference_target_id, isdirected, role_source; FK adreferencesource_adrelationty, adreferencetarget_adrelationty; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_reference_source_id` | Source Reference | `numeric(10,0)` |
| `ad_reference_target_id` | Target Reference | `numeric(10,0)` |
| `isdirected` | Directed | `character(1)` |
| `role_source` | Source Role | `character varying(50)` |
| `role_target` | Target Role | `character varying(50)` |
| `type` | Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adreferencesource_adrelationty` | `ad_relationtype.(ad_reference_source_id)` → `ad_reference.(ad_reference_id)` | Reference |
| outgoing | `adreferencetarget_adrelationty` | `ad_relationtype.(ad_reference_target_id)` → `ad_reference.(ad_reference_id)` | Reference |
| outgoing | `entitytype_adrelationtype` | `ad_relationtype.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_replication"></a>
## `ad_replication` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Replication`
- 사전 Description: Data Replication Target
- 근거 문장: 사전 Name='Replication'; Description='Data Replication Target'; 주요 열 ad_replicationstrategy_id, processing; FK adreplication_adreprun, adreplicationstrategy_adrep; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `replication`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_replicationstrategy_id` | Replication Strategy | `numeric(10,0)` |
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adreplication_adreprun` | `ad_replication_run.(ad_replication_id)` → `ad_replication.(ad_replication_id)` | Replication Run |
| outgoing | `adreplicationstrategy_adrep` | `ad_replication.(ad_replicationstrategy_id)` → `ad_replicationstrategy.(ad_replicationstrategy_id)` | Replication Strategy |

<a id="t-ad_replication_log"></a>
## `ad_replication_log` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Replication Log`
- 사전 Description: Data Replication Log Details
- 근거 문장: 사전 Name='Replication Log'; Description='Data Replication Log Details'; 주요 열 ad_replication_run_id, ad_replicationtable_id; FK adreplicationrun_adreplog, adreptable_adreplog; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `replication`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_replication_run_id` | Replication Run | `numeric(10,0)` |
| `ad_replicationtable_id` | Replication Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adreplicationrun_adreplog` | `ad_replication_log.(ad_replication_run_id)` → `ad_replication_run.(ad_replication_run_id)` | Replication Run |
| outgoing | `adreptable_adreplog` | `ad_replication_log.(ad_replicationtable_id)` → `ad_replicationtable.(ad_replicationtable_id)` | Replication Table |

<a id="t-ad_replication_run"></a>
## `ad_replication_run` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Replication Run`
- 사전 Description: Data Replication Run
- 근거 문장: 사전 Name='Replication Run'; Description='Data Replication Run'; 주요 열 ad_replication_id; FK adreplicationrun_adreplog, adreplication_adreprun; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `replication`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_replication_id` | Replication | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adreplicationrun_adreplog` | `ad_replication_log.(ad_replication_run_id)` → `ad_replication_run.(ad_replication_run_id)` | Replication Log |
| outgoing | `adreplication_adreprun` | `ad_replication_run.(ad_replication_id)` → `ad_replication.(ad_replication_id)` | Replication |

<a id="t-ad_replicationdocument"></a>
## `ad_replicationdocument` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Replication Document`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Replication Document'; 주요 열 ad_replicationstrategy_id, replicationtype; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `replication`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_replicationstrategy_id` | Replication Strategy | `numeric(10,0)` |
| `replicationtype` | Replication Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_replicationstrategy"></a>
## `ad_replicationstrategy` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Replication Strategy`
- 사전 Description: Data Replication Strategy
- 근거 문장: 사전 Name='Replication Strategy'; Description='Data Replication Strategy'; 주요 열 근거 부족; FK adreplicationstrategy_adrep, adrepstrategy_adreptable; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `replication`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adreplicationstrategy_adrep` | `ad_replication.(ad_replicationstrategy_id)` → `ad_replicationstrategy.(ad_replicationstrategy_id)` | Replication |
| incoming | `adrepstrategy_adreptable` | `ad_replicationtable.(ad_replicationstrategy_id)` → `ad_replicationstrategy.(ad_replicationstrategy_id)` | Replication Table |
| outgoing | `expprocessor_adreplicationstra` | `ad_replicationstrategy.(exp_processor_id)` → `exp_processor.(exp_processor_id)` | Export Processor |

<a id="t-ad_replicationtable"></a>
## `ad_replicationtable` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Replication Table`
- 사전 Description: Data Replication Strategy Table Info
- 근거 문장: 사전 Name='Replication Table'; Description='Data Replication Strategy Table Info'; 주요 열 ad_replicationstrategy_id, replicationtype; FK adreptable_adreplog, adrepstrategy_adreptable; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `replication`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_replicationstrategy_id` | Replication Strategy | `numeric(10,0)` |
| `replicationtype` | Replication Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adreptable_adreplog` | `ad_replication_log.(ad_replicationtable_id)` → `ad_replicationtable.(ad_replicationtable_id)` | Replication Log |
| outgoing | `adrepstrategy_adreptable` | `ad_replicationtable.(ad_replicationstrategy_id)` → `ad_replicationstrategy.(ad_replicationstrategy_id)` | Replication Strategy |

<a id="t-ad_reportview"></a>
## `ad_reportview` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report View`
- 사전 Description: View used to generate this report
- 근거 문장: 사전 Name='Report View'; Description='View used to generate this report'; 주요 열 whereclause; FK adreportview_adprocess, adreportview_adreportviewcolum; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `whereclause` | Sql WHERE | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adreportview_adprocess` | `ad_process.(ad_reportview_id)` → `ad_reportview.(ad_reportview_id)` | Process |
| incoming | `adreportview_adreportviewcolum` | `ad_reportview_column.(ad_reportview_id)` → `ad_reportview.(ad_reportview_id)` | Report View Selected column |
| incoming | `adreportview_col` | `ad_reportview_col.(ad_reportview_id)` → `ad_reportview.(ad_reportview_id)` | Report view Column |

<a id="t-ad_reportview_col"></a>
## `ad_reportview_col` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report view Column`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Report view Column'; 주요 열 ad_reportview_id; FK adreportview_col; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_reportview_id` | Report View | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adreportview_col` | `ad_reportview_col.(ad_reportview_id)` → `ad_reportview.(ad_reportview_id)` | Report View |

<a id="t-ad_reportview_column"></a>
## `ad_reportview_column` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report View Selected column`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Report View Selected column'; 주요 열 근거 부족; FK adreportview_adreportviewcolum; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adreportview_adreportviewcolum` | `ad_reportview_column.(ad_reportview_id)` → `ad_reportview.(ad_reportview_id)` | Report View |

<a id="t-ad_requiredplugin"></a>
## `ad_requiredplugin` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Required Plugin`
- 사전 Description: Register of plugins that are required when running the System
- 근거 문장: 사전 Name='Required Plugin'; Description='Register of plugins that are required when running the System'; 주요 열 pluginexpectedstate, pluginname, entitytype; FK entitytype_adrequiredplugin; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pluginexpectedstate` | Expected State | `character varying(20)` |
| `pluginname` | Plugin Name | `character varying(1000)` |
| `entitytype` | Entity Type | `character varying(40)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `entitytype_adrequiredplugin` | `ad_requiredplugin.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_role"></a>
## `ad_role` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Role`
- 사전 Description: Responsibility Role
- 근거 문장: 사전 Name='Role'; Description='Responsibility Role'; 주요 열 ispersonalaccess, isaccessallorgs, isuseuserorgaccess, isaccessadvanced; FK ad_role_included_parent, ad_role_included_role; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ispersonalaccess` | Personal Access | `character(1)` |
| `isaccessallorgs` | Access all Orgs | `character(1)` |
| `isuseuserorgaccess` | Use User Org Access | `character(1)` |
| `isaccessadvanced` | Access Advanced | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_role_included_parent` | `ad_role_included.(ad_role_id)` → `ad_role.(ad_role_id)` | Included Role |
| incoming | `ad_role_included_role` | `ad_role_included.(included_role_id)` → `ad_role.(ad_role_id)` | Included Role |
| incoming | `adrole_adcolumnaccess` | `ad_column_access.(ad_role_id)` → `ad_role.(ad_role_id)` | AD_Column_Access |
| incoming | `adrole_addocumentactionaccess` | `ad_document_action_access.(ad_role_id)` → `ad_role.(ad_role_id)` | Document Action Access |

<a id="t-ad_role_included"></a>
## `ad_role_included` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Included Role`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Included Role'; 주요 열 근거 부족; FK ad_role_included_parent, ad_role_included_role; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_role_included_parent` | `ad_role_included.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |
| outgoing | `ad_role_included_role` | `ad_role_included.(included_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_role_orgaccess"></a>
## `ad_role_orgaccess` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Role_OrgAccess`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Role_OrgAccess'; 주요 열 근거 부족; FK adrole_adroleorgaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adroleorgaccess` | `ad_role_orgaccess.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_rule"></a>
## `ad_rule` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Rule`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Rule'; 주요 열 accesslevel, entitytype, eventtype, ruletype; FK entityt_adrule, adrule_adtablescriptvalidator; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `accesslevel` | Data Access Level | `character(1)` |
| `entitytype` | Entity Type | `character varying(40)` |
| `eventtype` | Event Type | `character(1)` |
| `ruletype` | Rule Type | `character(1)` |
| `script` | Script | `character varying(4000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `entityt_adrule` | `ad_rule.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |
| incoming | `adrule_adtablescriptvalidator` | `ad_table_scriptvalidator.(ad_rule_id)` → `ad_rule.(ad_rule_id)` | Table Script Validator |
| incoming | `adrule_ctax` | `c_tax.(ad_rule_id)` → `ad_rule.(ad_rule_id)` | Tax |
| incoming | `adrule_hrattribute` | `hr_attribute.(ad_rule_id)` → `ad_rule.(ad_rule_id)` | Payroll Employee Attribute |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_schedule"></a>
## `ad_schedule` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Schedule`
- 사전 Description: Times for the Scheduler
- 근거 문장: 사전 Name='Schedule'; Description='Times for the Scheduler'; 주요 열 cronpattern, frequency, frequencytype, isignoreprocessingtime; FK adschedule_adalertprocessor, adschedule_adscheduler; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cronpattern` | Cron Scheduling Pattern | `character varying(255)` |
| `frequency` | Frequency | `numeric(10,0)` |
| `frequencytype` | Frequency Type | `character(1)` |
| `isignoreprocessingtime` | Ignore Processing Time | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adschedule_adalertprocessor` | `ad_alertprocessor.(ad_schedule_id)` → `ad_schedule.(ad_schedule_id)` | Alert Processor |
| incoming | `adschedule_adscheduler` | `ad_scheduler.(ad_schedule_id)` → `ad_schedule.(ad_schedule_id)` | Scheduler |

<a id="t-ad_scheduler"></a>
## `ad_scheduler` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Scheduler`
- 사전 Description: Schedule Processes
- 근거 문장: 사전 Name='Scheduler'; Description='Schedule Processes'; 주요 열 ad_process_id, frequencytype, frequency, processing; FK adscheduler_adschedulerpara, adscheduler_log; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_process_id` | Process | `numeric(10,0)` |
| `frequencytype` | Frequency Type | `character(1)` |
| `frequency` | Frequency | `numeric(10,0)` |
| `processing` | Process Now | `character(1)` |
| `isignoreprocessingtime` | Ignore Processing Time | `character(1)` |
| `cronpattern` | Cron Scheduling Pattern | `character varying(255)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adscheduler_adschedulerpara` | `ad_scheduler_para.(ad_scheduler_id)` → `ad_scheduler.(ad_scheduler_id)` | AD_Scheduler_Para |
| incoming | `adscheduler_log` | `ad_schedulerlog.(ad_scheduler_id)` → `ad_scheduler.(ad_scheduler_id)` | Scheduler Log |
| incoming | `adscheduler_recipient` | `ad_schedulerrecipient.(ad_scheduler_id)` → `ad_scheduler.(ad_scheduler_id)` | Scheduler Recipient |
| outgoing | `adprocess_adscheduler` | `ad_scheduler.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |

<a id="t-ad_scheduler_para"></a>
## `ad_scheduler_para` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Scheduler_Para`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Scheduler_Para'; 주요 열 근거 부족; FK adprocesspara_adschedulerpara, adscheduler_adschedulerpara; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprocesspara_adschedulerpara` | `ad_scheduler_para.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | Process Parameter |
| outgoing | `adscheduler_adschedulerpara` | `ad_scheduler_para.(ad_scheduler_id)` → `ad_scheduler.(ad_scheduler_id)` | Scheduler |

<a id="t-ad_schedulerlog"></a>
## `ad_schedulerlog` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Scheduler Log`
- 사전 Description: Result of the execution of the Scheduler
- 근거 문장: 사전 Name='Scheduler Log'; Description='Result of the execution of the Scheduler'; 주요 열 근거 부족; FK adscheduler_log; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adscheduler_log` | `ad_schedulerlog.(ad_scheduler_id)` → `ad_scheduler.(ad_scheduler_id)` | Scheduler |

<a id="t-ad_schedulerrecipient"></a>
## `ad_schedulerrecipient` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Scheduler Recipient`
- 사전 Description: Recipient of the Scheduler Notification
- 근거 문장: 사전 Name='Scheduler Recipient'; Description='Recipient of the Scheduler Notification'; 주요 열 ad_scheduler_id, filename; FK adscheduler_recipient; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_scheduler_id` | Scheduler | `numeric(10,0)` |
| `filename` | File Name | `character varying(255)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adscheduler_recipient` | `ad_schedulerrecipient.(ad_scheduler_id)` → `ad_scheduler.(ad_scheduler_id)` | Scheduler |

<a id="t-ad_searchdefinition"></a>
## `ad_searchdefinition` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Search Definition`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Search Definition'; 주요 열 ad_column_id, ad_table_id, ad_window_id, ad_style_id; FK adcolumn_adsearchdefinition, adstyle_adsearchdefinition; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_column_id` | Column | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |
| `ad_style_id` | Style | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adcolumn_adsearchdefinition` | `ad_searchdefinition.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `adstyle_adsearchdefinition` | `ad_searchdefinition.(ad_style_id)` → `ad_style.(ad_style_id)` | Style |
| outgoing | `adtable_adsearchdefinition` | `ad_searchdefinition.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `adwindow_adsearchdefinition` | `ad_searchdefinition.(ad_window_id)` → `ad_window.(ad_window_id)` | Window |

<a id="t-ad_sequence"></a>
## `ad_sequence` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Sequence`
- 사전 Description: Document Sequence
- 근거 문장: 사전 Name='Sequence'; Description='Document Sequence'; 주요 열 currentnext, currentnextsys; FK ad_sequence_doctypedoc, definitesequence_cdoctype; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `currentnext` | Current Next | `numeric(10,0)` |
| `currentnextsys` | Current Next (System) | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_sequence_doctypedoc` | `c_doctype.(docnosequence_id)` → `ad_sequence.(ad_sequence_id)` | Document Type |
| incoming | `definitesequence_cdoctype` | `c_doctype.(definitesequence_id)` → `ad_sequence.(ad_sequence_id)` | Document Type |

<a id="t-ad_sequence_audit"></a>
## `ad_sequence_audit` — 변경 기록·첨부·보관

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Sequence_Audit`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Sequence_Audit'; 주요 열 ad_table_id, record_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `record_id` | Record ID | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_sequence_no"></a>
## `ad_sequence_no` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Sequence_No`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Sequence_No'; 주요 열 currentnext; FK ad_sequence_sequenceno; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `currentnext` | Current Next | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_sequence_sequenceno` | `ad_sequence_no.(ad_sequence_id)` → `ad_sequence.(ad_sequence_id)` | Sequence |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_session"></a>
## `ad_session` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Session`
- 사전 Description: User Session Online or Web
- 근거 문장: 사전 Name='Session'; Description='User Session Online or Web'; 주요 열 ad_role_id; FK adrole_adsession; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_role_id` | Role | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adsession` | `ad_session.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_smtp"></a>
## `ad_smtp` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `SMTP Server`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='SMTP Server'; 주요 열 emailtest, issecuresmtp, issmtpauthorization, requestuser; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `emailtest` | EMail Test | `character(1)` |
| `issecuresmtp` | SMTP SSL/TLS | `character(1)` |
| `issmtpauthorization` | SMTP Authentication | `character(1)` |
| `requestuser` | Request User | `character varying(60)` |
| `requestuserpw` | Request User Password | `character varying(255)` |
| `smtphost` | Mail Host | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_statusline"></a>
## `ad_statusline` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Status Line`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Status Line'; 주요 열 entitytype, ad_message_id, sqlstatement, ad_style_id; FK admessage_adstatusline, adstyle_adstatusline; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `entitytype` | Entity Type | `character varying(40)` |
| `ad_message_id` | Message | `numeric(10,0)` |
| `sqlstatement` | SQL Expression/Statement | `character varying(2000)` |
| `ad_style_id` | Style | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `admessage_adstatusline` | `ad_statusline.(ad_message_id)` → `ad_message.(ad_message_id)` | Message |
| outgoing | `adstyle_adstatusline` | `ad_statusline.(ad_style_id)` → `ad_style.(ad_style_id)` | Style |
| outgoing | `entitytype_adstatusline` | `ad_statusline.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |
| incoming | `adstatusline_adstatuslineusedi` | `ad_statuslineusedin.(ad_statusline_id)` → `ad_statusline.(ad_statusline_id)` | AD_StatusLineUsedIn |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_statuslineusedin"></a>
## `ad_statuslineusedin` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_StatusLineUsedIn`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_StatusLineUsedIn'; 주요 열 ad_statusline_id, ad_window_id, ad_tab_id, isstatusline; FK adinfowindow_adstatuslineusedi, adstatusline_adstatuslineusedi; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_statusline_id` | Status Line | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |
| `ad_tab_id` | Tab | `numeric(10,0)` |
| `isstatusline` | Status Line | `character(1)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adinfowindow_adstatuslineusedi` | `ad_statuslineusedin.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Info Window |
| outgoing | `adstatusline_adstatuslineusedi` | `ad_statuslineusedin.(ad_statusline_id)` → `ad_statusline.(ad_statusline_id)` | Status Line |
| outgoing | `adtab_adstatuslineusedin` | `ad_statuslineusedin.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab |
| outgoing | `adtable_adstatuslineusedin` | `ad_statuslineusedin.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_storageprovider"></a>
## `ad_storageprovider` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Storage Provider`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Storage Provider'; 주요 열 username; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `username` | User Name | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_style"></a>
## `ad_style` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Style`
- 사전 Description: CSS style for field and label
- 근거 문장: 사전 Name='Style'; Description='CSS style for field and label'; 주요 열 근거 부족; FK adfieldstyle_adfield, adfieldstyle_adinfocolumn; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adfieldstyle_adfield` | `ad_field.(ad_fieldstyle_id)` → `ad_style.(ad_style_id)` | Field |
| incoming | `adfieldstyle_adinfocolumn` | `ad_infocolumn.(ad_fieldstyle_id)` → `ad_style.(ad_style_id)` | Info Column |
| incoming | `adfieldstyle_adprintformatitem` | `ad_printformatitem.(ad_fieldstyle_id)` → `ad_style.(ad_style_id)` | Print Format Item |
| incoming | `adfieldstyle_aduserdeffield` | `ad_userdef_field.(ad_fieldstyle_id)` → `ad_style.(ad_style_id)` | User defined Field |

<a id="t-ad_styleline"></a>
## `ad_styleline` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Style Line`
- 사전 Description: Style Line
- 근거 문장: 사전 Name='Style Line'; Description='Style Line'; 주요 열 ad_style_id; FK adstyle_adstyleline, entitytype_adstyleline; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_style_id` | Style | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adstyle_adstyleline` | `ad_styleline.(ad_style_id)` → `ad_style.(ad_style_id)` | Style |
| outgoing | `entitytype_adstyleline` | `ad_styleline.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

<a id="t-ad_sysconfig"></a>
## `ad_sysconfig` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `System Configurator`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='System Configurator'; 주요 열 entitytype, configurationlevel; FK entityt_adsysconfig; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `entitytype` | Entity Type | `character varying(40)` |
| `configurationlevel` | Configuration Level | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `entityt_adsysconfig` | `ad_sysconfig.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_system"></a>
## `ad_system` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `System`
- 사전 Description: System Definition
- 근거 문장: 사전 Name='System'; Description='System Definition'; 주요 열 username, processing, oldname; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `username` | User Name | `character varying(60)` |
| `processing` | Process Now | `character(1)` |
| `oldname` | Old Name | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-ad_tab"></a>
## `ad_tab` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tab`
- 사전 Description: Tab within a Window
- 근거 문장: 사전 Name='Tab'; Description='Tab within a Window'; 주요 열 ad_table_id, ad_window_id, seqno, ad_column_id; FK ad_tab_field, ad_tabtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_column_id` | Column | `numeric(10,0)` |
| `ad_columnsortorder_id` | Order Column | `numeric(10,0)` |
| `ad_columnsortyesno_id` | Included Column | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_tab_field` | `ad_field.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Field |
| incoming | `ad_tabtrl` | `ad_tab_trl.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab Trl |
| incoming | `adtab_adtabcustomization` | `ad_tab_customization.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab Customization |
| incoming | `adtab_aduserdeftab` | `ad_userdef_tab.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | User defined Tab |

<a id="t-ad_tab_customization"></a>
## `ad_tab_customization` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tab Customization`
- 사전 Description: Grid user customization
- 근거 문장: 사전 Name='Tab Customization'; Description='Grid user customization'; 주요 열 ad_tab_id, isdisplayedgrid; FK adtab_adtabcustomization; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_tab_id` | Tab | `numeric(10,0)` |
| `isdisplayedgrid` | Show in Grid | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtab_adtabcustomization` | `ad_tab_customization.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab |

<a id="t-ad_tab_trl"></a>
## `ad_tab_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tab Trl`
- 사전 Description: Tab within a Window
- 근거 문장: 사전 Name='Tab Trl'; Description='Tab within a Window'; 주요 열 근거 부족; FK ad_tabtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_tabtrl` | `ad_tab_trl.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab |

<a id="t-ad_table"></a>
## `ad_table` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Table`
- 사전 Description: Table for the Fields
- 근거 문장: 사전 Name='Table'; Description='Table for the Fields'; 주요 열 tablename, ad_window_id; FK ad_table_column, ad_table_tab; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `tablename` | DB Table Name | `character varying(60)` |
| `ad_window_id` | Window | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_table_column` | `ad_column.(ad_table_id)` → `ad_table.(ad_table_id)` | Column |
| incoming | `ad_table_tab` | `ad_tab.(ad_table_id)` → `ad_table.(ad_table_id)` | Tab |
| incoming | `add_table_reftable` | `ad_ref_table.(ad_table_id)` → `ad_table.(ad_table_id)` | AD_Ref_Table |
| incoming | `adtable_adaltertrule` | `ad_alertrule.(ad_table_id)` → `ad_table.(ad_table_id)` | Alert Rule |

<a id="t-ad_table_access"></a>
## `ad_table_access` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Table_Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Table_Access'; 주요 열 근거 부족; FK adrole_adtableaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adtableaccess` | `ad_table_access.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_table_scriptvalidator"></a>
## `ad_table_scriptvalidator` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Table Script Validator`
- 사전 Description: Script model validator for tables
- 근거 문장: 사전 Name='Table Script Validator'; Description='Script model validator for tables'; 주요 열 ad_table_id, seqno; FK adtable_adtablescriptvalidator; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_adtablescriptvalidator` | `ad_table_scriptvalidator.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

<a id="t-ad_table_trl"></a>
## `ad_table_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Table Trl`
- 사전 Description: Database Table information
- 근거 문장: 사전 Name='Table Trl'; Description='Database Table information'; 주요 열 근거 부족; FK adtable_adtabletrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_adtabletrl` | `ad_table_trl.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

<a id="t-ad_tableattribute"></a>
## `ad_tableattribute` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_TableAttribute_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_TableAttribute_ID'; 주요 열 ad_table_id; FK adtable_adtableattribute; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_adtableattribute` | `ad_tableattribute.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

<a id="t-ad_tableattributeset"></a>
## `ad_tableattributeset` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Table Attribute Set`
- 사전 Description: Creates a link between tables and attribute sets for flexible extensions. A table can have multiple attribute sets.
- 근거 문장: 사전 Name='Table Attribute Set'; Description='Creates a link between tables and attribute sets for flexible extensions. A table can have multiple attribute sets.'; 주요 열 ad_table_id; FK adtable_adtableattributeset; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_adtableattributeset` | `ad_tableattributeset.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

<a id="t-ad_tableindex"></a>
## `ad_tableindex` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Table Index`
- 사전 Description: Index definition for table
- 근거 문장: 사전 Name='Table Index'; Description='Index definition for table'; 주요 열 ad_table_id; FK adtableindex_adindexcolumn, adtable_adtableindex; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adtableindex_adindexcolumn` | `ad_indexcolumn.(ad_tableindex_id)` → `ad_tableindex.(ad_tableindex_id)` | Table Index Column |
| outgoing | `adtable_adtableindex` | `ad_tableindex.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `entityt_adtableindex` | `ad_tableindex.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

<a id="t-ad_tablepartition"></a>
## `ad_tablepartition` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Table Partition`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Table Partition'; 주요 열 ad_table_id, ad_column_id; FK adcolumn_adtablepartition, adtable_adtablepartition; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_column_id` | Column | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adcolumn_adtablepartition` | `ad_tablepartition.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `adtable_adtablepartition` | `ad_tablepartition.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `parenttablepartition_adtablepa` | `ad_tablepartition.(parent_tablepartition_id)` → `ad_tablepartition.(ad_tablepartition_id)` | Table Partition |

<a id="t-ad_tablevalrule"></a>
## `ad_tablevalrule` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dynamic Validation per Table`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Dynamic Validation per Table'; 주요 열 ad_table_id; FK adtable_adtablevalrule; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_adtablevalrule` | `ad_tablevalrule.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

<a id="t-ad_task"></a>
## `ad_task` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `OS Task`
- 사전 Description: Operation System Task
- 근거 문장: 사전 Name='OS Task'; Description='Operation System Task'; 주요 열 accesslevel, os_command, entitytype, isserverprocess; FK adtask_admenu, adctxhelp_adtask; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `accesslevel` | Data Access Level | `character(1)` |
| `os_command` | OS Command | `character varying(2000)` |
| `entitytype` | Entity Type | `character varying(40)` |
| `isserverprocess` | Server Process | `character(1)` |
| `ad_ctxhelp_id` | Context Help | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adtask_admenu` | `ad_menu.(ad_task_id)` → `ad_task.(ad_task_id)` | Menu |
| outgoing | `adctxhelp_adtask` | `ad_task.(ad_ctxhelp_id)` → `ad_ctxhelp.(ad_ctxhelp_id)` | Context Help |
| outgoing | `entityt_adtask` | `ad_task.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |
| incoming | `adtask_adtaskaccess` | `ad_task_access.(ad_task_id)` → `ad_task.(ad_task_id)` | AD_Task_Access |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_task_access"></a>
## `ad_task_access` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Task_Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Task_Access'; 주요 열 근거 부족; FK adrole_adtaskaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adtaskaccess` | `ad_task_access.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_task_trl"></a>
## `ad_task_trl` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `OS Task Trl`
- 사전 Description: Operation System Task
- 근거 문장: 사전 Name='OS Task Trl'; Description='Operation System Task'; 주요 열 istranslated; FK ad_language_tasktrl, ad_tasktrl; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istranslated` | Translated | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_language_tasktrl` | `ad_task_trl.(ad_language)` → `ad_language.(ad_language)` | Language ID |
| outgoing | `ad_tasktrl` | `ad_task_trl.(ad_task_id)` → `ad_task.(ad_task_id)` | OS Task |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_taskinstance"></a>
## `ad_taskinstance` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Task Instance`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Task Instance'; 주요 열 ad_task_id; FK ad_task_taskinstance; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_task_id` | OS Task | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_task_taskinstance` | `ad_taskinstance.(ad_task_id)` → `ad_task.(ad_task_id)` | OS Task |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_toolbarbutton"></a>
## `ad_toolbarbutton` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ToolBar Button`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ToolBar Button'; 주요 열 actionclassname, actionname, classname, componentname; FK adprocess_adtoolbarbutton, adtab_adtoolbarbutton; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `actionclassname` | Service Component Name | `character varying(255)` |
| `actionname` | Action Name | `character varying(60)` |
| `classname` | Classname | `character varying(255)` |
| `componentname` | Component Name | `character varying(255)` |
| `iscustomization` | Customization | `character(1)` |
| `keystroke_keycode` | Key Code | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprocess_adtoolbarbutton` | `ad_toolbarbutton.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |
| outgoing | `adtab_adtoolbarbutton` | `ad_toolbarbutton.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab |
| outgoing | `entitytype_adtoolbarbutton` | `ad_toolbarbutton.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |
| incoming | `adtoolbarbutton_adtoolbarbutto` | `ad_toolbarbuttonrestrict.(ad_toolbarbutton_id)` → `ad_toolbarbutton.(ad_toolbarbutton_id)` | ToolBar Button Restrict |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_toolbarbuttonrestrict"></a>
## `ad_toolbarbuttonrestrict` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ToolBar Button Restrict`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ToolBar Button Restrict'; 주요 열 action, ad_role_id, ad_toolbarbutton_id, ad_window_id; FK adprocess_adtoolbarbuttonrestr, adrole_adtoolbarbuttonrestrict; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `action` | Action | `character(1)` |
| `ad_role_id` | Role | `numeric(10,0)` |
| `ad_toolbarbutton_id` | ToolBar Button | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |
| `ad_process_id` | Process | `numeric(10,0)` |
| `isexclude` | Exclude | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprocess_adtoolbarbuttonrestr` | `ad_toolbarbuttonrestrict.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |
| outgoing | `adrole_adtoolbarbuttonrestrict` | `ad_toolbarbuttonrestrict.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |
| outgoing | `adtab_adtoolbarbuttonrestrict` | `ad_toolbarbuttonrestrict.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab |
| outgoing | `adtoolbarbutton_adtoolbarbutto` | `ad_toolbarbuttonrestrict.(ad_toolbarbutton_id)` → `ad_toolbarbutton.(ad_toolbarbutton_id)` | ToolBar Button |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_tree"></a>
## `ad_tree` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree`
- 사전 Description: Identifies a Tree
- 근거 문장: 사전 Name='Tree'; Description='Identifies a Tree'; 주요 열 ad_table_id; FK adtree_adtreebar, adtree_adtreenode; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adtree_adtreebar` | `ad_treebar.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | AD_TreeBar |
| incoming | `adtree_adtreenode` | `ad_treenode.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree Node |
| incoming | `adtree_adtreenodebp` | `ad_treenodebp.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree Node BP |
| incoming | `adtree_adtreenodecmc` | `ad_treenodecmc.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree Node CM Container |

<a id="t-ad_tree_favorite"></a>
## `ad_tree_favorite` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Favorite Tree`
- 사전 Description: Show user favorite menu on dashboard
- 근거 문장: 사전 Name='Favorite Tree'; Description='Show user favorite menu on dashboard'; 주요 열 근거 부족; FK adtreefavorite_adtreefavoriten; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adtreefavorite_adtreefavoriten` | `ad_tree_favorite_node.(ad_tree_favorite_id)` → `ad_tree_favorite.(ad_tree_favorite_id)` | Favorite Node Tree |

<a id="t-ad_tree_favorite_node"></a>
## `ad_tree_favorite_node` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Favorite Node Tree`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Favorite Node Tree'; 주요 열 ad_menu_id, ad_tree_favorite_id, seqno, loginopenseqno; FK admenu_adtreefavoritenode, adtreefavorite_adtreefavoriten; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_menu_id` | Menu | `numeric(10,0)` |
| `ad_tree_favorite_id` | Favorite Tree | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `loginopenseqno` | Login automatic open sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `admenu_adtreefavoritenode` | `ad_tree_favorite_node.(ad_menu_id)` → `ad_menu.(ad_menu_id)` | Menu |
| outgoing | `adtreefavorite_adtreefavoriten` | `ad_tree_favorite_node.(ad_tree_favorite_id)` → `ad_tree_favorite.(ad_tree_favorite_id)` | Favorite Tree |
| outgoing | `parent_adtreefavoritenode` | `ad_tree_favorite_node.(parent_id)` → `ad_tree_favorite_node.(ad_tree_favorite_node_id)` | Favorite Node Tree |

<a id="t-ad_treebar"></a>
## `ad_treebar` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_TreeBar`
- 사전 Description: User Selected tree nodes
- 근거 문장: 사전 Name='AD_TreeBar'; Description='User Selected tree nodes'; 주요 열 loginopenseqno; FK adtree_adtreebar; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `loginopenseqno` | Login automatic open sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreebar` | `ad_treebar.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenode"></a>
## `ad_treenode` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tree Node'; 주요 열 seqno; FK adtree_adtreenode; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenode` | `ad_treenode.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodebp"></a>
## `ad_treenodebp` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node BP`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tree Node BP'; 주요 열 seqno; FK adtree_adtreenodebp; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodebp` | `ad_treenodebp.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodecmc"></a>
## `ad_treenodecmc` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node CM Container`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tree Node CM Container'; 주요 열 seqno; FK adtree_adtreenodecmc; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodecmc` | `ad_treenodecmc.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodecmm"></a>
## `ad_treenodecmm` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node CM Media`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tree Node CM Media'; 주요 열 seqno; FK adtree_adtreenodecmm; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodecmm` | `ad_treenodecmm.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodecms"></a>
## `ad_treenodecms` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node CM Stage`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tree Node CM Stage'; 주요 열 seqno; FK adtree_adtreenodecms; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodecms` | `ad_treenodecms.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodecmt"></a>
## `ad_treenodecmt` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node CM Template`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tree Node CM Template'; 주요 열 seqno; FK adtree_adtreenodecmt; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodecmt` | `ad_treenodecmt.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodemm"></a>
## `ad_treenodemm` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node MM`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tree Node MM'; 주요 열 seqno; FK adtree_adtreenodemm; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodemm` | `ad_treenodemm.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodepr"></a>
## `ad_treenodepr` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node PR`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tree Node PR'; 주요 열 seqno; FK adtree_adtreenodepr; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodepr` | `ad_treenodepr.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodeu1"></a>
## `ad_treenodeu1` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node User 1`
- 사전 Description: User defined tree 1
- 근거 문장: 사전 Name='Tree Node User 1'; Description='User defined tree 1'; 주요 열 seqno; FK adtree_adtreenodeu1; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodeu1` | `ad_treenodeu1.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodeu2"></a>
## `ad_treenodeu2` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node User 2`
- 사전 Description: User defined tree 2
- 근거 문장: 사전 Name='Tree Node User 2'; Description='User defined tree 2'; 주요 열 seqno; FK adtree_adtreenodeu2; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodeu2` | `ad_treenodeu2.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodeu3"></a>
## `ad_treenodeu3` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node User 3`
- 사전 Description: User defined tree 3
- 근거 문장: 사전 Name='Tree Node User 3'; Description='User defined tree 3'; 주요 열 seqno; FK adtree_adtreenodeu3; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodeu3` | `ad_treenodeu3.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_treenodeu4"></a>
## `ad_treenodeu4` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tree Node User 4`
- 사전 Description: User defined tree 4
- 근거 문장: 사전 Name='Tree Node User 4'; Description='User defined tree 4'; 주요 열 seqno; FK adtree_adtreenodeu4; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtree_adtreenodeu4` | `ad_treenodeu4.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-ad_user"></a>
## `ad_user` — 공통 사용자·거래처 연락처

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User/Contact`
- 사전 Description: User within the system - Internal or Business Partner Contact
- 근거 문장: 사전 Name='User/Contact'; Description='User within the system - Internal or Business Partner Contact'; 주요 열 password, email, c_bpartner_id, emailuser; FK aduser_supervisor, salesrep_aduser; 사전 의미와 열/FK가 공통 사용자·거래처 연락처를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `user contact`를 근거로, 구조 근거가 있는 `user-contact` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `password` | Password | `character varying(1024)` |
| `email` | EMail Address | `character varying(60)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `emailuser` | EMail User ID | `character varying(60)` |
| `emailuserpw` | EMail User Password | `character varying(255)` |
| `c_bpartner_location_id` | Partner Location | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_supervisor` | `ad_user.(supervisor_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `salesrep_aduser` | `ad_user.(salesrep_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-ad_user_orgaccess"></a>
## `ad_user_orgaccess` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_User_OrgAccess`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_User_OrgAccess'; 주요 열 근거 부족; FK aduser_aduserorgaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_aduserorgaccess` | `ad_user_orgaccess.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-ad_user_roles"></a>
## `ad_user_roles` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_User_Roles`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_User_Roles'; 주요 열 근거 부족; FK adrole_aduserroles, aduser_userroles; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_aduserroles` | `ad_user_roles.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |
| outgoing | `aduser_userroles` | `ad_user_roles.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-ad_user_substitute"></a>
## `ad_user_substitute` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User Substitute`
- 사전 Description: Substitute of the user
- 근거 문장: 사전 Name='User Substitute'; Description='Substitute of the user'; 주요 열 ad_user_id; FK aduser_adusersub, adusersub_ad_usersub; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_adusersub` | `ad_user_substitute.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `adusersub_ad_usersub` | `ad_user_substitute.(substitute_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-ad_userbpaccess"></a>
## `ad_userbpaccess` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User BP Access`
- 사전 Description: User/concat access to Business Partner information and resources
- 근거 문장: 사전 Name='User BP Access'; Description='User/concat access to Business Partner information and resources'; 주요 열 ad_user_id, bpaccesstype; FK aduser_aduserbpaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `bpaccesstype` | Access Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_aduserbpaccess` | `ad_userbpaccess.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-ad_userdef_field"></a>
## `ad_userdef_field` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User defined Field`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='User defined Field'; 주요 열 ad_field_id, isdisplayed, seqno, ad_reference_value_id; FK adfield_aduserdeffield, adfieldgroup_aduserdeffield; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_field_id` | Field | `numeric(10,0)` |
| `isdisplayed` | Displayed | `character(1)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_reference_value_id` | Reference Key | `numeric(10,0)` |
| `ad_reference_id` | Reference | `numeric(10,0)` |
| `ad_labelstyle_id` | Label Style | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adfield_aduserdeffield` | `ad_userdef_field.(ad_field_id)` → `ad_field.(ad_field_id)` | Field |
| outgoing | `adfieldgroup_aduserdeffield` | `ad_userdef_field.(ad_fieldgroup_id)` → `ad_fieldgroup.(ad_fieldgroup_id)` | Field Group |
| outgoing | `adfieldstyle_aduserdeffield` | `ad_userdef_field.(ad_fieldstyle_id)` → `ad_style.(ad_style_id)` | Style |
| outgoing | `adlabelstyle_aduserdeffield` | `ad_userdef_field.(ad_labelstyle_id)` → `ad_style.(ad_style_id)` | Style |

<a id="t-ad_userdef_info"></a>
## `ad_userdef_info` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User defined Info Window`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='User defined Info Window'; 주요 열 seqno, ad_window_id; FK aduserdefinfo_aduserdefinfocol, adinfowindow_aduserdefinfo; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aduserdefinfo_aduserdefinfocol` | `ad_userdef_info_column.(ad_userdef_info_id)` → `ad_userdef_info.(ad_userdef_info_id)` | User defined Info Column |
| outgoing | `adinfowindow_aduserdefinfo` | `ad_userdef_info.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Info Window |
| outgoing | `adwindow_aduserdefinfo` | `ad_userdef_info.(ad_window_id)` → `ad_window.(ad_window_id)` | Window |
| outgoing | `powindow_aduserdefinfo` | `ad_userdef_info.(po_window_id)` → `ad_window.(ad_window_id)` | Window |

<a id="t-ad_userdef_info_column"></a>
## `ad_userdef_info_column` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User defined Info Column`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='User defined Info Column'; 주요 열 seqno, isdisplayed, ad_reference_id, ad_reference_value_id; FK adfieldstyle_aduserdefinfocolu, adinfocolumn_aduserdefinfocolu; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |
| `isdisplayed` | Displayed | `character(1)` |
| `ad_reference_id` | Reference | `numeric(10,0)` |
| `ad_reference_value_id` | Reference Key | `numeric(10,0)` |
| `seqnoselection` | Selection Column Sequence | `numeric(10,0)` |
| `ad_fieldstyle_id` | Field Style | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adfieldstyle_aduserdefinfocolu` | `ad_userdef_info_column.(ad_fieldstyle_id)` → `ad_style.(ad_style_id)` | Style |
| outgoing | `adinfocolumn_aduserdefinfocolu` | `ad_userdef_info_column.(ad_infocolumn_id)` → `ad_infocolumn.(ad_infocolumn_id)` | Info Column |
| outgoing | `adreference_aduserdefcolumn` | `ad_userdef_info_column.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | Reference |
| outgoing | `adreferencevalue_aduserdefinfo` | `ad_userdef_info_column.(ad_reference_value_id)` → `ad_reference.(ad_reference_id)` | Reference |

<a id="t-ad_userdef_info_related"></a>
## `ad_userdef_info_related` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User defined Info Related`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='User defined Info Related'; 주요 열 ad_userdef_info_id, ad_inforelated_id, displaylogic, seqno; FK adinforelated_aduserdefinforel, aduserdefinfo_aduserdefinforel; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_userdef_info_id` | User defined Info Window | `numeric(10,0)` |
| `ad_inforelated_id` | Info Related | `numeric(10,0)` |
| `displaylogic` | Display Logic | `character varying(2000)` |
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adinforelated_aduserdefinforel` | `ad_userdef_info_related.(ad_inforelated_id)` → `ad_inforelated.(ad_inforelated_id)` | Info Related |
| outgoing | `aduserdefinfo_aduserdefinforel` | `ad_userdef_info_related.(ad_userdef_info_id)` → `ad_userdef_info.(ad_userdef_info_id)` | User defined Info Window |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_userdef_proc"></a>
## `ad_userdef_proc` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User defined Process`
- 사전 Description: Primary Key : User defined Process
- 근거 문장: 사전 Name='User defined Process'; Description='Primary Key : User defined Process'; 주요 열 ad_process_id; FK aduserdefproc_aduserdefprocpar, adprocess_aduserdefproc; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_process_id` | Process | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aduserdefproc_aduserdefprocpar` | `ad_userdef_proc_parameter.(ad_userdef_proc_id)` → `ad_userdef_proc.(ad_userdef_proc_id)` | AD_UserDef_Proc_Parameter_ID |
| outgoing | `adprocess_aduserdefproc` | `ad_userdef_proc.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |

<a id="t-ad_userdef_proc_parameter"></a>
## `ad_userdef_proc_parameter` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_UserDef_Proc_Parameter_ID`
- 사전 Description: Primary Key : User defined Process Parameter
- 근거 문장: 사전 Name='AD_UserDef_Proc_Parameter_ID'; Description='Primary Key : User defined Process Parameter'; 주요 열 defaultvalue, ad_process_para_id, ad_reference_value_id, defaultvalue2; FK adprocesspara_aduserdefprocpar, aduserdefproc_aduserdefprocpar; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `defaultvalue` | Default Logic | `character varying(2000)` |
| `ad_process_para_id` | Process Parameter | `numeric(10,0)` |
| `ad_reference_value_id` | Reference Key | `numeric(10,0)` |
| `defaultvalue2` | Default Logic 2 | `character varying(2000)` |
| `valuemin` | Min. Value | `character varying(20)` |
| `valuemax` | Max. Value | `character varying(20)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprocesspara_aduserdefprocpar` | `ad_userdef_proc_parameter.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | Process Parameter |
| outgoing | `aduserdefproc_aduserdefprocpar` | `ad_userdef_proc_parameter.(ad_userdef_proc_id)` → `ad_userdef_proc.(ad_userdef_proc_id)` | User defined Process |

<a id="t-ad_userdef_tab"></a>
## `ad_userdef_tab` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User defined Tab`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='User defined Tab'; 주요 열 ad_tab_id, seqno; FK aduserdeftab_aduserdeffield, adtab_aduserdeftab; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_tab_id` | Tab | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aduserdeftab_aduserdeffield` | `ad_userdef_field.(ad_userdef_tab_id)` → `ad_userdef_tab.(ad_userdef_tab_id)` | User defined Field |
| outgoing | `adtab_aduserdeftab` | `ad_userdef_tab.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab |
| outgoing | `aduserdefwin_aduserdeftab` | `ad_userdef_tab.(ad_userdef_win_id)` → `ad_userdef_win.(ad_userdef_win_id)` | User defined Window |

<a id="t-ad_userdef_theme"></a>
## `ad_userdef_theme` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Theme Customization`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Theme Customization'; 주요 열 근거 부족; FK aduserdeftheme_aduserdefthemedetail; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aduserdeftheme_aduserdefthemedetail` | `ad_userdef_theme_detail.(ad_userdef_theme_id)` → `ad_userdef_theme.(ad_userdef_theme_id)` | Theme Customization Detail |

<a id="t-ad_userdef_theme_detail"></a>
## `ad_userdef_theme_detail` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Theme Customization Detail`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Theme Customization Detail'; 주요 열 근거 부족; FK aduserdeftheme_aduserdefthemedetail; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduserdeftheme_aduserdefthemedetail` | `ad_userdef_theme_detail.(ad_userdef_theme_id)` → `ad_userdef_theme.(ad_userdef_theme_id)` | Theme Customization |

<a id="t-ad_userdef_win"></a>
## `ad_userdef_win` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User defined Window`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='User defined Window'; 주요 열 ad_window_id; FK aduserdefwin_aduserdeftab, adwindow_aduserdefwin; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_window_id` | Window | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aduserdefwin_aduserdeftab` | `ad_userdef_tab.(ad_userdef_win_id)` → `ad_userdef_win.(ad_userdef_win_id)` | User defined Tab |
| outgoing | `adwindow_aduserdefwin` | `ad_userdef_win.(ad_window_id)` → `ad_window.(ad_window_id)` | Window |

<a id="t-ad_usermail"></a>
## `ad_usermail` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User Mail`
- 사전 Description: Mail sent to the user
- 근거 문장: 사전 Name='User Mail'; Description='Mail sent to the user'; 주요 열 ad_user_id, r_mailtext_id, w_mailmsg_id, messageid; FK aduser_adusermail, rmailtext_adusermail; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `r_mailtext_id` | Mail Template | `numeric(10,0)` |
| `w_mailmsg_id` | Mail Message | `numeric(10,0)` |
| `messageid` | Message ID | `character varying(120)` |
| `deliveryconfirmation` | Delivery Confirmation | `character varying(120)` |
| `isdelivered` | Delivered | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_adusermail` | `ad_usermail.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `rmailtext_adusermail` | `ad_usermail.(r_mailtext_id)` → `r_mailtext.(r_mailtext_id)` | Mail Template |
| outgoing | `wmailmsg_adusermail` | `ad_usermail.(w_mailmsg_id)` → `w_mailmsg.(w_mailmsg_id)` | Mail Message |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_userpreference"></a>
## `ad_userpreference` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_UserPreference_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_UserPreference_ID'; 주요 열 ad_user_id, autocommit, autonew, automaticdecimalplacesforamoun; FK aduser_aduserpreference; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `autocommit` | Save on Navigate | `character(1)` |
| `autonew` | Automatic New Record | `character(1)` |
| `automaticdecimalplacesforamoun` | Automatic Decimal Places For Amounts | `numeric(10,0)` |
| `toggleondoubleclick` | Toggle on Double Click | `character(1)` |
| `isdetailedzoomacross` | Detailed Zoom Across | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_aduserpreference` | `ad_userpreference.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_userquery"></a>
## `ad_userquery` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `User Query`
- 사전 Description: Saved User Query
- 근거 문장: 사전 Name='User Query'; Description='Saved User Query'; 주요 열 ad_table_id, ad_tab_id, ad_window_id; FK adtab_aduserquery, adtable_aduserquery; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_tab_id` | Tab | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtab_aduserquery` | `ad_userquery.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab |
| outgoing | `adtable_aduserquery` | `ad_userquery.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `adwindow_aduserquery` | `ad_userquery.(ad_window_id)` → `ad_window.(ad_window_id)` | Window |

<a id="t-ad_val_rule"></a>
## `ad_val_rule` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dynamic Validation`
- 사전 Description: Dynamic Validation Rule
- 근거 문장: 사전 Name='Dynamic Validation'; Description='Dynamic Validation Rule'; 주요 열 근거 부족; FK ad_valrule_column, ad_valrule_table; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_valrule_column` | `ad_column.(ad_val_rule_id)` → `ad_val_rule.(ad_val_rule_id)` | Column |
| incoming | `ad_valrule_table` | `ad_table.(ad_val_rule_id)` → `ad_val_rule.(ad_val_rule_id)` | Table |
| incoming | `advalrule_adattribute` | `ad_attribute.(ad_val_rule_id)` → `ad_val_rule.(ad_val_rule_id)` | System Attribute |
| incoming | `advalrule_adfield` | `ad_field.(ad_val_rule_id)` → `ad_val_rule.(ad_val_rule_id)` | Field |

<a id="t-ad_verifymigration"></a>
## `ad_verifymigration` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Verify Migration`
- 사전 Description: Verify Migration Helper
- 근거 문장: 사전 Name='Verify Migration'; Description='Verify Migration Helper'; 주요 열 ad_pinstance_id, ad_table_id, record_id, seqno; FK adcolumn_adverifymigration, adpinstance_adverifymigration; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_pinstance_id` | Process Instance | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `record_id` | Record ID | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `manualnote` | Note | `character varying(4000)` |
| `expectedvalue` | Expected Value | `character varying(4000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adcolumn_adverifymigration` | `ad_verifymigration.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `adpinstance_adverifymigration` | `ad_verifymigration.(ad_pinstance_id)` → `ad_pinstance.(ad_pinstance_id)` | Process Instance |
| outgoing | `adtable_adverifymigration` | `ad_verifymigration.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_viewcolumn"></a>
## `ad_viewcolumn` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Database View Column`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Database View Column'; 주요 열 columnname, seqno; FK entityt_adviewcolumn; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `columnname` | DB Column Name | `character varying(63)` |
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `entityt_adviewcolumn` | `ad_viewcolumn.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

<a id="t-ad_viewcomponent"></a>
## `ad_viewcomponent` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Database View Component`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Database View Component'; 주요 열 ad_table_id, entitytype, fromclause, otherclause; FK adviewcomponent_adviewcolumn, adtable_adviewcomponent; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `entitytype` | Entity Type | `character varying(40)` |
| `fromclause` | Sql FROM | `character varying(4000)` |
| `otherclause` | Other SQL Clause | `character varying(2000)` |
| `referenced_table_id` | Referenced Table | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adviewcomponent_adviewcolumn` | `ad_viewcolumn.(ad_viewcomponent_id)` → `ad_viewcomponent.(ad_viewcomponent_id)` | Database View Column |
| outgoing | `adtable_adviewcomponent` | `ad_viewcomponent.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `entityt_adviewcomponent` | `ad_viewcomponent.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |
| outgoing | `referencedtable_adviewcomponen` | `ad_viewcomponent.(referenced_table_id)` → `ad_table.(ad_table_id)` | Table |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_wf_activity"></a>
## `ad_wf_activity` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Activity`
- 사전 Description: Workflow Activity
- 근거 문장: 사전 Name='Workflow Activity'; Description='Workflow Activity'; 주요 열 ad_wf_process_id, ad_wf_node_id, ad_wf_responsible_id, wfstate; FK adwfactivity_adwfactivityappro, adwfactivity_adwfactresult; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_wf_process_id` | Workflow Process | `numeric(10,0)` |
| `ad_wf_node_id` | Node | `numeric(10,0)` |
| `ad_wf_responsible_id` | Workflow Responsible | `numeric(10,0)` |
| `wfstate` | Workflow State | `character(2)` |
| `ad_workflow_id` | Workflow | `numeric(10,0)` |
| `priority` | Priority | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adwfactivity_adwfactivityappro` | `ad_wf_activityapprover.(ad_wf_activity_id)` → `ad_wf_activity.(ad_wf_activity_id)` | Workflow Activity Approver |
| incoming | `adwfactivity_adwfactresult` | `ad_wf_activityresult.(ad_wf_activity_id)` → `ad_wf_activity.(ad_wf_activity_id)` | Workflow Activity Result |
| outgoing | `adwfnode_adwfactivity` | `ad_wf_activity.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Node |
| outgoing | `adwfprocess_adwfactivity` | `ad_wf_activity.(ad_wf_process_id)` → `ad_wf_process.(ad_wf_process_id)` | Workflow Process |

<a id="t-ad_wf_activityapprover"></a>
## `ad_wf_activityapprover` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Activity Approver`
- 사전 Description: Approvers of the Workflow Process Activity
- 근거 문장: 사전 Name='Workflow Activity Approver'; Description='Approvers of the Workflow Process Activity'; 주요 열 ad_wf_activity_id; FK adwfactivity_adwfactivityappro; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_wf_activity_id` | Workflow Activity | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adwfactivity_adwfactivityappro` | `ad_wf_activityapprover.(ad_wf_activity_id)` → `ad_wf_activity.(ad_wf_activity_id)` | Workflow Activity |

<a id="t-ad_wf_activityresult"></a>
## `ad_wf_activityresult` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Activity Result`
- 사전 Description: Result of the Workflow Process Activity
- 근거 문장: 사전 Name='Workflow Activity Result'; Description='Result of the Workflow Process Activity'; 주요 열 ad_wf_activity_id; FK adwfactivity_adwfactresult; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_wf_activity_id` | Workflow Activity | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adwfactivity_adwfactresult` | `ad_wf_activityresult.(ad_wf_activity_id)` → `ad_wf_activity.(ad_wf_activity_id)` | Workflow Activity |

<a id="t-ad_wf_block"></a>
## `ad_wf_block` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Block`
- 사전 Description: Workflow Transaction Execution Block
- 근거 문장: 사전 Name='Workflow Block'; Description='Workflow Transaction Execution Block'; 주요 열 ad_workflow_id; FK adwfblock_adwfnode, adworkflow_adwfblock; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_workflow_id` | Workflow | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adwfblock_adwfnode` | `ad_wf_node.(ad_wf_block_id)` → `ad_wf_block.(ad_wf_block_id)` | Node |
| outgoing | `adworkflow_adwfblock` | `ad_wf_block.(ad_workflow_id)` → `ad_workflow.(ad_workflow_id)` | Workflow |

<a id="t-ad_wf_eventaudit"></a>
## `ad_wf_eventaudit` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Event Audit`
- 사전 Description: Workflow Process Activity Event Audit Information
- 근거 문장: 사전 Name='Workflow Event Audit'; Description='Workflow Process Activity Event Audit Information'; 주요 열 wfstate, ad_wf_process_id, ad_wf_node_id, ad_wf_responsible_id; FK adwfnode_adwfeventaudit, adwfprocess_adwfeventaudit; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `wfstate` | Workflow State | `character(2)` |
| `ad_wf_process_id` | Workflow Process | `numeric(10,0)` |
| `ad_wf_node_id` | Node | `numeric(10,0)` |
| `ad_wf_responsible_id` | Workflow Responsible | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adwfnode_adwfeventaudit` | `ad_wf_eventaudit.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Node |
| outgoing | `adwfprocess_adwfeventaudit` | `ad_wf_eventaudit.(ad_wf_process_id)` → `ad_wf_process.(ad_wf_process_id)` | Workflow Process |
| outgoing | `adwfresponsib_adwfeventaudit` | `ad_wf_eventaudit.(ad_wf_responsible_id)` → `ad_wf_responsible.(ad_wf_responsible_id)` | Workflow Responsible |

<a id="t-ad_wf_nextcondition"></a>
## `ad_wf_nextcondition` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Transition Condition`
- 사전 Description: Workflow Node Transition Condition
- 근거 문장: 사전 Name='Transition Condition'; Description='Workflow Node Transition Condition'; 주요 열 ad_wf_nodenext_id; FK adwfnodenext_adwfnextcond; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_wf_nodenext_id` | Node Transition | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adwfnodenext_adwfnextcond` | `ad_wf_nextcondition.(ad_wf_nodenext_id)` → `ad_wf_nodenext.(ad_wf_nodenext_id)` | Node Transition |

<a id="t-ad_wf_node"></a>
## `ad_wf_node` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Node`
- 사전 Description: Workflow Node (activity) step or process
- 근거 문장: 사전 Name='Node'; Description='Workflow Node (activity) step or process'; 주요 열 ad_workflow_id, iscentrallymaintained, action, ad_wf_block_id; FK ad_wfnodetrl, adwfnode_adwfactivity; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_workflow_id` | Workflow | `numeric(10,0)` |
| `iscentrallymaintained` | Centrally maintained | `character(1)` |
| `action` | Action | `character(1)` |
| `ad_wf_block_id` | Workflow Block | `numeric(10,0)` |
| `priority` | Priority | `numeric(10,0)` |
| `ad_wf_responsible_id` | Workflow Responsible | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_wfnodetrl` | `ad_wf_node_trl.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Node Trl |
| incoming | `adwfnode_adwfactivity` | `ad_wf_activity.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Workflow Activity |
| incoming | `adwfnode_adwfeventaudit` | `ad_wf_eventaudit.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Workflow Event Audit |
| incoming | `adwfnode_adwfnodenext` | `ad_wf_nodenext.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Node Transition |

<a id="t-ad_wf_node_para"></a>
## `ad_wf_node_para` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Node Parameter`
- 사전 Description: Workflow Node Execution Parameter
- 근거 문장: 사전 Name='Workflow Node Parameter'; Description='Workflow Node Execution Parameter'; 주요 열 ad_wf_node_id; FK adwfnode_adwfnodepara; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_wf_node_id` | Node | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adwfnode_adwfnodepara` | `ad_wf_node_para.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Node |

<a id="t-ad_wf_node_trl"></a>
## `ad_wf_node_trl` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Node Trl`
- 사전 Description: Workflow Node (activity), step or process
- 근거 문장: 사전 Name='Node Trl'; Description='Workflow Node (activity), step or process'; 주요 열 근거 부족; FK ad_wfnodetrl; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_wfnodetrl` | `ad_wf_node_trl.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Node |

<a id="t-ad_wf_nodenext"></a>
## `ad_wf_nodenext` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Node Transition`
- 사전 Description: Workflow Node Transition
- 근거 문장: 사전 Name='Node Transition'; Description='Workflow Node Transition'; 주요 열 ad_wf_node_id, ad_wf_next_id, transitioncode; FK adwfnodenext_adwfnextcond, adwfnode_adwfnodenext; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_wf_node_id` | Node | `numeric(10,0)` |
| `ad_wf_next_id` | Next Node | `numeric(10,0)` |
| `transitioncode` | Transition Code | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adwfnodenext_adwfnextcond` | `ad_wf_nextcondition.(ad_wf_nodenext_id)` → `ad_wf_nodenext.(ad_wf_nodenext_id)` | Transition Condition |
| outgoing | `adwfnode_adwfnodenext` | `ad_wf_nodenext.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Node |
| outgoing | `adwfnodenext_adwfnodenext` | `ad_wf_nodenext.(ad_wf_next_id)` → `ad_wf_node.(ad_wf_node_id)` | Node |

<a id="t-ad_wf_process"></a>
## `ad_wf_process` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Process`
- 사전 Description: Actual Workflow Process Instance
- 근거 문장: 사전 Name='Workflow Process'; Description='Actual Workflow Process Instance'; 주요 열 ad_workflow_id, ad_wf_responsible_id, wfstate, priority; FK adwfproccess_adwfprocessdata, adwfprocess_adwfactivity; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_workflow_id` | Workflow | `numeric(10,0)` |
| `ad_wf_responsible_id` | Workflow Responsible | `numeric(10,0)` |
| `wfstate` | Workflow State | `character(2)` |
| `priority` | Priority | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adwfproccess_adwfprocessdata` | `ad_wf_processdata.(ad_wf_process_id)` → `ad_wf_process.(ad_wf_process_id)` | Workflow Process Data |
| incoming | `adwfprocess_adwfactivity` | `ad_wf_activity.(ad_wf_process_id)` → `ad_wf_process.(ad_wf_process_id)` | Workflow Activity |
| incoming | `adwfprocess_adwfeventaudit` | `ad_wf_eventaudit.(ad_wf_process_id)` → `ad_wf_process.(ad_wf_process_id)` | Workflow Event Audit |
| outgoing | `adwfprocess_adwfprocess` | `ad_wf_process.(ad_wf_process_id)` → `ad_wf_process.(ad_wf_process_id)` | Workflow Process |

<a id="t-ad_wf_processdata"></a>
## `ad_wf_processdata` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Process Data`
- 사전 Description: Workflow Process Context
- 근거 문장: 사전 Name='Workflow Process Data'; Description='Workflow Process Context'; 주요 열 ad_wf_process_id; FK adwfproccess_adwfprocessdata; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_wf_process_id` | Workflow Process | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adwfproccess_adwfprocessdata` | `ad_wf_processdata.(ad_wf_process_id)` → `ad_wf_process.(ad_wf_process_id)` | Workflow Process |

<a id="t-ad_wf_responsible"></a>
## `ad_wf_responsible` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Responsible`
- 사전 Description: Responsible for Workflow Execution
- 근거 문장: 사전 Name='Workflow Responsible'; Description='Responsible for Workflow Execution'; 주요 열 근거 부족; FK adwfresponsib_adwfeventaudit, adwfresponsible_adwfactivity; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adwfresponsib_adwfeventaudit` | `ad_wf_eventaudit.(ad_wf_responsible_id)` → `ad_wf_responsible.(ad_wf_responsible_id)` | Workflow Event Audit |
| incoming | `adwfresponsible_adwfactivity` | `ad_wf_activity.(ad_wf_responsible_id)` → `ad_wf_responsible.(ad_wf_responsible_id)` | Workflow Activity |
| incoming | `adwfresponsible_adwfnode` | `ad_wf_node.(ad_wf_responsible_id)` → `ad_wf_responsible.(ad_wf_responsible_id)` | Node |
| incoming | `adwfresponsible_adwfprocess` | `ad_wf_process.(ad_wf_responsible_id)` → `ad_wf_responsible.(ad_wf_responsible_id)` | Workflow Process |

<a id="t-ad_window"></a>
## `ad_window` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Window`
- 사전 Description: Data entry or display window
- 근거 문장: 사전 Name='Window'; Description='Data entry or display window'; 주요 열 ad_color_id; FK ad_window_preference, ad_window_tab; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_color_id` | System Color | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_window_preference` | `ad_preference.(ad_window_id)` → `ad_window.(ad_window_id)` | Preference |
| incoming | `ad_window_tab` | `ad_tab.(ad_window_id)` → `ad_window.(ad_window_id)` | Tab |
| incoming | `ad_window_table` | `ad_table.(ad_window_id)` → `ad_window.(ad_window_id)` | Table |
| incoming | `ad_windowtrl` | `ad_window_trl.(ad_window_id)` → `ad_window.(ad_window_id)` | Window Trl |

<a id="t-ad_window_access"></a>
## `ad_window_access` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Window_Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Window_Access'; 주요 열 근거 부족; FK adrole_adwindowaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_adwindowaccess` | `ad_window_access.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-ad_window_trl"></a>
## `ad_window_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Window Trl`
- 사전 Description: Data entry or display window
- 근거 문장: 사전 Name='Window Trl'; Description='Data entry or display window'; 주요 열 근거 부족; FK ad_windowtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_windowtrl` | `ad_window_trl.(ad_window_id)` → `ad_window.(ad_window_id)` | Window |

<a id="t-ad_wizardprocess"></a>
## `ad_wizardprocess` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Wizard Process`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Wizard Process'; 주요 열 근거 부족; FK adwfnode_adwizardprocess; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adwfnode_adwizardprocess` | `ad_wizardprocess.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Node |

<a id="t-ad_wlistbox_customization"></a>
## `ad_wlistbox_customization` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Customization of the Wlistbox`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Customization of the Wlistbox'; 주요 열 ad_user_id, custom, wlistboxname; FK aduser_adwlistboxcustomization; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `custom` | Custom | `character varying(4000)` |
| `wlistboxname` | WlistboxName | `character varying(80)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_adwlistboxcustomization` | `ad_wlistbox_customization.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-ad_workbench"></a>
## `ad_workbench` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workbench`
- 사전 Description: Collection of windows, reports
- 근거 문장: 사전 Name='Workbench'; Description='Collection of windows, reports'; 주요 열 ad_column_id, ad_color_id; FK admenu_adworkbench, adworkbench_addesktopwb; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_column_id` | Column | `numeric(10,0)` |
| `ad_color_id` | System Color | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `admenu_adworkbench` | `ad_menu.(ad_workbench_id)` → `ad_workbench.(ad_workbench_id)` | Menu |
| incoming | `adworkbench_addesktopwb` | `ad_desktopworkbench.(ad_workbench_id)` → `ad_workbench.(ad_workbench_id)` | Desktop Workbench |
| incoming | `adworkbench_adworkbenchtrl` | `ad_workbench_trl.(ad_workbench_id)` → `ad_workbench.(ad_workbench_id)` | Workbench Trl |
| incoming | `adworkbench_adworkbenchwindow` | `ad_workbenchwindow.(ad_workbench_id)` → `ad_workbench.(ad_workbench_id)` | Workbench Window |

<a id="t-ad_workbench_trl"></a>
## `ad_workbench_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workbench Trl`
- 사전 Description: Collection of windows, reports
- 근거 문장: 사전 Name='Workbench Trl'; Description='Collection of windows, reports'; 주요 열 근거 부족; FK adworkbench_adworkbenchtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adworkbench_adworkbenchtrl` | `ad_workbench_trl.(ad_workbench_id)` → `ad_workbench.(ad_workbench_id)` | Workbench |

<a id="t-ad_workbenchwindow"></a>
## `ad_workbenchwindow` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workbench Window`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Workbench Window'; 주요 열 seqno, ad_window_id, ad_form_id; FK adform_adworkbenchwindow, adwindow_adworkbenchwindow; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |
| `ad_form_id` | Special Form | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adform_adworkbenchwindow` | `ad_workbenchwindow.(ad_form_id)` → `ad_form.(ad_form_id)` | Special Form |
| outgoing | `adwindow_adworkbenchwindow` | `ad_workbenchwindow.(ad_window_id)` → `ad_window.(ad_window_id)` | Window |
| outgoing | `adworkbench_adworkbenchwindow` | `ad_workbenchwindow.(ad_workbench_id)` → `ad_workbench.(ad_workbench_id)` | Workbench |
| outgoing | `entityt_adworkbenchwindow` | `ad_workbenchwindow.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

<a id="t-ad_workflow"></a>
## `ad_workflow` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow`
- 사전 Description: Workflow or combination of tasks
- 근거 문장: 사전 Name='Workflow'; Description='Workflow or combination of tasks'; 주요 열 ad_wf_node_id, priority, ad_wf_responsible_id, ad_workflowprocessor_id; FK ad_workflowtrl, adworkflow_adwfactivity; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_wf_node_id` | Node | `numeric(10,0)` |
| `priority` | Priority | `numeric(10,0)` |
| `ad_wf_responsible_id` | Workflow Responsible | `numeric(10,0)` |
| `ad_workflowprocessor_id` | Workflow Processor | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ad_workflowtrl` | `ad_workflow_trl.(ad_workflow_id)` → `ad_workflow.(ad_workflow_id)` | Workflow Trl |
| incoming | `adworkflow_adwfactivity` | `ad_wf_activity.(ad_workflow_id)` → `ad_workflow.(ad_workflow_id)` | Workflow Activity |
| incoming | `adworkflow_adwfblock` | `ad_wf_block.(ad_workflow_id)` → `ad_workflow.(ad_workflow_id)` | Workflow Block |
| incoming | `adworkflow_adwfnode` | `ad_wf_node.(ad_workflow_id)` → `ad_workflow.(ad_workflow_id)` | Node |

<a id="t-ad_workflow_access"></a>
## `ad_workflow_access` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `AD_Workflow_Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='AD_Workflow_Access'; 주요 열 근거 부족; FK adworkfow_workflowaccess; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adworkfow_workflowaccess` | `ad_workflow_access.(ad_workflow_id)` → `ad_workflow.(ad_workflow_id)` | Workflow |

<a id="t-ad_workflow_trl"></a>
## `ad_workflow_trl` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Trl`
- 사전 Description: Workflow or combination of tasks
- 근거 문장: 사전 Name='Workflow Trl'; Description='Workflow or combination of tasks'; 주요 열 근거 부족; FK ad_workflowtrl; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ad_workflowtrl` | `ad_workflow_trl.(ad_workflow_id)` → `ad_workflow.(ad_workflow_id)` | Workflow |

<a id="t-ad_workflowprocessor"></a>
## `ad_workflowprocessor` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Processor`
- 사전 Description: Workflow Processor Server
- 근거 문장: 사전 Name='Workflow Processor'; Description='Workflow Processor Server'; 주요 열 alertoverpriority; FK adworkflowprocessor_adwf, adworkflowprocessor_log; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `alertoverpriority` | Alert over Priority | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `adworkflowprocessor_adwf` | `ad_workflow.(ad_workflowprocessor_id)` → `ad_workflowprocessor.(ad_workflowprocessor_id)` | Workflow |
| incoming | `adworkflowprocessor_log` | `ad_workflowprocessorlog.(ad_workflowprocessor_id)` → `ad_workflowprocessor.(ad_workflowprocessor_id)` | Workflow Processor Log |
| incoming | `adworkflowprocessor_pporderwor` | `pp_order_workflow.(ad_workflowprocessor_id)` → `ad_workflowprocessor.(ad_workflowprocessor_id)` | Manufacturing Order Workflow |

<a id="t-ad_workflowprocessorlog"></a>
## `ad_workflowprocessorlog` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Processor Log`
- 사전 Description: Result of the execution of the Workflow Processor
- 근거 문장: 사전 Name='Workflow Processor Log'; Description='Result of the execution of the Workflow Processor'; 주요 열 근거 부족; FK adworkflowprocessor_log; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adworkflowprocessor_log` | `ad_workflowprocessorlog.(ad_workflowprocessor_id)` → `ad_workflowprocessor.(ad_workflowprocessor_id)` | Workflow Processor |

<a id="t-ad_zoomcondition"></a>
## `ad_zoomcondition` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Zoom condition`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Zoom condition'; 주요 열 ad_table_id, ad_window_id, seqno, whereclause; FK adtable_adzoomcondition, adwindow_adzoomcondition; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `ad_window_id` | Window | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `whereclause` | Sql WHERE | `character varying(2000)` |
| `zoomlogic` | Zoom Logic | `character varying(2000)` |
| `entitytype` | Entity Type | `character varying(40)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_adzoomcondition` | `ad_zoomcondition.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `adwindow_adzoomcondition` | `ad_zoomcondition.(ad_window_id)` → `ad_window.(ad_window_id)` | Window |
| outgoing | `entitytype_adzoomcondition` | `ad_zoomcondition.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-asp_clientexception"></a>
## `asp_clientexception` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tenant Exception`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tenant Exception'; 주요 열 ad_field_id, ad_form_id, ad_process_id, ad_process_para_id; FK adfield_aspclientexception, adform_aspclientexception; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_field_id` | Field | `numeric(10,0)` |
| `ad_form_id` | Special Form | `numeric(10,0)` |
| `ad_process_id` | Process | `numeric(10,0)` |
| `ad_process_para_id` | Process Parameter | `numeric(10,0)` |
| `ad_tab_id` | Tab | `numeric(10,0)` |
| `ad_task_id` | OS Task | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adfield_aspclientexception` | `asp_clientexception.(ad_field_id)` → `ad_field.(ad_field_id)` | Field |
| outgoing | `adform_aspclientexception` | `asp_clientexception.(ad_form_id)` → `ad_form.(ad_form_id)` | Special Form |
| outgoing | `adprocess_aspclientexception` | `asp_clientexception.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |
| outgoing | `adprocesspara_aspclientexcepti` | `asp_clientexception.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | Process Parameter |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-asp_clientlevel"></a>
## `asp_clientlevel` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tenant Level`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tenant Level'; 주요 열 asp_level_id, asp_module_id; FK asplevel_aspclientlevel, aspmodule_aspclientlevel; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `asp_level_id` | ASP Level | `numeric(10,0)` |
| `asp_module_id` | ASP Module | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `asplevel_aspclientlevel` | `asp_clientlevel.(asp_level_id)` → `asp_level.(asp_level_id)` | ASP Level |
| outgoing | `aspmodule_aspclientlevel` | `asp_clientlevel.(asp_module_id)` → `asp_module.(asp_module_id)` | ASP Module |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-asp_field"></a>
## `asp_field` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP Field`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP Field'; 주요 열 ad_field_id; FK adfield_aspfield, asptab_aspfield; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_field_id` | Field | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adfield_aspfield` | `asp_field.(ad_field_id)` → `ad_field.(ad_field_id)` | Field |
| outgoing | `asptab_aspfield` | `asp_field.(asp_tab_id)` → `asp_tab.(asp_tab_id)` | ASP Tab |

<a id="t-asp_form"></a>
## `asp_form` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP Form`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP Form'; 주요 열 ad_form_id; FK adform_aspform; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_form_id` | Special Form | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adform_aspform` | `asp_form.(ad_form_id)` → `ad_form.(ad_form_id)` | Special Form |

<a id="t-asp_level"></a>
## `asp_level` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP Level`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP Level'; 주요 열 asp_module_id, processing; FK asplevel_aspclientlevel, asplevel_aspform; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `asp_module_id` | ASP Module | `numeric(10,0)` |
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `asplevel_aspclientlevel` | `asp_clientlevel.(asp_level_id)` → `asp_level.(asp_level_id)` | Tenant Level |
| incoming | `asplevel_aspform` | `asp_form.(asp_level_id)` → `asp_level.(asp_level_id)` | ASP Form |
| outgoing | `aspmodule_asplevel` | `asp_level.(asp_module_id)` → `asp_module.(asp_module_id)` | ASP Module |
| incoming | `asplevel_aspprocess` | `asp_process.(asp_level_id)` → `asp_level.(asp_level_id)` | ASP Process |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-asp_module"></a>
## `asp_module` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP Module`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP Module'; 주요 열 근거 부족; FK aspmodule_aspclientlevel, aspmodule_asplevel; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aspmodule_aspclientlevel` | `asp_clientlevel.(asp_module_id)` → `asp_module.(asp_module_id)` | Tenant Level |
| incoming | `aspmodule_asplevel` | `asp_level.(asp_module_id)` → `asp_module.(asp_module_id)` | ASP Level |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-asp_process"></a>
## `asp_process` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP Process`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP Process'; 주요 열 ad_process_id; FK aspprocess_aspprocesspara, adprocess_aspprocess; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_process_id` | Process | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aspprocess_aspprocesspara` | `asp_process_para.(asp_process_id)` → `asp_process.(asp_process_id)` | ASP Process Parameter |
| outgoing | `adprocess_aspprocess` | `asp_process.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |

<a id="t-asp_process_para"></a>
## `asp_process_para` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP Process Parameter`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP Process Parameter'; 주요 열 ad_process_para_id; FK adprocesspara_aspprocesspara, aspprocess_aspprocesspara; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_process_para_id` | Process Parameter | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprocesspara_aspprocesspara` | `asp_process_para.(ad_process_para_id)` → `ad_process_para.(ad_process_para_id)` | Process Parameter |
| outgoing | `aspprocess_aspprocesspara` | `asp_process_para.(asp_process_id)` → `asp_process.(asp_process_id)` | ASP Process |

<a id="t-asp_ref_list"></a>
## `asp_ref_list` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP_Ref_List`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP_Ref_List'; 주요 열 ad_reference_id, ad_ref_list_id, asp_level_id, asp_status; FK adreference_aspreflist, adreflist_aspreflist; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_reference_id` | Reference | `numeric(10,0)` |
| `ad_ref_list_id` | Reference List | `numeric(10,0)` |
| `asp_level_id` | ASP Level | `numeric(10,0)` |
| `asp_status` | ASP Status | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adreference_aspreflist` | `asp_ref_list.(ad_reference_id)` → `ad_reference.(ad_reference_id)` | Reference |
| outgoing | `adreflist_aspreflist` | `asp_ref_list.(ad_ref_list_id)` → `ad_ref_list.(ad_ref_list_id)` | Reference List |
| outgoing | `asplevel_aspreflist` | `asp_ref_list.(asp_level_id)` → `asp_level.(asp_level_id)` | ASP Level |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-asp_tab"></a>
## `asp_tab` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP Tab`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP Tab'; 주요 열 ad_tab_id; FK asptab_aspfield, adtab_asptab; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_tab_id` | Tab | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `asptab_aspfield` | `asp_field.(asp_tab_id)` → `asp_tab.(asp_tab_id)` | ASP Field |
| outgoing | `adtab_asptab` | `asp_tab.(ad_tab_id)` → `ad_tab.(ad_tab_id)` | Tab |
| outgoing | `aspwindow_asptab` | `asp_tab.(asp_window_id)` → `asp_window.(asp_window_id)` | ASP Window |

<a id="t-asp_task"></a>
## `asp_task` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP Task`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP Task'; 주요 열 ad_task_id, asp_level_id, asp_status; FK adtask_asptask, asplevel_asptask; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_task_id` | OS Task | `numeric(10,0)` |
| `asp_level_id` | ASP Level | `numeric(10,0)` |
| `asp_status` | ASP Status | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtask_asptask` | `asp_task.(ad_task_id)` → `ad_task.(ad_task_id)` | OS Task |
| outgoing | `asplevel_asptask` | `asp_task.(asp_level_id)` → `asp_level.(asp_level_id)` | ASP Level |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-asp_window"></a>
## `asp_window` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP Window`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP Window'; 주요 열 ad_window_id; FK aspwindow_asptab, adwindow_aspwindow; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_window_id` | Window | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aspwindow_asptab` | `asp_tab.(asp_window_id)` → `asp_window.(asp_window_id)` | ASP Tab |
| outgoing | `adwindow_aspwindow` | `asp_window.(ad_window_id)` → `ad_window.(ad_window_id)` | Window |

<a id="t-asp_workflow"></a>
## `asp_workflow` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `ASP Workflow`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='ASP Workflow'; 주요 열 ad_workflow_id; FK adworkflow_aspworkflow; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_workflow_id` | Workflow | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adworkflow_aspworkflow` | `asp_workflow.(ad_workflow_id)` → `ad_workflow.(ad_workflow_id)` | Workflow |

<a id="t-b_bid"></a>
## `b_bid` — 경매·입찰·판매 제안

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bid`
- 사전 Description: Bid for a Topic
- 근거 문장: 사전 Name='Bid'; Description='Bid for a Topic'; 주요 열 b_topic_id, b_buyerfunds_id; FK bbuyerfunds_bbid, btopic_bbid; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `b_topic_id` | Topic | `numeric(10,0)` |
| `b_buyerfunds_id` | Buyer Funds | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `bbuyerfunds_bbid` | `b_bid.(b_buyerfunds_id)` → `b_buyerfunds.(b_buyerfunds_id)` | Buyer Funds |
| outgoing | `btopic_bbid` | `b_bid.(b_topic_id)` → `b_topic.(b_topic_id)` | Topic |

<a id="t-b_bidcomment"></a>
## `b_bidcomment` — 경매·입찰·판매 제안

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bid Comment`
- 사전 Description: Make a comment to a Bid Topic
- 근거 문장: 사전 Name='Bid Comment'; Description='Make a comment to a Bid Topic'; 주요 열 근거 부족; FK btopic_bbidcomment; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `btopic_bbidcomment` | `b_bidcomment.(b_topic_id)` → `b_topic.(b_topic_id)` | Topic |

<a id="t-b_buyer"></a>
## `b_buyer` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `B_Buyer`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='B_Buyer'; 주요 열 validto; FK bbuyer_bbid, aduser_bbuyer; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `validto` | Valid to | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `bbuyer_bbid` | `b_bid.(ad_user_id)` → `b_buyer.(ad_user_id)` | Bid |
| outgoing | `aduser_bbuyer` | `b_buyer.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| incoming | `bbuyer_bbuyerfunds` | `b_buyerfunds.(ad_user_id)` → `b_buyer.(ad_user_id)` | Buyer Funds |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-b_buyerfunds"></a>
## `b_buyerfunds` — 경매·입찰·판매 제안

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Buyer Funds`
- 사전 Description: Buyer Funds for Bids on Topics
- 근거 문장: 사전 Name='Buyer Funds'; Description='Buyer Funds for Bids on Topics'; 주요 열 근거 부족; FK bbuyerfunds_bbid; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `bbuyerfunds_bbid` | `b_bid.(b_buyerfunds_id)` → `b_buyerfunds.(b_buyerfunds_id)` | Bid |

<a id="t-b_offer"></a>
## `b_offer` — 경매·입찰·판매 제안

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Offer`
- 사전 Description: Offer for a Topic
- 근거 문장: 사전 Name='Offer'; Description='Offer for a Topic'; 주요 열 b_topic_id, b_sellerfunds_id; FK bsellerfunds_boffer, btopic_boffer; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `b_topic_id` | Topic | `numeric(10,0)` |
| `b_sellerfunds_id` | Seller Funds | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `bsellerfunds_boffer` | `b_offer.(b_sellerfunds_id)` → `b_sellerfunds.(b_sellerfunds_id)` | Seller Funds |
| outgoing | `btopic_boffer` | `b_offer.(b_topic_id)` → `b_topic.(b_topic_id)` | Topic |

<a id="t-b_seller"></a>
## `b_seller` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `B_Seller`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='B_Seller'; 주요 열 validto, isinternal; FK bseller_boffer, aduser_bseller; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `validto` | Valid to | `timestamp without time zone` |
| `isinternal` | Internal | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `bseller_boffer` | `b_offer.(ad_user_id)` → `b_seller.(ad_user_id)` | Offer |
| outgoing | `aduser_bseller` | `b_seller.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| incoming | `bseller_bsellerfunds` | `b_sellerfunds.(ad_user_id)` → `b_seller.(ad_user_id)` | Seller Funds |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-b_sellerfunds"></a>
## `b_sellerfunds` — 경매·입찰·판매 제안

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Seller Funds`
- 사전 Description: Seller Funds from Offers on Topics
- 근거 문장: 사전 Name='Seller Funds'; Description='Seller Funds from Offers on Topics'; 주요 열 근거 부족; FK bsellerfunds_boffer; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `bsellerfunds_boffer` | `b_offer.(b_sellerfunds_id)` → `b_sellerfunds.(b_sellerfunds_id)` | Offer |

<a id="t-b_topic"></a>
## `b_topic` — 경매·입찰·판매 제안

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Topic`
- 사전 Description: Auction Topic
- 근거 문장: 사전 Name='Topic'; Description='Auction Topic'; 주요 열 b_topictype_id, b_topiccategory_id; FK btopic_bbid, btopic_bbidcomment; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `b_topictype_id` | Topic Type | `numeric(10,0)` |
| `b_topiccategory_id` | Topic Category | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `btopic_bbid` | `b_bid.(b_topic_id)` → `b_topic.(b_topic_id)` | Bid |
| incoming | `btopic_bbidcomment` | `b_bidcomment.(b_topic_id)` → `b_topic.(b_topic_id)` | Bid Comment |
| incoming | `btopic_boffer` | `b_offer.(b_topic_id)` → `b_topic.(b_topic_id)` | Offer |
| outgoing | `btopiccategory_btopic` | `b_topic.(b_topiccategory_id)` → `b_topiccategory.(b_topiccategory_id)` | Topic Category |

<a id="t-b_topiccategory"></a>
## `b_topiccategory` — 경매·입찰·판매 제안

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Topic Category`
- 사전 Description: Auction Topic Category
- 근거 문장: 사전 Name='Topic Category'; Description='Auction Topic Category'; 주요 열 b_topictype_id; FK btopiccategory_btopic, btopictype_btopiccategory; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `b_topictype_id` | Topic Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `btopiccategory_btopic` | `b_topic.(b_topiccategory_id)` → `b_topiccategory.(b_topiccategory_id)` | Topic |
| outgoing | `btopictype_btopiccategory` | `b_topiccategory.(b_topictype_id)` → `b_topictype.(b_topictype_id)` | Topic Type |

<a id="t-b_topictype"></a>
## `b_topictype` — 경매·입찰·판매 제안

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Topic Type`
- 사전 Description: Auction Topic Type
- 근거 문장: 사전 Name='Topic Type'; Description='Auction Topic Type'; 주요 열 m_pricelist_id; FK btopictype_btopic, btopictype_btopiccategory; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_pricelist_id` | Price List | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `btopictype_btopic` | `b_topic.(b_topictype_id)` → `b_topictype.(b_topictype_id)` | Topic |
| incoming | `btopictype_btopiccategory` | `b_topiccategory.(b_topictype_id)` → `b_topictype.(b_topictype_id)` | Topic Category |

<a id="t-c_1099box"></a>
## `c_1099box` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `1099 Box`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='1099 Box'; 주요 열 bucket; FK default1099box_cbpartner, c1099box_cinvoiceline; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `bucket` | Bucket | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `default1099box_cbpartner` | `c_bpartner.(default1099box_id)` → `c_1099box.(c_1099box_id)` | Business Partner |
| incoming | `c1099box_cinvoiceline` | `c_invoiceline.(c_1099box_id)` → `c_1099box.(c_1099box_id)` | Invoice Line |
| incoming | `c1099box_iinvoice` | `i_invoice.(c_1099box_id)` → `c_1099box.(c_1099box_id)` | Import Invoice |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_acctprocessor"></a>
## `c_acctprocessor` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Accounting Processor`
- 사전 Description: Accounting Processor/Server Parameters
- 근거 문장: 사전 Name='Accounting Processor'; Description='Accounting Processor/Server Parameters'; 주요 열 c_acctschema_id; FK cacctprocessor_log, cacctschema_cacctprocessor; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cacctprocessor_log` | `c_acctprocessorlog.(c_acctprocessor_id)` → `c_acctprocessor.(c_acctprocessor_id)` | Accounting Processor Log |
| outgoing | `cacctschema_cacctprocessor` | `c_acctprocessor.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |

<a id="t-c_acctprocessorlog"></a>
## `c_acctprocessorlog` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Accounting Processor Log`
- 사전 Description: Result of the execution of the Accounting Processor
- 근거 문장: 사전 Name='Accounting Processor Log'; Description='Result of the execution of the Accounting Processor'; 주요 열 근거 부족; FK cacctprocessor_log; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctprocessor_log` | `c_acctprocessorlog.(c_acctprocessor_id)` → `c_acctprocessor.(c_acctprocessor_id)` | Accounting Processor |

<a id="t-c_acctschema"></a>
## `c_acctschema` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Accounting Schema`
- 사전 Description: Rules for accounting
- 근거 문장: 사전 Name='Accounting Schema'; Description='Rules for accounting'; 주요 열 isallownegativeposting; FK c_acctschema_gl_journal, cacctschema_aassetacct; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isallownegativeposting` | Allow Negative Posting | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_acctschema_gl_journal` | `gl_journal.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Journal |
| incoming | `cacctschema_aassetacct` | `a_asset_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | A_Asset_Acct_ID |
| incoming | `cacctschema_aassetgroupacct` | `a_asset_group_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Asset Group Accounting |
| incoming | `cacctschema_afundingmodeacct` | `a_fundingmode_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Asset Funding Mode Accounting |

<a id="t-c_acctschema_default"></a>
## `c_acctschema_default` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_AcctSchema_Default`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_AcctSchema_Default'; 주요 열 w_inventory_acct, w_invactualadjust_acct, w_differences_acct, w_revaluation_acct; FK cacctschema_default, chrevenue_cacctschemadefault; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `w_inventory_acct` | (Not Used) | `numeric(10,0)` |
| `w_invactualadjust_acct` | Inventory Adjustment | `numeric(10,0)` |
| `w_differences_acct` | Warehouse Differences | `numeric(10,0)` |
| `w_revaluation_acct` | Inventory Revaluation | `numeric(10,0)` |
| `p_revenue_acct` | Product Revenue | `numeric(10,0)` |
| `p_expense_acct` | Product Expense | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_default` | `c_acctschema_default.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `chrevenue_cacctschemadefault` | `c_acctschema_default.(ch_revenue_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `creceivableservices_cacctschem` | `c_acctschema_default.(c_receivable_services_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `paveragecostvariance_cacctsche` | `c_acctschema_default.(p_averagecostvariance_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_acctschema_element"></a>
## `c_acctschema_element` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Acct.Schema Element`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Acct.Schema Element'; 주요 열 c_acctschema_id, elementtype, seqno, c_element_id; FK aasset_cacctschemaelement, adcolumn2_cacctschemaelement; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `elementtype` | Type | `character(2)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `c_element_id` | Element | `numeric(10,0)` |
| `ismandatory` | Mandatory | `character(1)` |
| `isbalanced` | Balanced | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aasset_cacctschemaelement` | `c_acctschema_element.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |
| outgoing | `adcolumn2_cacctschemaelement` | `c_acctschema_element.(ad_column2_id)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `adcolumn_cacctschemaelement` | `c_acctschema_element.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `adorg_caschemaelement` | `c_acctschema_element.(org_id)` → `ad_org.(ad_org_id)` | Organization |

검토 후보: 회계·원장·예산 (규칙 점수 13); 애플리케이션 사전·화면·서식 (규칙 점수 13).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_acctschema_gl"></a>
## `c_acctschema_gl` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_AcctSchema_GL`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_AcctSchema_GL'; 주요 열 suspensebalancing_acct, suspenseerror_acct, currencybalancing_acct, retainedearning_acct; FK cacctschema_cacctschemagl, commitmentoffset_cacctschemagl; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `suspensebalancing_acct` | Suspense Balancing Acct | `numeric(10,0)` |
| `suspenseerror_acct` | Suspense Error Acct | `numeric(10,0)` |
| `currencybalancing_acct` | Currency Balancing Acct | `numeric(10,0)` |
| `retainedearning_acct` | Retained Earning Acct | `numeric(10,0)` |
| `incomesummary_acct` | Income Summary Acct | `numeric(10,0)` |
| `intercompanydueto_acct` | Intercompany Due To Acct | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_cacctschemagl` | `c_acctschema_gl.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `commitmentoffset_cacctschemagl` | `c_acctschema_gl.(commitmentoffset_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `commitmentoffsetsales_cacctsch` | `c_acctschema_gl.(commitmentoffsetsales_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_currencybalancing_cschemagl` | `c_acctschema_gl.(currencybalancing_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_activity"></a>
## `c_activity` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Activity`
- 사전 Description: Business Activity
- 근거 문장: 사전 Name='Activity'; Description='Business Activity'; 주요 열 근거 부족; FK cactivity_cactivitytrl, cactivity_cproject; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cactivity_cactivitytrl` | `c_activity_trl.(c_activity_id)` → `c_activity.(c_activity_id)` | Activity Trl |
| incoming | `cactivity_cproject` | `c_project.(c_activity_id)` → `c_activity.(c_activity_id)` | Project |

<a id="t-c_activity_trl"></a>
## `c_activity_trl` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Activity Trl`
- 사전 Description: Business Activity
- 근거 문장: 사전 Name='Activity Trl'; Description='Business Activity'; 주요 열 근거 부족; FK cactivity_cactivitytrl; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cactivity_cactivitytrl` | `c_activity_trl.(c_activity_id)` → `c_activity.(c_activity_id)` | Activity |

<a id="t-c_addresstransaction"></a>
## `c_addresstransaction` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Address Transaction`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Address Transaction'; 주요 열 address1, address2, address3, address4; FK caddressvalidation_caddresstra, clocation_caddresstransaction; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `address1` | Address 1 | `character varying(60)` |
| `address2` | Address 2 | `character varying(60)` |
| `address3` | Address 3 | `character varying(60)` |
| `address4` | Address 4 | `character varying(60)` |
| `c_addressvalidation_id` | Address Validation | `numeric(10,0)` |
| `c_location_id` | Address | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `caddressvalidation_caddresstra` | `c_addresstransaction.(c_addressvalidation_id)` → `c_addressvalidation.(c_addressvalidation_id)` | Address Validation |
| outgoing | `clocation_caddresstransaction` | `c_addresstransaction.(c_location_id)` → `c_location.(c_location_id)` | Address |

<a id="t-c_addressvalidation"></a>
## `c_addressvalidation` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Address Validation`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Address Validation'; 주요 열 c_addressvalidationcfg_id; FK caddressvalidation_caddresstra, caddressvalidation_clocation; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_addressvalidationcfg_id` | Address Validation Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `caddressvalidation_caddresstra` | `c_addresstransaction.(c_addressvalidation_id)` → `c_addressvalidation.(c_addressvalidation_id)` | Address Transaction |
| incoming | `caddressvalidation_clocation` | `c_location.(c_addressvalidation_id)` → `c_addressvalidation.(c_addressvalidation_id)` | Address |
| outgoing | `caddressvalidationcfg_caddress` | `c_addressvalidation.(c_addressvalidationcfg_id)` → `c_addressvalidationcfg.(c_addressvalidationcfg_id)` | Address Validation Configuration |

<a id="t-c_addressvalidationcfg"></a>
## `c_addressvalidationcfg` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Address Validation Configuration`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Address Validation Configuration'; 주요 열 addressvalidationclass, hostaddress, proxyaddress; FK caddressvalidationcfg_caddress; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `addressvalidationclass` | Address Validation Class | `character varying(100)` |
| `hostaddress` | Host Address | `character varying(60)` |
| `proxyaddress` | Proxy address | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `caddressvalidationcfg_caddress` | `c_addressvalidation.(c_addressvalidationcfg_id)` → `c_addressvalidationcfg.(c_addressvalidationcfg_id)` | Address Validation |

<a id="t-c_allocationhdr"></a>
## `c_allocationhdr` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Allocation`
- 사전 Description: Payment allocation
- 근거 문장: 사전 Name='Allocation'; Description='Payment allocation'; 주요 열 근거 부족; FK callocation_callocationline, reversal_callocationhdr; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `callocation_callocationline` | `c_allocationline.(c_allocationhdr_id)` → `c_allocationhdr.(c_allocationhdr_id)` | Allocation Line |
| outgoing | `reversal_callocationhdr` | `c_allocationhdr.(reversal_id)` → `c_allocationhdr.(c_allocationhdr_id)` | Allocation |

<a id="t-c_allocationline"></a>
## `c_allocationline` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Allocation Line`
- 사전 Description: Allocation Line
- 근거 문장: 사전 Name='Allocation Line'; Description='Allocation Line'; 주요 열 c_payment_id, c_cashline_id, c_allocationhdr_id, c_banktransfer_id; FK cpaymtallocate_callocationline, callocation_callocationline; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_payment_id` | Payment | `numeric(10,0)` |
| `c_cashline_id` | Cash Journal Line | `numeric(10,0)` |
| `c_allocationhdr_id` | Allocation | `numeric(10,0)` |
| `c_banktransfer_id` | Bank Transfer | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cpaymtallocate_callocationline` | `c_paymentallocate.(c_allocationline_id)` → `c_allocationline.(c_allocationline_id)` | Allocate Payment |
| outgoing | `callocation_callocationline` | `c_allocationline.(c_allocationhdr_id)` → `c_allocationhdr.(c_allocationhdr_id)` | Allocation |
| outgoing | `cbanktransfer_callocationline` | `c_allocationline.(c_banktransfer_id)` → `c_banktransfer.(c_banktransfer_id)` | Bank Transfer |
| outgoing | `ccashline_callocationline` | `c_allocationline.(c_cashline_id)` → `c_cashline.(c_cashline_id)` | Cash Journal Line |

<a id="t-c_bank"></a>
## `c_bank` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bank`
- 사전 Description: Bank
- 근거 문장: 사전 Name='Bank'; Description='Bank'; 주요 열 routingno; FK cbank_cbankaccount, cbank_cbpbankaccount; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `routingno` | Routing No | `character varying(20)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cbank_cbankaccount` | `c_bankaccount.(c_bank_id)` → `c_bank.(c_bank_id)` | Bank Account |
| incoming | `cbank_cbpbankaccount` | `c_bp_bankaccount.(c_bank_id)` → `c_bank.(c_bank_id)` | Partner Bank Account |

<a id="t-c_bankaccount"></a>
## `c_bankaccount` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bank Account`
- 사전 Description: Account at the Bank
- 근거 문장: 사전 Name='Bank Account'; Description='Account at the Bank'; 주요 열 c_bank_id, accountno, iban, paymentexportclass; FK cbankaccount_cbadoc, cbankaccount_cbankaccountproce; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bank_id` | Bank | `numeric(10,0)` |
| `accountno` | Account No | `character varying(20)` |
| `iban` | IBAN | `character varying(40)` |
| `paymentexportclass` | Payment Export Class | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cbankaccount_cbadoc` | `c_bankaccountdoc.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account Document |
| incoming | `cbankaccount_cbankaccountproce` | `c_bankaccount_processor.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account Processor |
| incoming | `cbankaccount_cbankacctacct` | `c_bankaccount_acct.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | C_BankAccount_Acct |
| incoming | `cbankaccount_cbankstatement` | `c_bankstatement.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Statement |

<a id="t-c_bankaccount_acct"></a>
## `c_bankaccount_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_BankAccount_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_BankAccount_Acct'; 주요 열 b_intransit_acct, b_asset_acct, b_expense_acct, b_interestrev_acct; FK cacctschema_cbankaccountacct, vc_basset_cbankaccount; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `b_intransit_acct` | Bank In Transit | `numeric(10,0)` |
| `b_asset_acct` | Bank Asset | `numeric(10,0)` |
| `b_expense_acct` | Bank Expense | `numeric(10,0)` |
| `b_interestrev_acct` | Bank Interest Revenue | `numeric(10,0)` |
| `b_interestexp_acct` | Bank Interest Expense | `numeric(10,0)` |
| `b_unidentified_acct` | Bank Unidentified Receipts | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_cbankaccountacct` | `c_bankaccount_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `vc_basset_cbankaccount` | `c_bankaccount_acct.(b_asset_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_bexpense_cbankaccount` | `c_bankaccount_acct.(b_expense_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_binterestexp_cbankaccount` | `c_bankaccount_acct.(b_interestexp_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_bankaccount_processor"></a>
## `c_bankaccount_processor` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bank Account Processor`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Bank Account Processor'; 주요 열 근거 부족; FK cbankaccount_cbankaccountproce, cpaymentprocessor_cbankaccount; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cbankaccount_cbankaccountproce` | `c_bankaccount_processor.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |
| outgoing | `cpaymentprocessor_cbankaccount` | `c_bankaccount_processor.(c_paymentprocessor_id)` → `c_paymentprocessor.(c_paymentprocessor_id)` | Payment Processor |

<a id="t-c_bankaccountdoc"></a>
## `c_bankaccountdoc` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bank Account Document`
- 사전 Description: Checks, Transfers, etc.
- 근거 문장: 사전 Name='Bank Account Document'; Description='Checks, Transfers, etc.'; 주요 열 c_bankaccount_id, paymentrule; FK cbankaccount_cbadoc; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bankaccount_id` | Bank Account | `numeric(10,0)` |
| `paymentrule` | Payment Rule | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cbankaccount_cbadoc` | `c_bankaccountdoc.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |

<a id="t-c_bankstatement"></a>
## `c_bankstatement` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bank Statement`
- 사전 Description: Bank Statement of account
- 근거 문장: 사전 Name='Bank Statement'; Description='Bank Statement of account'; 주요 열 c_bankaccount_id, statementdate, statementdifference, eftstatementreference; FK cbankstatement_ibankstatement, cbstatement_cbstatementline; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bankaccount_id` | Bank Account | `numeric(10,0)` |
| `statementdate` | Statement date | `timestamp without time zone` |
| `statementdifference` | Statement difference | `numeric` |
| `eftstatementreference` | EFT Statement Reference | `character varying(60)` |
| `eftstatementdate` | EFT Statement Date | `timestamp without time zone` |
| `matchstatement` | Match Statement | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cbankstatement_ibankstatement` | `i_bankstatement.(c_bankstatement_id)` → `c_bankstatement.(c_bankstatement_id)` | Import Bank Statement |
| incoming | `cbstatement_cbstatementline` | `c_bankstatementline.(c_bankstatement_id)` → `c_bankstatement.(c_bankstatement_id)` | Bank statement line |
| outgoing | `cbankaccount_cbankstatement` | `c_bankstatement.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |

<a id="t-c_bankstatementline"></a>
## `c_bankstatementline` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bank statement line`
- 사전 Description: Line on a statement from this Bank
- 근거 문장: 사전 Name='Bank statement line'; Description='Line on a statement from this Bank'; 주요 열 c_bankstatement_id, c_payment_id, createpayment, statementlinedate; FK cbankstmtline_ibankstmt, cbstatement_cbstatementline; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bankstatement_id` | Bank Statement | `numeric(10,0)` |
| `c_payment_id` | Payment | `numeric(10,0)` |
| `createpayment` | Create Payment | `character(1)` |
| `statementlinedate` | Statement Line Date | `timestamp without time zone` |
| `eftstatementlinedate` | EFT Statement Line Date | `timestamp without time zone` |
| `matchstatement` | Match Statement | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cbankstmtline_ibankstmt` | `i_bankstatement.(c_bankstatementline_id)` → `c_bankstatementline.(c_bankstatementline_id)` | Import Bank Statement |
| outgoing | `cbstatement_cbstatementline` | `c_bankstatementline.(c_bankstatement_id)` → `c_bankstatement.(c_bankstatement_id)` | Bank Statement |
| outgoing | `cpayment_cbankstmtline` | `c_bankstatementline.(c_payment_id)` → `c_payment.(c_payment_id)` | Payment |

<a id="t-c_bankstatementloader"></a>
## `c_bankstatementloader` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bank Statement Loader`
- 사전 Description: Definition of Bank Statement Loader (SWIFT, OFX)
- 근거 문장: 사전 Name='Bank Statement Loader'; Description='Definition of Bank Statement Loader (SWIFT, OFX)'; 주요 열 c_bankaccount_id, accountno; FK cbankacct_cbankstmtloader; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bankaccount_id` | Bank Account | `numeric(10,0)` |
| `accountno` | Account No | `character varying(20)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cbankacct_cbankstmtloader` | `c_bankstatementloader.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |

<a id="t-c_bankstatementmatcher"></a>
## `c_bankstatementmatcher` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bank Statement Matcher`
- 사전 Description: Algorithm to match Bank Statement Info to Business Partners, Invoices and Payments
- 근거 문장: 사전 Name='Bank Statement Matcher'; Description='Algorithm to match Bank Statement Info to Business Partners, Invoices and Payments'; 주요 열 classname, seqno; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `classname` | Classname | `character varying(255)` |
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_banktransfer"></a>
## `c_banktransfer` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bank Transfer`
- 사전 Description: Bank Transfer
- 근거 문장: 사전 Name='Bank Transfer'; Description='Bank Transfer'; 주요 열 from_c_bankaccount_id, to_c_bankaccount_id, from_tendertype, to_tendertype; FK cbanktransfer_callocationline, cbanktransfer_cpayment; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `from_c_bankaccount_id` | From Bank Account | `numeric(10,0)` |
| `to_c_bankaccount_id` | To Bank Account | `numeric(10,0)` |
| `from_tendertype` | From Tender Type | `character(1)` |
| `to_tendertype` | To Tender Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cbanktransfer_callocationline` | `c_allocationline.(c_banktransfer_id)` → `c_banktransfer.(c_banktransfer_id)` | Allocation Line |
| incoming | `cbanktransfer_cpayment` | `c_payment.(c_banktransfer_id)` → `c_banktransfer.(c_banktransfer_id)` | Payment |
| outgoing | `fromcbankaccount_cbanktransfer` | `c_banktransfer.(from_c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |
| outgoing | `tocbankaccount_cbanktransfer` | `c_banktransfer.(to_c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |

<a id="t-c_bp_bankaccount"></a>
## `c_bp_bankaccount` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Partner Bank Account`
- 사전 Description: Bank Account of the Business Partner
- 근거 문장: 사전 Name='Partner Bank Account'; Description='Bank Account of the Business Partner'; 주요 열 c_bank_id, routingno, accountno, creditcardtype; FK cbpbankaccount_cpaymenttransac, cbpbankaccount_cpayselectionch; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bank_id` | Bank | `numeric(10,0)` |
| `routingno` | Routing No | `character varying(20)` |
| `accountno` | Account No | `character varying(20)` |
| `creditcardtype` | Credit Card | `character(1)` |
| `creditcardnumber` | Number | `character varying(20)` |
| `creditcardvv` | Verification Code | `character varying(4)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cbpbankaccount_cpaymenttransac` | `c_paymenttransaction.(c_bp_bankaccount_id)` → `c_bp_bankaccount.(c_bp_bankaccount_id)` | Payment Transaction |
| incoming | `cbpbankaccount_cpayselectionch` | `c_payselectioncheck.(c_bp_bankaccount_id)` → `c_bp_bankaccount.(c_bp_bankaccount_id)` | Pay Selection Check |
| incoming | `cbpbankacct_cpayment` | `c_payment.(c_bp_bankaccount_id)` → `c_bp_bankaccount.(c_bp_bankaccount_id)` | Payment |
| outgoing | `cbank_cbpbankaccount` | `c_bp_bankaccount.(c_bank_id)` → `c_bank.(c_bank_id)` | Bank |

<a id="t-c_bp_customer_acct"></a>
## `c_bp_customer_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_BP_Customer_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_BP_Customer_Acct'; 주요 열 c_receivable_acct, c_prepayment_acct, c_receivable_services_acct; FK cacctschema_cbpcustomeracct, creceivableservices_cbpcustome; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_receivable_acct` | Customer Receivables | `numeric(10,0)` |
| `c_prepayment_acct` | Customer Prepayment | `numeric(10,0)` |
| `c_receivable_services_acct` | Receivable Services | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_cbpcustomeracct` | `c_bp_customer_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `creceivableservices_cbpcustome` | `c_bp_customer_acct.(c_receivable_services_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_cprepayment_cbpcustomer` | `c_bp_customer_acct.(c_prepayment_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_creceivable_cbpcustomer` | `c_bp_customer_acct.(c_receivable_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_bp_edi"></a>
## `c_bp_edi` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `EDI Definition`
- 사전 Description: Electronic Data Interchange
- 근거 문장: 사전 Name='EDI Definition'; Description='Electronic Data Interchange'; 주요 열 editype; FK cbpedi_medi; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `editype` | EDI Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cbpedi_medi` | `m_edi.(c_bp_edi_id)` → `c_bp_edi.(c_bp_edi_id)` | EDI Transaction |

<a id="t-c_bp_employee_acct"></a>
## `c_bp_employee_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_BP_Employee_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_BP_Employee_Acct'; 주요 열 e_expense_acct, e_prepayment_acct; FK cacctschema_cbpemployeeacct, vc_eexpense_cbpemployee; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `e_expense_acct` | Employee Expense | `numeric(10,0)` |
| `e_prepayment_acct` | Employee Prepayment | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_cbpemployeeacct` | `c_bp_employee_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `vc_eexpense_cbpemployee` | `c_bp_employee_acct.(e_expense_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_eprepayment_cbpemployee` | `c_bp_employee_acct.(e_prepayment_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_bp_group"></a>
## `c_bp_group` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Business Partner Group`
- 사전 Description: Business Partner Group
- 근거 문장: 사전 Name='Business Partner Group'; Description='Business Partner Group'; 주요 열 근거 부족; FK cbpgroup_cbpartner, cbpgroup_cbpgroupacct; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cbpgroup_cbpartner` | `c_bpartner.(c_bp_group_id)` → `c_bp_group.(c_bp_group_id)` | Business Partner |
| incoming | `cbpgroup_cbpgroupacct` | `c_bp_group_acct.(c_bp_group_id)` → `c_bp_group.(c_bp_group_id)` | Business Partner Group Acct |
| incoming | `cbpgroup_ibpartner` | `i_bpartner.(c_bp_group_id)` → `c_bp_group.(c_bp_group_id)` | Import Business Partner |

<a id="t-c_bp_group_acct"></a>
## `c_bp_group_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Business Partner Group Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Business Partner Group Acct'; 주요 열 c_receivable_acct, c_prepayment_acct, v_liability_acct, v_liability_services_acct; FK cacctschema_cbpgroupacct, creceivableservices_cbpgroupac; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_receivable_acct` | Customer Receivables | `numeric(10,0)` |
| `c_prepayment_acct` | Customer Prepayment | `numeric(10,0)` |
| `v_liability_acct` | Vendor Liability | `numeric(10,0)` |
| `v_liability_services_acct` | Vendor Service Liability | `numeric(10,0)` |
| `v_prepayment_acct` | Vendor Prepayment | `numeric(10,0)` |
| `paydiscount_exp_acct` | Payment Discount Expense | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_cbpgroupacct` | `c_bp_group_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `creceivableservices_cbpgroupac` | `c_bp_group_acct.(c_receivable_services_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_cprepayment_cbpgroup` | `c_bp_group_acct.(c_prepayment_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_creceivable_cbpgroup` | `c_bp_group_acct.(c_receivable_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_bp_relation"></a>
## `c_bp_relation` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Partner Relation`
- 사전 Description: Business Partner Relation
- 근거 문장: 사전 Name='Partner Relation'; Description='Business Partner Relation'; 주요 열 c_bpartner_id, c_bpartner_location_id, c_bpartnerrelation_id, c_bpartnerrelation_location_id; FK cbpartner_cbprelation, cbpartner_cbprelationbp; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `c_bpartner_location_id` | Partner Location | `numeric(10,0)` |
| `c_bpartnerrelation_id` | Related Partner | `numeric(10,0)` |
| `c_bpartnerrelation_location_id` | Related Partner Location | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cbpartner_cbprelation` | `c_bp_relation.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `cbpartner_cbprelationbp` | `c_bp_relation.(c_bpartnerrelation_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `cbplocation_cbprelation` | `c_bp_relation.(c_bpartner_location_id)` → `c_bpartner_location.(c_bpartner_location_id)` | Partner Location |
| outgoing | `cbplocation_cbprelationbp` | `c_bp_relation.(c_bpartnerrelation_location_id)` → `c_bpartner_location.(c_bpartner_location_id)` | Partner Location |

<a id="t-c_bp_shippingacct"></a>
## `c_bp_shippingacct` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Business Partner Shipping Account`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Business Partner Shipping Account'; 주요 열 c_bpartner_id, c_bpartner_location_id; FK cbpartner_cbpshippingacct, cbpartnerlocation_cbpshippinga; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `c_bpartner_location_id` | Partner Location | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cbpartner_cbpshippingacct` | `c_bp_shippingacct.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `cbpartnerlocation_cbpshippinga` | `c_bp_shippingacct.(c_bpartner_location_id)` → `c_bpartner_location.(c_bpartner_location_id)` | Partner Location |

<a id="t-c_bp_vendor_acct"></a>
## `c_bp_vendor_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_BP_Vendor_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_BP_Vendor_Acct'; 주요 열 v_liability_acct, v_liability_services_acct, v_prepayment_acct; FK cacctschema_cbpvendoracct, vc_vliability_cbpvendor; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `v_liability_acct` | Vendor Liability | `numeric(10,0)` |
| `v_liability_services_acct` | Vendor Service Liability | `numeric(10,0)` |
| `v_prepayment_acct` | Vendor Prepayment | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_cbpvendoracct` | `c_bp_vendor_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `vc_vliability_cbpvendor` | `c_bp_vendor_acct.(v_liability_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_vliabilityservices_cbpvendo` | `c_bp_vendor_acct.(v_liability_services_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_vprepayment_cbpvendor` | `c_bp_vendor_acct.(v_prepayment_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_bp_withholding"></a>
## `c_bp_withholding` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_BP_Withholding`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_BP_Withholding'; 주요 열 ismandatorywithholding; FK cwithholding_cbpwithholding; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ismandatorywithholding` | Mandatory Withholding | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cwithholding_cbpwithholding` | `c_bp_withholding.(c_withholding_id)` → `c_withholding.(c_withholding_id)` | Withholding |

<a id="t-c_bpartner"></a>
## `c_bpartner` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Business Partner`
- 사전 Description: Identifies a Business Partner
- 근거 문장: 사전 Name='Business Partner'; Description='Identifies a Business Partner'; 주요 열 c_bp_group_id, isvendor, iscustomer, issalesrep; FK c_bpartner_rrequest, c_buspartner_c_bp_vendor_acct; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bp_group_id` | Business Partner Group | `numeric(10,0)` |
| `isvendor` | Vendor | `character(1)` |
| `iscustomer` | Customer | `character(1)` |
| `issalesrep` | Sales Representative | `character(1)` |
| `salesrep_id` | Sales Representative | `numeric(10,0)` |
| `sendemail` | Send EMail | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_bpartner_rrequest` | `r_request.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Request |
| incoming | `c_buspartner_c_bp_vendor_acct` | `c_bp_vendor_acct.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | C_BP_Vendor_Acct |
| incoming | `cbpartner_aduser` | `ad_user.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | User/Contact |
| incoming | `cbpartner_cbpbankaccount` | `c_bp_bankaccount.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Partner Bank Account |

<a id="t-c_bpartner_location"></a>
## `c_bpartner_location` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Partner Location`
- 사전 Description: Identifies the (ship to) address for this Business Partner
- 근거 문장: 사전 Name='Partner Location'; Description='Identifies the (ship to) address for this Business Partner'; 주요 열 phone, phone2, c_salesregion_id, c_bpartner_id; FK cbpartnerloc_mdistlistline, cbpartnerlocation_cbpshippinga; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `phone` | Phone | `character varying(40)` |
| `phone2` | 2nd Phone | `character varying(40)` |
| `c_salesregion_id` | Sales Region | `numeric(10,0)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `c_location_id` | Address | `numeric(10,0)` |
| `customeraddressid` | Customer Address ID | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cbpartnerloc_mdistlistline` | `m_distributionlistline.(c_bpartner_location_id)` → `c_bpartner_location.(c_bpartner_location_id)` | Distribution List Line |
| incoming | `cbpartnerlocation_cbpshippinga` | `c_bp_shippingacct.(c_bpartner_location_id)` → `c_bpartner_location.(c_bpartner_location_id)` | Business Partner Shipping Account |
| incoming | `cbpartnerlocation_ibpartner` | `i_bpartner.(c_bpartner_location_id)` → `c_bpartner_location.(c_bpartner_location_id)` | Import Business Partner |
| incoming | `cbplocation_aduser` | `ad_user.(c_bpartner_location_id)` → `c_bpartner_location.(c_bpartner_location_id)` | User/Contact |

<a id="t-c_bpartner_product"></a>
## `c_bpartner_product` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Business Partner`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Product Business Partner'; 주요 열 shelflifeminpct, shelflifemindays, qualityrating, vendorproductno; FK cbpartner_cbpproduct, mproduct_cbpproduct; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `shelflifeminpct` | Min Shelf Life % | `numeric(10,0)` |
| `shelflifemindays` | Min Shelf Life Days | `numeric(10,0)` |
| `qualityrating` | Quality Rating | `numeric` |
| `vendorproductno` | Partner Product Key | `character varying(30)` |
| `vendorcategory` | Partner Category | `character varying(30)` |
| `manufacturer` | Manufacturer | `character varying(30)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cbpartner_cbpproduct` | `c_bpartner_product.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `mproduct_cbpproduct` | `c_bpartner_product.(m_product_id)` → `m_product.(m_product_id)` | Product |

검토 후보: 거래처·연락처·주소 (규칙 점수 9); 상품·속성·가격·단위 (규칙 점수 9).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_calendar"></a>
## `c_calendar` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Calendar`
- 사전 Description: Accounting Calendar Name
- 근거 문장: 사전 Name='Calendar'; Description='Accounting Calendar Name'; 주요 열 근거 부족; FK c_calendar_year, ccalendar_adorginfo; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_calendar_year` | `c_year.(c_calendar_id)` → `c_calendar.(c_calendar_id)` | Year |
| incoming | `ccalendar_adorginfo` | `ad_orginfo.(c_calendar_id)` → `c_calendar.(c_calendar_id)` | Organization Info |

<a id="t-c_campaign"></a>
## `c_campaign` — 프로모션·마케팅

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Campaign`
- 사전 Description: Marketing Campaign
- 근거 문장: 사전 Name='Campaign'; Description='Marketing Campaign'; 주요 열 c_channel_id, startdate, enddate; FK ccampaign_ccampaigntrl, ccampaign_mpromotion; 사전 의미와 열/FK가 프로모션·마케팅를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `campaign`를 근거로, 구조 근거가 있는 `promotion` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_channel_id` | Channel | `numeric(10,0)` |
| `startdate` | Start Date | `timestamp without time zone` |
| `enddate` | End Date | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccampaign_ccampaigntrl` | `c_campaign_trl.(c_campaign_id)` → `c_campaign.(c_campaign_id)` | Campaign Trl |
| incoming | `ccampaign_mpromotion` | `m_promotion.(c_campaign_id)` → `c_campaign.(c_campaign_id)` | Promotion |
| outgoing | `cchannel_ccampaign` | `c_campaign.(c_channel_id)` → `c_channel.(c_channel_id)` | Channel |

<a id="t-c_campaign_trl"></a>
## `c_campaign_trl` — 프로모션·마케팅

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Campaign Trl`
- 사전 Description: Marketing Campaign
- 근거 문장: 사전 Name='Campaign Trl'; Description='Marketing Campaign'; 주요 열 근거 부족; FK ccampaign_ccampaigntrl; 사전 의미와 열/FK가 프로모션·마케팅를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `campaign`를 근거로, 구조 근거가 있는 `promotion` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccampaign_ccampaigntrl` | `c_campaign_trl.(c_campaign_id)` → `c_campaign.(c_campaign_id)` | Campaign |

<a id="t-c_cash"></a>
## `c_cash` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cash Journal`
- 사전 Description: Cash Journal
- 근거 문장: 사전 Name='Cash Journal'; Description='Cash Journal'; 주요 열 c_cashbook_id, statementdate, statementdifference; FK ccash_ccashline, ccashbook_ccash; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_cashbook_id` | Cash Book | `numeric(10,0)` |
| `statementdate` | Statement date | `timestamp without time zone` |
| `statementdifference` | Statement difference | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccash_ccashline` | `c_cashline.(c_cash_id)` → `c_cash.(c_cash_id)` | Cash Journal Line |
| outgoing | `ccashbook_ccash` | `c_cash.(c_cashbook_id)` → `c_cashbook.(c_cashbook_id)` | Cash Book |

<a id="t-c_cashbook"></a>
## `c_cashbook` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cash Book`
- 사전 Description: Cash Book for recording petty cash transactions
- 근거 문장: 사전 Name='Cash Book'; Description='Cash Book for recording petty cash transactions'; 주요 열 근거 부족; FK c_payment__c_cashbo_c_cashbook, ccashbook_ccash; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_payment__c_cashbo_c_cashbook` | `c_payment.(c_cashbook_id)` → `c_cashbook.(c_cashbook_id)` | Payment |
| incoming | `ccashbook_ccash` | `c_cash.(c_cashbook_id)` → `c_cashbook.(c_cashbook_id)` | Cash Journal |
| incoming | `ccashbook_ccashbookacct` | `c_cashbook_acct.(c_cashbook_id)` → `c_cashbook.(c_cashbook_id)` | C_CashBook_Acct |
| incoming | `ccashbook_cpaymenttransaction` | `c_paymenttransaction.(c_cashbook_id)` → `c_cashbook.(c_cashbook_id)` | Payment Transaction |

<a id="t-c_cashbook_acct"></a>
## `c_cashbook_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_CashBook_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_CashBook_Acct'; 주요 열 cb_asset_acct, cb_cashtransfer_acct, cb_differences_acct, cb_expense_acct; FK cacctschema_ccashbookacct, vc_cbasset_ccashbook; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cb_asset_acct` | Cash Book Asset | `numeric(10,0)` |
| `cb_cashtransfer_acct` | Cash Transfer | `numeric(10,0)` |
| `cb_differences_acct` | Cash Book Differences | `numeric(10,0)` |
| `cb_expense_acct` | Cash Book Expense | `numeric(10,0)` |
| `cb_receipt_acct` | Cash Book Receipt | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_ccashbookacct` | `c_cashbook_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `vc_cbasset_ccashbook` | `c_cashbook_acct.(cb_asset_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_cbcashtransfer_ccashbook` | `c_cashbook_acct.(cb_cashtransfer_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_cbdifferences_ccashbook` | `c_cashbook_acct.(cb_differences_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_cashline"></a>
## `c_cashline` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cash Journal Line`
- 사전 Description: Cash Journal Line
- 근거 문장: 사전 Name='Cash Journal Line'; Description='Cash Journal Line'; 주요 열 c_cash_id, c_bankaccount_id, c_payment_id; FK ccashline_callocationline, cbankacct_ccashline; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_cash_id` | Cash Journal | `numeric(10,0)` |
| `c_bankaccount_id` | Bank Account | `numeric(10,0)` |
| `c_payment_id` | Payment | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccashline_callocationline` | `c_allocationline.(c_cashline_id)` → `c_cashline.(c_cashline_id)` | Allocation Line |
| outgoing | `cbankacct_ccashline` | `c_cashline.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |
| outgoing | `ccash_ccashline` | `c_cashline.(c_cash_id)` → `c_cash.(c_cash_id)` | Cash Journal |
| outgoing | `cpayment_ccashline` | `c_cashline.(c_payment_id)` → `c_payment.(c_payment_id)` | Payment |

<a id="t-c_cashplan"></a>
## `c_cashplan` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cash Plan`
- 사전 Description: Cash Plan
- 근거 문장: 사전 Name='Cash Plan'; Description='Cash Plan'; 주요 열 근거 부족; FK ccashplan_ccashplanline; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccashplan_ccashplanline` | `c_cashplanline.(c_cashplan_id)` → `c_cashplan.(c_cashplan_id)` | Cash Plan Line |

<a id="t-c_cashplanline"></a>
## `c_cashplanline` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cash Plan Line`
- 사전 Description: Cash Plan Line
- 근거 문장: 사전 Name='Cash Plan Line'; Description='Cash Plan Line'; 주요 열 c_cashplan_id; FK ccashplan_ccashplanline; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_cashplan_id` | Cash Plan | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccashplan_ccashplanline` | `c_cashplanline.(c_cashplan_id)` → `c_cashplan.(c_cashplan_id)` | Cash Plan |

<a id="t-c_channel"></a>
## `c_channel` — 프로모션·마케팅

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Channel`
- 사전 Description: Sales Channel
- 근거 문장: 사전 Name='Channel'; Description='Sales Channel'; 주요 열 근거 부족; FK cchannel_ccampaign; 사전 의미와 열/FK가 프로모션·마케팅를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cchannel_ccampaign` | `c_campaign.(c_channel_id)` → `c_channel.(c_channel_id)` | Campaign |

<a id="t-c_charge"></a>
## `c_charge` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Charge`
- 사전 Description: Additional document charges
- 근거 문장: 사전 Name='Charge'; Description='Additional document charges'; 주요 열 chargeamt, issametax, issamecurrency, c_taxcategory_id; FK ccharge_aassetaddition, cchargefreight_adclientinfo; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `chargeamt` | Charge amount | `numeric` |
| `issametax` | Same Tax | `character(1)` |
| `issamecurrency` | Same Currency | `character(1)` |
| `c_taxcategory_id` | Tax Category | `numeric(10,0)` |
| `istaxincluded` | Price includes Tax | `character(1)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccharge_aassetaddition` | `a_asset_addition.(c_charge_id)` → `c_charge.(c_charge_id)` | Asset Addition |
| incoming | `cchargefreight_adclientinfo` | `ad_clientinfo.(c_chargefreight_id)` → `c_charge.(c_charge_id)` | AD_ClientInfo |
| incoming | `ccharge_cacctschemaelement` | `c_acctschema_element.(c_charge_id)` → `c_charge.(c_charge_id)` | Acct.Schema Element |
| incoming | `ccharge_callocationline` | `c_allocationline.(c_charge_id)` → `c_charge.(c_charge_id)` | Allocation Line |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_charge_acct"></a>
## `c_charge_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_Charge_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_Charge_Acct'; 주요 열 ch_expense_acct, ch_revenue_acct; FK cacctschema_cchargeacct, chrevenue_cchargeacct; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ch_expense_acct` | Charge Account | `numeric(10,0)` |
| `ch_revenue_acct` | Charge Revenue (Deprecated) | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_cchargeacct` | `c_charge_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `chrevenue_cchargeacct` | `c_charge_acct.(ch_revenue_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_chexpense_ccharge` | `c_charge_acct.(ch_expense_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_charge_trl"></a>
## `c_charge_trl` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Charge Trl`
- 사전 Description: Additional document charges
- 근거 문장: 사전 Name='Charge Trl'; Description='Additional document charges'; 주요 열 istranslated; FK adlangu_cchargetrl, ccharge_cchargetrl; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istranslated` | Translated | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlangu_cchargetrl` | `c_charge_trl.(ad_language)` → `ad_language.(ad_language)` | Language ID |
| outgoing | `ccharge_cchargetrl` | `c_charge_trl.(c_charge_id)` → `c_charge.(c_charge_id)` | Charge |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_chargetype"></a>
## `c_chargetype` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Charge Type`
- 사전 Description: Charge Type
- 근거 문장: 사전 Name='Charge Type'; Description='Charge Type'; 주요 열 근거 부족; FK cchargetype_ccharge, cchargetype_cchargetypedoctype; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cchargetype_ccharge` | `c_charge.(c_chargetype_id)` → `c_chargetype.(c_chargetype_id)` | Charge |
| incoming | `cchargetype_cchargetypedoctype` | `c_chargetype_doctype.(c_chargetype_id)` → `c_chargetype.(c_chargetype_id)` | Charge Type by Doc Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_chargetype_doctype"></a>
## `c_chargetype_doctype` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Charge Type by Doc Type`
- 사전 Description: Configuration table for charges to be used by document type
- 근거 문장: 사전 Name='Charge Type by Doc Type'; Description='Configuration table for charges to be used by document type'; 주요 열 근거 부족; FK cdoctype_cchargetypedoctype; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cdoctype_cchargetypedoctype` | `c_chargetype_doctype.(c_doctype_id)` → `c_doctype.(c_doctype_id)` | Document Type |

<a id="t-c_city"></a>
## `c_city` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `City`
- 사전 Description: City
- 근거 문장: 사전 Name='City'; Description='City'; 주요 열 c_country_id, c_region_id; FK ccountry_ccity, cregion_ccity; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_country_id` | Country | `numeric(10,0)` |
| `c_region_id` | Region | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccountry_ccity` | `c_city.(c_country_id)` → `c_country.(c_country_id)` | Country |
| outgoing | `cregion_ccity` | `c_city.(c_region_id)` → `c_region.(c_region_id)` | Region |

<a id="t-c_commission"></a>
## `c_commission` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Commission`
- 사전 Description: Commission
- 근거 문장: 사전 Name='Commission'; Description='Commission'; 주요 열 c_bpartner_id, c_currency_id, frequencytype, docbasistype; FK cbpartner_ccommission, ccharge_ccommission; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `c_currency_id` | Currency | `numeric(10,0)` |
| `frequencytype` | Frequency Type | `character(1)` |
| `docbasistype` | Calculation Basis | `character(1)` |
| `listdetails` | List Details | `character(1)` |
| `datelastrun` | Date Last Run | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cbpartner_ccommission` | `c_commission.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `ccharge_ccommission` | `c_commission.(c_charge_id)` → `c_charge.(c_charge_id)` | Charge |
| outgoing | `ccurrency_ccommission` | `c_commission.(c_currency_id)` → `c_currency.(c_currency_id)` | Currency |
| outgoing | `mproduct_ccommission` | `c_commission.(m_product_id)` → `m_product.(m_product_id)` | Product |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_commissionamt"></a>
## `c_commissionamt` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Commission Amount`
- 사전 Description: Generated Commission Amount 
- 근거 문장: 사전 Name='Commission Amount'; Description='Generated Commission Amount '; 주요 열 c_commissionrun_id, c_commissionline_id, convertedamt, actualqty; FK ccomline_ccomamt, ccommentrun_ccommissionamt; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_commissionrun_id` | Commission Run | `numeric(10,0)` |
| `c_commissionline_id` | Commission Line | `numeric(10,0)` |
| `convertedamt` | Converted Amount | `numeric` |
| `actualqty` | Actual Quantity | `numeric` |
| `commissionamt` | Commission Amount | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccomline_ccomamt` | `c_commissionamt.(c_commissionline_id)` → `c_commissionline.(c_commissionline_id)` | Commission Line |
| outgoing | `ccommentrun_ccommissionamt` | `c_commissionamt.(c_commissionrun_id)` → `c_commissionrun.(c_commissionrun_id)` | Commission Run |
| incoming | `ccommissionamt_ccomdetail` | `c_commissiondetail.(c_commissionamt_id)` → `c_commissionamt.(c_commissionamt_id)` | Commission Detail |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_commissiondetail"></a>
## `c_commissiondetail` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Commission Detail`
- 사전 Description: Supporting information for Commission Amounts
- 근거 문장: 사전 Name='Commission Detail'; Description='Supporting information for Commission Amounts'; 주요 열 c_commissionamt_id, reference, c_orderline_id, c_invoiceline_id; FK ccommissionamt_ccomdetail, ccurrency_ccommissiondetail; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_commissionamt_id` | Commission Amount | `numeric(10,0)` |
| `reference` | Reference | `character varying(60)` |
| `c_orderline_id` | Sales Order Line | `numeric(10,0)` |
| `c_invoiceline_id` | Invoice Line | `numeric(10,0)` |
| `info` | Info | `character varying(60)` |
| `c_currency_id` | Currency | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccommissionamt_ccomdetail` | `c_commissiondetail.(c_commissionamt_id)` → `c_commissionamt.(c_commissionamt_id)` | Commission Amount |
| outgoing | `ccurrency_ccommissiondetail` | `c_commissiondetail.(c_currency_id)` → `c_currency.(c_currency_id)` | Currency |
| outgoing | `cinvoiceline_ccommissiondet` | `c_commissiondetail.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` | Invoice Line |
| outgoing | `corderline_ccommissiondetail` | `c_commissiondetail.(c_orderline_id)` → `c_orderline.(c_orderline_id)` | Sales Order Line |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_commissionline"></a>
## `c_commissionline` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Commission Line`
- 사전 Description: Commission Line
- 근거 문장: 사전 Name='Commission Line'; Description='Commission Line'; 주요 열 c_commission_id, line, amtsubtract, amtmultiplier; FK ccomline_ccomamt, adorgtrx_ccommissionline; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_commission_id` | Commission | `numeric(10,0)` |
| `line` | Line No | `numeric(10,0)` |
| `amtsubtract` | Subtract Amount | `numeric` |
| `amtmultiplier` | Multiplier Amount | `numeric` |
| `qtysubtract` | Subtract Quantity | `numeric` |
| `qtymultiplier` | Multiplier Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccomline_ccomamt` | `c_commissionamt.(c_commissionline_id)` → `c_commissionline.(c_commissionline_id)` | Commission Amount |
| outgoing | `adorgtrx_ccommissionline` | `c_commissionline.(org_id)` → `ad_org.(ad_org_id)` | Organization |
| outgoing | `cbpartner_ccommissionline` | `c_commissionline.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `cbpgroup_commissionline` | `c_commissionline.(c_bp_group_id)` → `c_bp_group.(c_bp_group_id)` | Business Partner Group |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_commissionrun"></a>
## `c_commissionrun` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Commission Run`
- 사전 Description: Commission Run or Process
- 근거 문장: 사전 Name='Commission Run'; Description='Commission Run or Process'; 주요 열 processing; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-c_contactactivity"></a>
## `c_contactactivity` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Contact Activity`
- 사전 Description: Events, tasks, communications related to a contact
- 근거 문장: 사전 Name='Contact Activity'; Description='Events, tasks, communications related to a contact'; 주요 열 salesrep_id, contactactivitytype; FK aduser_ccontactactivity, salesrep_ccontactactivity; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `salesrep_id` | Sales Representative | `numeric(10,0)` |
| `contactactivitytype` | Activity Type | `character varying(10)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_ccontactactivity` | `c_contactactivity.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `salesrep_ccontactactivity` | `c_contactactivity.(salesrep_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-c_conversion_rate"></a>
## `c_conversion_rate` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Conversion Rate`
- 사전 Description: Rate used for converting currencies
- 근거 문장: 사전 Name='Conversion Rate'; Description='Rate used for converting currencies'; 주요 열 c_currency_id, c_currency_id_to, c_conversiontype_id; FK cconversionrate_iconvrate, c_currencyconvrateto; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_currency_id` | Currency | `numeric(10,0)` |
| `c_currency_id_to` | Currency To | `numeric(10,0)` |
| `c_conversiontype_id` | Currency Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cconversionrate_iconvrate` | `i_conversion_rate.(c_conversion_rate_id)` → `c_conversion_rate.(c_conversion_rate_id)` | Import Conversion Rate |
| outgoing | `c_currencyconvrateto` | `c_conversion_rate.(c_currency_id_to)` → `c_currency.(c_currency_id)` | Currency |
| outgoing | `cconversiontype_cconvrate` | `c_conversion_rate.(c_conversiontype_id)` → `c_conversiontype.(c_conversiontype_id)` | Currency Type |
| outgoing | `ccurrency_cconversionrate` | `c_conversion_rate.(c_currency_id)` → `c_currency.(c_currency_id)` | Currency |

<a id="t-c_conversiontype"></a>
## `c_conversiontype` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Currency Type`
- 사전 Description: Currency Conversion Rate Type
- 근거 문장: 사전 Name='Currency Type'; Description='Currency Conversion Rate Type'; 주요 열 근거 부족; FK cconversiontype_cconvrate, cconvtype_iconvrate; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cconversiontype_cconvrate` | `c_conversion_rate.(c_conversiontype_id)` → `c_conversiontype.(c_conversiontype_id)` | Conversion Rate |
| incoming | `cconvtype_iconvrate` | `i_conversion_rate.(c_conversiontype_id)` → `c_conversiontype.(c_conversiontype_id)` | Import Conversion Rate |

<a id="t-c_costcenter"></a>
## `c_costcenter` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cost Center`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Cost Center'; 주요 열 근거 부족; FK ccostcenter_aassetaddition, ccostcenter_aassetdisposed; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccostcenter_aassetaddition` | `a_asset_addition.(c_costcenter_id)` → `c_costcenter.(c_costcenter_id)` | Asset Addition |
| incoming | `ccostcenter_aassetdisposed` | `a_asset_disposed.(c_costcenter_id)` → `c_costcenter.(c_costcenter_id)` | Asset Disposed |
| incoming | `ccostcenter_aassetreval` | `a_asset_reval.(c_costcenter_id)` → `c_costcenter.(c_costcenter_id)` | Asset Revaluation |
| incoming | `ccostcenter_aassettransfer` | `a_asset_transfer.(c_costcenter_id)` → `c_costcenter.(c_costcenter_id)` | A_Asset_Transfer_ID |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_country"></a>
## `c_country` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Country`
- 사전 Description: Country 
- 근거 문장: 사전 Name='Country'; Description='Country '; 주요 열 countrycode, c_currency_id, isocountrycodealpha3; FK ccountry_ccity, ccountry_ccountrygroupcountry; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `countrycode` | ISO Country Code | `character(2)` |
| `c_currency_id` | Currency | `numeric(10,0)` |
| `isocountrycodealpha3` | ISO Alpha-3 Code | `character varying(3)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccountry_ccity` | `c_city.(c_country_id)` → `c_country.(c_country_id)` | City |
| incoming | `ccountry_ccountrygroupcountry` | `c_countrygroupcountry.(c_country_id)` → `c_country.(c_country_id)` | Country on Country Group |
| incoming | `ccountry_ccountrytrl` | `c_country_trl.(c_country_id)` → `c_country.(c_country_id)` | Country Trl |
| incoming | `ccountry_cregion` | `c_region.(c_country_id)` → `c_country.(c_country_id)` | Region |

<a id="t-c_country_trl"></a>
## `c_country_trl` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Country Trl`
- 사전 Description: Country 
- 근거 문장: 사전 Name='Country Trl'; Description='Country '; 주요 열 근거 부족; FK ccountry_ccountrytrl; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccountry_ccountrytrl` | `c_country_trl.(c_country_id)` → `c_country.(c_country_id)` | Country |

<a id="t-c_countrygroup"></a>
## `c_countrygroup` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Country Group`
- 사전 Description: Group of countries that share common needs like tax agreements
- 근거 문장: 사전 Name='Country Group'; Description='Group of countries that share common needs like tax agreements'; 주요 열 근거 부족; FK ccountrygroup_ccountrygroupcou, ccountrygroup_ccountrygrouptrl; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccountrygroup_ccountrygroupcou` | `c_countrygroupcountry.(c_countrygroup_id)` → `c_countrygroup.(c_countrygroup_id)` | Country on Country Group |
| incoming | `ccountrygroup_ccountrygrouptrl` | `c_countrygroup_trl.(c_countrygroup_id)` → `c_countrygroup.(c_countrygroup_id)` | Country Group Trl |

<a id="t-c_countrygroup_trl"></a>
## `c_countrygroup_trl` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Country Group Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Country Group Trl'; 주요 열 근거 부족; FK ccountrygroup_ccountrygrouptrl; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccountrygroup_ccountrygrouptrl` | `c_countrygroup_trl.(c_countrygroup_id)` → `c_countrygroup.(c_countrygroup_id)` | Country Group |

<a id="t-c_countrygroupcountry"></a>
## `c_countrygroupcountry` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Country on Country Group`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Country on Country Group'; 주요 열 c_countrygroup_id, c_country_id; FK ccountry_ccountrygroupcountry, ccountrygroup_ccountrygroupcou; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_countrygroup_id` | Country Group | `numeric(10,0)` |
| `c_country_id` | Country | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccountry_ccountrygroupcountry` | `c_countrygroupcountry.(c_country_id)` → `c_country.(c_country_id)` | Country |
| outgoing | `ccountrygroup_ccountrygroupcou` | `c_countrygroupcountry.(c_countrygroup_id)` → `c_countrygroup.(c_countrygroup_id)` | Country Group |

<a id="t-c_currency"></a>
## `c_currency` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Currency`
- 사전 Description: The Currency for this record
- 근거 문장: 사전 Name='Currency'; Description='The Currency for this record'; 주요 열 iso_code, cursymbol; FK c_currencyconvrateto, ccurrency_cconversionrate; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `iso_code` | ISO Currency Code | `character(3)` |
| `cursymbol` | Symbol | `character varying(10)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_currencyconvrateto` | `c_conversion_rate.(c_currency_id_to)` → `c_currency.(c_currency_id)` | Conversion Rate |
| incoming | `ccurrency_cconversionrate` | `c_conversion_rate.(c_currency_id)` → `c_currency.(c_currency_id)` | Conversion Rate |
| incoming | `ccurrency_ccountry` | `c_country.(c_currency_id)` → `c_currency.(c_currency_id)` | Country |
| incoming | `ccurrency_ccurrencyacct` | `c_currency_acct.(c_currency_id)` → `c_currency.(c_currency_id)` | C_Currency_Acct |

<a id="t-c_currency_acct"></a>
## `c_currency_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_Currency_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_Currency_Acct'; 주요 열 unrealizedgain_acct, unrealizedloss_acct, realizedgain_acct, realizedloss_acct; FK cacctschema_ccurrencyacct, vc_realizedgain_ccurrency; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `unrealizedgain_acct` | Unrealized Gain Acct | `numeric(10,0)` |
| `unrealizedloss_acct` | Unrealized Loss Acct | `numeric(10,0)` |
| `realizedgain_acct` | Realized Gain Acct | `numeric(10,0)` |
| `realizedloss_acct` | Realized Loss Acct | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_ccurrencyacct` | `c_currency_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `vc_realizedgain_ccurrency` | `c_currency_acct.(realizedgain_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_realizedloss_ccurrency` | `c_currency_acct.(realizedloss_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_unrealizedgain_ccurrency` | `c_currency_acct.(unrealizedgain_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_currency_trl"></a>
## `c_currency_trl` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Currency Trl`
- 사전 Description: The Currency for this record
- 근거 문장: 사전 Name='Currency Trl'; Description='The Currency for this record'; 주요 열 cursymbol; FK ccurrency_ccurrencytrl; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cursymbol` | Symbol | `character varying(10)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccurrency_ccurrencytrl` | `c_currency_trl.(c_currency_id)` → `c_currency.(c_currency_id)` | Currency |

<a id="t-c_cycle"></a>
## `c_cycle` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Project Cycle`
- 사전 Description: Identifier for this Project Reporting Cycle
- 근거 문장: 사전 Name='Project Cycle'; Description='Identifier for this Project Reporting Cycle'; 주요 열 c_currency_id; FK ccurrency_ccycle, ccycle_ccyclestep; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_currency_id` | Currency | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccurrency_ccycle` | `c_cycle.(c_currency_id)` → `c_currency.(c_currency_id)` | Currency |
| incoming | `ccycle_ccyclestep` | `c_cyclestep.(c_cycle_id)` → `c_cycle.(c_cycle_id)` | Cycle Step |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_cyclephase"></a>
## `c_cyclephase` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_CyclePhase`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_CyclePhase'; 주요 열 근거 부족; FK ccyclestep_ccyclephase, cphase_ccyclephase; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccyclestep_ccyclephase` | `c_cyclephase.(c_cyclestep_id)` → `c_cyclestep.(c_cyclestep_id)` | Cycle Step |
| outgoing | `cphase_ccyclephase` | `c_cyclephase.(c_phase_id)` → `c_phase.(c_phase_id)` | Standard Phase |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_cyclestep"></a>
## `c_cyclestep` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cycle Step`
- 사전 Description: The step for this Cycle
- 근거 문장: 사전 Name='Cycle Step'; Description='The step for this Cycle'; 주요 열 c_cycle_id, seqno, relativeweight; FK ccyclestep_ccyclephase, ccycle_ccyclestep; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_cycle_id` | Project Cycle | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `relativeweight` | Relative Weight | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccyclestep_ccyclephase` | `c_cyclephase.(c_cyclestep_id)` → `c_cyclestep.(c_cyclestep_id)` | C_CyclePhase |
| outgoing | `ccycle_ccyclestep` | `c_cyclestep.(c_cycle_id)` → `c_cycle.(c_cycle_id)` | Project Cycle |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_department"></a>
## `c_department` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Department`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Department'; 주요 열 근거 부족; FK cdepartment_aassetaddition, cdepartment_aassetdisposed; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cdepartment_aassetaddition` | `a_asset_addition.(c_department_id)` → `c_department.(c_department_id)` | Asset Addition |
| incoming | `cdepartment_aassetdisposed` | `a_asset_disposed.(c_department_id)` → `c_department.(c_department_id)` | Asset Disposed |
| incoming | `cdepartment_aassetreval` | `a_asset_reval.(c_department_id)` → `c_department.(c_department_id)` | Asset Revaluation |
| incoming | `cdepartment_aassettransfer` | `a_asset_transfer.(c_department_id)` → `c_department.(c_department_id)` | A_Asset_Transfer_ID |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_depositbatch"></a>
## `c_depositbatch` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Deposit Batch`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Deposit Batch'; 주요 열 c_bankaccount_id, c_doctype_id, createfrom, datedeposit; FK cdepositbatch_cbankstatementli, cbankaccount_cdepositbatch; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bankaccount_id` | Bank Account | `numeric(10,0)` |
| `c_doctype_id` | Document Type | `numeric(10,0)` |
| `createfrom` | Create lines from | `character(1)` |
| `datedeposit` | Deposit Date | `timestamp without time zone` |
| `datedoc` | Document Date | `timestamp without time zone` |
| `depositamt` | Deposit Amount | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cdepositbatch_cbankstatementli` | `c_bankstatementline.(c_depositbatch_id)` → `c_depositbatch.(c_depositbatch_id)` | Bank statement line |
| outgoing | `cbankaccount_cdepositbatch` | `c_depositbatch.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |
| outgoing | `ccurrency_cdepositbatch` | `c_depositbatch.(c_currency_id)` → `c_currency.(c_currency_id)` | Currency |
| outgoing | `cdoctype_cdepositbatch` | `c_depositbatch.(c_doctype_id)` → `c_doctype.(c_doctype_id)` | Document Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_depositbatchline"></a>
## `c_depositbatchline` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Deposit Batch Line`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Deposit Batch Line'; 주요 열 c_payment_id, line, payamt, processed; FK cdepositbatch_cdepositbatchlin, cpayment_cdepositbatchline; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_payment_id` | Payment | `numeric(10,0)` |
| `line` | Line No | `numeric(10,0)` |
| `payamt` | Payment amount | `numeric` |
| `processed` | Processed | `character(1)` |
| `processing` | Process Now | `character(1)` |
| `c_depositbatch_id` | Deposit Batch | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cdepositbatch_cdepositbatchlin` | `c_depositbatchline.(c_depositbatch_id)` → `c_depositbatch.(c_depositbatch_id)` | Deposit Batch |
| outgoing | `cpayment_cdepositbatchline` | `c_depositbatchline.(c_payment_id)` → `c_payment.(c_payment_id)` | Payment |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_docbasegroup"></a>
## `c_docbasegroup` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Document Base Type Group`
- 사전 Description: Group of Document Base Type for Period Control
- 근거 문장: 사전 Name='Document Base Type Group'; Description='Group of Document Base Type for Period Control'; 주요 열 근거 부족; FK cperioddocgroup_cperioddocgrou; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cperioddocgroup_cperioddocgrou` | `c_docbasegroupline.(c_docbasegroup_id)` → `c_docbasegroup.(c_docbasegroup_id)` | Document Base Type Group Line |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_docbasegroupline"></a>
## `c_docbasegroupline` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Document Base Type Group Line`
- 사전 Description: Line Items of a Document Base Type Group
- 근거 문장: 사전 Name='Document Base Type Group Line'; Description='Line Items of a Document Base Type Group'; 주요 열 c_docbasegroup_id, docbasetype; FK cperioddocgroup_cperioddocgrou; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_docbasegroup_id` | Document Base Type Group | `numeric(10,0)` |
| `docbasetype` | Document Base Type | `character varying(3)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cperioddocgroup_cperioddocgrou` | `c_docbasegroupline.(c_docbasegroup_id)` → `c_docbasegroup.(c_docbasegroup_id)` | Document Base Type Group |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_doctype"></a>
## `c_doctype` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Document Type`
- 사전 Description: Document type or rules
- 근거 문장: 사전 Name='Document Type'; Description='Document type or rules'; 주요 열 docbasetype, c_doctypeproforma_id, c_doctypeshipment_id, c_doctypeinvoice_id; FK cdoctype_addocumentactionacces, cdoctype_cchargetypedoctype; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `docbasetype` | Document Base Type | `character(3)` |
| `c_doctypeproforma_id` | Document Type for ProForma | `numeric(10,0)` |
| `c_doctypeshipment_id` | Document Type for Shipment | `numeric(10,0)` |
| `c_doctypeinvoice_id` | Document Type for Invoice | `numeric(10,0)` |
| `c_doctypedifference_id` | Difference Document | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cdoctype_addocumentactionacces` | `ad_document_action_access.(c_doctype_id)` → `c_doctype.(c_doctype_id)` | Document Action Access |
| incoming | `cdoctype_cchargetypedoctype` | `c_chargetype_doctype.(c_doctype_id)` → `c_doctype.(c_doctype_id)` | Charge Type by Doc Type |
| incoming | `cdoctype_cdoctypetrl` | `c_doctype_trl.(c_doctype_id)` → `c_doctype.(c_doctype_id)` | Document Type Trl |
| outgoing | `ad_sequence_doctypedoc` | `c_doctype.(docnosequence_id)` → `ad_sequence.(ad_sequence_id)` | Sequence |

<a id="t-c_doctype_trl"></a>
## `c_doctype_trl` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Document Type Trl`
- 사전 Description: Document type or rules
- 근거 문장: 사전 Name='Document Type Trl'; Description='Document type or rules'; 주요 열 근거 부족; FK cdoctype_cdoctypetrl; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cdoctype_cdoctypetrl` | `c_doctype_trl.(c_doctype_id)` → `c_doctype.(c_doctype_id)` | Document Type |

<a id="t-c_doctypecounter"></a>
## `c_doctypecounter` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Counter Document`
- 사전 Description: Counter Document Relationship
- 근거 문장: 사전 Name='Counter Document'; Description='Counter Document Relationship'; 주요 열 c_doctype_id, counter_c_doctype_id, isvalid, processing; FK cdoctype_cdoctypecounter, cdoctypecount_cdoctypecount; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_doctype_id` | Document Type | `numeric(10,0)` |
| `counter_c_doctype_id` | Counter Document Type | `numeric(10,0)` |
| `isvalid` | Valid | `character(1)` |
| `processing` | Process Now | `character(1)` |
| `docaction` | Document Action | `character(2)` |
| `iscreatecounter` | Create Counter Document | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cdoctype_cdoctypecounter` | `c_doctypecounter.(c_doctype_id)` → `c_doctype.(c_doctype_id)` | Document Type |
| outgoing | `cdoctypecount_cdoctypecount` | `c_doctypecounter.(counter_c_doctype_id)` → `c_doctype.(c_doctype_id)` | Document Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_dunning"></a>
## `c_dunning` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dunning`
- 사전 Description: Dunning Rules for overdue invoices
- 근거 문장: 사전 Name='Dunning'; Description='Dunning Rules for overdue invoices'; 주요 열 근거 부족; FK cdunning_cdunninglevel, cdunning_cdunningrun; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cdunning_cdunninglevel` | `c_dunninglevel.(c_dunning_id)` → `c_dunning.(c_dunning_id)` | Dunning Level |
| incoming | `cdunning_cdunningrun` | `c_dunningrun.(c_dunning_id)` → `c_dunning.(c_dunning_id)` | Dunning Run |

<a id="t-c_dunninglevel"></a>
## `c_dunninglevel` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dunning Level`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Dunning Level'; 주요 열 c_dunning_id, issetpaymentterm, c_paymentterm_id, isstatement; FK cdunninglevel_cdltrl, cdunninglevel_cdunningrun; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_dunning_id` | Dunning | `numeric(10,0)` |
| `issetpaymentterm` | Set Payment Term | `character(1)` |
| `c_paymentterm_id` | Payment Term | `numeric(10,0)` |
| `isstatement` | Is Statement | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cdunninglevel_cdltrl` | `c_dunninglevel_trl.(c_dunninglevel_id)` → `c_dunninglevel.(c_dunninglevel_id)` | Dunning Level Trl |
| incoming | `cdunninglevel_cdunningrun` | `c_dunningrun.(c_dunninglevel_id)` → `c_dunninglevel.(c_dunninglevel_id)` | Dunning Run |
| incoming | `cdunninglevel_cdunningrunentry` | `c_dunningrunentry.(c_dunninglevel_id)` → `c_dunninglevel.(c_dunninglevel_id)` | Dunning Run Entry |
| outgoing | `cdunning_cdunninglevel` | `c_dunninglevel.(c_dunning_id)` → `c_dunning.(c_dunning_id)` | Dunning |

<a id="t-c_dunninglevel_trl"></a>
## `c_dunninglevel_trl` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dunning Level Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Dunning Level Trl'; 주요 열 근거 부족; FK cdunninglevel_cdltrl; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cdunninglevel_cdltrl` | `c_dunninglevel_trl.(c_dunninglevel_id)` → `c_dunninglevel.(c_dunninglevel_id)` | Dunning Level |

<a id="t-c_dunningrun"></a>
## `c_dunningrun` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dunning Run`
- 사전 Description: Dunning Run
- 근거 문장: 사전 Name='Dunning Run'; Description='Dunning Run'; 주요 열 c_dunninglevel_id, c_dunning_id; FK cdunningrun_cdunningrunentry, cdunning_cdunningrun; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_dunninglevel_id` | Dunning Level | `numeric(10,0)` |
| `c_dunning_id` | Dunning | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cdunningrun_cdunningrunentry` | `c_dunningrunentry.(c_dunningrun_id)` → `c_dunningrun.(c_dunningrun_id)` | Dunning Run Entry |
| outgoing | `cdunning_cdunningrun` | `c_dunningrun.(c_dunning_id)` → `c_dunning.(c_dunning_id)` | Dunning |
| outgoing | `cdunninglevel_cdunningrun` | `c_dunningrun.(c_dunninglevel_id)` → `c_dunninglevel.(c_dunninglevel_id)` | Dunning Level |

<a id="t-c_dunningrunentry"></a>
## `c_dunningrunentry` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dunning Run Entry`
- 사전 Description: Dunning Run Entry
- 근거 문장: 사전 Name='Dunning Run Entry'; Description='Dunning Run Entry'; 주요 열 c_dunningrun_id, c_dunninglevel_id; FK cdunningrunentry_line, cdunninglevel_cdunningrunentry; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_dunningrun_id` | Dunning Run | `numeric(10,0)` |
| `c_dunninglevel_id` | Dunning Level | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cdunningrunentry_line` | `c_dunningrunline.(c_dunningrunentry_id)` → `c_dunningrunentry.(c_dunningrunentry_id)` | Dunning Run Line |
| outgoing | `cdunninglevel_cdunningrunentry` | `c_dunningrunentry.(c_dunninglevel_id)` → `c_dunninglevel.(c_dunninglevel_id)` | Dunning Level |
| outgoing | `cdunningrun_cdunningrunentry` | `c_dunningrunentry.(c_dunningrun_id)` → `c_dunningrun.(c_dunningrun_id)` | Dunning Run |

<a id="t-c_dunningrunline"></a>
## `c_dunningrunline` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dunning Run Line`
- 사전 Description: Dunning Run Line
- 근거 문장: 사전 Name='Dunning Run Line'; Description='Dunning Run Line'; 주요 열 c_dunningrunentry_id, c_payment_id; FK cdunningrunentry_line, cinvoicepayschedule_cdunningru; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_dunningrunentry_id` | Dunning Run Entry | `numeric(10,0)` |
| `c_payment_id` | Payment | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cdunningrunentry_line` | `c_dunningrunline.(c_dunningrunentry_id)` → `c_dunningrunentry.(c_dunningrunentry_id)` | Dunning Run Entry |
| outgoing | `cinvoicepayschedule_cdunningru` | `c_dunningrunline.(c_invoicepayschedule_id)` → `c_invoicepayschedule.(c_invoicepayschedule_id)` | Invoice Payment Schedule |
| outgoing | `cpayment_cdunningrunline` | `c_dunningrunline.(c_payment_id)` → `c_payment.(c_payment_id)` | Payment |

<a id="t-c_element"></a>
## `c_element` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Element`
- 사전 Description: Accounting Element
- 근거 문장: 사전 Name='Element'; Description='Accounting Element'; 주요 열 ad_tree_id; FK celement_caschemaelement, celement_celementvalue; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_tree_id` | Tree | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `celement_caschemaelement` | `c_acctschema_element.(c_element_id)` → `c_element.(c_element_id)` | Acct.Schema Element |
| incoming | `celement_celementvalue` | `c_elementvalue.(c_element_id)` → `c_element.(c_element_id)` | Account Element |
| outgoing | `adtree_celement` | `c_element.(ad_tree_id)` → `ad_tree.(ad_tree_id)` | Tree |

<a id="t-c_elementvalue"></a>
## `c_elementvalue` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Account Element`
- 사전 Description: Account Element
- 근거 문장: 사전 Name='Account Element'; Description='Account Element'; 주요 열 accounttype, accountsign, c_element_id, postbudget; FK account_factacctsummary, account_gljournalline; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `accounttype` | Account Type | `character(1)` |
| `accountsign` | Account Sign | `character(1)` |
| `c_element_id` | Element | `numeric(10,0)` |
| `postbudget` | Post Budget | `character(1)` |
| `isbankaccount` | Bank Account | `character(1)` |
| `c_bankaccount_id` | Bank Account | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `account_factacctsummary` | `fact_acct_summary.(account_id)` → `c_elementvalue.(c_elementvalue_id)` | Accounting Fact summary |
| incoming | `account_gljournalline` | `gl_journalline.(account_id)` → `c_elementvalue.(c_elementvalue_id)` | Journal Line |
| incoming | `account_ifajournal` | `i_fajournal.(account_id)` → `c_elementvalue.(c_elementvalue_id)` | FA Journal |
| incoming | `celementvalue_caschemaelement` | `c_acctschema_element.(c_elementvalue_id)` → `c_elementvalue.(c_elementvalue_id)` | Acct.Schema Element |

<a id="t-c_elementvalue_trl"></a>
## `c_elementvalue_trl` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Account Element Trl`
- 사전 Description: Account Element
- 근거 문장: 사전 Name='Account Element Trl'; Description='Account Element'; 주요 열 istranslated; FK adlanguage_celementvaluetrl, celementvalue_cevaluetrl; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istranslated` | Translated | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlanguage_celementvaluetrl` | `c_elementvalue_trl.(ad_language)` → `ad_language.(ad_language)` | Language ID |
| outgoing | `celementvalue_cevaluetrl` | `c_elementvalue_trl.(c_elementvalue_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |

검토 후보: 회계·원장·예산 (규칙 점수 11); 애플리케이션 사전·화면·서식 (규칙 점수 11).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_greeting"></a>
## `c_greeting` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Greeting`
- 사전 Description: Greeting to print on correspondence
- 근거 문장: 사전 Name='Greeting'; Description='Greeting to print on correspondence'; 주요 열 근거 부족; FK cgreeting_cgreetingtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cgreeting_cgreetingtrl` | `c_greeting_trl.(c_greeting_id)` → `c_greeting.(c_greeting_id)` | Greeting Trl |

<a id="t-c_greeting_trl"></a>
## `c_greeting_trl` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Greeting Trl`
- 사전 Description: Greeting to print on correspondence
- 근거 문장: 사전 Name='Greeting Trl'; Description='Greeting to print on correspondence'; 주요 열 근거 부족; FK cgreeting_cgreetingtrl; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cgreeting_cgreetingtrl` | `c_greeting_trl.(c_greeting_id)` → `c_greeting.(c_greeting_id)` | Greeting |

<a id="t-c_interorg_acct"></a>
## `c_interorg_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_InterOrg_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_InterOrg_Acct'; 주요 열 intercompanydueto_acct, intercompanyduefrom_acct; FK cacctschema_cinterorgacct, vc_intercompanyduefrom_cintero; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `intercompanydueto_acct` | Intercompany Due To Acct | `numeric(10,0)` |
| `intercompanyduefrom_acct` | Intercompany Due From Acct | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_cinterorgacct` | `c_interorg_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `vc_intercompanyduefrom_cintero` | `c_interorg_acct.(intercompanyduefrom_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_intercompanydueto_cinterorg` | `c_interorg_acct.(intercompanydueto_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_invoice"></a>
## `c_invoice` — 청구·대변 문서

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Invoice`
- 사전 Description: Invoice Identifier
- 근거 문장: 사전 Name='Invoice'; Description='Invoice Identifier'; 주요 열 dateinvoiced, totallines, grandtotal; FK cinvoice_cinvoicebatchline, cinvoice_cinvoiceline; 사전 의미와 열/FK가 청구·대변 문서를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `dateinvoiced` | Date Invoiced | `timestamp without time zone` |
| `totallines` | Total Lines | `numeric` |
| `grandtotal` | Grand Total | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cinvoice_cinvoicebatchline` | `c_invoicebatchline.(c_invoice_id)` → `c_invoice.(c_invoice_id)` | Invoice Batch Line |
| incoming | `cinvoice_cinvoiceline` | `c_invoiceline.(c_invoice_id)` → `c_invoice.(c_invoice_id)` | Invoice Line |
| incoming | `cinvoice_cinvoicepaysched` | `c_invoicepayschedule.(c_invoice_id)` → `c_invoice.(c_invoice_id)` | Invoice Payment Schedule |
| incoming | `cinvoice_cinvoicetax` | `c_invoicetax.(c_invoice_id)` → `c_invoice.(c_invoice_id)` | C_InvoiceTax |

<a id="t-c_invoicebatch"></a>
## `c_invoicebatch` — 청구·대변 문서

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Invoice Batch`
- 사전 Description: Expense Invoice Batch Header
- 근거 문장: 사전 Name='Invoice Batch'; Description='Expense Invoice Batch Header'; 주요 열 근거 부족; FK cinvoicebatch_cinvoicebline; 사전 의미와 열/FK가 청구·대변 문서를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cinvoicebatch_cinvoicebline` | `c_invoicebatchline.(c_invoicebatch_id)` → `c_invoicebatch.(c_invoicebatch_id)` | Invoice Batch Line |

<a id="t-c_invoicebatchline"></a>
## `c_invoicebatchline` — 청구·대변 문서

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Invoice Batch Line`
- 사전 Description: Expense Invoice Batch Line
- 근거 문장: 사전 Name='Invoice Batch Line'; Description='Expense Invoice Batch Line'; 주요 열 c_invoicebatch_id, dateinvoiced, c_invoice_id, c_invoiceline_id; FK cinvoice_cinvoicebatchline, cinvoicebatch_cinvoicebline; 사전 의미와 열/FK가 청구·대변 문서를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_invoicebatch_id` | Invoice Batch | `numeric(10,0)` |
| `dateinvoiced` | Date Invoiced | `timestamp without time zone` |
| `c_invoice_id` | Invoice | `numeric(10,0)` |
| `c_invoiceline_id` | Invoice Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cinvoice_cinvoicebatchline` | `c_invoicebatchline.(c_invoice_id)` → `c_invoice.(c_invoice_id)` | Invoice |
| outgoing | `cinvoicebatch_cinvoicebline` | `c_invoicebatchline.(c_invoicebatch_id)` → `c_invoicebatch.(c_invoicebatch_id)` | Invoice Batch |
| outgoing | `cinvoiceline_cinvoicebline` | `c_invoicebatchline.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` | Invoice Line |

<a id="t-c_invoiceline"></a>
## `c_invoiceline` — 청구·대변 문서

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Invoice Line`
- 사전 Description: Invoice Detail Line
- 근거 문장: 사전 Name='Invoice Line'; Description='Invoice Detail Line'; 주요 열 c_invoice_id, qtyinvoiced, ref_invoiceline_id; FK cinvliceline_iinvoice, cinvoiceline_cinvoicebline; 사전 의미와 열/FK가 청구·대변 문서를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_invoice_id` | Invoice | `numeric(10,0)` |
| `qtyinvoiced` | Quantity Invoiced | `numeric` |
| `ref_invoiceline_id` | Referenced Invoice Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cinvliceline_iinvoice` | `i_invoice.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` | Import Invoice |
| incoming | `cinvoiceline_cinvoicebline` | `c_invoicebatchline.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` | Invoice Batch Line |
| incoming | `cinvoiceline_mmatchpo` | `m_matchpo.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` | Match PO |
| incoming | `convoiceline_mmatchinv` | `m_matchinv.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` | Match Invoice |

<a id="t-c_invoicepayschedule"></a>
## `c_invoicepayschedule` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Invoice Payment Schedule`
- 사전 Description: Invoice Payment Schedule
- 근거 문장: 사전 Name='Invoice Payment Schedule'; Description='Invoice Payment Schedule'; 주요 열 c_payschedule_id; FK cinvoicepayschedule_cdunningru, cpayschedule_cinvoicepaysched; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_payschedule_id` | Payment Schedule | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cinvoicepayschedule_cdunningru` | `c_dunningrunline.(c_invoicepayschedule_id)` → `c_invoicepayschedule.(c_invoicepayschedule_id)` | Dunning Run Line |
| outgoing | `cpayschedule_cinvoicepaysched` | `c_invoicepayschedule.(c_payschedule_id)` → `c_payschedule.(c_payschedule_id)` | Payment Schedule |

<a id="t-c_invoiceschedule"></a>
## `c_invoiceschedule` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Invoice Schedule`
- 사전 Description: Schedule for generating Invoices
- 근거 문장: 사전 Name='Invoice Schedule'; Description='Schedule for generating Invoices'; 주요 열 invoicefrequency; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `invoicefrequency` | Invoice Frequency | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-c_invoicetax"></a>
## `c_invoicetax` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_InvoiceTax`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_InvoiceTax'; 주요 열 taxbaseamt, taxamt, istaxincluded, c_taxprovider_id; FK ctax_cinvoicetax, ctaxprovider_cinvoicetax; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `taxbaseamt` | Tax base Amount | `numeric` |
| `taxamt` | Tax Amount | `numeric` |
| `istaxincluded` | Price includes Tax | `character(1)` |
| `c_taxprovider_id` | Tax Provider | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ctax_cinvoicetax` | `c_invoicetax.(c_tax_id)` → `c_tax.(c_tax_id)` | Tax |
| outgoing | `ctaxprovider_cinvoicetax` | `c_invoicetax.(c_taxprovider_id)` → `c_taxprovider.(c_taxprovider_id)` | Tax Provider |

<a id="t-c_job"></a>
## `c_job` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Position`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Position'; 주요 열 c_jobcategory_id, isemployee; FK cjob_aduser, cjobcategory_cjob; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_jobcategory_id` | Position Category | `numeric(10,0)` |
| `isemployee` | Employee | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cjob_aduser` | `ad_user.(c_job_id)` → `c_job.(c_job_id)` | User/Contact |
| outgoing | `cjobcategory_cjob` | `c_job.(c_jobcategory_id)` → `c_jobcategory.(c_jobcategory_id)` | Position Category |
| incoming | `cjob_cjobassignment` | `c_jobassignment.(c_job_id)` → `c_job.(c_job_id)` | Position Assignment |
| incoming | `cjob_cjobremuneration` | `c_jobremuneration.(c_job_id)` → `c_job.(c_job_id)` | Position Remuneration |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_jobassignment"></a>
## `c_jobassignment` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Position Assignment`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Position Assignment'; 주요 열 ad_user_id, c_job_id, validfrom, validto; FK aduser_cjobassignment, cjob_cjobassignment; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `c_job_id` | Position | `numeric(10,0)` |
| `validfrom` | Valid from | `timestamp without time zone` |
| `validto` | Valid to | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_cjobassignment` | `c_jobassignment.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `cjob_cjobassignment` | `c_jobassignment.(c_job_id)` → `c_job.(c_job_id)` | Position |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_jobcategory"></a>
## `c_jobcategory` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Position Category`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Position Category'; 주요 열 근거 부족; FK cjobcategory_cjob; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cjobcategory_cjob` | `c_job.(c_jobcategory_id)` → `c_jobcategory.(c_jobcategory_id)` | Position |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_jobremuneration"></a>
## `c_jobremuneration` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Position Remuneration`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Position Remuneration'; 주요 열 c_job_id, c_remuneration_id, validfrom, validto; FK cjob_cjobremuneration, cremuneration_cjobrem; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_job_id` | Position | `numeric(10,0)` |
| `c_remuneration_id` | Remuneration | `numeric(10,0)` |
| `validfrom` | Valid from | `timestamp without time zone` |
| `validto` | Valid to | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cjob_cjobremuneration` | `c_jobremuneration.(c_job_id)` → `c_job.(c_job_id)` | Position |
| outgoing | `cremuneration_cjobrem` | `c_jobremuneration.(c_remuneration_id)` → `c_remuneration.(c_remuneration_id)` | Remuneration |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_landedcost"></a>
## `c_landedcost` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Landed Cost`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Landed Cost'; 주요 열 c_invoiceline_id, m_costelement_id, m_inoutline_id, m_inout_id; FK ccostelement_clandedcost, cinvoiceline_clandedcost; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_invoiceline_id` | Invoice Line | `numeric(10,0)` |
| `m_costelement_id` | Cost Element | `numeric(10,0)` |
| `m_inoutline_id` | Shipment/Receipt Line | `numeric(10,0)` |
| `m_inout_id` | Shipment/Receipt | `numeric(10,0)` |
| `m_product_id` | Product | `numeric(10,0)` |
| `landedcostdistribution` | Cost Distribution | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ccostelement_clandedcost` | `c_landedcost.(m_costelement_id)` → `m_costelement.(m_costelement_id)` | Cost Element |
| outgoing | `cinvoiceline_clandedcost` | `c_landedcost.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` | Invoice Line |
| outgoing | `minout_clandedcost` | `c_landedcost.(m_inout_id)` → `m_inout.(m_inout_id)` | Shipment/Receipt |
| outgoing | `minoutline_clandedcost` | `c_landedcost.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Shipment/Receipt Line |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_landedcostallocation"></a>
## `c_landedcostallocation` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Landed Cost Allocation`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Landed Cost Allocation'; 주요 열 c_invoiceline_id, m_product_id, m_attributesetinstance_id, m_costelement_id; FK cinvoiceline_clandedcostalloc, masi_clandedcostallocation; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_invoiceline_id` | Invoice Line | `numeric(10,0)` |
| `m_product_id` | Product | `numeric(10,0)` |
| `m_attributesetinstance_id` | Attribute Set Instance | `numeric(10,0)` |
| `m_costelement_id` | Cost Element | `numeric(10,0)` |
| `amt` | Amount | `numeric` |
| `qty` | Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cinvoiceline_clandedcostalloc` | `c_landedcostallocation.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` | Invoice Line |
| outgoing | `masi_clandedcostallocation` | `c_landedcostallocation.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |
| outgoing | `mcostelement_mlandedcostalloc` | `c_landedcostallocation.(m_costelement_id)` → `m_costelement.(m_costelement_id)` | Cost Element |
| outgoing | `minoutline_clandedcostallocati` | `c_landedcostallocation.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Shipment/Receipt Line |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_location"></a>
## `c_location` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Address`
- 사전 Description: Location or Address
- 근거 문장: 사전 Name='Address'; Description='Location or Address'; 주요 열 address1, address2, postal, postal_add; FK bplocation_aduser, clocation_aduser; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `address1` | Address 1 | `character varying(60)` |
| `address2` | Address 2 | `character varying(60)` |
| `postal` | ZIP | `character varying(10)` |
| `postal_add` | Additional Zip | `character varying(10)` |
| `c_country_id` | Country | `numeric(10,0)` |
| `c_region_id` | Region | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `bplocation_aduser` | `ad_user.(bp_location_id)` → `c_location.(c_location_id)` | User/Contact |
| incoming | `clocation_aduser` | `ad_user.(c_location_id)` → `c_location.(c_location_id)` | User/Contact |
| incoming | `clocation_caddresstransaction` | `c_addresstransaction.(c_location_id)` → `c_location.(c_location_id)` | Address Transaction |
| incoming | `clocation_cbplocation` | `c_bpartner_location.(c_location_id)` → `c_location.(c_location_id)` | Partner Location |

<a id="t-c_nonbusinessday"></a>
## `c_nonbusinessday` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Non Business Day`
- 사전 Description: Day on which business is not transacted
- 근거 문장: 사전 Name='Non Business Day'; Description='Day on which business is not transacted'; 주요 열 date1, c_calendar_id, c_country_id; FK c_calendarnonbusinessday, ccountry_cnonbusinessday; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `date1` | Date | `timestamp without time zone` |
| `c_calendar_id` | Calendar | `numeric(10,0)` |
| `c_country_id` | Country | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `c_calendarnonbusinessday` | `c_nonbusinessday.(c_calendar_id)` → `c_calendar.(c_calendar_id)` | Calendar |
| outgoing | `ccountry_cnonbusinessday` | `c_nonbusinessday.(c_country_id)` → `c_country.(c_country_id)` | Country |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_onlinetrxhistory"></a>
## `c_onlinetrxhistory` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Online Transaction History`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Online Transaction History'; 주요 열 ad_table_id, iserror, record_id, textmsg; FK adtable_conlinetrxhistory; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `iserror` | Error | `character(1)` |
| `record_id` | Record ID | `numeric(10,0)` |
| `textmsg` | Text Message | `character varying(2000)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_conlinetrxhistory` | `c_onlinetrxhistory.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_opportunity"></a>
## `c_opportunity` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Sales Opportunity`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Sales Opportunity'; 주요 열 documentno, c_bpartner_id, ad_user_id, c_campaign_id; FK copportunity_ccontactactivity, aduser_copportunity; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `documentno` | Document No | `character varying(60)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `c_campaign_id` | Campaign | `numeric(10,0)` |
| `closedate` | Close Date | `timestamp without time zone` |
| `expectedclosedate` | Expected Close Date | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `copportunity_ccontactactivity` | `c_contactactivity.(c_opportunity_id)` → `c_opportunity.(c_opportunity_id)` | Contact Activity |
| outgoing | `aduser_copportunity` | `c_opportunity.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `cbpartner_copportunity` | `c_opportunity.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `ccampaign_copportunity` | `c_opportunity.(c_campaign_id)` → `c_campaign.(c_campaign_id)` | Campaign |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_order"></a>
## `c_order` — 주문·수주·발주

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Order`
- 사전 Description: Order
- 근거 문장: 사전 Name='Order'; Description='Order'; 주요 열 issotrx, dateordered, c_bpartner_id, c_bpartner_location_id; FK corder_corderlandedcost, corder_corderline; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `issotrx` | Sales Transaction | `character(1)` |
| `dateordered` | Date Ordered | `timestamp without time zone` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `c_bpartner_location_id` | Partner Location | `numeric(10,0)` |
| `m_pricelist_id` | Price List | `numeric(10,0)` |
| `c_ordersource_id` | Order Source | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `corder_corderlandedcost` | `c_orderlandedcost.(c_order_id)` → `c_order.(c_order_id)` | Estimated Landed Cost |
| incoming | `corder_corderline` | `c_orderline.(c_order_id)` → `c_order.(c_order_id)` | Sales Order Line |
| incoming | `corder_corderpayschedule` | `c_orderpayschedule.(c_order_id)` → `c_order.(c_order_id)` | Order Payment Schedule |
| incoming | `corder_cordertax` | `c_ordertax.(c_order_id)` → `c_order.(c_order_id)` | Order Tax |

<a id="t-c_orderlandedcost"></a>
## `c_orderlandedcost` — 주문·수주·발주

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Estimated Landed Cost`
- 사전 Description: Estimated Landed Cost for Purchase Order
- 근거 문장: 사전 Name='Estimated Landed Cost'; Description='Estimated Landed Cost for Purchase Order'; 주요 열 c_order_id; FK corderlandedcost_corderlandedc, corder_corderlandedcost; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_order_id` | Order | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `corderlandedcost_corderlandedc` | `c_orderlandedcostallocation.(c_orderlandedcost_id)` → `c_orderlandedcost.(c_orderlandedcost_id)` | Estimated Landed Cost Allocation |
| outgoing | `corder_corderlandedcost` | `c_orderlandedcost.(c_order_id)` → `c_order.(c_order_id)` | Order |

<a id="t-c_orderlandedcostallocation"></a>
## `c_orderlandedcostallocation` — 주문·수주·발주

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Estimated Landed Cost Allocation`
- 사전 Description: Estimate landed cost allocation for order line
- 근거 문장: 사전 Name='Estimated Landed Cost Allocation'; Description='Estimate landed cost allocation for order line'; 주요 열 c_orderlandedcost_id, c_orderline_id; FK corderlandedcost_corderlandedc, corderline_corderlandedcostall; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_orderlandedcost_id` | Estimated Landed Cost | `numeric(10,0)` |
| `c_orderline_id` | Sales Order Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `corderlandedcost_corderlandedc` | `c_orderlandedcostallocation.(c_orderlandedcost_id)` → `c_orderlandedcost.(c_orderlandedcost_id)` | Estimated Landed Cost |
| outgoing | `corderline_corderlandedcostall` | `c_orderlandedcostallocation.(c_orderline_id)` → `c_orderline.(c_orderline_id)` | Sales Order Line |

<a id="t-c_orderline"></a>
## `c_orderline` — 주문·수주·발주

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Sales Order Line`
- 사전 Description: Sales Order Line
- 근거 문장: 사전 Name='Sales Order Line'; Description='Sales Order Line'; 주요 열 c_order_id, c_bpartner_id, c_bpartner_location_id, dateordered; FK corderline_corderlandedcostall, corderline_iorder; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_order_id` | Order | `numeric(10,0)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `c_bpartner_location_id` | Partner Location | `numeric(10,0)` |
| `dateordered` | Date Ordered | `timestamp without time zone` |
| `qtyordered` | Ordered Quantity | `numeric` |
| `ref_orderline_id` | Referenced Order Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `corderline_corderlandedcostall` | `c_orderlandedcostallocation.(c_orderline_id)` → `c_orderline.(c_orderline_id)` | Estimated Landed Cost Allocation |
| incoming | `corderline_iorder` | `i_order.(c_orderline_id)` → `c_orderline.(c_orderline_id)` | Import Order |
| incoming | `corderline_mmatchpo` | `m_matchpo.(c_orderline_id)` → `c_orderline.(c_orderline_id)` | Match PO |
| incoming | `corderline_mrequisitionline` | `m_requisitionline.(c_orderline_id)` → `c_orderline.(c_orderline_id)` | Requisition Line |

<a id="t-c_orderpayschedule"></a>
## `c_orderpayschedule` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Order Payment Schedule`
- 사전 Description: Order Payment Schedule
- 근거 문장: 사전 Name='Order Payment Schedule'; Description='Order Payment Schedule'; 주요 열 c_order_id, c_payschedule_id, discountamt, discountdate; FK corder_corderpayschedule, cpayschedule_corderpayschedule; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_order_id` | Order | `numeric(10,0)` |
| `c_payschedule_id` | Payment Schedule | `numeric(10,0)` |
| `discountamt` | Discount Amount | `numeric` |
| `discountdate` | Discount Date | `timestamp without time zone` |
| `dueamt` | Amount due | `numeric` |
| `duedate` | Due Date | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `corder_corderpayschedule` | `c_orderpayschedule.(c_order_id)` → `c_order.(c_order_id)` | Order |
| outgoing | `cpayschedule_corderpayschedule` | `c_orderpayschedule.(c_payschedule_id)` → `c_payschedule.(c_payschedule_id)` | Payment Schedule |

검토 후보: 주문·수주·발주 (규칙 점수 12); 입출금·은행·결제 배분 (규칙 점수 12); 프로세스·스케줄·시스템 운영 (규칙 점수 12).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_ordersource"></a>
## `c_ordersource` — 주문·수주·발주

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Order Source`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Order Source'; 주요 열 근거 부족; FK c_order__c_orders_c_ordersou, cordersource_iorder; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_order__c_orders_c_ordersou` | `c_order.(c_ordersource_id)` → `c_ordersource.(c_ordersource_id)` | Order |
| incoming | `cordersource_iorder` | `i_order.(c_ordersource_id)` → `c_ordersource.(c_ordersource_id)` | Import Order |

<a id="t-c_ordertax"></a>
## `c_ordertax` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Order Tax`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Order Tax'; 주요 열 taxbaseamt, taxamt, istaxincluded, c_taxprovider_id; FK ctax_cordertax, ctaxprovider_cordertax; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `taxbaseamt` | Tax base Amount | `numeric` |
| `taxamt` | Tax Amount | `numeric` |
| `istaxincluded` | Price includes Tax | `character(1)` |
| `c_taxprovider_id` | Tax Provider | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ctax_cordertax` | `c_ordertax.(c_tax_id)` → `c_tax.(c_tax_id)` | Tax |
| outgoing | `ctaxprovider_cordertax` | `c_ordertax.(c_taxprovider_id)` → `c_taxprovider.(c_taxprovider_id)` | Tax Provider |

<a id="t-c_orgassignment"></a>
## `c_orgassignment` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Org Assignment`
- 사전 Description: Assigment to (transaction) Organization
- 근거 문장: 사전 Name='Org Assignment'; Description='Assigment to (transaction) Organization'; 주요 열 ad_user_id, validfrom, validto; FK aduser_corgassignment; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `validfrom` | Valid from | `timestamp without time zone` |
| `validto` | Valid to | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_corgassignment` | `c_orgassignment.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_payment"></a>
## `c_payment` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payment`
- 사전 Description: Payment identifier
- 근거 문장: 사전 Name='Payment'; Description='Payment identifier'; 주요 열 c_bankaccount_id, c_paymentbatch_id, tendertype, creditcardtype; FK cpayment_callocationline, cpayment_cbankstmtline; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bankaccount_id` | Bank Account | `numeric(10,0)` |
| `c_paymentbatch_id` | Payment Batch | `numeric(10,0)` |
| `tendertype` | Tender type | `character(1)` |
| `creditcardtype` | Credit Card | `character(1)` |
| `creditcardnumber` | Number | `character varying(20)` |
| `creditcardvv` | Verification Code | `character varying(4)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cpayment_callocationline` | `c_allocationline.(c_payment_id)` → `c_payment.(c_payment_id)` | Allocation Line |
| incoming | `cpayment_cbankstmtline` | `c_bankstatementline.(c_payment_id)` → `c_payment.(c_payment_id)` | Bank statement line |
| incoming | `cpayment_ccashline` | `c_cashline.(c_payment_id)` → `c_payment.(c_payment_id)` | Cash Journal Line |
| incoming | `cpayment_cdunningrunline` | `c_dunningrunline.(c_payment_id)` → `c_payment.(c_payment_id)` | Dunning Run Line |

<a id="t-c_paymentallocate"></a>
## `c_paymentallocate` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Allocate Payment`
- 사전 Description: Allocate Payment to Invoices
- 근거 문장: 사전 Name='Allocate Payment'; Description='Allocate Payment to Invoices'; 주요 열 c_payment_id, c_allocationline_id; FK cpayment_cpaymentallocate, cpaymtallocate_callocationline; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_payment_id` | Payment | `numeric(10,0)` |
| `c_allocationline_id` | Allocation Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cpayment_cpaymentallocate` | `c_paymentallocate.(c_payment_id)` → `c_payment.(c_payment_id)` | Payment |
| outgoing | `cpaymtallocate_callocationline` | `c_paymentallocate.(c_allocationline_id)` → `c_allocationline.(c_allocationline_id)` | Allocation Line |

<a id="t-c_paymentbatch"></a>
## `c_paymentbatch` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payment Batch`
- 사전 Description: Payment batch for EFT
- 근거 문장: 사전 Name='Payment Batch'; Description='Payment batch for EFT'; 주요 열 c_paymentprocessor_id; FK cpaymentbatch_cpayment, cpaymentbatch_cpaymenttransact; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_paymentprocessor_id` | Payment Processor | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cpaymentbatch_cpayment` | `c_payment.(c_paymentbatch_id)` → `c_paymentbatch.(c_paymentbatch_id)` | Payment |
| incoming | `cpaymentbatch_cpaymenttransact` | `c_paymenttransaction.(c_paymentbatch_id)` → `c_paymentbatch.(c_paymentbatch_id)` | Payment Transaction |
| outgoing | `cpaymtprocessor_cpaymtbatch` | `c_paymentbatch.(c_paymentprocessor_id)` → `c_paymentprocessor.(c_paymentprocessor_id)` | Payment Processor |

<a id="t-c_paymentprocessor"></a>
## `c_paymentprocessor` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payment Processor`
- 사전 Description: Payment processor for electronic payments
- 근거 문장: 사전 Name='Payment Processor'; Description='Payment processor for electronic payments'; 주요 열 c_bankaccount_id; FK cpaymentprocessor_cbankaccount, cpaymentprocessor_cbpbankaccou; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bankaccount_id` | Bank Account | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cpaymentprocessor_cbankaccount` | `c_bankaccount_processor.(c_paymentprocessor_id)` → `c_paymentprocessor.(c_paymentprocessor_id)` | Bank Account Processor |
| incoming | `cpaymentprocessor_cbpbankaccou` | `c_bp_bankaccount.(c_paymentprocessor_id)` → `c_paymentprocessor.(c_paymentprocessor_id)` | Partner Bank Account |
| incoming | `cpaymentprocessor_cpayment` | `c_payment.(c_paymentprocessor_id)` → `c_paymentprocessor.(c_paymentprocessor_id)` | Payment |
| incoming | `cpaymentprocessor_cpaymenttran` | `c_paymenttransaction.(c_paymentprocessor_id)` → `c_paymentprocessor.(c_paymentprocessor_id)` | Payment Transaction |

<a id="t-c_paymentterm"></a>
## `c_paymentterm` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payment Term`
- 사전 Description: The terms for Payment of this transaction
- 근거 문장: 사전 Name='Payment Term'; Description='The terms for Payment of this transaction'; 주요 열 paymenttermusage; FK cpaymentterm_cdunninglevel, cpaymentterm_cpayschedule; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `paymenttermusage` | Payment Term Usage | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cpaymentterm_cdunninglevel` | `c_dunninglevel.(c_paymentterm_id)` → `c_paymentterm.(c_paymentterm_id)` | Dunning Level |
| incoming | `cpaymentterm_cpayschedule` | `c_payschedule.(c_paymentterm_id)` → `c_paymentterm.(c_paymentterm_id)` | Payment Schedule |
| incoming | `cpaymentterm_cpaytermtrl` | `c_paymentterm_trl.(c_paymentterm_id)` → `c_paymentterm.(c_paymentterm_id)` | Payment Term Trl |

<a id="t-c_paymentterm_trl"></a>
## `c_paymentterm_trl` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payment Term Trl`
- 사전 Description: The terms of Payment (timing, discount)
- 근거 문장: 사전 Name='Payment Term Trl'; Description='The terms of Payment (timing, discount)'; 주요 열 근거 부족; FK cpaymentterm_cpaytermtrl; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cpaymentterm_cpaytermtrl` | `c_paymentterm_trl.(c_paymentterm_id)` → `c_paymentterm.(c_paymentterm_id)` | Payment Term |

<a id="t-c_paymenttransaction"></a>
## `c_paymenttransaction` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payment Transaction`
- 사전 Description: Payment Transaction
- 근거 문장: 사전 Name='Payment Transaction'; Description='Payment Transaction'; 주요 열 accountno, c_bankaccount_id, c_cashbook_id, c_payment_id; FK cbankaccount_cpaymenttransacti, cbpbankaccount_cpaymenttransac; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `accountno` | Account No | `character varying(20)` |
| `c_bankaccount_id` | Bank Account | `numeric(10,0)` |
| `c_cashbook_id` | Cash Book | `numeric(10,0)` |
| `c_payment_id` | Payment | `numeric(10,0)` |
| `c_paymentbatch_id` | Payment Batch | `numeric(10,0)` |
| `c_paymentprocessor_id` | Payment Processor | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cbankaccount_cpaymenttransacti` | `c_paymenttransaction.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |
| outgoing | `cbpbankaccount_cpaymenttransac` | `c_paymenttransaction.(c_bp_bankaccount_id)` → `c_bp_bankaccount.(c_bp_bankaccount_id)` | Partner Bank Account |
| outgoing | `ccashbook_cpaymenttransaction` | `c_paymenttransaction.(c_cashbook_id)` → `c_cashbook.(c_cashbook_id)` | Cash Book |
| outgoing | `cpayment_cpaymenttransaction` | `c_paymenttransaction.(c_payment_id)` → `c_payment.(c_payment_id)` | Payment |

<a id="t-c_payschedule"></a>
## `c_payschedule` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payment Schedule`
- 사전 Description: Payment Schedule Template
- 근거 문장: 사전 Name='Payment Schedule'; Description='Payment Schedule Template'; 주요 열 c_paymentterm_id; FK cpayschedule_cinvoicepaysched, cpayschedule_corderpayschedule; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_paymentterm_id` | Payment Term | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cpayschedule_cinvoicepaysched` | `c_invoicepayschedule.(c_payschedule_id)` → `c_payschedule.(c_payschedule_id)` | Invoice Payment Schedule |
| incoming | `cpayschedule_corderpayschedule` | `c_orderpayschedule.(c_payschedule_id)` → `c_payschedule.(c_payschedule_id)` | Order Payment Schedule |
| outgoing | `cpaymentterm_cpayschedule` | `c_payschedule.(c_paymentterm_id)` → `c_paymentterm.(c_paymentterm_id)` | Payment Term |

<a id="t-c_payselection"></a>
## `c_payselection` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payment Selection`
- 사전 Description: Payment Selection
- 근거 문장: 사전 Name='Payment Selection'; Description='Payment Selection'; 주요 열 c_bankaccount_id, isonepaymentperinvoice, reversepreparepayment; FK cpaysel_cpayselline, cpayselection_cpayselectcheck; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bankaccount_id` | Bank Account | `numeric(10,0)` |
| `isonepaymentperinvoice` | One Payment Per Invoice | `character(1)` |
| `reversepreparepayment` | Reverse Prepare Payment | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cpaysel_cpayselline` | `c_payselectionline.(c_payselection_id)` → `c_payselection.(c_payselection_id)` | Payment Selection Line |
| incoming | `cpayselection_cpayselectcheck` | `c_payselectioncheck.(c_payselection_id)` → `c_payselection.(c_payselection_id)` | Pay Selection Check |
| outgoing | `cbankaccount_cpayselection` | `c_payselection.(c_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |

<a id="t-c_payselectioncheck"></a>
## `c_payselectioncheck` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Pay Selection Check`
- 사전 Description: Payment Selection Check
- 근거 문장: 사전 Name='Pay Selection Check'; Description='Payment Selection Check'; 주요 열 c_payselection_id, payamt, c_payment_id, paymentrule; FK cpayselcheck_cpayselline, cbpbankaccount_cpayselectionch; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_payselection_id` | Payment Selection | `numeric(10,0)` |
| `payamt` | Payment amount | `numeric` |
| `c_payment_id` | Payment | `numeric(10,0)` |
| `paymentrule` | Payment Rule | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cpayselcheck_cpayselline` | `c_payselectionline.(c_payselectioncheck_id)` → `c_payselectioncheck.(c_payselectioncheck_id)` | Payment Selection Line |
| outgoing | `cbpbankaccount_cpayselectionch` | `c_payselectioncheck.(c_bp_bankaccount_id)` → `c_bp_bankaccount.(c_bp_bankaccount_id)` | Partner Bank Account |
| outgoing | `cpayment_cpayselectioncheck` | `c_payselectioncheck.(c_payment_id)` → `c_payment.(c_payment_id)` | Payment |
| outgoing | `cpayselection_cpayselectcheck` | `c_payselectioncheck.(c_payselection_id)` → `c_payselection.(c_payselection_id)` | Payment Selection |

<a id="t-c_payselectionline"></a>
## `c_payselectionline` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payment Selection Line`
- 사전 Description: Payment Selection Line
- 근거 문장: 사전 Name='Payment Selection Line'; Description='Payment Selection Line'; 주요 열 c_payselection_id, paymentrule, payamt, c_payselectioncheck_id; FK cpaysel_cpayselline, cpayselcheck_cpayselline; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_payselection_id` | Payment Selection | `numeric(10,0)` |
| `paymentrule` | Payment Rule | `character(1)` |
| `payamt` | Payment amount | `numeric` |
| `c_payselectioncheck_id` | Pay Selection Check | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cpaysel_cpayselline` | `c_payselectionline.(c_payselection_id)` → `c_payselection.(c_payselection_id)` | Payment Selection |
| outgoing | `cpayselcheck_cpayselline` | `c_payselectionline.(c_payselectioncheck_id)` → `c_payselectioncheck.(c_payselectioncheck_id)` | Pay Selection Check |

<a id="t-c_period"></a>
## `c_period` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Period`
- 사전 Description: Period of the Calendar
- 근거 문장: 사전 Name='Period'; Description='Period of the Calendar'; 주요 열 periodno, c_year_id, startdate, enddate; FK c_period_periodcontrol, cperiod_hrperiod; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `periodno` | Period No | `numeric(10,0)` |
| `c_year_id` | Year | `numeric(10,0)` |
| `startdate` | Start Date | `timestamp without time zone` |
| `enddate` | End Date | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_period_periodcontrol` | `c_periodcontrol.(c_period_id)` → `c_period.(c_period_id)` | Period Control |
| incoming | `cperiod_hrperiod` | `hr_period.(c_period_id)` → `c_period.(c_period_id)` | Payroll Period |
| outgoing | `c_year_period` | `c_period.(c_year_id)` → `c_year.(c_year_id)` | Year |

<a id="t-c_periodcontrol"></a>
## `c_periodcontrol` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Period Control`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Period Control'; 주요 열 c_period_id, docbasetype; FK c_period_periodcontrol; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_period_id` | Period | `numeric(10,0)` |
| `docbasetype` | Document Base Type | `character(3)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `c_period_periodcontrol` | `c_periodcontrol.(c_period_id)` → `c_period.(c_period_id)` | Period |

<a id="t-c_phase"></a>
## `c_phase` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Standard Phase`
- 사전 Description: Standard Phase of the Project Type
- 근거 문장: 사전 Name='Standard Phase'; Description='Standard Phase of the Project Type'; 주요 열 c_projecttype_id, standardqty; FK cphase_cproject, cphase_cprojectphase; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_projecttype_id` | Project Type | `numeric(10,0)` |
| `standardqty` | Standard Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cphase_cproject` | `c_project.(c_phase_id)` → `c_phase.(c_phase_id)` | Project |
| incoming | `cphase_cprojectphase` | `c_projectphase.(c_phase_id)` → `c_phase.(c_phase_id)` | Project Phase |
| incoming | `cphase_ctask` | `c_task.(c_phase_id)` → `c_phase.(c_phase_id)` | Standard Task |
| outgoing | `cprojecttype_cphase` | `c_phase.(c_projecttype_id)` → `c_projecttype.(c_projecttype_id)` | Project Type |

<a id="t-c_pos"></a>
## `c_pos` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `POS Terminal`
- 사전 Description: Point of Sales Terminal
- 근거 문장: 사전 Name='POS Terminal'; Description='Point of Sales Terminal'; 주요 열 m_pricelist_id, c_bpartnercashtrx_id; FK cposkeylayout_cpos, oskkeylayout_cpos; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `pos`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_pricelist_id` | Price List | `numeric(10,0)` |
| `c_bpartnercashtrx_id` | Template B.Partner | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cposkeylayout_cpos` | `c_pos.(c_poskeylayout_id)` → `c_poskeylayout.(c_poskeylayout_id)` | POS Key Layout |
| outgoing | `oskkeylayout_cpos` | `c_pos.(osk_keylayout_id)` → `c_poskeylayout.(c_poskeylayout_id)` | POS Key Layout |
| outgoing | `osnpkeylayout_cpos` | `c_pos.(osnp_keylayout_id)` → `c_poskeylayout.(c_poskeylayout_id)` | POS Key Layout |

<a id="t-c_poskey"></a>
## `c_poskey` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `POS Key`
- 사전 Description: POS Function Key
- 근거 문장: 사전 Name='POS Key'; Description='POS Function Key'; 주요 열 근거 부족; FK cposkeylayout_c_poskey, subkeylayout_cposkey; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `pos`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cposkeylayout_c_poskey` | `c_poskey.(c_poskeylayout_id)` → `c_poskeylayout.(c_poskeylayout_id)` | POS Key Layout |
| outgoing | `subkeylayout_cposkey` | `c_poskey.(subkeylayout_id)` → `c_poskeylayout.(c_poskeylayout_id)` | POS Key Layout |

<a id="t-c_poskeylayout"></a>
## `c_poskeylayout` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `POS Key Layout`
- 사전 Description: POS Function Key Layout
- 근거 문장: 사전 Name='POS Key Layout'; Description='POS Function Key Layout'; 주요 열 근거 부족; FK cposkeylayout_c_poskey, cposkeylayout_cpos; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `pos`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cposkeylayout_c_poskey` | `c_poskey.(c_poskeylayout_id)` → `c_poskeylayout.(c_poskeylayout_id)` | POS Key |
| incoming | `cposkeylayout_cpos` | `c_pos.(c_poskeylayout_id)` → `c_poskeylayout.(c_poskeylayout_id)` | POS Terminal |
| incoming | `oskkeylayout_cpos` | `c_pos.(osk_keylayout_id)` → `c_poskeylayout.(c_poskeylayout_id)` | POS Terminal |
| incoming | `osnpkeylayout_cpos` | `c_pos.(osnp_keylayout_id)` → `c_poskeylayout.(c_poskeylayout_id)` | POS Terminal |

<a id="t-c_pospayment"></a>
## `c_pospayment` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `POS Payment`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='POS Payment'; 주요 열 근거 부족; FK cpostendertype_cpospayment; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `pos`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cpostendertype_cpospayment` | `c_pospayment.(c_postendertype_id)` → `c_postendertype.(c_postendertype_id)` | POS Tender Type |

<a id="t-c_postendertype"></a>
## `c_postendertype` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `POS Tender Type`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='POS Tender Type'; 주요 열 근거 부족; FK cpostendertype_cpospayment; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `pos`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cpostendertype_cpospayment` | `c_pospayment.(c_postendertype_id)` → `c_postendertype.(c_postendertype_id)` | POS Payment |

<a id="t-c_project"></a>
## `c_project` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Project`
- 사전 Description: Financial Project
- 근거 문장: 사전 Name='Project'; Description='Financial Project'; 주요 열 plannedamt, plannedqty, plannedmarginamt, committedamt; FK c_project_projectacct, cproject_cprojectissue; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `plannedamt` | Planned Amount | `numeric` |
| `plannedqty` | Planned Quantity | `numeric` |
| `plannedmarginamt` | Planned Margin | `numeric` |
| `committedamt` | Committed Amount | `numeric` |
| `datecontract` | Contract Date | `timestamp without time zone` |
| `c_projecttype_id` | Project Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_project_projectacct` | `c_project_acct.(c_project_id)` → `c_project.(c_project_id)` | C_Project_Acct |
| incoming | `cproject_cprojectissue` | `c_projectissue.(c_project_id)` → `c_project.(c_project_id)` | Project Issue |
| incoming | `cproject_cprojectline` | `c_projectline.(c_project_id)` → `c_project.(c_project_id)` | Project Line |
| incoming | `cproject_cprojectphase` | `c_projectphase.(c_project_id)` → `c_project.(c_project_id)` | Project Phase |

<a id="t-c_project_acct"></a>
## `c_project_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_Project_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_Project_Acct'; 주요 열 pj_asset_acct, pj_wip_acct; FK cacctschema_cprojectacct, vc_pjasset_cproject; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pj_asset_acct` | Project Asset | `numeric(10,0)` |
| `pj_wip_acct` | Work In Progress | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_cprojectacct` | `c_project_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `vc_pjasset_cproject` | `c_project_acct.(pj_asset_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_pjwip_cproject` | `c_project_acct.(pj_wip_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_projectissue"></a>
## `c_projectissue` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Project Issue`
- 사전 Description: Project Issues (Material, Labor)
- 근거 문장: 사전 Name='Project Issue'; Description='Project Issues (Material, Labor)'; 주요 열 c_project_id, movementqty; FK cprojectissue_cprojectissuema, cprojectissue_cprojectline; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_project_id` | Project | `numeric(10,0)` |
| `movementqty` | Movement Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cprojectissue_cprojectissuema` | `c_projectissuema.(c_projectissue_id)` → `c_projectissue.(c_projectissue_id)` | C_ProjectIssueMA |
| incoming | `cprojectissue_cprojectline` | `c_projectline.(c_projectissue_id)` → `c_projectissue.(c_projectissue_id)` | Project Line |
| outgoing | `cproject_cprojectissue` | `c_projectissue.(c_project_id)` → `c_project.(c_project_id)` | Project |
| outgoing | `reversal_cprojectissue` | `c_projectissue.(reversal_id)` → `c_projectissue.(c_projectissue_id)` | Project Issue |

<a id="t-c_projectissuema"></a>
## `c_projectissuema` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_ProjectIssueMA`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_ProjectIssueMA'; 주요 열 movementqty; FK cprojectissue_cprojectissuema; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `movementqty` | Movement Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cprojectissue_cprojectissuema` | `c_projectissuema.(c_projectissue_id)` → `c_projectissue.(c_projectissue_id)` | Project Issue |

<a id="t-c_projectline"></a>
## `c_projectline` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Project Line`
- 사전 Description: Task or step in a project
- 근거 문장: 사전 Name='Project Line'; Description='Task or step in a project'; 주요 열 c_project_id, plannedqty, plannedprice, plannedamt; FK cproject_cprojectline, cprojectissue_cprojectline; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_project_id` | Project | `numeric(10,0)` |
| `plannedqty` | Planned Quantity | `numeric` |
| `plannedprice` | Planned Price | `numeric` |
| `plannedamt` | Planned Amount | `numeric` |
| `plannedmarginamt` | Planned Margin | `numeric` |
| `committedamt` | Committed Amount | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cproject_cprojectline` | `c_projectline.(c_project_id)` → `c_project.(c_project_id)` | Project |
| outgoing | `cprojectissue_cprojectline` | `c_projectline.(c_projectissue_id)` → `c_projectissue.(c_projectissue_id)` | Project Issue |
| outgoing | `cprojectphase_cprojectline` | `c_projectline.(c_projectphase_id)` → `c_projectphase.(c_projectphase_id)` | Project Phase |
| outgoing | `cprojecttask_cprojectline` | `c_projectline.(c_projecttask_id)` → `c_projecttask.(c_projecttask_id)` | Project Task |

<a id="t-c_projectphase"></a>
## `c_projectphase` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Project Phase`
- 사전 Description: Phase of a Project
- 근거 문장: 사전 Name='Project Phase'; Description='Phase of a Project'; 주요 열 c_project_id, startdate, c_phase_id, qty; FK cprojectphase_cprojectline, cprojectphase_cprojecttask; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_project_id` | Project | `numeric(10,0)` |
| `startdate` | Start Date | `timestamp without time zone` |
| `c_phase_id` | Standard Phase | `numeric(10,0)` |
| `qty` | Quantity | `numeric` |
| `committedamt` | Committed Amount | `numeric` |
| `plannedamt` | Planned Amount | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cprojectphase_cprojectline` | `c_projectline.(c_projectphase_id)` → `c_projectphase.(c_projectphase_id)` | Project Line |
| incoming | `cprojectphase_cprojecttask` | `c_projecttask.(c_projectphase_id)` → `c_projectphase.(c_projectphase_id)` | Project Task |
| outgoing | `cphase_cprojectphase` | `c_projectphase.(c_phase_id)` → `c_phase.(c_phase_id)` | Standard Phase |
| outgoing | `cproject_cprojectphase` | `c_projectphase.(c_project_id)` → `c_project.(c_project_id)` | Project |

<a id="t-c_projecttask"></a>
## `c_projecttask` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Project Task`
- 사전 Description: Actual Project Task in a Phase
- 근거 문장: 사전 Name='Project Task'; Description='Actual Project Task in a Phase'; 주요 열 c_task_id, c_projectphase_id, qty, plannedamt; FK cprojecttask_cprojectline, cprojectphase_cprojecttask; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_task_id` | Standard Task | `numeric(10,0)` |
| `c_projectphase_id` | Project Phase | `numeric(10,0)` |
| `qty` | Quantity | `numeric` |
| `plannedamt` | Planned Amount | `numeric` |
| `committedamt` | Committed Amount | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cprojecttask_cprojectline` | `c_projectline.(c_projecttask_id)` → `c_projecttask.(c_projecttask_id)` | Project Line |
| outgoing | `cprojectphase_cprojecttask` | `c_projecttask.(c_projectphase_id)` → `c_projectphase.(c_projectphase_id)` | Project Phase |
| outgoing | `ctask_cprojecttask` | `c_projecttask.(c_task_id)` → `c_task.(c_task_id)` | Standard Task |

<a id="t-c_projecttype"></a>
## `c_projecttype` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Project Type`
- 사전 Description: Type of the project
- 근거 문장: 사전 Name='Project Type'; Description='Type of the project'; 주요 열 projectcategory; FK cprojecttype_cphase, cprojecttype_cproject; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `projectcategory` | Project Category | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cprojecttype_cphase` | `c_phase.(c_projecttype_id)` → `c_projecttype.(c_projecttype_id)` | Standard Phase |
| incoming | `cprojecttype_cproject` | `c_project.(c_projecttype_id)` → `c_projecttype.(c_projecttype_id)` | Project |

<a id="t-c_recurring"></a>
## `c_recurring` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Recurring`
- 사전 Description: Recurring Document
- 근거 문장: 사전 Name='Recurring'; Description='Recurring Document'; 주요 열 recurringtype, c_order_id, c_invoice_id, c_payment_id; FK cinvoice_crecurring, corder_crecurring; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `recurringtype` | Recurring Type | `character(1)` |
| `c_order_id` | Order | `numeric(10,0)` |
| `c_invoice_id` | Invoice | `numeric(10,0)` |
| `c_payment_id` | Payment | `numeric(10,0)` |
| `c_project_id` | Project | `numeric(10,0)` |
| `gl_journalbatch_id` | Journal Batch | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cinvoice_crecurring` | `c_recurring.(c_invoice_id)` → `c_invoice.(c_invoice_id)` | Invoice |
| outgoing | `corder_crecurring` | `c_recurring.(c_order_id)` → `c_order.(c_order_id)` | Order |
| outgoing | `cpayment_crecurring` | `c_recurring.(c_payment_id)` → `c_payment.(c_payment_id)` | Payment |
| outgoing | `cproject_crecurring` | `c_recurring.(c_project_id)` → `c_project.(c_project_id)` | Project |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_recurring_run"></a>
## `c_recurring_run` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Recurring Run`
- 사전 Description: Recurring Document Run
- 근거 문장: 사전 Name='Recurring Run'; Description='Recurring Document Run'; 주요 열 c_payment_id, c_order_id, c_invoice_id, c_project_id; FK cinvoice_crecurringrun, corder_crecurringrun; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_payment_id` | Payment | `numeric(10,0)` |
| `c_order_id` | Order | `numeric(10,0)` |
| `c_invoice_id` | Invoice | `numeric(10,0)` |
| `c_project_id` | Project | `numeric(10,0)` |
| `gl_journalbatch_id` | Journal Batch | `numeric(10,0)` |
| `c_recurring_id` | Recurring | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cinvoice_crecurringrun` | `c_recurring_run.(c_invoice_id)` → `c_invoice.(c_invoice_id)` | Invoice |
| outgoing | `corder_crecurringrun` | `c_recurring_run.(c_order_id)` → `c_order.(c_order_id)` | Order |
| outgoing | `cpayment_crecurringrun` | `c_recurring_run.(c_payment_id)` → `c_payment.(c_payment_id)` | Payment |
| outgoing | `cproject_crecurringrun` | `c_recurring_run.(c_project_id)` → `c_project.(c_project_id)` | Project |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_recurringgroup"></a>
## `c_recurringgroup` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Recurring Group`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Recurring Group'; 주요 열 근거 부족; FK crecurringgroup_crecurring; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `crecurringgroup_crecurring` | `c_recurring.(c_recurringgroup_id)` → `c_recurringgroup.(c_recurringgroup_id)` | Recurring |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_region"></a>
## `c_region` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Region`
- 사전 Description: Identifies a geographical Region
- 근거 문장: 사전 Name='Region'; Description='Identifies a geographical Region'; 주요 열 c_country_id; FK cregion_ccity, cregion_cregiontrl; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_country_id` | Country | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cregion_ccity` | `c_city.(c_region_id)` → `c_region.(c_region_id)` | City |
| incoming | `cregion_cregiontrl` | `c_region_trl.(c_region_id)` → `c_region.(c_region_id)` | Region |
| outgoing | `ccountry_cregion` | `c_region.(c_country_id)` → `c_country.(c_country_id)` | Country |

<a id="t-c_region_trl"></a>
## `c_region_trl` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Region`
- 사전 Description: Identifies a geographical Region
- 근거 문장: 사전 Name='Region'; Description='Identifies a geographical Region'; 주요 열 근거 부족; FK cregion_cregiontrl; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cregion_cregiontrl` | `c_region_trl.(c_region_id)` → `c_region.(c_region_id)` | Region |

<a id="t-c_remuneration"></a>
## `c_remuneration` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Remuneration`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Remuneration'; 주요 열 remunerationtype, standardhours, grossramt, grossrcost; FK cremuneration_cjobrem, cremuneration_cuserrem; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `remunerationtype` | Remuneration Type | `character(1)` |
| `standardhours` | Standard Hours | `numeric(10,0)` |
| `grossramt` | Gross Amount | `numeric` |
| `grossrcost` | Gross Cost | `numeric` |
| `overtimeamt` | Overtime Amount | `numeric` |
| `overtimecost` | Overtime Cost | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cremuneration_cjobrem` | `c_jobremuneration.(c_remuneration_id)` → `c_remuneration.(c_remuneration_id)` | Position Remuneration |
| incoming | `cremuneration_cuserrem` | `c_userremuneration.(c_remuneration_id)` → `c_remuneration.(c_remuneration_id)` | Employee Remuneration |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_revenuerecog_service"></a>
## `c_revenuerecog_service` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Revenue Recognition Service`
- 사전 Description: Plan for recognizing or recording revenue based on service
- 근거 문장: 사전 Name='Revenue Recognition Service'; Description='Plan for recognizing or recording revenue based on service'; 주요 열 c_revenuerecognition_id, line, percent; FK crevenuerecognition_crevenuere, crevenuerecogservice_crevenuer; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_revenuerecognition_id` | Revenue Recognition | `numeric(10,0)` |
| `line` | Line No | `numeric(10,0)` |
| `percent` | Percent | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `crevenuerecognition_crevenuere` | `c_revenuerecog_service.(c_revenuerecognition_id)` → `c_revenuerecognition.(c_revenuerecognition_id)` | Revenue Recognition |
| incoming | `crevenuerecogservice_crevenuer` | `c_revenuerecognition_run.(c_revenuerecog_service_id)` → `c_revenuerecog_service.(c_revenuerecog_service_id)` | Revenue Recognition Run |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_revenuerecognition"></a>
## `c_revenuerecognition` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Revenue Recognition`
- 사전 Description: Method for recording revenue
- 근거 문장: 사전 Name='Revenue Recognition'; Description='Method for recording revenue'; 주요 열 istimebased, recognitionfrequency, nomonths, fixedrecogday; FK crevenuerecognition_crevenuere, crevenuerecognition_plan; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istimebased` | Time based | `character(1)` |
| `recognitionfrequency` | Recognition frequency | `character(1)` |
| `nomonths` | Number of Months | `numeric(10,0)` |
| `fixedrecogday` | Fixed recognition day | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `crevenuerecognition_crevenuere` | `c_revenuerecog_service.(c_revenuerecognition_id)` → `c_revenuerecognition.(c_revenuerecognition_id)` | Revenue Recognition Service |
| incoming | `crevenuerecognition_plan` | `c_revenuerecognition_plan.(c_revenuerecognition_id)` → `c_revenuerecognition.(c_revenuerecognition_id)` | Revenue Recognition Plan |
| incoming | `crevrecognition_mproduct` | `m_product.(c_revenuerecognition_id)` → `c_revenuerecognition.(c_revenuerecognition_id)` | Product |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_revenuerecognition_plan"></a>
## `c_revenuerecognition_plan` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Revenue Recognition Plan`
- 사전 Description: Plan for recognizing or recording revenue
- 근거 문장: 사전 Name='Revenue Recognition Plan'; Description='Plan for recognizing or recording revenue'; 주요 열 c_acctschema_id, c_revenuerecognition_id, c_invoiceline_id, unearnedrevenue_acct; FK cacctschema_crevrecplan, ccurrency_crevenuerecplan; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `c_revenuerecognition_id` | Revenue Recognition | `numeric(10,0)` |
| `c_invoiceline_id` | Invoice Line | `numeric(10,0)` |
| `unearnedrevenue_acct` | Unearned Revenue | `numeric(10,0)` |
| `p_revenue_acct` | Product Revenue | `numeric(10,0)` |
| `c_currency_id` | Currency | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_crevrecplan` | `c_revenuerecognition_plan.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `ccurrency_crevenuerecplan` | `c_revenuerecognition_plan.(c_currency_id)` → `c_currency.(c_currency_id)` | Currency |
| outgoing | `cinvoiceline_crevenuerecplan` | `c_revenuerecognition_plan.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` | Invoice Line |
| outgoing | `crevenuerecognition_plan` | `c_revenuerecognition_plan.(c_revenuerecognition_id)` → `c_revenuerecognition.(c_revenuerecognition_id)` | Revenue Recognition |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_revenuerecognition_run"></a>
## `c_revenuerecognition_run` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Revenue Recognition Run`
- 사전 Description: Revenue Recognition Run or Process
- 근거 문장: 사전 Name='Revenue Recognition Run'; Description='Revenue Recognition Run or Process'; 주요 열 c_revenuerecognition_plan_id, gl_journal_id, recognizedamt, daterecognized; FK crevenuerecogservice_crevenuer, crevrecplan_crefrecrun; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_revenuerecognition_plan_id` | Revenue Recognition Plan | `numeric(10,0)` |
| `gl_journal_id` | Journal | `numeric(10,0)` |
| `recognizedamt` | Recognized Amount | `numeric` |
| `daterecognized` | Recognition Date | `timestamp without time zone` |
| `c_revenuerecog_service_id` | Revenue Recognition Service | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `crevenuerecogservice_crevenuer` | `c_revenuerecognition_run.(c_revenuerecog_service_id)` → `c_revenuerecog_service.(c_revenuerecog_service_id)` | Revenue Recognition Service |
| outgoing | `crevrecplan_crefrecrun` | `c_revenuerecognition_run.(c_revenuerecognition_plan_id)` → `c_revenuerecognition_plan.(c_revenuerecognition_plan_id)` | Revenue Recognition Plan |
| outgoing | `gljournal_crevenuerecrun` | `c_revenuerecognition_run.(gl_journal_id)` → `gl_journal.(gl_journal_id)` | Journal |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_rfq"></a>
## `c_rfq` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RfQ`
- 사전 Description: Request for Quotation
- 근거 문장: 사전 Name='RfQ'; Description='Request for Quotation'; 주요 열 c_bpartner_id, c_bpartner_location_id; FK crfq_crfqline, crfq_crfqresponse; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `c_bpartner_location_id` | Partner Location | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `crfq_crfqline` | `c_rfqline.(c_rfq_id)` → `c_rfq.(c_rfq_id)` | RfQ Line |
| incoming | `crfq_crfqresponse` | `c_rfqresponse.(c_rfq_id)` → `c_rfq.(c_rfq_id)` | RfQ Response |
| outgoing | `crfqtopic_crfq` | `c_rfq.(c_rfq_topic_id)` → `c_rfq_topic.(c_rfq_topic_id)` | RfQ Topic |

<a id="t-c_rfq_topic"></a>
## `c_rfq_topic` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RfQ Topic`
- 사전 Description: Topic for Request for Quotations
- 근거 문장: 사전 Name='RfQ Topic'; Description='Topic for Request for Quotations'; 주요 열 근거 부족; FK c_rfqtopic_subscriber, crfqtopic_crfq; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_rfqtopic_subscriber` | `c_rfq_topicsubscriber.(c_rfq_topic_id)` → `c_rfq_topic.(c_rfq_topic_id)` | RfQ Subscriber |
| incoming | `crfqtopic_crfq` | `c_rfq.(c_rfq_topic_id)` → `c_rfq_topic.(c_rfq_topic_id)` | RfQ |

<a id="t-c_rfq_topicsubscriber"></a>
## `c_rfq_topicsubscriber` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RfQ Subscriber`
- 사전 Description: Request for Quotation Topic Subscriber
- 근거 문장: 사전 Name='RfQ Subscriber'; Description='Request for Quotation Topic Subscriber'; 주요 열 c_bpartner_id, c_bpartner_location_id; FK c_rfqtopic_subscriber; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `c_bpartner_location_id` | Partner Location | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `c_rfqtopic_subscriber` | `c_rfq_topicsubscriber.(c_rfq_topic_id)` → `c_rfq_topic.(c_rfq_topic_id)` | RfQ Topic |

<a id="t-c_rfq_topicsubscriberonly"></a>
## `c_rfq_topicsubscriberonly` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RfQ Topic Subscriber Restriction`
- 사전 Description: Include Subscriber only for certain products or product categories
- 근거 문장: 사전 Name='RfQ Topic Subscriber Restriction'; Description='Include Subscriber only for certain products or product categories'; 주요 열 m_product_id, m_product_category_id; FK mprodcategory_crfqtsubonly, mproduct_crfqtsubonly; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_product_id` | Product | `numeric(10,0)` |
| `m_product_category_id` | Product Category | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mprodcategory_crfqtsubonly` | `c_rfq_topicsubscriberonly.(m_product_category_id)` → `m_product_category.(m_product_category_id)` | Product Category |
| outgoing | `mproduct_crfqtsubonly` | `c_rfq_topicsubscriberonly.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-c_rfqline"></a>
## `c_rfqline` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RfQ Line`
- 사전 Description: Request for Quotation Line
- 근거 문장: 사전 Name='RfQ Line'; Description='Request for Quotation Line'; 주요 열 근거 부족; FK crfqline_crfqlineqty, crfqline_crfqresponseline; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `crfqline_crfqlineqty` | `c_rfqlineqty.(c_rfqline_id)` → `c_rfqline.(c_rfqline_id)` | RfQ Line Quantity |
| incoming | `crfqline_crfqresponseline` | `c_rfqresponseline.(c_rfqline_id)` → `c_rfqline.(c_rfqline_id)` | RfQ Response Line |
| outgoing | `crfq_crfqline` | `c_rfqline.(c_rfq_id)` → `c_rfq.(c_rfq_id)` | RfQ |

<a id="t-c_rfqlineqty"></a>
## `c_rfqlineqty` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RfQ Line Quantity`
- 사전 Description: Request for Quotation Line Quantity
- 근거 문장: 사전 Name='RfQ Line Quantity'; Description='Request for Quotation Line Quantity'; 주요 열 근거 부족; FK crfqlineqty_crfqresplineqty, crfqline_crfqlineqty; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `crfqlineqty_crfqresplineqty` | `c_rfqresponselineqty.(c_rfqlineqty_id)` → `c_rfqlineqty.(c_rfqlineqty_id)` | RfQ Response Line Qty |
| outgoing | `crfqline_crfqlineqty` | `c_rfqlineqty.(c_rfqline_id)` → `c_rfqline.(c_rfqline_id)` | RfQ Line |

<a id="t-c_rfqresponse"></a>
## `c_rfqresponse` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RfQ Response`
- 사전 Description: Request for Quotation Response from a potential Vendor
- 근거 문장: 사전 Name='RfQ Response'; Description='Request for Quotation Response from a potential Vendor'; 주요 열 c_rfq_id, c_bpartner_id, c_bpartner_location_id, ad_user_id; FK aduser_crfqresponse, cbpartner_crfqresponse; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_rfq_id` | RfQ | `numeric(10,0)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `c_bpartner_location_id` | Partner Location | `numeric(10,0)` |
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `c_currency_id` | Currency | `numeric(10,0)` |
| `dateinvited` | Invited | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_crfqresponse` | `c_rfqresponse.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `cbpartner_crfqresponse` | `c_rfqresponse.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `cbplocation_crfqresponse` | `c_rfqresponse.(c_bpartner_location_id)` → `c_bpartner_location.(c_bpartner_location_id)` | Partner Location |
| outgoing | `ccurrency_crfqresponse` | `c_rfqresponse.(c_currency_id)` → `c_currency.(c_currency_id)` | Currency |

검토 후보: 거래처·연락처·주소 (규칙 점수 8); 요청·지원·이슈 (규칙 점수 8).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_rfqresponseline"></a>
## `c_rfqresponseline` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RfQ Response Line`
- 사전 Description: Request for Quotation Response Line
- 근거 문장: 사전 Name='RfQ Response Line'; Description='Request for Quotation Response Line'; 주요 열 근거 부족; FK crfqresonseline_qty, crfqline_crfqresponseline; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `crfqresonseline_qty` | `c_rfqresponselineqty.(c_rfqresponseline_id)` → `c_rfqresponseline.(c_rfqresponseline_id)` | RfQ Response Line Qty |
| outgoing | `crfqline_crfqresponseline` | `c_rfqresponseline.(c_rfqline_id)` → `c_rfqline.(c_rfqline_id)` | RfQ Line |
| outgoing | `crfqresponse_line` | `c_rfqresponseline.(c_rfqresponse_id)` → `c_rfqresponse.(c_rfqresponse_id)` | RfQ Response |

<a id="t-c_rfqresponselineqty"></a>
## `c_rfqresponselineqty` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RfQ Response Line Qty`
- 사전 Description: Request for Quotation Response Line Quantity
- 근거 문장: 사전 Name='RfQ Response Line Qty'; Description='Request for Quotation Response Line Quantity'; 주요 열 근거 부족; FK crfqlineqty_crfqresplineqty, crfqresonseline_qty; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `crfqlineqty_crfqresplineqty` | `c_rfqresponselineqty.(c_rfqlineqty_id)` → `c_rfqlineqty.(c_rfqlineqty_id)` | RfQ Line Quantity |
| outgoing | `crfqresonseline_qty` | `c_rfqresponselineqty.(c_rfqresponseline_id)` → `c_rfqresponseline.(c_rfqresponseline_id)` | RfQ Response Line |

<a id="t-c_salesregion"></a>
## `c_salesregion` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Sales Region`
- 사전 Description: Sales coverage region
- 근거 문장: 사전 Name='Sales Region'; Description='Sales coverage region'; 주요 열 근거 부족; FK csalesregion_csalesregiontrl; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `csalesregion_csalesregiontrl` | `c_salesregion_trl.(c_salesregion_id)` → `c_salesregion.(c_salesregion_id)` | Sales Region Trl |

<a id="t-c_salesregion_trl"></a>
## `c_salesregion_trl` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Sales Region Trl`
- 사전 Description: Sales coverage region
- 근거 문장: 사전 Name='Sales Region Trl'; Description='Sales coverage region'; 주요 열 근거 부족; FK csalesregion_csalesregiontrl; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `csalesregion_csalesregiontrl` | `c_salesregion_trl.(c_salesregion_id)` → `c_salesregion.(c_salesregion_id)` | Sales Region |

<a id="t-c_salesstage"></a>
## `c_salesstage` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Sales Stage`
- 사전 Description: Stages of the sales process
- 근거 문장: 사전 Name='Sales Stage'; Description='Stages of the sales process'; 주요 열 근거 부족; FK csalesstage_csalesstagetrl; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `csalesstage_csalesstagetrl` | `c_salesstage_trl.(c_salesstage_id)` → `c_salesstage.(c_salesstage_id)` | Sales Stage Trl |

<a id="t-c_salesstage_trl"></a>
## `c_salesstage_trl` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Sales Stage Trl`
- 사전 Description: Stages of the sales process
- 근거 문장: 사전 Name='Sales Stage Trl'; Description='Stages of the sales process'; 주요 열 근거 부족; FK csalesstage_csalesstagetrl; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `csalesstage_csalesstagetrl` | `c_salesstage_trl.(c_salesstage_id)` → `c_salesstage.(c_salesstage_id)` | Sales Stage |

<a id="t-c_servicelevel"></a>
## `c_servicelevel` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Service Level`
- 사전 Description: Product Revenue Recognition Service Level 
- 근거 문장: 사전 Name='Service Level'; Description='Product Revenue Recognition Service Level '; 주요 열 m_product_id; FK cservicelevel_line, mproduct_cservicelevel; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_product_id` | Product | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cservicelevel_line` | `c_servicelevelline.(c_servicelevel_id)` → `c_servicelevel.(c_servicelevel_id)` | Service Level Line |
| outgoing | `mproduct_cservicelevel` | `c_servicelevel.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-c_servicelevelline"></a>
## `c_servicelevelline` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Service Level Line`
- 사전 Description: Product Revenue Recognition Service Level Line
- 근거 문장: 사전 Name='Service Level Line'; Description='Product Revenue Recognition Service Level Line'; 주요 열 근거 부족; FK cservicelevel_line; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cservicelevel_line` | `c_servicelevelline.(c_servicelevel_id)` → `c_servicelevel.(c_servicelevel_id)` | Service Level |

<a id="t-c_subacct"></a>
## `c_subacct` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Sub Account`
- 사전 Description: Sub account for Element Value
- 근거 문장: 사전 Name='Sub Account'; Description='Sub account for Element Value'; 주요 열 근거 부족; FK celementvalue_csubacct; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `celementvalue_csubacct` | `c_subacct.(c_elementvalue_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |

<a id="t-c_subscription"></a>
## `c_subscription` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Subscription`
- 사전 Description: Subscription of a Business Partner of a Product to renew
- 근거 문장: 사전 Name='Subscription'; Description='Subscription of a Business Partner of a Product to renew'; 주요 열 c_bpartner_id, m_product_id, c_subscriptiontype_id, startdate; FK cbpartner_csubscription, csubscrtype_csubscription; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `m_product_id` | Product | `numeric(10,0)` |
| `c_subscriptiontype_id` | Subscription Type | `numeric(10,0)` |
| `startdate` | Start Date | `timestamp without time zone` |
| `paiduntildate` | Paid Until | `timestamp without time zone` |
| `isdue` | Due | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cbpartner_csubscription` | `c_subscription.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `csubscrtype_csubscription` | `c_subscription.(c_subscriptiontype_id)` → `c_subscriptiontype.(c_subscriptiontype_id)` | Subscription Type |
| outgoing | `mproduct_csubscription` | `c_subscription.(m_product_id)` → `m_product.(m_product_id)` | Product |
| incoming | `csubcription_csubscrdelivery` | `c_subscription_delivery.(c_subscription_id)` → `c_subscription.(c_subscription_id)` | Subscription Delivery |

검토 후보: 거래처·연락처·주소 (규칙 점수 5); 상품·속성·가격·단위 (규칙 점수 5).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_subscription_delivery"></a>
## `c_subscription_delivery` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Subscription Delivery`
- 사전 Description: Optional Delivery Record for a Subscription
- 근거 문장: 사전 Name='Subscription Delivery'; Description='Optional Delivery Record for a Subscription'; 주요 열 c_subscription_id; FK csubcription_csubscrdelivery; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_subscription_id` | Subscription | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `csubcription_csubscrdelivery` | `c_subscription_delivery.(c_subscription_id)` → `c_subscription.(c_subscription_id)` | Subscription |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_subscriptiontype"></a>
## `c_subscriptiontype` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Subscription Type`
- 사전 Description: Type of subscription
- 근거 문장: 사전 Name='Subscription Type'; Description='Type of subscription'; 주요 열 frequencytype, frequency; FK csubscrtype_csubscription, csubscriptiontype_mproduct; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `frequencytype` | Frequency Type | `character(1)` |
| `frequency` | Frequency | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `csubscrtype_csubscription` | `c_subscription.(c_subscriptiontype_id)` → `c_subscriptiontype.(c_subscriptiontype_id)` | Subscription |
| incoming | `csubscriptiontype_mproduct` | `m_product.(c_subscriptiontype_id)` → `c_subscriptiontype.(c_subscriptiontype_id)` | Product |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_task"></a>
## `c_task` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Standard Task`
- 사전 Description: Standard Project Type Task
- 근거 문장: 사전 Name='Standard Task'; Description='Standard Project Type Task'; 주요 열 c_phase_id, standardqty; FK ctask_cprojecttask, cphase_ctask; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_phase_id` | Standard Phase | `numeric(10,0)` |
| `standardqty` | Standard Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ctask_cprojecttask` | `c_projecttask.(c_task_id)` → `c_task.(c_task_id)` | Project Task |
| outgoing | `cphase_ctask` | `c_task.(c_phase_id)` → `c_phase.(c_phase_id)` | Standard Phase |

<a id="t-c_tax"></a>
## `c_tax` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax`
- 사전 Description: Tax identifier
- 근거 문장: 사전 Name='Tax'; Description='Tax identifier'; 주요 열 rate, c_taxcategory_id, c_taxprovider_id; FK ctax_cinvoicetax, ctax_cordertax; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `rate` | Rate | `numeric` |
| `c_taxcategory_id` | Tax Category | `numeric(10,0)` |
| `c_taxprovider_id` | Tax Provider | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ctax_cinvoicetax` | `c_invoicetax.(c_tax_id)` → `c_tax.(c_tax_id)` | C_InvoiceTax |
| incoming | `ctax_cordertax` | `c_ordertax.(c_tax_id)` → `c_tax.(c_tax_id)` | Order Tax |
| incoming | `ctax_ctaxacct` | `c_tax_acct.(c_tax_id)` → `c_tax.(c_tax_id)` | C_Tax_Acct |
| incoming | `ctax_ctaxdeclline` | `c_taxdeclarationline.(c_tax_id)` → `c_tax.(c_tax_id)` | Tax Declaration Line |

<a id="t-c_tax_acct"></a>
## `c_tax_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_Tax_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_Tax_Acct'; 주요 열 t_due_acct, t_liability_acct, t_credit_acct, t_receivables_acct; FK cacctschema_ctaxacct, vc_tcredit_ctax; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `t_due_acct` | Tax Due | `numeric(10,0)` |
| `t_liability_acct` | Tax Liability | `numeric(10,0)` |
| `t_credit_acct` | Tax Credit | `numeric(10,0)` |
| `t_receivables_acct` | Tax Receivables | `numeric(10,0)` |
| `t_expense_acct` | Tax Expense | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_ctaxacct` | `c_tax_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `vc_tcredit_ctax` | `c_tax_acct.(t_credit_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_tdue_ctax` | `c_tax_acct.(t_due_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_texpense_ctax` | `c_tax_acct.(t_expense_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_tax_trl"></a>
## `c_tax_trl` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Trl`
- 사전 Description: Tax identifier
- 근거 문장: 사전 Name='Tax Trl'; Description='Tax identifier'; 주요 열 근거 부족; FK ctax_ctaxtrl; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ctax_ctaxtrl` | `c_tax_trl.(c_tax_id)` → `c_tax.(c_tax_id)` | Tax |

<a id="t-c_taxbase"></a>
## `c_taxbase` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Base`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tax Base'; 주요 열 근거 부족; FK ctaxbase_ctaxdefinition; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ctaxbase_ctaxdefinition` | `c_taxdefinition.(c_taxbase_id)` → `c_taxbase.(c_taxbase_id)` | Tax Definition |

<a id="t-c_taxcategory"></a>
## `c_taxcategory` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Category`
- 사전 Description: Tax Category
- 근거 문장: 사전 Name='Tax Category'; Description='Tax Category'; 주요 열 근거 부족; FK ctaxcategory_ctax, ctaxcategory_ctaxdefinition; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ctaxcategory_ctax` | `c_tax.(c_taxcategory_id)` → `c_taxcategory.(c_taxcategory_id)` | Tax |
| incoming | `ctaxcategory_ctaxdefinition` | `c_taxdefinition.(c_taxcategory_id)` → `c_taxcategory.(c_taxcategory_id)` | Tax Definition |
| incoming | `ctaxcategory_trl` | `c_taxcategory_trl.(c_taxcategory_id)` → `c_taxcategory.(c_taxcategory_id)` | Tax Category Trl |

<a id="t-c_taxcategory_trl"></a>
## `c_taxcategory_trl` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Category Trl`
- 사전 Description: Tax Category
- 근거 문장: 사전 Name='Tax Category Trl'; Description='Tax Category'; 주요 열 근거 부족; FK ctaxcategory_trl; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ctaxcategory_trl` | `c_taxcategory_trl.(c_taxcategory_id)` → `c_taxcategory.(c_taxcategory_id)` | Tax Category |

<a id="t-c_taxdeclaration"></a>
## `c_taxdeclaration` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Declaration`
- 사전 Description: Define the declaration to the tax authorities
- 근거 문장: 사전 Name='Tax Declaration'; Description='Define the declaration to the tax authorities'; 주요 열 근거 부족; FK ctaxdecl_ctaxdeclacct, ctaxdeclaration_ctaxdeclline; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ctaxdecl_ctaxdeclacct` | `c_taxdeclarationacct.(c_taxdeclaration_id)` → `c_taxdeclaration.(c_taxdeclaration_id)` | Tax Declaration Accounting |
| incoming | `ctaxdeclaration_ctaxdeclline` | `c_taxdeclarationline.(c_taxdeclaration_id)` → `c_taxdeclaration.(c_taxdeclaration_id)` | Tax Declaration Line |

<a id="t-c_taxdeclarationacct"></a>
## `c_taxdeclarationacct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Declaration Accounting`
- 사전 Description: Tax Accounting Reconciliation 
- 근거 문장: 사전 Name='Tax Declaration Accounting'; Description='Tax Accounting Reconciliation '; 주요 열 fact_acct_id, c_acctschema_id; FK cacctschema_ctaxdeclacct, factacct_ctaxdeclacct; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `fact_acct_id` | Accounting Fact | `numeric(10,0)` |
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_ctaxdeclacct` | `c_taxdeclarationacct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `factacct_ctaxdeclacct` | `c_taxdeclarationacct.(fact_acct_id)` → `fact_acct.(fact_acct_id)` | Accounting Fact |

<a id="t-c_taxdeclarationline"></a>
## `c_taxdeclarationline` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Declaration Line`
- 사전 Description: Tax Declaration Document Information
- 근거 문장: 사전 Name='Tax Declaration Line'; Description='Tax Declaration Document Information'; 주요 열 c_taxdeclaration_id, c_tax_id, taxbaseamt, taxamt; FK ctax_ctaxdeclline, ctaxdeclaration_ctaxdeclline; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_taxdeclaration_id` | Tax Declaration | `numeric(10,0)` |
| `c_tax_id` | Tax | `numeric(10,0)` |
| `taxbaseamt` | Tax base Amount | `numeric` |
| `taxamt` | Tax Amount | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ctax_ctaxdeclline` | `c_taxdeclarationline.(c_tax_id)` → `c_tax.(c_tax_id)` | Tax |
| outgoing | `ctaxdeclaration_ctaxdeclline` | `c_taxdeclarationline.(c_taxdeclaration_id)` → `c_taxdeclaration.(c_taxdeclaration_id)` | Tax Declaration |

<a id="t-c_taxdefinition"></a>
## `c_taxdefinition` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Definition`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tax Definition'; 주요 열 c_taxbase_id, c_taxcategory_id, c_taxgroup_id, c_taxtype_id; FK ctax_ctaxdefinition, ctaxbase_ctaxdefinition; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_taxbase_id` | Tax Base | `numeric(10,0)` |
| `c_taxcategory_id` | Tax Category | `numeric(10,0)` |
| `c_taxgroup_id` | Tax Group | `numeric(10,0)` |
| `c_taxtype_id` | Tax Type | `numeric(10,0)` |
| `c_tax_id` | Tax | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ctax_ctaxdefinition` | `c_taxdefinition.(c_tax_id)` → `c_tax.(c_tax_id)` | Tax |
| outgoing | `ctaxbase_ctaxdefinition` | `c_taxdefinition.(c_taxbase_id)` → `c_taxbase.(c_taxbase_id)` | Tax Base |
| outgoing | `ctaxcategory_ctaxdefinition` | `c_taxdefinition.(c_taxcategory_id)` → `c_taxcategory.(c_taxcategory_id)` | Tax Category |
| outgoing | `ctaxgroup_ctaxdefinition` | `c_taxdefinition.(c_taxgroup_id)` → `c_taxgroup.(c_taxgroup_id)` | Tax Group |

<a id="t-c_taxgroup"></a>
## `c_taxgroup` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Group`
- 사전 Description: Tax Group
- 근거 문장: 사전 Name='Tax Group'; Description='Tax Group'; 주요 열 근거 부족; FK ctaxgroup_ctaxdefinition; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ctaxgroup_ctaxdefinition` | `c_taxdefinition.(c_taxgroup_id)` → `c_taxgroup.(c_taxgroup_id)` | Tax Definition |

<a id="t-c_taxpostal"></a>
## `c_taxpostal` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax ZIP`
- 사전 Description: Tax Postal/ZIP
- 근거 문장: 사전 Name='Tax ZIP'; Description='Tax Postal/ZIP'; 주요 열 c_tax_id; FK ctax_ctaxpostal; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_tax_id` | Tax | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ctax_ctaxpostal` | `c_taxpostal.(c_tax_id)` → `c_tax.(c_tax_id)` | Tax |

<a id="t-c_taxprovider"></a>
## `c_taxprovider` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Provider`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tax Provider'; 주요 열 c_taxprovidercfg_id; FK ctaxprovider_cinvoicetax, ctaxprovider_cordertax; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_taxprovidercfg_id` | Tax Provider Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ctaxprovider_cinvoicetax` | `c_invoicetax.(c_taxprovider_id)` → `c_taxprovider.(c_taxprovider_id)` | C_InvoiceTax |
| incoming | `ctaxprovider_cordertax` | `c_ordertax.(c_taxprovider_id)` → `c_taxprovider.(c_taxprovider_id)` | Order Tax |
| incoming | `ctaxprovider_ctax` | `c_tax.(c_taxprovider_id)` → `c_taxprovider.(c_taxprovider_id)` | Tax |
| incoming | `ctaxprovider_mrmatax` | `m_rmatax.(c_taxprovider_id)` → `c_taxprovider.(c_taxprovider_id)` | RMA Tax |

<a id="t-c_taxprovidercfg"></a>
## `c_taxprovidercfg` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Provider Configuration`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tax Provider Configuration'; 주요 열 근거 부족; FK ctaxprovidercfg_ctaxprovider; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ctaxprovidercfg_ctaxprovider` | `c_taxprovider.(c_taxprovidercfg_id)` → `c_taxprovidercfg.(c_taxprovidercfg_id)` | Tax Provider |

<a id="t-c_taxtype"></a>
## `c_taxtype` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Tax Type`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Tax Type'; 주요 열 근거 부족; FK ctaxtype_ctaxdefinition; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ctaxtype_ctaxdefinition` | `c_taxdefinition.(c_taxtype_id)` → `c_taxtype.(c_taxtype_id)` | Tax Definition |

<a id="t-c_uom"></a>
## `c_uom` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `UOM`
- 사전 Description: Unit of Measure
- 근거 문장: 사전 Name='UOM'; Description='Unit of Measure'; 주요 열 uomsymbol; FK c_uom_m_product_po, c_uomconversionto; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `uomsymbol` | Symbol | `character varying(10)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_uom_m_product_po` | `m_product_po.(c_uom_id)` → `c_uom.(c_uom_id)` | Product Purchasing |
| incoming | `c_uomconversionto` | `c_uom_conversion.(c_uom_to_id)` → `c_uom.(c_uom_id)` | UOM Conversion |
| incoming | `cuom_cuomconversion` | `c_uom_conversion.(c_uom_id)` → `c_uom.(c_uom_id)` | UOM Conversion |
| incoming | `cuom_cuomtrl` | `c_uom_trl.(c_uom_id)` → `c_uom.(c_uom_id)` | UOM Trl |

<a id="t-c_uom_conversion"></a>
## `c_uom_conversion` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `UOM Conversion`
- 사전 Description: Unit of Measure Conversion
- 근거 문장: 사전 Name='UOM Conversion'; Description='Unit of Measure Conversion'; 주요 열 c_uom_id, c_uom_to_id, multiplyrate, m_product_id; FK c_uomconversionto, cuom_cuomconversion; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_uom_id` | UOM | `numeric(10,0)` |
| `c_uom_to_id` | UoM To | `numeric(10,0)` |
| `multiplyrate` | Multiply Rate | `numeric` |
| `m_product_id` | Product | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `c_uomconversionto` | `c_uom_conversion.(c_uom_to_id)` → `c_uom.(c_uom_id)` | UOM |
| outgoing | `cuom_cuomconversion` | `c_uom_conversion.(c_uom_id)` → `c_uom.(c_uom_id)` | UOM |
| outgoing | `mproduct_cuomconversion` | `c_uom_conversion.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-c_uom_trl"></a>
## `c_uom_trl` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `UOM Trl`
- 사전 Description: Unit of Measure
- 근거 문장: 사전 Name='UOM Trl'; Description='Unit of Measure'; 주요 열 uomsymbol; FK cuom_cuomtrl; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `uomsymbol` | Symbol | `character varying(10)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cuom_cuomtrl` | `c_uom_trl.(c_uom_id)` → `c_uom.(c_uom_id)` | UOM |

<a id="t-c_userremuneration"></a>
## `c_userremuneration` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Employee Remuneration`
- 사전 Description: Employee Wage or Salary Overwrite
- 근거 문장: 사전 Name='Employee Remuneration'; Description='Employee Wage or Salary Overwrite'; 주요 열 ad_user_id, c_remuneration_id, validfrom, validto; FK aduser_cuserremuneration, cremuneration_cuserrem; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `c_remuneration_id` | Remuneration | `numeric(10,0)` |
| `validfrom` | Valid from | `timestamp without time zone` |
| `validto` | Valid to | `timestamp without time zone` |
| `grossramt` | Gross Amount | `numeric` |
| `grossrcost` | Gross Cost | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_cuserremuneration` | `c_userremuneration.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `cremuneration_cuserrem` | `c_userremuneration.(c_remuneration_id)` → `c_remuneration.(c_remuneration_id)` | Remuneration |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-c_validcombination"></a>
## `c_validcombination` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Combination`
- 사전 Description: Valid Account Combination
- 근거 문장: 사전 Name='Combination'; Description='Valid Account Combination'; 주요 열 c_acctschema_id, account_id, c_subacct_id; FK aaccumdepreciation_aassetacct, aaccumdepreciation_aassetgroup; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `account_id` | Account | `numeric(10,0)` |
| `c_subacct_id` | Sub Account | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `aaccumdepreciation_aassetacct` | `a_asset_acct.(a_accumdepreciation_acct)` → `c_validcombination.(c_validcombination_id)` | A_Asset_Acct_ID |
| incoming | `aaccumdepreciation_aassetgroup` | `a_asset_group_acct.(a_accumdepreciation_acct)` → `c_validcombination.(c_validcombination_id)` | Asset Group Accounting |
| incoming | `aasset_aassetgroupacct` | `a_asset_group_acct.(a_asset_acct)` → `c_validcombination.(c_validcombination_id)` | Asset Group Accounting |
| incoming | `aassetvc_aassetacct` | `a_asset_acct.(a_asset_acct)` → `c_validcombination.(c_validcombination_id)` | A_Asset_Acct_ID |

<a id="t-c_withholding"></a>
## `c_withholding` — 세금·원천징수

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Withholding`
- 사전 Description: Withholding type defined
- 근거 문장: 사전 Name='Withholding'; Description='Withholding type defined'; 주요 열 istaxwithholding, istaxprorated, ispercentwithholding; FK cwithholding_cbpwithholding, cwithholding_cwithholdingacct; 사전 의미와 열/FK가 세금·원천징수를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istaxwithholding` | Tax withholding | `character(1)` |
| `istaxprorated` | Prorate tax | `character(1)` |
| `ispercentwithholding` | Percent withholding | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cwithholding_cbpwithholding` | `c_bp_withholding.(c_withholding_id)` → `c_withholding.(c_withholding_id)` | C_BP_Withholding |
| incoming | `cwithholding_cwithholdingacct` | `c_withholding_acct.(c_withholding_id)` → `c_withholding.(c_withholding_id)` | C_Withholding_Acct |

<a id="t-c_withholding_acct"></a>
## `c_withholding_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `C_Withholding_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='C_Withholding_Acct'; 주요 열 withholding_acct; FK cacctschema_cwithholdingacct, vc_withholding_cwithholding; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `withholding_acct` | Withholding | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_cwithholdingacct` | `c_withholding_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `vc_withholding_cwithholding` | `c_withholding_acct.(withholding_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-c_year"></a>
## `c_year` — 테넌트·조직·통화·지역·달력 기준

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Year`
- 사전 Description: Calendar Year
- 근거 문장: 사전 Name='Year'; Description='Calendar Year'; 주요 열 c_calendar_id; FK c_year_period, cyear_hrperiod; 사전 의미와 열/FK가 테넌트·조직·통화·지역·달력 기준를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_calendar_id` | Calendar | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `c_year_period` | `c_period.(c_year_id)` → `c_year.(c_year_id)` | Period |
| incoming | `cyear_hrperiod` | `hr_period.(c_year_id)` → `c_year.(c_year_id)` | Payroll Period |
| outgoing | `c_calendar_year` | `c_year.(c_calendar_id)` → `c_calendar.(c_calendar_id)` | Calendar |

<a id="t-cm_accesscontainer"></a>
## `cm_accesscontainer` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Access Container`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Access Container'; 주요 열 근거 부족; FK cmaccessprofile_cmacccontainer; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmaccessprofile_cmacccontainer` | `cm_accesscontainer.(cm_accessprofile_id)` → `cm_accessprofile.(cm_accessprofile_id)` | Web Access Profile |

<a id="t-cm_accesslistbpgroup"></a>
## `cm_accesslistbpgroup` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Access BP Group`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Access BP Group'; 주요 열 근거 부족; FK cmaccessprofile_cmalbpgroup; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmaccessprofile_cmalbpgroup` | `cm_accesslistbpgroup.(cm_accessprofile_id)` → `cm_accessprofile.(cm_accessprofile_id)` | Web Access Profile |

<a id="t-cm_accesslistrole"></a>
## `cm_accesslistrole` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Access Role`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Access Role'; 주요 열 근거 부족; FK adrole_cmalistrole, cmaccessprofile_cmalistrole; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_cmalistrole` | `cm_accesslistrole.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |
| outgoing | `cmaccessprofile_cmalistrole` | `cm_accesslistrole.(cm_accessprofile_id)` → `cm_accessprofile.(cm_accessprofile_id)` | Web Access Profile |

<a id="t-cm_accessmedia"></a>
## `cm_accessmedia` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Access Media`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Access Media'; 주요 열 근거 부족; FK cmaccessprofile_cmaccessmedia; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmaccessprofile_cmaccessmedia` | `cm_accessmedia.(cm_accessprofile_id)` → `cm_accessprofile.(cm_accessprofile_id)` | Web Access Profile |

<a id="t-cm_accessnewschannel"></a>
## `cm_accessnewschannel` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Access NewsChannel`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Access NewsChannel'; 주요 열 근거 부족; FK cmaccesprofile_cmanewschannel; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmaccesprofile_cmanewschannel` | `cm_accessnewschannel.(cm_accessprofile_id)` → `cm_accessprofile.(cm_accessprofile_id)` | Web Access Profile |

<a id="t-cm_accessprofile"></a>
## `cm_accessprofile` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Access Profile`
- 사전 Description: Web Access Profile
- 근거 문장: 사전 Name='Web Access Profile'; Description='Web Access Profile'; 주요 열 근거 부족; FK cmaccesprofile_cmanewschannel, cmaccessprofile_cmacccontainer; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmaccesprofile_cmanewschannel` | `cm_accessnewschannel.(cm_accessprofile_id)` → `cm_accessprofile.(cm_accessprofile_id)` | Web Access NewsChannel |
| incoming | `cmaccessprofile_cmacccontainer` | `cm_accesscontainer.(cm_accessprofile_id)` → `cm_accessprofile.(cm_accessprofile_id)` | Web Access Container |
| incoming | `cmaccessprofile_cmaccessmedia` | `cm_accessmedia.(cm_accessprofile_id)` → `cm_accessprofile.(cm_accessprofile_id)` | Web Access Media |
| incoming | `cmaccessprofile_cmaccessstage` | `cm_accessstage.(cm_accessprofile_id)` → `cm_accessprofile.(cm_accessprofile_id)` | Web Access Stage |

<a id="t-cm_accessstage"></a>
## `cm_accessstage` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Access Stage`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Access Stage'; 주요 열 근거 부족; FK cmaccessprofile_cmaccessstage; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmaccessprofile_cmaccessstage` | `cm_accessstage.(cm_accessprofile_id)` → `cm_accessprofile.(cm_accessprofile_id)` | Web Access Profile |

<a id="t-cm_ad"></a>
## `cm_ad` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Advertisement`
- 사전 Description: An Advertisement is something like a banner
- 근거 문장: 사전 Name='Advertisement'; Description='An Advertisement is something like a banner'; 주요 열 cm_ad_cat_id, cm_media_id, targeturl, target_frame; FK cmadcat_cmad, cmmedia_cmad; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_ad_cat_id` | Advertisement Category | `numeric(10,0)` |
| `cm_media_id` | Media Item | `numeric(10,0)` |
| `targeturl` | Target URL | `character varying(120)` |
| `target_frame` | Target Frame | `character varying(20)` |
| `actualclick` | Actual Click Count | `numeric(10,0)` |
| `maxclick` | Max Click Count | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmadcat_cmad` | `cm_ad.(cm_ad_cat_id)` → `cm_ad_cat.(cm_ad_cat_id)` | Advertisement Category |
| outgoing | `cmmedia_cmad` | `cm_ad.(cm_media_id)` → `cm_media.(cm_media_id)` | Media Item |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_ad_cat"></a>
## `cm_ad_cat` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Advertisement Category`
- 사전 Description: Advertisement Categories define rotations and ad blocks
- 근거 문장: 사전 Name='Advertisement Category'; Description='Advertisement Categories define rotations and ad blocks'; 주요 열 cm_webproject_id; FK cmadcat_cmad, cmwebproject_cmadcat; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_webproject_id` | Web Project | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmadcat_cmad` | `cm_ad.(cm_ad_cat_id)` → `cm_ad_cat.(cm_ad_cat_id)` | Advertisement |
| outgoing | `cmwebproject_cmadcat` | `cm_ad_cat.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Web Project |
| incoming | `cmadcat_cmtemplateadcat` | `cm_template_ad_cat.(cm_ad_cat_id)` → `cm_ad_cat.(cm_ad_cat_id)` | Template Advertising Category |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_broadcastserver"></a>
## `cm_broadcastserver` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Broadcast Server`
- 사전 Description: Web Broadcast Server
- 근거 문장: 사전 Name='Broadcast Server'; Description='Web Broadcast Server'; 주요 열 ip_address, lastsynchronized, cm_webproject_id; FK cmwebproject_cmbroadcastserver, cmbroadcastserver_cmwebalog; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ip_address` | IP Address | `character varying(20)` |
| `lastsynchronized` | Last Synchronized | `timestamp without time zone` |
| `cm_webproject_id` | Web Project | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmwebproject_cmbroadcastserver` | `cm_broadcastserver.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Web Project |
| incoming | `cmbroadcastserver_cmwebalog` | `cm_webaccesslog.(cm_broadcastserver_id)` → `cm_broadcastserver.(cm_broadcastserver_id)` | Web Access Log |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_chat"></a>
## `cm_chat` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Chat`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Chat'; 주요 열 ad_table_id, record_id, confidentialtype, cm_chattype_id; FK adtable_cmchat, cmchattype_cmchat; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `record_id` | Record ID | `numeric(10,0)` |
| `confidentialtype` | Confidentiality | `character(1)` |
| `cm_chattype_id` | Chat Type | `numeric(10,0)` |
| `moderationtype` | Moderation Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_cmchat` | `cm_chat.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `cmchattype_cmchat` | `cm_chat.(cm_chattype_id)` → `cm_chattype.(cm_chattype_id)` | Chat Type |
| incoming | `cmchat_chchatentry` | `cm_chatentry.(cm_chat_id)` → `cm_chat.(cm_chat_id)` | Chat Entry |
| incoming | `cmchat_cmchatupdate` | `cm_chatupdate.(cm_chat_id)` → `cm_chat.(cm_chat_id)` | Chat Update |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_chatentry"></a>
## `cm_chatentry` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Chat Entry`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Chat Entry'; 주요 열 cm_chat_id, confidentialtype, characterdata, cm_chatentryparent_id; FK aduser_cmchatentry, cmchat_chchatentry; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_chat_id` | Chat | `numeric(10,0)` |
| `confidentialtype` | Confidentiality | `character(1)` |
| `characterdata` | Character Data | `text` |
| `cm_chatentryparent_id` | Chat Entry Parent | `numeric(10,0)` |
| `cm_chatentrygrandparent_id` | Chat Entry Grandparent | `numeric(10,0)` |
| `chatentrytype` | Chat Entry Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_cmchatentry` | `cm_chatentry.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `cmchat_chchatentry` | `cm_chatentry.(cm_chat_id)` → `cm_chat.(cm_chat_id)` | Chat |
| outgoing | `cmchatentry_grandparent` | `cm_chatentry.(cm_chatentrygrandparent_id)` → `cm_chatentry.(cm_chatentry_id)` | Chat Entry |
| outgoing | `cmentrty_cmentryparent` | `cm_chatentry.(cm_chatentryparent_id)` → `cm_chatentry.(cm_chatentry_id)` | Chat Entry |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_chattype"></a>
## `cm_chattype` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Chat Type`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Chat Type'; 주요 열 ad_table_id, moderationtype; FK cmchattype_cmchat, adtable_cmchattype; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_table_id` | Table | `numeric(10,0)` |
| `moderationtype` | Moderation Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmchattype_cmchat` | `cm_chat.(cm_chattype_id)` → `cm_chattype.(cm_chattype_id)` | Chat |
| outgoing | `adtable_cmchattype` | `cm_chattype.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| incoming | `cmchattype_cmchattypeupdate` | `cm_chattypeupdate.(cm_chattype_id)` → `cm_chattype.(cm_chattype_id)` | Chat Type Update |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_chattypeupdate"></a>
## `cm_chattypeupdate` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Chat Type Update`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Chat Type Update'; 주요 열 isselfservice; FK aduser_cmchattypeupdate, cmchattype_cmchattypeupdate; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isselfservice` | Self-Service | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_cmchattypeupdate` | `cm_chattypeupdate.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `cmchattype_cmchattypeupdate` | `cm_chattypeupdate.(cm_chattype_id)` → `cm_chattype.(cm_chattype_id)` | Chat Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_chatupdate"></a>
## `cm_chatupdate` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Chat Update`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Chat Update'; 주요 열 isselfservice; FK aduser_cmchatupdate, cmchat_cmchatupdate; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isselfservice` | Self-Service | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_cmchatupdate` | `cm_chatupdate.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `cmchat_cmchatupdate` | `cm_chatupdate.(cm_chat_id)` → `cm_chat.(cm_chat_id)` | Chat |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_container"></a>
## `cm_container` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Container`
- 사전 Description: Web Container contains content like images, text etc.
- 근거 문장: 사전 Name='Web Container'; Description='Web Container contains content like images, text etc.'; 주요 열 cm_webproject_id, cm_template_id, containertype, containerlinkurl; FK cmcontainer_cmaccesscontainer, cmcontainer_cmcontainerelement; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_webproject_id` | Web Project | `numeric(10,0)` |
| `cm_template_id` | Template | `numeric(10,0)` |
| `containertype` | Web Container Type | `character(1)` |
| `containerlinkurl` | External Link (URL) | `character varying(60)` |
| `relativeurl` | Relative URL | `character varying(120)` |
| `meta_content` | Meta Content Type | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmcontainer_cmaccesscontainer` | `cm_accesscontainer.(cm_container_id)` → `cm_container.(cm_container_id)` | Web Access Container |
| incoming | `cmcontainer_cmcontainerelement` | `cm_container_element.(cm_container_id)` → `cm_container.(cm_container_id)` | Container Element |
| incoming | `cmcontainer_cmcontainertrl` | `cm_container_trl.(cm_container_id)` → `cm_container.(cm_container_id)` | Web Container Trl |
| incoming | `cmcontainer_cmcontainerttable` | `cm_containerttable.(cm_container_id)` → `cm_container.(cm_container_id)` | Container T.Table |

<a id="t-cm_container_element"></a>
## `cm_container_element` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Container Element`
- 사전 Description: Container element i.e. Headline, Content, Footer etc.
- 근거 문장: 사전 Name='Container Element'; Description='Container element i.e. Headline, Content, Footer etc.'; 주요 열 cm_container_id, contenthtml; FK cmcontainerelement_cmcetrl, cmcontainer_cmcontainerelement; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_container_id` | Web Container | `numeric(10,0)` |
| `contenthtml` | Content HTML | `text` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmcontainerelement_cmcetrl` | `cm_container_element_trl.(cm_container_element_id)` → `cm_container_element.(cm_container_element_id)` | Container Element Trl |
| outgoing | `cmcontainer_cmcontainerelement` | `cm_container_element.(cm_container_id)` → `cm_container.(cm_container_id)` | Web Container |

<a id="t-cm_container_element_trl"></a>
## `cm_container_element_trl` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Container Element Trl`
- 사전 Description: Container element i.e. Headline, Content, Footer etc.
- 근거 문장: 사전 Name='Container Element Trl'; Description='Container element i.e. Headline, Content, Footer etc.'; 주요 열 istranslated, contenthtml; FK adlanguage_cmcontainereletrl, cmcontainerelement_cmcetrl; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istranslated` | Translated | `character(1)` |
| `contenthtml` | Content HTML | `text` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlanguage_cmcontainereletrl` | `cm_container_element_trl.(ad_language)` → `ad_language.(ad_language)` | Language ID |
| outgoing | `cmcontainerelement_cmcetrl` | `cm_container_element_trl.(cm_container_element_id)` → `cm_container_element.(cm_container_element_id)` | Container Element |

검토 후보: 애플리케이션 사전·화면·서식 (규칙 점수 12); 웹 콘텐츠·미디어 (규칙 점수 12).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_container_trl"></a>
## `cm_container_trl` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Container Trl`
- 사전 Description: Web Container contains content like images, text etc.
- 근거 문장: 사전 Name='Web Container Trl'; Description='Web Container contains content like images, text etc.'; 주요 열 structurexml, containerxml; FK cmcontainer_cmcontainertrl; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `structurexml` | Structure XML | `character varying(2000)` |
| `containerxml` | Container XML | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmcontainer_cmcontainertrl` | `cm_container_trl.(cm_container_id)` → `cm_container.(cm_container_id)` | Web Container |

<a id="t-cm_container_url"></a>
## `cm_container_url` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Container URL`
- 사전 Description: Contains info on used URLs
- 근거 문장: 사전 Name='Container URL'; Description='Contains info on used URLs'; 주요 열 cm_container_id; FK cmcontainer_cmcontainerurl; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_container_id` | Web Container | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmcontainer_cmcontainerurl` | `cm_container_url.(cm_container_id)` → `cm_container.(cm_container_id)` | Web Container |

<a id="t-cm_containerttable"></a>
## `cm_containerttable` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Container T.Table`
- 사전 Description: Container Template Table
- 근거 문장: 사전 Name='Container T.Table'; Description='Container Template Table'; 주요 열 cm_container_id, cm_templatetable_id; FK cmcontainer_cmcontainerttable, cmttable_cmcontainertable; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_container_id` | Web Container | `numeric(10,0)` |
| `cm_templatetable_id` | Template Table | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmcontainer_cmcontainerttable` | `cm_containerttable.(cm_container_id)` → `cm_container.(cm_container_id)` | Web Container |
| outgoing | `cmttable_cmcontainertable` | `cm_containerttable.(cm_templatetable_id)` → `cm_templatetable.(cm_templatetable_id)` | Template Table |

<a id="t-cm_cstage"></a>
## `cm_cstage` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Container Stage`
- 사전 Description: Container Stage contains the staging content like images, text etc.
- 근거 문장: 사전 Name='Web Container Stage'; Description='Container Stage contains the staging content like images, text etc.'; 주요 열 cm_webproject_id, cm_template_id, containertype, containerlinkurl; FK cmcstage_cmcstageelement, cmcstage_cmcstagetrl; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_webproject_id` | Web Project | `numeric(10,0)` |
| `cm_template_id` | Template | `numeric(10,0)` |
| `containertype` | Web Container Type | `character(1)` |
| `containerlinkurl` | External Link (URL) | `character varying(60)` |
| `relativeurl` | Relative URL | `character varying(120)` |
| `meta_content` | Meta Content Type | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmcstage_cmcstageelement` | `cm_cstage_element.(cm_cstage_id)` → `cm_cstage.(cm_cstage_id)` | Container Stage Element |
| incoming | `cmcstage_cmcstagetrl` | `cm_cstage_trl.(cm_cstage_id)` → `cm_cstage.(cm_cstage_id)` | Web Container Stage Trl |
| incoming | `cmstage_cmcstagettable` | `cm_cstagettable.(cm_cstage_id)` → `cm_cstage.(cm_cstage_id)` | Stage T.Table |
| outgoing | `cmcstage_cmcstagelink` | `cm_cstage.(cm_cstagelink_id)` → `cm_cstage.(cm_cstage_id)` | Web Container Stage |

<a id="t-cm_cstage_element"></a>
## `cm_cstage_element` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Container Stage Element`
- 사전 Description: Container element i.e. Headline, Content, Footer etc.
- 근거 문장: 사전 Name='Container Stage Element'; Description='Container element i.e. Headline, Content, Footer etc.'; 주요 열 cm_cstage_id, contenthtml; FK cmcstageelement_cmcsetrl, cmcstage_cmcstageelement; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_cstage_id` | Web Container Stage | `numeric(10,0)` |
| `contenthtml` | Content HTML | `text` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmcstageelement_cmcsetrl` | `cm_cstage_element_trl.(cm_cstage_element_id)` → `cm_cstage_element.(cm_cstage_element_id)` | Container Stage Element Trl |
| outgoing | `cmcstage_cmcstageelement` | `cm_cstage_element.(cm_cstage_id)` → `cm_cstage.(cm_cstage_id)` | Web Container Stage |

<a id="t-cm_cstage_element_trl"></a>
## `cm_cstage_element_trl` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Container Stage Element Trl`
- 사전 Description: Container element i.e. Headline, Content, Footer etc.
- 근거 문장: 사전 Name='Container Stage Element Trl'; Description='Container element i.e. Headline, Content, Footer etc.'; 주요 열 istranslated, contenthtml; FK adlanguage_cmcstageeletrl, cmcstageelement_cmcsetrl; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istranslated` | Translated | `character(1)` |
| `contenthtml` | Content HTML | `text` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlanguage_cmcstageeletrl` | `cm_cstage_element_trl.(ad_language)` → `ad_language.(ad_language)` | Language ID |
| outgoing | `cmcstageelement_cmcsetrl` | `cm_cstage_element_trl.(cm_cstage_element_id)` → `cm_cstage_element.(cm_cstage_element_id)` | Container Stage Element |

검토 후보: 애플리케이션 사전·화면·서식 (규칙 점수 12); 웹 콘텐츠·미디어 (규칙 점수 12).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_cstage_trl"></a>
## `cm_cstage_trl` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Container Stage Trl`
- 사전 Description: Web Container Stage contains the staging content like images, text etc.
- 근거 문장: 사전 Name='Web Container Stage Trl'; Description='Web Container Stage contains the staging content like images, text etc.'; 주요 열 structurexml, containerxml; FK cmcstage_cmcstagetrl; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `structurexml` | Structure XML | `character varying(2000)` |
| `containerxml` | Container XML | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmcstage_cmcstagetrl` | `cm_cstage_trl.(cm_cstage_id)` → `cm_cstage.(cm_cstage_id)` | Web Container Stage |

<a id="t-cm_cstagettable"></a>
## `cm_cstagettable` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Stage T.Table`
- 사전 Description: Containet Stage Template Table
- 근거 문장: 사전 Name='Stage T.Table'; Description='Containet Stage Template Table'; 주요 열 근거 부족; FK cmttable_cmstagettable; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmttable_cmstagettable` | `cm_cstagettable.(cm_templatetable_id)` → `cm_templatetable.(cm_templatetable_id)` | Template Table |

<a id="t-cm_media"></a>
## `cm_media` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Media Item`
- 사전 Description: Contains media content like images, flash movies etc.
- 근거 문장: 사전 Name='Media Item'; Description='Contains media content like images, flash movies etc.'; 주요 열 mediatype, cm_webproject_id, contenttext; FK cmmedia_cmaccessmedia, cmmedia_cmmediadeploy; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `mediatype` | Media Type | `character(3)` |
| `cm_webproject_id` | Web Project | `numeric(10,0)` |
| `contenttext` | Content | `text` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmmedia_cmaccessmedia` | `cm_accessmedia.(cm_media_id)` → `cm_media.(cm_media_id)` | Web Access Media |
| incoming | `cmmedia_cmmediadeploy` | `cm_mediadeploy.(cm_media_id)` → `cm_media.(cm_media_id)` | Media Deploy |
| outgoing | `cmwebproject_cmmedia` | `cm_media.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Web Project |

<a id="t-cm_media_server"></a>
## `cm_media_server` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Media Server`
- 사전 Description: Media Server list to which content should get transfered
- 근거 문장: 사전 Name='Media Server'; Description='Media Server list to which content should get transfered'; 주요 열 cm_webproject_id, url; FK cmmediaserver_cmmediadeploy, cmwebproject_cmmediaserver; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_webproject_id` | Web Project | `numeric(10,0)` |
| `url` | URL | `character varying(120)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmmediaserver_cmmediadeploy` | `cm_mediadeploy.(cm_media_server_id)` → `cm_media_server.(cm_media_server_id)` | Media Deploy |
| outgoing | `cmwebproject_cmmediaserver` | `cm_media_server.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Web Project |

<a id="t-cm_mediadeploy"></a>
## `cm_mediadeploy` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Media Deploy`
- 사전 Description: Media Deployment Log
- 근거 문장: 사전 Name='Media Deploy'; Description='Media Deployment Log'; 주요 열 cm_media_server_id, cm_media_id; FK cmmedia_cmmediadeploy, cmmediaserver_cmmediadeploy; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_media_server_id` | Media Server | `numeric(10,0)` |
| `cm_media_id` | Media Item | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmmedia_cmmediadeploy` | `cm_mediadeploy.(cm_media_id)` → `cm_media.(cm_media_id)` | Media Item |
| outgoing | `cmmediaserver_cmmediadeploy` | `cm_mediadeploy.(cm_media_server_id)` → `cm_media_server.(cm_media_server_id)` | Media Server |

<a id="t-cm_newschannel"></a>
## `cm_newschannel` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `News Channel`
- 사전 Description: News channel for rss feed
- 근거 문장: 사전 Name='News Channel'; Description='News channel for rss feed'; 주요 열 cm_webproject_id; FK cmnewschannel_cmnewsitem, cnmewschannel_cmaccessnewsc; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_webproject_id` | Web Project | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmnewschannel_cmnewsitem` | `cm_newsitem.(cm_newschannel_id)` → `cm_newschannel.(cm_newschannel_id)` | News Item / Article |
| incoming | `cnmewschannel_cmaccessnewsc` | `cm_accessnewschannel.(cm_newschannel_id)` → `cm_newschannel.(cm_newschannel_id)` | Web Access NewsChannel |
| outgoing | `cmwebproject_cmnewschannel` | `cm_newschannel.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Web Project |

<a id="t-cm_newsitem"></a>
## `cm_newsitem` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `News Item / Article`
- 사전 Description: News item or article defines base content
- 근거 문장: 사전 Name='News Item / Article'; Description='News item or article defines base content'; 주요 열 cm_newschannel_id, linkurl, contenthtml; FK cmnewschannel_cmnewsitem; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_newschannel_id` | News Channel | `numeric(10,0)` |
| `linkurl` | Link URL | `character varying(120)` |
| `contenthtml` | Content HTML | `text` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmnewschannel_cmnewsitem` | `cm_newsitem.(cm_newschannel_id)` → `cm_newschannel.(cm_newschannel_id)` | News Channel |

<a id="t-cm_template"></a>
## `cm_template` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Template`
- 사전 Description: Template defines how content is displayed
- 근거 문장: 사전 Name='Template'; Description='Template defines how content is displayed'; 주요 열 cm_webproject_id, isnews, templatexst; FK cmtemplate_cmcontainer, cmtemplate_cmcstage; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_webproject_id` | Web Project | `numeric(10,0)` |
| `isnews` | Uses News | `character(1)` |
| `templatexst` | Template XST | `text` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmtemplate_cmcontainer` | `cm_container.(cm_template_id)` → `cm_template.(cm_template_id)` | Web Container |
| incoming | `cmtemplate_cmcstage` | `cm_cstage.(cm_template_id)` → `cm_template.(cm_template_id)` | Web Container Stage |
| incoming | `cmtemplate_cmtemplateadcat` | `cm_template_ad_cat.(cm_template_id)` → `cm_template.(cm_template_id)` | Template Advertising Category |
| incoming | `cmtemplate_cmttable` | `cm_templatetable.(cm_template_id)` → `cm_template.(cm_template_id)` | Template Table |

<a id="t-cm_template_ad_cat"></a>
## `cm_template_ad_cat` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Template Advertising Category`
- 사전 Description: Get together the Template and the Advertising Category
- 근거 문장: 사전 Name='Template Advertising Category'; Description='Get together the Template and the Advertising Category'; 주요 열 근거 부족; FK cmtemplate_cmtemplateadcat; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmtemplate_cmtemplateadcat` | `cm_template_ad_cat.(cm_template_id)` → `cm_template.(cm_template_id)` | Template |

<a id="t-cm_templatetable"></a>
## `cm_templatetable` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Template Table`
- 사전 Description: CM Template Table Link
- 근거 문장: 사전 Name='Template Table'; Description='CM Template Table Link'; 주요 열 cm_template_id, ad_table_id, whereclause, otherclause; FK cmttable_cmcontainertable, cmttable_cmstagettable; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_template_id` | Template | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `whereclause` | Sql WHERE | `character varying(2000)` |
| `otherclause` | Other SQL Clause | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmttable_cmcontainertable` | `cm_containerttable.(cm_templatetable_id)` → `cm_templatetable.(cm_templatetable_id)` | Container T.Table |
| incoming | `cmttable_cmstagettable` | `cm_cstagettable.(cm_templatetable_id)` → `cm_templatetable.(cm_templatetable_id)` | Stage T.Table |
| outgoing | `adtable_cmtemplatetable` | `cm_templatetable.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `cmtemplate_cmttable` | `cm_templatetable.(cm_template_id)` → `cm_template.(cm_template_id)` | Template |

검토 후보: 애플리케이션 사전·화면·서식 (규칙 점수 14); 웹 콘텐츠·미디어 (규칙 점수 14).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-cm_webaccesslog"></a>
## `cm_webaccesslog` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Access Log`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Access Log'; 주요 열 ad_user_id; FK aduser_cmwebaccesslog; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_cmwebaccesslog` | `cm_webaccesslog.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-cm_webproject"></a>
## `cm_webproject` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Project`
- 사전 Description: A web project is the main data container for Containers, URLs, Ads, Media etc.
- 근거 문장: 사전 Name='Web Project'; Description='A web project is the main data container for Containers, URLs, Ads, Media etc.'; 주요 열 meta_content; FK cmwebproject_cmcontainer, cmwebproject_cmcstage; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `meta_content` | Meta Content Type | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `cmwebproject_cmcontainer` | `cm_container.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Web Container |
| incoming | `cmwebproject_cmcstage` | `cm_cstage.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Web Container Stage |
| incoming | `cmwebproject_cmmedia` | `cm_media.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Media Item |
| incoming | `cmwebproject_cmmediaserver` | `cm_media_server.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Media Server |

<a id="t-cm_webproject_domain"></a>
## `cm_webproject_domain` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `WebProject Domain`
- 사전 Description: Web Project Domain handling
- 근거 문장: 사전 Name='WebProject Domain'; Description='Web Project Domain handling'; 주요 열 cm_webproject_id, cm_container_id; FK cmcontainer_cmwebprojectdomain, cmwebproject_cmwpdomain; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `cm_webproject_id` | Web Project | `numeric(10,0)` |
| `cm_container_id` | Web Container | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cmcontainer_cmwebprojectdomain` | `cm_webproject_domain.(cm_container_id)` → `cm_container.(cm_container_id)` | Web Container |
| outgoing | `cmwebproject_cmwpdomain` | `cm_webproject_domain.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Web Project |

<a id="t-cm_wikitoken"></a>
## `cm_wikitoken` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Wiki Token`
- 사전 Description: Wiki Token
- 근거 문장: 사전 Name='Wiki Token'; Description='Wiki Token'; 주요 열 tokentype, selectclause, ad_table_id, whereclause; FK adtable_cmwikitoken; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `tokentype` | Token Type | `character(1)` |
| `selectclause` | Sql SELECT | `character varying(2000)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `whereclause` | Sql WHERE | `character varying(2000)` |
| `macro` | Macro | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_cmwikitoken` | `cm_wikitoken.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-dbreplicasyncverifier"></a>
## `dbreplicasyncverifier` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 lastupdate; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `lastupdate` | 미지정 | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-dd_networkdistribution"></a>
## `dd_networkdistribution` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Network Distribution`
- 사전 Description: Network Distribution
- 근거 문장: 사전 Name='Network Distribution'; Description='Network Distribution'; 주요 열 근거 부족; FK ddnetworkdistribution_ddnetwor; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ddnetworkdistribution_ddnetwor` | `dd_networkdistributionline.(dd_networkdistribution_id)` → `dd_networkdistribution.(dd_networkdistribution_id)` | Network Distribution Line |

<a id="t-dd_networkdistributionline"></a>
## `dd_networkdistributionline` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Network Distribution Line`
- 사전 Description: Network Distribution Line
- 근거 문장: 사전 Name='Network Distribution Line'; Description='Network Distribution Line'; 주요 열 m_shipper_id, dd_networkdistribution_id; FK ddnetworkdistribution_ddnetwor, mshipper_ddnetworkdistribution; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shipper_id` | Shipper | `numeric(10,0)` |
| `dd_networkdistribution_id` | Network Distribution | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ddnetworkdistribution_ddnetwor` | `dd_networkdistributionline.(dd_networkdistribution_id)` → `dd_networkdistribution.(dd_networkdistribution_id)` | Network Distribution |
| outgoing | `mshipper_ddnetworkdistribution` | `dd_networkdistributionline.(m_shipper_id)` → `m_shipper.(m_shipper_id)` | Shipper |

<a id="t-dd_order"></a>
## `dd_order` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Distribution Order`
- 사전 Description: Distribution Order
- 근거 문장: 사전 Name='Distribution Order'; Description='Distribution Order'; 주요 열 documentno, ad_orgtrx_id, ad_user_id, c_activity_id; FK adorgtrx_ddorder, aduser_ddorder; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `documentno` | Document No | `character varying(30)` |
| `ad_orgtrx_id` | Trx Organization | `numeric(10,0)` |
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `c_activity_id` | Activity | `numeric(10,0)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `c_bpartner_location_id` | Partner Location | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adorgtrx_ddorder` | `dd_order.(ad_orgtrx_id)` → `ad_org.(ad_org_id)` | Organization |
| outgoing | `aduser_ddorder` | `dd_order.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `cactivity_ddorder` | `dd_order.(c_activity_id)` → `c_activity.(c_activity_id)` | Activity |
| outgoing | `cbpartner_ddorder` | `dd_order.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |

검토 후보: 출하·입고·반품·배송 (규칙 점수 15); 주문·수주·발주 (규칙 점수 15).
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-dd_orderline"></a>
## `dd_orderline` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Distribution Order Line`
- 사전 Description: Distribution Order Line
- 근거 문장: 사전 Name='Distribution Order Line'; Description='Distribution Order Line'; 주요 열 qtyintransit, qtyordered, dd_order_id, confirmedqty; FK ddorderline_mmovementline, ddorder_ddorderline; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `qtyintransit` | Qty In Transit | `numeric` |
| `qtyordered` | Ordered Quantity | `numeric` |
| `dd_order_id` | Distribution Order | `numeric(10,0)` |
| `confirmedqty` | Confirmed Quantity | `numeric` |
| `freightamt` | Freight Amount | `numeric` |
| `m_locatorto_id` | Locator To | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ddorderline_mmovementline` | `m_movementline.(dd_orderline_id)` → `dd_orderline.(dd_orderline_id)` | Move Line |
| outgoing | `ddorder_ddorderline` | `dd_orderline.(dd_order_id)` → `dd_order.(dd_order_id)` | Distribution Order |
| outgoing | `mshipper_ddorderline` | `dd_orderline.(m_shipper_id)` → `m_shipper.(m_shipper_id)` | Shipper |

<a id="t-exp_format"></a>
## `exp_format` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Export Format`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Export Format'; 주요 열 testimportmodel, processing, testexportmodel; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `export`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `testimportmodel` | Test Import Model | `character(1)` |
| `processing` | Process Now | `character(1)` |
| `testexportmodel` | Test Export Model | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-exp_formatline"></a>
## `exp_formatline` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Format Line`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Format Line'; 주요 열 exp_format_id, position, ismandatory, type; FK adcolumn_expformatline, expembeddedformat_expformatlin; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `exp_format_id` | Export Format | `numeric(10,0)` |
| `position` | Position | `numeric(10,0)` |
| `ismandatory` | Mandatory | `character(1)` |
| `type` | Type | `character(1)` |
| `ad_column_id` | Column | `numeric(10,0)` |
| `exp_embeddedformat_id` | Embedded Format | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adcolumn_expformatline` | `exp_formatline.(ad_column_id)` → `ad_column.(ad_column_id)` | Column |
| outgoing | `expembeddedformat_expformatlin` | `exp_formatline.(exp_embeddedformat_id)` → `exp_format.(exp_format_id)` | Export Format |
| outgoing | `expformat_expformatline` | `exp_formatline.(exp_format_id)` → `exp_format.(exp_format_id)` | Export Format |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-exp_processor"></a>
## `exp_processor` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Export Processor`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Export Processor'; 주요 열 근거 부족; FK expprocessor_adreplicationstra, expprocessortype_expprocessor; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `export`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `expprocessor_adreplicationstra` | `ad_replicationstrategy.(exp_processor_id)` → `exp_processor.(exp_processor_id)` | Replication Strategy |
| outgoing | `expprocessortype_expprocessor` | `exp_processor.(exp_processor_type_id)` → `exp_processor_type.(exp_processor_type_id)` | Export Processor Type |

<a id="t-exp_processor_type"></a>
## `exp_processor_type` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Export Processor Type`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Export Processor Type'; 주요 열 근거 부족; FK expprocessortype_expprocessor; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `export`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `expprocessortype_expprocessor` | `exp_processor.(exp_processor_type_id)` → `exp_processor_type.(exp_processor_type_id)` | Export Processor |

<a id="t-exp_processorparameter"></a>
## `exp_processorparameter` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Processor Parameter`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Processor Parameter'; 주요 열 exp_processor_id, parametervalue; FK expprocessor_expprocessorparam; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `exp_processor_id` | Export Processor | `numeric(10,0)` |
| `parametervalue` | Parameter Value | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `expprocessor_expprocessorparam` | `exp_processorparameter.(exp_processor_id)` → `exp_processor.(exp_processor_id)` | Export Processor |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-fact_acct"></a>
## `fact_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Accounting Fact`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Accounting Fact'; 주요 열 c_acctschema_id, account_id, dateacct, gl_budget_id; FK factacct_ctaxdeclacct, factacct_factreconciliation; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `account_id` | Account | `numeric(10,0)` |
| `dateacct` | Account Date | `timestamp without time zone` |
| `gl_budget_id` | Budget | `numeric(10,0)` |
| `postingtype` | Posting Type | `character(1)` |
| `amtsourcedr` | Source Debit | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `factacct_ctaxdeclacct` | `c_taxdeclarationacct.(fact_acct_id)` → `fact_acct.(fact_acct_id)` | Tax Declaration Accounting |
| incoming | `factacct_factreconciliation` | `fact_reconciliation.(fact_acct_id)` → `fact_acct.(fact_acct_id)` | Accounting Fact Reconciliation |
| incoming | `factacct_tinvoicegl` | `t_invoicegl.(fact_acct_id)` → `fact_acct.(fact_acct_id)` | T_InvoiceGL |
| outgoing | `cacctschema_factacct` | `fact_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |

<a id="t-fact_acct_summary"></a>
## `fact_acct_summary` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Accounting Fact summary`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Accounting Fact summary'; 주요 열 account_id, amtacctcr, amtacctdr, c_acctschema_id; FK account_factacctsummary, cacctschema_factacctsummary; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `account_id` | Account | `numeric(10,0)` |
| `amtacctcr` | Accounted Credit | `numeric` |
| `amtacctdr` | Accounted Debit | `numeric` |
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `c_subacct_id` | Sub Account | `numeric(10,0)` |
| `gl_budget_id` | Budget | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `account_factacctsummary` | `fact_acct_summary.(account_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `cacctschema_factacctsummary` | `fact_acct_summary.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `glbudget_factacctsummary` | `fact_acct_summary.(gl_budget_id)` → `gl_budget.(gl_budget_id)` | Budget |
| outgoing | `pareportcube_factacctsummary` | `fact_acct_summary.(pa_reportcube_id)` → `pa_reportcube.(pa_reportcube_id)` | Report Cube |

<a id="t-fact_reconciliation"></a>
## `fact_reconciliation` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Accounting Fact Reconciliation`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Accounting Fact Reconciliation'; 주요 열 fact_acct_id; FK factacct_factreconciliation; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `fact_acct_id` | Accounting Fact | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `factacct_factreconciliation` | `fact_reconciliation.(fact_acct_id)` → `fact_acct.(fact_acct_id)` | Accounting Fact |

<a id="t-gl_budget"></a>
## `gl_budget` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Budget`
- 사전 Description: General Ledger Budget
- 근거 문장: 사전 Name='Budget'; Description='General Ledger Budget'; 주요 열 budgetstatus; FK glbudget_factacct, glbudget_factacctsummary; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `budgetstatus` | Budget Status | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `glbudget_factacct` | `fact_acct.(gl_budget_id)` → `gl_budget.(gl_budget_id)` | Accounting Fact |
| incoming | `glbudget_factacctsummary` | `fact_acct_summary.(gl_budget_id)` → `gl_budget.(gl_budget_id)` | Accounting Fact summary |
| incoming | `glbudget_glbudgetcontrol` | `gl_budgetcontrol.(gl_budget_id)` → `gl_budget.(gl_budget_id)` | Budget Control |
| incoming | `glbudget_gljournal` | `gl_journal.(gl_budget_id)` → `gl_budget.(gl_budget_id)` | Journal |

<a id="t-gl_budgetcontrol"></a>
## `gl_budgetcontrol` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Budget Control`
- 사전 Description: Budget Control
- 근거 문장: 사전 Name='Budget Control'; Description='Budget Control'; 주요 열 c_acctschema_id, gl_budget_id, budgetcontrolscope; FK cacctschema_glbudgetcontrol, glbudget_glbudgetcontrol; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `gl_budget_id` | Budget | `numeric(10,0)` |
| `budgetcontrolscope` | Control Scope | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_glbudgetcontrol` | `gl_budgetcontrol.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `glbudget_glbudgetcontrol` | `gl_budgetcontrol.(gl_budget_id)` → `gl_budget.(gl_budget_id)` | Budget |

<a id="t-gl_category"></a>
## `gl_category` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `GL Category`
- 사전 Description: General Ledger Category
- 근거 문장: 사전 Name='GL Category'; Description='General Ledger Category'; 주요 열 근거 부족; FK glcategory_factacct, glcategory_glcategorytrl; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `glcategory_factacct` | `fact_acct.(gl_category_id)` → `gl_category.(gl_category_id)` | Accounting Fact |
| incoming | `glcategory_glcategorytrl` | `gl_category_trl.(gl_category_id)` → `gl_category.(gl_category_id)` | GL Category Trl |
| incoming | `glcategory_gljournal` | `gl_journal.(gl_category_id)` → `gl_category.(gl_category_id)` | Journal |
| incoming | `glcategory_gljournalbatch` | `gl_journalbatch.(gl_category_id)` → `gl_category.(gl_category_id)` | Journal Batch |

<a id="t-gl_category_trl"></a>
## `gl_category_trl` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `GL Category Trl`
- 사전 Description: General Ledger Category
- 근거 문장: 사전 Name='GL Category Trl'; Description='General Ledger Category'; 주요 열 근거 부족; FK glcategory_glcategorytrl; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `glcategory_glcategorytrl` | `gl_category_trl.(gl_category_id)` → `gl_category.(gl_category_id)` | GL Category |

<a id="t-gl_distribution"></a>
## `gl_distribution` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `GL Distribution`
- 사전 Description: General Ledger Distribution
- 근거 문장: 사전 Name='GL Distribution'; Description='General Ledger Distribution'; 주요 열 postingtype, c_acctschema_id, anyacct, account_id; FK gldistribution_gldistline, cacctschema_gldist; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `postingtype` | Posting Type | `character(1)` |
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `anyacct` | Any Account | `character(1)` |
| `account_id` | Account | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `gldistribution_gldistline` | `gl_distributionline.(gl_distribution_id)` → `gl_distribution.(gl_distribution_id)` | GL Distribution Line |
| outgoing | `cacctschema_gldist` | `gl_distribution.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `cevalueacct_gldist` | `gl_distribution.(account_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `cevalueuser1_gldist` | `gl_distribution.(user1_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |

<a id="t-gl_distributionline"></a>
## `gl_distributionline` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `GL Distribution Line`
- 사전 Description: General Ledger Distribution Line
- 근거 문장: 사전 Name='GL Distribution Line'; Description='General Ledger Distribution Line'; 주요 열 gl_distribution_id, overwriteacct, account_id; FK cevalueacct_gldistline, cevalueuser1_gldistline; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `gl_distribution_id` | GL Distribution | `numeric(10,0)` |
| `overwriteacct` | Overwrite Account | `character(1)` |
| `account_id` | Account | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cevalueacct_gldistline` | `gl_distributionline.(account_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `cevalueuser1_gldistline` | `gl_distributionline.(user1_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `cevalueuser2_gldistline` | `gl_distributionline.(user2_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `gldistribution_gldistline` | `gl_distributionline.(gl_distribution_id)` → `gl_distribution.(gl_distribution_id)` | GL Distribution |

<a id="t-gl_fund"></a>
## `gl_fund` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `GL Fund`
- 사전 Description: General Ledger Funds Control
- 근거 문장: 사전 Name='GL Fund'; Description='General Ledger Funds Control'; 주요 열 c_acctschema_id; FK cacctschema_glfund; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_glfund` | `gl_fund.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |

<a id="t-gl_fundrestriction"></a>
## `gl_fundrestriction` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Fund Restriction`
- 사전 Description: Restriction of Funds
- 근거 문장: 사전 Name='Fund Restriction'; Description='Restriction of Funds'; 주요 열 gl_fund_id, c_elementvalue_id; FK celementvalue_glfundrestr, glfund_glfundrestriction; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `gl_fund_id` | GL Fund | `numeric(10,0)` |
| `c_elementvalue_id` | Account Element | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `celementvalue_glfundrestr` | `gl_fundrestriction.(c_elementvalue_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `glfund_glfundrestriction` | `gl_fundrestriction.(gl_fund_id)` → `gl_fund.(gl_fund_id)` | GL Fund |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-gl_journal"></a>
## `gl_journal` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Journal`
- 사전 Description: General Ledger Journal
- 근거 문장: 사전 Name='Journal'; Description='General Ledger Journal'; 주요 열 c_acctschema_id, postingtype, gl_budget_id, dateacct; FK gljournal_gljournalline, gljournal_ifajournal; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `postingtype` | Posting Type | `character(1)` |
| `gl_budget_id` | Budget | `numeric(10,0)` |
| `dateacct` | Account Date | `timestamp without time zone` |
| `gl_journalbatch_id` | Journal Batch | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `gljournal_gljournalline` | `gl_journalline.(gl_journal_id)` → `gl_journal.(gl_journal_id)` | Journal Line |
| incoming | `gljournal_ifajournal` | `i_fajournal.(gl_journal_id)` → `gl_journal.(gl_journal_id)` | FA Journal |
| incoming | `gljournal_igljournal` | `i_gljournal.(gl_journal_id)` → `gl_journal.(gl_journal_id)` | Import GL Journal |
| outgoing | `c_acctschema_gl_journal` | `gl_journal.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |

<a id="t-gl_journalbatch"></a>
## `gl_journalbatch` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Journal Batch`
- 사전 Description: General Ledger Journal Batch
- 근거 문장: 사전 Name='Journal Batch'; Description='General Ledger Journal Batch'; 주요 열 postingtype, dateacct; FK gljournalbatch_gljournal, gljournalbatch_ifajournal; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `postingtype` | Posting Type | `character(1)` |
| `dateacct` | Account Date | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `gljournalbatch_gljournal` | `gl_journal.(gl_journalbatch_id)` → `gl_journalbatch.(gl_journalbatch_id)` | Journal |
| incoming | `gljournalbatch_ifajournal` | `i_fajournal.(gl_journalbatch_id)` → `gl_journalbatch.(gl_journalbatch_id)` | FA Journal |
| incoming | `gljournalbatch_igljournal` | `i_gljournal.(gl_journalbatch_id)` → `gl_journalbatch.(gl_journalbatch_id)` | Import GL Journal |
| outgoing | `glcategory_gljournalbatch` | `gl_journalbatch.(gl_category_id)` → `gl_category.(gl_category_id)` | GL Category |

<a id="t-gl_journalgenerator"></a>
## `gl_journalgenerator` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `GL Journal Generator`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='GL Journal Generator'; 주요 열 c_elementvalueadjustdr_id, c_elementvalueadjustcr_id, c_acctschema_id, postingtype; FK cacctschema_qssjournalgenerato, celementvalueadjustcr_qssjourn; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_elementvalueadjustdr_id` | Account Adjust DR | `numeric(10,0)` |
| `c_elementvalueadjustcr_id` | Account Adjust CR | `numeric(10,0)` |
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `postingtype` | Posting Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_qssjournalgenerato` | `gl_journalgenerator.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `celementvalueadjustcr_qssjourn` | `gl_journalgenerator.(c_elementvalueadjustcr_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `celementvalueadjustdr_qssjourn` | `gl_journalgenerator.(c_elementvalueadjustdr_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `glcategory_qssjournalgenerator` | `gl_journalgenerator.(gl_category_id)` → `gl_category.(gl_category_id)` | GL Category |

<a id="t-gl_journalgeneratorline"></a>
## `gl_journalgeneratorline` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Generator Line`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Generator Line'; 주요 열 gl_journalgenerator_id, seqno, c_elementvaluedr_id, c_elementvaluecr_id; FK cbpartner_qssjournalgeneratorl, celementvaluecr_qssjournalgene; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `gl_journalgenerator_id` | GL Journal Generator | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `c_elementvaluedr_id` | Account DR | `numeric(10,0)` |
| `c_elementvaluecr_id` | Account CR | `numeric(10,0)` |
| `bpdimensiontype` | Type of BP Dimension | `character(1)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cbpartner_qssjournalgeneratorl` | `gl_journalgeneratorline.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `celementvaluecr_qssjournalgene` | `gl_journalgeneratorline.(c_elementvaluecr_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `celementvaluedr_qssjournalgene` | `gl_journalgeneratorline.(c_elementvaluedr_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `qssjournalgenerator_qssjournal` | `gl_journalgeneratorline.(gl_journalgenerator_id)` → `gl_journalgenerator.(gl_journalgenerator_id)` | GL Journal Generator |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-gl_journalgeneratorsource"></a>
## `gl_journalgeneratorsource` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Generator Source`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Generator Source'; 주요 열 gl_journalgeneratorline_id, c_elementvalue_id, amtmultiplier, roundfactor; FK celementvalue_qssjournalgenera, glcategory_gljournalgenerators; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `gl_journalgeneratorline_id` | Generator Line | `numeric(10,0)` |
| `c_elementvalue_id` | Account Element | `numeric(10,0)` |
| `amtmultiplier` | Multiplier Amount | `numeric` |
| `roundfactor` | Round Factor | `numeric(10,0)` |
| `gl_category_id` | GL Category | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `celementvalue_qssjournalgenera` | `gl_journalgeneratorsource.(c_elementvalue_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `glcategory_gljournalgenerators` | `gl_journalgeneratorsource.(gl_category_id)` → `gl_category.(gl_category_id)` | GL Category |
| outgoing | `qssjournalgeneratorline_qssjou` | `gl_journalgeneratorsource.(gl_journalgeneratorline_id)` → `gl_journalgeneratorline.(gl_journalgeneratorline_id)` | Generator Line |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-gl_journalline"></a>
## `gl_journalline` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Journal Line`
- 사전 Description: General Ledger Journal Line
- 근거 문장: 사전 Name='Journal Line'; Description='General Ledger Journal Line'; 주요 열 gl_journal_id, amtsourcedr, amtsourcecr, dateacct; FK gljourbelline_igljournal, gljournalline_ifajournal; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `gl_journal_id` | Journal | `numeric(10,0)` |
| `amtsourcedr` | Source Debit | `numeric` |
| `amtsourcecr` | Source Credit | `numeric` |
| `dateacct` | Account Date | `timestamp without time zone` |
| `amtacctdr` | Accounted Debit | `numeric` |
| `amtacctcr` | Accounted Credit | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `gljourbelline_igljournal` | `i_gljournal.(gl_journalline_id)` → `gl_journalline.(gl_journalline_id)` | Import GL Journal |
| incoming | `gljournalline_ifajournal` | `i_fajournal.(gl_journalline_id)` → `gl_journalline.(gl_journalline_id)` | FA Journal |
| outgoing | `account_gljournalline` | `gl_journalline.(account_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `aliasvalidcombination_gljourna` | `gl_journalline.(alias_validcombination_id)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-hr_attribute"></a>
## `hr_attribute` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Employee Attribute`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Employee Attribute'; 주요 열 amount, hr_concept_id, hr_department_id, hr_employee_id; FK hrconcept_hrattribute, hrdepartment_hrattribute; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `amount` | Amount | `numeric` |
| `hr_concept_id` | Payroll Concept | `numeric(10,0)` |
| `hr_department_id` | Payroll Department | `numeric(10,0)` |
| `hr_employee_id` | Payroll Employee | `numeric(10,0)` |
| `hr_job_id` | Payroll Job | `numeric(10,0)` |
| `hr_payroll_id` | Payroll | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `hrconcept_hrattribute` | `hr_attribute.(hr_concept_id)` → `hr_concept.(hr_concept_id)` | Payroll Concept |
| outgoing | `hrdepartment_hrattribute` | `hr_attribute.(hr_department_id)` → `hr_department.(hr_department_id)` | Payroll Department |
| outgoing | `hremployee_hrattribute` | `hr_attribute.(hr_employee_id)` → `hr_employee.(hr_employee_id)` | Payroll Employee |
| outgoing | `hrjob_hrattribute` | `hr_attribute.(hr_job_id)` → `hr_job.(hr_job_id)` | Payroll Job |

<a id="t-hr_concept"></a>
## `hr_concept` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Concept`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Concept'; 주요 열 hr_concept_category_id, hr_department_id, hr_job_id, hr_payroll_id; FK hrconcept_hrattribute, hrconcept_hrconceptacct; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_concept_category_id` | Payroll Concept Category | `numeric(10,0)` |
| `hr_department_id` | Payroll Department | `numeric(10,0)` |
| `hr_job_id` | Payroll Job | `numeric(10,0)` |
| `hr_payroll_id` | Payroll | `numeric(10,0)` |
| `isemployee` | Employee | `character(1)` |
| `validfrom` | Valid from | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrconcept_hrattribute` | `hr_attribute.(hr_concept_id)` → `hr_concept.(hr_concept_id)` | Payroll Employee Attribute |
| incoming | `hrconcept_hrconceptacct` | `hr_concept_acct.(hr_concept_id)` → `hr_concept.(hr_concept_id)` | Payroll Concept Account |
| incoming | `hrconcept_hrmovement` | `hr_movement.(hr_concept_id)` → `hr_concept.(hr_concept_id)` | Payroll Movement |
| incoming | `hrconcept_hrpayrollconcept` | `hr_payrollconcept.(hr_concept_id)` → `hr_concept.(hr_concept_id)` | Payroll Concept |

<a id="t-hr_concept_acct"></a>
## `hr_concept_acct` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Concept Account`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Concept Account'; 주요 열 hr_concept_id; FK hrconcept_hrconceptacct; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_concept_id` | Payroll Concept | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `hrconcept_hrconceptacct` | `hr_concept_acct.(hr_concept_id)` → `hr_concept.(hr_concept_id)` | Payroll Concept |

<a id="t-hr_concept_category"></a>
## `hr_concept_category` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Concept Category`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Concept Category'; 주요 열 hr_concept_acct; FK hrconceptcategory_hrconcept, hrconceptcategory_hrmovement; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_concept_acct` | Payroll Concept Account | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrconceptcategory_hrconcept` | `hr_concept.(hr_concept_category_id)` → `hr_concept_category.(hr_concept_category_id)` | Payroll Concept |
| incoming | `hrconceptcategory_hrmovement` | `hr_movement.(hr_concept_category_id)` → `hr_concept_category.(hr_concept_category_id)` | Payroll Movement |

<a id="t-hr_contract"></a>
## `hr_contract` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Contract`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Contract'; 주요 열 validfrom, validto; FK hrcontract_hrpayroll; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `validfrom` | Valid from | `timestamp without time zone` |
| `validto` | Valid to | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrcontract_hrpayroll` | `hr_payroll.(hr_contract_id)` → `hr_contract.(hr_contract_id)` | Payroll |

<a id="t-hr_department"></a>
## `hr_department` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Department`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Department'; 주요 열 근거 부족; FK hrdepartment_hrattribute, hrdepartment_hrconcept; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrdepartment_hrattribute` | `hr_attribute.(hr_department_id)` → `hr_department.(hr_department_id)` | Payroll Employee Attribute |
| incoming | `hrdepartment_hrconcept` | `hr_concept.(hr_department_id)` → `hr_department.(hr_department_id)` | Payroll Concept |
| incoming | `hrdepartment_hremployee` | `hr_employee.(hr_department_id)` → `hr_department.(hr_department_id)` | Payroll Employee |
| incoming | `hrdepartment_hrjob` | `hr_job.(hr_department_id)` → `hr_department.(hr_department_id)` | Payroll Job |

<a id="t-hr_employee"></a>
## `hr_employee` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Employee`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Employee'; 주요 열 hr_department_id, hr_job_id, hr_payroll_id; FK hremployee_hrattribute, hremployee_hrlist; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_department_id` | Payroll Department | `numeric(10,0)` |
| `hr_job_id` | Payroll Job | `numeric(10,0)` |
| `hr_payroll_id` | Payroll | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hremployee_hrattribute` | `hr_attribute.(hr_employee_id)` → `hr_employee.(hr_employee_id)` | Payroll Employee Attribute |
| incoming | `hremployee_hrlist` | `hr_list.(hr_employee_id)` → `hr_employee.(hr_employee_id)` | Payroll List |
| incoming | `hremployee_hrprocess` | `hr_process.(hr_employee_id)` → `hr_employee.(hr_employee_id)` | Payroll Process |
| outgoing | `hrdepartment_hremployee` | `hr_employee.(hr_department_id)` → `hr_department.(hr_department_id)` | Payroll Department |

<a id="t-hr_job"></a>
## `hr_job` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Job`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Job'; 주요 열 hr_department_id; FK hrjob_hrattribute, hrjob_hrconcept; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_department_id` | Payroll Department | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrjob_hrattribute` | `hr_attribute.(hr_job_id)` → `hr_job.(hr_job_id)` | Payroll Employee Attribute |
| incoming | `hrjob_hrconcept` | `hr_concept.(hr_job_id)` → `hr_job.(hr_job_id)` | Payroll Concept |
| incoming | `hrjob_hremployee` | `hr_employee.(hr_job_id)` → `hr_job.(hr_job_id)` | Payroll Employee |
| incoming | `hrjob_hrmovement` | `hr_movement.(hr_job_id)` → `hr_job.(hr_job_id)` | Payroll Movement |

<a id="t-hr_list"></a>
## `hr_list` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll List`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll List'; 주요 열 hr_department_id, hr_employee_id, hr_listtype_id, hr_payroll_id; FK hrlist_hrlistversion, hrlistbase_hrlistversion; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_department_id` | Payroll Department | `numeric(10,0)` |
| `hr_employee_id` | Payroll Employee | `numeric(10,0)` |
| `hr_listtype_id` | Payroll List Type | `numeric(10,0)` |
| `hr_payroll_id` | Payroll | `numeric(10,0)` |
| `isemployee` | Employee | `character(1)` |
| `validfrom` | Valid from | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrlist_hrlistversion` | `hr_listversion.(hr_list_id)` → `hr_list.(hr_list_id)` | Payroll List Version |
| incoming | `hrlistbase_hrlistversion` | `hr_listversion.(hr_listbase_id)` → `hr_list.(hr_list_id)` | Payroll List Version |
| outgoing | `hrdepartment_hrlist` | `hr_list.(hr_department_id)` → `hr_department.(hr_department_id)` | Payroll Department |
| outgoing | `hremployee_hrlist` | `hr_list.(hr_employee_id)` → `hr_employee.(hr_employee_id)` | Payroll Employee |

<a id="t-hr_listline"></a>
## `hr_listline` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll List Line`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll List Line'; 주요 열 hr_listversion_id; FK hrlistversion_hrlistline; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_listversion_id` | Payroll List Version | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `hrlistversion_hrlistline` | `hr_listline.(hr_listversion_id)` → `hr_listversion.(hr_listversion_id)` | Payroll List Version |

<a id="t-hr_listtype"></a>
## `hr_listtype` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll List Type`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll List Type'; 주요 열 근거 부족; FK hrlisttype_hrlist; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrlisttype_hrlist` | `hr_list.(hr_listtype_id)` → `hr_listtype.(hr_listtype_id)` | Payroll List |

<a id="t-hr_listversion"></a>
## `hr_listversion` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll List Version`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll List Version'; 주요 열 hr_listbase_id, hr_list_id, validfrom, validto; FK hrlistversion_hrlistline, hrlist_hrlistversion; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_listbase_id` | Payroll List Base | `numeric(10,0)` |
| `hr_list_id` | Payroll List | `numeric(10,0)` |
| `validfrom` | Valid from | `timestamp without time zone` |
| `validto` | Valid to | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrlistversion_hrlistline` | `hr_listline.(hr_listversion_id)` → `hr_listversion.(hr_listversion_id)` | Payroll List Line |
| outgoing | `hrlist_hrlistversion` | `hr_listversion.(hr_list_id)` → `hr_list.(hr_list_id)` | Payroll List |
| outgoing | `hrlistbase_hrlistversion` | `hr_listversion.(hr_listbase_id)` → `hr_list.(hr_list_id)` | Payroll List |

<a id="t-hr_movement"></a>
## `hr_movement` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Movement`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Movement'; 주요 열 hr_concept_category_id, hr_process_id, hr_concept_id, hr_department_id; FK hrmovement_ihrmovement, hrconcept_hrmovement; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_concept_category_id` | Payroll Concept Category | `numeric(10,0)` |
| `hr_process_id` | Payroll Process | `numeric(10,0)` |
| `hr_concept_id` | Payroll Concept | `numeric(10,0)` |
| `hr_department_id` | Payroll Department | `numeric(10,0)` |
| `hr_job_id` | Payroll Job | `numeric(10,0)` |
| `qty` | Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrmovement_ihrmovement` | `i_hr_movement.(hr_movement_id)` → `hr_movement.(hr_movement_id)` | Payroll Movement Import |
| outgoing | `hrconcept_hrmovement` | `hr_movement.(hr_concept_id)` → `hr_concept.(hr_concept_id)` | Payroll Concept |
| outgoing | `hrconceptcategory_hrmovement` | `hr_movement.(hr_concept_category_id)` → `hr_concept_category.(hr_concept_category_id)` | Payroll Concept Category |
| outgoing | `hrdepartment_hrmovement` | `hr_movement.(hr_department_id)` → `hr_department.(hr_department_id)` | Payroll Department |

<a id="t-hr_payroll"></a>
## `hr_payroll` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll'; 주요 열 hr_contract_id; FK hrpayroll_hrattribute, hrpayroll_hrconcept; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_contract_id` | Payroll Contract | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrpayroll_hrattribute` | `hr_attribute.(hr_payroll_id)` → `hr_payroll.(hr_payroll_id)` | Payroll Employee Attribute |
| incoming | `hrpayroll_hrconcept` | `hr_concept.(hr_payroll_id)` → `hr_payroll.(hr_payroll_id)` | Payroll Concept |
| incoming | `hrpayroll_hremployee` | `hr_employee.(hr_payroll_id)` → `hr_payroll.(hr_payroll_id)` | Payroll Employee |
| incoming | `hrpayroll_hrlist` | `hr_list.(hr_payroll_id)` → `hr_payroll.(hr_payroll_id)` | Payroll List |

<a id="t-hr_payrollconcept"></a>
## `hr_payrollconcept` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Concept`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Concept'; 주요 열 hr_concept_id, hr_payroll_id; FK hrconcept_hrpayrollconcept, hrpayroll_hrpayrollconcept; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_concept_id` | Payroll Concept | `numeric(10,0)` |
| `hr_payroll_id` | Payroll | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `hrconcept_hrpayrollconcept` | `hr_payrollconcept.(hr_concept_id)` → `hr_concept.(hr_concept_id)` | Payroll Concept |
| outgoing | `hrpayroll_hrpayrollconcept` | `hr_payrollconcept.(hr_payroll_id)` → `hr_payroll.(hr_payroll_id)` | Payroll |

<a id="t-hr_period"></a>
## `hr_period` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Period`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Period'; 주요 열 hr_payroll_id, hr_year_id; FK hrperiod_hrprocess, hrpayroll_hrperiod; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_payroll_id` | Payroll | `numeric(10,0)` |
| `hr_year_id` | Payroll Year | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrperiod_hrprocess` | `hr_process.(hr_period_id)` → `hr_period.(hr_period_id)` | Payroll Process |
| outgoing | `hrpayroll_hrperiod` | `hr_period.(hr_payroll_id)` → `hr_payroll.(hr_payroll_id)` | Payroll |
| outgoing | `hryear_hrperiod` | `hr_period.(hr_year_id)` → `hr_year.(hr_year_id)` | Payroll Year |

<a id="t-hr_process"></a>
## `hr_process` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Process`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Process'; 주요 열 hr_job_id, hr_employee_id, hr_department_id, hr_payroll_id; FK hrprocess_hrmovement, hrprocess_ihrmovement; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_job_id` | Payroll Job | `numeric(10,0)` |
| `hr_employee_id` | Payroll Employee | `numeric(10,0)` |
| `hr_department_id` | Payroll Department | `numeric(10,0)` |
| `hr_payroll_id` | Payroll | `numeric(10,0)` |
| `hr_period_id` | Payroll Period | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hrprocess_hrmovement` | `hr_movement.(hr_process_id)` → `hr_process.(hr_process_id)` | Payroll Movement |
| incoming | `hrprocess_ihrmovement` | `i_hr_movement.(hr_process_id)` → `hr_process.(hr_process_id)` | Payroll Movement Import |
| outgoing | `hrdepartment_hrprocess` | `hr_process.(hr_department_id)` → `hr_department.(hr_department_id)` | Payroll Department |
| outgoing | `hremployee_hrprocess` | `hr_process.(hr_employee_id)` → `hr_employee.(hr_employee_id)` | Payroll Employee |

<a id="t-hr_year"></a>
## `hr_year` — 인사·급여

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Year`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Year'; 주요 열 hr_payroll_id, qty; FK hryear_hrperiod, hrpayroll_hryear; 사전 의미와 열/FK가 인사·급여를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `payroll`를 근거로, 구조 근거가 있는 `payroll` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `hr_payroll_id` | Payroll | `numeric(10,0)` |
| `qty` | Quantity | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `hryear_hrperiod` | `hr_period.(hr_year_id)` → `hr_year.(hr_year_id)` | Payroll Period |
| outgoing | `hrpayroll_hryear` | `hr_year.(hr_payroll_id)` → `hr_payroll.(hr_payroll_id)` | Payroll |

<a id="t-i_asset"></a>
## `i_asset` — 자산·감가상각

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Asset`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Asset'; 주요 열 a_accumdepreciation_acct, a_asset_acct, a_asset_cost, a_asset_group_id; FK aassetgroup_iasset, adepreciationtableheader_iasse; 사전 의미와 열/FK가 자산·감가상각를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `a_accumdepreciation_acct` | Accumulated Depreciation Account | `numeric(10,0)` |
| `a_asset_acct` | Asset Acct | `numeric(10,0)` |
| `a_asset_cost` | Asset Cost | `numeric` |
| `a_asset_group_id` | Asset Group | `numeric(10,0)` |
| `a_asset_id` | Asset | `numeric(10,0)` |
| `a_asset_life_current_year` | A_Asset_Life_Current_Year | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aassetgroup_iasset` | `i_asset.(a_asset_group_id)` → `a_asset_group.(a_asset_group_id)` | Asset Group |
| outgoing | `adepreciationtableheader_iasse` | `i_asset.(a_depreciation_table_header_id)` → `a_depreciation_table_header.(a_depreciation_table_header_id)` | A_Depreciation_Table_Header_ID |

<a id="t-i_bankstatement"></a>
## `i_bankstatement` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Bank Statement`
- 사전 Description: Import of the Bank Statement
- 근거 문장: 사전 Name='Import Bank Statement'; Description='Import of the Bank Statement'; 주요 열 i_isimported, i_errormsg, processed, processing; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processed` | Processed | `character(1)` |
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_bpartner"></a>
## `i_bpartner` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Business Partner`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Import Business Partner'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_conversion_rate"></a>
## `i_conversion_rate` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Conversion Rate`
- 사전 Description: Import Currency Conversion Rate
- 근거 문장: 사전 Name='Import Conversion Rate'; Description='Import Currency Conversion Rate'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_elementvalue"></a>
## `i_elementvalue` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Account`
- 사전 Description: Import Account Value
- 근거 문장: 사전 Name='Import Account'; Description='Import Account Value'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_fajournal"></a>
## `i_fajournal` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `FA Journal`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='FA Journal'; 주요 열 c_subacct_id, accountvalue, account_id, acctschemaname; FK account_ifajournal, cacctschema_ifajournal; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_subacct_id` | Sub Account | `numeric(10,0)` |
| `accountvalue` | Account Key | `character varying(80)` |
| `account_id` | Account | `numeric(10,0)` |
| `acctschemaname` | Account Schema Name | `character varying(120)` |
| `amtacctcr` | Accounted Credit | `numeric` |
| `amtacctdr` | Accounted Debit | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `account_ifajournal` | `i_fajournal.(account_id)` → `c_elementvalue.(c_elementvalue_id)` | Account Element |
| outgoing | `cacctschema_ifajournal` | `i_fajournal.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `cvalidcombination_ifajournal` | `i_fajournal.(c_validcombination_id)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `glbudget_ifajournal` | `i_fajournal.(gl_budget_id)` → `gl_budget.(gl_budget_id)` | Budget |

<a id="t-i_fixedasset"></a>
## `i_fixedasset` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Imported Fixed Asset`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Imported Fixed Asset'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `imported`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_gljournal"></a>
## `i_gljournal` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import GL Journal`
- 사전 Description: Import General Ledger Journal
- 근거 문장: 사전 Name='Import GL Journal'; Description='Import General Ledger Journal'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_hr_movement"></a>
## `i_hr_movement` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Payroll Movement Import`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Payroll Movement Import'; 주요 열 processed, i_isimported, i_errormsg, processing; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `processed` | Processed | `character(1)` |
| `i_isimported` | Imported | `character varying(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_inoutlineconfirm"></a>
## `i_inoutlineconfirm` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Ship/Receipt Confirmation Import Line`
- 사전 Description: Material Shipment or Receipt Confirmation Import Line
- 근거 문장: 사전 Name='Ship/Receipt Confirmation Import Line'; Description='Material Shipment or Receipt Confirmation Import Line'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_inventory"></a>
## `i_inventory` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Inventory`
- 사전 Description: Import Inventory Transactions
- 근거 문장: 사전 Name='Import Inventory'; Description='Import Inventory Transactions'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_invoice"></a>
## `i_invoice` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Invoice`
- 사전 Description: Import Invoice
- 근거 문장: 사전 Name='Import Invoice'; Description='Import Invoice'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_movement"></a>
## `i_movement` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `I_Movement_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='I_Movement_ID'; 주요 열 processed, i_isimported, processing, i_errormsg; FK adorgtrx_imovement, aduser_imovement; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `processed` | Processed | `character(1)` |
| `i_isimported` | Imported | `character(1)` |
| `processing` | Process Now | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `productvalue` | Product Key | `character varying(40)` |
| `m_product_id` | Product | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adorgtrx_imovement` | `i_movement.(ad_orgtrx_id)` → `ad_org.(ad_org_id)` | Organization |
| outgoing | `aduser_imovement` | `i_movement.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `cbpartner_imovement` | `i_movement.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `ccampaign_imovement` | `i_movement.(c_campaign_id)` → `c_campaign.(c_campaign_id)` | Campaign |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-i_order"></a>
## `i_order` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Order`
- 사전 Description: Import Orders
- 근거 문장: 사전 Name='Import Order'; Description='Import Orders'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_payment"></a>
## `i_payment` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Payment`
- 사전 Description: Import Payment
- 근거 문장: 사전 Name='Import Payment'; Description='Import Payment'; 주요 열 i_isimported, i_errormsg, processed, creditcardtype; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processed` | Processed | `character(1)` |
| `creditcardtype` | Credit Card | `character(1)` |
| `creditcardnumber` | Number | `character varying(20)` |
| `creditcardvv` | Verification Code | `character varying(4)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_pricelist"></a>
## `i_pricelist` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Price List`
- 사전 Description: Import Price List and Versions
- 근거 문장: 사전 Name='Import Price List'; Description='Import Price List and Versions'; 주요 열 i_errormsg, i_isimported, processed, processing; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `i_isimported` | Imported | `character(1)` |
| `processed` | Processed | `character(1)` |
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_product"></a>
## `i_product` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Product`
- 사전 Description: Import Item or Service
- 근거 문장: 사전 Name='Import Product'; Description='Import Item or Service'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_productplanning"></a>
## `i_productplanning` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Product Planning`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Import Product Planning'; 주요 열 i_errormsg, i_isimported, processed, processing; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `i_isimported` | Imported | `character(1)` |
| `processed` | Processed | `character(1)` |
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-i_reportline"></a>
## `i_reportline` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Report Line Set`
- 사전 Description: Import Report Line Set values
- 근거 문장: 사전 Name='Import Report Line Set'; Description='Import Report Line Set values'; 주요 열 i_isimported, i_errormsg, processing, processed; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `i_isimported` | Imported | `character(1)` |
| `i_errormsg` | Import Error Message | `character varying(2000)` |
| `processing` | Process Now | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-imp_processor"></a>
## `imp_processor` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Processor`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Import Processor'; 주요 열 processing; FK impprocessor_impprocessorlog, impprocessor_impprocessorparam; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `impprocessor_impprocessorlog` | `imp_processorlog.(imp_processor_id)` → `imp_processor.(imp_processor_id)` | Import Processor Log |
| incoming | `impprocessor_impprocessorparam` | `imp_processorparameter.(imp_processor_id)` → `imp_processor.(imp_processor_id)` | Import Processor Parameter |
| outgoing | `impprocessortype_impprocessor` | `imp_processor.(imp_processor_type_id)` → `imp_processor_type.(imp_processor_type_id)` | Import Processor Type |

<a id="t-imp_processor_type"></a>
## `imp_processor_type` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Processor Type`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Import Processor Type'; 주요 열 근거 부족; FK impprocessortype_impprocessor; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `impprocessortype_impprocessor` | `imp_processor.(imp_processor_type_id)` → `imp_processor_type.(imp_processor_type_id)` | Import Processor |

<a id="t-imp_processorlog"></a>
## `imp_processorlog` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Processor Log`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Import Processor Log'; 주요 열 근거 부족; FK impprocessor_impprocessorlog; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `impprocessor_impprocessorlog` | `imp_processorlog.(imp_processor_id)` → `imp_processor.(imp_processor_id)` | Import Processor |

<a id="t-imp_processorparameter"></a>
## `imp_processorparameter` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Import Processor Parameter`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Import Processor Parameter'; 주요 열 근거 부족; FK impprocessor_impprocessorparam; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `import`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `impprocessor_impprocessorparam` | `imp_processorparameter.(imp_processor_id)` → `imp_processor.(imp_processor_id)` | Import Processor |

<a id="t-k_category"></a>
## `k_category` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Knowledge Category`
- 사전 Description: Knowledge Category
- 근거 문장: 사전 Name='Knowledge Category'; Description='Knowledge Category'; 주요 열 근거 부족; FK kcategory_kcategoryvalue, kcategory_kentrycategory; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `kcategory_kcategoryvalue` | `k_categoryvalue.(k_category_id)` → `k_category.(k_category_id)` | Category Value |
| incoming | `kcategory_kentrycategory` | `k_entrycategory.(k_category_id)` → `k_category.(k_category_id)` | K_EntryCategory |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-k_categoryvalue"></a>
## `k_categoryvalue` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Category Value`
- 사전 Description: The value of the category
- 근거 문장: 사전 Name='Category Value'; Description='The value of the category'; 주요 열 k_category_id; FK kcategory_kcategoryvalue, kcategoryvalue_kentrycategory; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `k_category_id` | Knowledge Category | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `kcategory_kcategoryvalue` | `k_categoryvalue.(k_category_id)` → `k_category.(k_category_id)` | Knowledge Category |
| incoming | `kcategoryvalue_kentrycategory` | `k_entrycategory.(k_categoryvalue_id)` → `k_categoryvalue.(k_categoryvalue_id)` | K_EntryCategory |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-k_comment"></a>
## `k_comment` — 지식·분류·문서

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Entry Comment`
- 사전 Description: Knowledge Entry Comment
- 근거 문장: 사전 Name='Entry Comment'; Description='Knowledge Entry Comment'; 주요 열 k_entry_id, textmsg; FK kentry_kcomment; 사전 의미와 열/FK가 지식·분류·문서를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `k_entry_id` | Entry | `numeric(10,0)` |
| `textmsg` | Text Message | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `kentry_kcomment` | `k_comment.(k_entry_id)` → `k_entry.(k_entry_id)` | Entry |

<a id="t-k_entry"></a>
## `k_entry` — 지식·분류·문서

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Entry`
- 사전 Description: Knowledge Entry
- 근거 문장: 사전 Name='Entry'; Description='Knowledge Entry'; 주요 열 k_topic_id, keywords, k_source_id, textmsg; FK kentry_kcomment, ksource_kentry; 사전 의미와 열/FK가 지식·분류·문서를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `k_topic_id` | Knowledge Topic | `numeric(10,0)` |
| `keywords` | Keywords | `character varying(255)` |
| `k_source_id` | Knowledge Source | `numeric(10,0)` |
| `textmsg` | Text Message | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `kentry_kcomment` | `k_comment.(k_entry_id)` → `k_entry.(k_entry_id)` | Entry Comment |
| outgoing | `ksource_kentry` | `k_entry.(k_source_id)` → `k_source.(k_source_id)` | Knowledge Source |
| outgoing | `ktopic_kentry` | `k_entry.(k_topic_id)` → `k_topic.(k_topic_id)` | Knowledge Topic |

<a id="t-k_entrycategory"></a>
## `k_entrycategory` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `K_EntryCategory`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='K_EntryCategory'; 주요 열 k_categoryvalue_id; FK kcategory_kentrycategory, kcategoryvalue_kentrycategory; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `k_categoryvalue_id` | Category Value | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `kcategory_kentrycategory` | `k_entrycategory.(k_category_id)` → `k_category.(k_category_id)` | Knowledge Category |
| outgoing | `kcategoryvalue_kentrycategory` | `k_entrycategory.(k_categoryvalue_id)` → `k_categoryvalue.(k_categoryvalue_id)` | Category Value |
| outgoing | `kentry_kentrycatalog` | `k_entrycategory.(k_entry_id)` → `k_entry.(k_entry_id)` | Entry |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-k_entryrelated"></a>
## `k_entryrelated` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Related Entry`
- 사전 Description: Related Entry for this Enntry
- 근거 문장: 사전 Name='Related Entry'; Description='Related Entry for this Enntry'; 주요 열 근거 부족; FK kentry_kentryrelated, kentry_kentryrelatedid; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `kentry_kentryrelated` | `k_entryrelated.(k_entry_id)` → `k_entry.(k_entry_id)` | Entry |
| outgoing | `kentry_kentryrelatedid` | `k_entryrelated.(k_entryrelated_id)` → `k_entry.(k_entry_id)` | Entry |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-k_index"></a>
## `k_index` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Index`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Index'; 주요 열 keyword, excerpt, ad_table_id, record_id; FK adtable_kindex, cdoctype_kindex; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `keyword` | Keyword | `character varying(255)` |
| `excerpt` | Excerpt | `character varying(2000)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `record_id` | Record ID | `numeric(10,0)` |
| `sourceupdated` | Source Updated | `timestamp without time zone` |
| `cm_webproject_id` | Web Project | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_kindex` | `k_index.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `cdoctype_kindex` | `k_index.(c_doctype_id)` → `c_doctype.(c_doctype_id)` | Document Type |
| outgoing | `cmwebproject_kindex` | `k_index.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Web Project |
| outgoing | `rrequesttype_kindex` | `k_index.(r_requesttype_id)` → `r_requesttype.(r_requesttype_id)` | Request Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-k_indexlog"></a>
## `k_indexlog` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Index Log`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Index Log'; 주요 열 indexquery, indexqueryresult, querysource; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `indexquery` | Index Query | `character varying(255)` |
| `indexqueryresult` | Query Result | `numeric(10,0)` |
| `querysource` | Query Source | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-k_indexstop"></a>
## `k_indexstop` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Index Stop`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Index Stop'; 주요 열 keyword, ismanual, cm_webproject_id, r_requesttype_id; FK cdoctype_kindexstop, cmwebproject_kindexstop; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `keyword` | Keyword | `character varying(255)` |
| `ismanual` | Manual | `character(1)` |
| `cm_webproject_id` | Web Project | `numeric(10,0)` |
| `r_requesttype_id` | Request Type | `numeric(10,0)` |
| `c_doctype_id` | Document Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cdoctype_kindexstop` | `k_indexstop.(c_doctype_id)` → `c_doctype.(c_doctype_id)` | Document Type |
| outgoing | `cmwebproject_kindexstop` | `k_indexstop.(cm_webproject_id)` → `cm_webproject.(cm_webproject_id)` | Web Project |
| outgoing | `rrequesttype_kindexstop` | `k_indexstop.(r_requesttype_id)` → `r_requesttype.(r_requesttype_id)` | Request Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-k_source"></a>
## `k_source` — 지식·분류·문서

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Knowledge Source`
- 사전 Description: Source of a Knowledge Entry
- 근거 문장: 사전 Name='Knowledge Source'; Description='Source of a Knowledge Entry'; 주요 열 근거 부족; FK ksource_kentry; 사전 의미와 열/FK가 지식·분류·문서를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ksource_kentry` | `k_entry.(k_source_id)` → `k_source.(k_source_id)` | Entry |

<a id="t-k_synonym"></a>
## `k_synonym` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Knowledge Synonym`
- 사전 Description: Knowlege Keyword Synonym
- 근거 문장: 사전 Name='Knowledge Synonym'; Description='Knowlege Keyword Synonym'; 주요 열 synonymname, ad_language; FK adlangu_ksynonym; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `synonymname` | Synonym Name | `character varying(60)` |
| `ad_language` | Language | `character varying(6)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlangu_ksynonym` | `k_synonym.(ad_language)` → `ad_language.(ad_language)` | Language ID |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-k_topic"></a>
## `k_topic` — 지식·분류·문서

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Knowledge Topic`
- 사전 Description: Knowledge Topic
- 근거 문장: 사전 Name='Knowledge Topic'; Description='Knowledge Topic'; 주요 열 k_type_id; FK ktopic_kentry, ktype_ktopic; 사전 의미와 열/FK가 지식·분류·문서를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `k_type_id` | Knowledge Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ktopic_kentry` | `k_entry.(k_topic_id)` → `k_topic.(k_topic_id)` | Entry |
| outgoing | `ktype_ktopic` | `k_topic.(k_type_id)` → `k_type.(k_type_id)` | Knowledge Type |

<a id="t-k_type"></a>
## `k_type` — 지식·분류·문서

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Knowledge Type`
- 사전 Description: Knowledge Type
- 근거 문장: 사전 Name='Knowledge Type'; Description='Knowledge Type'; 주요 열 근거 부족; FK ktype_ktopic; 사전 의미와 열/FK가 지식·분류·문서를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ktype_ktopic` | `k_topic.(k_type_id)` → `k_type.(k_type_id)` | Knowledge Topic |

<a id="t-m_attribute"></a>
## `m_attribute` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Attribute`
- 사전 Description: Product Attribute
- 근거 문장: 사전 Name='Attribute'; Description='Product Attribute'; 주요 열 m_attributesearch_id, attributevaluetype, ad_reference_value_id, defaultvalue; FK mattribute_mattributevalue; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_attributesearch_id` | Attribute Search | `numeric(10,0)` |
| `attributevaluetype` | Attribute Value Type | `character(1)` |
| `ad_reference_value_id` | Reference Key | `numeric(10,0)` |
| `defaultvalue` | Default Logic | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mattribute_mattributevalue` | `m_attributevalue.(m_attribute_id)` → `m_attribute.(m_attribute_id)` | Attribute Value |

<a id="t-m_attributeinstance"></a>
## `m_attributeinstance` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_AttributeInstance`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_AttributeInstance'; 주요 열 m_attributevalue_id, valuenumber, valuedate, valuemultipleselection; FK mattribute_mattributeinst, mattributevalue_mattrinst; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_attributevalue_id` | Attribute Value | `numeric(10,0)` |
| `valuenumber` | Value | `numeric` |
| `valuedate` | Value Date | `timestamp without time zone` |
| `valuemultipleselection` | Value Multiple Selection | `character varying(255)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mattribute_mattributeinst` | `m_attributeinstance.(m_attribute_id)` → `m_attribute.(m_attribute_id)` | Attribute |
| outgoing | `mattributevalue_mattrinst` | `m_attributeinstance.(m_attributevalue_id)` → `m_attributevalue.(m_attributevalue_id)` | Attribute Value |
| outgoing | `mattrsetinst__mattrinst` | `m_attributeinstance.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_attributeinstanceline"></a>
## `m_attributeinstanceline` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Attribute Instance Values`
- 사전 Description: Selected attribute values of an attribute instance
- 근거 문장: 사전 Name='Attribute Instance Values'; Description='Selected attribute values of an attribute instance'; 주요 열 line, m_attributevalue_id; FK mattributevalue_mattributeinst; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `line` | Line No | `numeric(10,0)` |
| `m_attributevalue_id` | Attribute Value | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mattributevalue_mattributeinst` | `m_attributeinstanceline.(m_attributevalue_id)` → `m_attributevalue.(m_attributevalue_id)` | Attribute Value |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_attributesearch"></a>
## `m_attributesearch` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Attribute Search`
- 사전 Description: Common Search Attribute 
- 근거 문장: 사전 Name='Attribute Search'; Description='Common Search Attribute '; 주요 열 근거 부족; FK mattributesearch_mattribute; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mattributesearch_mattribute` | `m_attribute.(m_attributesearch_id)` → `m_attributesearch.(m_attributesearch_id)` | Attribute |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_attributeset"></a>
## `m_attributeset` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Attribute Set`
- 사전 Description: Product Attribute Set
- 근거 문장: 사전 Name='Attribute Set'; Description='Product Attribute Set'; 주요 열 m_attributeset_type; FK mattributeset_adtableattributeset, mattributeset_iproduct; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_attributeset_type` | Attribute Set Type | `character varying(3)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mattributeset_adtableattributeset` | `ad_tableattributeset.(m_attributeset_id)` → `m_attributeset.(m_attributeset_id)` | Table Attribute Set |
| incoming | `mattributeset_iproduct` | `i_product.(m_attributeset_id)` → `m_attributeset.(m_attributeset_id)` | Import Product |
| incoming | `mattributeset_masexclude` | `m_attributesetexclude.(m_attributeset_id)` → `m_attributeset.(m_attributeset_id)` | Exclude Attribute Set |
| incoming | `mattributeset_mattribsetinst` | `m_attributesetinstance.(m_attributeset_id)` → `m_attributeset.(m_attributeset_id)` | Attribute Set Instance |

<a id="t-m_attributesetexclude"></a>
## `m_attributesetexclude` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Exclude Attribute Set`
- 사전 Description: Exclude the ability to enter Attribute Sets
- 근거 문장: 사전 Name='Exclude Attribute Set'; Description='Exclude the ability to enter Attribute Sets'; 주요 열 m_attributeset_id; FK mattributeset_masexclude; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_attributeset_id` | Attribute Set | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mattributeset_masexclude` | `m_attributesetexclude.(m_attributeset_id)` → `m_attributeset.(m_attributeset_id)` | Attribute Set |

<a id="t-m_attributesetinstance"></a>
## `m_attributesetinstance` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Attribute Set Instance`
- 사전 Description: Product Attribute Set Instance
- 근거 문장: 사전 Name='Attribute Set Instance'; Description='Product Attribute Set Instance'; 주요 열 m_attributeset_id; FK masi_mbomproduct, masi_mcost; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_attributeset_id` | Attribute Set | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `masi_mbomproduct` | `m_bomproduct.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | BOM Component |
| incoming | `masi_mcost` | `m_cost.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Product Cost |
| incoming | `mattributesetinstance_aassetpr` | `a_asset_product.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Asset Product |
| incoming | `mattrsetinst_mproduct` | `m_product.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Product |

<a id="t-m_attributeuse"></a>
## `m_attributeuse` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_AttributeUse`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_AttributeUse'; 주요 열 seqno, defaultvalue, entitytype; FK entitytype_mattributeuse, mattribute_mattributeuse; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `seqno` | Sequence | `numeric(10,0)` |
| `defaultvalue` | Default Logic | `character varying(2000)` |
| `entitytype` | Entity Type | `character varying(40)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `entitytype_mattributeuse` | `m_attributeuse.(entitytype)` → `ad_entitytype.(entitytype)` | Entity Type |
| outgoing | `mattribute_mattributeuse` | `m_attributeuse.(m_attribute_id)` → `m_attribute.(m_attribute_id)` | Attribute |
| outgoing | `mattributeset_mattributeuse` | `m_attributeuse.(m_attributeset_id)` → `m_attributeset.(m_attributeset_id)` | Attribute Set |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_attributevalue"></a>
## `m_attributevalue` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Attribute Value`
- 사전 Description: Product Attribute Value
- 근거 문장: 사전 Name='Attribute Value'; Description='Product Attribute Value'; 주요 열 m_attribute_id; FK mattribute_mattributevalue; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_attribute_id` | Attribute | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mattribute_mattributevalue` | `m_attributevalue.(m_attribute_id)` → `m_attribute.(m_attribute_id)` | Attribute |

<a id="t-m_bom"></a>
## `m_bom` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `BOM`
- 사전 Description: Bill of Material
- 근거 문장: 사전 Name='BOM'; Description='Bill of Material'; 주요 열 bomtype; FK mbom_mbomproduct; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `bom`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `bomtype` | BOM Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mbom_mbomproduct` | `m_bomproduct.(m_bom_id)` → `m_bom.(m_bom_id)` | BOM Component |

<a id="t-m_bomalternative"></a>
## `m_bomalternative` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Alternative Group`
- 사전 Description: Product BOM Alternative Group
- 근거 문장: 사전 Name='Alternative Group'; Description='Product BOM Alternative Group'; 주요 열 근거 부족; FK mbomalternative_mbomproduct; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `bom`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mbomalternative_mbomproduct` | `m_bomproduct.(m_bomalternative_id)` → `m_bomalternative.(m_bomalternative_id)` | BOM Component |

<a id="t-m_bomproduct"></a>
## `m_bomproduct` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `BOM Component`
- 사전 Description: Bill of Material Component (Product)
- 근거 문장: 사전 Name='BOM Component'; Description='Bill of Material Component (Product)'; 주요 열 m_bom_id, m_bomalternative_id; FK mbom_mbomproduct, mbomalternative_mbomproduct; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `bom`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_bom_id` | BOM | `numeric(10,0)` |
| `m_bomalternative_id` | Alternative Group | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mbom_mbomproduct` | `m_bomproduct.(m_bom_id)` → `m_bom.(m_bom_id)` | BOM |
| outgoing | `mbomalternative_mbomproduct` | `m_bomproduct.(m_bomalternative_id)` → `m_bomalternative.(m_bomalternative_id)` | Alternative Group |
| outgoing | `mproductop_mbomproduct` | `m_bomproduct.(m_productoperation_id)` → `m_productoperation.(m_productoperation_id)` | Product Operation |

<a id="t-m_bp_price"></a>
## `m_bp_price` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Business Partner Price`
- 사전 Description: Business Partner specific pricing that will override the price list
- 근거 문장: 사전 Name='Business Partner Price'; Description='Business Partner specific pricing that will override the price list'; 주요 열 breakvalue, m_product_id, pricelimit, pricelist; FK mproduct_mbpprice; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `breakvalue` | Break Value | `numeric` |
| `m_product_id` | Product | `numeric(10,0)` |
| `pricelimit` | Limit Price | `numeric` |
| `pricelist` | List Price | `numeric` |
| `pricestd` | Standard Price | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mproduct_mbpprice` | `m_bp_price.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_changenotice"></a>
## `m_changenotice` — 프로세스·스케줄·시스템 운영

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Change Notice`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Change Notice'; 주요 열 processing; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 프로세스·스케줄·시스템 운영를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `processing` | Process Now | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-m_changerequest"></a>
## `m_changerequest` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Change Request`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Change Request'; 주요 열 근거 부족; FK mchangerequest_rrequest; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mchangerequest_rrequest` | `r_request.(m_changerequest_id)` → `m_changerequest.(m_changerequest_id)` | Request |

<a id="t-m_commodityshipment"></a>
## `m_commodityshipment` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Commodity Shipment`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Commodity Shipment'; 주요 열 exportlicensenum, harmonizedcode, m_product_id, countryofmanufacture_id; FK countryofmanufacture_mcommodit, mproduct_mcommodityshipment; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `exportlicensenum` | Export License Number | `character varying(30)` |
| `harmonizedcode` | Harmonized Code | `character varying(30)` |
| `m_product_id` | Product | `numeric(10,0)` |
| `countryofmanufacture_id` | Country Of Manufacture | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `countryofmanufacture_mcommodit` | `m_commodityshipment.(countryofmanufacture_id)` → `c_country.(c_country_id)` | Country |
| outgoing | `mproduct_mcommodityshipment` | `m_commodityshipment.(m_product_id)` → `m_product.(m_product_id)` | Product |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_cost"></a>
## `m_cost` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Cost`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Product Cost'; 주요 열 근거 부족; FK masi_mcost, mproduct_mcost; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `masi_mcost` | `m_cost.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |
| outgoing | `mproduct_mcost` | `m_cost.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_costdetail"></a>
## `m_costdetail` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cost Detail`
- 사전 Description: Cost Detail Information
- 근거 문장: 사전 Name='Cost Detail'; Description='Cost Detail Information'; 주요 열 c_acctschema_id, m_product_id, m_attributesetinstance_id, m_costelement_id; FK cacctschema_mcostdetail, corderline_mcostdetail; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `m_product_id` | Product | `numeric(10,0)` |
| `m_attributesetinstance_id` | Attribute Set Instance | `numeric(10,0)` |
| `m_costelement_id` | Cost Element | `numeric(10,0)` |
| `c_orderline_id` | Sales Order Line | `numeric(10,0)` |
| `m_inoutline_id` | Shipment/Receipt Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_mcostdetail` | `m_costdetail.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `corderline_mcostdetail` | `m_costdetail.(c_orderline_id)` → `c_orderline.(c_orderline_id)` | Sales Order Line |
| outgoing | `cprojectissue_mcostdetail` | `m_costdetail.(c_projectissue_id)` → `c_projectissue.(c_projectissue_id)` | Project Issue |
| outgoing | `masi_mcostdetail` | `m_costdetail.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_costelement"></a>
## `m_costelement` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cost Element`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Cost Element'; 주요 열 costelementtype, costingmethod, iscalculated; FK ccostelement_clandedcost, mcostelement_mlandedcostalloc; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `costelementtype` | Cost Element Type | `character(1)` |
| `costingmethod` | Costing Method | `character(1)` |
| `iscalculated` | Calculated | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ccostelement_clandedcost` | `c_landedcost.(m_costelement_id)` → `m_costelement.(m_costelement_id)` | Landed Cost |
| incoming | `mcostelement_mlandedcostalloc` | `c_landedcostallocation.(m_costelement_id)` → `m_costelement.(m_costelement_id)` | Landed Cost Allocation |
| incoming | `mcostelement_corderlandedcost` | `c_orderlandedcost.(m_costelement_id)` → `m_costelement.(m_costelement_id)` | Estimated Landed Cost |
| incoming | `mcostelement_mcost` | `m_cost.(m_costelement_id)` → `m_costelement.(m_costelement_id)` | Product Cost |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_costhistory"></a>
## `m_costhistory` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cost History`
- 사전 Description: Movement history for M_Cost
- 근거 문장: 사전 Name='Cost History'; Description='Movement history for M_Cost'; 주요 열 m_attributesetinstance_id, m_costdetail_id, m_costelement_id, m_costtype_id; FK mattributesetinstance_mcosthis, mcostdetail_mcosthistory; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_attributesetinstance_id` | Attribute Set Instance | `numeric(10,0)` |
| `m_costdetail_id` | Cost Detail | `numeric(10,0)` |
| `m_costelement_id` | Cost Element | `numeric(10,0)` |
| `m_costtype_id` | Cost Type | `numeric(10,0)` |
| `newcamt` | New Accumulated Amt | `numeric` |
| `newcostprice` | New Cost Price | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mattributesetinstance_mcosthis` | `m_costhistory.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |
| outgoing | `mcostdetail_mcosthistory` | `m_costhistory.(m_costdetail_id)` → `m_costdetail.(m_costdetail_id)` | Cost Detail |
| outgoing | `mcostelement_mcosthistory` | `m_costhistory.(m_costelement_id)` → `m_costelement.(m_costelement_id)` | Cost Element |
| outgoing | `mcosttype_mcosthistory` | `m_costhistory.(m_costtype_id)` → `m_costtype.(m_costtype_id)` | Cost Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_costqueue"></a>
## `m_costqueue` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cost Queue`
- 사전 Description: FiFo/LiFo Cost Queue
- 근거 문장: 사전 Name='Cost Queue'; Description='FiFo/LiFo Cost Queue'; 주요 열 m_costtype_id, c_acctschema_id, m_product_id, m_attributesetinstance_id; FK cacctschema_mcostqueue, masi_mcostqueue; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_costtype_id` | Cost Type | `numeric(10,0)` |
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `m_product_id` | Product | `numeric(10,0)` |
| `m_attributesetinstance_id` | Attribute Set Instance | `numeric(10,0)` |
| `m_costelement_id` | Cost Element | `numeric(10,0)` |
| `currentcostprice` | Current Cost Price | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_mcostqueue` | `m_costqueue.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `masi_mcostqueue` | `m_costqueue.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |
| outgoing | `mcostelement_mcostqueue` | `m_costqueue.(m_costelement_id)` → `m_costelement.(m_costelement_id)` | Cost Element |
| outgoing | `mcosttype_mcostqueue` | `m_costqueue.(m_costtype_id)` → `m_costtype.(m_costtype_id)` | Cost Type |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_costtype"></a>
## `m_costtype` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Cost Type`
- 사전 Description: Type of Cost
- 근거 문장: 사전 Name='Cost Type'; Description='Type of Cost'; 주요 열 근거 부족; FK mcosttype_cacctschema, mcosttype_mcost; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mcosttype_cacctschema` | `c_acctschema.(m_costtype_id)` → `m_costtype.(m_costtype_id)` | Accounting Schema |
| incoming | `mcosttype_mcost` | `m_cost.(m_costtype_id)` → `m_costtype.(m_costtype_id)` | Product Cost |
| incoming | `mcosttype_mcosthistory` | `m_costhistory.(m_costtype_id)` → `m_costtype.(m_costtype_id)` | Cost History |
| incoming | `mcosttype_mcostqueue` | `m_costqueue.(m_costtype_id)` → `m_costtype.(m_costtype_id)` | Cost Queue |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_demand"></a>
## `m_demand` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Demand`
- 사전 Description: Material Demand
- 근거 문장: 사전 Name='Demand'; Description='Material Demand'; 주요 열 근거 부족; FK mdemand_mdemandline; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mdemand_mdemandline` | `m_demandline.(m_demand_id)` → `m_demand.(m_demand_id)` | Demand Line |

<a id="t-m_demanddetail"></a>
## `m_demanddetail` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Demand Detail`
- 사전 Description: Material Demand Line Source Detail
- 근거 문장: 사전 Name='Demand Detail'; Description='Material Demand Line Source Detail'; 주요 열 근거 부족; FK mdemandline_mdemanddetail; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mdemandline_mdemanddetail` | `m_demanddetail.(m_demandline_id)` → `m_demandline.(m_demandline_id)` | Demand Line |

<a id="t-m_demandline"></a>
## `m_demandline` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Demand Line`
- 사전 Description: Material Demand Line
- 근거 문장: 사전 Name='Demand Line'; Description='Material Demand Line'; 주요 열 근거 부족; FK mdemandline_mdemanddetail, mdemand_mdemandline; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mdemandline_mdemanddetail` | `m_demanddetail.(m_demandline_id)` → `m_demandline.(m_demandline_id)` | Demand Detail |
| outgoing | `mdemand_mdemandline` | `m_demandline.(m_demand_id)` → `m_demand.(m_demand_id)` | Demand |

<a id="t-m_discountschema"></a>
## `m_discountschema` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Discount Schema`
- 사전 Description: Schema to calculate the trade discount percentage
- 근거 문장: 사전 Name='Discount Schema'; Description='Schema to calculate the trade discount percentage'; 주요 열 근거 부족; FK mdiscounts_mdsbreak, mdiscounts_mplversion; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mdiscounts_mdsbreak` | `m_discountschemabreak.(m_discountschema_id)` → `m_discountschema.(m_discountschema_id)` | Discount Schema Break |
| incoming | `mdiscounts_mplversion` | `m_pricelist_version.(m_discountschema_id)` → `m_discountschema.(m_discountschema_id)` | Price List Version |
| incoming | `mdiscountschema_mdsline` | `m_discountschemaline.(m_discountschema_id)` → `m_discountschema.(m_discountschema_id)` | Discount Price List |

<a id="t-m_discountschemabreak"></a>
## `m_discountschemabreak` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Discount Schema Break`
- 사전 Description: Trade Discount Break
- 근거 문장: 사전 Name='Discount Schema Break'; Description='Trade Discount Break'; 주요 열 m_discountschema_id, breakvalue, m_product_category_id, m_product_id; FK mdiscounts_mdsbreak, mprodcategory_mdiscountsbreak; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_discountschema_id` | Discount Schema | `numeric(10,0)` |
| `breakvalue` | Break Value | `numeric` |
| `m_product_category_id` | Product Category | `numeric(10,0)` |
| `m_product_id` | Product | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mdiscounts_mdsbreak` | `m_discountschemabreak.(m_discountschema_id)` → `m_discountschema.(m_discountschema_id)` | Discount Schema |
| outgoing | `mprodcategory_mdiscountsbreak` | `m_discountschemabreak.(m_product_category_id)` → `m_product_category.(m_product_category_id)` | Product Category |
| outgoing | `mproduct_mdiscountsbreak` | `m_discountschemabreak.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_discountschemaline"></a>
## `m_discountschemaline` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Discount Price List`
- 사전 Description: Line of the price list trade discount schema
- 근거 문장: 사전 Name='Discount Price List'; Description='Line of the price list trade discount schema'; 주요 열 m_discountschema_id, m_product_category_id, m_product_id; FK mdiscountschema_mdsline, mprodcategory_mdiscountsline; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_discountschema_id` | Discount Schema | `numeric(10,0)` |
| `m_product_category_id` | Product Category | `numeric(10,0)` |
| `m_product_id` | Product | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mdiscountschema_mdsline` | `m_discountschemaline.(m_discountschema_id)` → `m_discountschema.(m_discountschema_id)` | Discount Schema |
| outgoing | `mprodcategory_mdiscountsline` | `m_discountschemaline.(m_product_category_id)` → `m_product_category.(m_product_category_id)` | Product Category |
| outgoing | `mproduct_mdiscountsline` | `m_discountschemaline.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_distributionlist"></a>
## `m_distributionlist` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Distribution List`
- 사전 Description: Distribution Lists allow to distribute products to a selected list of partners
- 근거 문장: 사전 Name='Distribution List'; Description='Distribution Lists allow to distribute products to a selected list of partners'; 주요 열 근거 부족; FK mdistributionlist_line, mdistributionlist_runline; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mdistributionlist_line` | `m_distributionlistline.(m_distributionlist_id)` → `m_distributionlist.(m_distributionlist_id)` | Distribution List Line |
| incoming | `mdistributionlist_runline` | `m_distributionrunline.(m_distributionlist_id)` → `m_distributionlist.(m_distributionlist_id)` | Distribution Run Line |
| incoming | `mdistributionlist_tdrdetail` | `t_distributionrundetail.(m_distributionlist_id)` → `m_distributionlist.(m_distributionlist_id)` | T_DistributionRunDetail |

<a id="t-m_distributionlistline"></a>
## `m_distributionlistline` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Distribution List Line`
- 사전 Description: Distribution List Line with Business Partner and Quantity/Percentage
- 근거 문장: 사전 Name='Distribution List Line'; Description='Distribution List Line with Business Partner and Quantity/Percentage'; 주요 열 m_distributionlist_id, minqty; FK mdistributionlline_tdrdetail, mdistributionlist_line; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_distributionlist_id` | Distribution List | `numeric(10,0)` |
| `minqty` | Minimum Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mdistributionlline_tdrdetail` | `t_distributionrundetail.(m_distributionlistline_id)` → `m_distributionlistline.(m_distributionlistline_id)` | T_DistributionRunDetail |
| outgoing | `mdistributionlist_line` | `m_distributionlistline.(m_distributionlist_id)` → `m_distributionlist.(m_distributionlist_id)` | Distribution List |

<a id="t-m_distributionrun"></a>
## `m_distributionrun` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Distribution Run`
- 사전 Description: Distribution Run create Orders to distribute products to a selected list of partners
- 근거 문장: 사전 Name='Distribution Run'; Description='Distribution Run create Orders to distribute products to a selected list of partners'; 주요 열 근거 부족; FK mdistributionrun_line, mdistributionrun_tdrdetail; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mdistributionrun_line` | `m_distributionrunline.(m_distributionrun_id)` → `m_distributionrun.(m_distributionrun_id)` | Distribution Run Line |
| incoming | `mdistributionrun_tdrdetail` | `t_distributionrundetail.(m_distributionrun_id)` → `m_distributionrun.(m_distributionrun_id)` | T_DistributionRunDetail |

<a id="t-m_distributionrunline"></a>
## `m_distributionrunline` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Distribution Run Line`
- 사전 Description: Distribution Run Lines define Distribution List, the Product and Quantiries
- 근거 문장: 사전 Name='Distribution Run Line'; Description='Distribution Run Lines define Distribution List, the Product and Quantiries'; 주요 열 m_distributionrun_id, m_distributionlist_id, totalqty, minqty; FK mdistributionrline_tdrdetail, mdistributionlist_runline; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_distributionrun_id` | Distribution Run | `numeric(10,0)` |
| `m_distributionlist_id` | Distribution List | `numeric(10,0)` |
| `totalqty` | Total Quantity | `numeric` |
| `minqty` | Minimum Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mdistributionrline_tdrdetail` | `t_distributionrundetail.(m_distributionrunline_id)` → `m_distributionrunline.(m_distributionrunline_id)` | T_DistributionRunDetail |
| outgoing | `mdistributionlist_runline` | `m_distributionrunline.(m_distributionlist_id)` → `m_distributionlist.(m_distributionlist_id)` | Distribution List |
| outgoing | `mdistributionrun_line` | `m_distributionrunline.(m_distributionrun_id)` → `m_distributionrun.(m_distributionrun_id)` | Distribution Run |

<a id="t-m_edi"></a>
## `m_edi` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `EDI Transaction`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='EDI Transaction'; 주요 열 c_bp_edi_id, edistatus, processed; FK medi_ediinfo, cbpedi_medi; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bp_edi_id` | EDI Definition | `numeric(10,0)` |
| `edistatus` | EDI Status | `character(1)` |
| `processed` | Processed | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `medi_ediinfo` | `m_edi_info.(m_edi_id)` → `m_edi.(m_edi_id)` | EDI Log |
| outgoing | `cbpedi_medi` | `m_edi.(c_bp_edi_id)` → `c_bp_edi.(c_bp_edi_id)` | EDI Definition |

<a id="t-m_edi_info"></a>
## `m_edi_info` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `EDI Log`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='EDI Log'; 주요 열 m_edi_id; FK medi_ediinfo; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_edi_id` | EDI Transaction | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `medi_ediinfo` | `m_edi_info.(m_edi_id)` → `m_edi.(m_edi_id)` | EDI Transaction |

<a id="t-m_forecast"></a>
## `m_forecast` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Forecast`
- 사전 Description: Material Forecast
- 근거 문장: 사전 Name='Forecast'; Description='Material Forecast'; 주요 열 isdefault, c_calendar_id, c_year_id, processing; FK mforecast_iproductplanning, ccalendar_mforecast; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isdefault` | Default | `character(1)` |
| `c_calendar_id` | Calendar | `numeric(10,0)` |
| `c_year_id` | Year | `numeric(10,0)` |
| `processing` | Process Now | `character(1)` |
| `m_pricelist_id` | Price List | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mforecast_iproductplanning` | `i_productplanning.(m_forecast_id)` → `m_forecast.(m_forecast_id)` | Import Product Planning |
| outgoing | `ccalendar_mforecast` | `m_forecast.(c_calendar_id)` → `c_calendar.(c_calendar_id)` | Calendar |
| outgoing | `cyear_mforecast` | `m_forecast.(c_year_id)` → `c_year.(c_year_id)` | Year |
| outgoing | `mpricelist_mforecast` | `m_forecast.(m_pricelist_id)` → `m_pricelist.(m_pricelist_id)` | Price List |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_forecastline"></a>
## `m_forecastline` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Forecast Line`
- 사전 Description: Forecast Line
- 근거 문장: 사전 Name='Forecast Line'; Description='Forecast Line'; 주요 열 m_forecast_id, c_period_id, qty, m_product_id; FK mforecastline_iproductplanning, mforecastline_mdemanddetail; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_forecast_id` | Forecast | `numeric(10,0)` |
| `c_period_id` | Period | `numeric(10,0)` |
| `qty` | Quantity | `numeric` |
| `m_product_id` | Product | `numeric(10,0)` |
| `qtycalculated` | Calculated Quantity | `numeric` |
| `m_warehouse_id` | Warehouse | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mforecastline_iproductplanning` | `i_productplanning.(m_forecastline_id)` → `m_forecastline.(m_forecastline_id)` | Import Product Planning |
| incoming | `mforecastline_mdemanddetail` | `m_demanddetail.(m_forecastline_id)` → `m_forecastline.(m_forecastline_id)` | Demand Detail |
| outgoing | `cperiod_mforecastline` | `m_forecastline.(c_period_id)` → `c_period.(c_period_id)` | Period |
| outgoing | `mforecast_mforecastline` | `m_forecastline.(m_forecast_id)` → `m_forecast.(m_forecast_id)` | Forecast |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_freight"></a>
## `m_freight` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Freight`
- 사전 Description: Freight Rate
- 근거 문장: 사전 Name='Freight'; Description='Freight Rate'; 주요 열 m_shipper_id, m_freightcategory_id, freightamt; FK mfreightcategory_mfreight, mshipper_mfreight; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shipper_id` | Shipper | `numeric(10,0)` |
| `m_freightcategory_id` | Freight Category | `numeric(10,0)` |
| `freightamt` | Freight Amount | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mfreightcategory_mfreight` | `m_freight.(m_freightcategory_id)` → `m_freightcategory.(m_freightcategory_id)` | Freight Category |
| outgoing | `mshipper_mfreight` | `m_freight.(m_shipper_id)` → `m_shipper.(m_shipper_id)` | Shipper |

<a id="t-m_freightcategory"></a>
## `m_freightcategory` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Freight Category`
- 사전 Description: Category of the Freight
- 근거 문장: 사전 Name='Freight Category'; Description='Category of the Freight'; 주요 열 근거 부족; FK mfreightcategory_mfreight; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mfreightcategory_mfreight` | `m_freight.(m_freightcategory_id)` → `m_freightcategory.(m_freightcategory_id)` | Freight |

<a id="t-m_inout"></a>
## `m_inout` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipment/Receipt`
- 사전 Description: Material Shipment Document
- 근거 문장: 사전 Name='Shipment/Receipt'; Description='Material Shipment Document'; 주요 열 movementdate, freightcostrule, freightamt, m_shipper_id; FK minout_minoutconfirm, minout_minoutline; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `movementdate` | Movement Date | `timestamp without time zone` |
| `freightcostrule` | Freight Cost Rule | `character(1)` |
| `freightamt` | Freight Amount | `numeric` |
| `m_shipper_id` | Shipper | `numeric(10,0)` |
| `trackingno` | Tracking No | `character varying(60)` |
| `m_rma_id` | RMA | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `minout_minoutconfirm` | `m_inoutconfirm.(m_inout_id)` → `m_inout.(m_inout_id)` | Ship/Receipt Confirmation |
| incoming | `minout_minoutline` | `m_inoutline.(m_inout_id)` → `m_inout.(m_inout_id)` | Shipment/Receipt Line |
| incoming | `minout_mpackage` | `m_package.(m_inout_id)` → `m_inout.(m_inout_id)` | Package |
| incoming | `minout_mrma` | `m_rma.(inout_id)` → `m_inout.(m_inout_id)` | RMA |

<a id="t-m_inoutconfirm"></a>
## `m_inoutconfirm` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Ship/Receipt Confirmation`
- 사전 Description: Material Shipment or Receipt Confirmation
- 근거 문장: 사전 Name='Ship/Receipt Confirmation'; Description='Material Shipment or Receipt Confirmation'; 주요 열 m_inout_id; FK minoutconfirm_minoutlineconf, minout_minoutconfirm; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_inout_id` | Shipment/Receipt | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `minoutconfirm_minoutlineconf` | `m_inoutlineconfirm.(m_inoutconfirm_id)` → `m_inoutconfirm.(m_inoutconfirm_id)` | Ship/Receipt Confirmation Line |
| outgoing | `minout_minoutconfirm` | `m_inoutconfirm.(m_inout_id)` → `m_inout.(m_inout_id)` | Shipment/Receipt |

<a id="t-m_inoutline"></a>
## `m_inoutline` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipment/Receipt Line`
- 사전 Description: Line on Shipment or Receipt document
- 근거 문장: 사전 Name='Shipment/Receipt Line'; Description='Line on Shipment or Receipt document'; 주요 열 m_inout_id, m_locator_id, movementqty, confirmedqty; FK minoutline_minoutconfirm, minoutline_mmatchinv; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_inout_id` | Shipment/Receipt | `numeric(10,0)` |
| `m_locator_id` | Locator | `numeric(10,0)` |
| `movementqty` | Movement Quantity | `numeric` |
| `confirmedqty` | Confirmed Quantity | `numeric` |
| `pickedqty` | Picked Quantity | `numeric` |
| `scrappedqty` | Scrapped Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `minoutline_minoutconfirm` | `m_inoutlineconfirm.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Ship/Receipt Confirmation Line |
| incoming | `minoutline_mmatchinv` | `m_matchinv.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Match Invoice |
| incoming | `minoutline_mmatchpo` | `m_matchpo.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Match PO |
| incoming | `minoutline_mpackageline` | `m_packageline.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Package Line |

<a id="t-m_inoutlineconfirm"></a>
## `m_inoutlineconfirm` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Ship/Receipt Confirmation Line`
- 사전 Description: Material Shipment or Receipt Confirmation Line
- 근거 문장: 사전 Name='Ship/Receipt Confirmation Line'; Description='Material Shipment or Receipt Confirmation Line'; 주요 열 m_inoutconfirm_id, m_inoutline_id, targetqty, confirmedqty; FK minoutlineconfirm_import, minoutconfirm_minoutlineconf; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_inoutconfirm_id` | Ship/Receipt Confirmation | `numeric(10,0)` |
| `m_inoutline_id` | Shipment/Receipt Line | `numeric(10,0)` |
| `targetqty` | Target Quantity | `numeric` |
| `confirmedqty` | Confirmed Quantity | `numeric` |
| `differenceqty` | Difference | `numeric` |
| `scrappedqty` | Scrapped Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `minoutlineconfirm_import` | `i_inoutlineconfirm.(m_inoutlineconfirm_id)` → `m_inoutlineconfirm.(m_inoutlineconfirm_id)` | Ship/Receipt Confirmation Import Line |
| outgoing | `minoutconfirm_minoutlineconf` | `m_inoutlineconfirm.(m_inoutconfirm_id)` → `m_inoutconfirm.(m_inoutconfirm_id)` | Ship/Receipt Confirmation |
| outgoing | `minoutline_minoutconfirm` | `m_inoutlineconfirm.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Shipment/Receipt Line |

<a id="t-m_inoutlinema"></a>
## `m_inoutlinema` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_InOutLineMA`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_InOutLineMA'; 주요 열 movementqty, isautogenerated; FK masi_minourlinema, minoutline_minoutlinema; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `movementqty` | Movement Quantity | `numeric` |
| `isautogenerated` | Auto Generated | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `masi_minourlinema` | `m_inoutlinema.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |
| outgoing | `minoutline_minoutlinema` | `m_inoutlinema.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Shipment/Receipt Line |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_inventory"></a>
## `m_inventory` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Phys.Inventory`
- 사전 Description: Parameters for a Physical Inventory
- 근거 문장: 사전 Name='Phys.Inventory'; Description='Parameters for a Physical Inventory'; 주요 열 m_warehouse_id; FK minventory_iinventory, minventory_minventoryline; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_warehouse_id` | Warehouse | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `minventory_iinventory` | `i_inventory.(m_inventory_id)` → `m_inventory.(m_inventory_id)` | Import Inventory |
| incoming | `minventory_minventoryline` | `m_inventoryline.(m_inventory_id)` → `m_inventory.(m_inventory_id)` | Phys.Inventory Line |
| incoming | `minventory_mmovconfirm` | `m_movementconfirm.(m_inventory_id)` → `m_inventory.(m_inventory_id)` | Move Confirm |
| outgoing | `mperpetualinv_minventory` | `m_inventory.(m_perpetualinv_id)` → `m_perpetualinv.(m_perpetualinv_id)` | Perpetual Inventory |

<a id="t-m_inventoryline"></a>
## `m_inventoryline` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Phys.Inventory Line`
- 사전 Description: Unique line in an Inventory document
- 근거 문장: 사전 Name='Phys.Inventory Line'; Description='Unique line in an Inventory document'; 주요 열 m_inventory_id, m_locator_id, qtybook, qtycount; FK mcostingline_iinventory, minventoryline_iinventory; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_inventory_id` | Phys.Inventory | `numeric(10,0)` |
| `m_locator_id` | Locator | `numeric(10,0)` |
| `qtybook` | Quantity book | `numeric` |
| `qtycount` | Quantity count | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mcostingline_iinventory` | `i_inventory.(m_costingline_id)` → `m_inventoryline.(m_inventoryline_id)` | Import Inventory |
| incoming | `minventoryline_iinventory` | `i_inventory.(m_inventoryline_id)` → `m_inventoryline.(m_inventoryline_id)` | Import Inventory |
| incoming | `minventoryline_milinema` | `m_inventorylinema.(m_inventoryline_id)` → `m_inventoryline.(m_inventoryline_id)` | M_InventoryLineMA |
| incoming | `minventoryline_mmovlineconfirm` | `m_movementlineconfirm.(m_inventoryline_id)` → `m_inventoryline.(m_inventoryline_id)` | Move Line Confirm |

<a id="t-m_inventorylinema"></a>
## `m_inventorylinema` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_InventoryLineMA`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_InventoryLineMA'; 주요 열 movementqty; FK minventoryline_milinema; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `movementqty` | Movement Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `minventoryline_milinema` | `m_inventorylinema.(m_inventoryline_id)` → `m_inventoryline.(m_inventoryline_id)` | Phys.Inventory Line |

<a id="t-m_locator"></a>
## `m_locator` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Locator`
- 사전 Description: Warehouse Locator
- 근거 문장: 사전 Name='Locator'; Description='Warehouse Locator'; 주요 열 m_warehouse_id, m_locatortype_id; FK mlocator_iinventory, mlocator_minventorycount; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_warehouse_id` | Warehouse | `numeric(10,0)` |
| `m_locatortype_id` | Locator Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mlocator_iinventory` | `i_inventory.(m_locator_id)` → `m_locator.(m_locator_id)` | Import Inventory |
| incoming | `mlocator_minventorycount` | `m_transaction.(m_locator_id)` → `m_locator.(m_locator_id)` | Inventory Transaction |
| incoming | `mlocator_minventoryline` | `m_inventoryline.(m_locator_id)` → `m_locator.(m_locator_id)` | Phys.Inventory Line |
| incoming | `mlocator_movementline` | `m_movementline.(m_locatorto_id)` → `m_locator.(m_locator_id)` | Move Line |

<a id="t-m_locatortype"></a>
## `m_locatortype` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Locator Type`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Locator Type'; 주요 열 근거 부족; FK mlocatortype_mlocator; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mlocatortype_mlocator` | `m_locator.(m_locatortype_id)` → `m_locatortype.(m_locatortype_id)` | Locator |

<a id="t-m_lot"></a>
## `m_lot` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Lot`
- 사전 Description: Product Lot Definition
- 근거 문장: 사전 Name='Lot'; Description='Product Lot Definition'; 주요 열 m_lotctl_id; FK mlotctl_mlot; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_lotctl_id` | Lot Control | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mlotctl_mlot` | `m_lot.(m_lotctl_id)` → `m_lotctl.(m_lotctl_id)` | Lot Control |

<a id="t-m_lotctl"></a>
## `m_lotctl` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Lot Control`
- 사전 Description: Product Lot Control
- 근거 문장: 사전 Name='Lot Control'; Description='Product Lot Control'; 주요 열 근거 부족; FK mlotctl_mlot, mlotctl_mlotctlexclude; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mlotctl_mlot` | `m_lot.(m_lotctl_id)` → `m_lotctl.(m_lotctl_id)` | Lot |
| incoming | `mlotctl_mlotctlexclude` | `m_lotctlexclude.(m_lotctl_id)` → `m_lotctl.(m_lotctl_id)` | Exclude Lot |

<a id="t-m_lotctlexclude"></a>
## `m_lotctlexclude` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Exclude Lot`
- 사전 Description: Exclude the ability to create Lots in Attribute Sets
- 근거 문장: 사전 Name='Exclude Lot'; Description='Exclude the ability to create Lots in Attribute Sets'; 주요 열 m_lotctl_id; FK mlotctl_mlotctlexclude; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_lotctl_id` | Lot Control | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mlotctl_mlotctlexclude` | `m_lotctlexclude.(m_lotctl_id)` → `m_lotctl.(m_lotctl_id)` | Lot Control |

<a id="t-m_matchinv"></a>
## `m_matchinv` — 청구·대변 문서

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Match Invoice`
- 사전 Description: Match Shipment/Receipt to Invoice
- 근거 문장: 사전 Name='Match Invoice'; Description='Match Shipment/Receipt to Invoice'; 주요 열 c_invoiceline_id; FK convoiceline_mmatchinv, refmatchinv_mmatchinv; 사전 의미와 열/FK가 청구·대변 문서를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_invoiceline_id` | Invoice Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `convoiceline_mmatchinv` | `m_matchinv.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` | Invoice Line |
| outgoing | `refmatchinv_mmatchinv` | `m_matchinv.(ref_matchinv_id)` → `m_matchinv.(m_matchinv_id)` | Match Invoice |
| outgoing | `reversal_mmatchinv` | `m_matchinv.(reversal_id)` → `m_matchinv.(m_matchinv_id)` | Match Invoice |

<a id="t-m_matchpo"></a>
## `m_matchpo` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Match PO`
- 사전 Description: Match Purchase Order to Shipment/Receipt and Invoice
- 근거 문장: 사전 Name='Match PO'; Description='Match Purchase Order to Shipment/Receipt and Invoice'; 주요 열 m_inoutline_id, qty; FK minoutline_mmatchpo, refmatchpo_mmatchpo; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_inoutline_id` | Shipment/Receipt Line | `numeric(10,0)` |
| `qty` | Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `minoutline_mmatchpo` | `m_matchpo.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Shipment/Receipt Line |
| outgoing | `refmatchpo_mmatchpo` | `m_matchpo.(ref_matchpo_id)` → `m_matchpo.(m_matchpo_id)` | Match PO |
| outgoing | `reversal_mmatchpo` | `m_matchpo.(reversal_id)` → `m_matchpo.(m_matchpo_id)` | Match PO |

<a id="t-m_movement"></a>
## `m_movement` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Inventory Move`
- 사전 Description: Movement of Inventory
- 근거 문장: 사전 Name='Inventory Move'; Description='Movement of Inventory'; 주요 열 m_warehouse_id, m_warehouseto_id; FK mmovement_mmovementconfirm, mmovement_mmovementline; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_warehouse_id` | Warehouse | `numeric(10,0)` |
| `m_warehouseto_id` | Warehouse To | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mmovement_mmovementconfirm` | `m_movementconfirm.(m_movement_id)` → `m_movement.(m_movement_id)` | Move Confirm |
| incoming | `mmovement_mmovementline` | `m_movementline.(m_movement_id)` → `m_movement.(m_movement_id)` | Move Line |
| outgoing | `mwarehouse_mmovement` | `m_movement.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | Warehouse |
| outgoing | `mwarehouseto_mmovement` | `m_movement.(m_warehouseto_id)` → `m_warehouse.(m_warehouse_id)` | Warehouse |

<a id="t-m_movementconfirm"></a>
## `m_movementconfirm` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Move Confirm`
- 사전 Description: Inventory Move Confirmation
- 근거 문장: 사전 Name='Move Confirm'; Description='Inventory Move Confirmation'; 주요 열 m_movement_id; FK mmovementconfirm_mmovlineconf, mmovement_mmovementconfirm; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_movement_id` | Inventory Move | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mmovementconfirm_mmovlineconf` | `m_movementlineconfirm.(m_movementconfirm_id)` → `m_movementconfirm.(m_movementconfirm_id)` | Move Line Confirm |
| outgoing | `mmovement_mmovementconfirm` | `m_movementconfirm.(m_movement_id)` → `m_movement.(m_movement_id)` | Inventory Move |

<a id="t-m_movementline"></a>
## `m_movementline` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Move Line`
- 사전 Description: Inventory Move document Line
- 근거 문장: 사전 Name='Move Line'; Description='Inventory Move document Line'; 주요 열 m_movement_id, m_locator_id, m_locatorto_id, movementqty; FK mmovementline_mmovlineconfirm, ddorderline_mmovementline; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_movement_id` | Inventory Move | `numeric(10,0)` |
| `m_locator_id` | Locator | `numeric(10,0)` |
| `m_locatorto_id` | Locator To | `numeric(10,0)` |
| `movementqty` | Movement Quantity | `numeric` |
| `confirmedqty` | Confirmed Quantity | `numeric` |
| `scrappedqty` | Scrapped Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mmovementline_mmovlineconfirm` | `m_movementlineconfirm.(m_movementline_id)` → `m_movementline.(m_movementline_id)` | Move Line Confirm |
| outgoing | `ddorderline_mmovementline` | `m_movementline.(dd_orderline_id)` → `dd_orderline.(dd_orderline_id)` | Distribution Order Line |
| outgoing | `mmovement_mmovementline` | `m_movementline.(m_movement_id)` → `m_movement.(m_movement_id)` | Inventory Move |
| outgoing | `reversalline_mmovementline` | `m_movementline.(reversalline_id)` → `m_movementline.(m_movementline_id)` | Move Line |

<a id="t-m_movementlineconfirm"></a>
## `m_movementlineconfirm` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Move Line Confirm`
- 사전 Description: Inventory Move Line Confirmation
- 근거 문장: 사전 Name='Move Line Confirm'; Description='Inventory Move Line Confirmation'; 주요 열 m_movementconfirm_id, m_movementline_id, targetqty, confirmedqty; FK mmovementconfirm_mmovlineconf, mmovementline_mmovlineconfirm; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_movementconfirm_id` | Move Confirm | `numeric(10,0)` |
| `m_movementline_id` | Move Line | `numeric(10,0)` |
| `targetqty` | Target Quantity | `numeric` |
| `confirmedqty` | Confirmed Quantity | `numeric` |
| `differenceqty` | Difference | `numeric` |
| `scrappedqty` | Scrapped Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mmovementconfirm_mmovlineconf` | `m_movementlineconfirm.(m_movementconfirm_id)` → `m_movementconfirm.(m_movementconfirm_id)` | Move Confirm |
| outgoing | `mmovementline_mmovlineconfirm` | `m_movementlineconfirm.(m_movementline_id)` → `m_movementline.(m_movementline_id)` | Move Line |

<a id="t-m_movementlinema"></a>
## `m_movementlinema` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_MovementLineMA`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_MovementLineMA'; 주요 열 movementqty, isautogenerated; FK masi_mmovementlinema, mmovementline_mmovementlinema; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `movementqty` | Movement Quantity | `numeric` |
| `isautogenerated` | Auto Generated | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `masi_mmovementlinema` | `m_movementlinema.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |
| outgoing | `mmovementline_mmovementlinema` | `m_movementlinema.(m_movementline_id)` → `m_movementline.(m_movementline_id)` | Move Line |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_operationresource"></a>
## `m_operationresource` — 자원·시간·경비·교육

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Operation Resource`
- 사전 Description: Product Operation Resource
- 근거 문장: 사전 Name='Operation Resource'; Description='Product Operation Resource'; 주요 열 setuptime, unitruntime, teardowntime; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `setuptime` | Setup Time | `numeric` |
| `unitruntime` | Runtime per Unit | `numeric` |
| `teardowntime` | Teardown Time | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-m_package"></a>
## `m_package` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Package`
- 사전 Description: Shipment Package
- 근거 문장: 사전 Name='Package'; Description='Shipment Package'; 주요 열 m_inout_id, m_shipper_id, trackinginfo, isfuturedayshipment; FK mpackage_mpackageline, mpackage_mpackagemps; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_inout_id` | Shipment/Receipt | `numeric(10,0)` |
| `m_shipper_id` | Shipper | `numeric(10,0)` |
| `trackinginfo` | Tracking Info | `character varying(255)` |
| `isfuturedayshipment` | Future Day Shipment | `character(1)` |
| `trackingno` | Tracking No | `character varying(255)` |
| `m_shipperlabels_id` | Shipper Labels | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mpackage_mpackageline` | `m_packageline.(m_package_id)` → `m_package.(m_package_id)` | Package Line |
| incoming | `mpackage_mpackagemps` | `m_packagemps.(m_package_id)` → `m_package.(m_package_id)` | Package MPS |
| incoming | `mpackage_mshippingtransaction` | `m_shippingtransaction.(m_package_id)` → `m_package.(m_package_id)` | Shipping Transaction |
| outgoing | `cbpshippingacct_mpackage` | `m_package.(c_bp_shippingacct_id)` → `c_bp_shippingacct.(c_bp_shippingacct_id)` | Business Partner Shipping Account |

<a id="t-m_packageline"></a>
## `m_packageline` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Package Line`
- 사전 Description: The detail content of the Package
- 근거 문장: 사전 Name='Package Line'; Description='The detail content of the Package'; 주요 열 m_package_id, m_inoutline_id, qty, m_packagemps_id; FK minoutline_mpackageline, mpackage_mpackageline; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_package_id` | Package | `numeric(10,0)` |
| `m_inoutline_id` | Shipment/Receipt Line | `numeric(10,0)` |
| `qty` | Quantity | `numeric` |
| `m_packagemps_id` | Package MPS | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `minoutline_mpackageline` | `m_packageline.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Shipment/Receipt Line |
| outgoing | `mpackage_mpackageline` | `m_packageline.(m_package_id)` → `m_package.(m_package_id)` | Package |
| outgoing | `mpackagemps_mpackageline` | `m_packageline.(m_packagemps_id)` → `m_packagemps.(m_packagemps_id)` | Package MPS |

<a id="t-m_packagemps"></a>
## `m_packagemps` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Package MPS`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Package MPS'; 주요 열 m_package_id, mastertrackingno, trackingno; FK mpackagemps_mpackageline, mpackagemps_mshippingtransacti; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_package_id` | Package | `numeric(10,0)` |
| `mastertrackingno` | Master Tracking No | `character varying(255)` |
| `trackingno` | Tracking No | `character varying(255)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mpackagemps_mpackageline` | `m_packageline.(m_packagemps_id)` → `m_packagemps.(m_packagemps_id)` | Package Line |
| incoming | `mpackagemps_mshippingtransacti` | `m_shippingtransactionline.(m_packagemps_id)` → `m_packagemps.(m_packagemps_id)` | Shipping Transaction Line |
| outgoing | `mpackage_mpackagemps` | `m_packagemps.(m_package_id)` → `m_package.(m_package_id)` | Package |

<a id="t-m_parttype"></a>
## `m_parttype` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Part Type`
- 사전 Description: Manufacturing part type
- 근거 문장: 사전 Name='Part Type'; Description='Manufacturing part type'; 주요 열 근거 부족; FK mparttype_mproduct; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mparttype_mproduct` | `m_product.(m_parttype_id)` → `m_parttype.(m_parttype_id)` | Product |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_perpetualinv"></a>
## `m_perpetualinv` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Perpetual Inventory`
- 사전 Description: Rules for generating physical inventory
- 근거 문장: 사전 Name='Perpetual Inventory'; Description='Rules for generating physical inventory'; 주요 열 m_warehouse_id; FK mperpetualinv_minventory, mwarehouse_mperpetualinv; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_warehouse_id` | Warehouse | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mperpetualinv_minventory` | `m_inventory.(m_perpetualinv_id)` → `m_perpetualinv.(m_perpetualinv_id)` | Phys.Inventory |
| outgoing | `mwarehouse_mperpetualinv` | `m_perpetualinv.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | Warehouse |

<a id="t-m_pricelist"></a>
## `m_pricelist` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Price List`
- 사전 Description: Unique identifier of a Price List
- 근거 문장: 사전 Name='Price List'; Description='Unique identifier of a Price List'; 주요 열 basepricelist_id, issopricelist, enforcepricelimit; FK mpricelist_ipricelist, mpricelist_mpricelisttrl; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `basepricelist_id` | Base Price List | `numeric(10,0)` |
| `issopricelist` | Sales Price list | `character(1)` |
| `enforcepricelimit` | Enforce price limit | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mpricelist_ipricelist` | `i_pricelist.(m_pricelist_id)` → `m_pricelist.(m_pricelist_id)` | Import Price List |
| incoming | `mpricelist_mpricelisttrl` | `m_pricelist_trl.(m_pricelist_id)` → `m_pricelist.(m_pricelist_id)` | Price List |
| incoming | `mpricelist_mpricelistversion` | `m_pricelist_version.(m_pricelist_id)` → `m_pricelist.(m_pricelist_id)` | Price List Version |
| outgoing | `basepricelist` | `m_pricelist.(basepricelist_id)` → `m_pricelist.(m_pricelist_id)` | Price List |

<a id="t-m_pricelist_trl"></a>
## `m_pricelist_trl` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Price List`
- 사전 Description: Unique identifier of a Price List
- 근거 문장: 사전 Name='Price List'; Description='Unique identifier of a Price List'; 주요 열 근거 부족; FK mpricelist_mpricelisttrl; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mpricelist_mpricelisttrl` | `m_pricelist_trl.(m_pricelist_id)` → `m_pricelist.(m_pricelist_id)` | Price List |

<a id="t-m_pricelist_version"></a>
## `m_pricelist_version` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Price List Version`
- 사전 Description: Identifies a unique instance of a Price List
- 근거 문장: 사전 Name='Price List Version'; Description='Identifies a unique instance of a Price List'; 주요 열 m_pricelist_id, m_discountschema_id, m_pricelist_version_base_id; FK mpricelistver_mproductprice, mpricelistversion_ipricelist; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_pricelist_id` | Price List | `numeric(10,0)` |
| `m_discountschema_id` | Discount Schema | `numeric(10,0)` |
| `m_pricelist_version_base_id` | Base Price List | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mpricelistver_mproductprice` | `m_productprice.(m_pricelist_version_id)` → `m_pricelist_version.(m_pricelist_version_id)` | Product Price |
| incoming | `mpricelistversion_ipricelist` | `i_pricelist.(m_pricelist_version_id)` → `m_pricelist_version.(m_pricelist_version_id)` | Import Price List |
| incoming | `mpricelistversion_mpricelistve` | `m_pricelist_version_trl.(m_pricelist_version_id)` → `m_pricelist_version.(m_pricelist_version_id)` | Price List Version Trl |
| incoming | `mpricelistversion_mproductpric` | `m_productpricevendorbreak.(m_pricelist_version_id)` → `m_pricelist_version.(m_pricelist_version_id)` | Product Price Break |

<a id="t-m_pricelist_version_trl"></a>
## `m_pricelist_version_trl` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Price List Version Trl`
- 사전 Description: Identifies a unique instance of a Price List
- 근거 문장: 사전 Name='Price List Version Trl'; Description='Identifies a unique instance of a Price List'; 주요 열 근거 부족; FK mpricelistversion_mpricelistve; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mpricelistversion_mpricelistve` | `m_pricelist_version_trl.(m_pricelist_version_id)` → `m_pricelist_version.(m_pricelist_version_id)` | Price List Version |

<a id="t-m_product"></a>
## `m_product` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product`
- 사전 Description: Product Service Item
- 근거 문장: 사전 Name='Product'; Description='Product Service Item'; 주요 열 upc, sku, c_uom_id, m_product_category_id; FK m_product_m_product_acct, m_product_productpo; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `upc` | UPC/EAN | `character varying(30)` |
| `sku` | SKU | `character varying(30)` |
| `c_uom_id` | UOM | `numeric(10,0)` |
| `m_product_category_id` | Product Category | `numeric(10,0)` |
| `producttype` | Product Type | `character(1)` |
| `m_attributeset_id` | Attribute Set | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `m_product_m_product_acct` | `m_product_acct.(m_product_id)` → `m_product.(m_product_id)` | Product Acct |
| incoming | `m_product_productpo` | `m_product_po.(m_product_id)` → `m_product.(m_product_id)` | Product Purchasing |
| incoming | `mproduct_aassetproduct` | `a_asset_product.(m_product_id)` → `m_product.(m_product_id)` | Asset Product |
| incoming | `mproduct_aregproduct` | `a_registrationproduct.(m_product_id)` → `m_product.(m_product_id)` | Registration Product |

<a id="t-m_product_acct"></a>
## `m_product_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Product Acct'; 주요 열 p_revenue_acct, p_expense_acct, p_asset_acct, p_purchasepricevariance_acct; FK cacctschema_mproductacct, paveragecostvariance_mproducta; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `p_revenue_acct` | Product Revenue | `numeric(10,0)` |
| `p_expense_acct` | Product Expense | `numeric(10,0)` |
| `p_asset_acct` | Product Asset | `numeric(10,0)` |
| `p_purchasepricevariance_acct` | Purchase Price Variance | `numeric(10,0)` |
| `p_invoicepricevariance_acct` | Invoice Price Variance | `numeric(10,0)` |
| `p_cogs_acct` | Product COGS | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_mproductacct` | `m_product_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `paveragecostvariance_mproducta` | `m_product_acct.(p_averagecostvariance_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `pburden_mproductacct` | `m_product_acct.(p_burden_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `pcostadjustment_mproductacct` | `m_product_acct.(p_costadjustment_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-m_product_bom_old"></a>
## `m_product_bom_old` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 line, m_product_id, m_productbom_id, bomqty; FK mproduct_bomproduct, mproduct_mproductbom; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `line` | 미지정 | `numeric(10,0)` |
| `m_product_id` | 미지정 | `numeric(10,0)` |
| `m_productbom_id` | 미지정 | `numeric(10,0)` |
| `bomqty` | 미지정 | `numeric` |
| `bomtype` | 미지정 | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mproduct_bomproduct` | `m_product_bom_old.(m_productbom_id)` → `m_product.(m_product_id)` | Product |
| outgoing | `mproduct_mproductbom` | `m_product_bom_old.(m_product_id)` → `m_product.(m_product_id)` | Product |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_product_category"></a>
## `m_product_category` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Category`
- 사전 Description: Category of a Product
- 근거 문장: 사전 Name='Product Category'; Description='Category of a Product'; 주요 열 m_product_category_parent_id; FK mprodcat_mprodcatacct, mprodcategory_crfqtsubonly; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_product_category_parent_id` | Parent Product Category | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mprodcat_mprodcatacct` | `m_product_category_acct.(m_product_category_id)` → `m_product_category.(m_product_category_id)` | Product Category Acct |
| incoming | `mprodcategory_crfqtsubonly` | `c_rfq_topicsubscriberonly.(m_product_category_id)` → `m_product_category.(m_product_category_id)` | RfQ Topic Subscriber Restriction |
| incoming | `mprodcategory_mdiscountsbreak` | `m_discountschemabreak.(m_product_category_id)` → `m_product_category.(m_product_category_id)` | Discount Schema Break |
| incoming | `mprodcategory_mdiscountsline` | `m_discountschemaline.(m_product_category_id)` → `m_product_category.(m_product_category_id)` | Discount Price List |

<a id="t-m_product_category_acct"></a>
## `m_product_category_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Category Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Product Category Acct'; 주요 열 p_revenue_acct, p_expense_acct, p_asset_acct, p_cogs_acct; FK cacctschema_mprodcatacct, paveragecostvariance_mproductc; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `p_revenue_acct` | Product Revenue | `numeric(10,0)` |
| `p_expense_acct` | Product Expense | `numeric(10,0)` |
| `p_asset_acct` | Product Asset | `numeric(10,0)` |
| `p_cogs_acct` | Product COGS | `numeric(10,0)` |
| `p_purchasepricevariance_acct` | Purchase Price Variance | `numeric(10,0)` |
| `p_invoicepricevariance_acct` | Invoice Price Variance | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_mprodcatacct` | `m_product_category_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `paveragecostvariance_mproductc` | `m_product_category_acct.(p_averagecostvariance_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `pburden_mproductcategoryacct` | `m_product_category_acct.(p_burden_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `pcostadjustment_mproductcatego` | `m_product_category_acct.(p_costadjustment_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-m_product_category_trl"></a>
## `m_product_category_trl` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Category Trl`
- 사전 Description: Category of a Product
- 근거 문장: 사전 Name='Product Category Trl'; Description='Category of a Product'; 주요 열 근거 부족; FK mproductcategory_mproductcateg; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mproductcategory_mproductcateg` | `m_product_category_trl.(m_product_category_id)` → `m_product_category.(m_product_category_id)` | Product Category |

<a id="t-m_product_po"></a>
## `m_product_po` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Purchasing`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Product Purchasing'; 주요 열 c_uom_id, pricelist, upc; FK c_uom_m_product_po, m_product_productpo; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_uom_id` | UOM | `numeric(10,0)` |
| `pricelist` | List Price | `numeric` |
| `upc` | UPC/EAN | `character varying(20)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `c_uom_m_product_po` | `m_product_po.(c_uom_id)` → `c_uom.(c_uom_id)` | UOM |
| outgoing | `m_product_productpo` | `m_product_po.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_product_qualitytest"></a>
## `m_product_qualitytest` — 품질 시험·규격

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Quality Test`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Product Quality Test'; 주요 열 m_product_id, m_qualitytest_id, expectedresult; FK mqualitytest_mproductqualityte; 사전 의미와 열/FK가 품질 시험·규격를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `quality`를 근거로, 구조 근거가 있는 `quality` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_product_id` | Product | `numeric(10,0)` |
| `m_qualitytest_id` | Quality Test | `numeric(10,0)` |
| `expectedresult` | Expected Result | `character varying(255)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mqualitytest_mproductqualityte` | `m_product_qualitytest.(m_qualitytest_id)` → `m_qualitytest.(m_qualitytest_id)` | Quality Test |

<a id="t-m_product_trl"></a>
## `m_product_trl` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Trl`
- 사전 Description: Product, Service, Item
- 근거 문장: 사전 Name='Product Trl'; Description='Product, Service, Item'; 주요 열 근거 부족; FK mproduct_mproducttrl; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mproduct_mproducttrl` | `m_product_trl.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_productdownload"></a>
## `m_productdownload` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Download`
- 사전 Description: Product downloads
- 근거 문장: 사전 Name='Product Download'; Description='Product downloads'; 주요 열 m_product_id; FK mproduct_mproductdownload; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_product_id` | Product | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mproduct_mproductdownload` | `m_productdownload.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_production"></a>
## `m_production` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Production`
- 사전 Description: Plan for producing a product
- 근거 문장: 사전 Name='Production'; Description='Plan for producing a product'; 주요 열 pp_product_bom_id; FK mproduction_mproductionline, mproduction_plan; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `production`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pp_product_bom_id` | BOM & Formula | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mproduction_mproductionline` | `m_productionline.(m_production_id)` → `m_production.(m_production_id)` | Production Line |
| incoming | `mproduction_plan` | `m_productionplan.(m_production_id)` → `m_production.(m_production_id)` | Production Plan |
| outgoing | `ppproductbom_mproduction` | `m_production.(pp_product_bom_id)` → `pp_product_bom.(pp_product_bom_id)` | BOM & Formula |
| outgoing | `reversal_mproduction` | `m_production.(reversal_id)` → `m_production.(m_production_id)` | Production |

<a id="t-m_productionline"></a>
## `m_productionline` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Production Line`
- 사전 Description: Document Line representing a production
- 근거 문장: 사전 Name='Production Line'; Description='Document Line representing a production'; 주요 열 m_productionplan_id, m_production_id; FK mproductionline_mplinema, mproduction_mproductionline; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `production`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_productionplan_id` | Production Plan | `numeric(10,0)` |
| `m_production_id` | Production | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mproductionline_mplinema` | `m_productionlinema.(m_productionline_id)` → `m_productionline.(m_productionline_id)` | Production Line MA |
| outgoing | `mproduction_mproductionline` | `m_productionline.(m_production_id)` → `m_production.(m_production_id)` | Production |
| outgoing | `mproductionplan_line` | `m_productionline.(m_productionplan_id)` → `m_productionplan.(m_productionplan_id)` | Production Plan |

<a id="t-m_productionlinema"></a>
## `m_productionlinema` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Production Line MA`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Production Line MA'; 주요 열 근거 부족; FK mproductionline_mplinema; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `production`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mproductionline_mplinema` | `m_productionlinema.(m_productionline_id)` → `m_productionline.(m_productionline_id)` | Production Line |

<a id="t-m_productionplan"></a>
## `m_productionplan` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Production Plan`
- 사전 Description: Plan for how a product is produced
- 근거 문장: 사전 Name='Production Plan'; Description='Plan for how a product is produced'; 주요 열 m_production_id; FK mproductionplan_line, mproduction_plan; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `production`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_production_id` | Production | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mproductionplan_line` | `m_productionline.(m_productionplan_id)` → `m_productionplan.(m_productionplan_id)` | Production Line |
| outgoing | `mproduction_plan` | `m_productionplan.(m_production_id)` → `m_production.(m_production_id)` | Production |

<a id="t-m_productoperation"></a>
## `m_productoperation` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Operation`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Product Operation'; 주요 열 m_product_id; FK mproductop_mbomproduct, mproductop_mopresource; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_product_id` | Product | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mproductop_mbomproduct` | `m_bomproduct.(m_productoperation_id)` → `m_productoperation.(m_productoperation_id)` | BOM Component |
| incoming | `mproductop_mopresource` | `m_operationresource.(m_productoperation_id)` → `m_productoperation.(m_productoperation_id)` | Operation Resource |
| outgoing | `mproduct_mproductoperation` | `m_productoperation.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_productprice"></a>
## `m_productprice` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Price`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Product Price'; 주요 열 m_pricelist_version_id, m_product_id, pricelist, pricestd; FK mpricelistver_mproductprice, mproduct_mproductprice; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_pricelist_version_id` | Price List Version | `numeric(10,0)` |
| `m_product_id` | Product | `numeric(10,0)` |
| `pricelist` | List Price | `numeric` |
| `pricestd` | Standard Price | `numeric` |
| `pricelimit` | Limit Price | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mpricelistver_mproductprice` | `m_productprice.(m_pricelist_version_id)` → `m_pricelist_version.(m_pricelist_version_id)` | Price List Version |
| outgoing | `mproduct_mproductprice` | `m_productprice.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_productpricevendorbreak"></a>
## `m_productpricevendorbreak` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Price Break`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Product Price Break'; 주요 열 breakvalue, m_pricelist_version_id, m_product_id, pricelimit; FK mpricelistversion_mproductpric, mproduct_mproductpricevendorbr; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `breakvalue` | Break Value | `numeric` |
| `m_pricelist_version_id` | Price List Version | `numeric(10,0)` |
| `m_product_id` | Product | `numeric(10,0)` |
| `pricelimit` | Limit Price | `numeric` |
| `pricelist` | List Price | `numeric` |
| `pricestd` | Standard Price | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mpricelistversion_mproductpric` | `m_productpricevendorbreak.(m_pricelist_version_id)` → `m_pricelist_version.(m_pricelist_version_id)` | Price List Version |
| outgoing | `mproduct_mproductpricevendorbr` | `m_productpricevendorbreak.(m_product_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_promotion"></a>
## `m_promotion` — 프로모션·마케팅

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Promotion`
- 사전 Description: Promotion setup
- 근거 문장: 사전 Name='Promotion'; Description='Promotion setup'; 주요 열 promotionpriority, c_campaign_id; FK mpromotion_mpromotiondistribut, mpromotion_mpromotionline; 사전 의미와 열/FK가 프로모션·마케팅를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `promotion`를 근거로, 구조 근거가 있는 `promotion` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `promotionpriority` | Relative Priority | `numeric(10,0)` |
| `c_campaign_id` | Campaign | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mpromotion_mpromotiondistribut` | `m_promotiondistribution.(m_promotion_id)` → `m_promotion.(m_promotion_id)` | Promotion Distribution |
| incoming | `mpromotion_mpromotionline` | `m_promotionline.(m_promotion_id)` → `m_promotion.(m_promotion_id)` | Promotion Line |
| incoming | `mpromotion_mpromotionprecondit` | `m_promotionprecondition.(m_promotion_id)` → `m_promotion.(m_promotion_id)` | Promotion Pre Condition |
| incoming | `mpromotion_mpromotionreward` | `m_promotionreward.(m_promotion_id)` → `m_promotion.(m_promotion_id)` | Promotion Reward |

<a id="t-m_promotiondistribution"></a>
## `m_promotiondistribution` — 프로모션·마케팅

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Promotion Distribution`
- 사전 Description: Distribute order line items into multiple bucket for reward calculation
- 근거 문장: 사전 Name='Promotion Distribution'; Description='Distribute order line items into multiple bucket for reward calculation'; 주요 열 m_promotionline_id, m_promotion_id; FK mpromotiondistribution_mpromot, mtargetdistribution_mpromotion; 사전 의미와 열/FK가 프로모션·마케팅를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `promotion`를 근거로, 구조 근거가 있는 `promotion` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_promotionline_id` | Promotion Line | `numeric(10,0)` |
| `m_promotion_id` | Promotion | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mpromotiondistribution_mpromot` | `m_promotionreward.(m_promotiondistribution_id)` → `m_promotiondistribution.(m_promotiondistribution_id)` | Promotion Reward |
| incoming | `mtargetdistribution_mpromotion` | `m_promotionreward.(m_targetdistribution_id)` → `m_promotiondistribution.(m_promotiondistribution_id)` | Promotion Reward |
| outgoing | `mpromotion_mpromotiondistribut` | `m_promotiondistribution.(m_promotion_id)` → `m_promotion.(m_promotion_id)` | Promotion |
| outgoing | `mpromotionline_mpromotiondistr` | `m_promotiondistribution.(m_promotionline_id)` → `m_promotionline.(m_promotionline_id)` | Promotion Line |

<a id="t-m_promotiongroup"></a>
## `m_promotiongroup` — 프로모션·마케팅

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Promotion Group`
- 사전 Description: Grouping of product for promotion setup
- 근거 문장: 사전 Name='Promotion Group'; Description='Grouping of product for promotion setup'; 주요 열 근거 부족; FK mpromotiongroup_mpromotiongrou, mpromotiongroup_mpromotionline; 사전 의미와 열/FK가 프로모션·마케팅를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `promotion`를 근거로, 구조 근거가 있는 `promotion` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mpromotiongroup_mpromotiongrou` | `m_promotiongroupline.(m_promotiongroup_id)` → `m_promotiongroup.(m_promotiongroup_id)` | Promotion Group Line |
| incoming | `mpromotiongroup_mpromotionline` | `m_promotionline.(m_promotiongroup_id)` → `m_promotiongroup.(m_promotiongroup_id)` | Promotion Line |

<a id="t-m_promotiongroupline"></a>
## `m_promotiongroupline` — 프로모션·마케팅

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Promotion Group Line`
- 사전 Description: Line items of a promotion group
- 근거 문장: 사전 Name='Promotion Group Line'; Description='Line items of a promotion group'; 주요 열 m_product_id, m_promotiongroup_id; FK mpromotiongroup_mpromotiongrou; 사전 의미와 열/FK가 프로모션·마케팅를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `promotion`를 근거로, 구조 근거가 있는 `promotion` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_product_id` | Product | `numeric(10,0)` |
| `m_promotiongroup_id` | Promotion Group | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mpromotiongroup_mpromotiongrou` | `m_promotiongroupline.(m_promotiongroup_id)` → `m_promotiongroup.(m_promotiongroup_id)` | Promotion Group |

<a id="t-m_promotionline"></a>
## `m_promotionline` — 프로모션·마케팅

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Promotion Line`
- 사전 Description: Promotion line items
- 근거 문장: 사전 Name='Promotion Line'; Description='Promotion line items'; 주요 열 m_promotiongroup_id, m_promotion_id; FK mpromotionline_mpromotiondistr, mpromotion_mpromotionline; 사전 의미와 열/FK가 프로모션·마케팅를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `promotion`를 근거로, 구조 근거가 있는 `promotion` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_promotiongroup_id` | Promotion Group | `numeric(10,0)` |
| `m_promotion_id` | Promotion | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mpromotionline_mpromotiondistr` | `m_promotiondistribution.(m_promotionline_id)` → `m_promotionline.(m_promotionline_id)` | Promotion Distribution |
| outgoing | `mpromotion_mpromotionline` | `m_promotionline.(m_promotion_id)` → `m_promotion.(m_promotion_id)` | Promotion |
| outgoing | `mpromotiongroup_mpromotionline` | `m_promotionline.(m_promotiongroup_id)` → `m_promotiongroup.(m_promotiongroup_id)` | Promotion Group |

<a id="t-m_promotionprecondition"></a>
## `m_promotionprecondition` — 프로모션·마케팅

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Promotion Pre Condition`
- 사전 Description: Pre condition for promotion
- 근거 문장: 사전 Name='Promotion Pre Condition'; Description='Pre condition for promotion'; 주요 열 c_bpartner_id, enddate, m_promotion_id, promotioncode; FK mpromotion_mpromotionprecondit; 사전 의미와 열/FK가 프로모션·마케팅를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `promotion`를 근거로, 구조 근거가 있는 `promotion` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `enddate` | End Date | `timestamp without time zone` |
| `m_promotion_id` | Promotion | `numeric(10,0)` |
| `promotioncode` | Promotion Code | `character varying(30)` |
| `promotioncounter` | Usage Counter | `numeric(10,0)` |
| `promotionusagelimit` | Usage Limit | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mpromotion_mpromotionprecondit` | `m_promotionprecondition.(m_promotion_id)` → `m_promotion.(m_promotion_id)` | Promotion |

<a id="t-m_promotionreward"></a>
## `m_promotionreward` — 프로모션·마케팅

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Promotion Reward`
- 사전 Description: Setup reward for the promotion
- 근거 문장: 사전 Name='Promotion Reward'; Description='Setup reward for the promotion'; 주요 열 m_promotiondistribution_id, m_promotion_id, rewardtype; FK mpromotion_mpromotionreward, mpromotiondistribution_mpromot; 사전 의미와 열/FK가 프로모션·마케팅를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `promotion`를 근거로, 구조 근거가 있는 `promotion` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_promotiondistribution_id` | Promotion Distribution | `numeric(10,0)` |
| `m_promotion_id` | Promotion | `numeric(10,0)` |
| `rewardtype` | Reward Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mpromotion_mpromotionreward` | `m_promotionreward.(m_promotion_id)` → `m_promotion.(m_promotion_id)` | Promotion |
| outgoing | `mpromotiondistribution_mpromot` | `m_promotionreward.(m_promotiondistribution_id)` → `m_promotiondistribution.(m_promotiondistribution_id)` | Promotion Distribution |
| outgoing | `mtargetdistribution_mpromotion` | `m_promotionreward.(m_targetdistribution_id)` → `m_promotiondistribution.(m_promotiondistribution_id)` | Promotion Distribution |

<a id="t-m_qualitytest"></a>
## `m_qualitytest` — 품질 시험·규격

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Quality Test`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Quality Test'; 주요 열 근거 부족; FK mqualitytest_mproductqualityte, mqualitytest_mqualitytestresul; 사전 의미와 열/FK가 품질 시험·규격를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `quality`를 근거로, 구조 근거가 있는 `quality` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mqualitytest_mproductqualityte` | `m_product_qualitytest.(m_qualitytest_id)` → `m_qualitytest.(m_qualitytest_id)` | Product Quality Test |
| incoming | `mqualitytest_mqualitytestresul` | `m_qualitytestresult.(m_qualitytest_id)` → `m_qualitytest.(m_qualitytest_id)` | Quality Test Result |

<a id="t-m_qualitytestresult"></a>
## `m_qualitytestresult` — 품질 시험·규격

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Quality Test Result`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Quality Test Result'; 주요 열 m_qualitytest_id, result; FK mqualitytest_mqualitytestresul; 사전 의미와 열/FK가 품질 시험·규격를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `quality`를 근거로, 구조 근거가 있는 `quality` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_qualitytest_id` | Quality Test | `numeric(10,0)` |
| `result` | Result | `character varying(255)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mqualitytest_mqualitytestresul` | `m_qualitytestresult.(m_qualitytest_id)` → `m_qualitytest.(m_qualitytest_id)` | Quality Test |

<a id="t-m_relatedproduct"></a>
## `m_relatedproduct` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Related`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Product Related'; 주요 열 근거 부족; FK mproduct_mrelated_product, mproduct_mrelatedproduct; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mproduct_mrelated_product` | `m_relatedproduct.(m_product_id)` → `m_product.(m_product_id)` | Product |
| outgoing | `mproduct_mrelatedproduct` | `m_relatedproduct.(relatedproduct_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_replenish"></a>
## `m_replenish` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_Replenish`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_Replenish'; 주요 열 m_warehousesource_id, m_locator_id; FK m_warehouse_replenish, mlocator_mreplenish; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_warehousesource_id` | Source Warehouse | `numeric(10,0)` |
| `m_locator_id` | Locator | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `m_warehouse_replenish` | `m_replenish.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | Warehouse |
| outgoing | `mlocator_mreplenish` | `m_replenish.(m_locator_id)` → `m_locator.(m_locator_id)` | Locator |
| outgoing | `mwarehousesource_mreplenish` | `m_replenish.(m_warehousesource_id)` → `m_warehouse.(m_warehouse_id)` | Warehouse |

<a id="t-m_requisition"></a>
## `m_requisition` — 주문·수주·발주

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Requisition`
- 사전 Description: Material Requisition
- 근거 문장: 사전 Name='Requisition'; Description='Material Requisition'; 주요 열 m_pricelist_id; FK mrequisition_mrequisitionline; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_pricelist_id` | Price List | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mrequisition_mrequisitionline` | `m_requisitionline.(m_requisition_id)` → `m_requisition.(m_requisition_id)` | Requisition Line |

<a id="t-m_requisitionline"></a>
## `m_requisitionline` — 주문·수주·발주

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Requisition Line`
- 사전 Description: Material Requisition Line
- 근거 문장: 사전 Name='Requisition Line'; Description='Material Requisition Line'; 주요 열 m_requisition_id, c_orderline_id, c_bpartner_id; FK corderline_mrequisitionline, mrequisition_mrequisitionline; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_requisition_id` | Requisition | `numeric(10,0)` |
| `c_orderline_id` | Sales Order Line | `numeric(10,0)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `corderline_mrequisitionline` | `m_requisitionline.(c_orderline_id)` → `c_orderline.(c_orderline_id)` | Sales Order Line |
| outgoing | `mrequisition_mrequisitionline` | `m_requisitionline.(m_requisition_id)` → `m_requisition.(m_requisition_id)` | Requisition |

<a id="t-m_rma"></a>
## `m_rma` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RMA`
- 사전 Description: Return Material Authorization
- 근거 문장: 사전 Name='RMA'; Description='Return Material Authorization'; 주요 열 근거 부족; FK mrma_mrmaline, mrma_mrmatax; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `authorization`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mrma_mrmaline` | `m_rmaline.(m_rma_id)` → `m_rma.(m_rma_id)` | RMA Line |
| incoming | `mrma_mrmatax` | `m_rmatax.(m_rma_id)` → `m_rma.(m_rma_id)` | RMA Tax |
| outgoing | `mrmatype_mrma` | `m_rma.(m_rmatype_id)` → `m_rmatype.(m_rmatype_id)` | RMA Type |
| outgoing | `refrma_mrma` | `m_rma.(ref_rma_id)` → `m_rma.(m_rma_id)` | RMA |

<a id="t-m_rmaline"></a>
## `m_rmaline` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RMA Line`
- 사전 Description: Return Material Authorization Line
- 근거 문장: 사전 Name='RMA Line'; Description='Return Material Authorization Line'; 주요 열 근거 부족; FK mrma_mrmaline, refrmaline_mrmaline; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `authorization`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mrma_mrmaline` | `m_rmaline.(m_rma_id)` → `m_rma.(m_rma_id)` | RMA |
| outgoing | `refrmaline_mrmaline` | `m_rmaline.(ref_rmaline_id)` → `m_rmaline.(m_rmaline_id)` | RMA Line |

<a id="t-m_rmatax"></a>
## `m_rmatax` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RMA Tax`
- 사전 Description: Return Material Authorization Tax
- 근거 문장: 사전 Name='RMA Tax'; Description='Return Material Authorization Tax'; 주요 열 근거 부족; FK mrma_mrmatax; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `authorization`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mrma_mrmatax` | `m_rmatax.(m_rma_id)` → `m_rma.(m_rma_id)` | RMA |

<a id="t-m_rmatype"></a>
## `m_rmatype` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `RMA Type`
- 사전 Description: Return Material Authorization Type
- 근거 문장: 사전 Name='RMA Type'; Description='Return Material Authorization Type'; 주요 열 근거 부족; FK mrmatype_mrma; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `authorization`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mrmatype_mrma` | `m_rma.(m_rmatype_id)` → `m_rmatype.(m_rmatype_id)` | RMA |

<a id="t-m_sernoctl"></a>
## `m_sernoctl` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Serial No Control`
- 사전 Description: Product Serial Number Control
- 근거 문장: 사전 Name='Serial No Control'; Description='Product Serial Number Control'; 주요 열 근거 부족; FK msernoctl_attributeset; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `msernoctl_attributeset` | `m_attributeset.(m_sernoctl_id)` → `m_sernoctl.(m_sernoctl_id)` | Attribute Set |

<a id="t-m_sernoctlexclude"></a>
## `m_sernoctlexclude` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Exclude Ser No`
- 사전 Description: Exclude the ability to create Serial Numbers in Attribute Sets
- 근거 문장: 사전 Name='Exclude Ser No'; Description='Exclude the ability to create Serial Numbers in Attribute Sets'; 주요 열 m_sernoctl_id, ad_table_id, issotrx; FK adtable_msernoctlexclude, msernoctl_msernoctlexclude; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_sernoctl_id` | Serial No Control | `numeric(10,0)` |
| `ad_table_id` | Table | `numeric(10,0)` |
| `issotrx` | Sales Transaction | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_msernoctlexclude` | `m_sernoctlexclude.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `msernoctl_msernoctlexclude` | `m_sernoctlexclude.(m_sernoctl_id)` → `m_sernoctl.(m_sernoctl_id)` | Serial No Control |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_shipper"></a>
## `m_shipper` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipper`
- 사전 Description: Method or manner of product delivery
- 근거 문장: 사전 Name='Shipper'; Description='Method or manner of product delivery'; 주요 열 m_shippingprocessor_id, m_shippercfg_id; FK mshipper_ddnetworkdistribution, mshipper_ddorder; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shippingprocessor_id` | Shipping Processor | `numeric(10,0)` |
| `m_shippercfg_id` | Shipper Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshipper_ddnetworkdistribution` | `dd_networkdistributionline.(m_shipper_id)` → `m_shipper.(m_shipper_id)` | Network Distribution Line |
| incoming | `mshipper_ddorder` | `dd_order.(m_shipper_id)` → `m_shipper.(m_shipper_id)` | Distribution Order |
| incoming | `mshipper_ddorderline` | `dd_orderline.(m_shipper_id)` → `m_shipper.(m_shipper_id)` | Distribution Order Line |
| incoming | `mshipper_mfreight` | `m_freight.(m_shipper_id)` → `m_shipper.(m_shipper_id)` | Freight |

<a id="t-m_shippercfg"></a>
## `m_shippercfg` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipper Configuration`
- 사전 Description: Method or manner of product delivery
- 근거 문장: 사전 Name='Shipper Configuration'; Description='Method or manner of product delivery'; 주요 열 trackingurl, m_shippingprocessorcfg_id; FK mshippercfg_mshipper, mshippercfg_mshipperlabelscfg; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `trackingurl` | Tracking URL | `character varying(120)` |
| `m_shippingprocessorcfg_id` | Shipping Processor Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshippercfg_mshipper` | `m_shipper.(m_shippercfg_id)` → `m_shippercfg.(m_shippercfg_id)` | Shipper |
| incoming | `mshippercfg_mshipperlabelscfg` | `m_shipperlabelscfg.(m_shippercfg_id)` → `m_shippercfg.(m_shippercfg_id)` | Shipper Labels Configuration |
| incoming | `mshippercfg_mshipperpackagingc` | `m_shipperpackagingcfg.(m_shippercfg_id)` → `m_shippercfg.(m_shippercfg_id)` | Shipper Packaging Configuration |
| incoming | `mshippercfg_mshipperpickuptype` | `m_shipperpickuptypescfg.(m_shippercfg_id)` → `m_shippercfg.(m_shippercfg_id)` | Shipper Pickup Types Configuration |

<a id="t-m_shipperlabels"></a>
## `m_shipperlabels` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipper Labels`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Shipper Labels'; 주요 열 m_shipper_id, m_shipperlabelscfg_id; FK mshipperlabels_mpackage, mshipperlabels_mshippingtransa; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shipper_id` | Shipper | `numeric(10,0)` |
| `m_shipperlabelscfg_id` | Shipper Labels Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshipperlabels_mpackage` | `m_package.(m_shipperlabels_id)` → `m_shipperlabels.(m_shipperlabels_id)` | Package |
| incoming | `mshipperlabels_mshippingtransa` | `m_shippingtransaction.(m_shipperlabels_id)` → `m_shipperlabels.(m_shipperlabels_id)` | Shipping Transaction |
| outgoing | `mshipper_mshipperlabels` | `m_shipperlabels.(m_shipper_id)` → `m_shipper.(m_shipper_id)` | Shipper |
| outgoing | `mshipperlabelscfg_mshipperlabe` | `m_shipperlabels.(m_shipperlabelscfg_id)` → `m_shipperlabelscfg.(m_shipperlabelscfg_id)` | Shipper Labels Configuration |

<a id="t-m_shipperlabelscfg"></a>
## `m_shipperlabelscfg` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipper Labels Configuration`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Shipper Labels Configuration'; 주요 열 m_shippercfg_id; FK mshipperlabelscfg_mshipperlabe, mshippercfg_mshipperlabelscfg; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shippercfg_id` | Shipper Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshipperlabelscfg_mshipperlabe` | `m_shipperlabels.(m_shipperlabelscfg_id)` → `m_shipperlabelscfg.(m_shipperlabelscfg_id)` | Shipper Labels |
| outgoing | `mshippercfg_mshipperlabelscfg` | `m_shipperlabelscfg.(m_shippercfg_id)` → `m_shippercfg.(m_shippercfg_id)` | Shipper Configuration |

<a id="t-m_shipperpackaging"></a>
## `m_shipperpackaging` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipper Packaging`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Shipper Packaging'; 주요 열 m_shipper_id, m_shipperpackagingcfg_id; FK mshipperpackaging_mpackage, mshipperpackaging_mshippingtra; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shipper_id` | Shipper | `numeric(10,0)` |
| `m_shipperpackagingcfg_id` | Shipper Packaging Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshipperpackaging_mpackage` | `m_package.(m_shipperpackaging_id)` → `m_shipperpackaging.(m_shipperpackaging_id)` | Package |
| incoming | `mshipperpackaging_mshippingtra` | `m_shippingtransaction.(m_shipperpackaging_id)` → `m_shipperpackaging.(m_shipperpackaging_id)` | Shipping Transaction |
| outgoing | `mshipper_mshipperpackaging` | `m_shipperpackaging.(m_shipper_id)` → `m_shipper.(m_shipper_id)` | Shipper |
| outgoing | `mshipperpackagingcfg_mshipperp` | `m_shipperpackaging.(m_shipperpackagingcfg_id)` → `m_shipperpackagingcfg.(m_shipperpackagingcfg_id)` | Shipper Packaging Configuration |

<a id="t-m_shipperpackagingcfg"></a>
## `m_shipperpackagingcfg` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipper Packaging Configuration`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Shipper Packaging Configuration'; 주요 열 m_shippercfg_id; FK mshipperpackagingcfg_mshipperp, mshippercfg_mshipperpackagingc; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shippercfg_id` | Shipper Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshipperpackagingcfg_mshipperp` | `m_shipperpackaging.(m_shipperpackagingcfg_id)` → `m_shipperpackagingcfg.(m_shipperpackagingcfg_id)` | Shipper Packaging |
| outgoing | `mshippercfg_mshipperpackagingc` | `m_shipperpackagingcfg.(m_shippercfg_id)` → `m_shippercfg.(m_shippercfg_id)` | Shipper Configuration |

<a id="t-m_shipperpickuptypes"></a>
## `m_shipperpickuptypes` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipper Pickup Types`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Shipper Pickup Types'; 주요 열 m_shipper_id, m_shipperpickuptypescfg_id; FK mshipperpickuptypes_mpackage, mshipperpickuptypes_mshippingt; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shipper_id` | Shipper | `numeric(10,0)` |
| `m_shipperpickuptypescfg_id` | Shipper Pickup Types Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshipperpickuptypes_mpackage` | `m_package.(m_shipperpickuptypes_id)` → `m_shipperpickuptypes.(m_shipperpickuptypes_id)` | Package |
| incoming | `mshipperpickuptypes_mshippingt` | `m_shippingtransaction.(m_shipperpickuptypes_id)` → `m_shipperpickuptypes.(m_shipperpickuptypes_id)` | Shipping Transaction |
| outgoing | `mshipper_mshipperpickuptypes` | `m_shipperpickuptypes.(m_shipper_id)` → `m_shipper.(m_shipper_id)` | Shipper |
| outgoing | `mshipperpickuptypescfg_mshippe` | `m_shipperpickuptypes.(m_shipperpickuptypescfg_id)` → `m_shipperpickuptypescfg.(m_shipperpickuptypescfg_id)` | Shipper Pickup Types Configuration |

<a id="t-m_shipperpickuptypescfg"></a>
## `m_shipperpickuptypescfg` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipper Pickup Types Configuration`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Shipper Pickup Types Configuration'; 주요 열 m_shippercfg_id; FK mshipperpickuptypescfg_mshippe, mshippercfg_mshipperpickuptype; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shippercfg_id` | Shipper Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshipperpickuptypescfg_mshippe` | `m_shipperpickuptypes.(m_shipperpickuptypescfg_id)` → `m_shipperpickuptypescfg.(m_shipperpickuptypescfg_id)` | Shipper Pickup Types |
| outgoing | `mshippercfg_mshipperpickuptype` | `m_shipperpickuptypescfg.(m_shippercfg_id)` → `m_shippercfg.(m_shippercfg_id)` | Shipper Configuration |

<a id="t-m_shippingprocessor"></a>
## `m_shippingprocessor` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipping Processor`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Shipping Processor'; 주요 열 m_shippingprocessorcfg_id; FK mshippingprocessor_cbpshipping, mshippingprocessor_mshipper; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shippingprocessorcfg_id` | Shipping Processor Configuration | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshippingprocessor_cbpshipping` | `c_bp_shippingacct.(m_shippingprocessor_id)` → `m_shippingprocessor.(m_shippingprocessor_id)` | Business Partner Shipping Account |
| incoming | `mshippingprocessor_mshipper` | `m_shipper.(m_shippingprocessor_id)` → `m_shippingprocessor.(m_shippingprocessor_id)` | Shipper |
| incoming | `mshippingprocessor_mshippingtr` | `m_shippingtransaction.(m_shippingprocessor_id)` → `m_shippingprocessor.(m_shippingprocessor_id)` | Shipping Transaction |
| outgoing | `mshippingprocessorcfg_mshippin` | `m_shippingprocessor.(m_shippingprocessorcfg_id)` → `m_shippingprocessorcfg.(m_shippingprocessorcfg_id)` | Shipping Processor Configuration |

<a id="t-m_shippingprocessorcfg"></a>
## `m_shippingprocessorcfg` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipping Processor Configuration`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Shipping Processor Configuration'; 주요 열 근거 부족; FK mshippingprocessorcfg_mshipper, mshippingprocessorcfg_mshippin; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshippingprocessorcfg_mshipper` | `m_shippercfg.(m_shippingprocessorcfg_id)` → `m_shippingprocessorcfg.(m_shippingprocessorcfg_id)` | Shipper Configuration |
| incoming | `mshippingprocessorcfg_mshippin` | `m_shippingprocessor.(m_shippingprocessorcfg_id)` → `m_shippingprocessorcfg.(m_shippingprocessorcfg_id)` | Shipping Processor |

<a id="t-m_shippingtransaction"></a>
## `m_shippingtransaction` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipping Transaction`
- 사전 Description: Shipping Transaction
- 근거 문장: 사전 Name='Shipping Transaction'; Description='Shipping Transaction'; 주요 열 freightcharges, isfuturedayshipment, m_inout_id, m_package_id; FK mshippingtransaction_mshipping, cbpshippingacct_mshippingtrans; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `freightcharges` | Freight Charges | `character varying(10)` |
| `isfuturedayshipment` | Future Day Shipment | `character(1)` |
| `m_inout_id` | Shipment/Receipt | `numeric(10,0)` |
| `m_package_id` | Package | `numeric(10,0)` |
| `m_shipper_id` | Shipper | `numeric(10,0)` |
| `m_shipperlabels_id` | Shipper Labels | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mshippingtransaction_mshipping` | `m_shippingtransactionline.(m_shippingtransaction_id)` → `m_shippingtransaction.(m_shippingtransaction_id)` | Shipping Transaction Line |
| outgoing | `cbpshippingacct_mshippingtrans` | `m_shippingtransaction.(c_bp_shippingacct_id)` → `c_bp_shippingacct.(c_bp_shippingacct_id)` | Business Partner Shipping Account |
| outgoing | `minout_mshippingtransaction` | `m_shippingtransaction.(m_inout_id)` → `m_inout.(m_inout_id)` | Shipment/Receipt |
| outgoing | `mpackage_mshippingtransaction` | `m_shippingtransaction.(m_package_id)` → `m_package.(m_package_id)` | Package |

<a id="t-m_shippingtransactionline"></a>
## `m_shippingtransactionline` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Shipping Transaction Line`
- 사전 Description: Shipping Transaction Line
- 근거 문장: 사전 Name='Shipping Transaction Line'; Description='Shipping Transaction Line'; 주요 열 m_shippingtransaction_id, mastertrackingno, trackingno, m_packagemps_id; FK mpackagemps_mshippingtransacti, mshippingtransaction_mshipping; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_shippingtransaction_id` | Shipping Transaction | `numeric(10,0)` |
| `mastertrackingno` | Master Tracking No | `character varying(255)` |
| `trackingno` | Tracking No | `character varying(255)` |
| `m_packagemps_id` | Package MPS | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mpackagemps_mshippingtransacti` | `m_shippingtransactionline.(m_packagemps_id)` → `m_packagemps.(m_packagemps_id)` | Package MPS |
| outgoing | `mshippingtransaction_mshipping` | `m_shippingtransactionline.(m_shippingtransaction_id)` → `m_shippingtransaction.(m_shippingtransaction_id)` | Shipping Transaction |

<a id="t-m_storageonhand"></a>
## `m_storageonhand` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_StorageOnHand`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_StorageOnHand'; 주요 열 qtyonhand; FK mlocator_mstorageonhand; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `qtyonhand` | On Hand Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mlocator_mstorageonhand` | `m_storageonhand.(m_locator_id)` → `m_locator.(m_locator_id)` | Locator |

<a id="t-m_storagereservation"></a>
## `m_storagereservation` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_StorageReservation`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_StorageReservation'; 주요 열 근거 부족; FK mwarehouse_mstoragereservation; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mwarehouse_mstoragereservation` | `m_storagereservation.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | Warehouse |

<a id="t-m_storagereservationlog"></a>
## `m_storagereservationlog` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Storage Reservation Log`
- 사전 Description: Log for every storage reservation quantity change
- 근거 문장: 사전 Name='Storage Reservation Log'; Description='Log for every storage reservation quantity change'; 주요 열 m_warehouse_id; FK mwh_mstoragereservationlog; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_warehouse_id` | Warehouse | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mwh_mstoragereservationlog` | `m_storagereservationlog.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | Warehouse |

<a id="t-m_substitute"></a>
## `m_substitute` — 상품·속성·가격·단위

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_Substitute`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_Substitute'; 주요 열 근거 부족; FK mproduct_substitute, mproduct_substitutesub; 사전 의미와 열/FK가 상품·속성·가격·단위를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mproduct_substitute` | `m_substitute.(m_product_id)` → `m_product.(m_product_id)` | Product |
| outgoing | `mproduct_substitutesub` | `m_substitute.(substitute_id)` → `m_product.(m_product_id)` | Product |

<a id="t-m_transaction"></a>
## `m_transaction` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Inventory Transaction`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Inventory Transaction'; 주요 열 m_locator_id, movementqty, m_inventoryline_id; FK minventoryline_mtransaction, mlocator_minventorycount; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_locator_id` | Locator | `numeric(10,0)` |
| `movementqty` | Movement Quantity | `numeric` |
| `m_inventoryline_id` | Phys.Inventory Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `minventoryline_mtransaction` | `m_transaction.(m_inventoryline_id)` → `m_inventoryline.(m_inventoryline_id)` | Phys.Inventory Line |
| outgoing | `mlocator_minventorycount` | `m_transaction.(m_locator_id)` → `m_locator.(m_locator_id)` | Locator |
| outgoing | `mmovementline_mtransaction` | `m_transaction.(m_movementline_id)` → `m_movementline.(m_movementline_id)` | Move Line |

<a id="t-m_transactionallocation"></a>
## `m_transactionallocation` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_TransactionAllocation`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_TransactionAllocation'; 주요 열 m_product_id, m_attributesetinstance_id, isallocated, qty; FK mattributesetinst_mtrxalloc, minoutline_mtrxalloc; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_product_id` | Product | `numeric(10,0)` |
| `m_attributesetinstance_id` | Attribute Set Instance | `numeric(10,0)` |
| `isallocated` | Allocated | `character(1)` |
| `qty` | Quantity | `numeric` |
| `ismanual` | Manual | `character(1)` |
| `m_inoutline_id` | Shipment/Receipt Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mattributesetinst_mtrxalloc` | `m_transactionallocation.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |
| outgoing | `minoutline_mtrxalloc` | `m_transactionallocation.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Shipment/Receipt Line |
| outgoing | `minoutlineout_mtrxalloc` | `m_transactionallocation.(out_m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Shipment/Receipt Line |
| outgoing | `minventoryline_mtrxalloc` | `m_transactionallocation.(m_inventoryline_id)` → `m_inventoryline.(m_inventoryline_id)` | Phys.Inventory Line |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-m_warehouse"></a>
## `m_warehouse` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Warehouse`
- 사전 Description: Storage Warehouse and Service Point
- 근거 문장: 사전 Name='Warehouse'; Description='Storage Warehouse and Service Point'; 주요 열 m_warehousesource_id; FK m_warehouse_locator, m_warehouse_replenish; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_warehousesource_id` | Source Warehouse | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `m_warehouse_locator` | `m_locator.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | Locator |
| incoming | `m_warehouse_replenish` | `m_replenish.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | M_Replenish |
| incoming | `m_warehouse_warehouse_acct` | `m_warehouse_acct.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | M_Warehouse_Acct |
| incoming | `mwarehouse_iinventory` | `i_inventory.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | Import Inventory |

<a id="t-m_warehouse_acct"></a>
## `m_warehouse_acct` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `M_Warehouse_Acct`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='M_Warehouse_Acct'; 주요 열 w_inventory_acct, w_invactualadjust_acct, w_differences_acct, w_revaluation_acct; FK cacctschema_mwarehouseacct, vc_wdifferences_mwarehouse; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `w_inventory_acct` | (Not Used) | `numeric(10,0)` |
| `w_invactualadjust_acct` | Inventory Adjustment | `numeric(10,0)` |
| `w_differences_acct` | Warehouse Differences | `numeric(10,0)` |
| `w_revaluation_acct` | Inventory Revaluation | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cacctschema_mwarehouseacct` | `m_warehouse_acct.(c_acctschema_id)` → `c_acctschema.(c_acctschema_id)` | Accounting Schema |
| outgoing | `vc_wdifferences_mwarehouse` | `m_warehouse_acct.(w_differences_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_winvactualadjust_mwarehouse` | `m_warehouse_acct.(w_invactualadjust_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |
| outgoing | `vc_winventory_mwarehouse` | `m_warehouse_acct.(w_inventory_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

<a id="t-mfa_method"></a>
## `mfa_method` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `MFA Method`
- 사전 Description: Multi-factor Authentication Method
- 근거 문장: 사전 Name='MFA Method'; Description='Multi-factor Authentication Method'; 주요 열 근거 부족; FK mfamethod_mfaregistration, mfamethod_mfarule; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `mfa`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `mfamethod_mfaregistration` | `mfa_registration.(mfa_method_id)` → `mfa_method.(mfa_method_id)` | MFA Registration |
| incoming | `mfamethod_mfarule` | `mfa_rule.(mfa_method_id)` → `mfa_method.(mfa_method_id)` | MFA Rule |

<a id="t-mfa_registereddevice"></a>
## `mfa_registereddevice` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `MFA Registered Device`
- 사전 Description: Multi-factor Authentication Registered Device
- 근거 문장: 사전 Name='MFA Registered Device'; Description='Multi-factor Authentication Registered Device'; 주요 열 ad_user_id; FK aduser_mfaregistereddevice; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `mfa`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_user_id` | User/Contact | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_mfaregistereddevice` | `mfa_registereddevice.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-mfa_registration"></a>
## `mfa_registration` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `MFA Registration`
- 사전 Description: Multi-factor Authentication Registration
- 근거 문장: 사전 Name='MFA Registration'; Description='Multi-factor Authentication Registration'; 주요 열 mfa_method_id, ad_user_id; FK aduser_mfaregistration, mfamethod_mfaregistration; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `mfa`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `mfa_method_id` | MFA Method | `numeric(10,0)` |
| `ad_user_id` | User/Contact | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_mfaregistration` | `mfa_registration.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `mfamethod_mfaregistration` | `mfa_registration.(mfa_method_id)` → `mfa_method.(mfa_method_id)` | MFA Method |

<a id="t-mfa_rule"></a>
## `mfa_rule` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `MFA Rule`
- 사전 Description: Multi-factor Authentication Rule
- 근거 문장: 사전 Name='MFA Rule'; Description='Multi-factor Authentication Rule'; 주요 열 mfa_method_id; FK mfamethod_mfarule; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `mfa`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `mfa_method_id` | MFA Method | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mfamethod_mfarule` | `mfa_rule.(mfa_method_id)` → `mfa_method.(mfa_method_id)` | MFA Method |

<a id="t-pa_achievement"></a>
## `pa_achievement` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Achievement`
- 사전 Description: Performance Achievement
- 근거 문장: 사전 Name='Achievement'; Description='Performance Achievement'; 주요 열 pa_measure_id; FK pameasure_paachievement; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_measure_id` | Measure | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pameasure_paachievement` | `pa_achievement.(pa_measure_id)` → `pa_measure.(pa_measure_id)` | Measure |

<a id="t-pa_benchmark"></a>
## `pa_benchmark` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Benchmark`
- 사전 Description: Performance Benchmark
- 근거 문장: 사전 Name='Benchmark'; Description='Performance Benchmark'; 주요 열 근거 부족; FK pabenchmark_pabenchmarkdata, pabenchmark_pameasure; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pabenchmark_pabenchmarkdata` | `pa_benchmarkdata.(pa_benchmark_id)` → `pa_benchmark.(pa_benchmark_id)` | Benchmark Data |
| incoming | `pabenchmark_pameasure` | `pa_measure.(pa_benchmark_id)` → `pa_benchmark.(pa_benchmark_id)` | Measure |

<a id="t-pa_benchmarkdata"></a>
## `pa_benchmarkdata` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Benchmark Data`
- 사전 Description: Performance Benchmark Data Point
- 근거 문장: 사전 Name='Benchmark Data'; Description='Performance Benchmark Data Point'; 주요 열 pa_benchmark_id, benchmarkdate, benchmarkvalue; FK pabenchmark_pabenchmarkdata; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_benchmark_id` | Benchmark | `numeric(10,0)` |
| `benchmarkdate` | Date | `timestamp without time zone` |
| `benchmarkvalue` | Value | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pabenchmark_pabenchmarkdata` | `pa_benchmarkdata.(pa_benchmark_id)` → `pa_benchmark.(pa_benchmark_id)` | Benchmark |

<a id="t-pa_colorschema"></a>
## `pa_colorschema` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Color Schema`
- 사전 Description: Performance Color Schema
- 근거 문장: 사전 Name='Color Schema'; Description='Performance Color Schema'; 주요 열 ad_printcolor1_id, ad_printcolor2_id, ad_printcolor3_id, ad_printcolor4_id; FK adprintcolor1_pacolorschema, adprintcolor2_pacolorschema; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_printcolor1_id` | Color 1 | `numeric(10,0)` |
| `ad_printcolor2_id` | Color 2 | `numeric(10,0)` |
| `ad_printcolor3_id` | Color 3 | `numeric(10,0)` |
| `ad_printcolor4_id` | Color 4 | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adprintcolor1_pacolorschema` | `pa_colorschema.(ad_printcolor1_id)` → `ad_printcolor.(ad_printcolor_id)` | Print Color |
| outgoing | `adprintcolor2_pacolorschema` | `pa_colorschema.(ad_printcolor2_id)` → `ad_printcolor.(ad_printcolor_id)` | Print Color |
| outgoing | `adprintcolor3_pacolorschema` | `pa_colorschema.(ad_printcolor3_id)` → `ad_printcolor.(ad_printcolor_id)` | Print Color |
| outgoing | `adprintcolor4_pacolorschema` | `pa_colorschema.(ad_printcolor4_id)` → `ad_printcolor.(ad_printcolor_id)` | Print Color |

<a id="t-pa_dashboardcontent"></a>
## `pa_dashboardcontent` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dashboard Content`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Dashboard Content'; 주요 열 pa_goal_id, goaldisplay, isembedreportcontent, ad_chart_id; FK padashboardcontacc_padashboard, padashboardcontent_padashboard; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `dashboard`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_goal_id` | Goal | `numeric(10,0)` |
| `goaldisplay` | Goal Display | `character(1)` |
| `isembedreportcontent` | Embed Report Content | `character(1)` |
| `ad_chart_id` | Chart | `numeric(10,0)` |
| `ad_printformat_id` | Print Format | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `padashboardcontacc_padashboard` | `pa_dashboardcontent_access.(pa_dashboardcontent_id)` → `pa_dashboardcontent.(pa_dashboardcontent_id)` | PA_DashboardContent_Access_ID |
| incoming | `padashboardcontent_padashboard` | `pa_dashboardcontent_trl.(pa_dashboardcontent_id)` → `pa_dashboardcontent.(pa_dashboardcontent_id)` | Dashboard Content Trl |
| incoming | `padashboardcontent_padashpref` | `pa_dashboardpreference.(pa_dashboardcontent_id)` → `pa_dashboardcontent.(pa_dashboardcontent_id)` | Dashboard Preference |
| outgoing | `adchart_padashboardcontent` | `pa_dashboardcontent.(ad_chart_id)` → `ad_chart.(ad_chart_id)` | Chart |

<a id="t-pa_dashboardcontent_access"></a>
## `pa_dashboardcontent_access` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `PA_DashboardContent_Access_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='PA_DashboardContent_Access_ID'; 주요 열 pa_dashboardcontent_id; FK padashboardcontacc_padashboard; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `dashboard`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_dashboardcontent_id` | Dashboard Content | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `padashboardcontacc_padashboard` | `pa_dashboardcontent_access.(pa_dashboardcontent_id)` → `pa_dashboardcontent.(pa_dashboardcontent_id)` | Dashboard Content |

<a id="t-pa_dashboardcontent_trl"></a>
## `pa_dashboardcontent_trl` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dashboard Content Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Dashboard Content Trl'; 주요 열 근거 부족; FK padashboardcontent_padashboard; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `dashboard`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `padashboardcontent_padashboard` | `pa_dashboardcontent_trl.(pa_dashboardcontent_id)` → `pa_dashboardcontent.(pa_dashboardcontent_id)` | Dashboard Content |

<a id="t-pa_dashboardpreference"></a>
## `pa_dashboardpreference` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Dashboard Preference`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Dashboard Preference'; 주요 열 pa_dashboardcontent_id; FK padashboardcontent_padashpref; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `dashboard`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_dashboardcontent_id` | Dashboard Content | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `padashboardcontent_padashpref` | `pa_dashboardpreference.(pa_dashboardcontent_id)` → `pa_dashboardcontent.(pa_dashboardcontent_id)` | Dashboard Content |

<a id="t-pa_documentstatus"></a>
## `pa_documentstatus` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Document Status`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Document Status'; 주요 열 ad_role_id, ad_user_id, c_project_id, seqno; FK adfieldgroup_padocumentstatus, adform_padocumentstatus; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_role_id` | Role | `numeric(10,0)` |
| `ad_user_id` | User/Contact | `numeric(10,0)` |
| `c_project_id` | Project | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |
| `name_printcolor_id` | Print Color for Name | `numeric(10,0)` |
| `name_printfont_id` | Print Font for Name | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adfieldgroup_padocumentstatus` | `pa_documentstatus.(ad_fieldgroup_id)` → `ad_fieldgroup.(ad_fieldgroup_id)` | Field Group |
| outgoing | `adform_padocumentstatus` | `pa_documentstatus.(ad_form_id)` → `ad_form.(ad_form_id)` | Special Form |
| outgoing | `adinfowindow_padocumentstatus` | `pa_documentstatus.(ad_infowindow_id)` → `ad_infowindow.(ad_infowindow_id)` | Info Window |
| outgoing | `adprocess_padocumentstatus` | `pa_documentstatus.(ad_process_id)` → `ad_process.(ad_process_id)` | Process |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-pa_documentstatus_trl"></a>
## `pa_documentstatus_trl` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Document Status Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Document Status Trl'; 주요 열 istranslated; FK adlanguage_padocumentstatustrl, padocumentstatus_padocumentsta; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istranslated` | Translated | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlanguage_padocumentstatustrl` | `pa_documentstatus_trl.(ad_language)` → `ad_language.(ad_language)` | Language ID |
| outgoing | `padocumentstatus_padocumentsta` | `pa_documentstatus_trl.(pa_documentstatus_id)` → `pa_documentstatus.(pa_documentstatus_id)` | Document Status |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-pa_documentstatusaccess"></a>
## `pa_documentstatusaccess` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Document Status Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Document Status Access'; 주요 열 ad_role_id, ad_user_id; FK adrole_padocumentstatusaccess, aduser_padocumentstatusaccess; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `access`를 근거로, 구조 근거가 있는 `identity` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_role_id` | Role | `numeric(10,0)` |
| `ad_user_id` | User/Contact | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_padocumentstatusaccess` | `pa_documentstatusaccess.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |
| outgoing | `aduser_padocumentstatusaccess` | `pa_documentstatusaccess.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-pa_goal"></a>
## `pa_goal` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Goal`
- 사전 Description: Performance Goal
- 근거 문장: 사전 Name='Goal'; Description='Performance Goal'; 주요 열 pa_colorschema_id, pa_goalparent_id, pa_measure_id, measuretarget; FK pagoal_padashboardcontent, pagoal_pagoalrestriction; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_colorschema_id` | Color Schema | `numeric(10,0)` |
| `pa_goalparent_id` | Parent Goal | `numeric(10,0)` |
| `pa_measure_id` | Measure | `numeric(10,0)` |
| `measuretarget` | Measure Target | `numeric` |
| `measurescope` | Measure Scope | `character(1)` |
| `measuredisplay` | Measure Display | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pagoal_padashboardcontent` | `pa_dashboardcontent.(pa_goal_id)` → `pa_goal.(pa_goal_id)` | Dashboard Content |
| incoming | `pagoal_pagoalrestriction` | `pa_goalrestriction.(pa_goal_id)` → `pa_goal.(pa_goal_id)` | Goal Restriction |
| outgoing | `pacolorschema_pagoal` | `pa_goal.(pa_colorschema_id)` → `pa_colorschema.(pa_colorschema_id)` | Color Schema |
| outgoing | `pagoalparent_pagoal` | `pa_goal.(pa_goalparent_id)` → `pa_goal.(pa_goal_id)` | Goal |

<a id="t-pa_goalrestriction"></a>
## `pa_goalrestriction` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Goal Restriction`
- 사전 Description: Performance Goal Restriction
- 근거 문장: 사전 Name='Goal Restriction'; Description='Performance Goal Restriction'; 주요 열 goalrestrictiontype, pa_goal_id; FK pagoal_pagoalrestriction; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `goalrestrictiontype` | Restriction Type | `character(1)` |
| `pa_goal_id` | Goal | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pagoal_pagoalrestriction` | `pa_goalrestriction.(pa_goal_id)` → `pa_goal.(pa_goal_id)` | Goal |

<a id="t-pa_hierarchy"></a>
## `pa_hierarchy` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Reporting Hierarchy`
- 사전 Description: Reporting Hierarchy
- 근거 문장: 사전 Name='Reporting Hierarchy'; Description='Reporting Hierarchy'; 주요 열 근거 부족; FK pahierarchy_pameasure; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `reporting`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pahierarchy_pameasure` | `pa_measure.(pa_hierarchy_id)` → `pa_hierarchy.(pa_hierarchy_id)` | Measure |

<a id="t-pa_measure"></a>
## `pa_measure` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Measure`
- 사전 Description: Concrete Performance Measurement
- 근거 문장: 사전 Name='Measure'; Description='Concrete Performance Measurement'; 주요 열 measuretype, calculationclass, pa_measurecalc_id, pa_benchmark_id; FK pameasure_paachievement, pameasure_pagoal; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `measuretype` | Measure Type | `character(1)` |
| `calculationclass` | Calculation Class | `character varying(60)` |
| `pa_measurecalc_id` | Measure Calculation | `numeric(10,0)` |
| `pa_benchmark_id` | Benchmark | `numeric(10,0)` |
| `pa_ratio_id` | Ratio | `numeric(10,0)` |
| `measuredatatype` | Measure Data Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pameasure_paachievement` | `pa_achievement.(pa_measure_id)` → `pa_measure.(pa_measure_id)` | Achievement |
| incoming | `pameasure_pagoal` | `pa_goal.(pa_measure_id)` → `pa_measure.(pa_measure_id)` | Goal |
| outgoing | `pabenchmark_pameasure` | `pa_measure.(pa_benchmark_id)` → `pa_benchmark.(pa_benchmark_id)` | Benchmark |
| outgoing | `pahierarchy_pameasure` | `pa_measure.(pa_hierarchy_id)` → `pa_hierarchy.(pa_hierarchy_id)` | Reporting Hierarchy |

<a id="t-pa_measurecalc"></a>
## `pa_measurecalc` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Measure Calculation`
- 사전 Description: Calculation method for measuring performance
- 근거 문장: 사전 Name='Measure Calculation'; Description='Calculation method for measuring performance'; 주요 열 selectclause, whereclause; FK pameasurecalc_pameasure, pameasurecalc_paratioelement; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `selectclause` | Sql SELECT | `character varying(2000)` |
| `whereclause` | Sql WHERE | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pameasurecalc_pameasure` | `pa_measure.(pa_measurecalc_id)` → `pa_measurecalc.(pa_measurecalc_id)` | Measure |
| incoming | `pameasurecalc_paratioelement` | `pa_ratioelement.(pa_measurecalc_id)` → `pa_measurecalc.(pa_measurecalc_id)` | Ratio Element |

<a id="t-pa_ratio"></a>
## `pa_ratio` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Ratio`
- 사전 Description: Performace Ratio
- 근거 문장: 사전 Name='Ratio'; Description='Performace Ratio'; 주요 열 근거 부족; FK paratio_pameasure, paratio_paratioelement; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `paratio_pameasure` | `pa_measure.(pa_ratio_id)` → `pa_ratio.(pa_ratio_id)` | Measure |
| incoming | `paratio_paratioelement` | `pa_ratioelement.(pa_ratio_id)` → `pa_ratio.(pa_ratio_id)` | Ratio Element |
| incoming | `paratioused_paratioelement` | `pa_ratioelement.(pa_ratioused_id)` → `pa_ratio.(pa_ratio_id)` | Ratio Element |

<a id="t-pa_ratioelement"></a>
## `pa_ratioelement` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Ratio Element`
- 사전 Description: Performance Ratio Element
- 근거 문장: 사전 Name='Ratio Element'; Description='Performance Ratio Element'; 주요 열 pa_ratio_id, ratiooperand, ratioelementtype, pa_ratioused_id; FK pameasurecalc_paratioelement, paratio_paratioelement; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_ratio_id` | Ratio | `numeric(10,0)` |
| `ratiooperand` | Operand | `character(1)` |
| `ratioelementtype` | Element Type | `character(1)` |
| `pa_ratioused_id` | Ratio Used | `numeric(10,0)` |
| `pa_measurecalc_id` | Measure Calculation | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pameasurecalc_paratioelement` | `pa_ratioelement.(pa_measurecalc_id)` → `pa_measurecalc.(pa_measurecalc_id)` | Measure Calculation |
| outgoing | `paratio_paratioelement` | `pa_ratioelement.(pa_ratio_id)` → `pa_ratio.(pa_ratio_id)` | Ratio |
| outgoing | `paratioused_paratioelement` | `pa_ratioelement.(pa_ratioused_id)` → `pa_ratio.(pa_ratio_id)` | Ratio |

<a id="t-pa_report"></a>
## `pa_report` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Financial Report`
- 사전 Description: Financial Report
- 근거 문장: 사전 Name='Financial Report'; Description='Financial Report'; 주요 열 pa_reportlineset_id, pa_reportcolumnset_id, ad_printformat_id, pa_reportcube_id; FK jasperprocess_pareport, pareport_columnset; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_reportlineset_id` | Report Line Set | `numeric(10,0)` |
| `pa_reportcolumnset_id` | Report Column Set | `numeric(10,0)` |
| `ad_printformat_id` | Print Format | `numeric(10,0)` |
| `pa_reportcube_id` | Report Cube | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `jasperprocess_pareport` | `pa_report.(jasperprocess_id)` → `ad_process.(ad_process_id)` | Process |
| outgoing | `pareport_columnset` | `pa_report.(pa_reportcolumnset_id)` → `pa_reportcolumnset.(pa_reportcolumnset_id)` | Report Column Set |
| outgoing | `pareport_lineset` | `pa_report.(pa_reportlineset_id)` → `pa_reportlineset.(pa_reportlineset_id)` | Report Line Set |
| outgoing | `pareportcube_pareport` | `pa_report.(pa_reportcube_id)` → `pa_reportcube.(pa_reportcube_id)` | Report Cube |

<a id="t-pa_reportcolumn"></a>
## `pa_reportcolumn` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report Column`
- 사전 Description: Column in Report
- 근거 문장: 사전 Name='Report Column'; Description='Column in Report'; 주요 열 pa_reportcolumnset_id, calculationtype; FK pareportcolumn_pareportcolumnt, pareportcolumn_oper1; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_reportcolumnset_id` | Report Column Set | `numeric(10,0)` |
| `calculationtype` | Calculation | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pareportcolumn_pareportcolumnt` | `pa_reportcolumn_trl.(pa_reportcolumn_id)` → `pa_reportcolumn.(pa_reportcolumn_id)` | Report Column Trl |
| outgoing | `pareportcolumn_oper1` | `pa_reportcolumn.(oper_1_id)` → `pa_reportcolumn.(pa_reportcolumn_id)` | Report Column |
| outgoing | `pareportcolumn_oper2` | `pa_reportcolumn.(oper_2_id)` → `pa_reportcolumn.(pa_reportcolumn_id)` | Report Column |
| outgoing | `pareportcolumnset_column` | `pa_reportcolumn.(pa_reportcolumnset_id)` → `pa_reportcolumnset.(pa_reportcolumnset_id)` | Report Column Set |

<a id="t-pa_reportcolumn_trl"></a>
## `pa_reportcolumn_trl` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report Column Trl`
- 사전 Description: Column in Report
- 근거 문장: 사전 Name='Report Column Trl'; Description='Column in Report'; 주요 열 근거 부족; FK pareportcolumn_pareportcolumnt; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pareportcolumn_pareportcolumnt` | `pa_reportcolumn_trl.(pa_reportcolumn_id)` → `pa_reportcolumn.(pa_reportcolumn_id)` | Report Column |

<a id="t-pa_reportcolumnset"></a>
## `pa_reportcolumnset` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report Column Set`
- 사전 Description: Collection of Columns for Report
- 근거 문장: 사전 Name='Report Column Set'; Description='Collection of Columns for Report'; 주요 열 근거 부족; FK pareport_columnset, pareportcolumnset_column; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pareport_columnset` | `pa_report.(pa_reportcolumnset_id)` → `pa_reportcolumnset.(pa_reportcolumnset_id)` | Financial Report |
| incoming | `pareportcolumnset_column` | `pa_reportcolumn.(pa_reportcolumnset_id)` → `pa_reportcolumnset.(pa_reportcolumnset_id)` | Report Column |

<a id="t-pa_reportcube"></a>
## `pa_reportcube` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report Cube`
- 사전 Description: Define reporting cube for pre-calculation of summary accounting data.
- 근거 문장: 사전 Name='Report Cube'; Description='Define reporting cube for pre-calculation of summary accounting data.'; 주요 열 근거 부족; FK pareportcube_pareport; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pareportcube_pareport` | `pa_report.(pa_reportcube_id)` → `pa_reportcube.(pa_reportcube_id)` | Financial Report |

<a id="t-pa_reportline"></a>
## `pa_reportline` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report Line`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Report Line'; 주요 열 pa_reportlineset_id, calculationtype; FK pareportline_ireportline, pareportline_pareportlinetrl; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_reportlineset_id` | Report Line Set | `numeric(10,0)` |
| `calculationtype` | Calculation | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pareportline_ireportline` | `i_reportline.(pa_reportline_id)` → `pa_reportline.(pa_reportline_id)` | Import Report Line Set |
| incoming | `pareportline_pareportlinetrl` | `pa_reportline_trl.(pa_reportline_id)` → `pa_reportline.(pa_reportline_id)` | Report Line Trl |
| incoming | `pareportline_pareportsource` | `pa_reportsource.(pa_reportline_id)` → `pa_reportline.(pa_reportline_id)` | Report Source |
| incoming | `pareportline_treport` | `t_report.(pa_reportline_id)` → `pa_reportline.(pa_reportline_id)` | T_Report |

<a id="t-pa_reportline_trl"></a>
## `pa_reportline_trl` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report Line Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Report Line Trl'; 주요 열 근거 부족; FK pareportline_pareportlinetrl; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pareportline_pareportlinetrl` | `pa_reportline_trl.(pa_reportline_id)` → `pa_reportline.(pa_reportline_id)` | Report Line |

<a id="t-pa_reportlineset"></a>
## `pa_reportlineset` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report Line Set`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Report Line Set'; 주요 열 근거 부족; FK pareport_lineset, pareportlineset_ireportline; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pareport_lineset` | `pa_report.(pa_reportlineset_id)` → `pa_reportlineset.(pa_reportlineset_id)` | Financial Report |
| incoming | `pareportlineset_ireportline` | `i_reportline.(pa_reportlineset_id)` → `pa_reportlineset.(pa_reportlineset_id)` | Import Report Line Set |
| incoming | `pareportlineset_line` | `pa_reportline.(pa_reportlineset_id)` → `pa_reportlineset.(pa_reportlineset_id)` | Report Line |

<a id="t-pa_reportsource"></a>
## `pa_reportsource` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Report Source`
- 사전 Description: Restriction of what will be shown in Report Line
- 근거 문장: 사전 Name='Report Source'; Description='Restriction of what will be shown in Report Line'; 주요 열 pa_reportline_id; FK pareportsource_ireportline, pareportline_pareportsource; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_reportline_id` | Report Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pareportsource_ireportline` | `i_reportline.(pa_reportsource_id)` → `pa_reportsource.(pa_reportsource_id)` | Import Report Line Set |
| outgoing | `pareportline_pareportsource` | `pa_reportsource.(pa_reportline_id)` → `pa_reportline.(pa_reportline_id)` | Report Line |

<a id="t-pa_sla_criteria"></a>
## `pa_sla_criteria` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `SLA Criteria`
- 사전 Description: Service Level Agreement Criteria
- 근거 문장: 사전 Name='SLA Criteria'; Description='Service Level Agreement Criteria'; 주요 열 ismanual, classname; FK paslacriteria_paslagoal; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ismanual` | Manual | `character(1)` |
| `classname` | Classname | `character varying(255)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `paslacriteria_paslagoal` | `pa_sla_goal.(pa_sla_criteria_id)` → `pa_sla_criteria.(pa_sla_criteria_id)` | SLA Goal |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-pa_sla_goal"></a>
## `pa_sla_goal` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `SLA Goal`
- 사전 Description: Service Level Agreement Goal
- 근거 문장: 사전 Name='SLA Goal'; Description='Service Level Agreement Goal'; 주요 열 measuretarget, measureactual; FK paslagoal_paslameasure; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `measuretarget` | Measure Target | `numeric` |
| `measureactual` | Measure Actual | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `paslagoal_paslameasure` | `pa_sla_measure.(pa_sla_goal_id)` → `pa_sla_goal.(pa_sla_goal_id)` | SLA Measure |

<a id="t-pa_sla_measure"></a>
## `pa_sla_measure` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `SLA Measure`
- 사전 Description: Service Level Agreement Measure
- 근거 문장: 사전 Name='SLA Measure'; Description='Service Level Agreement Measure'; 주요 열 pa_sla_goal_id, measureactual; FK paslagoal_paslameasure; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pa_sla_goal_id` | SLA Goal | `numeric(10,0)` |
| `measureactual` | Measure Actual | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `paslagoal_paslameasure` | `pa_sla_measure.(pa_sla_goal_id)` → `pa_sla_goal.(pa_sla_goal_id)` | SLA Goal |

<a id="t-pp_cost_collector"></a>
## `pp_cost_collector` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Cost Collector`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Manufacturing Cost Collector'; 주요 열 pp_order_bomline_id, pp_order_id, pp_order_node_id, pp_order_workflow_id; FK ppcostcollector_ppccma, pporder_ppcostcollector; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pp_order_bomline_id` | Manufacturing Order BOM Line | `numeric(10,0)` |
| `pp_order_id` | Manufacturing Order | `numeric(10,0)` |
| `pp_order_node_id` | Manufacturing Order Activity | `numeric(10,0)` |
| `pp_order_workflow_id` | Manufacturing Order Workflow | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ppcostcollector_ppccma` | `pp_cost_collectorma.(pp_cost_collector_id)` → `pp_cost_collector.(pp_cost_collector_id)` | Manufacturing Order MA |
| outgoing | `pporder_ppcostcollector` | `pp_cost_collector.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Order |
| outgoing | `pporderbomline_ppcostcollector` | `pp_cost_collector.(pp_order_bomline_id)` → `pp_order_bomline.(pp_order_bomline_id)` | Manufacturing Order BOM Line |
| outgoing | `ppordernode_ppcostcollector` | `pp_cost_collector.(pp_order_node_id)` → `pp_order_node.(pp_order_node_id)` | Manufacturing Order Activity |

<a id="t-pp_cost_collectorma"></a>
## `pp_cost_collectorma` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order MA`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Manufacturing Order MA'; 주요 열 근거 부족; FK ppcostcollector_ppccma; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ppcostcollector_ppccma` | `pp_cost_collectorma.(pp_cost_collector_id)` → `pp_cost_collector.(pp_cost_collector_id)` | Manufacturing Cost Collector |

<a id="t-pp_mrp"></a>
## `pp_mrp` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Material Requirement Planning`
- 사전 Description: Material Requirement Planning
- 근거 문장: 사전 Name='Material Requirement Planning'; Description='Material Requirement Planning'; 주요 열 pp_order_bomline_id, pp_order_id; FK pporder_ppmrp, pporderbomline_ppmrp; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `material requirement`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pp_order_bomline_id` | Manufacturing Order BOM Line | `numeric(10,0)` |
| `pp_order_id` | Manufacturing Order | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pporder_ppmrp` | `pp_mrp.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Order |
| outgoing | `pporderbomline_ppmrp` | `pp_mrp.(pp_order_bomline_id)` → `pp_order_bomline.(pp_order_bomline_id)` | Manufacturing Order BOM Line |

<a id="t-pp_order"></a>
## `pp_order` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order`
- 사전 Description: Manufacturing Order
- 근거 문장: 사전 Name='Manufacturing Order'; Description='Manufacturing Order'; 주요 열 pp_product_bom_id, qtybatchsize, qtybatchs, ad_workflow_id; FK pporder_ppcostcollector, pporder_ppmrp; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pp_product_bom_id` | BOM & Formula | `numeric(10,0)` |
| `qtybatchsize` | Qty Batch Size | `numeric` |
| `qtybatchs` | Qty Batch | `numeric` |
| `ad_workflow_id` | Workflow | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pporder_ppcostcollector` | `pp_cost_collector.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Cost Collector |
| incoming | `pporder_ppmrp` | `pp_mrp.(pp_order_id)` → `pp_order.(pp_order_id)` | Material Requirement Planning |
| incoming | `pporder_pporderbom` | `pp_order_bom.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Order BOM |
| incoming | `pporder_pporderbomline` | `pp_order_bomline.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Order BOM Line |

<a id="t-pp_order_bom"></a>
## `pp_order_bom` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order BOM`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Manufacturing Order BOM'; 주요 열 bomtype, pp_order_id; FK pporderbom_pporderbomline, pporderbom_pporderbomtrl; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `bomtype` | BOM Type | `character(1)` |
| `pp_order_id` | Manufacturing Order | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pporderbom_pporderbomline` | `pp_order_bomline.(pp_order_bom_id)` → `pp_order_bom.(pp_order_bom_id)` | Manufacturing Order BOM Line |
| incoming | `pporderbom_pporderbomtrl` | `pp_order_bom_trl.(pp_order_bom_id)` → `pp_order_bom.(pp_order_bom_id)` | Manufacturing Order BOM Trl |
| outgoing | `pporder_pporderbom` | `pp_order_bom.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Order |

<a id="t-pp_order_bom_trl"></a>
## `pp_order_bom_trl` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order BOM Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Manufacturing Order BOM Trl'; 주요 열 근거 부족; FK pporderbom_pporderbomtrl; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pporderbom_pporderbomtrl` | `pp_order_bom_trl.(pp_order_bom_id)` → `pp_order_bom.(pp_order_bom_id)` | Manufacturing Order BOM |

<a id="t-pp_order_bomline"></a>
## `pp_order_bomline` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order BOM Line`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Manufacturing Order BOM Line'; 주요 열 iscritical, pp_order_bom_id, pp_order_id, qtybom; FK pporderbomline_ppcostcollector, pporderbomline_ppmrp; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `iscritical` | Is Critical Component | `character(1)` |
| `pp_order_bom_id` | Manufacturing Order BOM | `numeric(10,0)` |
| `pp_order_id` | Manufacturing Order | `numeric(10,0)` |
| `qtybom` | Quantity | `numeric` |
| `qtybatch` | Quantity in % | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pporderbomline_ppcostcollector` | `pp_cost_collector.(pp_order_bomline_id)` → `pp_order_bomline.(pp_order_bomline_id)` | Manufacturing Cost Collector |
| incoming | `pporderbomline_ppmrp` | `pp_mrp.(pp_order_bomline_id)` → `pp_order_bomline.(pp_order_bomline_id)` | Material Requirement Planning |
| incoming | `pporderbomline_pporderbomlinet` | `pp_order_bomline_trl.(pp_order_bomline_id)` → `pp_order_bomline.(pp_order_bomline_id)` | Manufacturing Order BOM Line Trl |
| outgoing | `pporder_pporderbomline` | `pp_order_bomline.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Order |

<a id="t-pp_order_bomline_trl"></a>
## `pp_order_bomline_trl` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order BOM Line Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Manufacturing Order BOM Line Trl'; 주요 열 근거 부족; FK pporderbomline_pporderbomlinet; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pporderbomline_pporderbomlinet` | `pp_order_bomline_trl.(pp_order_bomline_id)` → `pp_order_bomline.(pp_order_bomline_id)` | Manufacturing Order BOM Line |

<a id="t-pp_order_cost"></a>
## `pp_order_cost` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order Cost`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Manufacturing Order Cost'; 주요 열 ad_workflow_id, pp_order_id; FK pporder_ppordercost; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_workflow_id` | Workflow | `numeric(10,0)` |
| `pp_order_id` | Manufacturing Order | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pporder_ppordercost` | `pp_order_cost.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Order |

<a id="t-pp_order_node"></a>
## `pp_order_node` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order Activity`
- 사전 Description: Manufacturing Order Activity
- 근거 문장: 사전 Name='Manufacturing Order Activity'; Description='Manufacturing Order Activity'; 주요 열 ad_workflow_id, pp_order_id, pp_order_workflow_id, workflow_id; FK ppordernext_ppordernodenext, ppordernode_ppcostcollector; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_workflow_id` | Workflow | `numeric(10,0)` |
| `pp_order_id` | Manufacturing Order | `numeric(10,0)` |
| `pp_order_workflow_id` | Manufacturing Order Workflow | `numeric(10,0)` |
| `workflow_id` | Workflow | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ppordernext_ppordernodenext` | `pp_order_nodenext.(pp_order_next_id)` → `pp_order_node.(pp_order_node_id)` | Manufacturing Order Activity Next |
| incoming | `ppordernode_ppcostcollector` | `pp_cost_collector.(pp_order_node_id)` → `pp_order_node.(pp_order_node_id)` | Manufacturing Cost Collector |
| incoming | `ppordernode_ppordernodeasset` | `pp_order_node_asset.(pp_order_node_id)` → `pp_order_node.(pp_order_node_id)` | Manufacturing Order Activity Asset |
| incoming | `ppordernode_ppordernodenext` | `pp_order_nodenext.(pp_order_node_id)` → `pp_order_node.(pp_order_node_id)` | Manufacturing Order Activity Next |

<a id="t-pp_order_node_asset"></a>
## `pp_order_node_asset` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order Activity Asset`
- 사전 Description: Manufacturing Order Activity Asset
- 근거 문장: 사전 Name='Manufacturing Order Activity Asset'; Description='Manufacturing Order Activity Asset'; 주요 열 pp_order_id, pp_order_node_id, pp_order_workflow_id; FK pporder_ppordernodeasset, ppordernode_ppordernodeasset; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pp_order_id` | Manufacturing Order | `numeric(10,0)` |
| `pp_order_node_id` | Manufacturing Order Activity | `numeric(10,0)` |
| `pp_order_workflow_id` | Manufacturing Order Workflow | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pporder_ppordernodeasset` | `pp_order_node_asset.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Order |
| outgoing | `ppordernode_ppordernodeasset` | `pp_order_node_asset.(pp_order_node_id)` → `pp_order_node.(pp_order_node_id)` | Manufacturing Order Activity |
| outgoing | `pporderworkflow_ppordernodeass` | `pp_order_node_asset.(pp_order_workflow_id)` → `pp_order_workflow.(pp_order_workflow_id)` | Manufacturing Order Workflow |

<a id="t-pp_order_node_product"></a>
## `pp_order_node_product` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order Activity Product`
- 사전 Description: Manufacturing Order Activity Product
- 근거 문장: 사전 Name='Manufacturing Order Activity Product'; Description='Manufacturing Order Activity Product'; 주요 열 pp_order_id, pp_order_node_id, pp_order_workflow_id; FK pporder_ppordernodeproduct, ppordernode_ppordernodeproduct; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pp_order_id` | Manufacturing Order | `numeric(10,0)` |
| `pp_order_node_id` | Manufacturing Order Activity | `numeric(10,0)` |
| `pp_order_workflow_id` | Manufacturing Order Workflow | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pporder_ppordernodeproduct` | `pp_order_node_product.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Order |
| outgoing | `ppordernode_ppordernodeproduct` | `pp_order_node_product.(pp_order_node_id)` → `pp_order_node.(pp_order_node_id)` | Manufacturing Order Activity |
| outgoing | `pporderworkflow_ppordernodepro` | `pp_order_node_product.(pp_order_workflow_id)` → `pp_order_workflow.(pp_order_workflow_id)` | Manufacturing Order Workflow |

<a id="t-pp_order_node_trl"></a>
## `pp_order_node_trl` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order Activity Trl`
- 사전 Description: Workflow Node (activity), step or process
- 근거 문장: 사전 Name='Manufacturing Order Activity Trl'; Description='Workflow Node (activity), step or process'; 주요 열 근거 부족; FK ppordernode_ppordernodetrl; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ppordernode_ppordernodetrl` | `pp_order_node_trl.(pp_order_node_id)` → `pp_order_node.(pp_order_node_id)` | Manufacturing Order Activity |

<a id="t-pp_order_nodenext"></a>
## `pp_order_nodenext` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order Activity Next`
- 사전 Description: Manufacturing Order Activity Next
- 근거 문장: 사전 Name='Manufacturing Order Activity Next'; Description='Manufacturing Order Activity Next'; 주요 열 pp_order_id, pp_order_next_id, pp_order_node_id; FK pporder_ppordernodenext, ppordernext_ppordernodenext; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pp_order_id` | Manufacturing Order | `numeric(10,0)` |
| `pp_order_next_id` | Manufacturing Order Activity Next | `numeric(10,0)` |
| `pp_order_node_id` | Manufacturing Order Activity | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pporder_ppordernodenext` | `pp_order_nodenext.(pp_order_id)` → `pp_order.(pp_order_id)` | Manufacturing Order |
| outgoing | `ppordernext_ppordernodenext` | `pp_order_nodenext.(pp_order_next_id)` → `pp_order_node.(pp_order_node_id)` | Manufacturing Order Activity |
| outgoing | `ppordernode_ppordernodenext` | `pp_order_nodenext.(pp_order_node_id)` → `pp_order_node.(pp_order_node_id)` | Manufacturing Order Activity |

<a id="t-pp_order_workflow"></a>
## `pp_order_workflow` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order Workflow`
- 사전 Description: Manufacturing Order Workflow
- 근거 문장: 사전 Name='Manufacturing Order Workflow'; Description='Manufacturing Order Workflow'; 주요 열 ad_workflow_id, pp_order_id, pp_order_node_id, qtybatchsize; FK pporderworkflow_ppcostcollecto, pporderworkflow_ppordernode; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_workflow_id` | Workflow | `numeric(10,0)` |
| `pp_order_id` | Manufacturing Order | `numeric(10,0)` |
| `pp_order_node_id` | Manufacturing Order Activity | `numeric(10,0)` |
| `qtybatchsize` | Qty Batch Size | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `pporderworkflow_ppcostcollecto` | `pp_cost_collector.(pp_order_workflow_id)` → `pp_order_workflow.(pp_order_workflow_id)` | Manufacturing Cost Collector |
| incoming | `pporderworkflow_ppordernode` | `pp_order_node.(pp_order_workflow_id)` → `pp_order_workflow.(pp_order_workflow_id)` | Manufacturing Order Activity |
| incoming | `pporderworkflow_ppordernodeass` | `pp_order_node_asset.(pp_order_workflow_id)` → `pp_order_workflow.(pp_order_workflow_id)` | Manufacturing Order Activity Asset |
| incoming | `pporderworkflow_ppordernodepro` | `pp_order_node_product.(pp_order_workflow_id)` → `pp_order_workflow.(pp_order_workflow_id)` | Manufacturing Order Activity Product |

<a id="t-pp_order_workflow_trl"></a>
## `pp_order_workflow_trl` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Manufacturing Order Workflow Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Manufacturing Order Workflow Trl'; 주요 열 근거 부족; FK pporderworkflow_pporderworkflo; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `manufacturing`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pporderworkflow_pporderworkflo` | `pp_order_workflow_trl.(pp_order_workflow_id)` → `pp_order_workflow.(pp_order_workflow_id)` | Manufacturing Order Workflow |

<a id="t-pp_product_bom"></a>
## `pp_product_bom` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `BOM & Formula`
- 사전 Description: BOM & Formula
- 근거 문장: 사전 Name='BOM & Formula'; Description='BOM & Formula'; 주요 열 bomtype; FK ppproductbom_iproductplanning, ppproductbom_mproduction; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `bom`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `bomtype` | BOM Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ppproductbom_iproductplanning` | `i_productplanning.(pp_product_bom_id)` → `pp_product_bom.(pp_product_bom_id)` | Import Product Planning |
| incoming | `ppproductbom_mproduction` | `m_production.(pp_product_bom_id)` → `pp_product_bom.(pp_product_bom_id)` | Production |
| incoming | `ppproductbom_pporder` | `pp_order.(pp_product_bom_id)` → `pp_product_bom.(pp_product_bom_id)` | Manufacturing Order |
| incoming | `ppproductbom_ppproductbomline` | `pp_product_bomline.(pp_product_bom_id)` → `pp_product_bom.(pp_product_bom_id)` | BOM Line |

<a id="t-pp_product_bom_trl"></a>
## `pp_product_bom_trl` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `BOM & Formula Trl`
- 사전 Description: BOM & Formula
- 근거 문장: 사전 Name='BOM & Formula Trl'; Description='BOM & Formula'; 주요 열 근거 부족; FK ppproductbom_ppproductbomtrl; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `bom`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ppproductbom_ppproductbomtrl` | `pp_product_bom_trl.(pp_product_bom_id)` → `pp_product_bom.(pp_product_bom_id)` | BOM & Formula |

<a id="t-pp_product_bomline"></a>
## `pp_product_bomline` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `BOM Line`
- 사전 Description: BOM Line
- 근거 문장: 사전 Name='BOM Line'; Description='BOM Line'; 주요 열 iscritical, pp_product_bom_id, qtybom, qtybatch; FK ppproductbomline_ppproductboml, ppproductbom_ppproductbomline; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `bom`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `iscritical` | Is Critical Component | `character(1)` |
| `pp_product_bom_id` | BOM & Formula | `numeric(10,0)` |
| `qtybom` | Quantity | `numeric` |
| `qtybatch` | Quantity in % | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ppproductbomline_ppproductboml` | `pp_product_bomline_trl.(pp_product_bomline_id)` → `pp_product_bomline.(pp_product_bomline_id)` | BOM Line Trl |
| outgoing | `ppproductbom_ppproductbomline` | `pp_product_bomline.(pp_product_bom_id)` → `pp_product_bom.(pp_product_bom_id)` | BOM & Formula |

<a id="t-pp_product_bomline_trl"></a>
## `pp_product_bomline_trl` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `BOM Line Trl`
- 사전 Description: BOM Line
- 근거 문장: 사전 Name='BOM Line Trl'; Description='BOM Line'; 주요 열 근거 부족; FK ppproductbomline_ppproductboml; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `bom`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ppproductbomline_ppproductboml` | `pp_product_bomline_trl.(pp_product_bomline_id)` → `pp_product_bomline.(pp_product_bomline_id)` | BOM Line |

<a id="t-pp_product_planning"></a>
## `pp_product_planning` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Product Planning`
- 사전 Description: Product Planning
- 근거 문장: 사전 Name='Product Planning'; Description='Product Planning'; 주요 열 ad_workflow_id, pp_product_bom_id; FK ppproductplanning_iproductplan, ppproductbom_ppproductplanning; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `product planning`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_workflow_id` | Workflow | `numeric(10,0)` |
| `pp_product_bom_id` | BOM & Formula | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `ppproductplanning_iproductplan` | `i_productplanning.(pp_product_planning_id)` → `pp_product_planning.(pp_product_planning_id)` | Import Product Planning |
| outgoing | `ppproductbom_ppproductplanning` | `pp_product_planning.(pp_product_bom_id)` → `pp_product_bom.(pp_product_bom_id)` | BOM & Formula |

<a id="t-pp_wf_node_asset"></a>
## `pp_wf_node_asset` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Node Asset`
- 사전 Description: Workflow Node Asset
- 근거 문장: 사전 Name='Workflow Node Asset'; Description='Workflow Node Asset'; 주요 열 ad_wf_node_id; FK adwfnode_ppwfnodeasset; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_wf_node_id` | Node | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adwfnode_ppwfnodeasset` | `pp_wf_node_asset.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Node |

<a id="t-pp_wf_node_product"></a>
## `pp_wf_node_product` — 워크플로 정의·실행

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Workflow Node Product`
- 사전 Description: Workflow Node Product
- 근거 문장: 사전 Name='Workflow Node Product'; Description='Workflow Node Product'; 주요 열 ad_wf_node_id; FK adwfnode_ppwfnodeproduct; 사전 의미와 열/FK가 워크플로 정의·실행를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `workflow`를 근거로, 구조 근거가 있는 `workflow` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_wf_node_id` | Node | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adwfnode_ppwfnodeproduct` | `pp_wf_node_product.(ad_wf_node_id)` → `ad_wf_node.(ad_wf_node_id)` | Node |

<a id="t-qm_specification"></a>
## `qm_specification` — 품질 시험·규격

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Quality Specification`
- 사전 Description: Quality Specification
- 근거 문장: 사전 Name='Quality Specification'; Description='Quality Specification'; 주요 열 m_product_id, validfrom; FK qmspecification_qmspecificatio; 사전 의미와 열/FK가 품질 시험·규격를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `quality`를 근거로, 구조 근거가 있는 `quality` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `m_product_id` | Product | `numeric(10,0)` |
| `validfrom` | Valid from | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `qmspecification_qmspecificatio` | `qm_specificationline.(qm_specification_id)` → `qm_specification.(qm_specification_id)` | QM Specification Line |

<a id="t-qm_specificationline"></a>
## `qm_specificationline` — 품질 시험·규격

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `QM Specification Line`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='QM Specification Line'; 주요 열 validfrom, qm_specification_id; FK qmspecification_qmspecificatio; 사전 의미와 열/FK가 품질 시험·규격를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `specification`를 근거로, 구조 근거가 있는 `quality` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `validfrom` | Valid from | `character varying(22)` |
| `qm_specification_id` | Quality Specification | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `qmspecification_qmspecificatio` | `qm_specificationline.(qm_specification_id)` → `qm_specification.(qm_specification_id)` | Quality Specification |

<a id="t-r_category"></a>
## `r_category` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Category`
- 사전 Description: Request Category
- 근거 문장: 사전 Name='Category'; Description='Request Category'; 주요 열 근거 부족; FK rcategory_rrequest, rcategory_rrequestaction; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rcategory_rrequest` | `r_request.(r_category_id)` → `r_category.(r_category_id)` | Request |
| incoming | `rcategory_rrequestaction` | `r_requestaction.(r_category_id)` → `r_category.(r_category_id)` | Request History |

<a id="t-r_categoryupdates"></a>
## `r_categoryupdates` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `R_CategoryUpdates`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='R_CategoryUpdates'; 주요 열 isselfservice; FK aduser_rcategoryupdates, rcategory_rcategoryupdates; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isselfservice` | Self-Service | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_rcategoryupdates` | `r_categoryupdates.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `rcategory_rcategoryupdates` | `r_categoryupdates.(r_category_id)` → `r_category.(r_category_id)` | Category |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-r_contactinterest"></a>
## `r_contactinterest` — 거래처·연락처·주소

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `R_ContactInterest`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='R_ContactInterest'; 주요 열 근거 부족; FK aduser_rcontactinterest; 사전 의미와 열/FK가 거래처·연락처·주소를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_rcontactinterest` | `r_contactinterest.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

<a id="t-r_group"></a>
## `r_group` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Group`
- 사전 Description: Request Group
- 근거 문장: 사전 Name='Group'; Description='Request Group'; 주요 열 근거 부족; FK rgroup_rrequest, rgroup_rrequestaction; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rgroup_rrequest` | `r_request.(r_group_id)` → `r_group.(r_group_id)` | Request |
| incoming | `rgroup_rrequestaction` | `r_requestaction.(r_group_id)` → `r_group.(r_group_id)` | Request History |

<a id="t-r_groupupdates"></a>
## `r_groupupdates` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `R_GroupUpdates`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='R_GroupUpdates'; 주요 열 isselfservice; FK aduser_ruserupdates, rgroup_rgroupupdates; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isselfservice` | Self-Service | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `aduser_ruserupdates` | `r_groupupdates.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |
| outgoing | `rgroup_rgroupupdates` | `r_groupupdates.(r_group_id)` → `r_group.(r_group_id)` | Group |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-r_interestarea"></a>
## `r_interestarea` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Interest Area`
- 사전 Description: Interest Area or Topic
- 근거 문장: 사전 Name='Interest Area'; Description='Interest Area or Topic'; 주요 열 isselfservice; FK rinterestarea_adldapaccess, rinterestarea_ibpartner; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `isselfservice` | Self-Service | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rinterestarea_adldapaccess` | `ad_ldapaccess.(r_interestarea_id)` → `r_interestarea.(r_interestarea_id)` | Ldap Access |
| incoming | `rinterestarea_ibpartner` | `i_bpartner.(r_interestarea_id)` → `r_interestarea.(r_interestarea_id)` | Import Business Partner |
| incoming | `rinterestarea_rcontactinterest` | `r_contactinterest.(r_interestarea_id)` → `r_interestarea.(r_interestarea_id)` | R_ContactInterest |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-r_issueknown"></a>
## `r_issueknown` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Known Issue`
- 사전 Description: Known Issue
- 근거 문장: 사전 Name='Known Issue'; Description='Known Issue'; 주요 열 issuesummary, r_issuestatus_id, r_request_id, r_issuerecommendation_id; FK rissuerecommendation_rissuekno, rissuestatus_rissueknown; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `issuesummary` | Issue Summary | `character varying(255)` |
| `r_issuestatus_id` | Issue Status | `numeric(10,0)` |
| `r_request_id` | Request | `numeric(10,0)` |
| `r_issuerecommendation_id` | Issue Recommendation | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `rissuerecommendation_rissuekno` | `r_issueknown.(r_issuerecommendation_id)` → `r_issuerecommendation.(r_issuerecommendation_id)` | Issue Recommendation |
| outgoing | `rissuestatus_rissueknown` | `r_issueknown.(r_issuestatus_id)` → `r_issuestatus.(r_issuestatus_id)` | Issue Status |
| outgoing | `rrequest_rissueknown` | `r_issueknown.(r_request_id)` → `r_request.(r_request_id)` | Request |

<a id="t-r_issueproject"></a>
## `r_issueproject` — 프로젝트·활동·작업

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Issue Project`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Issue Project'; 주요 열 c_project_id; FK cproject_rissueproject; 사전 의미와 열/FK가 프로젝트·활동·작업를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_project_id` | Project | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cproject_rissueproject` | `r_issueproject.(c_project_id)` → `c_project.(c_project_id)` | Project |

<a id="t-r_issuerecommendation"></a>
## `r_issuerecommendation` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Issue Recommendation`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Issue Recommendation'; 주요 열 근거 부족; FK rissuerecommendation_rissuekno; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rissuerecommendation_rissuekno` | `r_issueknown.(r_issuerecommendation_id)` → `r_issuerecommendation.(r_issuerecommendation_id)` | Known Issue |

<a id="t-r_issuesource"></a>
## `r_issuesource` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 r_issuesystem_id, r_issueproject_id, r_issueuser_id, statisticsinfo; FK rissueproject_rissuesource, rissuesystem_rissuesource; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `r_issuesystem_id` | 미지정 | `numeric(10,0)` |
| `r_issueproject_id` | 미지정 | `numeric(10,0)` |
| `r_issueuser_id` | 미지정 | `numeric(10,0)` |
| `statisticsinfo` | 미지정 | `character varying(60)` |
| `profileinfo` | 미지정 | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `rissueproject_rissuesource` | `r_issuesource.(r_issueproject_id)` → `r_issueproject.(r_issueproject_id)` | Issue Project |
| outgoing | `rissuesystem_rissuesource` | `r_issuesource.(r_issuesystem_id)` → `r_issuesystem.(r_issuesystem_id)` | Issue System |
| outgoing | `rissueuser_rissuesource` | `r_issuesource.(r_issueuser_id)` → `r_issueuser.(r_issueuser_id)` | Issue User |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-r_issuestatus"></a>
## `r_issuestatus` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Issue Status`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Issue Status'; 주요 열 근거 부족; FK rissuestatus_rissueknown; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rissuestatus_rissueknown` | `r_issueknown.(r_issuestatus_id)` → `r_issuestatus.(r_issuestatus_id)` | Known Issue |

<a id="t-r_issuesystem"></a>
## `r_issuesystem` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Issue System`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Issue System'; 주요 열 dbaddress, statisticsinfo, profileinfo, systemstatus; FK rissuesystem_ad_issue, rissuesystem_rissuesource; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `dbaddress` | DB Address | `character varying(255)` |
| `statisticsinfo` | Statistics | `character varying(60)` |
| `profileinfo` | Profile | `character varying(4000)` |
| `systemstatus` | System Status | `character(1)` |
| `a_asset_id` | Asset | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rissuesystem_ad_issue` | `ad_issue.(r_issuesystem_id)` → `r_issuesystem.(r_issuesystem_id)` | System Issue |
| incoming | `rissuesystem_rissuesource` | `r_issuesource.(r_issuesystem_id)` → `r_issuesystem.(r_issuesystem_id)` | 미지정 |
| outgoing | `aasset_rissuesystem` | `r_issuesystem.(a_asset_id)` → `a_asset.(a_asset_id)` | Asset |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-r_issueuser"></a>
## `r_issueuser` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Issue User`
- 사전 Description: User who reported issues
- 근거 문장: 사전 Name='Issue User'; Description='User who reported issues'; 주요 열 username, ad_user_id; FK rissueuser_adissue, rissueuser_rissuesource; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `username` | User Name | `character varying(60)` |
| `ad_user_id` | User/Contact | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rissueuser_adissue` | `ad_issue.(r_issueuser_id)` → `r_issueuser.(r_issueuser_id)` | System Issue |
| incoming | `rissueuser_rissuesource` | `r_issuesource.(r_issueuser_id)` → `r_issueuser.(r_issueuser_id)` | 미지정 |
| outgoing | `aduser_rissueuser` | `r_issueuser.(ad_user_id)` → `ad_user.(ad_user_id)` | User/Contact |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-r_mailtext"></a>
## `r_mailtext` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Mail Template`
- 사전 Description: Text templates for mailings
- 근거 문장: 사전 Name='Mail Template'; Description='Text templates for mailings'; 주요 열 ishtml; FK rmailtext_rmailtexttrl; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ishtml` | HTML | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rmailtext_rmailtexttrl` | `r_mailtext_trl.(r_mailtext_id)` → `r_mailtext.(r_mailtext_id)` | Mail Template Trl |

<a id="t-r_mailtext_trl"></a>
## `r_mailtext_trl` — 웹 콘텐츠·미디어

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Mail Template Trl`
- 사전 Description: Text templates for mailings
- 근거 문장: 사전 Name='Mail Template Trl'; Description='Text templates for mailings'; 주요 열 근거 부족; FK rmailtext_rmailtexttrl; 사전 의미와 열/FK가 웹 콘텐츠·미디어를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `rmailtext_rmailtexttrl` | `r_mailtext_trl.(r_mailtext_id)` → `r_mailtext.(r_mailtext_id)` | Mail Template |

<a id="t-r_request"></a>
## `r_request` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Request`
- 사전 Description: Request from a Business Partner or Prospect
- 근거 문장: 사전 Name='Request'; Description='Request from a Business Partner or Prospect'; 주요 열 r_requesttype_id, r_group_id, r_category_id, r_status_id; FK rrequest_rissueknown, rrequest_rrequestaction; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `r_requesttype_id` | Request Type | `numeric(10,0)` |
| `r_group_id` | Group | `numeric(10,0)` |
| `r_category_id` | Category | `numeric(10,0)` |
| `r_status_id` | Status | `numeric(10,0)` |
| `r_resolution_id` | Resolution | `numeric(10,0)` |
| `r_requestrelated_id` | Related Request | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rrequest_rissueknown` | `r_issueknown.(r_request_id)` → `r_request.(r_request_id)` | Known Issue |
| incoming | `rrequest_rrequestaction` | `r_requestaction.(r_request_id)` → `r_request.(r_request_id)` | Request History |
| incoming | `rrequest_rrequestupdate` | `r_requestupdate.(r_request_id)` → `r_request.(r_request_id)` | Request Update |
| incoming | `rrequest_rrupdates` | `r_requestupdates.(r_request_id)` → `r_request.(r_request_id)` | Request Update Recipiants |

<a id="t-r_requestaction"></a>
## `r_requestaction` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Request History`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Request History'; 주요 열 r_request_id, r_group_id, r_category_id, r_status_id; FK rcategory_rrequestaction, rgroup_rrequestaction; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `r_request_id` | Request | `numeric(10,0)` |
| `r_group_id` | Group | `numeric(10,0)` |
| `r_category_id` | Category | `numeric(10,0)` |
| `r_status_id` | Status | `numeric(10,0)` |
| `r_resolution_id` | Resolution | `numeric(10,0)` |
| `confidentialtype` | Confidentiality | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `rcategory_rrequestaction` | `r_requestaction.(r_category_id)` → `r_category.(r_category_id)` | Category |
| outgoing | `rgroup_rrequestaction` | `r_requestaction.(r_group_id)` → `r_group.(r_group_id)` | Group |
| outgoing | `rrequest_rrequestaction` | `r_requestaction.(r_request_id)` → `r_request.(r_request_id)` | Request |
| outgoing | `rrequesttype_rrequestaction` | `r_requestaction.(r_requesttype_id)` → `r_requesttype.(r_requesttype_id)` | Request Type |

<a id="t-r_requestprocessor"></a>
## `r_requestprocessor` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Request Processor`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Request Processor'; 주요 열 r_requesttype_id; FK rrequestprocessor_log, rrequestprocessor_route; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `r_requesttype_id` | Request Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rrequestprocessor_log` | `r_requestprocessorlog.(r_requestprocessor_id)` → `r_requestprocessor.(r_requestprocessor_id)` | Request Processor Log |
| incoming | `rrequestprocessor_route` | `r_requestprocessor_route.(r_requestprocessor_id)` → `r_requestprocessor.(r_requestprocessor_id)` | Request Routing |
| outgoing | `rrequesttype_rrequestprocessor` | `r_requestprocessor.(r_requesttype_id)` → `r_requesttype.(r_requesttype_id)` | Request Type |

<a id="t-r_requestprocessor_route"></a>
## `r_requestprocessor_route` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Request Routing`
- 사전 Description: Automatic routing of requests
- 근거 문장: 사전 Name='Request Routing'; Description='Automatic routing of requests'; 주요 열 r_requestprocessor_id, r_requesttype_id; FK rrequestprocessor_route, rrequesttype_rprocessorrule; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `r_requestprocessor_id` | Request Processor | `numeric(10,0)` |
| `r_requesttype_id` | Request Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `rrequestprocessor_route` | `r_requestprocessor_route.(r_requestprocessor_id)` → `r_requestprocessor.(r_requestprocessor_id)` | Request Processor |
| outgoing | `rrequesttype_rprocessorrule` | `r_requestprocessor_route.(r_requesttype_id)` → `r_requesttype.(r_requesttype_id)` | Request Type |

<a id="t-r_requestprocessorlog"></a>
## `r_requestprocessorlog` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Request Processor Log`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Request Processor Log'; 주요 열 summary; FK rrequestprocessor_log; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `summary` | Summary | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `rrequestprocessor_log` | `r_requestprocessorlog.(r_requestprocessor_id)` → `r_requestprocessor.(r_requestprocessor_id)` | Request Processor |

<a id="t-r_requesttype"></a>
## `r_requesttype` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Request Type`
- 사전 Description: Type of request (e.g. Inquiry, Complaint, ..)
- 근거 문장: 사전 Name='Request Type'; Description='Type of request (e.g. Inquiry, Complaint, ..)'; 주요 열 confidentialtype, isautochangerequest, isconfidentialinfo, r_statuscategory_id; FK rrequesttype_rprocessorrule, rrequesttype_rrequest; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `confidentialtype` | Confidentiality | `character(1)` |
| `isautochangerequest` | Create Change Request | `character(1)` |
| `isconfidentialinfo` | Confidential Info | `character(1)` |
| `r_statuscategory_id` | Status Category | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rrequesttype_rprocessorrule` | `r_requestprocessor_route.(r_requesttype_id)` → `r_requesttype.(r_requesttype_id)` | Request Routing |
| incoming | `rrequesttype_rrequest` | `r_request.(r_requesttype_id)` → `r_requesttype.(r_requesttype_id)` | Request |
| incoming | `rrequesttype_rrequestaction` | `r_requestaction.(r_requesttype_id)` → `r_requesttype.(r_requesttype_id)` | Request History |
| incoming | `rrequesttype_rrequestprocessor` | `r_requestprocessor.(r_requesttype_id)` → `r_requesttype.(r_requesttype_id)` | Request Processor |

<a id="t-r_requesttypeupdates"></a>
## `r_requesttypeupdates` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Request Type Updates`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Request Type Updates'; 주요 열 근거 부족; FK rrequesttype_rrtupdates; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `rrequesttype_rrtupdates` | `r_requesttypeupdates.(r_requesttype_id)` → `r_requesttype.(r_requesttype_id)` | Request Type |

<a id="t-r_requestupdate"></a>
## `r_requestupdate` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Request Update`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Request Update'; 주요 열 r_request_id, confidentialtypeentry, result; FK rrequest_rrequestupdate; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `r_request_id` | Request | `numeric(10,0)` |
| `confidentialtypeentry` | Entry Confidentiality | `character(1)` |
| `result` | Result | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `rrequest_rrequestupdate` | `r_requestupdate.(r_request_id)` → `r_request.(r_request_id)` | Request |

<a id="t-r_requestupdates"></a>
## `r_requestupdates` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Request Update Recipiants`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Request Update Recipiants'; 주요 열 근거 부족; FK rrequest_rrupdates; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `rrequest_rrupdates` | `r_requestupdates.(r_request_id)` → `r_request.(r_request_id)` | Request |

<a id="t-r_resolution"></a>
## `r_resolution` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Resolution`
- 사전 Description: Request Resolution
- 근거 문장: 사전 Name='Resolution'; Description='Request Resolution'; 주요 열 근거 부족; FK rresolution_rrequest, rresolution_rrequestaction; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rresolution_rrequest` | `r_request.(r_resolution_id)` → `r_resolution.(r_resolution_id)` | Request |
| incoming | `rresolution_rrequestaction` | `r_requestaction.(r_resolution_id)` → `r_resolution.(r_resolution_id)` | Request History |

<a id="t-r_standardresponse"></a>
## `r_standardresponse` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Standard Response`
- 사전 Description: Request Standard Response 
- 근거 문장: 사전 Name='Standard Response'; Description='Request Standard Response '; 주요 열 근거 부족; FK rstandardresponse_rrequest; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rstandardresponse_rrequest` | `r_request.(r_standardresponse_id)` → `r_standardresponse.(r_standardresponse_id)` | Request |

<a id="t-r_status"></a>
## `r_status` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Status`
- 사전 Description: Request Status
- 근거 문장: 사전 Name='Status'; Description='Request Status'; 주요 열 r_statuscategory_id; FK rstatus_rrequest, rstatus_rrequestaction; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `r_statuscategory_id` | Status Category | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rstatus_rrequest` | `r_request.(r_status_id)` → `r_status.(r_status_id)` | Request |
| incoming | `rstatus_rrequestaction` | `r_requestaction.(r_status_id)` → `r_status.(r_status_id)` | Request History |
| outgoing | `nextstatus_rstatus` | `r_status.(next_status_id)` → `r_status.(r_status_id)` | Status |
| outgoing | `rstatuscategory_rstatus` | `r_status.(r_statuscategory_id)` → `r_statuscategory.(r_statuscategory_id)` | Status Category |

<a id="t-r_statuscategory"></a>
## `r_statuscategory` — 요청·지원·이슈

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Status Category`
- 사전 Description: Request Status Category
- 근거 문장: 사전 Name='Status Category'; Description='Request Status Category'; 주요 열 근거 부족; FK rstatuscategory_rrequesttype, rstatuscategory_rstatus; 사전 의미와 열/FK가 요청·지원·이슈를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `rstatuscategory_rrequesttype` | `r_requesttype.(r_statuscategory_id)` → `r_statuscategory.(r_statuscategory_id)` | Request Type |
| incoming | `rstatuscategory_rstatus` | `r_status.(r_statuscategory_id)` → `r_statuscategory.(r_statuscategory_id)` | Status |

<a id="t-s_expensetype"></a>
## `s_expensetype` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Expense Type`
- 사전 Description: Expense report type
- 근거 문장: 사전 Name='Expense Type'; Description='Expense report type'; 주요 열 근거 부족; FK cuom_sexpensetype; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cuom_sexpensetype` | `s_expensetype.(c_uom_id)` → `c_uom.(c_uom_id)` | UOM |

<a id="t-s_resource"></a>
## `s_resource` — 자원·시간·경비·교육

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Resource`
- 사전 Description: Resource
- 근거 문장: 사전 Name='Resource'; Description='Resource'; 주요 열 s_resourcetype_id, chargeableqty, ismanufacturingresource, waitingtime; FK sresource_sresourceassignment, sresource_sresunavailable; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `s_resourcetype_id` | Resource Type | `numeric(10,0)` |
| `chargeableqty` | Chargeable Quantity | `numeric` |
| `ismanufacturingresource` | Manufacturing Resource | `character(1)` |
| `waitingtime` | Waiting Time | `numeric` |
| `manufacturingresourcetype` | Manufacturing Resource Type | `character(2)` |
| `queuingtime` | Queuing Time | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `sresource_sresourceassignment` | `s_resourceassignment.(s_resource_id)` → `s_resource.(s_resource_id)` | Resource Assignment |
| incoming | `sresource_sresunavailable` | `s_resourceunavailable.(s_resource_id)` → `s_resource.(s_resource_id)` | Resource Unavailability |
| outgoing | `sresourcetype_sresource` | `s_resource.(s_resourcetype_id)` → `s_resourcetype.(s_resourcetype_id)` | Resource Type |

<a id="t-s_resourceassignment"></a>
## `s_resourceassignment` — 자원·시간·경비·교육

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Resource Assignment`
- 사전 Description: Resource Assignment
- 근거 문장: 사전 Name='Resource Assignment'; Description='Resource Assignment'; 주요 열 s_resource_id, assigndatefrom, assigndateto, qty; FK sresourceassign_steline, sresource_sresourceassignment; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `s_resource_id` | Resource | `numeric(10,0)` |
| `assigndatefrom` | Assign From | `timestamp without time zone` |
| `assigndateto` | Assign To | `timestamp without time zone` |
| `qty` | Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `sresourceassign_steline` | `s_timeexpenseline.(s_resourceassignment_id)` → `s_resourceassignment.(s_resourceassignment_id)` | Expense Line |
| outgoing | `sresource_sresourceassignment` | `s_resourceassignment.(s_resource_id)` → `s_resource.(s_resource_id)` | Resource |

<a id="t-s_resourcetype"></a>
## `s_resourcetype` — 자원·시간·경비·교육

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Resource Type`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Resource Type'; 주요 열 timeslotstart, timeslotend, istimeslot, chargeableqty; FK sresourcetype_sresource; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `timeslotstart` | Slot Start | `timestamp without time zone` |
| `timeslotend` | Slot End | `timestamp without time zone` |
| `istimeslot` | Time Slot | `character(1)` |
| `chargeableqty` | Chargeable Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `sresourcetype_sresource` | `s_resource.(s_resourcetype_id)` → `s_resourcetype.(s_resourcetype_id)` | Resource |

<a id="t-s_resourceunavailable"></a>
## `s_resourceunavailable` — 자원·시간·경비·교육

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Resource Unavailability`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Resource Unavailability'; 주요 열 s_resource_id, datefrom, dateto; FK sresource_sresunavailable; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `s_resource_id` | Resource | `numeric(10,0)` |
| `datefrom` | Date From | `timestamp without time zone` |
| `dateto` | Date To | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `sresource_sresunavailable` | `s_resourceunavailable.(s_resource_id)` → `s_resource.(s_resource_id)` | Resource |

<a id="t-s_timeexpense"></a>
## `s_timeexpense` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Expense Report`
- 사전 Description: Time and Expense Report
- 근거 문장: 사전 Name='Expense Report'; Description='Time and Expense Report'; 주요 열 datereport; FK stimeexpense_line; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `datereport` | Report Date | `timestamp without time zone` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `stimeexpense_line` | `s_timeexpenseline.(s_timeexpense_id)` → `s_timeexpense.(s_timeexpense_id)` | Expense Line |

<a id="t-s_timeexpenseline"></a>
## `s_timeexpenseline` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Expense Line`
- 사전 Description: Time and Expense Report Line
- 근거 문장: 사전 Name='Expense Line'; Description='Time and Expense Report Line'; 주요 열 istimereport; FK cuom_stimeexpenseline, stimeexpense_line; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istimereport` | Time Report | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cuom_stimeexpenseline` | `s_timeexpenseline.(c_uom_id)` → `c_uom.(c_uom_id)` | UOM |
| outgoing | `stimeexpense_line` | `s_timeexpenseline.(s_timeexpense_id)` → `s_timeexpense.(s_timeexpense_id)` | Expense Report |

<a id="t-s_timetype"></a>
## `s_timetype` — 자원·시간·경비·교육

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Time Type`
- 사전 Description: Type of time recorded
- 근거 문장: 사전 Name='Time Type'; Description='Type of time recorded'; 주요 열 근거 부족; FK stimetype_stimeexpenseline; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `stimetype_stimeexpenseline` | `s_timeexpenseline.(s_timetype_id)` → `s_timetype.(s_timetype_id)` | Expense Line |

<a id="t-s_training"></a>
## `s_training` — 자원·시간·경비·교육

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Training`
- 사전 Description: Repeated Training
- 근거 문장: 사전 Name='Training'; Description='Repeated Training'; 주요 열 근거 부족; FK straining_strainingclass; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `straining_strainingclass` | `s_training_class.(s_training_id)` → `s_training.(s_training_id)` | Training Class |

<a id="t-s_training_class"></a>
## `s_training_class` — 자원·시간·경비·교육

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Training Class`
- 사전 Description: The actual training class instance
- 근거 문장: 사전 Name='Training Class'; Description='The actual training class instance'; 주요 열 s_training_id; FK straining_strainingclass; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `s_training_id` | Training | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `straining_strainingclass` | `s_training_class.(s_training_id)` → `s_training.(s_training_id)` | Training |

<a id="t-sso_principalconfig"></a>
## `sso_principalconfig` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `SSO Configuration`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='SSO Configuration'; 주요 열 sso_applicationclientid, sso_applicationlogouturl, sso_applicationredirecturis, sso_applicationsecretkey; FK ssologinbuttonimage_ssoprincip; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `sso_applicationclientid` | Application Client ID | `character varying(100)` |
| `sso_applicationlogouturl` | Application Logout URL | `character varying(1000)` |
| `sso_applicationredirecturis` | Application Redirect URIs | `character varying(1000)` |
| `sso_applicationsecretkey` | Application Secret Key | `character varying(100)` |
| `sso_authorizationtenantid` | Tenant ID | `character varying(100)` |
| `isdefault` | Default | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `ssologinbuttonimage_ssoprincip` | `sso_principalconfig.(sso_loginbuttonimage_id)` → `ad_image.(ad_image_id)` | Image |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_1099extract"></a>
## `t_1099extract` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `1099 Extract`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='1099 Extract'; 주요 열 ad_pinstance_id, amtbucket01, amtbucket02, amtbucket03; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_pinstance_id` | Process Instance | `numeric(10,0)` |
| `amtbucket01` | Amount Bucket 1 | `numeric` |
| `amtbucket02` | Amount Bucket 2 | `numeric` |
| `amtbucket03` | Amount Bucket 3 | `numeric` |
| `amtbucket04` | Amount Bucket 4 | `numeric` |
| `amtbucket05` | Amount Bucket 5 | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_aging"></a>
## `t_aging` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `T_Aging`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='T_Aging'; 주요 열 statementdate, duedate, daysdue, islistinvoices; FK adpinstance_taging, cactivity_taging; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `statementdate` | Statement date | `timestamp without time zone` |
| `duedate` | Due Date | `timestamp without time zone` |
| `daysdue` | Days due | `numeric(10,0)` |
| `islistinvoices` | List Invoices | `character(1)` |
| `issotrx` | Sales Transaction | `character(1)` |
| `c_bp_group_id` | Business Partner Group | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adpinstance_taging` | `t_aging.(ad_pinstance_id)` → `ad_pinstance.(ad_pinstance_id)` | Process Instance |
| outgoing | `cactivity_taging` | `t_aging.(c_activity_id)` → `c_activity.(c_activity_id)` | Activity |
| outgoing | `cbpartner_taging` | `t_aging.(c_bpartner_id)` → `c_bpartner.(c_bpartner_id)` | Business Partner |
| outgoing | `cbpgroup_taging` | `t_aging.(c_bp_group_id)` → `c_bp_group.(c_bp_group_id)` | Business Partner Group |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_alter_column"></a>
## `t_alter_column` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 tablename, columnname, datatype, nullclause; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `tablename` | 미지정 | `name` |
| `columnname` | 미지정 | `name` |
| `datatype` | 미지정 | `name` |
| `nullclause` | 미지정 | `character varying(10)` |
| `defaultclause` | 미지정 | `character varying(200)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_bankregister"></a>
## `t_bankregister` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Bank Register`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Bank Register'; 주요 열 c_bank_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bank_id` | Bank | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-t_bom_indented"></a>
## `t_bom_indented` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Indented BOM Report`
- 사전 Description: Indented BOM Report
- 근거 문장: 사전 Name='Indented BOM Report'; Description='Indented BOM Report'; 주요 열 ad_pinstance_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_pinstance_id` | Process Instance | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-t_bomline"></a>
## `t_bomline` — 제조·BOM·소요 계획

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Temporal BOM Line`
- 사전 Description: Temporal BOM Line
- 근거 문장: 사전 Name='Temporal BOM Line'; Description='Temporal BOM Line'; 주요 열 pp_product_bomline_id, pp_product_bom_id, qtybom; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 제조·BOM·소요 계획를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `bom`를 근거로, 구조 근거가 있는 `manufacturing` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pp_product_bomline_id` | BOM Line | `numeric(10,0)` |
| `pp_product_bom_id` | BOM & Formula | `numeric(10,0)` |
| `qtybom` | Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-t_cashflow"></a>
## `t_cashflow` — 입출금·은행·결제 배분

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `T_CashFlow_ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='T_CashFlow_ID'; 주요 열 c_cashplanline_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 입출금·은행·결제 배분를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_cashplanline_id` | Cash Plan Line | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-t_distributionrundetail"></a>
## `t_distributionrundetail` — 출하·입고·반품·배송

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `T_DistributionRunDetail`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='T_DistributionRunDetail'; 주요 열 minqty, qty; FK mdistributionlist_tdrdetail, mdistributionlline_tdrdetail; 사전 의미와 열/FK가 출하·입고·반품·배송를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `minqty` | Minimum Quantity | `numeric` |
| `qty` | Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mdistributionlist_tdrdetail` | `t_distributionrundetail.(m_distributionlist_id)` → `m_distributionlist.(m_distributionlist_id)` | Distribution List |
| outgoing | `mdistributionlline_tdrdetail` | `t_distributionrundetail.(m_distributionlistline_id)` → `m_distributionlistline.(m_distributionlistline_id)` | Distribution List Line |
| outgoing | `mdistributionrline_tdrdetail` | `t_distributionrundetail.(m_distributionrunline_id)` → `m_distributionrunline.(m_distributionrunline_id)` | Distribution Run Line |
| outgoing | `mdistributionrun_tdrdetail` | `t_distributionrundetail.(m_distributionrun_id)` → `m_distributionrun.(m_distributionrun_id)` | Distribution Run |

<a id="t-t_fact_acct_history"></a>
## `t_fact_acct_history` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Accounting Fact History`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Accounting Fact History'; 주요 열 fact_acct_id, c_acctschema_id, account_id, dateacct; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `fact_acct_id` | Accounting Fact | `numeric(10,0)` |
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `account_id` | Account | `numeric(10,0)` |
| `dateacct` | Account Date | `timestamp without time zone` |
| `gl_budget_id` | Budget | `numeric(10,0)` |
| `postingtype` | Posting Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-t_inventoryvalue"></a>
## `t_inventoryvalue` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `T_InventoryValue`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='T_InventoryValue'; 주요 열 qtyonhand; FK mwarehouse_tinventoryvalue; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `qtyonhand` | On Hand Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mwarehouse_tinventoryvalue` | `t_inventoryvalue.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | Warehouse |

<a id="t-t_invoicegl"></a>
## `t_invoicegl` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `T_InvoiceGL`
- 사전 Description: Gain/Loss - actual data shown id T_InvoiceGL_v
- 근거 문장: 사전 Name='T_InvoiceGL'; Description='Gain/Loss - actual data shown id T_InvoiceGL_v'; 주요 열 amtsourcebalance, amtacctbalance; FK factacct_tinvoicegl; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `amtsourcebalance` | Source Balance | `numeric` |
| `amtacctbalance` | Accounted Balance | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `factacct_tinvoicegl` | `t_invoicegl.(fact_acct_id)` → `fact_acct.(fact_acct_id)` | Accounting Fact |

<a id="t-t_moveclient"></a>
## `t_moveclient` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 ad_pinstance_id, tablename, source_key, target_key; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_pinstance_id` | 미지정 | `numeric(10,0)` |
| `tablename` | 미지정 | `character varying(40)` |
| `source_key` | 미지정 | `character varying(36)` |
| `target_key` | 미지정 | `character varying(36)` |
| `identifier` | 미지정 | `character varying(4000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_mrp_crp"></a>
## `t_mrp_crp` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Temporal MRP & CRP`
- 사전 Description: Temporal MRP & CRP
- 근거 문장: 사전 Name='Temporal MRP & CRP'; Description='Temporal MRP & CRP'; 주요 열 ad_pinstance_id, seqno; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_pinstance_id` | Process Instance | `numeric(10,0)` |
| `seqno` | Sequence | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_reconciliation"></a>
## `t_reconciliation` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Account reconciliation report`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Account reconciliation report'; 주요 열 ad_pinstance_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_pinstance_id` | Process Instance | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-t_replenish"></a>
## `t_replenish` — 재고·창고·로케이터

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `T_Replenish`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='T_Replenish'; 주요 열 qtyonhand, qtyreserved, m_warehousesource_id; FK mwarehouse_treplenish, mwarehousesource_treplenish; 사전 의미와 열/FK가 재고·창고·로케이터를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `qtyonhand` | On Hand Quantity | `numeric` |
| `qtyreserved` | Reserved Quantity | `numeric` |
| `m_warehousesource_id` | Source Warehouse | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `mwarehouse_treplenish` | `t_replenish.(m_warehouse_id)` → `m_warehouse.(m_warehouse_id)` | Warehouse |
| outgoing | `mwarehousesource_treplenish` | `t_replenish.(m_warehousesource_id)` → `m_warehouse.(m_warehouse_id)` | Warehouse |

<a id="t-t_report"></a>
## `t_report` — 보고서·성과·대시보드

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `T_Report`
- 사전 Description: Temporary Reporting Table
- 근거 문장: 사전 Name='T_Report'; Description='Temporary Reporting Table'; 주요 열 근거 부족; FK pareportline_treport; 사전 의미와 열/FK가 보고서·성과·대시보드를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `report`를 근거로, 구조 근거가 있는 `reporting` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `pareportline_treport` | `t_report.(pa_reportline_id)` → `pa_reportline.(pa_reportline_id)` | Report Line |

<a id="t-t_reportstatement"></a>
## `t_reportstatement` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `T_ReportStatement`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='T_ReportStatement'; 주요 열 levelno, dateacct, amtacctdr, amtacctcr; FK adpinstance_treportstatement; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `levelno` | Level no | `numeric(10,0)` |
| `dateacct` | Account Date | `timestamp without time zone` |
| `amtacctdr` | Accounted Debit | `numeric` |
| `amtacctcr` | Accounted Credit | `numeric` |
| `balance` | Balance | `numeric` |
| `qty` | Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adpinstance_treportstatement` | `t_reportstatement.(ad_pinstance_id)` → `ad_pinstance.(ad_pinstance_id)` | Process Instance |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_selection"></a>
## `t_selection` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 viewid; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `viewid` | 미지정 | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_selection2"></a>
## `t_selection2` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 근거 부족; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_selection_infowindow"></a>
## `t_selection_infowindow` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `미지정`
- 사전 Description: 미지정
- 근거 문장: 사전 Name=None; 주요 열 viewid, value_string, value_date, value_number; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `viewid` | 미지정 | `character varying(2000)` |
| `value_string` | 미지정 | `character varying(4000)` |
| `value_date` | 미지정 | `timestamp without time zone` |
| `value_number` | 미지정 | `numeric` |
| `info` | 미지정 | `character varying(60)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_spool"></a>
## `t_spool` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `T_Spool`
- 사전 Description: Temporary Spool Table
- 근거 문장: 사전 Name='T_Spool'; Description='Temporary Spool Table'; 주요 열 msgtext; FK adpinstance_tspool; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `msgtext` | Message Text | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adpinstance_tspool` | `t_spool.(ad_pinstance_id)` → `ad_pinstance.(ad_pinstance_id)` | Process Instance |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_transaction"></a>
## `t_transaction` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `T_Transaction`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='T_Transaction'; 주요 열 movementtype, m_locator_id, m_product_id, m_attributesetinstance_id; FK adpinstance_ttransaction, cprojectissue_ttransaction; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `movementtype` | Movement Type | `character(2)` |
| `m_locator_id` | Locator | `numeric(10,0)` |
| `m_product_id` | Product | `numeric(10,0)` |
| `m_attributesetinstance_id` | Attribute Set Instance | `numeric(10,0)` |
| `movementdate` | Movement Date | `timestamp without time zone` |
| `movementqty` | Movement Quantity | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adpinstance_ttransaction` | `t_transaction.(ad_pinstance_id)` → `ad_pinstance.(ad_pinstance_id)` | Process Instance |
| outgoing | `cprojectissue_ttransaction` | `t_transaction.(c_projectissue_id)` → `c_projectissue.(c_projectissue_id)` | Project Issue |
| outgoing | `masi_ttransaction` | `t_transaction.(m_attributesetinstance_id)` → `m_attributesetinstance.(m_attributesetinstance_id)` | Attribute Set Instance |
| outgoing | `minoutline_ttransaction` | `t_transaction.(m_inoutline_id)` → `m_inoutline.(m_inoutline_id)` | Shipment/Receipt Line |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-t_trialbalance"></a>
## `t_trialbalance` — 회계·원장·예산

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Trial Balance`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Trial Balance'; 주요 열 c_acctschema_id, dateacct, gl_budget_id, postingtype; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 회계·원장·예산를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_acctschema_id` | Accounting Schema | `numeric(10,0)` |
| `dateacct` | Account Date | `timestamp without time zone` |
| `gl_budget_id` | Budget | `numeric(10,0)` |
| `postingtype` | Posting Type | `character(1)` |
| `amtsourcedr` | Source Debit | `numeric` |
| `amtsourcecr` | Source Credit | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

<a id="t-test"></a>
## `test` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Test ID`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Test ID'; 주요 열 t_integer, t_number, t_date, t_datetime; FK adtable_test, vc_account_test; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `t_integer` | Integer | `numeric(10,0)` |
| `t_number` | Number | `numeric` |
| `t_date` | Date | `timestamp without time zone` |
| `t_datetime` | DateTime | `timestamp without time zone` |
| `c_uom_id` | UOM | `numeric(10,0)` |
| `t_qty` | Qty | `numeric` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adtable_test` | `test.(ad_table_id)` → `ad_table.(ad_table_id)` | Table |
| outgoing | `vc_account_test` | `test.(account_acct)` → `c_validcombination.(c_validcombination_id)` | Combination |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-testuu"></a>
## `testuu` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Test UU Based Table`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Test UU Based Table'; 주요 열 근거 부족; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-testuu_trl"></a>
## `testuu_trl` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Test UU Based Table Trl`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Test UU Based Table Trl'; 주요 열 istranslated; FK adlanguage_testuutrl; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `istranslated` | Translated | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adlanguage_testuutrl` | `testuu_trl.(ad_language)` → `ad_language.(ad_language)` | Language ID |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-testuudet"></a>
## `testuudet` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Test UU Detail`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Test UU Detail'; 주요 열 testuu_uus; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `testuu_uus` | Multi Test UU | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-u_blacklistcheque"></a>
## `u_blacklistcheque` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Black List Cheque`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Black List Cheque'; 주요 열 bankname, chequeno; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `bankname` | Bank Name | `character varying(120)` |
| `chequeno` | Cheque No | `character varying(120)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-u_posterminal"></a>
## `u_posterminal` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `POS Terminal`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='POS Terminal'; 주요 열 autolock, card_bankaccount_id, cardtransferbankaccount_id, cardtransfercashbook_id; FK cardbankaccount_uposterminal, cardtransferbankaccount_uposte; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `autolock` | Auto Lock | `character(1)` |
| `card_bankaccount_id` | Card Bank Account | `numeric(10,0)` |
| `cardtransferbankaccount_id` | Transfer Card trx to | `numeric(10,0)` |
| `cardtransfercashbook_id` | Transfer Card trx to | `numeric(10,0)` |
| `cardtransfertype` | Card Transfer Type | `character(1)` |
| `cashbooktransfertype` | Cash Book Transfer Type | `character(1)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `cardbankaccount_uposterminal` | `u_posterminal.(card_bankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |
| outgoing | `cardtransferbankaccount_uposte` | `u_posterminal.(cardtransferbankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |
| outgoing | `cardtransfercashbook_upostermi` | `u_posterminal.(cardtransfercashbook_id)` → `c_cashbook.(c_cashbook_id)` | Cash Book |
| outgoing | `cashtransferbankaccount_uposte` | `u_posterminal.(cashtransferbankaccount_id)` → `c_bankaccount.(c_bankaccount_id)` | Bank Account |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-u_rolemenu"></a>
## `u_rolemenu` — 사용자·인증·접근 권한

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Role Menu`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Role Menu'; 주요 열 ad_role_id; FK adrole_urolemenu; 사전 의미와 열/FK가 사용자·인증·접근 권한를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ad_role_id` | Role | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `adrole_urolemenu` | `u_rolemenu.(ad_role_id)` → `ad_role.(ad_role_id)` | Role |

<a id="t-u_web_properties"></a>
## `u_web_properties` — 업무영역 확인 필요

상태: **확인 필요**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Properties`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Properties'; 주요 열 u_key, u_value; FK 합치하는 참조 근거 없음; 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `u_key` | Key | `character varying(240)` |
| `u_value` | Value | `character varying(240)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |

검토 후보: 해당 사전/구조 규칙의 합치 후보 없음.
확인 필요 사유: 사전 의미와 독립적인 주요 열/FK 근거의 합치가 없거나, 서로 다른 영역의 근거 점수가 같아 하나로 제안하지 않음.

<a id="t-u_webmenu"></a>
## `u_webmenu` — 애플리케이션 사전·화면·서식

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Menu`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Menu'; 주요 열 근거 부족; FK uwebmenu_urolemenu, parentmenu_uwebmenu; 사전 의미와 열/FK가 애플리케이션 사전·화면·서식를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `uwebmenu_urolemenu` | `u_rolemenu.(u_webmenu_id)` → `u_webmenu.(u_webmenu_id)` | Role Menu |
| outgoing | `parentmenu_uwebmenu` | `u_webmenu.(parentmenu_id)` → `u_webmenu.(u_webmenu_id)` | Web Menu |

<a id="t-w_advertisement"></a>
## `w_advertisement` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Advertisement`
- 사전 Description: Web Advertisement
- 근거 문장: 사전 Name='Advertisement'; Description='Web Advertisement'; 주요 열 c_bpartner_id, w_clickcount_id, w_countercount_id, imageurl; FK wclickcount_wadvertisement, wcountercount_wadvertisement; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `w_clickcount_id` | Click Count | `numeric(10,0)` |
| `w_countercount_id` | Counter Count | `numeric(10,0)` |
| `imageurl` | Image URL | `character varying(120)` |
| `webparam1` | Web Parameter 1 | `character varying(2000)` |
| `webparam2` | Web Parameter 2 | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `wclickcount_wadvertisement` | `w_advertisement.(w_clickcount_id)` → `w_clickcount.(w_clickcount_id)` | Click Count |
| outgoing | `wcountercount_wadvertisement` | `w_advertisement.(w_countercount_id)` → `w_countercount.(w_countercount_id)` | Counter Count |

<a id="t-w_basket"></a>
## `w_basket` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Basket`
- 사전 Description: Web Basket
- 근거 문장: 사전 Name='Basket'; Description='Web Basket'; 주요 열 c_bpartner_id, m_pricelist_id; FK wbasket_wbasketline; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `basket`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |
| `m_pricelist_id` | Price List | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `wbasket_wbasketline` | `w_basketline.(w_basket_id)` → `w_basket.(w_basket_id)` | Basket Line |

<a id="t-w_basketline"></a>
## `w_basketline` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Basket Line`
- 사전 Description: Web Basket Line
- 근거 문장: 사전 Name='Basket Line'; Description='Web Basket Line'; 주요 열 w_basket_id; FK wbasket_wbasketline; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `basket`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `w_basket_id` | Basket | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `wbasket_wbasketline` | `w_basketline.(w_basket_id)` → `w_basket.(w_basket_id)` | Basket |

<a id="t-w_click"></a>
## `w_click` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Click`
- 사전 Description: Individual Web Click
- 근거 문장: 사전 Name='Web Click'; Description='Individual Web Click'; 주요 열 targeturl, w_clickcount_id; FK wclickcount_wclick; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web click`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `targeturl` | Target URL | `character varying(120)` |
| `w_clickcount_id` | Click Count | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `wclickcount_wclick` | `w_click.(w_clickcount_id)` → `w_clickcount.(w_clickcount_id)` | Click Count |

<a id="t-w_clickcount"></a>
## `w_clickcount` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Click Count`
- 사전 Description: Web Click Management
- 근거 문장: 사전 Name='Click Count'; Description='Web Click Management'; 주요 열 targeturl, c_bpartner_id; FK wclickcount_wadvertisement, wclickcount_wclick; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `web click`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `targeturl` | Target URL | `character varying(120)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `wclickcount_wadvertisement` | `w_advertisement.(w_clickcount_id)` → `w_clickcount.(w_clickcount_id)` | Advertisement |
| incoming | `wclickcount_wclick` | `w_click.(w_clickcount_id)` → `w_clickcount.(w_clickcount_id)` | Web Click |

<a id="t-w_counter"></a>
## `w_counter` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Counter`
- 사전 Description: Individual Count hit
- 근거 문장: 사전 Name='Web Counter'; Description='Individual Count hit'; 주요 열 pageurl, w_countercount_id; FK wcountercount_wcounter; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web counter`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pageurl` | Page URL | `character varying(120)` |
| `w_countercount_id` | Counter Count | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `wcountercount_wcounter` | `w_counter.(w_countercount_id)` → `w_countercount.(w_countercount_id)` | Counter Count |

<a id="t-w_countercount"></a>
## `w_countercount` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Counter Count`
- 사전 Description: Web Counter Count Management
- 근거 문장: 사전 Name='Counter Count'; Description='Web Counter Count Management'; 주요 열 pageurl, c_bpartner_id; FK wcountercount_wadvertisement, wcountercount_wcounter; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `web counter`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `pageurl` | Page URL | `character varying(120)` |
| `c_bpartner_id` | Business Partner | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `wcountercount_wadvertisement` | `w_advertisement.(w_countercount_id)` → `w_countercount.(w_countercount_id)` | Advertisement |
| incoming | `wcountercount_wcounter` | `w_counter.(w_countercount_id)` → `w_countercount.(w_countercount_id)` | Web Counter |

<a id="t-w_mailmsg"></a>
## `w_mailmsg` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Mail Message`
- 사전 Description: Web Store Mail Message Template
- 근거 문장: 사전 Name='Mail Message'; Description='Web Store Mail Message Template'; 주요 열 w_store_id; FK wmailmsg_wmailmsgtrl, wstore_wmailmsg; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `web store`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `w_store_id` | Web Store | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `wmailmsg_wmailmsgtrl` | `w_mailmsg_trl.(w_mailmsg_id)` → `w_mailmsg.(w_mailmsg_id)` | Mail Message Trl |
| outgoing | `wstore_wmailmsg` | `w_mailmsg.(w_store_id)` → `w_store.(w_store_id)` | Web Store |

<a id="t-w_mailmsg_trl"></a>
## `w_mailmsg_trl` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Mail Message Trl`
- 사전 Description: Web Store Mail Message Template
- 근거 문장: 사전 Name='Mail Message Trl'; Description='Web Store Mail Message Template'; 주요 열 근거 부족; FK wmailmsg_wmailmsgtrl; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Description의 `web store`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `wmailmsg_wmailmsgtrl` | `w_mailmsg_trl.(w_mailmsg_id)` → `w_mailmsg.(w_mailmsg_id)` | Mail Message |

<a id="t-w_store"></a>
## `w_store` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Store`
- 사전 Description: A Web Store of the Client
- 근거 문장: 사전 Name='Web Store'; Description='A Web Store of the Client'; 주요 열 webinfo, webparam1, webparam2, webparam3; FK wstore_wmailmsg, wstore_wstoretrl; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web store`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `webinfo` | Web Store Info | `character varying(2000)` |
| `webparam1` | Web Parameter 1 | `character varying(2000)` |
| `webparam2` | Web Parameter 2 | `character varying(2000)` |
| `webparam3` | Web Parameter 3 | `character varying(2000)` |
| `webparam4` | Web Parameter 4 | `character varying(2000)` |
| `webparam5` | Web Parameter 5 | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `wstore_wmailmsg` | `w_mailmsg.(w_store_id)` → `w_store.(w_store_id)` | Mail Message |
| incoming | `wstore_wstoretrl` | `w_store_trl.(w_store_id)` → `w_store.(w_store_id)` | Web Store Trl |

<a id="t-w_store_trl"></a>
## `w_store_trl` — 웹 상점·POS·웹 접점

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Store Trl`
- 사전 Description: A Web Store of the Tenant
- 근거 문장: 사전 Name='Web Store Trl'; Description='A Web Store of the Tenant'; 주요 열 webinfo, webparam1, webparam2, webparam3; FK wstore_wstoretrl; 사전 의미와 열/FK가 웹 상점·POS·웹 접점를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web store`를 근거로, 구조 근거가 있는 `web-store` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `webinfo` | Web Store Info | `character varying(2000)` |
| `webparam1` | Web Parameter 1 | `character varying(2000)` |
| `webparam2` | Web Parameter 2 | `character varying(2000)` |
| `webparam3` | Web Parameter 3 | `character varying(2000)` |
| `webparam4` | Web Parameter 4 | `character varying(2000)` |
| `webparam5` | Web Parameter 5 | `character varying(2000)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `wstore_wstoretrl` | `w_store_trl.(w_store_id)` → `w_store.(w_store_id)` | Web Store |

<a id="t-ws_webservice"></a>
## `ws_webservice` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Service`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Service'; 주요 열 근거 부족; FK wswebservice_wswebservicemetho, wswebservice_wswebservicetype; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web service`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `wswebservice_wswebservicemetho` | `ws_webservicemethod.(ws_webservice_id)` → `ws_webservice.(ws_webservice_id)` | Web Service Method |
| incoming | `wswebservice_wswebservicetype` | `ws_webservicetype.(ws_webservice_id)` → `ws_webservice.(ws_webservice_id)` | Web Service Type |

<a id="t-ws_webservice_para"></a>
## `ws_webservice_para` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Service Parameters`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Service Parameters'; 주요 열 ws_webservicetype_id; FK wswebservicetype_wswebservicep; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web service`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ws_webservicetype_id` | Web Service Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `wswebservicetype_wswebservicep` | `ws_webservice_para.(ws_webservicetype_id)` → `ws_webservicetype.(ws_webservicetype_id)` | Web Service Type |

<a id="t-ws_webservicefieldinput"></a>
## `ws_webservicefieldinput` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Service Field Input`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Service Field Input'; 주요 열 ws_webservicetype_id; FK wswebservicetype_wswebservicfi; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web service`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ws_webservicetype_id` | Web Service Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `wswebservicetype_wswebservicfi` | `ws_webservicefieldinput.(ws_webservicetype_id)` → `ws_webservicetype.(ws_webservicetype_id)` | Web Service Type |

<a id="t-ws_webservicefieldoutput"></a>
## `ws_webservicefieldoutput` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Service Field Output`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Service Field Output'; 주요 열 ws_webservicetype_id; FK wswebservicetype_wswebservicfo; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web service`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ws_webservicetype_id` | Web Service Type | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `wswebservicetype_wswebservicfo` | `ws_webservicefieldoutput.(ws_webservicetype_id)` → `ws_webservicetype.(ws_webservicetype_id)` | Web Service Type |

<a id="t-ws_webservicemethod"></a>
## `ws_webservicemethod` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Service Method`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Service Method'; 주요 열 ws_webservice_id; FK wswebservicemethod_wswebservic, wswebservice_wswebservicemetho; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web service`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ws_webservice_id` | Web Service | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `wswebservicemethod_wswebservic` | `ws_webservicetype.(ws_webservicemethod_id)` → `ws_webservicemethod.(ws_webservicemethod_id)` | Web Service Type |
| outgoing | `wswebservice_wswebservicemetho` | `ws_webservicemethod.(ws_webservice_id)` → `ws_webservice.(ws_webservice_id)` | Web Service |

<a id="t-ws_webservicetype"></a>
## `ws_webservicetype` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Service Type`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Service Type'; 주요 열 ws_webservice_id, ws_webservicemethod_id; FK wswebservicetype_wswebservicep, wswebservicetype_wswebservicet; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web service`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| `ws_webservice_id` | Web Service | `numeric(10,0)` |
| `ws_webservicemethod_id` | Web Service Method | `numeric(10,0)` |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| incoming | `wswebservicetype_wswebservicep` | `ws_webservice_para.(ws_webservicetype_id)` → `ws_webservicetype.(ws_webservicetype_id)` | Web Service Parameters |
| incoming | `wswebservicetype_wswebservicet` | `ws_webservicetypeaccess.(ws_webservicetype_id)` → `ws_webservicetype.(ws_webservicetype_id)` | Web Service Type Access |
| incoming | `wswebservicetype_wswebservicfi` | `ws_webservicefieldinput.(ws_webservicetype_id)` → `ws_webservicetype.(ws_webservicetype_id)` | Web Service Field Input |
| incoming | `wswebservicetype_wswebservicfo` | `ws_webservicefieldoutput.(ws_webservicetype_id)` → `ws_webservicetype.(ws_webservicetype_id)` | Web Service Field Output |

<a id="t-ws_webservicetypeaccess"></a>
## `ws_webservicetypeaccess` — 데이터 연계·가져오기·내보내기

상태: **근거 기반 분류안(공식 분류 아님)**. 방식: 자동 사전 의미 + 주요 열/FK 교차대조. 업무 담당자 공식 승인: 없음.

- 사전 Name: `Web Service Type Access`
- 사전 Description: 미지정
- 근거 문장: 사전 Name='Web Service Type Access'; 주요 열 근거 부족; FK wswebservicetype_wswebservicet; 사전 의미와 열/FK가 데이터 연계·가져오기·내보내기를 함께 가리켜 제안.

명시 용도 구분: 사전 Name의 `web service`를 근거로, 구조 근거가 있는 `data-exchange` 후보를 선택했습니다.

| 주요 열 | 원본 열 논리명 | 타입 |
|---|---|---|
| 없음/근거 부족 | — | — |

| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |
|---|---|---|---|
| outgoing | `wswebservicetype_wswebservicet` | `ws_webservicetypeaccess.(ws_webservicetype_id)` → `ws_webservicetype.(ws_webservicetype_id)` | Web Service Type |
