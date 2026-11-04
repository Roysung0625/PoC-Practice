# c_job — 직위

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_job` |
| 한국어 논리명(문서용 해석) | 직위 |
| 원본 논리명 | Position |
| 원본 사전 ID | 789 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 4 |
| 물리 열 수 | 14 |
| 나가는 FK / 들어오는 FK | 1 / 4 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

직위의 명칭·분류와 직원용 여부를 정의하며 사용자 배치와 보수 설정에서 참조한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_job_pkey` | `c_job_id` |
| UNIQUE | `c_job_uu_idx` | `c_job_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_job_id` | Position | numeric(10,0) | 불가 | 예 | — | Job Position |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 12 | `c_jobcategory_id` | Position Category | numeric(10,0) | 불가 | — | — | Job Position Category |
| 13 | `isemployee` | Employee | character(1) | 불가 | — | 'N'::bpchar | Indicates if  this Business Partner is an employee |
| 14 | `c_job_uu` | C_Job_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_user"]
    n1["c_job"]
    n2["c_jobassignment"]
    n3["c_jobcategory"]
    n4["c_jobremuneration"]
    n5["m_operationresource"]
    n1 -->|"c_jobcategory_id → c_jobcategory_id"| n3
    n0 -->|"c_job_id → c_job_id"| n1
    n2 -->|"c_job_id → c_job_id"| n1
    n4 -->|"c_job_id → c_job_id"| n1
    n5 -->|"c_job_id → c_job_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cjobcategory_cjob` <!-- FK_OUT: adempiere.c_job.cjobcategory_cjob --> | [`c_job`](c_job.md) | `c_jobcategory_id` | [`c_jobcategory`](c_jobcategory.md) | `c_jobcategory_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cjob_aduser` <!-- FK_IN: adempiere.ad_user.cjob_aduser --> | [`ad_user`](../ad/ad_user.md) | `c_job_id` | [`c_job`](c_job.md) | `c_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cjob_cjobassignment` <!-- FK_IN: adempiere.c_jobassignment.cjob_cjobassignment --> | [`c_jobassignment`](c_jobassignment.md) | `c_job_id` | [`c_job`](c_job.md) | `c_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cjob_cjobremuneration` <!-- FK_IN: adempiere.c_jobremuneration.cjob_cjobremuneration --> | [`c_jobremuneration`](c_jobremuneration.md) | `c_job_id` | [`c_job`](c_job.md) | `c_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cjob_moperationresource` <!-- FK_IN: adempiere.m_operationresource.cjob_moperationresource --> | [`m_operationresource`](../m/m_operationresource.md) | `c_job_id` | [`c_job`](c_job.md) | `c_job_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
