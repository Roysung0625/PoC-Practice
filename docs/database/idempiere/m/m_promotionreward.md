# m_promotionreward — 판매 촉진 혜택

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_promotionreward` |
| 한국어 논리명(문서용 해석) | 판매 촉진 혜택 |
| 원본 논리명 | Promotion Reward |
| 원본 사전 ID | 53182 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 20 |
| 나가는 FK / 들어오는 FK | 4 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

판매 촉진 조건을 충족할 때 제공할 혜택을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Setup reward for the promotion
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_promotionreward_key` | `m_promotionreward_id` |
| UNIQUE | `m_promotionreward_uu_idx` | `m_promotionreward_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | NULL::numeric | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | NULL::numeric | Organizational entity within tenant |
| 3 | `amount` | Amount | numeric | 허용 | — | — | Amount in a defined currency |
| 4 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | — | Additional document charges |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `distributionsorting` | Distribution Sorting | character(1) | 허용 | — | — | Quantity distribution sorting by unit price |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `isforalldistribution` | For all distribution | character(1) | 불가 | — | 'N'::bpchar | This reward is for all distribution |
| 10 | `issamedistribution` | Same distribution for source and target | character(1) | 불가 | — | 'Y'::bpchar | Use the same distribution for source and target |
| 11 | `m_promotiondistribution_id` | Promotion Distribution | numeric(10,0) | 허용 | — | — | — |
| 12 | `m_promotionreward_id` | Promotion Reward | numeric(10,0) | 불가 | 예 | — | — |
| 13 | `m_promotion_id` | Promotion | numeric(10,0) | 불가 | — | — | — |
| 14 | `m_targetdistribution_id` | Target distribution | numeric(10,0) | 허용 | — | — | Get product from target distribution to apply the promotion reward |
| 15 | `qty` | Quantity | numeric | 허용 | — | — | Quantity |
| 16 | `rewardtype` | Reward Type | character(1) | 불가 | — | — | Type of reward which consists of percentage discount, flat discount or absolute amount |
| 17 | `seqno` | Sequence | numeric(10,0) | 불가 | — | NULL::numeric | Method of ordering records; lowest number comes first |
| 18 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 19 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 20 | `m_promotionreward_uu` | M_PromotionReward_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_charge"]
    n1["m_promotion"]
    n2["m_promotiondistribution"]
    n3["m_promotionreward"]
    n3 -->|"c_charge_id → c_charge_id"| n0
    n3 -->|"m_promotion_id → m_promotion_id"| n1
    n3 -->|"m_promotiondistribution_id → m_promotiondistribution_id"| n2
    n3 -->|"m_targetdistribution_id → m_promotiondistribution_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccharge_mpromotionreward` <!-- FK_OUT: adempiere.m_promotionreward.ccharge_mpromotionreward --> | [`m_promotionreward`](m_promotionreward.md) | `c_charge_id` | [`c_charge`](../c/c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpromotion_mpromotionreward` <!-- FK_OUT: adempiere.m_promotionreward.mpromotion_mpromotionreward --> | [`m_promotionreward`](m_promotionreward.md) | `m_promotion_id` | [`m_promotion`](m_promotion.md) | `m_promotion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpromotiondistribution_mpromot` <!-- FK_OUT: adempiere.m_promotionreward.mpromotiondistribution_mpromot --> | [`m_promotionreward`](m_promotionreward.md) | `m_promotiondistribution_id` | [`m_promotiondistribution`](m_promotiondistribution.md) | `m_promotiondistribution_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mtargetdistribution_mpromotion` <!-- FK_OUT: adempiere.m_promotionreward.mtargetdistribution_mpromotion --> | [`m_promotionreward`](m_promotionreward.md) | `m_targetdistribution_id` | [`m_promotiondistribution`](m_promotiondistribution.md) | `m_promotiondistribution_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
