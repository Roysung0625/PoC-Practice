# hr_attribute — 직원 급여 속성

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.hr_attribute` |
| 한국어 논리명(문서용 해석) | 직원 급여 속성 |
| 원본 논리명 | Payroll Employee Attribute |
| 원본 사전 ID | 53087 |
| 분류 | `hr` — 인사·급여 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 28 |
| 나가는 FK / 들어오는 FK | 8 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

직원·급여 항목별 적용 값과 계산 규칙·유효 기간을 관리하며 금액·수량·문자·서비스 날짜 등의 형식을 담는다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `hr_attribute_key` | `hr_attribute_id` |
| UNIQUE | `hr_attribute_uu_idx` | `hr_attribute_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_rule_id` | Rule | numeric(10,0) | 허용 | — | — | — |
| 4 | `amount` | Amount | numeric | 허용 | — | — | Amount in a defined currency |
| 5 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 6 | `columntype` | Column Type | character(1) | 허용 | — | — | — |
| 7 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 8 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 9 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 10 | `hr_attribute_acct` | Payroll Attribute Account | numeric(10,0) | 허용 | — | — | — |
| 11 | `hr_attribute_id` | Payroll Employee Attribute | numeric(10,0) | 불가 | 예 | — | — |
| 12 | `hr_concept_id` | Payroll Concept | numeric(10,0) | 불가 | — | — | — |
| 13 | `hr_department_id` | Payroll Department | numeric(10,0) | 허용 | — | — | — |
| 14 | `hr_employee_id` | Payroll Employee | numeric(10,0) | 허용 | — | — | — |
| 15 | `hr_job_id` | Payroll Job | numeric(10,0) | 허용 | — | — | — |
| 16 | `hr_payroll_id` | Payroll | numeric(10,0) | 허용 | — | — | — |
| 17 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 18 | `isprinted` | Printed | character(1) | 허용 | — | — | Indicates if this document / line is printed |
| 19 | `maxvalue` | Max Value | numeric(10,0) | 허용 | — | — | — |
| 20 | `minvalue` | Min Value | numeric(10,0) | 허용 | — | — | — |
| 21 | `qty` | Quantity | numeric | 허용 | — | — | Quantity |
| 22 | `servicedate` | Service date | timestamp without time zone | 허용 | — | — | Date service was provided |
| 23 | `textmsg` | Text Message | character varying(255) | 허용 | — | — | Text Message |
| 24 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 25 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 26 | `validfrom` | Valid from | timestamp without time zone | 불가 | — | — | Valid from including this date (first day) |
| 27 | `validto` | Valid to | timestamp without time zone | 허용 | — | — | Valid to including this date (last day) |
| 28 | `hr_attribute_uu` | HR_Attribute_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_rule"]
    n1["c_bpartner"]
    n2["c_validcombination"]
    n3["hr_attribute"]
    n4["hr_concept"]
    n5["hr_department"]
    n6["hr_employee"]
    n7["hr_job"]
    n8["hr_payroll"]
    n3 -->|"ad_rule_id → ad_rule_id"| n0
    n3 -->|"c_bpartner_id → c_bpartner_id"| n1
    n3 -->|"hr_attribute_acct → c_validcombination_id"| n2
    n3 -->|"hr_concept_id → hr_concept_id"| n4
    n3 -->|"hr_department_id → hr_department_id"| n5
    n3 -->|"hr_employee_id → hr_employee_id"| n6
    n3 -->|"hr_job_id → hr_job_id"| n7
    n3 -->|"hr_payroll_id → hr_payroll_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adrule_hrattribute` <!-- FK_OUT: adempiere.hr_attribute.adrule_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `ad_rule_id` | [`ad_rule`](../ad/ad_rule.md) | `ad_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_hrattribute` <!-- FK_OUT: adempiere.hr_attribute.cbpartner_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrattribute_hrattribute` <!-- FK_OUT: adempiere.hr_attribute.hrattribute_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_attribute_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrconcept_hrattribute` <!-- FK_OUT: adempiere.hr_attribute.hrconcept_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_concept_id` | [`hr_concept`](hr_concept.md) | `hr_concept_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrdepartment_hrattribute` <!-- FK_OUT: adempiere.hr_attribute.hrdepartment_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hremployee_hrattribute` <!-- FK_OUT: adempiere.hr_attribute.hremployee_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_employee_id` | [`hr_employee`](hr_employee.md) | `hr_employee_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrjob_hrattribute` <!-- FK_OUT: adempiere.hr_attribute.hrjob_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_job_id` | [`hr_job`](hr_job.md) | `hr_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrpayroll_hrattribute` <!-- FK_OUT: adempiere.hr_attribute.hrpayroll_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
