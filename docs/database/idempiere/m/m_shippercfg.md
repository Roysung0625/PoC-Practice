# m_shippercfg — 배송업체 구성

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_shippercfg` |
| 한국어 논리명(문서용 해석) | 배송업체 구성 |
| 원본 논리명 | Shipper Configuration |
| 원본 사전 ID | 200047 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 19 |
| 나가는 FK / 들어오는 FK | 1 / 4 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제품 배송 방식에 대한 구성 정의를 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Method or manner of product delivery
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| UNIQUE | `m_shippercfg_uu_idx` | `m_shippercfg_uu` |
| PRIMARY KEY | `x_shipper_key` | `m_shippercfg_id` |
| UNIQUE | `x_shipper_unique_columns` | `ad_client_id`, `ad_org_id`, `name` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 4 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 5 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 6 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 7 | `isinternational` | International | character(1) | 불가 | — | 'N'::bpchar | — |
| 8 | `isonline` | Online Access | character(1) | 불가 | — | 'N'::bpchar | Can be accessed online  |
| 9 | `isresidential` | Residential | character(1) | 불가 | — | 'N'::bpchar | — |
| 10 | `issaturdaydelivery` | Saturday Delivery | character(1) | 불가 | — | 'N'::bpchar | — |
| 11 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 12 | `shippingservicecode` | Service Code | character varying(40) | 허용 | — | NULL::character varying | — |
| 13 | `trackingurl` | Tracking URL | character varying(120) | 허용 | — | NULL::character varying | URL of the shipper to track shipments |
| 14 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 15 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 16 | `m_shippercfg_id` | Shipper Configuration | numeric(10,0) | 불가 | 예 | — | — |
| 17 | `m_shippercfg_uu` | M_ShipperCfg_UU | uuid | 허용 | — | — | — |
| 18 | `m_shippingprocessorcfg_id` | Shipping Processor Configuration | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 19 | `copyfrom` | Copy From | character(1) | 허용 | — | NULL::bpchar | Copy From Record |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["m_shipper"]
    n1["m_shippercfg"]
    n2["m_shipperlabelscfg"]
    n3["m_shipperpackagingcfg"]
    n4["m_shipperpickuptypescfg"]
    n5["m_shippingprocessorcfg"]
    n1 -->|"m_shippingprocessorcfg_id → m_shippingprocessorcfg_id"| n5
    n0 -->|"m_shippercfg_id → m_shippercfg_id"| n1
    n2 -->|"m_shippercfg_id → m_shippercfg_id"| n1
    n3 -->|"m_shippercfg_id → m_shippercfg_id"| n1
    n4 -->|"m_shippercfg_id → m_shippercfg_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mshippingprocessorcfg_mshipper` <!-- FK_OUT: adempiere.m_shippercfg.mshippingprocessorcfg_mshipper --> | [`m_shippercfg`](m_shippercfg.md) | `m_shippingprocessorcfg_id` | [`m_shippingprocessorcfg`](m_shippingprocessorcfg.md) | `m_shippingprocessorcfg_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mshippercfg_mshipper` <!-- FK_IN: adempiere.m_shipper.mshippercfg_mshipper --> | [`m_shipper`](m_shipper.md) | `m_shippercfg_id` | [`m_shippercfg`](m_shippercfg.md) | `m_shippercfg_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshippercfg_mshipperlabelscfg` <!-- FK_IN: adempiere.m_shipperlabelscfg.mshippercfg_mshipperlabelscfg --> | [`m_shipperlabelscfg`](m_shipperlabelscfg.md) | `m_shippercfg_id` | [`m_shippercfg`](m_shippercfg.md) | `m_shippercfg_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshippercfg_mshipperpackagingc` <!-- FK_IN: adempiere.m_shipperpackagingcfg.mshippercfg_mshipperpackagingc --> | [`m_shipperpackagingcfg`](m_shipperpackagingcfg.md) | `m_shippercfg_id` | [`m_shippercfg`](m_shippercfg.md) | `m_shippercfg_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshippercfg_mshipperpickuptype` <!-- FK_IN: adempiere.m_shipperpickuptypescfg.mshippercfg_mshipperpickuptype --> | [`m_shipperpickuptypescfg`](m_shipperpickuptypescfg.md) | `m_shippercfg_id` | [`m_shippercfg`](m_shippercfg.md) | `m_shippercfg_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
