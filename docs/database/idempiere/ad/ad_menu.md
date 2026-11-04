# ad_menu — 메뉴

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_menu` |
| 한국어 논리명(문서용 해석) | 메뉴 |
| 원본 논리명 | Menu |
| 원본 사전 ID | 116 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 813 |
| 물리 열 수 | 25 |
| 나가는 FK / 들어오는 FK | 10 / 4 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

시스템 메뉴 항목을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Identifies a Menu
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_menu_pkey` | `ad_menu_id` |
| UNIQUE | `ad_menu_uu_idx` | `ad_menu_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_menu_id` | Menu | numeric(10,0) | 불가 | 예 | — | Identifies a Menu |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 9 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `issummary` | Summary Level | character(1) | 불가 | — | 'N'::bpchar | This is a summary entity |
| 12 | `issotrx` | Sales Transaction | character(1) | 불가 | — | 'Y'::bpchar | This is a Sales Transaction |
| 13 | `isreadonly` | Read Only | character(1) | 불가 | — | 'N'::bpchar | Field is read only |
| 14 | `action` | Action | character(1) | 허용 | — | — | Indicates the Action to be performed |
| 15 | `ad_window_id` | Window | numeric(10,0) | 허용 | — | — | Data entry or display window |
| 16 | `ad_workflow_id` | Workflow | numeric(10,0) | 허용 | — | — | Workflow or combination of tasks |
| 17 | `ad_task_id` | OS Task | numeric(10,0) | 허용 | — | — | Operation System Task |
| 18 | `ad_process_id` | Process | numeric(10,0) | 허용 | — | — | Process or Report |
| 19 | `ad_form_id` | Special Form | numeric(10,0) | 허용 | — | — | Special Form |
| 20 | `ad_workbench_id` | Workbench | numeric(10,0) | 허용 | — | — | Collection of windows, reports |
| 21 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 22 | `iscentrallymaintained` | Centrally maintained | character(1) | 허용 | — | 'Y'::bpchar | Information maintained in System Element table |
| 23 | `ad_menu_uu` | AD_Menu_UU | uuid | 허용 | — | — | — |
| 24 | `ad_infowindow_id` | Info Window | numeric(10,0) | 허용 | — | NULL::numeric | Info and search/select Window |
| 25 | `predefinedcontextvariables` | Predefined Context Variables | character varying(4000) | 허용 | — | NULL::character varying | Predefined context variables to inject when opening a menu entry or a window |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 14개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_entitytype"]
    n2["ad_form"]
    n3["ad_infowindow"]
    n4["ad_menu"]
    n5["ad_org"]
    n6["ad_process"]
    n7["ad_task"]
    n8["ad_window"]
    n9["ad_workbench"]
    n10["ad_workflow"]
    n4 -->|"ad_org_id → ad_org_id"| n5
    n4 -->|"ad_client_id → ad_client_id"| n0
    n4 -->|"ad_form_id → ad_form_id"| n2
    n4 -->|"ad_infowindow_id → ad_infowindow_id"| n3
    n4 -->|"ad_workbench_id → ad_workbench_id"| n9
    n4 -->|"ad_process_id → ad_process_id"| n6
    n4 -->|"ad_task_id → ad_task_id"| n7
    n4 -->|"ad_window_id → ad_window_id"| n8
    n4 -->|"ad_workflow_id → ad_workflow_id"| n10
    n4 -->|"entitytype → entitytype"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ad_menu_org` <!-- FK_OUT: adempiere.ad_menu.ad_menu_org --> | [`ad_menu`](ad_menu.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adclient_admenu` <!-- FK_OUT: adempiere.ad_menu.adclient_admenu --> | [`ad_menu`](ad_menu.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_admenu` <!-- FK_OUT: adempiere.ad_menu.adform_admenu --> | [`ad_menu`](ad_menu.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adinfowindow_admenu` <!-- FK_OUT: adempiere.ad_menu.adinfowindow_admenu --> | [`ad_menu`](ad_menu.md) | `ad_infowindow_id` | [`ad_infowindow`](ad_infowindow.md) | `ad_infowindow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `admenu_adworkbench` <!-- FK_OUT: adempiere.ad_menu.admenu_adworkbench --> | [`ad_menu`](ad_menu.md) | `ad_workbench_id` | [`ad_workbench`](ad_workbench.md) | `ad_workbench_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocess_admenu` <!-- FK_OUT: adempiere.ad_menu.adprocess_admenu --> | [`ad_menu`](ad_menu.md) | `ad_process_id` | [`ad_process`](ad_process.md) | `ad_process_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtask_admenu` <!-- FK_OUT: adempiere.ad_menu.adtask_admenu --> | [`ad_menu`](ad_menu.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwindow_admenu` <!-- FK_OUT: adempiere.ad_menu.adwindow_admenu --> | [`ad_menu`](ad_menu.md) | `ad_window_id` | [`ad_window`](ad_window.md) | `ad_window_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_admenu` <!-- FK_OUT: adempiere.ad_menu.adworkflow_admenu --> | [`ad_menu`](ad_menu.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_admenu` <!-- FK_OUT: adempiere.ad_menu.entityt_admenu --> | [`ad_menu`](ad_menu.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ad_menutrl` <!-- FK_IN: adempiere.ad_menu_trl.ad_menutrl --> | [`ad_menu_trl`](ad_menu_trl.md) | `ad_menu_id` | [`ad_menu`](ad_menu.md) | `ad_menu_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `admenu_adpackageexpcommon` <!-- FK_IN: adempiere.ad_package_exp_common.admenu_adpackageexpcommon --> | [`ad_package_exp_common`](ad_package_exp_common.md) | `ad_menu_id` | [`ad_menu`](ad_menu.md) | `ad_menu_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `admenu_adpackageexpdetail` <!-- FK_IN: adempiere.ad_package_exp_detail.admenu_adpackageexpdetail --> | [`ad_package_exp_detail`](ad_package_exp_detail.md) | `ad_menu_id` | [`ad_menu`](ad_menu.md) | `ad_menu_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `admenu_adtreefavoritenode` <!-- FK_IN: adempiere.ad_tree_favorite_node.admenu_adtreefavoritenode --> | [`ad_tree_favorite_node`](ad_tree_favorite_node.md) | `ad_menu_id` | [`ad_menu`](ad_menu.md) | `ad_menu_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `issotrx`가 있습니다. 판매(`Y`)와 구매(`N`)를 구분해서 분석합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
