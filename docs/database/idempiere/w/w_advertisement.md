# w_advertisement — 웹 광고

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.w_advertisement` |
| 한국어 논리명(문서용 해석) | 웹 광고 |
| 원본 논리명 | Advertisement |
| 원본 사전 ID | 579 |
| 분류 | `w` — 웹 상점·카운터 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 28 |
| 나가는 FK / 들어오는 FK | 4 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

웹에 게시하는 광고 정보를 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Web Advertisement
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `w_advertisement_pkey` | `w_advertisement_id` |
| UNIQUE | `w_advertisement_uu_idx` | `w_advertisement_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `w_advertisement_id` | Advertisement | numeric(10,0) | 불가 | 예 | — | Web Advertisement |
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
| 12 | `isselfservice` | Self-Service | character(1) | 불가 | — | 'N'::bpchar | This is a Self-Service entry or this entry can be changed via Self-Service |
| 13 | `c_bpartner_id` | Business Partner | numeric(10,0) | 불가 | — | — | Identifies a Business Partner |
| 14 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | — | User within the system - Internal or Business Partner Contact |
| 15 | `w_clickcount_id` | Click Count | numeric(10,0) | 허용 | — | — | Web Click Management |
| 16 | `w_countercount_id` | Counter Count | numeric(10,0) | 허용 | — | — | Web Counter Count Management |
| 17 | `validfrom` | Valid from | timestamp without time zone | 허용 | — | — | Valid from including this date (first day) |
| 18 | `validto` | Valid to | timestamp without time zone | 허용 | — | — | Valid to including this date (last day) |
| 19 | `imageurl` | Image URL | character varying(120) | 허용 | — | — | URL of  image |
| 20 | `adtext` | Advertisement Text | character varying(2000) | 허용 | — | — | Text of the Advertisement |
| 21 | `webparam1` | Web Parameter 1 | character varying(2000) | 허용 | — | — | Web Site Parameter 1 (default: header image) |
| 22 | `webparam2` | Web Parameter 2 | character varying(2000) | 허용 | — | — | Web Site Parameter 2 (default index page) |
| 23 | `webparam3` | Web Parameter 3 | character varying(2000) | 허용 | — | — | Web Site Parameter 3 (default left - menu) |
| 24 | `webparam4` | Web Parameter 4 | character varying(2000) | 허용 | — | — | Web Site Parameter 4 (default footer left) |
| 25 | `publishstatus` | Publication Status | character(1) | 불가 | — | — | Status of Publication |
| 26 | `version` | Version | numeric(10,0) | 허용 | — | — | Version of the table definition |
| 27 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 28 | `w_advertisement_uu` | W_Advertisement_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_user"]
    n1["c_bpartner"]
    n2["w_advertisement"]
    n3["w_clickcount"]
    n4["w_countercount"]
    n2 -->|"ad_user_id → ad_user_id"| n0
    n2 -->|"c_bpartner_id → c_bpartner_id"| n1
    n2 -->|"w_clickcount_id → w_clickcount_id"| n3
    n2 -->|"w_countercount_id → w_countercount_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aduser_wadvertisement` <!-- FK_OUT: adempiere.w_advertisement.aduser_wadvertisement --> | [`w_advertisement`](w_advertisement.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_wadvertisement` <!-- FK_OUT: adempiere.w_advertisement.cbpartner_wadvertisement --> | [`w_advertisement`](w_advertisement.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `wclickcount_wadvertisement` <!-- FK_OUT: adempiere.w_advertisement.wclickcount_wadvertisement --> | [`w_advertisement`](w_advertisement.md) | `w_clickcount_id` | [`w_clickcount`](w_clickcount.md) | `w_clickcount_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `wcountercount_wadvertisement` <!-- FK_OUT: adempiere.w_advertisement.wcountercount_wadvertisement --> | [`w_advertisement`](w_advertisement.md) | `w_countercount_id` | [`w_countercount`](w_countercount.md) | `w_countercount_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
