# hr_employee — 급여 직원

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.hr_employee` |
| 한국어 논리명(문서용 해석) | 급여 직원 |
| 원본 논리명 | Payroll Employee |
| 원본 사전 ID | 53086 |
| 분류 | `hr` — 인사·급여 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 22 |
| 나가는 FK / 들어오는 FK | 5 / 3 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

급여 대상 직원을 거래처와 연결하고 부서·직무·급여 체계 및 입퇴사 날짜를 관리한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `hr_employee_key` | `hr_employee_id` |
| UNIQUE | `hr_employee_uu_idx` | `hr_employee_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `code` | Validation code | character varying(1) | 허용 | — | — | Validation Code |
| 2 | `name` | Name | character varying(30) | 허용 | — | — | Alphanumeric identifier of the entity |
| 3 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 4 | `c_bpartner_id` | Business Partner | numeric(10,0) | 불가 | — | — | Identifies a Business Partner |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `enddate` | End Date | timestamp without time zone | 허용 | — | — | Last effective date (inclusive) |
| 8 | `hr_department_id` | Payroll Department | numeric(10,0) | 불가 | — | — | — |
| 9 | `hr_employee_id` | Payroll Employee | numeric(10,0) | 불가 | 예 | — | — |
| 10 | `hr_job_id` | Payroll Job | numeric(10,0) | 불가 | — | — | — |
| 11 | `hr_payroll_id` | Payroll | numeric(10,0) | 허용 | — | — | — |
| 12 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 13 | `name2` | Name 2 | character varying(30) | 허용 | — | — | Additional Name |
| 14 | `nationalcode` | National Code | character varying(60) | 허용 | — | — | — |
| 15 | `sscode` | Social Security Code | character varying(60) | 허용 | — | — | — |
| 16 | `startdate` | Start Date | timestamp without time zone | 불가 | — | — | First effective day (inclusive) |
| 17 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 18 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 19 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 20 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 21 | `imageurl` | Image URL | character varying(120) | 허용 | — | NULL::character varying | URL of  image |
| 22 | `hr_employee_uu` | HR_Employee_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_activity"]
    n1["c_bpartner"]
    n2["hr_attribute"]
    n3["hr_department"]
    n4["hr_employee"]
    n5["hr_job"]
    n6["hr_list"]
    n7["hr_payroll"]
    n8["hr_process"]
    n4 -->|"c_activity_id → c_activity_id"| n0
    n4 -->|"c_bpartner_id → c_bpartner_id"| n1
    n4 -->|"hr_department_id → hr_department_id"| n3
    n4 -->|"hr_job_id → hr_job_id"| n5
    n4 -->|"hr_payroll_id → hr_payroll_id"| n7
    n2 -->|"hr_employee_id → hr_employee_id"| n4
    n6 -->|"hr_employee_id → hr_employee_id"| n4
    n8 -->|"hr_employee_id → hr_employee_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cactivity_hremployee` <!-- FK_OUT: adempiere.hr_employee.cactivity_hremployee --> | [`hr_employee`](hr_employee.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_hremployee` <!-- FK_OUT: adempiere.hr_employee.cbpartner_hremployee --> | [`hr_employee`](hr_employee.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrdepartment_hremployee` <!-- FK_OUT: adempiere.hr_employee.hrdepartment_hremployee --> | [`hr_employee`](hr_employee.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrjob_hremployee` <!-- FK_OUT: adempiere.hr_employee.hrjob_hremployee --> | [`hr_employee`](hr_employee.md) | `hr_job_id` | [`hr_job`](hr_job.md) | `hr_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrpayroll_hremployee` <!-- FK_OUT: adempiere.hr_employee.hrpayroll_hremployee --> | [`hr_employee`](hr_employee.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `hremployee_hrattribute` <!-- FK_IN: adempiere.hr_attribute.hremployee_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_employee_id` | [`hr_employee`](hr_employee.md) | `hr_employee_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hremployee_hrlist` <!-- FK_IN: adempiere.hr_list.hremployee_hrlist --> | [`hr_list`](hr_list.md) | `hr_employee_id` | [`hr_employee`](hr_employee.md) | `hr_employee_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hremployee_hrprocess` <!-- FK_IN: adempiere.hr_process.hremployee_hrprocess --> | [`hr_process`](hr_process.md) | `hr_employee_id` | [`hr_employee`](hr_employee.md) | `hr_employee_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
