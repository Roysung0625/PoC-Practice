# cm_media_server — 미디어 서버

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.cm_media_server` |
| 한국어 논리명(문서용 해석) | 미디어 서버 |
| 원본 논리명 | Media Server |
| 원본 사전 ID | 859 |
| 분류 | `cm` — 웹 콘텐츠 관리 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 19 |
| 나가는 FK / 들어오는 FK | 1 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

미디어 전송 대상 서버 목록을 관리하며 정적 서버에 미디어를 배치하는 구성에 사용한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Media Server list to which content should get transfered
- 원본 도움말: For performance optimization we save media content on static servers
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `cm_media_server_pkey` | `cm_media_server_id` |
| UNIQUE | `cm_media_server_uu_idx` | `cm_media_server_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `cm_media_server_id` | Media Server | numeric(10,0) | 불가 | 예 | — | Media Server list to which content should get transferred |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 5 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 6 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 7 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 12 | `cm_webproject_id` | Web Project | numeric(10,0) | 불가 | — | — | A web project is the main data container for Containers, URLs, Ads, Media etc. |
| 13 | `ispassive` | Transfer passive | character(1) | 불가 | — | 'Y'::bpchar | FTP passive transfer |
| 14 | `url` | URL | character varying(120) | 허용 | — | — | Full URL address - e.g. http://www.idempiere.org |
| 15 | `ip_address` | IP Address | character varying(20) | 허용 | — | — | Defines the IP address to transfer data to |
| 16 | `username` | User Name | character varying(40) | 허용 | — | — | — |
| 17 | `password` | Password | character varying(40) | 허용 | — | — | Password of any length (case sensitive) |
| 18 | `folder` | Folder | character varying(60) | 허용 | — | — | A folder on a local or remote system to store data into |
| 19 | `cm_media_server_uu` | CM_Media_Server_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 2개 중 2개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["cm_media_server"]
    n1["cm_mediadeploy"]
    n2["cm_webproject"]
    n0 -->|"cm_webproject_id → cm_webproject_id"| n2
    n1 -->|"cm_media_server_id → cm_media_server_id"| n0
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cmwebproject_cmmediaserver` <!-- FK_OUT: adempiere.cm_media_server.cmwebproject_cmmediaserver --> | [`cm_media_server`](cm_media_server.md) | `cm_webproject_id` | [`cm_webproject`](cm_webproject.md) | `cm_webproject_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cmmediaserver_cmmediadeploy` <!-- FK_IN: adempiere.cm_mediadeploy.cmmediaserver_cmmediadeploy --> | [`cm_mediadeploy`](cm_mediadeploy.md) | `cm_media_server_id` | [`cm_media_server`](cm_media_server.md) | `cm_media_server_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
