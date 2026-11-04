# ad_userdef_proc_parameter — 사용자 정의 프로세스 인수

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_userdef_proc_parameter` |
| 한국어 논리명(문서용 해석) | 사용자 정의 프로세스 인수 |
| 원본 논리명 | AD_UserDef_Proc_Parameter_ID |
| 원본 사전 ID | 200233 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 32 |
| 나가는 FK / 들어오는 FK | 6 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

사용자 정의 프로세스에서 입력 매개변수의 표시·기본값·필수 여부·검증 및 순서를 재설정한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Primary Key : User defined Process Parameter
- 원본 도움말: User defined Process Parameter
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_userdef_proc_parameter_key` | `ad_userdef_proc_parameter_id` |
| UNIQUE | `ad_userdef_proc_parameteruuidx` | `ad_userdef_proc_parameter_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_userdef_procparam_unique`: `CREATE UNIQUE INDEX ad_userdef_procparam_unique ON adempiere.ad_userdef_proc_parameter USING btree (ad_userdef_proc_id, ad_process_para_id)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_userdef_proc_parameter_id` | AD_UserDef_Proc_Parameter_ID | numeric(10,0) | 불가 | 예 | — | Primary Key : User defined Process Parameter |
| 2 | `ad_userdef_proc_parameter_uu` | AD_UserDef_Proc_Parameter_UU | uuid | 허용 | — | — | — |
| 3 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 4 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 5 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | — | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 8 | `updated` | Updated | timestamp without time zone | 불가 | — | — | Date this record was updated |
| 9 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 10 | `ad_userdef_proc_id` | User defined Process | numeric(10,0) | 불가 | — | — | Primary Key : User defined Process |
| 11 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 12 | `help` | Comment/Help | character varying(2000) | 허용 | — | NULL::character varying | Comment or Hint |
| 13 | `isdisplayed` | Displayed | character(1) | 허용 | — | — | Determines, if this field is displayed |
| 14 | `displaylogic` | Display Logic | character varying(2000) | 허용 | — | NULL::character varying | If the Field is displayed, the result determines if the field is actually displayed |
| 15 | `defaultvalue` | Default Logic | character varying(2000) | 허용 | — | NULL::character varying | Default value hierarchy, separated by ; |
| 16 | `ad_process_para_id` | Process Parameter | numeric(10,0) | 불가 | — | — | — |
| 17 | `name` | Name | character varying(60) | 허용 | — | NULL::character varying | Alphanumeric identifier of the entity |
| 18 | `readonlylogic` | Read Only Logic | character varying(2000) | 허용 | — | NULL::character varying | Logic to determine if field is read only (applies only when field is read-write) |
| 19 | `mandatorylogic` | Mandatory Logic | character varying(2000) | 허용 | — | NULL::character varying | — |
| 20 | `ad_reference_id` | Reference | numeric(10,0) | 허용 | — | NULL::numeric | System Reference and Validation |
| 21 | `ad_reference_value_id` | Reference Key | numeric(10,0) | 허용 | — | NULL::numeric | Required to specify, if data type is Table or List |
| 22 | `ad_val_rule_id` | Dynamic Validation | numeric(10,0) | 허용 | — | NULL::numeric | Dynamic Validation Rule |
| 23 | `defaultvalue2` | Default Logic 2 | character varying(2000) | 허용 | — | NULL::character varying | Default value hierarchy, separated by ; |
| 24 | `placeholder` | Placeholder | character varying(255) | 허용 | — | NULL::character varying | — |
| 25 | `placeholder2` | Placeholder2 | character varying(255) | 허용 | — | NULL::character varying | — |
| 26 | `isrange` | Range | character(1) | 허용 | — | NULL::bpchar | The parameter is a range of values |
| 27 | `ismandatory` | Mandatory | character(1) | 허용 | — | NULL::bpchar | Data entry is required in this column |
| 28 | `valuemin` | Min. Value | character varying(20) | 허용 | — | NULL::character varying | Minimum Value for a field |
| 29 | `valuemax` | Max. Value | character varying(20) | 허용 | — | NULL::character varying | Maximum Value for a field |
| 30 | `seqno` | Sequence | numeric(10,0) | 허용 | — | NULL::numeric | Method of ordering records; lowest number comes first |
| 31 | `vformat` | Value Format | character varying(40) | 허용 | — | NULL::character varying | Format of the value; Can contain fixed format elements, Variables: "_lLoOaAcCa09", or ~regex |
| 32 | `ad_fieldgroup_id` | Field Group | numeric(10,0) | 허용 | — | NULL::numeric | Logical grouping of fields |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 6개 중 6개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_fieldgroup"]
    n1["ad_process_para"]
    n2["ad_reference"]
    n3["ad_userdef_proc"]
    n4["ad_userdef_proc_parameter"]
    n5["ad_val_rule"]
    n4 -->|"ad_fieldgroup_id → ad_fieldgroup_id"| n0
    n4 -->|"ad_process_para_id → ad_process_para_id"| n1
    n4 -->|"ad_reference_id → ad_reference_id"| n2
    n4 -->|"ad_reference_value_id → ad_reference_id"| n2
    n4 -->|"ad_userdef_proc_id → ad_userdef_proc_id"| n3
    n4 -->|"ad_val_rule_id → ad_val_rule_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adfieldgroup_aduserdefprocpara` <!-- FK_OUT: adempiere.ad_userdef_proc_parameter.adfieldgroup_aduserdefprocpara --> | [`ad_userdef_proc_parameter`](ad_userdef_proc_parameter.md) | `ad_fieldgroup_id` | [`ad_fieldgroup`](ad_fieldgroup.md) | `ad_fieldgroup_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocesspara_aduserdefprocpar` <!-- FK_OUT: adempiere.ad_userdef_proc_parameter.adprocesspara_aduserdefprocpar --> | [`ad_userdef_proc_parameter`](ad_userdef_proc_parameter.md) | `ad_process_para_id` | [`ad_process_para`](ad_process_para.md) | `ad_process_para_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreference_aduserdefprocparam` <!-- FK_OUT: adempiere.ad_userdef_proc_parameter.adreference_aduserdefprocparam --> | [`ad_userdef_proc_parameter`](ad_userdef_proc_parameter.md) | `ad_reference_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreferencevalue_aduserdefproc` <!-- FK_OUT: adempiere.ad_userdef_proc_parameter.adreferencevalue_aduserdefproc --> | [`ad_userdef_proc_parameter`](ad_userdef_proc_parameter.md) | `ad_reference_value_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduserdefproc_aduserdefprocpar` <!-- FK_OUT: adempiere.ad_userdef_proc_parameter.aduserdefproc_aduserdefprocpar --> | [`ad_userdef_proc_parameter`](ad_userdef_proc_parameter.md) | `ad_userdef_proc_id` | [`ad_userdef_proc`](ad_userdef_proc.md) | `ad_userdef_proc_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_aduserdefprocparamet` <!-- FK_OUT: adempiere.ad_userdef_proc_parameter.advalrule_aduserdefprocparamet --> | [`ad_userdef_proc_parameter`](ad_userdef_proc_parameter.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
