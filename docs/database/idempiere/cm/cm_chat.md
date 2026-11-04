# cm_chat — 레코드 대화

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.cm_chat` |
| 한국어 논리명(문서용 해석) | 레코드 대화 |
| 원본 논리명 | Chat |
| 원본 사전 ID | 876 |
| 분류 | `cm` — 웹 콘텐츠 관리 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 2 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

대상 테이블과 레코드에 연결되는 대화 공간의 유형·공개 범위·검토 방식을 관리한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `cm_chat_pkey` | `cm_chat_id` |
| UNIQUE | `cm_chat_uu_idx` | `cm_chat_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `cm_chat_record`: `CREATE UNIQUE INDEX cm_chat_record ON adempiere.cm_chat USING btree (ad_table_id, record_id)`
- `cm_chat_record_uu`: `CREATE UNIQUE INDEX cm_chat_record_uu ON adempiere.cm_chat USING btree (record_uu)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `cm_chat_id` | Chat | numeric(10,0) | 불가 | 예 | — | Chat or discussion thread |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `description` | Description | character varying(255) | 불가 | — | — | Optional short description of the record |
| 10 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 11 | `record_id` | Record ID | numeric(10,0) | 허용 | — | — | Direct internal record ID |
| 12 | `confidentialtype` | Confidentiality | character(1) | 불가 | — | — | Type of Confidentiality |
| 13 | `cm_chattype_id` | Chat Type | numeric(10,0) | 허용 | — | — | Type of discussion / chat |
| 14 | `moderationtype` | Moderation Type | character(1) | 허용 | — | — | Type of moderation |
| 15 | `cm_chat_uu` | CM_Chat_UU | uuid | 허용 | — | — | — |
| 16 | `record_uu` | Record UUID | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_table"]
    n1["cm_chat"]
    n2["cm_chatentry"]
    n3["cm_chattype"]
    n4["cm_chatupdate"]
    n1 -->|"ad_table_id → ad_table_id"| n0
    n1 -->|"cm_chattype_id → cm_chattype_id"| n3
    n2 -->|"cm_chat_id → cm_chat_id"| n1
    n4 -->|"cm_chat_id → cm_chat_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adtable_cmchat` <!-- FK_OUT: adempiere.cm_chat.adtable_cmchat --> | [`cm_chat`](cm_chat.md) | `ad_table_id` | [`ad_table`](../ad/ad_table.md) | `ad_table_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cmchattype_cmchat` <!-- FK_OUT: adempiere.cm_chat.cmchattype_cmchat --> | [`cm_chat`](cm_chat.md) | `cm_chattype_id` | [`cm_chattype`](cm_chattype.md) | `cm_chattype_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cmchat_chchatentry` <!-- FK_IN: adempiere.cm_chatentry.cmchat_chchatentry --> | [`cm_chatentry`](cm_chatentry.md) | `cm_chat_id` | [`cm_chat`](cm_chat.md) | `cm_chat_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cmchat_cmchatupdate` <!-- FK_IN: adempiere.cm_chatupdate.cmchat_cmchatupdate --> | [`cm_chatupdate`](cm_chatupdate.md) | `cm_chat_id` | [`cm_chat`](cm_chat.md) | `cm_chat_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `record_id`는 가리키는 테이블이 메타데이터에 따라 달라질 수 있습니다. 물리 FK 목록에 없는 대상은 별도 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
