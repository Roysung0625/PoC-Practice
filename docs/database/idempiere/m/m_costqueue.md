# m_costqueue — 선입·후입 원가 대기열

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_costqueue` |
| 한국어 논리명(문서용 해석) | 선입·후입 원가 대기열 |
| 원본 논리명 | Cost Queue |
| 원본 사전 ID | 817 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 5 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

FIFO 또는 LIFO 방식의 원가 계산에 사용하는 원가 대기열을 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: FiFo/LiFo Cost Queue
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_costqueue_pkey` | `m_costqueue_id` |
| UNIQUE | `m_costqueue_uu_idx` | `m_costqueue_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_costqueue_id` | Cost Queue | numeric(10,0) | 불가 | 예 | — | FiFo/LiFo Cost Queue |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `m_costtype_id` | Cost Type | numeric(10,0) | 불가 | — | — | Type of Cost (e.g. Current, Plan, Future) |
| 10 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 불가 | — | — | Rules for accounting |
| 11 | `m_product_id` | Product | numeric(10,0) | 불가 | — | — | Product, Service, Item |
| 12 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 불가 | — | — | Product Attribute Set Instance |
| 13 | `m_costelement_id` | Cost Element | numeric(10,0) | 불가 | — | — | Product Cost Element |
| 14 | `currentcostprice` | Current Cost Price | numeric | 불가 | — | 0 | The currently used cost price |
| 15 | `currentqty` | Current Quantity | numeric | 불가 | — | 0 | Current Quantity |
| 16 | `m_costqueue_uu` | M_CostQueue_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_acctschema"]
    n1["m_attributesetinstance"]
    n2["m_costelement"]
    n3["m_costqueue"]
    n4["m_costtype"]
    n5["m_product"]
    n3 -->|"c_acctschema_id → c_acctschema_id"| n0
    n3 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n1
    n3 -->|"m_costelement_id → m_costelement_id"| n2
    n3 -->|"m_costtype_id → m_costtype_id"| n4
    n3 -->|"m_product_id → m_product_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cacctschema_mcostqueue` <!-- FK_OUT: adempiere.m_costqueue.cacctschema_mcostqueue --> | [`m_costqueue`](m_costqueue.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `masi_mcostqueue` <!-- FK_OUT: adempiere.m_costqueue.masi_mcostqueue --> | [`m_costqueue`](m_costqueue.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcostelement_mcostqueue` <!-- FK_OUT: adempiere.m_costqueue.mcostelement_mcostqueue --> | [`m_costqueue`](m_costqueue.md) | `m_costelement_id` | [`m_costelement`](m_costelement.md) | `m_costelement_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcosttype_mcostqueue` <!-- FK_OUT: adempiere.m_costqueue.mcosttype_mcostqueue --> | [`m_costqueue`](m_costqueue.md) | `m_costtype_id` | [`m_costtype`](m_costtype.md) | `m_costtype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mcostqueue` <!-- FK_OUT: adempiere.m_costqueue.mproduct_mcostqueue --> | [`m_costqueue`](m_costqueue.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
