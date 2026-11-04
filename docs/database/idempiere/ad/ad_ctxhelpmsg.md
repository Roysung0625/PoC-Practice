# ad_ctxhelpmsg — 문맥 도움말 메시지

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_ctxhelpmsg` |
| 한국어 논리명(문서용 해석) | 문맥 도움말 메시지 |
| 원본 논리명 | Context Help Message |
| 원본 사전 ID | 200064 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 12 |
| 나가는 FK / 들어오는 FK | 1 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

문맥 도움말에 속한 메시지를 줄 순서별로 관리한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_ctxhelpmsg_key` | `ad_ctxhelpmsg_id` |
| UNIQUE | `ad_ctxhelpmsg_uu_idx` | `ad_ctxhelpmsg_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_ctxhelpmsg_limit`: `CREATE UNIQUE INDEX ad_ctxhelpmsg_limit ON adempiere.ad_ctxhelpmsg USING btree (ad_ctxhelp_id, ad_client_id, ad_org_id)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_ctxhelp_id` | Context Help | numeric(10,0) | 불가 | — | — | — |
| 3 | `ad_ctxhelpmsg_id` | Context Help Message | numeric(10,0) | 불가 | 예 | — | — |
| 4 | `ad_ctxhelpmsg_uu` | AD_CtxHelpMsg_UU | uuid | 허용 | — | — | — |
| 5 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `line` | — | numeric(10,0) | 허용 | — | — | — |
| 10 | `msgtext` | Message Text | character varying(2000) | 불가 | — | — | Textual Informational, Menu or Error Message |
| 11 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 12 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 3개 중 3개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_ctxhelp"]
    n1["ad_ctxhelpmsg"]
    n2["ad_ctxhelpmsg_trl"]
    n3["ad_ctxhelpsuggestion"]
    n1 -->|"ad_ctxhelp_id → ad_ctxhelp_id"| n0
    n2 -->|"ad_ctxhelpmsg_id → ad_ctxhelpmsg_id"| n1
    n3 -->|"ad_ctxhelpmsg_id → ad_ctxhelpmsg_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adctxhelp_adctxhelpmsg` <!-- FK_OUT: adempiere.ad_ctxhelpmsg.adctxhelp_adctxhelpmsg --> | [`ad_ctxhelpmsg`](ad_ctxhelpmsg.md) | `ad_ctxhelp_id` | [`ad_ctxhelp`](ad_ctxhelp.md) | `ad_ctxhelp_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adctxhelpmsg_adctxhelpmsgtrl` <!-- FK_IN: adempiere.ad_ctxhelpmsg_trl.adctxhelpmsg_adctxhelpmsgtrl --> | [`ad_ctxhelpmsg_trl`](ad_ctxhelpmsg_trl.md) | `ad_ctxhelpmsg_id` | [`ad_ctxhelpmsg`](ad_ctxhelpmsg.md) | `ad_ctxhelpmsg_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adctxhelpmsg_adctxhelpsuggesti` <!-- FK_IN: adempiere.ad_ctxhelpsuggestion.adctxhelpmsg_adctxhelpsuggesti --> | [`ad_ctxhelpsuggestion`](ad_ctxhelpsuggestion.md) | `ad_ctxhelpmsg_id` | [`ad_ctxhelpmsg`](ad_ctxhelpmsg.md) | `ad_ctxhelpmsg_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
