# ad_inforelated — 연관 조회 창

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_inforelated` |
| 한국어 논리명(문서용 해석) | 연관 조회 창 |
| 원본 논리명 | Info Related |
| 원본 사전 ID | 200089 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 19 |
| 나가는 FK / 들어오는 FK | 9 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

조회 창 사이의 연관 관계와 연결 열·표시 조건을 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_inforelated_key` | `ad_inforelated_id` |
| UNIQUE | `ad_inforelated_uu_idx` | `ad_inforelated_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_inforelated_id` | Info Related | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | — | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | — | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 11 | `help` | Comment/Help | character varying(2000) | 허용 | — | NULL::character varying | Comment or Hint |
| 12 | `ad_infowindow_id` | Info Window | numeric(10,0) | 불가 | — | — | Info and search/select Window |
| 13 | `seqno` | Sequence | numeric(10,0) | 불가 | — | — | Method of ordering records; lowest number comes first |
| 14 | `relatedinfo_id` | Related Info Window | numeric(10,0) | 불가 | — | (0)::numeric | — |
| 15 | `relatedcolumn_id` | Related Info Column | numeric(10,0) | 불가 | — | (0)::numeric | — |
| 16 | `ad_inforelated_uu` | AD_InfoRelated_UU | uuid | 허용 | — | — | — |
| 17 | `parentrelatedcolumn_id` | Parent Related Column | numeric(10,0) | 허용 | — | NULL::numeric | column in parent info window, link with column in this relate info |
| 18 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 19 | `displaylogic` | Display Logic | character varying(2000) | 허용 | — | NULL::character varying | If the Field is displayed, the result determines if the field is actually displayed |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 10개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_entitytype"]
    n2["ad_infocolumn"]
    n3["ad_inforelated"]
    n4["ad_infowindow"]
    n5["ad_org"]
    n6["ad_user"]
    n7["ad_userdef_info_related"]
    n3 -->|"ad_client_id → ad_client_id"| n0
    n3 -->|"ad_infowindow_id → ad_infowindow_id"| n4
    n3 -->|"ad_org_id → ad_org_id"| n5
    n3 -->|"createdby → ad_user_id"| n6
    n3 -->|"entitytype → entitytype"| n1
    n3 -->|"parentrelatedcolumn_id → ad_infocolumn_id"| n2
    n3 -->|"relatedcolumn_id → ad_infocolumn_id"| n2
    n3 -->|"relatedinfo_id → ad_infowindow_id"| n4
    n3 -->|"updatedby → ad_user_id"| n6
    n7 -->|"ad_inforelated_id → ad_inforelated_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adclient_adinforelated` <!-- FK_OUT: adempiere.ad_inforelated.adclient_adinforelated --> | [`ad_inforelated`](ad_inforelated.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adinfowindow_adinforelated` <!-- FK_OUT: adempiere.ad_inforelated.adinfowindow_adinforelated --> | [`ad_inforelated`](ad_inforelated.md) | `ad_infowindow_id` | [`ad_infowindow`](ad_infowindow.md) | `ad_infowindow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorg_adinforelated` <!-- FK_OUT: adempiere.ad_inforelated.adorg_adinforelated --> | [`ad_inforelated`](ad_inforelated.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `createdby_adinforelated` <!-- FK_OUT: adempiere.ad_inforelated.createdby_adinforelated --> | [`ad_inforelated`](ad_inforelated.md) | `createdby` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entitytype_adinforelated` <!-- FK_OUT: adempiere.ad_inforelated.entitytype_adinforelated --> | [`ad_inforelated`](ad_inforelated.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `parentrelatedcolumn_adinforela` <!-- FK_OUT: adempiere.ad_inforelated.parentrelatedcolumn_adinforela --> | [`ad_inforelated`](ad_inforelated.md) | `parentrelatedcolumn_id` | [`ad_infocolumn`](ad_infocolumn.md) | `ad_infocolumn_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `relatedcolumn_adinforelated` <!-- FK_OUT: adempiere.ad_inforelated.relatedcolumn_adinforelated --> | [`ad_inforelated`](ad_inforelated.md) | `relatedcolumn_id` | [`ad_infocolumn`](ad_infocolumn.md) | `ad_infocolumn_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `relatedinfo_adinforelated` <!-- FK_OUT: adempiere.ad_inforelated.relatedinfo_adinforelated --> | [`ad_inforelated`](ad_inforelated.md) | `relatedinfo_id` | [`ad_infowindow`](ad_infowindow.md) | `ad_infowindow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `updatedby_adinforelated` <!-- FK_OUT: adempiere.ad_inforelated.updatedby_adinforelated --> | [`ad_inforelated`](ad_inforelated.md) | `updatedby` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adinforelated_aduserdefinforel` <!-- FK_IN: adempiere.ad_userdef_info_related.adinforelated_aduserdefinforel --> | [`ad_userdef_info_related`](ad_userdef_info_related.md) | `ad_inforelated_id` | [`ad_inforelated`](ad_inforelated.md) | `ad_inforelated_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
