# ad_toolbarbutton — 도구 모음 버튼

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_toolbarbutton` |
| 한국어 논리명(문서용 해석) | 도구 모음 버튼 |
| 원본 논리명 | ToolBar Button |
| 원본 사전 ID | 200003 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 87 |
| 물리 열 수 | 28 |
| 나가는 FK / 들어오는 FK | 3 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

버튼 동작·구현 클래스·단축키·표시 조건과 연결 프로세스를 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_toolbarbutton_key` | `ad_toolbarbutton_id` |
| UNIQUE | `ad_toolbarbutton_uu_idx` | `ad_toolbarbutton_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `actionclassname` | Service Component Name | character varying(255) | 허용 | — | NULL::character varying | The service component name that implements the interface for toolbar actions |
| 2 | `actionname` | Action Name | character varying(60) | 허용 | — | NULL::character varying | Action name on the toolbar |
| 3 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 4 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 5 | `ad_toolbarbutton_id` | ToolBar Button | numeric(10,0) | 불가 | 예 | — | — |
| 6 | `classname` | Classname | character varying(255) | 허용 | — | — | Java Classname |
| 7 | `componentname` | Component Name | character varying(255) | 불가 | — | — | — |
| 8 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 9 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 10 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 11 | `iscustomization` | Customization | character(1) | 불가 | — | 'N'::bpchar | The change is a customization of the data dictionary and can be applied after Migration |
| 12 | `keystroke_keycode` | Key Code | numeric(10,0) | 허용 | — | NULL::numeric | Key Code for shortcuts |
| 13 | `keystroke_modifiers` | Keystroke Modifiers | numeric(10,0) | 허용 | — | NULL::numeric | Keystroke Modifiers for shortcuts |
| 14 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 15 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 16 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 17 | `ad_toolbarbutton_uu` | AD_ToolBarButton_UU | uuid | 허용 | — | — | — |
| 18 | `action` | Action | character(1) | 불가 | — | 'W'::bpchar | Indicates the Action to be performed |
| 19 | `ad_tab_id` | Tab | numeric(10,0) | 허용 | — | NULL::numeric | Tab within a Window |
| 20 | `ad_process_id` | Process | numeric(10,0) | 허용 | — | NULL::numeric | Process or Report |
| 21 | `displaylogic` | Display Logic | character varying(2000) | 허용 | — | NULL::character varying | If the Field is displayed, the result determines if the field is actually displayed |
| 22 | `seqno` | Sequence | numeric(10,0) | 허용 | — | NULL::numeric | Method of ordering records; lowest number comes first |
| 23 | `isadvancedbutton` | Advanced Button | character(1) | 불가 | — | 'N'::bpchar | This Button contains advanced Functionality |
| 24 | `isaddseparator` | Add Separator | character(1) | 불가 | — | 'N'::bpchar | — |
| 25 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 26 | `isshowmore` | Group in show more | character(1) | 허용 | — | 'N'::bpchar | — |
| 27 | `readonlylogic` | Read Only Logic | character varying(2000) | 허용 | — | NULL::character varying | Logic to determine if field is read only (applies only when field is read-write) |
| 28 | `pressedlogic` | Pressed Logic | character varying(2000) | 허용 | — | NULL::character varying | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_entitytype"]
    n1["ad_process"]
    n2["ad_tab"]
    n3["ad_toolbarbutton"]
    n4["ad_toolbarbuttonrestrict"]
    n3 -->|"ad_process_id → ad_process_id"| n1
    n3 -->|"ad_tab_id → ad_tab_id"| n2
    n3 -->|"entitytype → entitytype"| n0
    n4 -->|"ad_toolbarbutton_id → ad_toolbarbutton_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adprocess_adtoolbarbutton` <!-- FK_OUT: adempiere.ad_toolbarbutton.adprocess_adtoolbarbutton --> | [`ad_toolbarbutton`](ad_toolbarbutton.md) | `ad_process_id` | [`ad_process`](ad_process.md) | `ad_process_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtab_adtoolbarbutton` <!-- FK_OUT: adempiere.ad_toolbarbutton.adtab_adtoolbarbutton --> | [`ad_toolbarbutton`](ad_toolbarbutton.md) | `ad_tab_id` | [`ad_tab`](ad_tab.md) | `ad_tab_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entitytype_adtoolbarbutton` <!-- FK_OUT: adempiere.ad_toolbarbutton.entitytype_adtoolbarbutton --> | [`ad_toolbarbutton`](ad_toolbarbutton.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adtoolbarbutton_adtoolbarbutto` <!-- FK_IN: adempiere.ad_toolbarbuttonrestrict.adtoolbarbutton_adtoolbarbutto --> | [`ad_toolbarbuttonrestrict`](ad_toolbarbuttonrestrict.md) | `ad_toolbarbutton_id` | [`ad_toolbarbutton`](ad_toolbarbutton.md) | `ad_toolbarbutton_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
