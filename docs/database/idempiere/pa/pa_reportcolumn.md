# pa_reportcolumn — 재무 보고서 열

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.pa_reportcolumn` |
| 한국어 논리명(문서용 해석) | 재무 보고서 열 |
| 원본 논리명 | Report Column |
| 원본 사전 ID | 446 |
| 분류 | `pa` — 성과·보고서·대시보드 |
| 전체 테넌트 행 수 | 17 |
| 물리 열 수 | 59 |
| 나가는 FK / 들어오는 FK | 15 / 3 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

보고서에 표시할 개별 열을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Column in Report
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `pa_reportcolumn_pkey` | `pa_reportcolumn_id` |
| UNIQUE | `pa_reportcolumn_uu_idx` | `pa_reportcolumn_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `pa_reportcolumn_id` | Report Column | numeric(10,0) | 불가 | 예 | — | Column in Report |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `pa_reportcolumnset_id` | Report Column Set | numeric(10,0) | 불가 | — | — | Collection of Columns for Report |
| 10 | `name` | Name | character varying(255) | 불가 | — | — | Alphanumeric identifier of the entity |
| 11 | `seqno` | Sequence | numeric(10,0) | 불가 | — | — | Method of ordering records; lowest number comes first |
| 12 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 13 | `isprinted` | Printed | character(1) | 불가 | — | 'Y'::bpchar | Indicates if this document / line is printed |
| 14 | `postingtype` | Posting Type | character(1) | 불가 | — | — | The type of posted amount for the transaction |
| 15 | `gl_budget_id` | Budget | numeric(10,0) | 허용 | — | — | General Ledger Budget |
| 16 | `columntype` | Column Type | character(1) | 불가 | — | — | — |
| 17 | `relativeperiod` | Relative Period | numeric(10,0) | 허용 | — | — | Period offset (0 is current) |
| 18 | `currencytype` | Currency Type | character(1) | 허용 | — | — | — |
| 19 | `calculationtype` | Calculation | character(1) | 허용 | — | — | — |
| 20 | `amounttype` | Amount Type | character(2) | 허용 | — | — | Type of amount to report |
| 21 | `c_currency_id` | Currency | numeric(10,0) | 허용 | — | — | The Currency for this record |
| 22 | `isadhocconversion` | Ad hoc Conversion | character(1) | 허용 | — | 'N'::bpchar | Perform conversion for all amounts to currency |
| 23 | `oper_1_id` | Operand 1 | numeric(10,0) | 허용 | — | — | First operand for calculation |
| 24 | `oper_2_id` | Operand 2 | numeric(10,0) | 허용 | — | — | Second operand for calculation |
| 25 | `elementtype` | Type | character(2) | 허용 | — | — | Element Type (account or user defined) |
| 26 | `org_id` | Organization | numeric(10,0) | 허용 | — | — | Organizational entity within tenant |
| 27 | `c_elementvalue_id` | Account Element | numeric(10,0) | 허용 | — | — | Account Element |
| 28 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 29 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 30 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 31 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | — | Marketing Campaign |
| 32 | `c_location_id` | Address | numeric(10,0) | 허용 | — | — | Location or Address |
| 33 | `c_salesregion_id` | Sales Region | numeric(10,0) | 허용 | — | — | Sales coverage region |
| 34 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 35 | `userelement1_id` | User Column 1 | numeric(10,0) | 허용 | — | — | User defined accounting Element |
| 36 | `userelement2_id` | User Column 2 | numeric(10,0) | 허용 | — | — | User defined accounting Element |
| 37 | `isincludenullsorg` | Include Nulls in Org | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the organization |
| 38 | `isincludenullselementvalue` | Include Nulls in Account | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the account |
| 39 | `isincludenullsbpartner` | Include Nulls in BPartner | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the business partner |
| 40 | `isincludenullsproduct` | Include Nulls in Product | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the product |
| 41 | `isincludenullslocation` | Include Nulls in Location | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the location |
| 42 | `isincludenullsproject` | Include Nulls in Project | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the project |
| 43 | `isincludenullssalesregion` | Include Nulls in Sales Region | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the sales region |
| 44 | `isincludenullsactivity` | Include Nulls in Activity | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the activity |
| 45 | `isincludenullscampaign` | Include Nulls in Campaign | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the campaign |
| 46 | `isincludenullsuserelement1` | Include Nulls in User Element 1 | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the user element 1 |
| 47 | `isincludenullsuserelement2` | Include Nulls in User Element 2 | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the user element 2 |
| 48 | `factor` | Factor | character(1) | 허용 | — | — | Scaling factor. |
| 49 | `formatpattern` | Format Pattern | character varying(22) | 허용 | — | — | The pattern used to format a number or date. |
| 50 | `isincludenullsorgtrx` | Include Nulls in Org Trx | character(1) | 불가 | — | 'N'::bpchar | Include nulls in the selection of the organization transaction |
| 51 | `ad_orgtrx_id` | Trx Organization | numeric(10,0) | 허용 | — | — | Performing or initiating organization |
| 52 | `paperiodtype` | Period Type | character(1) | 허용 | — | 'P'::bpchar | PA Period Type |
| 53 | `paamounttype` | Amount Type | character(1) | 허용 | — | 'B'::bpchar | PA Amount Type for reporting |
| 54 | `pa_reportcolumn_uu` | PA_ReportColumn_UU | uuid | 허용 | — | — | — |
| 55 | `oper_2_linename` | Operand 2 Line Name | character varying(512) | 허용 | — | NULL::character varying | Name of the financial report line to take values from |
| 56 | `isallowoppositesign` | Allow Opposite Sign | character(1) | 허용 | — | 'N'::bpchar | Allow column values to be displayed with the opposite sign |
| 57 | `relativeperiodto` | Relative Period To | numeric | 허용 | — | — | Period offset (0 is current) |
| 58 | `roundfactor` | Round Factor | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 59 | `multiplier` | Multiplier | numeric | 허용 | — | — | Type Multiplier (Credit = -1) |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 16개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_org"]
    n1["c_activity"]
    n2["c_bpartner"]
    n3["c_campaign"]
    n4["c_currency"]
    n5["c_elementvalue"]
    n6["c_location"]
    n7["c_project"]
    n8["c_salesregion"]
    n9["pa_reportcolumn"]
    n9 -->|"org_id → ad_org_id"| n0
    n9 -->|"ad_orgtrx_id → ad_org_id"| n0
    n9 -->|"c_activity_id → c_activity_id"| n1
    n9 -->|"c_bpartner_id → c_bpartner_id"| n2
    n9 -->|"c_campaign_id → c_campaign_id"| n3
    n9 -->|"c_currency_id → c_currency_id"| n4
    n9 -->|"c_elementvalue_id → c_elementvalue_id"| n5
    n9 -->|"c_location_id → c_location_id"| n6
    n9 -->|"c_project_id → c_project_id"| n7
    n9 -->|"c_salesregion_id → c_salesregion_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adorg_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.adorg_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorgtrx_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.adorgtrx_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `ad_orgtrx_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.cactivity_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.cbpartner_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccampaign_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.ccampaign_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `c_campaign_id` | [`c_campaign`](../c/c_campaign.md) | `c_campaign_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.ccurrency_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalue_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.celementvalue_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `c_elementvalue_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `clocation_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.clocation_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `c_location_id` | [`c_location`](../c/c_location.md) | `c_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.cproject_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.csalesregion_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `c_salesregion_id` | [`c_salesregion`](../c/c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glbudget_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.glbudget_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `gl_budget_id` | [`gl_budget`](../gl/gl_budget.md) | `gl_budget_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_pareportcolumn` <!-- FK_OUT: adempiere.pa_reportcolumn.mproduct_pareportcolumn --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pareportcolumn_oper1` <!-- FK_OUT: adempiere.pa_reportcolumn.pareportcolumn_oper1 --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `oper_1_id` | [`pa_reportcolumn`](pa_reportcolumn.md) | `pa_reportcolumn_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `pareportcolumn_oper2` <!-- FK_OUT: adempiere.pa_reportcolumn.pareportcolumn_oper2 --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `oper_2_id` | [`pa_reportcolumn`](pa_reportcolumn.md) | `pa_reportcolumn_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `pareportcolumnset_column` <!-- FK_OUT: adempiere.pa_reportcolumn.pareportcolumnset_column --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `pa_reportcolumnset_id` | [`pa_reportcolumnset`](pa_reportcolumnset.md) | `pa_reportcolumnset_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `pareportcolumn_oper1` <!-- FK_IN: adempiere.pa_reportcolumn.pareportcolumn_oper1 --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `oper_1_id` | [`pa_reportcolumn`](pa_reportcolumn.md) | `pa_reportcolumn_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `pareportcolumn_oper2` <!-- FK_IN: adempiere.pa_reportcolumn.pareportcolumn_oper2 --> | [`pa_reportcolumn`](pa_reportcolumn.md) | `oper_2_id` | [`pa_reportcolumn`](pa_reportcolumn.md) | `pa_reportcolumn_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `pareportcolumn_pareportcolumnt` <!-- FK_IN: adempiere.pa_reportcolumn_trl.pareportcolumn_pareportcolumnt --> | [`pa_reportcolumn_trl`](pa_reportcolumn_trl.md) | `pa_reportcolumn_id` | [`pa_reportcolumn`](pa_reportcolumn.md) | `pa_reportcolumn_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
