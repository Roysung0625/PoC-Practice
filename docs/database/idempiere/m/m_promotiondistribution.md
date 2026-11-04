# m_promotiondistribution — 판매 촉진 수량 배분

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_promotiondistribution` |
| 한국어 논리명(문서용 해석) | 판매 촉진 수량 배분 |
| 원본 논리명 | Promotion Distribution |
| 원본 사전 ID | 53181 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 2 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

혜택 계산을 위해 주문행의 품목을 여러 계산 묶음으로 배분하는 설정을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Distribute order line items into multiple bucket for reward calculation
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_promotiondistribution_key` | `m_promotiondistribution_id` |
| UNIQUE | `m_promotiondistribution_uu_idx` | `m_promotiondistribution_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | NULL::numeric | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | NULL::numeric | Organizational entity within tenant |
| 3 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 4 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 5 | `distributionsorting` | Distribution Sorting | character(1) | 허용 | — | — | Quantity distribution sorting by unit price |
| 6 | `distributiontype` | Distribution Type | character(1) | 불가 | — | — | Type of quantity distribution calculation using comparison qty and order qty as operand |
| 7 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 8 | `m_promotiondistribution_id` | Promotion Distribution | numeric(10,0) | 불가 | 예 | — | — |
| 9 | `m_promotionline_id` | Promotion Line | numeric(10,0) | 불가 | — | — | — |
| 10 | `m_promotion_id` | Promotion | numeric(10,0) | 불가 | — | — | — |
| 11 | `operation` | Operation | character varying(2) | 불가 | — | — | Compare Operation |
| 12 | `qty` | Quantity | numeric | 불가 | — | 0 | Quantity |
| 13 | `seqno` | Sequence | numeric(10,0) | 불가 | — | NULL::numeric | Method of ordering records; lowest number comes first |
| 14 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 15 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 16 | `m_promotiondistribution_uu` | M_PromotionDistribution_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["m_promotion"]
    n1["m_promotiondistribution"]
    n2["m_promotionline"]
    n3["m_promotionreward"]
    n1 -->|"m_promotion_id → m_promotion_id"| n0
    n1 -->|"m_promotionline_id → m_promotionline_id"| n2
    n3 -->|"m_promotiondistribution_id → m_promotiondistribution_id"| n1
    n3 -->|"m_targetdistribution_id → m_promotiondistribution_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mpromotion_mpromotiondistribut` <!-- FK_OUT: adempiere.m_promotiondistribution.mpromotion_mpromotiondistribut --> | [`m_promotiondistribution`](m_promotiondistribution.md) | `m_promotion_id` | [`m_promotion`](m_promotion.md) | `m_promotion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpromotionline_mpromotiondistr` <!-- FK_OUT: adempiere.m_promotiondistribution.mpromotionline_mpromotiondistr --> | [`m_promotiondistribution`](m_promotiondistribution.md) | `m_promotionline_id` | [`m_promotionline`](m_promotionline.md) | `m_promotionline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mpromotiondistribution_mpromot` <!-- FK_IN: adempiere.m_promotionreward.mpromotiondistribution_mpromot --> | [`m_promotionreward`](m_promotionreward.md) | `m_promotiondistribution_id` | [`m_promotiondistribution`](m_promotiondistribution.md) | `m_promotiondistribution_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mtargetdistribution_mpromotion` <!-- FK_IN: adempiere.m_promotionreward.mtargetdistribution_mpromotion --> | [`m_promotionreward`](m_promotionreward.md) | `m_targetdistribution_id` | [`m_promotiondistribution`](m_promotiondistribution.md) | `m_promotiondistribution_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
