# pa_documentstatus — 문서 상태 표시 설정

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.pa_documentstatus` |
| 한국어 논리명(문서용 해석) | 문서 상태 표시 설정 |
| 원본 논리명 | Document Status |
| 원본 사전 ID | 200216 |
| 분류 | `pa` — 성과·보고서·대시보드 |
| 전체 테넌트 행 수 | 16 |
| 물리 열 수 | 30 |
| 나가는 FK / 들어오는 FK | 15 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

테이블과 조회 조건을 기준으로 표시할 문서 상태 항목 및 연결 화면·표시 서식을 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `pa_documentstatus_key` | `pa_documentstatus_id` |
| UNIQUE | `pa_documentstatus_uu_idx` | `pa_documentstatus_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `pa_documentstatus_id` | Document Status | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `ad_role_id` | Role | numeric(10,0) | 허용 | — | — | Responsibility Role |
| 5 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | — | User within the system - Internal or Business Partner Contact |
| 6 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 7 | `created` | Created | timestamp without time zone | 불가 | — | — | Date this record was created |
| 8 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 9 | `updated` | Updated | timestamp without time zone | 불가 | — | — | Date this record was updated |
| 10 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 11 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 12 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 13 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 14 | `seqno` | Sequence | numeric(10,0) | 불가 | — | — | Method of ordering records; lowest number comes first |
| 15 | `name_printcolor_id` | Print Color for Name | numeric(10,0) | 허용 | — | — | — |
| 16 | `name_printfont_id` | Print Font for Name | numeric(10,0) | 허용 | — | — | — |
| 17 | `number_printcolor_id` | Print Color for Number | numeric(10,0) | 허용 | — | — | — |
| 18 | `number_printfont_id` | Print Font for Number | numeric(10,0) | 허용 | — | — | — |
| 19 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 20 | `whereclause` | Sql WHERE | character varying(2000) | 허용 | — | — | Fully qualified SQL WHERE clause |
| 21 | `ad_window_id` | Window | numeric(10,0) | 허용 | — | — | Data entry or display window |
| 22 | `ad_form_id` | Special Form | numeric(10,0) | 허용 | — | — | Special Form |
| 23 | `pa_documentstatus_uu` | PA_DocumentStatus_UU | uuid | 허용 | — | — | — |
| 24 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 25 | `ishidewhenzero` | Hide when Zero | character(1) | 불가 | — | 'N'::bpchar | Hide when the Value is Zero |
| 26 | `help` | Comment/Help | character varying(4000) | 허용 | — | NULL::character varying | Comment or Hint |
| 27 | `name_printcolorzero_id` | Print Color for Name when Zero | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 28 | `ad_fieldgroup_id` | Field Group | numeric(10,0) | 허용 | — | NULL::numeric | Logical grouping of fields |
| 29 | `ad_process_id` | Process | numeric(10,0) | 허용 | — | NULL::numeric | Process or Report |
| 30 | `ad_infowindow_id` | Info Window | numeric(10,0) | 허용 | — | NULL::numeric | Info and search/select Window |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 17개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_entitytype"]
    n1["ad_fieldgroup"]
    n2["ad_form"]
    n3["ad_infowindow"]
    n4["ad_process"]
    n5["ad_role"]
    n6["ad_table"]
    n7["ad_user"]
    n8["ad_window"]
    n9["c_project"]
    n10["pa_documentstatus"]
    n10 -->|"ad_fieldgroup_id → ad_fieldgroup_id"| n1
    n10 -->|"ad_form_id → ad_form_id"| n2
    n10 -->|"ad_infowindow_id → ad_infowindow_id"| n3
    n10 -->|"ad_process_id → ad_process_id"| n4
    n10 -->|"ad_role_id → ad_role_id"| n5
    n10 -->|"ad_table_id → ad_table_id"| n6
    n10 -->|"ad_user_id → ad_user_id"| n7
    n10 -->|"ad_window_id → ad_window_id"| n8
    n10 -->|"c_project_id → c_project_id"| n9
    n10 -->|"entitytype → entitytype"| n0
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adfieldgroup_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.adfieldgroup_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `ad_fieldgroup_id` | [`ad_fieldgroup`](../ad/ad_fieldgroup.md) | `ad_fieldgroup_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.adform_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `ad_form_id` | [`ad_form`](../ad/ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adinfowindow_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.adinfowindow_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `ad_infowindow_id` | [`ad_infowindow`](../ad/ad_infowindow.md) | `ad_infowindow_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocess_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.adprocess_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `ad_process_id` | [`ad_process`](../ad/ad_process.md) | `ad_process_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adrole_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.adrole_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `ad_role_id` | [`ad_role`](../ad/ad_role.md) | `ad_role_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtable_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.adtable_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `ad_table_id` | [`ad_table`](../ad/ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduser_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.aduser_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwindow_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.adwindow_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `ad_window_id` | [`ad_window`](../ad/ad_window.md) | `ad_window_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.cproject_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entitytype_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.entitytype_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `entitytype` | [`ad_entitytype`](../ad/ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `nameprintcolor_padocumentstatu` <!-- FK_OUT: adempiere.pa_documentstatus.nameprintcolor_padocumentstatu --> | [`pa_documentstatus`](pa_documentstatus.md) | `name_printcolor_id` | [`ad_printcolor`](../ad/ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `nameprintcolorzero_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.nameprintcolorzero_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `name_printcolorzero_id` | [`ad_printcolor`](../ad/ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `nameprintfont_padocumentstatus` <!-- FK_OUT: adempiere.pa_documentstatus.nameprintfont_padocumentstatus --> | [`pa_documentstatus`](pa_documentstatus.md) | `name_printfont_id` | [`ad_printfont`](../ad/ad_printfont.md) | `ad_printfont_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `numberprintcolor_padocumentsta` <!-- FK_OUT: adempiere.pa_documentstatus.numberprintcolor_padocumentsta --> | [`pa_documentstatus`](pa_documentstatus.md) | `number_printcolor_id` | [`ad_printcolor`](../ad/ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `numberprintfont_padocumentstat` <!-- FK_OUT: adempiere.pa_documentstatus.numberprintfont_padocumentstat --> | [`pa_documentstatus`](pa_documentstatus.md) | `number_printfont_id` | [`ad_printfont`](../ad/ad_printfont.md) | `ad_printfont_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `padocumentstatus_padocumentsta` <!-- FK_IN: adempiere.pa_documentstatus_trl.padocumentstatus_padocumentsta --> | [`pa_documentstatus_trl`](pa_documentstatus_trl.md) | `pa_documentstatus_id` | [`pa_documentstatus`](pa_documentstatus.md) | `pa_documentstatus_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `padocumentstatus_padocstataccs` <!-- FK_IN: adempiere.pa_documentstatusaccess.padocumentstatus_padocstataccs --> | [`pa_documentstatusaccess`](pa_documentstatusaccess.md) | `pa_documentstatus_id` | [`pa_documentstatus`](pa_documentstatus.md) | `pa_documentstatus_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
