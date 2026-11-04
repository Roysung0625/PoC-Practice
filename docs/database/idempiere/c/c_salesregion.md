# c_salesregion — 영업 지역

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_salesregion` |
| 한국어 논리명(문서용 해석) | 영업 지역 |
| 원본 논리명 | Sales Region |
| 원본 사전 ID | 230 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 2 |
| 물리 열 수 | 15 |
| 나가는 FK / 들어오는 FK | 1 / 14 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

영업 활동의 담당 또는 적용 지역을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Sales coverage region
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_salesregion_pkey` | `c_salesregion_id` |
| UNIQUE | `c_salesregion_uu_idx` | `c_salesregion_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `c_salesregion_value`: `CREATE UNIQUE INDEX c_salesregion_value ON adempiere.c_salesregion USING btree (ad_client_id, value)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_salesregion_id` | Sales Region | numeric(10,0) | 불가 | 예 | — | Sales coverage region |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `value` | Search Key | character varying(40) | 불가 | — | — | Search key for the record in the format required - must be unique |
| 10 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `issummary` | Summary Level | character(1) | 불가 | — | 'N'::bpchar | This is a summary entity |
| 13 | `salesrep_id` | Sales Representative | numeric(10,0) | 허용 | — | — | Sales Representative or Company Agent |
| 14 | `isdefault` | Default | character(1) | 불가 | — | 'N'::bpchar | Default value |
| 15 | `c_salesregion_uu` | C_SalesRegion_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 15개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_user"]
    n1["c_acctschema_element"]
    n2["c_bpartner_location"]
    n3["c_commissionline"]
    n4["c_salesregion"]
    n5["c_salesregion_trl"]
    n6["c_validcombination"]
    n7["fact_acct"]
    n8["fact_acct_summary"]
    n9["gl_distribution"]
    n10["gl_distributionline"]
    n4 -->|"salesrep_id → ad_user_id"| n0
    n1 -->|"c_salesregion_id → c_salesregion_id"| n4
    n2 -->|"c_salesregion_id → c_salesregion_id"| n4
    n3 -->|"c_salesregion_id → c_salesregion_id"| n4
    n5 -->|"c_salesregion_id → c_salesregion_id"| n4
    n6 -->|"c_salesregion_id → c_salesregion_id"| n4
    n7 -->|"c_salesregion_id → c_salesregion_id"| n4
    n8 -->|"c_salesregion_id → c_salesregion_id"| n4
    n9 -->|"c_salesregion_id → c_salesregion_id"| n4
    n10 -->|"c_salesregion_id → c_salesregion_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `salesrep_csalesregion` <!-- FK_OUT: adempiere.c_salesregion.salesrep_csalesregion --> | [`c_salesregion`](c_salesregion.md) | `salesrep_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `csalesregion_caschemaelement` <!-- FK_IN: adempiere.c_acctschema_element.csalesregion_caschemaelement --> | [`c_acctschema_element`](c_acctschema_element.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_bpartnerlocation` <!-- FK_IN: adempiere.c_bpartner_location.csalesregion_bpartnerlocation --> | [`c_bpartner_location`](c_bpartner_location.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_ccommissionline` <!-- FK_IN: adempiere.c_commissionline.csalesregion_ccommissionline --> | [`c_commissionline`](c_commissionline.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_csalesregiontrl` <!-- FK_IN: adempiere.c_salesregion_trl.csalesregion_csalesregiontrl --> | [`c_salesregion_trl`](c_salesregion_trl.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_vc` <!-- FK_IN: adempiere.c_validcombination.csalesregion_vc --> | [`c_validcombination`](c_validcombination.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_salesregion_factacct` <!-- FK_IN: adempiere.fact_acct.c_salesregion_factacct --> | [`fact_acct`](../fact/fact_acct.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_factacctsummary` <!-- FK_IN: adempiere.fact_acct_summary.csalesregion_factacctsummary --> | [`fact_acct_summary`](../fact/fact_acct_summary.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregopn_gldist` <!-- FK_IN: adempiere.gl_distribution.csalesregopn_gldist --> | [`gl_distribution`](../gl/gl_distribution.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_gldistline` <!-- FK_IN: adempiere.gl_distributionline.csalesregion_gldistline --> | [`gl_distributionline`](../gl/gl_distributionline.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_gljournalline` <!-- FK_IN: adempiere.gl_journalline.csalesregion_gljournalline --> | [`gl_journalline`](../gl/gl_journalline.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_ifajournal` <!-- FK_IN: adempiere.i_fajournal.csalesregion_ifajournal --> | [`i_fajournal`](../i/i_fajournal.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_igljournal` <!-- FK_IN: adempiere.i_gljournal.csalesregion_igljournal --> | [`i_gljournal`](../i/i_gljournal.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_pareportcolumn` <!-- FK_IN: adempiere.pa_reportcolumn.csalesregion_pareportcolumn --> | [`pa_reportcolumn`](../pa/pa_reportcolumn.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_pareportsource` <!-- FK_IN: adempiere.pa_reportsource.csalesregion_pareportsource --> | [`pa_reportsource`](../pa/pa_reportsource.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
