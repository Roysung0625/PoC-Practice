# m_forecastline — 자재 예측행

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_forecastline` |
| 한국어 논리명(문서용 해석) | 자재 예측행 |
| 원본 논리명 | Forecast Line |
| 원본 사전 ID | 722 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 50 |
| 물리 열 수 | 17 |
| 나가는 FK / 들어오는 FK | 5 / 3 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

자재 예측 문서의 개별 행을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Forecast Line
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_forecastline_pkey` | `m_forecastline_id` |
| UNIQUE | `m_forecastline_uu_idx` | `m_forecastline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_forecastline_id` | Forecast Line | numeric(10,0) | 불가 | 예 | — | Forecast Line |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `m_forecast_id` | Forecast | numeric(10,0) | 불가 | — | — | Material Forecast |
| 10 | `c_period_id` | Period | numeric(10,0) | 불가 | — | — | Period of the Calendar |
| 11 | `qty` | Quantity | numeric | 불가 | — | 0 | Quantity |
| 12 | `m_product_id` | Product | numeric(10,0) | 불가 | — | — | Product, Service, Item |
| 13 | `qtycalculated` | Calculated Quantity | numeric | 불가 | — | 0 | Calculated Quantity |
| 14 | `m_warehouse_id` | Warehouse | numeric(10,0) | 불가 | — | — | Storage Warehouse and Service Point |
| 15 | `datepromised` | Date Promised | timestamp without time zone | 불가 | — | — | Date Order was promised |
| 16 | `salesrep_id` | Sales Representative | numeric(10,0) | 허용 | — | — | Sales Representative or Company Agent |
| 17 | `m_forecastline_uu` | M_ForecastLine_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_user"]
    n1["c_period"]
    n2["i_productplanning"]
    n3["m_demanddetail"]
    n4["m_forecast"]
    n5["m_forecastline"]
    n6["m_product"]
    n7["m_warehouse"]
    n8["pp_mrp"]
    n5 -->|"c_period_id → c_period_id"| n1
    n5 -->|"m_forecast_id → m_forecast_id"| n4
    n5 -->|"m_product_id → m_product_id"| n6
    n5 -->|"m_warehouse_id → m_warehouse_id"| n7
    n5 -->|"salesrep_id → ad_user_id"| n0
    n2 -->|"m_forecastline_id → m_forecastline_id"| n5
    n3 -->|"m_forecastline_id → m_forecastline_id"| n5
    n8 -->|"m_forecastline_id → m_forecastline_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cperiod_mforecastline` <!-- FK_OUT: adempiere.m_forecastline.cperiod_mforecastline --> | [`m_forecastline`](m_forecastline.md) | `c_period_id` | [`c_period`](../c/c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mforecast_mforecastline` <!-- FK_OUT: adempiere.m_forecastline.mforecast_mforecastline --> | [`m_forecastline`](m_forecastline.md) | `m_forecast_id` | [`m_forecast`](m_forecast.md) | `m_forecast_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mforecastline` <!-- FK_OUT: adempiere.m_forecastline.mproduct_mforecastline --> | [`m_forecastline`](m_forecastline.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_mforecastline` <!-- FK_OUT: adempiere.m_forecastline.mwarehouse_mforecastline --> | [`m_forecastline`](m_forecastline.md) | `m_warehouse_id` | [`m_warehouse`](m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `salesrep_mforecastline` <!-- FK_OUT: adempiere.m_forecastline.salesrep_mforecastline --> | [`m_forecastline`](m_forecastline.md) | `salesrep_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mforecastline_iproductplanning` <!-- FK_IN: adempiere.i_productplanning.mforecastline_iproductplanning --> | [`i_productplanning`](../i/i_productplanning.md) | `m_forecastline_id` | [`m_forecastline`](m_forecastline.md) | `m_forecastline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mforecastline_mdemanddetail` <!-- FK_IN: adempiere.m_demanddetail.mforecastline_mdemanddetail --> | [`m_demanddetail`](m_demanddetail.md) | `m_forecastline_id` | [`m_forecastline`](m_forecastline.md) | `m_forecastline_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mforecastline_ppmrp` <!-- FK_IN: adempiere.pp_mrp.mforecastline_ppmrp --> | [`pp_mrp`](../pp/pp_mrp.md) | `m_forecastline_id` | [`m_forecastline`](m_forecastline.md) | `m_forecastline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
