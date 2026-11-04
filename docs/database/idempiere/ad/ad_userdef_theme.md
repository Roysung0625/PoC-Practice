# ad_userdef_theme — 사용자 테마 설정

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_userdef_theme` |
| 한국어 논리명(문서용 해석) | 사용자 테마 설정 |
| 원본 논리명 | Theme Customization |
| 원본 사전 ID | 200421 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 15 |
| 나가는 FK / 들어오는 FK | 6 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

역할·사용자별 화면 테마와 스타일시트를 관리한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_userdef_theme_key` | `ad_userdef_theme_id` |
| UNIQUE | `ad_userdef_theme_uu_idx` | `ad_userdef_theme_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_userdef_theme_unique`: `CREATE UNIQUE INDEX ad_userdef_theme_unique ON adempiere.ad_userdef_theme USING btree (theme, ad_client_id, ad_org_id, COALESCE(ad_user_id, (0)::numeric), COALESCE(ad_role_id, (0)::numeric))`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_role_id` | Role | numeric(10,0) | 허용 | — | — | Responsibility Role |
| 4 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | — | User within the system - Internal or Business Partner Contact |
| 5 | `ad_userdef_theme_id` | Theme Customization | numeric(10,0) | 불가 | 예 | — | — |
| 6 | `ad_userdef_theme_uu` | AD_UserDef_Theme_UU | uuid | 허용 | — | — | — |
| 7 | `created` | Created | timestamp without time zone | 불가 | — | — | Date this record was created |
| 8 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 9 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 10 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 11 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 12 | `theme` | Theme | character varying(60) | 불가 | — | — | Theme name |
| 13 | `updated` | Updated | timestamp without time zone | 불가 | — | — | Date this record was updated |
| 14 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 15 | `stylesheet` | Stylesheet | character varying(512) | 허용 | — | — | CSS (Stylesheet) used |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_org"]
    n2["ad_role"]
    n3["ad_user"]
    n4["ad_userdef_theme"]
    n5["ad_userdef_theme_detail"]
    n4 -->|"ad_client_id → ad_client_id"| n0
    n4 -->|"ad_org_id → ad_org_id"| n1
    n4 -->|"ad_role_id → ad_role_id"| n2
    n4 -->|"ad_user_id → ad_user_id"| n3
    n4 -->|"createdby → ad_user_id"| n3
    n4 -->|"updatedby → ad_user_id"| n3
    n5 -->|"ad_userdef_theme_id → ad_userdef_theme_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adclient_aduserdeftheme` <!-- FK_OUT: adempiere.ad_userdef_theme.adclient_aduserdeftheme --> | [`ad_userdef_theme`](ad_userdef_theme.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorg_aduserdeftheme` <!-- FK_OUT: adempiere.ad_userdef_theme.adorg_aduserdeftheme --> | [`ad_userdef_theme`](ad_userdef_theme.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adrole_aduserdeftheme` <!-- FK_OUT: adempiere.ad_userdef_theme.adrole_aduserdeftheme --> | [`ad_userdef_theme`](ad_userdef_theme.md) | `ad_role_id` | [`ad_role`](ad_role.md) | `ad_role_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduser_aduserdeftheme` <!-- FK_OUT: adempiere.ad_userdef_theme.aduser_aduserdeftheme --> | [`ad_userdef_theme`](ad_userdef_theme.md) | `ad_user_id` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `createdby_aduserdeftheme` <!-- FK_OUT: adempiere.ad_userdef_theme.createdby_aduserdeftheme --> | [`ad_userdef_theme`](ad_userdef_theme.md) | `createdby` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `updatedby_aduserdeftheme` <!-- FK_OUT: adempiere.ad_userdef_theme.updatedby_aduserdeftheme --> | [`ad_userdef_theme`](ad_userdef_theme.md) | `updatedby` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aduserdeftheme_aduserdefthemedetail` <!-- FK_IN: adempiere.ad_userdef_theme_detail.aduserdeftheme_aduserdefthemedetail --> | [`ad_userdef_theme_detail`](ad_userdef_theme_detail.md) | `ad_userdef_theme_id` | [`ad_userdef_theme`](ad_userdef_theme.md) | `ad_userdef_theme_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
