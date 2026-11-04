# ad_color — 시스템 색상

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_color` |
| 한국어 논리명(문서용 해석) | 시스템 색상 |
| 원본 논리명 | System Color |
| 원본 사전 ID | 457 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 26 |
| 나가는 FK / 들어오는 FK | 1 / 4 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

배경이나 상태 표시 등에 사용할 색상을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Color for backgrounds or indicators
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_color_pkey` | `ad_color_id` |
| UNIQUE | `ad_color_uu_idx` | `ad_color_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_color_id` | System Color | numeric(10,0) | 불가 | 예 | — | Color for backgrounds or indicators |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `isdefault` | Default | character(1) | 불가 | — | 'N'::bpchar | Default value |
| 11 | `colortype` | Color Type | character(1) | 불가 | — | — | Color presentation for this color |
| 12 | `red` | Red | numeric(10,0) | 불가 | — | — | RGB value |
| 13 | `green` | Green | numeric(10,0) | 불가 | — | — | RGB value  |
| 14 | `blue` | Blue | numeric(10,0) | 불가 | — | — | Color RGB blue value |
| 15 | `alpha` | Alpha | numeric(10,0) | 불가 | — | — | Color Alpha value 0-255 |
| 16 | `ad_image_id` | Image | numeric(10,0) | 허용 | — | — | Image or Icon |
| 17 | `imagealpha` | Image Alpha | numeric | 불가 | — | — | Image Texture Composite Alpha |
| 18 | `red_1` | 2nd Red | numeric(10,0) | 허용 | — | — | RGB value for second color |
| 19 | `green_1` | 2nd Green | numeric(10,0) | 허용 | — | — | RGB value for second color |
| 20 | `blue_1` | 2nd Blue | numeric(10,0) | 허용 | — | — | RGB value for second color |
| 21 | `alpha_1` | 2nd Alpha | numeric(10,0) | 허용 | — | — | Alpha value for second color |
| 22 | `linewidth` | Line Width | numeric(10,0) | 허용 | — | — | Width of the lines |
| 23 | `linedistance` | Line Distance | numeric(10,0) | 허용 | — | — | Distance between lines |
| 24 | `startpoint` | Start Point | numeric(10,0) | 허용 | — | — | Start point of the gradient colors |
| 25 | `repeatdistance` | Repeat Distance | numeric(10,0) | 허용 | — | — | Distance in points to repeat gradient color - or zero |
| 26 | `ad_color_uu` | AD_Color_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_color"]
    n1["ad_color_trl"]
    n2["ad_desktop"]
    n3["ad_image"]
    n4["ad_window"]
    n5["ad_workbench"]
    n0 -->|"ad_image_id → ad_image_id"| n3
    n1 -->|"ad_color_id → ad_color_id"| n0
    n2 -->|"ad_color_id → ad_color_id"| n0
    n4 -->|"ad_color_id → ad_color_id"| n0
    n5 -->|"ad_color_id → ad_color_id"| n0
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adimage_adcolor` <!-- FK_OUT: adempiere.ad_color.adimage_adcolor --> | [`ad_color`](ad_color.md) | `ad_image_id` | [`ad_image`](ad_image.md) | `ad_image_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adcolor_adcolortrl` <!-- FK_IN: adempiere.ad_color_trl.adcolor_adcolortrl --> | [`ad_color_trl`](ad_color_trl.md) | `ad_color_id` | [`ad_color`](ad_color.md) | `ad_color_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adcolor_addesktop` <!-- FK_IN: adempiere.ad_desktop.adcolor_addesktop --> | [`ad_desktop`](ad_desktop.md) | `ad_color_id` | [`ad_color`](ad_color.md) | `ad_color_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adcolor_adwindow` <!-- FK_IN: adempiere.ad_window.adcolor_adwindow --> | [`ad_window`](ad_window.md) | `ad_color_id` | [`ad_color`](ad_color.md) | `ad_color_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adcolor_adworkbench` <!-- FK_IN: adempiere.ad_workbench.adcolor_adworkbench --> | [`ad_workbench`](ad_workbench.md) | `ad_color_id` | [`ad_color`](ad_color.md) | `ad_color_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
