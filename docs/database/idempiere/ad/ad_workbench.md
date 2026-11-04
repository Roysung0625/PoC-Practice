# ad_workbench — 작업 공간

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_workbench` |
| 한국어 논리명(문서용 해석) | 작업 공간 |
| 원본 논리명 | Workbench |
| 원본 사전 ID | 468 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 4 / 6 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

창과 보고서를 묶어 작업 공간을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Collection of windows, reports
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_workbench_pkey` | `ad_workbench_id` |
| UNIQUE | `ad_workbench_uu_idx` | `ad_workbench_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_workbench_id` | Workbench | numeric(10,0) | 불가 | 예 | — | Collection of windows, reports |
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
| 12 | `ad_column_id` | Column | numeric(10,0) | 불가 | — | — | Column in the table |
| 13 | `ad_image_id` | Image | numeric(10,0) | 허용 | — | — | Image or Icon |
| 14 | `ad_color_id` | System Color | numeric(10,0) | 허용 | — | — | Color for backgrounds or indicators |
| 15 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 16 | `ad_workbench_uu` | AD_Workbench_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 10개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_color"]
    n1["ad_column"]
    n2["ad_desktopworkbench"]
    n3["ad_entitytype"]
    n4["ad_image"]
    n5["ad_menu"]
    n6["ad_package_exp_common"]
    n7["ad_package_exp_detail"]
    n8["ad_workbench"]
    n9["ad_workbench_trl"]
    n10["ad_workbenchwindow"]
    n8 -->|"ad_color_id → ad_color_id"| n0
    n8 -->|"ad_column_id → ad_column_id"| n1
    n8 -->|"ad_image_id → ad_image_id"| n4
    n8 -->|"entitytype → entitytype"| n3
    n2 -->|"ad_workbench_id → ad_workbench_id"| n8
    n5 -->|"ad_workbench_id → ad_workbench_id"| n8
    n6 -->|"ad_workbench_id → ad_workbench_id"| n8
    n7 -->|"ad_workbench_id → ad_workbench_id"| n8
    n9 -->|"ad_workbench_id → ad_workbench_id"| n8
    n10 -->|"ad_workbench_id → ad_workbench_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adcolor_adworkbench` <!-- FK_OUT: adempiere.ad_workbench.adcolor_adworkbench --> | [`ad_workbench`](ad_workbench.md) | `ad_color_id` | [`ad_color`](ad_color.md) | `ad_color_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adcolumn_adworkbench` <!-- FK_OUT: adempiere.ad_workbench.adcolumn_adworkbench --> | [`ad_workbench`](ad_workbench.md) | `ad_column_id` | [`ad_column`](ad_column.md) | `ad_column_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adimage_adworkbench` <!-- FK_OUT: adempiere.ad_workbench.adimage_adworkbench --> | [`ad_workbench`](ad_workbench.md) | `ad_image_id` | [`ad_image`](ad_image.md) | `ad_image_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adworkbench` <!-- FK_OUT: adempiere.ad_workbench.entityt_adworkbench --> | [`ad_workbench`](ad_workbench.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adworkbench_addesktopwb` <!-- FK_IN: adempiere.ad_desktopworkbench.adworkbench_addesktopwb --> | [`ad_desktopworkbench`](ad_desktopworkbench.md) | `ad_workbench_id` | [`ad_workbench`](ad_workbench.md) | `ad_workbench_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `admenu_adworkbench` <!-- FK_IN: adempiere.ad_menu.admenu_adworkbench --> | [`ad_menu`](ad_menu.md) | `ad_workbench_id` | [`ad_workbench`](ad_workbench.md) | `ad_workbench_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkbench_adpackageexpcommon` <!-- FK_IN: adempiere.ad_package_exp_common.adworkbench_adpackageexpcommon --> | [`ad_package_exp_common`](ad_package_exp_common.md) | `ad_workbench_id` | [`ad_workbench`](ad_workbench.md) | `ad_workbench_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkbench_adpackageexpdetail` <!-- FK_IN: adempiere.ad_package_exp_detail.adworkbench_adpackageexpdetail --> | [`ad_package_exp_detail`](ad_package_exp_detail.md) | `ad_workbench_id` | [`ad_workbench`](ad_workbench.md) | `ad_workbench_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkbench_adworkbenchtrl` <!-- FK_IN: adempiere.ad_workbench_trl.adworkbench_adworkbenchtrl --> | [`ad_workbench_trl`](ad_workbench_trl.md) | `ad_workbench_id` | [`ad_workbench`](ad_workbench.md) | `ad_workbench_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkbench_adworkbenchwindow` <!-- FK_IN: adempiere.ad_workbenchwindow.adworkbench_adworkbenchwindow --> | [`ad_workbenchwindow`](ad_workbenchwindow.md) | `ad_workbench_id` | [`ad_workbench`](ad_workbench.md) | `ad_workbench_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
