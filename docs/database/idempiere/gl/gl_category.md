# gl_category — 원장 분류

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.gl_category` |
| 한국어 논리명(문서용 해석) | 원장 분류 |
| 원본 논리명 | GL Category |
| 원본 사전 ID | 218 |
| 분류 | `gl` — 총계정원장·예산·분개 |
| 전체 테넌트 행 수 | 10 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 0 / 11 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

총계정원장 문서와 분개를 분류하는 기준을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: General Ledger Category
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `gl_category_pkey` | `gl_category_id` |
| UNIQUE | `gl_category_uu_idx` | `gl_category_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `gl_category_name`: `CREATE UNIQUE INDEX gl_category_name ON adempiere.gl_category USING btree (ad_client_id, name)`
- `gl_category_value`: `CREATE UNIQUE INDEX gl_category_value ON adempiere.gl_category USING btree (ad_client_id, value)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `gl_category_id` | GL Category | numeric(10,0) | 불가 | 예 | — | General Ledger Category |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `categorytype` | Category Type | character(1) | 불가 | — | — | Source of the Journal with this category |
| 12 | `isdefault` | Default | character(1) | 불가 | — | 'N'::bpchar | Default value |
| 13 | `docbasetype` | Document Base Type | character(3) | 허용 | — | — | Logical type of document |
| 14 | `gl_category_uu` | GL_Category_UU | uuid | 허용 | — | — | — |
| 15 | `value` | Search Key | character varying(60) | 불가 | — | NULL::character varying | Search key for the record in the format required - must be unique |
| 16 | `printname` | Print Text | character varying(60) | 허용 | — | NULL::character varying | The label text to be printed on a document or correspondence. |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 11개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset_reval_entry"]
    n1["a_depreciation_entry"]
    n2["c_doctype"]
    n3["fact_acct"]
    n4["gl_category"]
    n5["gl_category_trl"]
    n6["gl_journal"]
    n7["gl_journalbatch"]
    n8["gl_journalgenerator"]
    n9["gl_journalgeneratorsource"]
    n10["i_fajournal"]
    n0 -->|"gl_category_id → gl_category_id"| n4
    n1 -->|"gl_category_id → gl_category_id"| n4
    n2 -->|"gl_category_id → gl_category_id"| n4
    n3 -->|"gl_category_id → gl_category_id"| n4
    n5 -->|"gl_category_id → gl_category_id"| n4
    n6 -->|"gl_category_id → gl_category_id"| n4
    n7 -->|"gl_category_id → gl_category_id"| n4
    n8 -->|"gl_category_id → gl_category_id"| n4
    n9 -->|"gl_category_id → gl_category_id"| n4
    n10 -->|"gl_category_id → gl_category_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `glcategory_aassetrevalentry` <!-- FK_IN: adempiere.a_asset_reval_entry.glcategory_aassetrevalentry --> | [`a_asset_reval_entry`](../a/a_asset_reval_entry.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_adepreciationentry` <!-- FK_IN: adempiere.a_depreciation_entry.glcategory_adepreciationentry --> | [`a_depreciation_entry`](../a/a_depreciation_entry.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_cdoctype` <!-- FK_IN: adempiere.c_doctype.glcategory_cdoctype --> | [`c_doctype`](../c/c_doctype.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_factacct` <!-- FK_IN: adempiere.fact_acct.glcategory_factacct --> | [`fact_acct`](../fact/fact_acct.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_glcategorytrl` <!-- FK_IN: adempiere.gl_category_trl.glcategory_glcategorytrl --> | [`gl_category_trl`](gl_category_trl.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_gljournal` <!-- FK_IN: adempiere.gl_journal.glcategory_gljournal --> | [`gl_journal`](gl_journal.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_gljournalbatch` <!-- FK_IN: adempiere.gl_journalbatch.glcategory_gljournalbatch --> | [`gl_journalbatch`](gl_journalbatch.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_qssjournalgenerator` <!-- FK_IN: adempiere.gl_journalgenerator.glcategory_qssjournalgenerator --> | [`gl_journalgenerator`](gl_journalgenerator.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_gljournalgenerators` <!-- FK_IN: adempiere.gl_journalgeneratorsource.glcategory_gljournalgenerators --> | [`gl_journalgeneratorsource`](gl_journalgeneratorsource.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_ifajournal` <!-- FK_IN: adempiere.i_fajournal.glcategory_ifajournal --> | [`i_fajournal`](../i/i_fajournal.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_igljournal` <!-- FK_IN: adempiere.i_gljournal.glcategory_igljournal --> | [`i_gljournal`](../i/i_gljournal.md) | `gl_category_id` | [`gl_category`](gl_category.md) | `gl_category_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
