# ad_style — 화면 스타일

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_style` |
| 한국어 논리명(문서용 해석) | 화면 스타일 |
| 원본 논리명 | Style |
| 원본 사전 ID | 200207 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 13 |
| 나가는 FK / 들어오는 FK | 1 / 12 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

필드와 라벨에 적용할 CSS 스타일을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: CSS style for field and label
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_style_key` | `ad_style_id` |
| UNIQUE | `ad_style_uu_idx` | `ad_style_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_style_id` | Style | numeric(10,0) | 불가 | 예 | — | CSS style for field and label |
| 4 | `ad_style_uu` | Style | uuid | 불가 | — | — | CSS Style for field and label |
| 5 | `created` | Created | timestamp without time zone | 허용 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 11 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 12 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 13 | `iswrapwithspan` | Wrap With Span | character(1) | 불가 | — | 'N'::bpchar | Wrap content in Span and apply the Style to it. |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 13개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_entitytype"]
    n1["ad_field"]
    n2["ad_infocolumn"]
    n3["ad_label"]
    n4["ad_labelcategory"]
    n5["ad_printformatitem"]
    n6["ad_searchdefinition"]
    n7["ad_statusline"]
    n8["ad_style"]
    n9["ad_styleline"]
    n8 -->|"entitytype → entitytype"| n0
    n1 -->|"ad_fieldstyle_id → ad_style_id"| n8
    n1 -->|"ad_labelstyle_id → ad_style_id"| n8
    n2 -->|"ad_fieldstyle_id → ad_style_id"| n8
    n3 -->|"ad_labelstyle_id → ad_style_id"| n8
    n4 -->|"ad_labelstyle_id → ad_style_id"| n8
    n5 -->|"ad_fieldstyle_id → ad_style_id"| n8
    n6 -->|"ad_style_id → ad_style_id"| n8
    n7 -->|"ad_style_id → ad_style_id"| n8
    n9 -->|"ad_style_id → ad_style_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `entitytype_adstyle` <!-- FK_OUT: adempiere.ad_style.entitytype_adstyle --> | [`ad_style`](ad_style.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adfieldstyle_adfield` <!-- FK_IN: adempiere.ad_field.adfieldstyle_adfield --> | [`ad_field`](ad_field.md) | `ad_fieldstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adlabelstyle_adfield` <!-- FK_IN: adempiere.ad_field.adlabelstyle_adfield --> | [`ad_field`](ad_field.md) | `ad_labelstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfieldstyle_adinfocolumn` <!-- FK_IN: adempiere.ad_infocolumn.adfieldstyle_adinfocolumn --> | [`ad_infocolumn`](ad_infocolumn.md) | `ad_fieldstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adlabelstyle_adlabel` <!-- FK_IN: adempiere.ad_label.adlabelstyle_adlabel --> | [`ad_label`](ad_label.md) | `ad_labelstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adlabelstyle_clabelcategory` <!-- FK_IN: adempiere.ad_labelcategory.adlabelstyle_clabelcategory --> | [`ad_labelcategory`](ad_labelcategory.md) | `ad_labelstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfieldstyle_adprintformatitem` <!-- FK_IN: adempiere.ad_printformatitem.adfieldstyle_adprintformatitem --> | [`ad_printformatitem`](ad_printformatitem.md) | `ad_fieldstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adstyle_adsearchdefinition` <!-- FK_IN: adempiere.ad_searchdefinition.adstyle_adsearchdefinition --> | [`ad_searchdefinition`](ad_searchdefinition.md) | `ad_style_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adstyle_adstatusline` <!-- FK_IN: adempiere.ad_statusline.adstyle_adstatusline --> | [`ad_statusline`](ad_statusline.md) | `ad_style_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adstyle_adstyleline` <!-- FK_IN: adempiere.ad_styleline.adstyle_adstyleline --> | [`ad_styleline`](ad_styleline.md) | `ad_style_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfieldstyle_aduserdeffield` <!-- FK_IN: adempiere.ad_userdef_field.adfieldstyle_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_fieldstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adlabelstyle_aduserdeffield` <!-- FK_IN: adempiere.ad_userdef_field.adlabelstyle_aduserdeffield --> | [`ad_userdef_field`](ad_userdef_field.md) | `ad_labelstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adfieldstyle_aduserdefinfocolu` <!-- FK_IN: adempiere.ad_userdef_info_column.adfieldstyle_aduserdefinfocolu --> | [`ad_userdef_info_column`](ad_userdef_info_column.md) | `ad_fieldstyle_id` | [`ad_style`](ad_style.md) | `ad_style_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
