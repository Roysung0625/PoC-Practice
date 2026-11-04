# hr_concept — 급여 계산 항목

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.hr_concept` |
| 한국어 논리명(문서용 해석) | 급여 계산 항목 |
| 원본 논리명 | Payroll Concept |
| 원본 사전 ID | 53090 |
| 분류 | `hr` — 인사·급여 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 30 |
| 나가는 FK / 들어오는 FK | 5 / 5 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

급여 항목의 유형·값 형식·분류·차대 부호 및 출력·지급 여부를 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `hr_concept_key` | `hr_concept_id` |
| UNIQUE | `hr_concept_uu_idx` | `hr_concept_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `accountsign` | Account Sign | character(1) | 허용 | — | — | Indicates the Natural Sign of the Account as a Debit or Credit |
| 2 | `isreadwrite` | Read Write | character(1) | 허용 | — | — | Field is read / write |
| 3 | `isreceipt` | Receipt | character(1) | 허용 | — | — | This is a sales transaction (receipt) |
| 4 | `ispaid` | Paid | character(1) | 허용 | — | — | The document is fully paid |
| 5 | `value` | Search Key | character varying(40) | 허용 | — | — | Search key for the record in the format required - must be unique |
| 6 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 7 | `hr_concept_category_id` | Payroll Concept Category | numeric(10,0) | 허용 | — | — | — |
| 8 | `hr_concept_id` | Payroll Concept | numeric(10,0) | 불가 | 예 | — | — |
| 9 | `hr_department_id` | Payroll Department | numeric(10,0) | 허용 | — | — | — |
| 10 | `hr_job_id` | Payroll Job | numeric(10,0) | 허용 | — | — | — |
| 11 | `hr_payroll_id` | Payroll | numeric(10,0) | 허용 | — | — | — |
| 12 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 13 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 14 | `isemployee` | Employee | character(1) | 허용 | — | — | Indicates if  this Business Partner is an employee |
| 15 | `isprinted` | Printed | character(1) | 허용 | — | — | Indicates if this document / line is printed |
| 16 | `isregistered` | Registered | character(1) | 허용 | — | — | The application is registered. |
| 17 | `type` | Type | character(1) | 불가 | — | — | Type of Validation (SQL, Java Script, Java Language) |
| 18 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 19 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 20 | `validfrom` | Valid from | timestamp without time zone | 허용 | — | — | Valid from including this date (first day) |
| 21 | `validto` | Valid to | timestamp without time zone | 허용 | — | — | Valid to including this date (last day) |
| 22 | `isdefault` | Default | character(1) | 허용 | — | — | Default value |
| 23 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 24 | `columntype` | Column Type | character(1) | 불가 | — | — | — |
| 25 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 26 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 27 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 28 | `ad_reference_id` | Reference | numeric(10,0) | 허용 | — | NULL::numeric | System Reference and Validation |
| 29 | `seqno` | Sequence | numeric(10,0) | 허용 | — | NULL::numeric | Method of ordering records; lowest number comes first |
| 30 | `hr_concept_uu` | HR_Concept_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 10개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_reference"]
    n1["hr_attribute"]
    n2["hr_concept"]
    n3["hr_concept_acct"]
    n4["hr_concept_category"]
    n5["hr_department"]
    n6["hr_job"]
    n7["hr_movement"]
    n8["hr_payroll"]
    n9["hr_payrollconcept"]
    n10["i_hr_movement"]
    n2 -->|"ad_reference_id → ad_reference_id"| n0
    n2 -->|"hr_concept_category_id → hr_concept_category_id"| n4
    n2 -->|"hr_department_id → hr_department_id"| n5
    n2 -->|"hr_job_id → hr_job_id"| n6
    n2 -->|"hr_payroll_id → hr_payroll_id"| n8
    n1 -->|"hr_concept_id → hr_concept_id"| n2
    n3 -->|"hr_concept_id → hr_concept_id"| n2
    n7 -->|"hr_concept_id → hr_concept_id"| n2
    n9 -->|"hr_concept_id → hr_concept_id"| n2
    n10 -->|"hr_concept_id → hr_concept_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adreference_hrconcept` <!-- FK_OUT: adempiere.hr_concept.adreference_hrconcept --> | [`hr_concept`](hr_concept.md) | `ad_reference_id` | [`ad_reference`](../ad/ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrconceptcategory_hrconcept` <!-- FK_OUT: adempiere.hr_concept.hrconceptcategory_hrconcept --> | [`hr_concept`](hr_concept.md) | `hr_concept_category_id` | [`hr_concept_category`](hr_concept_category.md) | `hr_concept_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrdepartment_hrconcept` <!-- FK_OUT: adempiere.hr_concept.hrdepartment_hrconcept --> | [`hr_concept`](hr_concept.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrjob_hrconcept` <!-- FK_OUT: adempiere.hr_concept.hrjob_hrconcept --> | [`hr_concept`](hr_concept.md) | `hr_job_id` | [`hr_job`](hr_job.md) | `hr_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrpayroll_hrconcept` <!-- FK_OUT: adempiere.hr_concept.hrpayroll_hrconcept --> | [`hr_concept`](hr_concept.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `hrconcept_hrattribute` <!-- FK_IN: adempiere.hr_attribute.hrconcept_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_concept_id` | [`hr_concept`](hr_concept.md) | `hr_concept_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrconcept_hrconceptacct` <!-- FK_IN: adempiere.hr_concept_acct.hrconcept_hrconceptacct --> | [`hr_concept_acct`](hr_concept_acct.md) | `hr_concept_id` | [`hr_concept`](hr_concept.md) | `hr_concept_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrconcept_hrmovement` <!-- FK_IN: adempiere.hr_movement.hrconcept_hrmovement --> | [`hr_movement`](hr_movement.md) | `hr_concept_id` | [`hr_concept`](hr_concept.md) | `hr_concept_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrconcept_hrpayrollconcept` <!-- FK_IN: adempiere.hr_payrollconcept.hrconcept_hrpayrollconcept --> | [`hr_payrollconcept`](hr_payrollconcept.md) | `hr_concept_id` | [`hr_concept`](hr_concept.md) | `hr_concept_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrconcept_ihrmovement` <!-- FK_IN: adempiere.i_hr_movement.hrconcept_ihrmovement --> | [`i_hr_movement`](../i/i_hr_movement.md) | `hr_concept_id` | [`hr_concept`](hr_concept.md) | `hr_concept_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
