# hr_payroll — 급여 체계

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.hr_payroll` |
| 한국어 논리명(문서용 해석) | 급여 체계 |
| 원본 논리명 | Payroll |
| 원본 사전 ID | 53093 |
| 분류 | `hr` — 인사·급여 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 18 |
| 나가는 FK / 들어오는 FK | 3 / 8 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

급여 계산·지급 기준 체계를 정의하고 계약·지급 방식·인쇄 서식과 부대 항목을 연결한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `hr_payroll_key` | `hr_payroll_id` |
| UNIQUE | `hr_payroll_uu_idx` | `hr_payroll_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 2 | `value` | Search Key | character varying(40) | 허용 | — | — | Search key for the record in the format required - must be unique |
| 3 | `ad_printformat_id` | Print Format | numeric(10,0) | 허용 | — | — | Data Print Format |
| 4 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | — | Additional document charges |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 8 | `hr_contract_id` | Payroll Contract | numeric(10,0) | 불가 | — | — | — |
| 9 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 10 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 11 | `paymentrule` | Payment Rule | character(1) | 불가 | — | — | How you pay the invoice |
| 12 | `processed` | Processed | character(1) | 허용 | — | — | The document has been processed |
| 13 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 14 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 15 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 16 | `hr_payroll_id` | Payroll | numeric(10,0) | 불가 | 예 | — | — |
| 17 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 18 | `hr_payroll_uu` | HR_Payroll_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 11개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_printformat"]
    n1["c_charge"]
    n2["hr_attribute"]
    n3["hr_concept"]
    n4["hr_contract"]
    n5["hr_employee"]
    n6["hr_list"]
    n7["hr_payroll"]
    n8["hr_payrollconcept"]
    n9["hr_period"]
    n10["hr_process"]
    n7 -->|"ad_printformat_id → ad_printformat_id"| n0
    n7 -->|"c_charge_id → c_charge_id"| n1
    n7 -->|"hr_contract_id → hr_contract_id"| n4
    n2 -->|"hr_payroll_id → hr_payroll_id"| n7
    n3 -->|"hr_payroll_id → hr_payroll_id"| n7
    n5 -->|"hr_payroll_id → hr_payroll_id"| n7
    n6 -->|"hr_payroll_id → hr_payroll_id"| n7
    n8 -->|"hr_payroll_id → hr_payroll_id"| n7
    n9 -->|"hr_payroll_id → hr_payroll_id"| n7
    n10 -->|"hr_payroll_id → hr_payroll_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adprintformat_hrpayroll` <!-- FK_OUT: adempiere.hr_payroll.adprintformat_hrpayroll --> | [`hr_payroll`](hr_payroll.md) | `ad_printformat_id` | [`ad_printformat`](../ad/ad_printformat.md) | `ad_printformat_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccharge_hrpayroll` <!-- FK_OUT: adempiere.hr_payroll.ccharge_hrpayroll --> | [`hr_payroll`](hr_payroll.md) | `c_charge_id` | [`c_charge`](../c/c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrcontract_hrpayroll` <!-- FK_OUT: adempiere.hr_payroll.hrcontract_hrpayroll --> | [`hr_payroll`](hr_payroll.md) | `hr_contract_id` | [`hr_contract`](hr_contract.md) | `hr_contract_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `hrpayroll_hrattribute` <!-- FK_IN: adempiere.hr_attribute.hrpayroll_hrattribute --> | [`hr_attribute`](hr_attribute.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrpayroll_hrconcept` <!-- FK_IN: adempiere.hr_concept.hrpayroll_hrconcept --> | [`hr_concept`](hr_concept.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrpayroll_hremployee` <!-- FK_IN: adempiere.hr_employee.hrpayroll_hremployee --> | [`hr_employee`](hr_employee.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrpayroll_hrlist` <!-- FK_IN: adempiere.hr_list.hrpayroll_hrlist --> | [`hr_list`](hr_list.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrpayroll_hrpayrollconcept` <!-- FK_IN: adempiere.hr_payrollconcept.hrpayroll_hrpayrollconcept --> | [`hr_payrollconcept`](hr_payrollconcept.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrpayroll_hrperiod` <!-- FK_IN: adempiere.hr_period.hrpayroll_hrperiod --> | [`hr_period`](hr_period.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrpayroll_hrprocess` <!-- FK_IN: adempiere.hr_process.hrpayroll_hrprocess --> | [`hr_process`](hr_process.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `hrpayroll_hryear` <!-- FK_IN: adempiere.hr_year.hrpayroll_hryear --> | [`hr_year`](hr_year.md) | `hr_payroll_id` | [`hr_payroll`](hr_payroll.md) | `hr_payroll_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
