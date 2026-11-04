# ad_attribute — 시스템 확장 속성

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_attribute` |
| 한국어 논리명(문서용 해석) | 시스템 확장 속성 |
| 원본 논리명 | System Attribute |
| 원본 사전 ID | 405 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 32 |
| 나가는 FK / 들어오는 FK | 4 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

테이블에 적용할 속성의 참조 유형·검증·기본값·입력 및 표시 규칙을 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_attribute_pkey` | `ad_attribute_id` |
| UNIQUE | `ad_attribute_uu_idx` | `ad_attribute_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_attribute_id` | System Attribute | numeric(10,0) | 불가 | 예 | — | — |
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
| 12 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 13 | `ad_reference_id` | Reference | numeric(10,0) | 불가 | — | — | System Reference and Validation |
| 14 | `ad_reference_value_id` | Reference Key | numeric(10,0) | 허용 | — | — | Required to specify, if data type is Table or List |
| 15 | `ad_val_rule_id` | Dynamic Validation | numeric(10,0) | 허용 | — | — | Dynamic Validation Rule |
| 16 | `callout` | Callout | character varying(60) | 허용 | — | — | Fully qualified class names and method - separated by semicolons |
| 17 | `valuemin` | Min. Value | character varying(20) | 허용 | — | — | Minimum Value for a field |
| 18 | `valuemax` | Max. Value | character varying(20) | 허용 | — | — | Maximum Value for a field |
| 19 | `defaultvalue` | Default Logic | character varying(2000) | 허용 | — | — | Default value hierarchy, separated by ; |
| 20 | `isreadonly` | Read Only | character(1) | 불가 | — | 'N'::bpchar | Field is read only |
| 21 | `isupdateable` | Updatable | character(1) | 불가 | — | 'Y'::bpchar | Determines, if the field can be updated |
| 22 | `ismandatory` | Mandatory | character(1) | 불가 | — | 'N'::bpchar | Data entry is required in this column |
| 23 | `isencrypted` | Encrypted | character(1) | 불가 | — | 'N'::bpchar | Display or Storage is encrypted |
| 24 | `fieldlength` | Length | numeric(10,0) | 허용 | — | — | Length of the column in the database |
| 25 | `displaylength` | Display Length | numeric(10,0) | 허용 | — | — | Length of the display in characters |
| 26 | `displaylogic` | Display Logic | character varying(2000) | 허용 | — | — | If the Field is displayed, the result determines if the field is actually displayed |
| 27 | `vformat` | Value Format | character varying(60) | 허용 | — | — | Format of the value; Can contain fixed format elements, Variables: "_lLoOaAcCa09", or ~regex |
| 28 | `issameline` | Same Line | character(1) | 불가 | — | 'N'::bpchar | Displayed on same line as previous field |
| 29 | `isheading` | Heading only | character(1) | 불가 | — | 'N'::bpchar | Field without Column - Only label is displayed |
| 30 | `isfieldonly` | Field Only | character(1) | 불가 | — | 'N'::bpchar | Label is not displayed |
| 31 | `seqno` | Sequence | numeric(10,0) | 허용 | — | — | Method of ordering records; lowest number comes first |
| 32 | `ad_attribute_uu` | AD_Attribute_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_attribute"]
    n1["ad_attribute_value"]
    n2["ad_reference"]
    n3["ad_table"]
    n4["ad_val_rule"]
    n0 -->|"ad_reference_id → ad_reference_id"| n2
    n0 -->|"ad_reference_value_id → ad_reference_id"| n2
    n0 -->|"ad_table_id → ad_table_id"| n3
    n0 -->|"ad_val_rule_id → ad_val_rule_id"| n4
    n1 -->|"ad_attribute_id → ad_attribute_id"| n0
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adreference_adattribute` <!-- FK_OUT: adempiere.ad_attribute.adreference_adattribute --> | [`ad_attribute`](ad_attribute.md) | `ad_reference_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreferencevalue_adattribute` <!-- FK_OUT: adempiere.ad_attribute.adreferencevalue_adattribute --> | [`ad_attribute`](ad_attribute.md) | `ad_reference_value_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtable_adattribute` <!-- FK_OUT: adempiere.ad_attribute.adtable_adattribute --> | [`ad_attribute`](ad_attribute.md) | `ad_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_adattribute` <!-- FK_OUT: adempiere.ad_attribute.advalrule_adattribute --> | [`ad_attribute`](ad_attribute.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adattribute_adattributevalue` <!-- FK_IN: adempiere.ad_attribute_value.adattribute_adattributevalue --> | [`ad_attribute_value`](ad_attribute_value.md) | `ad_attribute_id` | [`ad_attribute`](ad_attribute.md) | `ad_attribute_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
