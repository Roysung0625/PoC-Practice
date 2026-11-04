# ad_field — 화면 필드

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_field` |
| 한국어 논리명(문서용 해석) | 화면 필드 |
| 원본 논리명 | Field |
| 원본 사전 ID | 107 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 21,281 |
| 물리 열 수 | 60 |
| 나가는 FK / 들어오는 FK | 14 / 5 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

데이터베이스 열을 화면 필드로 표현하기 위한 정의를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Field on a database table
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_field_pkey` | `ad_field_id` |
| UNIQUE | `ad_field_uu_idx` | `ad_field_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_field_column`: `CREATE UNIQUE INDEX ad_field_column ON adempiere.ad_field USING btree (ad_tab_id, ad_column_id)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_field_id` | Field | numeric(10,0) | 불가 | 예 | — | Field on a database table |
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
| 12 | `iscentrallymaintained` | Centrally maintained | character(1) | 불가 | — | 'Y'::bpchar | Information maintained in System Element table |
| 13 | `ad_tab_id` | Tab | numeric(10,0) | 불가 | — | — | Tab within a Window |
| 14 | `ad_column_id` | Column | numeric(10,0) | 허용 | — | — | Column in the table |
| 15 | `ad_fieldgroup_id` | Field Group | numeric(10,0) | 허용 | — | — | Logical grouping of fields |
| 16 | `isdisplayed` | Displayed | character(1) | 불가 | — | 'Y'::bpchar | Determines, if this field is displayed |
| 17 | `displaylogic` | Display Logic | character varying(2000) | 허용 | — | — | If the Field is displayed, the result determines if the field is actually displayed |
| 18 | `displaylength` | Display Length | numeric(10,0) | 허용 | — | — | Length of the display in characters |
| 19 | `isreadonly` | Read Only | character(1) | 불가 | — | 'N'::bpchar | Field is read only |
| 20 | `seqno` | Sequence | numeric(10,0) | 허용 | — | — | Method of ordering records; lowest number comes first |
| 21 | `sortno` | Record Sort No | numeric(10,0) | 허용 | — | — | Determines in what order the records are displayed |
| 22 | `issameline` | Same Line | character(1) | 불가 | — | 'N'::bpchar | Displayed on same line as previous field |
| 23 | `isheading` | Heading only | character(1) | 불가 | — | 'N'::bpchar | Field without Column - Only label is displayed |
| 24 | `isfieldonly` | Field Only | character(1) | 불가 | — | 'N'::bpchar | Label is not displayed |
| 25 | `isencrypted` | Encrypted | character(1) | 불가 | — | 'N'::bpchar | Display or Storage is encrypted |
| 26 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 27 | `obscuretype` | Obscure | character(3) | 허용 | — | — | Type of obscuring the data (limiting the display) |
| 28 | `ad_reference_id` | Reference | numeric(10,0) | 허용 | — | — | System Reference and Validation |
| 29 | `ismandatory` | Mandatory | character(1) | 허용 | — | — | Data entry is required in this column |
| 30 | `included_tab_id` | Included Tab | numeric(10,0) | 허용 | — | — | Included Tab in this Tab (Master Detail) |
| 31 | `defaultvalue` | Default Logic | character varying(2000) | 허용 | — | — | Default value hierarchy, separated by ; |
| 32 | `ad_reference_value_id` | Reference Key | numeric(10,0) | 허용 | — | — | Required to specify, if data type is Table or List |
| 33 | `ad_val_rule_id` | Dynamic Validation | numeric(10,0) | 허용 | — | — | Dynamic Validation Rule |
| 34 | `infofactoryclass` | Info Factory Class | character varying(255) | 허용 | — | — | Fully qualified class name that implements the InfoFactory interface |
| 35 | `ad_field_uu` | AD_Field_UU | uuid | 허용 | — | — | — |
| 36 | `isallowcopy` | Allow Copy | character(1) | 허용 | — | NULL::bpchar | Determine if a column must be copied when pushing the button to copy record |
| 37 | `seqnogrid` | Grid Sequence No | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 38 | `isdisplayedgrid` | Show in Grid | character(1) | 허용 | — | 'Y'::bpchar | — |
| 39 | `xposition` | X Position | numeric(10,0) | 허용 | — | (1)::numeric | Absolute X (horizontal) position in 1/72 of an inch |
| 40 | `numlines` | Number of Lines | numeric(10,0) | 허용 | — | (1)::numeric | Number of lines for a field |
| 41 | `columnspan` | Column Span | numeric(10,0) | 허용 | — | (1)::numeric | Number of column for a box of field |
| 42 | `isquickentry` | Quick Entry | character(1) | 불가 | — | 'N'::bpchar | — |
| 43 | `isupdateable` | Updatable | character(1) | 허용 | — | NULL::bpchar | Determines, if the field can be updated |
| 44 | `isalwaysupdateable` | Always Updatable | character(1) | 허용 | — | NULL::bpchar | The column is always updateable, even if the record is not active or processed |
| 45 | `mandatorylogic` | Mandatory Logic | character varying(2000) | 허용 | — | NULL::character varying | — |
| 46 | `readonlylogic` | Read Only Logic | character varying(2000) | 허용 | — | NULL::character varying | Logic to determine if field is read only (applies only when field is read-write) |
| 47 | `istoolbarbutton` | Toolbar Button | character(1) | 허용 | — | — | Show the button on the toolbar, the window, or both |
| 48 | `isadvancedfield` | Advanced Field | character(1) | 허용 | — | 'N'::bpchar | — |
| 49 | `isdefaultfocus` | Default Focus | character(1) | 불가 | — | 'N'::bpchar | — |
| 50 | `vformat` | Value Format | character varying(255) | 허용 | — | NULL::character varying | Format of the value; Can contain fixed format elements, Variables: "_lLoOaAcCa09", or ~regex |
| 51 | `ad_labelstyle_id` | Label Style | numeric(10,0) | 허용 | — | NULL::numeric | Label CSS Style |
| 52 | `ad_fieldstyle_id` | Field Style | numeric(10,0) | 허용 | — | NULL::numeric | Field CSS Style  |
| 53 | `placeholder` | Placeholder | character varying(255) | 허용 | — | NULL::character varying | — |
| 54 | `isquickform` | Quick Form | character(1) | 불가 | — | 'N'::bpchar | Display in Quick Form |
| 55 | `isselectioncolumn` | Selection Column | character(1) | 허용 | — | NULL::bpchar | Is this column used for finding rows in windows |
| 56 | `ad_val_rule_lookup_id` | Dynamic Validation (Lookup) | numeric(10,0) | 허용 | — | NULL::numeric | Override Dynamic Validation Rule for Lookup Window |
| 57 | `columnsql` | Column SQL | character varying(4000) | 허용 | — | — | Virtual Column (r/o) |
| 58 | `ad_chart_id` | Chart | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 59 | `alwaysupdatablelogic` | Always Updatable Logic | character varying(2000) | 허용 | — | NULL::character varying | Logic to determine if field is Updatable irrespective if record's active status or processed status. This logic Applicable only if Always Updatable is N. |
| 60 | `ishtml` | HTML | character(1) | 허용 | — | NULL::bpchar | Text has HTML tags |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 19개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_chart"]
    n1["ad_column"]
    n2["ad_field"]
    n3["ad_fieldgroup"]
    n4["ad_reference"]
    n5["ad_style"]
    n6["ad_tab"]
    n7["ad_val_rule"]
    n2 -->|"ad_column_id → ad_column_id"| n1
    n2 -->|"ad_tab_id → ad_tab_id"| n6
    n2 -->|"ad_chart_id → ad_chart_id"| n0
    n2 -->|"ad_fieldgroup_id → ad_fieldgroup_id"| n3
    n2 -->|"ad_fieldstyle_id → ad_style_id"| n5
    n2 -->|"ad_labelstyle_id → ad_style_id"| n5
    n2 -->|"ad_reference_id → ad_reference_id"| n4
    n2 -->|"ad_reference_value_id → ad_reference_id"| n4
    n2 -->|"ad_val_rule_id → ad_val_rule_id"| n7
    n2 -->|"ad_val_rule_lookup_id → ad_val_rule_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ad_column_field` <!-- FK_OUT: adempiere.ad_field.ad_column_field --> | [`ad_field`](ad_field.md) | `ad_column_id` | [`ad_column`](ad_column.md) | `ad_column_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_tab_field` <!-- FK_OUT: adempiere.ad_field.ad_tab_field --> | [`ad_field`](ad_field.md) | `ad_tab_id` | [`ad_tab`](ad_tab.md) | `ad_tab_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adchart_adfield` <!-- FK_OUT: adempiere.ad_field.adchart_adfield --> | [`ad_field`](ad_field.md) | `ad_chart_id` | [`ad_chart`](ad_chart.md) | `ad_chart_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfieldgroup_adfield` <!-- FK_OUT: adempiere.ad_field.adfieldgroup_adfield --> | [`ad_field`](ad_field.md) | `ad_fieldgroup_id` | [`ad_fieldgroup`](ad_fieldgroup.md) | `ad_fieldgroup_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfieldstyle_adfield` <!-- FK_OUT: adempiere.ad_field.adfieldstyle_adfield --> | [`ad_field`](ad_field.md) | `ad_fieldstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adlabelstyle_adfield` <!-- FK_OUT: adempiere.ad_field.adlabelstyle_adfield --> | [`ad_field`](ad_field.md) | `ad_labelstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreference_adfield` <!-- FK_OUT: adempiere.ad_field.adreference_adfield --> | [`ad_field`](ad_field.md) | `ad_reference_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreferencevalue_adfield` <!-- FK_OUT: adempiere.ad_field.adreferencevalue_adfield --> | [`ad_field`](ad_field.md) | `ad_reference_value_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_adfield` <!-- FK_OUT: adempiere.ad_field.advalrule_adfield --> | [`ad_field`](ad_field.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrulelookup_adfield` <!-- FK_OUT: adempiere.ad_field.advalrulelookup_adfield --> | [`ad_field`](ad_field.md) | `ad_val_rule_lookup_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adfield` <!-- FK_OUT: adempiere.ad_field.entityt_adfield --> | [`ad_field`](ad_field.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `fieldclient` <!-- FK_OUT: adempiere.ad_field.fieldclient --> | [`ad_field`](ad_field.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `fieldorg` <!-- FK_OUT: adempiere.ad_field.fieldorg --> | [`ad_field`](ad_field.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `includedtab_adfield` <!-- FK_OUT: adempiere.ad_field.includedtab_adfield --> | [`ad_field`](ad_field.md) | `included_tab_id` | [`ad_tab`](ad_tab.md) | `ad_tab_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ad_fieldtrl` <!-- FK_IN: adempiere.ad_field_trl.ad_fieldtrl --> | [`ad_field_trl`](ad_field_trl.md) | `ad_field_id` | [`ad_field`](ad_field.md) | `ad_field_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfield_adfieldsuggestion` <!-- FK_IN: adempiere.ad_fieldsuggestion.adfield_adfieldsuggestion --> | [`ad_fieldsuggestion`](ad_fieldsuggestion.md) | `ad_field_id` | [`ad_field`](ad_field.md) | `ad_field_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfield_aduserdeffield` <!-- FK_IN: adempiere.ad_userdef_field.adfield_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_field_id` | [`ad_field`](ad_field.md) | `ad_field_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfield_aspclientexception` <!-- FK_IN: adempiere.asp_clientexception.adfield_aspclientexception --> | [`asp_clientexception`](../asp/asp_clientexception.md) | `ad_field_id` | [`ad_field`](ad_field.md) | `ad_field_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfield_aspfield` <!-- FK_IN: adempiere.asp_field.adfield_aspfield --> | [`asp_field`](../asp/asp_field.md) | `ad_field_id` | [`ad_field`](ad_field.md) | `ad_field_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
