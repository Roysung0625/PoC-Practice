# m_costhistory — 원가 변경 이력

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_costhistory` |
| 한국어 논리명(문서용 해석) | 원가 변경 이력 |
| 원본 논리명 | Cost History |
| 원본 사전 ID | 200001 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 25 |
| 나가는 FK / 들어오는 FK | 5 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제품 원가 테이블의 변동 이력을 기록한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Movement history for M_Cost
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_costhistory_key` | `m_costhistory_id` |
| UNIQUE | `m_costhistory_uu_idx` | `m_costhistory_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 4 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 5 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 6 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 불가 | — | — | Product Attribute Set Instance |
| 7 | `m_costdetail_id` | Cost Detail | numeric(10,0) | 불가 | — | — | Cost Detail Information |
| 8 | `m_costelement_id` | Cost Element | numeric(10,0) | 불가 | — | — | Product Cost Element |
| 9 | `m_costhistory_id` | Cost History | numeric(10,0) | 불가 | 예 | — | Movement history for M_Cost |
| 10 | `m_costhistory_uu` | Cost History UUID | uuid | 불가 | — | — | — |
| 11 | `m_costtype_id` | Cost Type | numeric(10,0) | 불가 | — | — | Type of Cost (e.g. Current, Plan, Future) |
| 12 | `newcamt` | New Accumulated Amt | numeric | 허용 | — | — | Accumulated Amt after processing of M_CostDetail |
| 13 | `newcostprice` | New Cost Price | numeric | 불가 | — | — | New current cost price after processing of M_CostDetail |
| 14 | `newcqty` | New Accumulated Qty | numeric | 허용 | — | — | New Accumulated Qty after processing of M_CostDetail |
| 15 | `newqty` | New Current Quantity | numeric | 불가 | — | — | New current quantity after processing of M_CostDetail |
| 16 | `oldcamt` | Old Accumulated Amt | numeric | 허용 | — | — | Old accumulated amt before the processing of M_CostDetail |
| 17 | `oldcostprice` | Old Current Cost Price | numeric | 불가 | — | — | Old current cost price before the processing of M_CostDetail |
| 18 | `oldcqty` | Old Accumulated Qty | numeric | 허용 | — | — | Old accumulated qty before the processing of M_CostDetail |
| 19 | `oldqty` | Old Current Quantity | numeric | 불가 | — | — | Old current quantity before the processing of M_CostDetail |
| 20 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 21 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 22 | `m_product_id` | Product | numeric(10,0) | 허용 | — | NULL::numeric | Product, Service, Item |
| 23 | `dateacct` | Account Date | timestamp without time zone | 불가 | — | — | Accounting Date |
| 24 | `isbackdate` | Back-Date | character(1) | 불가 | — | 'N'::bpchar | — |
| 25 | `backdateprocessedon` | Back-Date Processed On | timestamp without time zone | 허용 | — | — | The date+time (expressed in decimal format) when the document has been processed |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["m_attributesetinstance"]
    n1["m_costdetail"]
    n2["m_costelement"]
    n3["m_costhistory"]
    n4["m_costtype"]
    n5["m_product"]
    n3 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n0
    n3 -->|"m_costdetail_id → m_costdetail_id"| n1
    n3 -->|"m_costelement_id → m_costelement_id"| n2
    n3 -->|"m_costtype_id → m_costtype_id"| n4
    n3 -->|"m_product_id → m_product_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mattributesetinstance_mcosthis` <!-- FK_OUT: adempiere.m_costhistory.mattributesetinstance_mcosthis --> | [`m_costhistory`](m_costhistory.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcostdetail_mcosthistory` <!-- FK_OUT: adempiere.m_costhistory.mcostdetail_mcosthistory --> | [`m_costhistory`](m_costhistory.md) | `m_costdetail_id` | [`m_costdetail`](m_costdetail.md) | `m_costdetail_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcostelement_mcosthistory` <!-- FK_OUT: adempiere.m_costhistory.mcostelement_mcosthistory --> | [`m_costhistory`](m_costhistory.md) | `m_costelement_id` | [`m_costelement`](m_costelement.md) | `m_costelement_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcosttype_mcosthistory` <!-- FK_OUT: adempiere.m_costhistory.mcosttype_mcosthistory --> | [`m_costhistory`](m_costhistory.md) | `m_costtype_id` | [`m_costtype`](m_costtype.md) | `m_costtype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mcosthistory` <!-- FK_OUT: adempiere.m_costhistory.mproduct_mcosthistory --> | [`m_costhistory`](m_costhistory.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
