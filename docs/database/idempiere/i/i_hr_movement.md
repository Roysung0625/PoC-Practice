# i_hr_movement — 급여 변동 내역 가져오기

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.i_hr_movement` |
| 한국어 논리명(문서용 해석) | 급여 변동 내역 가져오기 |
| 원본 논리명 | Payroll Movement Import |
| 원본 사전 ID | 53259 |
| 분류 | `i` — 데이터 가져오기 준비 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 26 |
| 나가는 FK / 들어오는 FK | 4 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

거래처·급여 개념·처리 건별 금액과 수량을 급여 변동 내역으로 가져오기 위한 데이터를 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `i_hr_movement_key` | `i_hr_movement_id` |
| UNIQUE | `i_hr_movement_uu_idx` | `i_hr_movement_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `i_hr_movement_id` | Payroll Movement Import | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 허용 | — | NULL::numeric | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 허용 | — | NULL::numeric | Organizational entity within tenant |
| 4 | `amount` | Amount | numeric | 허용 | — | — | Amount in a defined currency |
| 5 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | NULL::numeric | Identifies a Business Partner |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 허용 | — | NULL::numeric | User who created this records |
| 8 | `hr_concept_id` | Payroll Concept | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 9 | `hr_process_id` | Payroll Process | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 10 | `isactive` | Active | character(1) | 허용 | — | NULL::bpchar | The record is active in the system |
| 11 | `processed` | Processed | character(1) | 허용 | — | NULL::bpchar | The document has been processed |
| 12 | `qty` | Quantity | numeric | 허용 | — | — | Quantity |
| 13 | `servicedate` | Service date | timestamp without time zone | 허용 | — | — | Date service was provided |
| 14 | `textmsg` | Text Message | character varying(255) | 허용 | — | NULL::character varying | Text Message |
| 15 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 16 | `updatedby` | Updated By | numeric(10,0) | 허용 | — | NULL::numeric | User who updated this records |
| 17 | `validfrom` | Valid from | timestamp without time zone | 허용 | — | — | Valid from including this date (first day) |
| 18 | `i_isimported` | Imported | character varying(1) | 불가 | — | 'N'::character varying | Has this import been processed |
| 19 | `i_errormsg` | Import Error Message | character varying(2000) | 허용 | — | NULL::character varying | Messages generated from import process |
| 20 | `processing` | Process Now | character(1) | 허용 | — | NULL::bpchar | — |
| 21 | `bpartner_value` | Business Partner Key | character varying(40) | 허용 | — | NULL::character varying | The Key of the Business Partner |
| 22 | `conceptvalue` | Concept Value | character varying(40) | 허용 | — | NULL::character varying | Value of the Concept |
| 23 | `hr_movement_id` | Payroll Movement | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 24 | `processname` | Process Name | character varying(60) | 허용 | — | NULL::character varying | Name of the Process |
| 25 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 26 | `i_hr_movement_uu` | I_HR_Movement_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_bpartner"]
    n1["hr_concept"]
    n2["hr_movement"]
    n3["hr_process"]
    n4["i_hr_movement"]
    n4 -->|"c_bpartner_id → c_bpartner_id"| n0
    n4 -->|"hr_concept_id → hr_concept_id"| n1
    n4 -->|"hr_movement_id → hr_movement_id"| n2
    n4 -->|"hr_process_id → hr_process_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cbpartner_ihrmovement` <!-- FK_OUT: adempiere.i_hr_movement.cbpartner_ihrmovement --> | [`i_hr_movement`](i_hr_movement.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrconcept_ihrmovement` <!-- FK_OUT: adempiere.i_hr_movement.hrconcept_ihrmovement --> | [`i_hr_movement`](i_hr_movement.md) | `hr_concept_id` | [`hr_concept`](../hr/hr_concept.md) | `hr_concept_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrmovement_ihrmovement` <!-- FK_OUT: adempiere.i_hr_movement.hrmovement_ihrmovement --> | [`i_hr_movement`](i_hr_movement.md) | `hr_movement_id` | [`hr_movement`](../hr/hr_movement.md) | `hr_movement_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrprocess_ihrmovement` <!-- FK_OUT: adempiere.i_hr_movement.hrprocess_ihrmovement --> | [`i_hr_movement`](i_hr_movement.md) | `hr_process_id` | [`hr_process`](../hr/hr_process.md) | `hr_process_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
