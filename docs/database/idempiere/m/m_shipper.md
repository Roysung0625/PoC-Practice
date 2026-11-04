# m_shipper — 배송업체·배송 수단

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_shipper` |
| 한국어 논리명(문서용 해석) | 배송업체·배송 수단 |
| 원본 논리명 | Shipper |
| 원본 사전 ID | 253 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 3 |
| 물리 열 수 | 14 |
| 나가는 FK / 들어오는 FK | 3 / 15 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제품을 배송하는 업체 또는 배송 방식을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Method or manner of product delivery
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_shipper_pkey` | `m_shipper_id` |
| UNIQUE | `m_shipper_uu_idx` | `m_shipper_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_shipper_id` | Shipper | numeric(10,0) | 불가 | 예 | — | Method or manner of product delivery |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 10 | `m_shipper_uu` | M_Shipper_UU | uuid | 허용 | — | — | — |
| 11 | `m_shippingprocessor_id` | Shipping Processor | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 12 | `m_shippercfg_id` | Shipper Configuration | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 13 | `createfrom` | Create lines from | character(1) | 허용 | — | NULL::bpchar | Process which will generate a new document lines based on an existing document |
| 14 | `name` | Name | character varying(60) | 불가 | — | NULL::character varying | Alphanumeric identifier of the entity |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 18개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_bpartner"]
    n1["c_order"]
    n2["c_orderline"]
    n3["dd_networkdistributionline"]
    n4["dd_order"]
    n5["dd_orderline"]
    n6["i_movement"]
    n7["i_order"]
    n8["m_shipper"]
    n9["m_shippercfg"]
    n10["m_shippingprocessor"]
    n8 -->|"c_bpartner_id → c_bpartner_id"| n0
    n8 -->|"m_shippercfg_id → m_shippercfg_id"| n9
    n8 -->|"m_shippingprocessor_id → m_shippingprocessor_id"| n10
    n1 -->|"m_shipper_id → m_shipper_id"| n8
    n2 -->|"m_shipper_id → m_shipper_id"| n8
    n3 -->|"m_shipper_id → m_shipper_id"| n8
    n4 -->|"m_shipper_id → m_shipper_id"| n8
    n5 -->|"m_shipper_id → m_shipper_id"| n8
    n6 -->|"m_shipper_id → m_shipper_id"| n8
    n7 -->|"m_shipper_id → m_shipper_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cbpartner_mshipper` <!-- FK_OUT: adempiere.m_shipper.cbpartner_mshipper --> | [`m_shipper`](m_shipper.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshippercfg_mshipper` <!-- FK_OUT: adempiere.m_shipper.mshippercfg_mshipper --> | [`m_shipper`](m_shipper.md) | `m_shippercfg_id` | [`m_shippercfg`](m_shippercfg.md) | `m_shippercfg_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshippingprocessor_mshipper` <!-- FK_OUT: adempiere.m_shipper.mshippingprocessor_mshipper --> | [`m_shipper`](m_shipper.md) | `m_shippingprocessor_id` | [`m_shippingprocessor`](m_shippingprocessor.md) | `m_shippingprocessor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mshipper_corder` <!-- FK_IN: adempiere.c_order.mshipper_corder --> | [`c_order`](../c/c_order.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_corderline` <!-- FK_IN: adempiere.c_orderline.mshipper_corderline --> | [`c_orderline`](../c/c_orderline.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_ddnetworkdistribution` <!-- FK_IN: adempiere.dd_networkdistributionline.mshipper_ddnetworkdistribution --> | [`dd_networkdistributionline`](../dd/dd_networkdistributionline.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_ddorder` <!-- FK_IN: adempiere.dd_order.mshipper_ddorder --> | [`dd_order`](../dd/dd_order.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_ddorderline` <!-- FK_IN: adempiere.dd_orderline.mshipper_ddorderline --> | [`dd_orderline`](../dd/dd_orderline.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_imovement` <!-- FK_IN: adempiere.i_movement.mshipper_imovement --> | [`i_movement`](../i/i_movement.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_iorder` <!-- FK_IN: adempiere.i_order.mshipper_iorder --> | [`i_order`](../i/i_order.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_mfreight` <!-- FK_IN: adempiere.m_freight.mshipper_mfreight --> | [`m_freight`](m_freight.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_minout` <!-- FK_IN: adempiere.m_inout.mshipper_minout --> | [`m_inout`](m_inout.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_mmovement` <!-- FK_IN: adempiere.m_movement.mshipper_mmovement --> | [`m_movement`](m_movement.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_mpackage` <!-- FK_IN: adempiere.m_package.mshipper_mpackage --> | [`m_package`](m_package.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_mshipperlabels` <!-- FK_IN: adempiere.m_shipperlabels.mshipper_mshipperlabels --> | [`m_shipperlabels`](m_shipperlabels.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_mshipperpackaging` <!-- FK_IN: adempiere.m_shipperpackaging.mshipper_mshipperpackaging --> | [`m_shipperpackaging`](m_shipperpackaging.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_mshipperpickuptypes` <!-- FK_IN: adempiere.m_shipperpickuptypes.mshipper_mshipperpickuptypes --> | [`m_shipperpickuptypes`](m_shipperpickuptypes.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_mshippingtransaction` <!-- FK_IN: adempiere.m_shippingtransaction.mshipper_mshippingtransaction --> | [`m_shippingtransaction`](m_shippingtransaction.md) | `m_shipper_id` | [`m_shipper`](m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
