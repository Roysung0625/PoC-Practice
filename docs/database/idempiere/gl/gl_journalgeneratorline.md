# gl_journalgeneratorline — 분개 생성 대상 규칙

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.gl_journalgeneratorline` |
| 한국어 논리명(문서용 해석) | 분개 생성 대상 규칙 |
| 원본 논리명 | Generator Line |
| 원본 사전 ID | 200022 |
| 분류 | `gl` — 총계정원장·예산·분개 |
| 전체 테넌트 행 수 | 6 |
| 물리 열 수 | 22 |
| 나가는 FK / 들어오는 FK | 4 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

생성할 차변·대변 계정, 거래처 분석 방식, 금액 배수와 반올림 기준을 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `gl_journalgeneratorline_key` | `gl_journalgeneratorline_id` |
| UNIQUE | `gl_journalgeneratorline_uu_idx` | `gl_journalgeneratorline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `gl_journalgeneratorline_id` | Generator Line | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 5 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 6 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 7 | `help` | Comment/Help | character varying(2000) | 허용 | — | NULL::character varying | Comment or Hint |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `gl_journalgenerator_id` | GL Journal Generator | numeric(10,0) | 불가 | — | — | — |
| 10 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 11 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 12 | `seqno` | Sequence | numeric(10,0) | 불가 | — | — | Method of ordering records; lowest number comes first |
| 13 | `c_elementvaluedr_id` | Account DR | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 14 | `c_elementvaluecr_id` | Account CR | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 15 | `bpdimensiontype` | Type of BP Dimension | character(1) | 허용 | — | NULL::bpchar | — |
| 16 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | NULL::numeric | Identifies a Business Partner |
| 17 | `bpcolumn` | BP Column | character varying(124) | 허용 | — | — | — |
| 18 | `iscopyalldimensions` | Copy All Dimensions | character(1) | 불가 | — | 'N'::bpchar | — |
| 19 | `issameproduct` | Same Product | character(1) | 불가 | — | 'N'::bpchar | — |
| 20 | `amtmultiplier` | Multiplier Amount | numeric | 허용 | — | (1)::numeric | Multiplier Amount for generating commissions |
| 21 | `roundfactor` | Round Factor | numeric(10,0) | 허용 | — | (0)::numeric | — |
| 22 | `gl_journalgeneratorline_uu` | GL_JournalGeneratorLine_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_bpartner"]
    n1["c_elementvalue"]
    n2["gl_journalgenerator"]
    n3["gl_journalgeneratorline"]
    n4["gl_journalgeneratorsource"]
    n3 -->|"c_bpartner_id → c_bpartner_id"| n0
    n3 -->|"c_elementvaluecr_id → c_elementvalue_id"| n1
    n3 -->|"c_elementvaluedr_id → c_elementvalue_id"| n1
    n3 -->|"gl_journalgenerator_id → gl_journalgenerator_id"| n2
    n4 -->|"gl_journalgeneratorline_id → gl_journalgeneratorline_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cbpartner_qssjournalgeneratorl` <!-- FK_OUT: adempiere.gl_journalgeneratorline.cbpartner_qssjournalgeneratorl --> | [`gl_journalgeneratorline`](gl_journalgeneratorline.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvaluecr_qssjournalgene` <!-- FK_OUT: adempiere.gl_journalgeneratorline.celementvaluecr_qssjournalgene --> | [`gl_journalgeneratorline`](gl_journalgeneratorline.md) | `c_elementvaluecr_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvaluedr_qssjournalgene` <!-- FK_OUT: adempiere.gl_journalgeneratorline.celementvaluedr_qssjournalgene --> | [`gl_journalgeneratorline`](gl_journalgeneratorline.md) | `c_elementvaluedr_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `qssjournalgenerator_qssjournal` <!-- FK_OUT: adempiere.gl_journalgeneratorline.qssjournalgenerator_qssjournal --> | [`gl_journalgeneratorline`](gl_journalgeneratorline.md) | `gl_journalgenerator_id` | [`gl_journalgenerator`](gl_journalgenerator.md) | `gl_journalgenerator_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `qssjournalgeneratorline_qssjou` <!-- FK_IN: adempiere.gl_journalgeneratorsource.qssjournalgeneratorline_qssjou --> | [`gl_journalgeneratorsource`](gl_journalgeneratorsource.md) | `gl_journalgeneratorline_id` | [`gl_journalgeneratorline`](gl_journalgeneratorline.md) | `gl_journalgeneratorline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
