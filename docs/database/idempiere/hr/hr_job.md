# hr_job — 급여 직무

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.hr_job` |
| 한국어 논리명(문서용 해석) | 급여 직무 |
| 원본 논리명 | Payroll Job |
| 원본 사전 ID | 53089 |
| 분류 | `hr` — 인사·급여 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 17 |
| 나가는 FK / 들어오는 FK | 3 / 6 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

급여 직무와 소속 부서·상위 구조 관련 값·감독 사용자 정보를 관리한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `hr_job_key` | `hr_job_id` |
| UNIQUE | `hr_job_uu_idx` | `hr_job_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `hr_job_value`: `CREATE UNIQUE INDEX hr_job_value ON adempiere.hr_job USING btree (ad_client_id, value)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 4 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 5 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 6 | `hr_department_id` | Payroll Department | numeric(10,0) | 허용 | — | — | — |
| 7 | `hr_job_id` | Payroll Job | numeric(10,0) | 불가 | 예 | — | — |
| 8 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 9 | `isparent` | Parent link column | character(1) | 허용 | — | — | This column is a link to the parent table (e.g. header from lines) - incl. Association key columns |
| 10 | `jobcant` | Job Qty | numeric(10,0) | 허용 | — | — | — |
| 11 | `next_job_id` | Next Job | numeric(10,0) | 허용 | — | — | — |
| 12 | `supervisor_id` | Supervisor | numeric(10,0) | 허용 | — | — | Supervisor for this user/organization - used for escalation and approval |
| 13 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 14 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 15 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 16 | `value` | Search Key | character varying(40) | 허용 | — | — | Search key for the record in the format required - must be unique |
| 17 | `hr_job_uu` | HR_Job_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_user"]
    n1["hr_attribute"]
    n2["hr_concept"]
    n3["hr_department"]
    n4["hr_employee"]
    n5["hr_job"]
    n6["hr_movement"]
    n7["hr_process"]
    n5 -->|"hr_department_id → hr_department_id"| n3
    n5 -->|"next_job_id → hr_job_id"| n5
    n5 -->|"supervisor_id → ad_user_id"| n0
    n1 -->|"hr_job_id → hr_job_id"| n5
    n2 -->|"hr_job_id → hr_job_id"| n5
    n4 -->|"hr_job_id → hr_job_id"| n5
    n6 -->|"hr_job_id → hr_job_id"| n5
    n7 -->|"hr_job_id → hr_job_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `hrdepartment_hrjob` <!-- FK_OUT: adempiere.hr_job.hrdepartment_hrjob --> | [`hr_job`](hr_job.md) | `hr_department_id` | [`hr_department`](hr_department.md) | `hr_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `nextjob_hrjob` <!-- FK_OUT: adempiere.hr_job.nextjob_hrjob --> | [`hr_job`](hr_job.md) | `next_job_id` | [`hr_job`](hr_job.md) | `hr_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `supervisor_hrjob` <!-- FK_OUT: adempiere.hr_job.supervisor_hrjob --> | [`hr_job`](hr_job.md) | `supervisor_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `hrjob_hrattribute` <!-- FK_IN: adempiere.hr_attribute.hrjob_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_job_id` | [`hr_job`](hr_job.md) | `hr_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrjob_hrconcept` <!-- FK_IN: adempiere.hr_concept.hrjob_hrconcept --> | [`hr_concept`](hr_concept.md) | `hr_job_id` | [`hr_job`](hr_job.md) | `hr_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrjob_hremployee` <!-- FK_IN: adempiere.hr_employee.hrjob_hremployee --> | [`hr_employee`](hr_employee.md) | `hr_job_id` | [`hr_job`](hr_job.md) | `hr_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `nextjob_hrjob` <!-- FK_IN: adempiere.hr_job.nextjob_hrjob --> | [`hr_job`](hr_job.md) | `next_job_id` | [`hr_job`](hr_job.md) | `hr_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrjob_hrmovement` <!-- FK_IN: adempiere.hr_movement.hrjob_hrmovement --> | [`hr_movement`](hr_movement.md) | `hr_job_id` | [`hr_job`](hr_job.md) | `hr_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrjob_hrprocess` <!-- FK_IN: adempiere.hr_process.hrjob_hrprocess --> | [`hr_process`](hr_process.md) | `hr_job_id` | [`hr_job`](hr_job.md) | `hr_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
