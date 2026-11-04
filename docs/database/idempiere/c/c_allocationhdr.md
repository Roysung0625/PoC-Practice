# c_allocationhdr — 입출금 소거 전표

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_allocationhdr` |
| 한국어 논리명(문서용 해석) | 입출금 소거 전표 |
| 원본 논리명 | Allocation |
| 원본 사전 ID | 735 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 2 |
| 물리 열 수 | 25 |
| 나가는 FK / 들어오는 FK | 3 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

지급·수금과 청구서 사이의 금액 배분 및 소거 처리를 묶는 전표 머리글이다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Payment allocation
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_allocationhdr_pkey` | `c_allocationhdr_id` |
| UNIQUE | `c_allocationhdr_uu_idx` | `c_allocationhdr_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_allocationhdr_id` | Allocation | numeric(10,0) | 불가 | 예 | — | Payment allocation |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `documentno` | Document No | character varying(30) | 불가 | — | — | Document sequence number of the document |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `datetrx` | Transaction Date | timestamp without time zone | 불가 | — | — | Transaction Date |
| 12 | `dateacct` | Account Date | timestamp without time zone | 불가 | — | — | Accounting Date |
| 13 | `c_currency_id` | Currency | numeric(10,0) | 불가 | — | — | The Currency for this record |
| 14 | `approvalamt` | Approval Amount | numeric | 불가 | — | 0 | Document Approval Amount |
| 15 | `ismanual` | Manual | character(1) | 불가 | — | 'N'::bpchar | This is a manual process |
| 16 | `docstatus` | Document Status | character(2) | 불가 | — | — | The current status of the document |
| 17 | `docaction` | Document Action | character(2) | 불가 | — | — | The targeted status of the document |
| 18 | `isapproved` | Approved | character(1) | 불가 | — | 'N'::bpchar | Indicates if this document requires approval |
| 19 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 20 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 21 | `posted` | Posted | character(1) | 불가 | — | 'N'::bpchar | Posting status |
| 22 | `processedon` | Processed On | numeric | 허용 | — | — | The date+time (expressed in decimal format) when the document has been processed |
| 23 | `c_allocationhdr_uu` | C_AllocationHdr_UU | uuid | 허용 | — | — | — |
| 24 | `reversal_id` | Reversal ID | numeric(10,0) | 허용 | — | NULL::numeric | ID of document reversal |
| 25 | `c_doctype_id` | Document Type | numeric(10,0) | 허용 | — | NULL::numeric | Document type or rules |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_allocationhdr"]
    n1["c_allocationline"]
    n2["c_currency"]
    n3["c_doctype"]
    n0 -->|"c_currency_id → c_currency_id"| n2
    n0 -->|"c_doctype_id → c_doctype_id"| n3
    n0 -->|"reversal_id → c_allocationhdr_id"| n0
    n1 -->|"c_allocationhdr_id → c_allocationhdr_id"| n0
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccurrency_callocation` <!-- FK_OUT: adempiere.c_allocationhdr.ccurrency_callocation --> | [`c_allocationhdr`](c_allocationhdr.md) | `c_currency_id` | [`c_currency`](c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_callocationhdr` <!-- FK_OUT: adempiere.c_allocationhdr.cdoctype_callocationhdr --> | [`c_allocationhdr`](c_allocationhdr.md) | `c_doctype_id` | [`c_doctype`](c_doctype.md) | `c_doctype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversal_callocationhdr` <!-- FK_OUT: adempiere.c_allocationhdr.reversal_callocationhdr --> | [`c_allocationhdr`](c_allocationhdr.md) | `reversal_id` | [`c_allocationhdr`](c_allocationhdr.md) | `c_allocationhdr_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `reversal_callocationhdr` <!-- FK_IN: adempiere.c_allocationhdr.reversal_callocationhdr --> | [`c_allocationhdr`](c_allocationhdr.md) | `reversal_id` | [`c_allocationhdr`](c_allocationhdr.md) | `c_allocationhdr_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `callocation_callocationline` <!-- FK_IN: adempiere.c_allocationline.callocation_callocationline --> | [`c_allocationline`](c_allocationline.md) | `c_allocationhdr_id` | [`c_allocationhdr`](c_allocationhdr.md) | `c_allocationhdr_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
