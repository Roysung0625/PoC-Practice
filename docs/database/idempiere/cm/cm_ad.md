# cm_ad — 웹 광고

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.cm_ad` |
| 한국어 논리명(문서용 해석) | 웹 광고 |
| 원본 논리명 | Advertisement |
| 원본 사전 ID | 858 |
| 분류 | `cm` — 웹 콘텐츠 관리 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 26 |
| 나가는 FK / 들어오는 FK | 2 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

배너·제휴 정보·후원 링크 등 웹에 표시할 광고를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: An Advertisement is something like a banner
- 원본 도움말: You could use banner, partner infos, sponsored links etc. as an advertisement
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `cm_ad_pkey` | `cm_ad_id` |
| UNIQUE | `cm_ad_uu_idx` | `cm_ad_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `cm_ad_id` | Advertisement | numeric(10,0) | 불가 | 예 | — | An Advertisement is something like a banner |
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
| 12 | `cm_ad_cat_id` | Advertisement Category | numeric(10,0) | 불가 | — | — | Advertisement Category like Banner Homepage  |
| 13 | `cm_media_id` | Media Item | numeric(10,0) | 불가 | — | — | Contains media content like images, flash movies etc. |
| 14 | `targeturl` | Target URL | character varying(120) | 허용 | — | — | URL for the Target |
| 15 | `target_frame` | Target Frame | character varying(20) | 불가 | — | — | Which target should be used if user clicks? |
| 16 | `actualclick` | Actual Click Count | numeric(10,0) | 불가 | — | 0 | How many clicks have been counted |
| 17 | `maxclick` | Max Click Count | numeric(10,0) | 불가 | — | 0 | Maximum Click Count until banner is deactivated |
| 18 | `actualimpression` | Actual Impression Count | numeric(10,0) | 불가 | — | 0 | How many impressions have been counted |
| 19 | `maximpression` | Max Impression Count | numeric(10,0) | 불가 | — | 0 | Maximum Impression Count until banner is deactivated |
| 20 | `startimpression` | Start Count Impression | numeric(10,0) | 불가 | — | 0 | For rotation we need a start count |
| 21 | `startdate` | Start Date | timestamp without time zone | 불가 | — | — | First effective day (inclusive) |
| 22 | `enddate` | End Date | timestamp without time zone | 허용 | — | — | Last effective date (inclusive) |
| 23 | `contenthtml` | Content HTML | character varying(2000) | 허용 | — | — | Contains the content itself |
| 24 | `isadflag` | Special AD Flag | character(1) | 불가 | — | 'Y'::bpchar | Do we need to specially mention this ad? |
| 25 | `islogged` | Logging | character(1) | 불가 | — | 'Y'::bpchar | Do we need to log the banner impressions and clicks? (needs much performance) |
| 26 | `cm_ad_uu` | CM_Ad_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 2개 중 2개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["cm_ad"]
    n1["cm_ad_cat"]
    n2["cm_media"]
    n0 -->|"cm_ad_cat_id → cm_ad_cat_id"| n1
    n0 -->|"cm_media_id → cm_media_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cmadcat_cmad` <!-- FK_OUT: adempiere.cm_ad.cmadcat_cmad --> | [`cm_ad`](cm_ad.md) | `cm_ad_cat_id` | [`cm_ad_cat`](cm_ad_cat.md) | `cm_ad_cat_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cmmedia_cmad` <!-- FK_OUT: adempiere.cm_ad.cmmedia_cmad --> | [`cm_ad`](cm_ad.md) | `cm_media_id` | [`cm_media`](cm_media.md) | `cm_media_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
