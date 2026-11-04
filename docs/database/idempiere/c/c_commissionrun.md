# c_commissionrun — 판매 수수료 계산 실행

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_commissionrun` |
| 한국어 논리명(문서용 해석) | 판매 수수료 계산 실행 |
| 원본 논리명 | Commission Run |
| 원본 사전 ID | 436 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 17 |
| 나가는 FK / 들어오는 FK | 2 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

판매 수수료의 계산 실행 단위를 관리하고 계산 금액과 근거 상세를 실행별로 묶는다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Commission Run or Process
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_commissionrun_pkey` | `c_commissionrun_id` |
| UNIQUE | `c_commissionrun_uu_idx` | `c_commissionrun_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_commissionrun_id` | Commission Run | numeric(10,0) | 불가 | 예 | — | Commission Run or Process |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `documentno` | Document No | character varying(30) | 불가 | — | — | Document sequence number of the document |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `c_commission_id` | Commission | numeric(10,0) | 불가 | — | — | Commission |
| 12 | `startdate` | Start Date | timestamp without time zone | 불가 | — | — | First effective day (inclusive) |
| 13 | `grandtotal` | Grand Total | numeric | 불가 | — | 0 | Total amount of document |
| 14 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 15 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 16 | `c_commissionrun_uu` | C_CommissionRun_UU | uuid | 허용 | — | — | — |
| 17 | `c_invoice_id` | Invoice | numeric(10,0) | 허용 | — | NULL::numeric | Invoice Identifier |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 3개 중 3개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_commission"]
    n1["c_commissionamt"]
    n2["c_commissionrun"]
    n3["c_invoice"]
    n2 -->|"c_commission_id → c_commission_id"| n0
    n2 -->|"c_invoice_id → c_invoice_id"| n3
    n1 -->|"c_commissionrun_id → c_commissionrun_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccommission_ccommissionrun` <!-- FK_OUT: adempiere.c_commissionrun.ccommission_ccommissionrun --> | [`c_commissionrun`](c_commissionrun.md) | `c_commission_id` | [`c_commission`](c_commission.md) | `c_commission_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoice_ccommissionrun` <!-- FK_OUT: adempiere.c_commissionrun.cinvoice_ccommissionrun --> | [`c_commissionrun`](c_commissionrun.md) | `c_invoice_id` | [`c_invoice`](c_invoice.md) | `c_invoice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccommentrun_ccommissionamt` <!-- FK_IN: adempiere.c_commissionamt.ccommentrun_ccommissionamt --> | [`c_commissionamt`](c_commissionamt.md) | `c_commissionrun_id` | [`c_commissionrun`](c_commissionrun.md) | `c_commissionrun_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
