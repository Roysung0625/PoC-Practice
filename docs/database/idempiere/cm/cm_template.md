# cm_template — 웹 콘텐츠 템플릿

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.cm_template` |
| 한국어 논리명(문서용 해석) | 웹 콘텐츠 템플릿 |
| 원본 논리명 | Template |
| 원본 사전 ID | 854 |
| 분류 | `cm` — 웹 콘텐츠 관리 |
| 전체 테넌트 행 수 | 4 |
| 물리 열 수 | 22 |
| 나가는 FK / 들어오는 FK | 1 / 4 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

콘텐츠 표시를 위한 레이아웃과 처리 스크립트 등의 템플릿을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Template defines how content is displayed
- 원본 도움말: A template describes how content should get displayed, it contains layout and maybe also scripts on how to handle the content
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `cm_template_pkey` | `cm_template_id` |
| UNIQUE | `cm_template_uu_idx` | `cm_template_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `cm_template_id` | Template | numeric(10,0) | 불가 | 예 | — | Template defines how content is displayed |
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
| 12 | `cm_webproject_id` | Web Project | numeric(10,0) | 허용 | — | — | A web project is the main data container for Containers, URLs, Ads, Media etc. |
| 13 | `value` | Search Key | character varying(40) | 불가 | — | — | Search key for the record in the format required - must be unique |
| 14 | `isinclude` | Included | character(1) | 불가 | — | 'Y'::bpchar | Defines whether this content / template is included into another one |
| 15 | `isusead` | Use Ad | character(1) | 불가 | — | 'Y'::bpchar | Whether or not this templates uses Ad's |
| 16 | `isnews` | Uses News | character(1) | 불가 | — | 'Y'::bpchar | Template or container uses news channels |
| 17 | `elements` | Elements | character varying(2000) | 허용 | — | — | Contains list of elements separated by CR |
| 18 | `templatexst` | Template XST | text | 허용 | — | — | Contains the template code itself |
| 19 | `issummary` | Summary Level | character(1) | 불가 | — | 'N'::bpchar | This is a summary entity |
| 20 | `isvalid` | Valid | character(1) | 불가 | — | 'N'::bpchar | Element is valid |
| 21 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 22 | `cm_template_uu` | CM_Template_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["cm_container"]
    n1["cm_cstage"]
    n2["cm_template"]
    n3["cm_template_ad_cat"]
    n4["cm_templatetable"]
    n5["cm_webproject"]
    n2 -->|"cm_webproject_id → cm_webproject_id"| n5
    n0 -->|"cm_template_id → cm_template_id"| n2
    n1 -->|"cm_template_id → cm_template_id"| n2
    n3 -->|"cm_template_id → cm_template_id"| n2
    n4 -->|"cm_template_id → cm_template_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cmwebproject_cmtemplate` <!-- FK_OUT: adempiere.cm_template.cmwebproject_cmtemplate --> | [`cm_template`](cm_template.md) | `cm_webproject_id` | [`cm_webproject`](cm_webproject.md) | `cm_webproject_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cmtemplate_cmcontainer` <!-- FK_IN: adempiere.cm_container.cmtemplate_cmcontainer --> | [`cm_container`](cm_container.md) | `cm_template_id` | [`cm_template`](cm_template.md) | `cm_template_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cmtemplate_cmcstage` <!-- FK_IN: adempiere.cm_cstage.cmtemplate_cmcstage --> | [`cm_cstage`](cm_cstage.md) | `cm_template_id` | [`cm_template`](cm_template.md) | `cm_template_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cmtemplate_cmtemplateadcat` <!-- FK_IN: adempiere.cm_template_ad_cat.cmtemplate_cmtemplateadcat --> | [`cm_template_ad_cat`](cm_template_ad_cat.md) | `cm_template_id` | [`cm_template`](cm_template.md) | `cm_template_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cmtemplate_cmttable` <!-- FK_IN: adempiere.cm_templatetable.cmtemplate_cmttable --> | [`cm_templatetable`](cm_templatetable.md) | `cm_template_id` | [`cm_template`](cm_template.md) | `cm_template_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
