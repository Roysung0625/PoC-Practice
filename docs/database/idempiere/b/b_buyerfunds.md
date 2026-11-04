# b_buyerfunds — 경매 구매자 자금

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.b_buyerfunds` |
| 한국어 논리명(문서용 해석) | 경매 구매자 자금 |
| 원본 논리명 | Buyer Funds |
| 원본 사전 ID | 683 |
| 분류 | `b` — 입찰·토픽·구매자/판매자 연결 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 14 |
| 나가는 FK / 들어오는 FK | 4 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

주제별 입찰에 사용되는 구매자의 자금 내역을 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Buyer Funds for Bids on Topics
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `b_buyerfunds_pkey` | `b_buyerfunds_id` |
| UNIQUE | `b_buyerfunds_uu_idx` | `b_buyerfunds_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `b_buyerfunds_id` | Buyer Funds | numeric(10,0) | 불가 | 예 | — | Buyer Funds for Bids on Topics |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `ad_user_id` | User/Contact | numeric(10,0) | 불가 | — | — | User within the system - Internal or Business Partner Contact |
| 10 | `c_order_id` | Order | numeric(10,0) | 허용 | — | — | Order |
| 11 | `c_payment_id` | Payment | numeric(10,0) | 허용 | — | — | Payment identifier |
| 12 | `committedamt` | Committed Amount | numeric | 불가 | — | 0 | The (legal) commitment amount |
| 13 | `noncommittedamt` | Not Committed Amount | numeric | 불가 | — | 0 | Amount not committed yet |
| 14 | `b_buyerfunds_uu` | B_BuyerFunds_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_user"]
    n1["b_bid"]
    n2["b_buyer"]
    n3["b_buyerfunds"]
    n4["c_order"]
    n5["c_payment"]
    n3 -->|"ad_user_id → ad_user_id"| n0
    n3 -->|"ad_user_id → ad_user_id"| n2
    n3 -->|"c_order_id → c_order_id"| n4
    n3 -->|"c_payment_id → c_payment_id"| n5
    n1 -->|"b_buyerfunds_id → b_buyerfunds_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aduser_bbuyerfunds` <!-- FK_OUT: adempiere.b_buyerfunds.aduser_bbuyerfunds --> | [`b_buyerfunds`](b_buyerfunds.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `bbuyer_bbuyerfunds` <!-- FK_OUT: adempiere.b_buyerfunds.bbuyer_bbuyerfunds --> | [`b_buyerfunds`](b_buyerfunds.md) | `ad_user_id` | [`b_buyer`](b_buyer.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `corder_bbuyersfunds` <!-- FK_OUT: adempiere.b_buyerfunds.corder_bbuyersfunds --> | [`b_buyerfunds`](b_buyerfunds.md) | `c_order_id` | [`c_order`](../c/c_order.md) | `c_order_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpayment_bbuyerfunds` <!-- FK_OUT: adempiere.b_buyerfunds.cpayment_bbuyerfunds --> | [`b_buyerfunds`](b_buyerfunds.md) | `c_payment_id` | [`c_payment`](../c/c_payment.md) | `c_payment_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `bbuyerfunds_bbid` <!-- FK_IN: adempiere.b_bid.bbuyerfunds_bbid --> | [`b_bid`](b_bid.md) | `b_buyerfunds_id` | [`b_buyerfunds`](b_buyerfunds.md) | `b_buyerfunds_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
