# i_pricelist — 가격표 가져오기

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.i_pricelist` |
| 한국어 논리명(문서용 해석) | 가격표 가져오기 |
| 원본 논리명 | Import Price List |
| 원본 사전 ID | 53173 |
| 분류 | `i` — 데이터 가져오기 준비 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 34 |
| 나가는 FK / 들어오는 FK | 6 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

가격표 및 그 버전을 외부 데이터에서 가져오기 위한 중간 데이터를 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Import Price List and Versions
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `i_pricelist_key` | `i_pricelist_id` |
| UNIQUE | `i_pricelist_uu_idx` | `i_pricelist_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 허용 | — | NULL::numeric | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 허용 | — | NULL::numeric | Organizational entity within tenant |
| 3 | `bpartner_value` | Business Partner Key | character varying(40) | 허용 | — | — | The Key of the Business Partner |
| 4 | `breakvalue` | Break Value | numeric | 허용 | — | — | Low Value of trade discount break level |
| 5 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 6 | `c_currency_id` | Currency | numeric(10,0) | 허용 | — | — | The Currency for this record |
| 7 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 8 | `createdby` | Created By | numeric(10,0) | 허용 | — | — | User who created this records |
| 9 | `c_uom_id` | UOM | numeric(10,0) | 허용 | — | — | Unit of Measure |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `enforcepricelimit` | Enforce price limit | character(1) | 허용 | — | — | Do not allow prices below the limit price |
| 12 | `i_errormsg` | Import Error Message | character varying(2000) | 허용 | — | — | Messages generated from import process |
| 13 | `i_isimported` | Imported | character(1) | 불가 | — | 'N'::bpchar | Has this import been processed |
| 14 | `i_pricelist_id` | Import Price List | numeric(10,0) | 불가 | 예 | — | — |
| 15 | `isactive` | Active | character(1) | 허용 | — | 'Y'::bpchar | The record is active in the system |
| 16 | `iso_code` | ISO Currency Code | character varying(3) | 허용 | — | — | Three letter ISO 4217 Code of the Currency |
| 17 | `issopricelist` | Sales Price list | character(1) | 허용 | — | — | This is a Sales Price List |
| 18 | `istaxincluded` | Price includes Tax | character(1) | 허용 | — | — | Tax is included in the price  |
| 19 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 20 | `name` | Name | character varying(60) | 허용 | — | — | Alphanumeric identifier of the entity |
| 21 | `pricelimit` | Limit Price | numeric | 허용 | — | — | Lowest price for a product |
| 22 | `pricelist` | List Price | numeric | 허용 | — | — | List Price |
| 23 | `priceprecision` | Price Precision | numeric | 허용 | — | — | Precision (number of decimals) for the Price |
| 24 | `pricestd` | Standard Price | numeric | 허용 | — | — | Standard Price |
| 25 | `processed` | Processed | character(1) | 허용 | — | 'N'::bpchar | The document has been processed |
| 26 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 27 | `productvalue` | Product Key | character varying(40) | 허용 | — | — | Key of the Product |
| 28 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 29 | `updatedby` | Updated By | numeric(10,0) | 허용 | — | — | User who updated this records |
| 30 | `validfrom` | Valid from | timestamp without time zone | 허용 | — | — | Valid from including this date (first day) |
| 31 | `x12de355` | UOM Code | character varying(4) | 허용 | — | — | UOM EDI X12 Code |
| 32 | `m_pricelist_id` | Price List | numeric(10,0) | 허용 | — | — | Unique identifier of a Price List |
| 33 | `m_pricelist_version_id` | Price List Version | numeric(10,0) | 허용 | — | — | Identifies a unique instance of a Price List |
| 34 | `i_pricelist_uu` | I_PriceList_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 6개 중 6개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_bpartner"]
    n1["c_currency"]
    n2["c_uom"]
    n3["i_pricelist"]
    n4["m_pricelist"]
    n5["m_pricelist_version"]
    n6["m_product"]
    n3 -->|"c_bpartner_id → c_bpartner_id"| n0
    n3 -->|"c_currency_id → c_currency_id"| n1
    n3 -->|"c_uom_id → c_uom_id"| n2
    n3 -->|"m_pricelist_id → m_pricelist_id"| n4
    n3 -->|"m_pricelist_version_id → m_pricelist_version_id"| n5
    n3 -->|"m_product_id → m_product_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cbpartner_ipricelist` <!-- FK_OUT: adempiere.i_pricelist.cbpartner_ipricelist --> | [`i_pricelist`](i_pricelist.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_ipricelist` <!-- FK_OUT: adempiere.i_pricelist.ccurrency_ipricelist --> | [`i_pricelist`](i_pricelist.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cuom_ipricelist` <!-- FK_OUT: adempiere.i_pricelist.cuom_ipricelist --> | [`i_pricelist`](i_pricelist.md) | `c_uom_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpricelist_ipricelist` <!-- FK_OUT: adempiere.i_pricelist.mpricelist_ipricelist --> | [`i_pricelist`](i_pricelist.md) | `m_pricelist_id` | [`m_pricelist`](../m/m_pricelist.md) | `m_pricelist_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpricelistversion_ipricelist` <!-- FK_OUT: adempiere.i_pricelist.mpricelistversion_ipricelist --> | [`i_pricelist`](i_pricelist.md) | `m_pricelist_version_id` | [`m_pricelist_version`](../m/m_pricelist_version.md) | `m_pricelist_version_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_ipricelist` <!-- FK_OUT: adempiere.i_pricelist.mproduct_ipricelist --> | [`i_pricelist`](i_pricelist.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
