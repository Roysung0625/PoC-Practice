# m_edi — 전자문서 교환 거래

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_edi` |
| 한국어 논리명(문서용 해석) | 전자문서 교환 거래 |
| 원본 논리명 | EDI Transaction |
| 원본 사전 ID | 367 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 27 |
| 나가는 FK / 들어오는 FK | 3 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제품 수량·납기·가격에 대한 EDI 요청과 응답 및 송수신 상태를 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_edi_pkey` | `m_edi_id` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `m_edi_trx`: `CREATE UNIQUE INDEX m_edi_trx ON adempiere.m_edi USING btree (c_bp_edi_id, documentno, line)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_edi_id` | EDI Transaction | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_bp_edi_id` | EDI Definition | numeric(10,0) | 불가 | — | — | Electronic Data Interchange |
| 10 | `documentno` | Document No | character varying(30) | 불가 | — | — | Document sequence number of the document |
| 11 | `line` | Line No | numeric(10,0) | 불가 | — | — | Unique line for this document |
| 12 | `trxtype` | Transaction Type | character(1) | 불가 | — | — | Type of credit card transaction |
| 13 | `edistatus` | EDI Status | character(1) | 불가 | — | — | — |
| 14 | `m_warehouse_id` | Warehouse | numeric(10,0) | 불가 | — | — | Storage Warehouse and Service Point |
| 15 | `m_product_id` | Product | numeric(10,0) | 불가 | — | — | Product, Service, Item |
| 16 | `request_qty` | Request Qty | numeric | 불가 | — | 0 | — |
| 17 | `request_shipdate` | Request Ship date | timestamp without time zone | 불가 | — | — | — |
| 18 | `request_price` | Request Price | numeric | 허용 | — | 0 | — |
| 19 | `trxsent` | Transaction sent | timestamp without time zone | 불가 | — | — | — |
| 20 | `trxreceived` | Transaction received | timestamp without time zone | 허용 | — | — | — |
| 21 | `reply_received` | Reply Received | timestamp without time zone | 허용 | — | — | — |
| 22 | `reply_qtyconfirmed` | Reply Qty Confirmed | numeric | 허용 | — | 0 | — |
| 23 | `reply_qtyavailable` | Reply Qty Available | numeric | 허용 | — | 0 | — |
| 24 | `reply_shipdate` | Reply Ship date | timestamp without time zone | 허용 | — | — | — |
| 25 | `reply_price` | Reply Price | numeric | 허용 | — | 0 | Confirmed Price from EDI Partner |
| 26 | `reply_remarks` | Reply Remarks | character varying(2000) | 허용 | — | — | — |
| 27 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_bp_edi"]
    n1["m_edi"]
    n2["m_edi_info"]
    n3["m_product"]
    n4["m_warehouse"]
    n1 -->|"c_bp_edi_id → c_bp_edi_id"| n0
    n1 -->|"m_product_id → m_product_id"| n3
    n1 -->|"m_warehouse_id → m_warehouse_id"| n4
    n2 -->|"m_edi_id → m_edi_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cbpedi_medi` <!-- FK_OUT: adempiere.m_edi.cbpedi_medi --> | [`m_edi`](m_edi.md) | `c_bp_edi_id` | [`c_bp_edi`](../c/c_bp_edi.md) | `c_bp_edi_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_medi` <!-- FK_OUT: adempiere.m_edi.mproduct_medi --> | [`m_edi`](m_edi.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_medi` <!-- FK_OUT: adempiere.m_edi.mwarehouse_medi --> | [`m_edi`](m_edi.md) | `m_warehouse_id` | [`m_warehouse`](m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `medi_ediinfo` <!-- FK_IN: adempiere.m_edi_info.medi_ediinfo --> | [`m_edi_info`](m_edi_info.md) | `m_edi_id` | [`m_edi`](m_edi.md) | `m_edi_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
