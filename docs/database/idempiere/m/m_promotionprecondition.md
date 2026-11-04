# m_promotionprecondition — 판매 촉진 사전 조건

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_promotionprecondition` |
| 한국어 논리명(문서용 해석) | 판매 촉진 사전 조건 |
| 원본 논리명 | Promotion Pre Condition |
| 원본 사전 ID | 53180 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 21 |
| 나가는 FK / 들어오는 FK | 6 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

주문에 판매 촉진을 적용하기 전에 충족해야 하는 조건을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Pre condition for promotion
- 원본 도움말: Promotion is applicable to order that satisfy the pre condition
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_promotionprecondition_key` | `m_promotionprecondition_id` |
| UNIQUE | `m_promotionprecondition_uu_idx` | `m_promotionprecondition_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | NULL::numeric | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | NULL::numeric | Organizational entity within tenant |
| 3 | `c_bp_group_id` | Business Partner Group | numeric(10,0) | 허용 | — | — | Business Partner Group |
| 4 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `enddate` | End Date | timestamp without time zone | 허용 | — | — | Last effective date (inclusive) |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `m_pricelist_id` | Price List | numeric(10,0) | 허용 | — | — | Unique identifier of a Price List |
| 10 | `m_promotionprecondition_id` | Promotion Pre Condition | numeric(10,0) | 불가 | 예 | — | — |
| 11 | `m_promotion_id` | Promotion | numeric(10,0) | 불가 | — | — | — |
| 12 | `m_warehouse_id` | Warehouse | numeric(10,0) | 허용 | — | — | Storage Warehouse and Service Point |
| 13 | `promotioncode` | Promotion Code | character varying(30) | 허용 | — | — | User entered promotion code at sales time |
| 14 | `promotioncounter` | Usage Counter | numeric(10,0) | 허용 | — | 0 | Usage counter |
| 15 | `promotionusagelimit` | Usage Limit | numeric(10,0) | 허용 | — | 0 | Maximum usage limit |
| 16 | `seqno` | Sequence | numeric(10,0) | 불가 | — | 0 | Method of ordering records; lowest number comes first |
| 17 | `startdate` | Start Date | timestamp without time zone | 불가 | — | — | First effective day (inclusive) |
| 18 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 19 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 20 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | NULL::numeric | Business Activity |
| 21 | `m_promotionprecondition_uu` | M_PromotionPreCondition_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 6개 중 6개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_activity"]
    n1["c_bp_group"]
    n2["c_bpartner"]
    n3["m_pricelist"]
    n4["m_promotion"]
    n5["m_promotionprecondition"]
    n6["m_warehouse"]
    n5 -->|"c_activity_id → c_activity_id"| n0
    n5 -->|"c_bpartner_id → c_bpartner_id"| n2
    n5 -->|"c_bp_group_id → c_bp_group_id"| n1
    n5 -->|"m_pricelist_id → m_pricelist_id"| n3
    n5 -->|"m_promotion_id → m_promotion_id"| n4
    n5 -->|"m_warehouse_id → m_warehouse_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cactivity_mpromotionpreconditi` <!-- FK_OUT: adempiere.m_promotionprecondition.cactivity_mpromotionpreconditi --> | [`m_promotionprecondition`](m_promotionprecondition.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_mpromotionpreconditi` <!-- FK_OUT: adempiere.m_promotionprecondition.cbpartner_mpromotionpreconditi --> | [`m_promotionprecondition`](m_promotionprecondition.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpgroup_mpromotionpreconditio` <!-- FK_OUT: adempiere.m_promotionprecondition.cbpgroup_mpromotionpreconditio --> | [`m_promotionprecondition`](m_promotionprecondition.md) | `c_bp_group_id` | [`c_bp_group`](../c/c_bp_group.md) | `c_bp_group_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpricelist_mpromotionprecondit` <!-- FK_OUT: adempiere.m_promotionprecondition.mpricelist_mpromotionprecondit --> | [`m_promotionprecondition`](m_promotionprecondition.md) | `m_pricelist_id` | [`m_pricelist`](m_pricelist.md) | `m_pricelist_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpromotion_mpromotionprecondit` <!-- FK_OUT: adempiere.m_promotionprecondition.mpromotion_mpromotionprecondit --> | [`m_promotionprecondition`](m_promotionprecondition.md) | `m_promotion_id` | [`m_promotion`](m_promotion.md) | `m_promotion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_mpromotionprecondit` <!-- FK_OUT: adempiere.m_promotionprecondition.mwarehouse_mpromotionprecondit --> | [`m_promotionprecondition`](m_promotionprecondition.md) | `m_warehouse_id` | [`m_warehouse`](m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
