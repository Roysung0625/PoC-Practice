# ad_infocolumn — 조회 창 열

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_infocolumn` |
| 한국어 논리명(문서용 해석) | 조회 창 열 |
| 원본 논리명 | Info Column |
| 원본 사전 ID | 897 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 198 |
| 물리 열 수 | 41 |
| 나가는 FK / 들어오는 FK | 7 / 5 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

조회 창에 표시할 열과 검색 조건·표현식·참조·입력 규칙을 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_infocolumn_pkey` | `ad_infocolumn_id` |
| UNIQUE | `ad_infocolumn_uu_idx` | `ad_infocolumn_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_infocolumn_id` | Info Column | numeric(10,0) | 불가 | 예 | — | Info Window Column |
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
| 12 | `ad_infowindow_id` | Info Window | numeric(10,0) | 불가 | — | — | Info and search/select Window |
| 13 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 14 | `selectclause` | Sql SELECT | character varying(2000) | 불가 | — | — | SQL SELECT clause |
| 15 | `seqno` | Sequence | numeric(10,0) | 불가 | — | 0 | Method of ordering records; lowest number comes first |
| 16 | `isdisplayed` | Displayed | character(1) | 불가 | — | 'Y'::bpchar | Determines, if this field is displayed |
| 17 | `isquerycriteria` | Query Criteria | character(1) | 불가 | — | 'N'::bpchar | The column is also used as a query criteria |
| 18 | `ad_element_id` | System Element | numeric(10,0) | 허용 | — | — | System Element enables the central maintenance of column description and help. |
| 19 | `ad_reference_id` | Reference | numeric(10,0) | 불가 | — | — | System Reference and Validation |
| 20 | `ad_infocolumn_uu` | AD_InfoColumn_UU | uuid | 허용 | — | — | — |
| 21 | `ad_reference_value_id` | Reference Key | numeric(10,0) | 허용 | — | NULL::numeric | Required to specify, if data type is Table or List |
| 22 | `ad_val_rule_id` | Dynamic Validation | numeric(10,0) | 허용 | — | NULL::numeric | Dynamic Validation Rule |
| 23 | `iscentrallymaintained` | Centrally maintained | character(1) | 불가 | — | 'Y'::bpchar | Information maintained in System Element table |
| 24 | `displaylogic` | Display Logic | character varying(2000) | 허용 | — | NULL::character varying | If the Field is displayed, the result determines if the field is actually displayed |
| 25 | `columnname` | DB Column Name | character varying(63) | 불가 | — | — | Name of the column in the database |
| 26 | `queryoperator` | Query Operator | character varying(10) | 허용 | — | NULL::character varying | Operator for database query |
| 27 | `queryfunction` | Query Function | character varying(255) | 허용 | — | NULL::character varying | Database function for query |
| 28 | `isidentifier` | Identifier | character(1) | 불가 | — | 'N'::bpchar | This column is part of the record identifier |
| 29 | `seqnoselection` | Selection Column Sequence | numeric(10,0) | 허용 | — | (0)::numeric | Selection Column Sequence |
| 30 | `defaultvalue` | Default Logic | character varying(2000) | 허용 | — | NULL::character varying | Default value hierarchy, separated by ; |
| 31 | `ismandatory` | Mandatory | character(1) | 불가 | — | 'N'::bpchar | Data entry is required in this column |
| 32 | `iskey` | Key column | character(1) | 허용 | — | NULL::bpchar | This column is the key in this table |
| 33 | `isreadonly` | Read Only | character(1) | 불가 | — | 'Y'::bpchar | Field is read only |
| 34 | `placeholder` | Placeholder | character varying(255) | 허용 | — | NULL::character varying | — |
| 35 | `inputfieldvalidation` | Input field validation | character varying(2000) | 허용 | — | NULL::character varying | Input field validation query |
| 36 | `ad_fieldstyle_id` | Field Style | numeric(10,0) | 허용 | — | NULL::numeric | Field CSS Style  |
| 37 | `isautocomplete` | Auto complete | character(1) | 불가 | — | 'N'::bpchar | Automatic completion for text fields |
| 38 | `isqueryafterchange` | Query After Change | character(1) | 불가 | — | 'N'::bpchar | Issues a query request after the user has made changes to the field |
| 39 | `isrange` | Range | character(1) | 불가 | — | 'N'::bpchar | The parameter is a range of values |
| 40 | `defaultvalue2` | Default Logic 2 | character varying(2000) | 허용 | — | NULL::character varying | Default value hierarchy, separated by ; |
| 41 | `placeholder2` | Placeholder2 | character varying(255) | 허용 | — | NULL::character varying | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 12개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_element"]
    n1["ad_entitytype"]
    n2["ad_infocolumn"]
    n3["ad_infocolumn_trl"]
    n4["ad_infoprocess"]
    n5["ad_inforelated"]
    n6["ad_infowindow"]
    n7["ad_reference"]
    n8["ad_style"]
    n9["ad_val_rule"]
    n2 -->|"ad_element_id → ad_element_id"| n0
    n2 -->|"ad_fieldstyle_id → ad_style_id"| n8
    n2 -->|"ad_infowindow_id → ad_infowindow_id"| n6
    n2 -->|"ad_reference_id → ad_reference_id"| n7
    n2 -->|"ad_reference_value_id → ad_reference_id"| n7
    n2 -->|"ad_val_rule_id → ad_val_rule_id"| n9
    n2 -->|"entitytype → entitytype"| n1
    n3 -->|"ad_infocolumn_id → ad_infocolumn_id"| n2
    n4 -->|"ad_infocolumn_id → ad_infocolumn_id"| n2
    n5 -->|"parentrelatedcolumn_id → ad_infocolumn_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adelement_adinfocolumn` <!-- FK_OUT: adempiere.ad_infocolumn.adelement_adinfocolumn --> | [`ad_infocolumn`](ad_infocolumn.md) | `ad_element_id` | [`ad_element`](ad_element.md) | `ad_element_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfieldstyle_adinfocolumn` <!-- FK_OUT: adempiere.ad_infocolumn.adfieldstyle_adinfocolumn --> | [`ad_infocolumn`](ad_infocolumn.md) | `ad_fieldstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adinfowindow_adinfocolumn` <!-- FK_OUT: adempiere.ad_infocolumn.adinfowindow_adinfocolumn --> | [`ad_infocolumn`](ad_infocolumn.md) | `ad_infowindow_id` | [`ad_infowindow`](ad_infowindow.md) | `ad_infowindow_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreference_adinfocolumn` <!-- FK_OUT: adempiere.ad_infocolumn.adreference_adinfocolumn --> | [`ad_infocolumn`](ad_infocolumn.md) | `ad_reference_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreferencevalue_adinfocolumn` <!-- FK_OUT: adempiere.ad_infocolumn.adreferencevalue_adinfocolumn --> | [`ad_infocolumn`](ad_infocolumn.md) | `ad_reference_value_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `advalrule_adinfocolumn` <!-- FK_OUT: adempiere.ad_infocolumn.advalrule_adinfocolumn --> | [`ad_infocolumn`](ad_infocolumn.md) | `ad_val_rule_id` | [`ad_val_rule`](ad_val_rule.md) | `ad_val_rule_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adinfocolumn` <!-- FK_OUT: adempiere.ad_infocolumn.entityt_adinfocolumn --> | [`ad_infocolumn`](ad_infocolumn.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adinfocolumn_adinfocolumntrl` <!-- FK_IN: adempiere.ad_infocolumn_trl.adinfocolumn_adinfocolumntrl --> | [`ad_infocolumn_trl`](ad_infocolumn_trl.md) | `ad_infocolumn_id` | [`ad_infocolumn`](ad_infocolumn.md) | `ad_infocolumn_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adinfocolumn_adinfoprocess` <!-- FK_IN: adempiere.ad_infoprocess.adinfocolumn_adinfoprocess --> | [`ad_infoprocess`](ad_infoprocess.md) | `ad_infocolumn_id` | [`ad_infocolumn`](ad_infocolumn.md) | `ad_infocolumn_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `parentrelatedcolumn_adinforela` <!-- FK_IN: adempiere.ad_inforelated.parentrelatedcolumn_adinforela --> | [`ad_inforelated`](ad_inforelated.md) | `parentrelatedcolumn_id` | [`ad_infocolumn`](ad_infocolumn.md) | `ad_infocolumn_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `relatedcolumn_adinforelated` <!-- FK_IN: adempiere.ad_inforelated.relatedcolumn_adinforelated --> | [`ad_inforelated`](ad_inforelated.md) | `relatedcolumn_id` | [`ad_infocolumn`](ad_infocolumn.md) | `ad_infocolumn_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adinfocolumn_aduserdefinfocolu` <!-- FK_IN: adempiere.ad_userdef_info_column.adinfocolumn_aduserdefinfocolu --> | [`ad_userdef_info_column`](ad_userdef_info_column.md) | `ad_infocolumn_id` | [`ad_infocolumn`](ad_infocolumn.md) | `ad_infocolumn_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
