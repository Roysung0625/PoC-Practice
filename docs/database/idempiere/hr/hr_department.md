# hr_department — 급여 부서

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.hr_department` |
| 한국어 논리명(문서용 해석) | 급여 부서 |
| 원본 논리명 | Payroll Department |
| 원본 사전 ID | 53088 |
| 분류 | `hr` — 인사·급여 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 13 |
| 나가는 FK / 들어오는 FK | 1 / 7 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

급여 부서의 코드·이름과 업무 활동 연결을 관리한다. 공통 부서 기준 c_department와 구분한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `hr_department_key` | `hr_department_id` |
| UNIQUE | `hr_department_uu_idx` | `hr_department_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `hr_department_value`: `CREATE UNIQUE INDEX hr_department_value ON adempiere.hr_department USING btree (ad_client_id, value)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 4 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 5 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 6 | `hr_department_id` | Payroll Department | numeric(10,0) | 불가 | 예 | — | — |
| 7 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 8 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 9 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 10 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 11 | `value` | Search Key | character varying(40) | 허용 | — | — | Search key for the record in the format required - must be unique |
| 12 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 13 | `hr_department_uu` | HR_Department_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_activity"]
    n1["hr_attribute"]
    n2["hr_concept"]
    n3["hr_department"]
    n4["hr_employee"]
    n5["hr_job"]
    n6["hr_list"]
    n7["hr_movement"]
    n8["hr_process"]
    n3 -->|"c_activity_id → c_activity_id"| n0
    n1 -->|"hr_department_id → hr_department_id"| n3
    n2 -->|"hr_department_id → hr_department_id"| n3
    n4 -->|"hr_department_id → hr_department_id"| n3
    n5 -->|"hr_department_id → hr_department_id"| n3
    n6 -->|"hr_department_id → hr_department_id"| n3
    n7 -->|"hr_department_id → hr_department_id"| n3
    n8 -->|"hr_department_id → hr_department_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `activity_hrdepartment` <!-- FK_OUT: adempiere.hr_department.activity_hrdepartment --> | [`hr_department`](hr_department.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `hrdepartment_hrattribute` <!-- FK_IN: adempiere.hr_attribute.hrdepartment_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrdepartment_hrconcept` <!-- FK_IN: adempiere.hr_concept.hrdepartment_hrconcept --> | [`hr_concept`](hr_concept.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrdepartment_hremployee` <!-- FK_IN: adempiere.hr_employee.hrdepartment_hremployee --> | [`hr_employee`](hr_employee.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrdepartment_hrjob` <!-- FK_IN: adempiere.hr_job.hrdepartment_hrjob --> | [`hr_job`](hr_job.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrdepartment_hrlist` <!-- FK_IN: adempiere.hr_list.hrdepartment_hrlist --> | [`hr_list`](hr_list.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrdepartment_hrmovement` <!-- FK_IN: adempiere.hr_movement.hrdepartment_hrmovement --> | [`hr_movement`](hr_movement.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrdepartment_hrprocess` <!-- FK_IN: adempiere.hr_process.hrdepartment_hrprocess --> | [`hr_process`](hr_process.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
