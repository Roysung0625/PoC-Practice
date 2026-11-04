# c_period — 회계 기간

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_period` |
| 한국어 논리명(문서용 해석) | 회계 기간 |
| 원본 논리명 | Period |
| 원본 사전 ID | 145 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 360 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 3 / 17 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

회계 달력 안의 개별 기간을 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Period of the Calendar
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_period_pkey` | `c_period_id` |
| UNIQUE | `c_period_uu_idx` | `c_period_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `c_period_nounique`: `CREATE UNIQUE INDEX c_period_nounique ON adempiere.c_period USING btree (c_year_id, periodno)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_period_id` | Period | numeric(10,0) | 불가 | 예 | — | Period of the Calendar |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `periodno` | Period No | numeric(10,0) | 불가 | — | — | Unique Period Number |
| 11 | `c_year_id` | Year | numeric(10,0) | 불가 | — | — | Calendar Year |
| 12 | `startdate` | Start Date | timestamp without time zone | 불가 | — | — | First effective day (inclusive) |
| 13 | `enddate` | End Date | timestamp without time zone | 허용 | — | — | Last effective date (inclusive) |
| 14 | `periodtype` | Period Type | character(1) | 불가 | — | — | Period Type |
| 15 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 16 | `c_period_uu` | C_Period_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 20개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset_disposed"]
    n1["a_asset_reval_entry"]
    n2["a_asset_split"]
    n3["a_asset_transfer"]
    n4["a_depreciation_build"]
    n5["a_depreciation_entry"]
    n6["ad_client"]
    n7["ad_org"]
    n8["c_acctschema"]
    n9["c_period"]
    n10["c_year"]
    n9 -->|"ad_client_id → ad_client_id"| n6
    n9 -->|"ad_org_id → ad_org_id"| n7
    n9 -->|"c_year_id → c_year_id"| n10
    n0 -->|"c_period_id → c_period_id"| n9
    n1 -->|"c_period_id → c_period_id"| n9
    n2 -->|"c_period_id → c_period_id"| n9
    n3 -->|"c_period_id → c_period_id"| n9
    n4 -->|"c_period_id → c_period_id"| n9
    n5 -->|"c_period_id → c_period_id"| n9
    n8 -->|"c_period_id → c_period_id"| n9
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `c_periodclient` <!-- FK_OUT: adempiere.c_period.c_periodclient --> | [`c_period`](c_period.md) | `ad_client_id` | [`ad_client`](../ad/ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_periodorg` <!-- FK_OUT: adempiere.c_period.c_periodorg --> | [`c_period`](c_period.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_year_period` <!-- FK_OUT: adempiere.c_period.c_year_period --> | [`c_period`](c_period.md) | `c_year_id` | [`c_year`](c_year.md) | `c_year_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cperiod_aassetdisposed` <!-- FK_IN: adempiere.a_asset_disposed.cperiod_aassetdisposed --> | [`a_asset_disposed`](../a/a_asset_disposed.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_aassetrevalentry` <!-- FK_IN: adempiere.a_asset_reval_entry.cperiod_aassetrevalentry --> | [`a_asset_reval_entry`](../a/a_asset_reval_entry.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_aassetsplit` <!-- FK_IN: adempiere.a_asset_split.cperiod_aassetsplit --> | [`a_asset_split`](../a/a_asset_split.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_aassettransfer` <!-- FK_IN: adempiere.a_asset_transfer.cperiod_aassettransfer --> | [`a_asset_transfer`](../a/a_asset_transfer.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_adepreciationbuild` <!-- FK_IN: adempiere.a_depreciation_build.cperiod_adepreciationbuild --> | [`a_depreciation_build`](../a/a_depreciation_build.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_adepreciationentry` <!-- FK_IN: adempiere.a_depreciation_entry.cperiod_adepreciationentry --> | [`a_depreciation_entry`](../a/a_depreciation_entry.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_cacctschema` <!-- FK_IN: adempiere.c_acctschema.cperiod_cacctschema --> | [`c_acctschema`](c_acctschema.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_period_periodcontrol` <!-- FK_IN: adempiere.c_periodcontrol.c_period_periodcontrol --> | [`c_periodcontrol`](c_periodcontrol.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_factacct` <!-- FK_IN: adempiere.fact_acct.cperiod_factacct --> | [`fact_acct`](../fact/fact_acct.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_factacctsummary` <!-- FK_IN: adempiere.fact_acct_summary.cperiod_factacctsummary --> | [`fact_acct_summary`](../fact/fact_acct_summary.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_period_journal` <!-- FK_IN: adempiere.gl_journal.c_period_journal --> | [`gl_journal`](../gl/gl_journal.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_period_journalbatch` <!-- FK_IN: adempiere.gl_journalbatch.c_period_journalbatch --> | [`gl_journalbatch`](../gl/gl_journalbatch.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_hrperiod` <!-- FK_IN: adempiere.hr_period.cperiod_hrperiod --> | [`hr_period`](../hr/hr_period.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_ifajournal` <!-- FK_IN: adempiere.i_fajournal.cperiod_ifajournal --> | [`i_fajournal`](../i/i_fajournal.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_igljournal` <!-- FK_IN: adempiere.i_gljournal.cperiod_igljournal --> | [`i_gljournal`](../i/i_gljournal.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_mdemandline` <!-- FK_IN: adempiere.m_demandline.cperiod_mdemandline --> | [`m_demandline`](../m/m_demandline.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_mforecastline` <!-- FK_IN: adempiere.m_forecastline.cperiod_mforecastline --> | [`m_forecastline`](../m/m_forecastline.md) | `c_period_id` | [`c_period`](c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
