# k_entry — 지식 항목

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.k_entry` |
| 한국어 논리명(문서용 해석) | 지식 항목 |
| 원본 논리명 | Entry |
| 원본 사전 ID | 612 |
| 분류 | `k` — 지식·분류·문서 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 19 |
| 나가는 FK / 들어오는 FK | 3 / 4 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

지식 관리의 개별 콘텐츠 항목을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Knowledge Entry
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `k_entry_pkey` | `k_entry_id` |
| UNIQUE | `k_entry_uu_idx` | `k_entry_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `k_entry_id` | Entry | numeric(10,0) | 불가 | 예 | — | Knowledge Entry |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `k_topic_id` | Knowledge Topic | numeric(10,0) | 불가 | — | — | Knowledge Topic |
| 11 | `rating` | Rating | numeric(10,0) | 불가 | — | — | Classification or Importance |
| 12 | `ispublic` | Public | character(1) | 불가 | — | 'Y'::bpchar | Public can read entry |
| 13 | `keywords` | Keywords | character varying(255) | 허용 | — | — | List of Keywords - separated by space, comma or semicolon |
| 14 | `k_source_id` | Knowledge Source | numeric(10,0) | 허용 | — | — | Source of a Knowledge Entry |
| 15 | `descriptionurl` | Description URL | character varying(120) | 허용 | — | — | URL for the description |
| 16 | `validto` | Valid to | timestamp without time zone | 허용 | — | — | Valid to including this date (last day) |
| 17 | `ad_session_id` | Session | numeric(10,0) | 허용 | — | — | User Session Online or Web |
| 18 | `textmsg` | Text Message | character varying(2000) | 불가 | — | — | Text Message |
| 19 | `k_entry_uu` | K_Entry_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_session"]
    n1["k_comment"]
    n2["k_entry"]
    n3["k_entrycategory"]
    n4["k_entryrelated"]
    n5["k_source"]
    n6["k_topic"]
    n2 -->|"ad_session_id → ad_session_id"| n0
    n2 -->|"k_source_id → k_source_id"| n5
    n2 -->|"k_topic_id → k_topic_id"| n6
    n1 -->|"k_entry_id → k_entry_id"| n2
    n3 -->|"k_entry_id → k_entry_id"| n2
    n4 -->|"k_entry_id → k_entry_id"| n2
    n4 -->|"k_entryrelated_id → k_entry_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adsession_kentry` <!-- FK_OUT: adempiere.k_entry.adsession_kentry --> | [`k_entry`](k_entry.md) | `ad_session_id` | [`ad_session`](../ad/ad_session.md) | `ad_session_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ksource_kentry` <!-- FK_OUT: adempiere.k_entry.ksource_kentry --> | [`k_entry`](k_entry.md) | `k_source_id` | [`k_source`](k_source.md) | `k_source_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ktopic_kentry` <!-- FK_OUT: adempiere.k_entry.ktopic_kentry --> | [`k_entry`](k_entry.md) | `k_topic_id` | [`k_topic`](k_topic.md) | `k_topic_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `kentry_kcomment` <!-- FK_IN: adempiere.k_comment.kentry_kcomment --> | [`k_comment`](k_comment.md) | `k_entry_id` | [`k_entry`](k_entry.md) | `k_entry_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `kentry_kentrycatalog` <!-- FK_IN: adempiere.k_entrycategory.kentry_kentrycatalog --> | [`k_entrycategory`](k_entrycategory.md) | `k_entry_id` | [`k_entry`](k_entry.md) | `k_entry_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `kentry_kentryrelated` <!-- FK_IN: adempiere.k_entryrelated.kentry_kentryrelated --> | [`k_entryrelated`](k_entryrelated.md) | `k_entry_id` | [`k_entry`](k_entry.md) | `k_entry_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `kentry_kentryrelatedid` <!-- FK_IN: adempiere.k_entryrelated.kentry_kentryrelatedid --> | [`k_entryrelated`](k_entryrelated.md) | `k_entryrelated_id` | [`k_entry`](k_entry.md) | `k_entry_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
