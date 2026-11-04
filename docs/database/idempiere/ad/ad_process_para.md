# ad_process_para — 프로세스 입력 매개변수

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_process_para` |
| 한국어 논리명(문서용 해석) | 프로세스 입력 매개변수 |
| 원본 논리명 | Process Parameter |
| 원본 사전 ID | 285 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 1,223 |
| 물리 열 수 | 40 |
| 나가는 FK / 들어오는 FK | 7 / 8 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

프로세스 입력 항목의 유형·범위·기본값·검증 및 표시 조건을 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_process_para_pkey` | `ad_process_para_id` |
| UNIQUE | `ad_process_para_uu_idx` | `ad_process_para_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_procpara_procseqno`: `CREATE UNIQUE INDEX ad_procpara_procseqno ON adempiere.ad_process_para USING btree (ad_process_id, seqno)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_process_para_id` | Process Parameter | numeric(10,0) | 불가 | 예 | — | — |
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
| 12 | `ad_process_id` | Process | numeric(10,0) | 불가 | — | — | Process or Report |
| 13 | `seqno` | Sequence | numeric(10,0) | 불가 | — | — | Method of ordering records; lowest number comes first |
| 14 | `ad_reference_id` | Reference | numeric(10,0) | 불가 | — | — | System Reference and Validation |
| 15 | `ad_reference_value_id` | Reference Key | numeric(10,0) | 허용 | — | — | Required to specify, if data type is Table or List |
| 16 | `ad_val_rule_id` | Dynamic Validation | numeric(10,0) | 허용 | — | — | Dynamic Validation Rule |
| 17 | `columnname` | DB Column Name | character varying(63) | 불가 | — | — | Name of the column in the database |
| 18 | `iscentrallymaintained` | Centrally maintained | character(1) | 불가 | — | 'Y'::bpchar | Information maintained in System Element table |
| 19 | `fieldlength` | Length | numeric(10,0) | 불가 | — | — | Length of the column in the database |
| 20 | `ismandatory` | Mandatory | character(1) | 불가 | — | 'N'::bpchar | Data entry is required in this column |
| 21 | `isrange` | Range | character(1) | 불가 | — | 'N'::bpchar | The parameter is a range of values |
| 22 | `defaultvalue` | Default Logic | character varying(2000) | 허용 | — | — | Default value hierarchy, separated by ; |
| 23 | `defaultvalue2` | Default Logic 2 | character varying(2000) | 허용 | — | — | Default value hierarchy, separated by ; |
| 24 | `vformat` | Value Format | character varying(255) | 허용 | — | — | Format of the value; Can contain fixed format elements, Variables: "_lLoOaAcCa09", or ~regex |
| 25 | `valuemin` | Min. Value | character varying(20) | 허용 | — | — | Minimum Value for a field |
| 26 | `valuemax` | Max. Value | character varying(20) | 허용 | — | — | Maximum Value for a field |
| 27 | `ad_element_id` | System Element | numeric(10,0) | 허용 | — | — | System Element enables the central maintenance of column description and help. |
| 28 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 29 | `readonlylogic` | Read Only Logic | character varying(2000) | 허용 | — | — | Logic to determine if field is read only (applies only when field is read-write) |
| 30 | `displaylogic` | Display Logic | character varying(2000) | 허용 | — | — | If the Field is displayed, the result determines if the field is actually displayed |
| 31 | `ad_process_para_uu` | AD_Process_Para_UU | uuid | 허용 | — | — | — |
| 32 | `isencrypted` | Encrypted | character(1) | 불가 | — | 'N'::bpchar | Display or Storage is encrypted |
| 33 | `mandatorylogic` | Mandatory Logic | character varying(2000) | 허용 | — | NULL::character varying | — |
| 34 | `placeholder` | Placeholder | character varying(255) | 허용 | — | NULL::character varying | — |
| 35 | `placeholder2` | Placeholder2 | character varying(255) | 허용 | — | NULL::character varying | — |
| 36 | `isautocomplete` | Auto complete | character(1) | 불가 | — | 'N'::bpchar | Automatic completion for text fields |
| 37 | `ad_fieldgroup_id` | Field Group | numeric(10,0) | 허용 | — | NULL::numeric | Logical grouping of fields |
| 38 | `query` | Query | character varying(2000) | 허용 | — | NULL::character varying | SQL |
| 39 | `daterangeoption` | Date Range Option | character(1) | 불가 | — | 'D'::bpchar | Options, how the date editor will be displayed. |
| 40 | `isshownegatebutton` | Show Negate Button | character(1) | 불가 | — | 'N'::bpchar | Show Negate Button for Chosen Multiple editors |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 15개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_element"]
    n1["ad_entitytype"]
    n2["ad_fieldgroup"]
    n3["ad_process"]
    n4["ad_process_drillrule"]
    n5["ad_process_drillrule_para"]
    n6["ad_process_para"]
    n7["ad_process_para_trl"]
    n8["ad_reference"]
    n9["ad_val_rule"]
    n6 -->|"ad_element_id → ad_element_id"| n0
    n6 -->|"ad_fieldgroup_id → ad_fieldgroup_id"| n2
    n6 -->|"ad_process_id → ad_process_id"| n3
    n6 -->|"ad_reference_id → ad_reference_id"| n8
    n6 -->|"ad_reference_value_id → ad_reference_id"| n8
    n6 -->|"ad_val_rule_id → ad_val_rule_id"| n9
    n6 -->|"entitytype → entitytype"| n1
    n4 -->|"ad_process_para_id → ad_process_para_id"| n6
    n5 -->|"ad_process_para_id → ad_process_para_id"| n6
    n7 -->|"ad_process_para_id → ad_process_para_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adelement_adprocesspara` <!-- FK_OUT: adempiere.ad_process_para.adelement_adprocesspara --> | [`ad_process_para`](ad_process_para.md) | `ad_element_id` | [`ad_element`](ad_element.md) | `ad_element_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfieldgroup_adprocesspara` <!-- FK_OUT: adempiere.ad_process_para.adfieldgroup_adprocesspara --> | [`ad_process_para`](ad_process_para.md) | `ad_fieldgroup_id` | [`ad_fieldgroup`](ad_fieldgroup.md) | `ad_fieldgroup_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocess_adprocesspara` <!-- FK_OUT: adempiere.ad_process_para.adprocess_adprocesspara --> | [`ad_process_para`](ad_process_para.md) | `ad_process_id` | [`ad_process`](ad_process.md) | `ad_process_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreference_adprocesspara` <!-- FK_OUT: adempiere.ad_process_para.adreference_adprocesspara --> | [`ad_process_para`](ad_process_para.md) | `ad_reference_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreferencevalue_adprocpara` <!-- FK_OUT: adempiere.ad_process_para.adreferencevalue_adprocpara --> | [`ad_process_para`](ad_process_para.md) | `ad_reference_value_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_ad_processpara` <!-- FK_OUT: adempiere.ad_process_para.advalrule_ad_processpara --> | [`ad_process_para`](ad_process_para.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adprocesspara` <!-- FK_OUT: adempiere.ad_process_para.entityt_adprocesspara --> | [`ad_process_para`](ad_process_para.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adprocesspara_adprocessdrillru` <!-- FK_IN: adempiere.ad_process_drillrule.adprocesspara_adprocessdrillru --> | [`ad_process_drillrule`](ad_process_drillrule.md) | `ad_process_para_id` | [`ad_process_para`](ad_process_para.md) | `ad_process_para_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocesspara_addrillrulepara` <!-- FK_IN: adempiere.ad_process_drillrule_para.adprocesspara_addrillrulepara --> | [`ad_process_drillrule_para`](ad_process_drillrule_para.md) | `ad_process_para_id` | [`ad_process_para`](ad_process_para.md) | `ad_process_para_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocpara_adprocparatrl` <!-- FK_IN: adempiere.ad_process_para_trl.adprocpara_adprocparatrl --> | [`ad_process_para_trl`](ad_process_para_trl.md) | `ad_process_para_id` | [`ad_process_para`](ad_process_para.md) | `ad_process_para_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocesspara_adschedulerpara` <!-- FK_IN: adempiere.ad_scheduler_para.adprocesspara_adschedulerpara --> | [`ad_scheduler_para`](ad_scheduler_para.md) | `ad_process_para_id` | [`ad_process_para`](ad_process_para.md) | `ad_process_para_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocesspara_aduserdefprocpar` <!-- FK_IN: adempiere.ad_userdef_proc_parameter.adprocesspara_aduserdefprocpar --> | [`ad_userdef_proc_parameter`](ad_userdef_proc_parameter.md) | `ad_process_para_id` | [`ad_process_para`](ad_process_para.md) | `ad_process_para_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocesspara_adwfnodepara` <!-- FK_IN: adempiere.ad_wf_node_para.adprocesspara_adwfnodepara --> | [`ad_wf_node_para`](ad_wf_node_para.md) | `ad_process_para_id` | [`ad_process_para`](ad_process_para.md) | `ad_process_para_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocesspara_aspclientexcepti` <!-- FK_IN: adempiere.asp_clientexception.adprocesspara_aspclientexcepti --> | [`asp_clientexception`](../asp/asp_clientexception.md) | `ad_process_para_id` | [`ad_process_para`](ad_process_para.md) | `ad_process_para_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocesspara_aspprocesspara` <!-- FK_IN: adempiere.asp_process_para.adprocesspara_aspprocesspara --> | [`asp_process_para`](../asp/asp_process_para.md) | `ad_process_para_id` | [`ad_process_para`](ad_process_para.md) | `ad_process_para_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
