# ad_userdef_field — 사용자 정의 필드 설정

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_userdef_field` |
| 한국어 논리명(문서용 해석) | 사용자 정의 필드 설정 |
| 원본 논리명 | User defined Field |
| 원본 사전 ID | 464 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 47 |
| 나가는 FK / 들어오는 FK | 11 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

기존 필드의 이름·표시·입력·검증·배치를 사용자 정의 탭 안에서 재설정한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_userdef_field_pkey` | `ad_userdef_field_id` |
| UNIQUE | `ad_userdef_field_uu_idx` | `ad_userdef_field_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_userdef_field_unique`: `CREATE UNIQUE INDEX ad_userdef_field_unique ON adempiere.ad_userdef_field USING btree (ad_userdef_tab_id, ad_field_id)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_userdef_field_id` | User defined Field | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `ad_userdef_tab_id` | User defined Tab | numeric(10,0) | 불가 | — | — | — |
| 10 | `ad_field_id` | Field | numeric(10,0) | 불가 | — | — | Field on a database table |
| 11 | `name` | Name | character varying(60) | 허용 | — | — | Alphanumeric identifier of the entity |
| 12 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 13 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 14 | `isdisplayed` | Displayed | character(1) | 허용 | — | — | Determines, if this field is displayed |
| 15 | `isreadonly` | Read Only | character(1) | 허용 | — | — | Field is read only |
| 16 | `issameline` | Same Line | character(1) | 허용 | — | — | Displayed on same line as previous field |
| 17 | `isupdateable` | Updatable | character(1) | 허용 | — | — | Determines, if the field can be updated |
| 18 | `displaylength` | Display Length | numeric(10,0) | 불가 | — | 0 | Length of the display in characters |
| 19 | `displaylogic` | Display Logic | character varying(2000) | 허용 | — | — | If the Field is displayed, the result determines if the field is actually displayed |
| 20 | `defaultvalue` | Default Logic | character varying(2000) | 허용 | — | — | Default value hierarchy, separated by ; |
| 21 | `sortno` | Record Sort No | numeric(10,0) | 불가 | — | 0 | Determines in what order the records are displayed |
| 22 | `seqno` | Sequence | numeric(10,0) | 불가 | — | (0)::numeric | Method of ordering records; lowest number comes first |
| 23 | `ad_userdef_field_uu` | AD_UserDef_Field_UU | uuid | 허용 | — | — | — |
| 24 | `isalwaysupdateable` | Always Updatable | character(1) | 허용 | — | NULL::bpchar | The column is always updateable, even if the record is not active or processed |
| 25 | `mandatorylogic` | Mandatory Logic | character varying(2000) | 허용 | — | NULL::character varying | — |
| 26 | `readonlylogic` | Read Only Logic | character varying(2000) | 허용 | — | NULL::character varying | Logic to determine if field is read only (applies only when field is read-write) |
| 27 | `ad_reference_value_id` | Reference Key | numeric(10,0) | 허용 | — | NULL::numeric | Required to specify, if data type is Table or List |
| 28 | `ismandatory` | Mandatory | character(1) | 허용 | — | NULL::bpchar | Data entry is required in this column |
| 29 | `xposition` | X Position | numeric(10,0) | 허용 | — | NULL::numeric | Absolute X (horizontal) position in 1/72 of an inch |
| 30 | `numlines` | Number of Lines | numeric(10,0) | 허용 | — | NULL::numeric | Number of lines for a field |
| 31 | `columnspan` | Column Span | numeric(10,0) | 허용 | — | NULL::numeric | Number of column for a box of field |
| 32 | `istoolbarbutton` | Toolbar Button | character(1) | 허용 | — | — | Show the button on the toolbar, the window, or both |
| 33 | `ad_reference_id` | Reference | numeric(10,0) | 허용 | — | NULL::numeric | System Reference and Validation |
| 34 | `ad_val_rule_id` | Dynamic Validation | numeric(10,0) | 허용 | — | NULL::numeric | Dynamic Validation Rule |
| 35 | `vformat` | Value Format | character varying(255) | 허용 | — | NULL::character varying | Format of the value; Can contain fixed format elements, Variables: "_lLoOaAcCa09", or ~regex |
| 36 | `ad_labelstyle_id` | Label Style | numeric(10,0) | 허용 | — | NULL::numeric | Label CSS Style |
| 37 | `ad_fieldstyle_id` | Field Style | numeric(10,0) | 허용 | — | NULL::numeric | Field CSS Style  |
| 38 | `pa_dashboardcontent_id` | Dashboard Content | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 39 | `placeholder` | Placeholder | character varying(255) | 허용 | — | NULL::character varying | — |
| 40 | `isautocomplete` | Auto complete | character(1) | 허용 | — | NULL::bpchar | Automatic completion for text fields |
| 41 | `ad_val_rule_lookup_id` | Dynamic Validation (Lookup) | numeric(10,0) | 허용 | — | NULL::numeric | Override Dynamic Validation Rule for Lookup Window |
| 42 | `ad_fieldgroup_id` | Field Group | numeric(10,0) | 허용 | — | NULL::numeric | Logical grouping of fields |
| 43 | `seqnogrid` | Grid Sequence No | numeric(10,0) | 불가 | — | '0'::numeric | — |
| 44 | `isdisplayedgrid` | Show in Grid | character(1) | 허용 | — | NULL::bpchar | — |
| 45 | `ad_chart_id` | Chart | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 46 | `alwaysupdatablelogic` | Always Updatable Logic | character varying(2000) | 허용 | — | NULL::character varying | Logic to determine if field is Updatable irrespective if record's active status or processed status. This logic Applicable only if Always Updatable is N. |
| 47 | `ishtml` | HTML | character(1) | 허용 | — | NULL::bpchar | Text has HTML tags |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 11개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_chart"]
    n1["ad_field"]
    n2["ad_fieldgroup"]
    n3["ad_reference"]
    n4["ad_style"]
    n5["ad_userdef_field"]
    n6["ad_userdef_tab"]
    n7["ad_val_rule"]
    n5 -->|"ad_chart_id → ad_chart_id"| n0
    n5 -->|"ad_field_id → ad_field_id"| n1
    n5 -->|"ad_fieldgroup_id → ad_fieldgroup_id"| n2
    n5 -->|"ad_fieldstyle_id → ad_style_id"| n4
    n5 -->|"ad_labelstyle_id → ad_style_id"| n4
    n5 -->|"ad_reference_id → ad_reference_id"| n3
    n5 -->|"ad_reference_value_id → ad_reference_id"| n3
    n5 -->|"ad_userdef_tab_id → ad_userdef_tab_id"| n6
    n5 -->|"ad_val_rule_id → ad_val_rule_id"| n7
    n5 -->|"ad_val_rule_lookup_id → ad_val_rule_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adchart_aduserdeffield` <!-- FK_OUT: adempiere.ad_userdef_field.adchart_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_chart_id` | [`ad_chart`](ad_chart.md) | `ad_chart_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfield_aduserdeffield` <!-- FK_OUT: adempiere.ad_userdef_field.adfield_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_field_id` | [`ad_field`](ad_field.md) | `ad_field_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfieldgroup_aduserdeffield` <!-- FK_OUT: adempiere.ad_userdef_field.adfieldgroup_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_fieldgroup_id` | [`ad_fieldgroup`](ad_fieldgroup.md) | `ad_fieldgroup_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfieldstyle_aduserdeffield` <!-- FK_OUT: adempiere.ad_userdef_field.adfieldstyle_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_fieldstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adlabelstyle_aduserdeffield` <!-- FK_OUT: adempiere.ad_userdef_field.adlabelstyle_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_labelstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreference_aduserdeffield` <!-- FK_OUT: adempiere.ad_userdef_field.adreference_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_reference_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreferencevalue_aduserdeffiel` <!-- FK_OUT: adempiere.ad_userdef_field.adreferencevalue_aduserdeffiel --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_reference_value_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduserdeftab_aduserdeffield` <!-- FK_OUT: adempiere.ad_userdef_field.aduserdeftab_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_userdef_tab_id` | [`ad_userdef_tab`](ad_userdef_tab.md) | `ad_userdef_tab_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_aduserdeffield` <!-- FK_OUT: adempiere.ad_userdef_field.advalrule_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrulelookup_aduserdeffield` <!-- FK_OUT: adempiere.ad_userdef_field.advalrulelookup_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_val_rule_lookup_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `padashboardcontent_aduserdeffi` <!-- FK_OUT: adempiere.ad_userdef_field.padashboardcontent_aduserdeffi --> | [`ad_userdef_field`](ad_userdef_field.md) | `pa_dashboardcontent_id` | [`pa_dashboardcontent`](../pa/pa_dashboardcontent.md) | `pa_dashboardcontent_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
