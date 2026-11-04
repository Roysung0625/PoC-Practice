# c_commissionline — 판매 수수료 세부 규칙

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_commissionline` |
| 한국어 논리명(문서용 해석) | 판매 수수료 세부 규칙 |
| 원본 논리명 | Commission Line |
| 원본 사전 ID | 431 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 25 |
| 나가는 FK / 들어오는 FK | 7 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

상품·거래처·영업지역 등의 적용 범위와 금액·수량의 차감값 및 배수를 지정한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Commission Line
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_commissionline_pkey` | `c_commissionline_id` |
| UNIQUE | `c_commissionline_uu_idx` | `c_commissionline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_commissionline_id` | Commission Line | numeric(10,0) | 불가 | 예 | — | Commission Line |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_commission_id` | Commission | numeric(10,0) | 불가 | — | — | Commission |
| 10 | `line` | Line No | numeric(10,0) | 불가 | — | — | Unique line for this document |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `amtsubtract` | Subtract Amount | numeric | 불가 | — | — | Subtract Amount for generating commissions |
| 13 | `amtmultiplier` | Multiplier Amount | numeric | 불가 | — | — | Multiplier Amount for generating commissions |
| 14 | `qtysubtract` | Subtract Quantity | numeric | 불가 | — | — | Quantity to subtract when generating commissions |
| 15 | `qtymultiplier` | Multiplier Quantity | numeric | 불가 | — | — | Value to multiply quantities by for generating commissions. |
| 16 | `ispositiveonly` | Positive only | character(1) | 불가 | — | 'Y'::bpchar | Do not generate negative commissions |
| 17 | `commissionorders` | Commission only specified Orders | character(1) | 불가 | — | 'N'::bpchar | Commission only Orders or Invoices, where this Sales Rep is entered |
| 18 | `org_id` | Organization | numeric(10,0) | 허용 | — | — | Organizational entity within tenant |
| 19 | `m_product_category_id` | Product Category | numeric(10,0) | 허용 | — | — | Category of a Product |
| 20 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 21 | `c_bp_group_id` | Business Partner Group | numeric(10,0) | 허용 | — | — | Business Partner Group |
| 22 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 23 | `c_salesregion_id` | Sales Region | numeric(10,0) | 허용 | — | — | Sales coverage region |
| 24 | `paymentrule` | Payment Rule | character varying(1) | 허용 | — | — | How you pay the invoice |
| 25 | `c_commissionline_uu` | C_CommissionLine_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_org"]
    n1["c_bp_group"]
    n2["c_bpartner"]
    n3["c_commission"]
    n4["c_commissionamt"]
    n5["c_commissionline"]
    n6["c_salesregion"]
    n7["m_product"]
    n8["m_product_category"]
    n5 -->|"org_id → ad_org_id"| n0
    n5 -->|"c_bpartner_id → c_bpartner_id"| n2
    n5 -->|"c_bp_group_id → c_bp_group_id"| n1
    n5 -->|"c_commission_id → c_commission_id"| n3
    n5 -->|"c_salesregion_id → c_salesregion_id"| n6
    n5 -->|"m_product_id → m_product_id"| n7
    n5 -->|"m_product_category_id → m_product_category_id"| n8
    n4 -->|"c_commissionline_id → c_commissionline_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adorgtrx_ccommissionline` <!-- FK_OUT: adempiere.c_commissionline.adorgtrx_ccommissionline --> | [`c_commissionline`](c_commissionline.md) | `org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_ccommissionline` <!-- FK_OUT: adempiere.c_commissionline.cbpartner_ccommissionline --> | [`c_commissionline`](c_commissionline.md) | `c_bpartner_id` | [`c_bpartner`](c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpgroup_commissionline` <!-- FK_OUT: adempiere.c_commissionline.cbpgroup_commissionline --> | [`c_commissionline`](c_commissionline.md) | `c_bp_group_id` | [`c_bp_group`](c_bp_group.md) | `c_bp_group_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccommission_ccommissionline` <!-- FK_OUT: adempiere.c_commissionline.ccommission_ccommissionline --> | [`c_commissionline`](c_commissionline.md) | `c_commission_id` | [`c_commission`](c_commission.md) | `c_commission_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_ccommissionline` <!-- FK_OUT: adempiere.c_commissionline.csalesregion_ccommissionline --> | [`c_commissionline`](c_commissionline.md) | `c_salesregion_id` | [`c_salesregion`](c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_ccommissionline` <!-- FK_OUT: adempiere.c_commissionline.mproduct_ccommissionline --> | [`c_commissionline`](c_commissionline.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductcat_ccommissionline` <!-- FK_OUT: adempiere.c_commissionline.mproductcat_ccommissionline --> | [`c_commissionline`](c_commissionline.md) | `m_product_category_id` | [`m_product_category`](../m/m_product_category.md) | `m_product_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccomline_ccomamt` <!-- FK_IN: adempiere.c_commissionamt.ccomline_ccomamt --> | [`c_commissionamt`](c_commissionamt.md) | `c_commissionline_id` | [`c_commissionline`](c_commissionline.md) | `c_commissionline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
