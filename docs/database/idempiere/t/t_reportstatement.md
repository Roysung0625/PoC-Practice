# t_reportstatement — 계정 명세 보고 자료

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.t_reportstatement` |
| 한국어 논리명(문서용 해석) | 계정 명세 보고 자료 |
| 원본 논리명 | T_ReportStatement |
| 원본 사전 ID | 545 |
| 분류 | `t` — 작업·보고서용 보조 테이블 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 11 |
| 나가는 FK / 들어오는 FK | 1 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

실행 건별 회계 전기의 일자·차대변 금액·잔액·수량을 명세서용으로 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `t_reportstatement_pkey` | `ad_pinstance_id`, `fact_acct_id` |
| UNIQUE | `t_reportstatement_uu_idx` | `t_reportstatement_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_pinstance_id` | Process Instance | numeric(10,0) | 불가 | 예 | — | Instance of the process |
| 2 | `fact_acct_id` | Accounting Fact | numeric(10,0) | 불가 | 예 | — | — |
| 3 | `levelno` | Level no | numeric(10,0) | 불가 | — | — | — |
| 4 | `dateacct` | Account Date | timestamp without time zone | 불가 | — | — | Accounting Date |
| 5 | `name` | Name | character varying(60) | 허용 | — | — | Alphanumeric identifier of the entity |
| 6 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 7 | `amtacctdr` | Accounted Debit | numeric | 허용 | — | 0 | Accounted Debit Amount |
| 8 | `amtacctcr` | Accounted Credit | numeric | 허용 | — | 0 | Accounted Credit Amount |
| 9 | `balance` | Balance | numeric | 허용 | — | 0 | — |
| 10 | `qty` | Quantity | numeric | 허용 | — | 0 | Quantity |
| 11 | `t_reportstatement_uu` | T_ReportStatement_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 1개 중 1개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_pinstance"]
    n1["t_reportstatement"]
    n1 -->|"ad_pinstance_id → ad_pinstance_id"| n0
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adpinstance_treportstatement` <!-- FK_OUT: adempiere.t_reportstatement.adpinstance_treportstatement --> | [`t_reportstatement`](t_reportstatement.md) | `ad_pinstance_id` | [`ad_pinstance`](../ad/ad_pinstance.md) | `ad_pinstance_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
