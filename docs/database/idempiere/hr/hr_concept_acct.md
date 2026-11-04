# hr_concept_acct — 급여 항목 회계 계정

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.hr_concept_acct` |
| 한국어 논리명(문서용 해석) | 급여 항목 회계 계정 |
| 원본 논리명 | Payroll Concept Account |
| 원본 사전 ID | 53091 |
| 분류 | `hr` — 인사·급여 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 17 |
| 나가는 FK / 들어오는 FK | 7 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

급여 항목과 회계 스키마별 수익·비용 계정 및 거래처 그룹 등의 회계 연결을 관리한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `hr_concept_acct_key` | `hr_concept_acct_id` |
| UNIQUE | `hr_concept_acct_uu_idx` | `hr_concept_acct_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_bp_group_id` | Business Partner Group | numeric(10,0) | 허용 | — | — | Business Partner Group |
| 2 | `isbalancing` | Balancing | character(1) | 허용 | — | — | All transactions within an element value must balance (e.g. cost centers) |
| 3 | `user1_id` | User Element List 1 | numeric(10,0) | 허용 | — | — | User defined list element #1 |
| 4 | `user2_id` | User Element List 2 | numeric(10,0) | 허용 | — | — | User defined list element #2 |
| 5 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 6 | `hr_concept_acct_id` | Payroll Concept Account | numeric(10,0) | 불가 | 예 | — | — |
| 7 | `hr_concept_id` | Payroll Concept | numeric(10,0) | 불가 | — | — | — |
| 8 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 9 | `hr_revenue_acct` | Payroll Revenue Account | numeric(10,0) | 불가 | — | — | — |
| 10 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 11 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 12 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 13 | `hr_expense_acct` | Payroll Expense Account | numeric(10,0) | 불가 | — | — | — |
| 14 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 15 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 불가 | — | — | Rules for accounting |
| 16 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 17 | `hr_concept_acct_uu` | HR_Concept_Acct_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_acctschema"]
    n1["c_bp_group"]
    n2["c_elementvalue"]
    n3["c_validcombination"]
    n4["hr_concept"]
    n5["hr_concept_acct"]
    n5 -->|"c_acctschema_id → c_acctschema_id"| n0
    n5 -->|"c_bp_group_id → c_bp_group_id"| n1
    n5 -->|"hr_concept_id → hr_concept_id"| n4
    n5 -->|"hr_expense_acct → c_validcombination_id"| n3
    n5 -->|"hr_revenue_acct → c_validcombination_id"| n3
    n5 -->|"user2_id → c_validcombination_id"| n3
    n5 -->|"user1_id → c_elementvalue_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cacctschema_hrconceptacct` <!-- FK_OUT: adempiere.hr_concept_acct.cacctschema_hrconceptacct --> | [`hr_concept_acct`](hr_concept_acct.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpgroup_hrconceptacct` <!-- FK_OUT: adempiere.hr_concept_acct.cbpgroup_hrconceptacct --> | [`hr_concept_acct`](hr_concept_acct.md) | `c_bp_group_id` | [`c_bp_group`](../c/c_bp_group.md) | `c_bp_group_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrconcept_hrconceptacct` <!-- FK_OUT: adempiere.hr_concept_acct.hrconcept_hrconceptacct --> | [`hr_concept_acct`](hr_concept_acct.md) | `hr_concept_id` | [`hr_concept`](hr_concept.md) | `hr_concept_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrexpense_hrconceptacct` <!-- FK_OUT: adempiere.hr_concept_acct.hrexpense_hrconceptacct --> | [`hr_concept_acct`](hr_concept_acct.md) | `hr_expense_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrrevenue_hrconceptacct` <!-- FK_OUT: adempiere.hr_concept_acct.hrrevenue_hrconceptacct --> | [`hr_concept_acct`](hr_concept_acct.md) | `hr_revenue_acct` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `use_hrconceptacct` <!-- FK_OUT: adempiere.hr_concept_acct.use_hrconceptacct --> | [`hr_concept_acct`](hr_concept_acct.md) | `user2_id` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `user1_hrconceptacct` <!-- FK_OUT: adempiere.hr_concept_acct.user1_hrconceptacct --> | [`hr_concept_acct`](hr_concept_acct.md) | `user1_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
