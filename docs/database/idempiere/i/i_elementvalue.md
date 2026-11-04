# i_elementvalue — 계정과목 가져오기

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.i_elementvalue` |
| 한국어 논리명(문서용 해석) | 계정과목 가져오기 |
| 원본 논리명 | Import Account |
| 원본 사전 ID | 534 |
| 분류 | `i` — 데이터 가져오기 준비 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 31 |
| 나가는 FK / 들어오는 FK | 4 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

외부 계정 코드와 계정 유형·상위 계정 정보를 계정과목 사전으로 가져오기 위한 중간 데이터를 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Import Account Value
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `i_elementvalue_pkey` | `i_elementvalue_id` |
| UNIQUE | `i_elementvalue_uu_idx` | `i_elementvalue_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `i_elementvalue_id` | Import Account | numeric(10,0) | 불가 | 예 | — | Import Account Value |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 허용 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 허용 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 허용 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `createdby` | Created By | numeric(10,0) | 허용 | — | — | User who created this records |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 허용 | — | — | User who updated this records |
| 9 | `i_isimported` | Imported | character(1) | 불가 | — | 'N'::bpchar | Has this import been processed |
| 10 | `i_errormsg` | Import Error Message | character varying(2000) | 허용 | — | — | Messages generated from import process |
| 11 | `c_element_id` | Element | numeric(10,0) | 허용 | — | — | Accounting Element |
| 12 | `elementname` | Element Name | character varying(60) | 허용 | — | — | Name of the Element |
| 13 | `c_elementvalue_id` | Account Element | numeric(10,0) | 허용 | — | — | Account Element |
| 14 | `value` | Search Key | character varying(40) | 허용 | — | — | Search key for the record in the format required - must be unique |
| 15 | `name` | Name | character varying(60) | 허용 | — | — | Alphanumeric identifier of the entity |
| 16 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 17 | `accounttype` | Account Type | character(1) | 허용 | — | — | Indicates the type of account |
| 18 | `accountsign` | Account Sign | character(1) | 허용 | — | — | Indicates the Natural Sign of the Account as a Debit or Credit |
| 19 | `isdoccontrolled` | Document Controlled | character(1) | 허용 | — | 'N'::bpchar | Control account - If an account is controlled by a document, you cannot post manually to it |
| 20 | `issummary` | Summary Level | character(1) | 허용 | — | 'N'::bpchar | This is a summary entity |
| 21 | `parentvalue` | Parent Key | character varying(40) | 허용 | — | — | Key if the Parent |
| 22 | `parentelementvalue_id` | Parent Account | numeric(10,0) | 허용 | — | — | The parent (summary) account |
| 23 | `postactual` | Post Actual | character(1) | 허용 | — | 'Y'::bpchar | Actual Values can be posted |
| 24 | `postbudget` | Post Budget | character(1) | 허용 | — | 'Y'::bpchar | Budget values can be posted |
| 25 | `poststatistical` | Post Statistical | character(1) | 허용 | — | 'Y'::bpchar | Post statistical quantities to this account? |
| 26 | `postencumbrance` | Post Encumbrance | character(1) | 허용 | — | 'Y'::bpchar | Post commitments to this account |
| 27 | `default_account` | Default Account | character varying(30) | 허용 | — | — | Name of the Default Account Column |
| 28 | `ad_column_id` | Column | numeric(10,0) | 허용 | — | — | Column in the table |
| 29 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 30 | `processed` | Processed | character(1) | 허용 | — | 'N'::bpchar | The document has been processed |
| 31 | `i_elementvalue_uu` | I_ElementValue_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_column"]
    n1["c_element"]
    n2["c_elementvalue"]
    n3["i_elementvalue"]
    n3 -->|"ad_column_id → ad_column_id"| n0
    n3 -->|"c_element_id → c_element_id"| n1
    n3 -->|"c_elementvalue_id → c_elementvalue_id"| n2
    n3 -->|"parentelementvalue_id → c_elementvalue_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adcolumn_ielementvalue` <!-- FK_OUT: adempiere.i_elementvalue.adcolumn_ielementvalue --> | [`i_elementvalue`](i_elementvalue.md) | `ad_column_id` | [`ad_column`](../ad/ad_column.md) | `ad_column_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `celement_ielementvalue` <!-- FK_OUT: adempiere.i_elementvalue.celement_ielementvalue --> | [`i_elementvalue`](i_elementvalue.md) | `c_element_id` | [`c_element`](../c/c_element.md) | `c_element_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalue_ielementvalue` <!-- FK_OUT: adempiere.i_elementvalue.celementvalue_ielementvalue --> | [`i_elementvalue`](i_elementvalue.md) | `c_elementvalue_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cevalueparent_ielementvalue` <!-- FK_OUT: adempiere.i_elementvalue.cevalueparent_ielementvalue --> | [`i_elementvalue`](i_elementvalue.md) | `parentelementvalue_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
