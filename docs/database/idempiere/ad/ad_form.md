# ad_form — 특수 폼

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_form` |
| 한국어 논리명(문서용 해석) | 특수 폼 |
| 원본 논리명 | Special Form |
| 원본 사전 ID | 376 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 51 |
| 물리 열 수 | 19 |
| 나가는 FK / 들어오는 FK | 2 / 14 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

일반 데이터 창과 구분되는 특수 폼을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Special Form
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_form_pkey` | `ad_form_id` |
| UNIQUE | `ad_form_uu_idx` | `ad_form_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_form_id` | Special Form | numeric(10,0) | 불가 | 예 | — | Special Form |
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
| 12 | `accesslevel` | Data Access Level | character(1) | 불가 | — | — | Access Level required |
| 13 | `classname` | Classname | character varying(255) | 허용 | — | — | Java Classname |
| 14 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 15 | `isbetafunctionality` | Beta Functionality | character(1) | 불가 | — | 'N'::bpchar | This functionality is considered Beta |
| 16 | `jspurl` | jsp URL | character varying(120) | 허용 | — | — | Web URL of the jsp function |
| 17 | `ad_form_uu` | AD_Form_UU | uuid | 허용 | — | — | — |
| 18 | `ad_ctxhelp_id` | Context Help | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 19 | `imageurl` | Image URL | character varying(120) | 허용 | — | NULL::character varying | URL of  image |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 16개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_ctxhelp"]
    n1["ad_entitytype"]
    n2["ad_form"]
    n3["ad_form_access"]
    n4["ad_form_trl"]
    n5["ad_issue"]
    n6["ad_menu"]
    n7["ad_package_exp_common"]
    n8["ad_package_exp_detail"]
    n9["ad_preference"]
    n10["ad_process"]
    n2 -->|"ad_ctxhelp_id → ad_ctxhelp_id"| n0
    n2 -->|"entitytype → entitytype"| n1
    n3 -->|"ad_form_id → ad_form_id"| n2
    n4 -->|"ad_form_id → ad_form_id"| n2
    n5 -->|"ad_form_id → ad_form_id"| n2
    n6 -->|"ad_form_id → ad_form_id"| n2
    n7 -->|"ad_form_id → ad_form_id"| n2
    n8 -->|"ad_form_id → ad_form_id"| n2
    n9 -->|"ad_form_id → ad_form_id"| n2
    n10 -->|"ad_form_id → ad_form_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adctxhelp_adform` <!-- FK_OUT: adempiere.ad_form.adctxhelp_adform --> | [`ad_form`](ad_form.md) | `ad_ctxhelp_id` | [`ad_ctxhelp`](ad_ctxhelp.md) | `ad_ctxhelp_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adform` <!-- FK_OUT: adempiere.ad_form.entityt_adform --> | [`ad_form`](ad_form.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adform_adformaccess` <!-- FK_IN: adempiere.ad_form_access.adform_adformaccess --> | [`ad_form_access`](ad_form_access.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_adformtrl` <!-- FK_IN: adempiere.ad_form_trl.adform_adformtrl --> | [`ad_form_trl`](ad_form_trl.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_adissue` <!-- FK_IN: adempiere.ad_issue.adform_adissue --> | [`ad_issue`](ad_issue.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_admenu` <!-- FK_IN: adempiere.ad_menu.adform_admenu --> | [`ad_menu`](ad_menu.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_adpackageexpcommon` <!-- FK_IN: adempiere.ad_package_exp_common.adform_adpackageexpcommon --> | [`ad_package_exp_common`](ad_package_exp_common.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_adpackageexpdetail` <!-- FK_IN: adempiere.ad_package_exp_detail.adform_adpackageexpdetail --> | [`ad_package_exp_detail`](ad_package_exp_detail.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_adpreference` <!-- FK_IN: adempiere.ad_preference.adform_adpreference --> | [`ad_preference`](ad_preference.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_adprocess` <!-- FK_IN: adempiere.ad_process.adform_adprocess --> | [`ad_process`](ad_process.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_adwfnode` <!-- FK_IN: adempiere.ad_wf_node.adform_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_adworkbenchwindow` <!-- FK_IN: adempiere.ad_workbenchwindow.adform_adworkbenchwindow --> | [`ad_workbenchwindow`](ad_workbenchwindow.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_aspclientexception` <!-- FK_IN: adempiere.asp_clientexception.adform_aspclientexception --> | [`asp_clientexception`](../asp/asp_clientexception.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_aspform` <!-- FK_IN: adempiere.asp_form.adform_aspform --> | [`asp_form`](../asp/asp_form.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_padocumentstatus` <!-- FK_IN: adempiere.pa_documentstatus.adform_padocumentstatus --> | [`pa_documentstatus`](../pa/pa_documentstatus.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_ppordernode` <!-- FK_IN: adempiere.pp_order_node.adform_ppordernode --> | [`pp_order_node`](../pp/pp_order_node.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
