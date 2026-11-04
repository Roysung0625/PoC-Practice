# c_conversion_rate — 환율

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_conversion_rate` |
| 한국어 논리명(문서용 해석) | 환율 |
| 원본 논리명 | Conversion Rate |
| 원본 사전 ID | 140 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 4 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 5 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

통화 간 금액 변환에 사용하는 환율을 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Rate used for converting currencies
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_conversion_rate_pkey` | `c_conversion_rate_id` |
| UNIQUE | `c_conversion_rate_uu_idx` | `c_conversion_rate_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `c_conversionrate_once`: `CREATE UNIQUE INDEX c_conversionrate_once ON adempiere.c_conversion_rate USING btree (ad_client_id, ad_org_id, c_currency_id, c_currency_id_to, c_conversiontype_id, validfrom)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_conversion_rate_id` | Conversion Rate | numeric(10,0) | 불가 | 예 | — | Rate used for converting currencies |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_currency_id` | Currency | numeric(10,0) | 불가 | — | — | The Currency for this record |
| 10 | `c_currency_id_to` | Currency To | numeric(10,0) | 불가 | — | — | Target currency |
| 11 | `validfrom` | Valid from | timestamp without time zone | 불가 | — | — | Valid from including this date (first day) |
| 12 | `validto` | Valid to | timestamp without time zone | 허용 | — | — | Valid to including this date (last day) |
| 13 | `multiplyrate` | Multiply Rate | numeric | 불가 | — | 0 | Rate to multiple the source by to calculate the target. |
| 14 | `dividerate` | Divide Rate | numeric | 불가 | — | 0 | To convert Source number to Target number, the Source is divided |
| 15 | `c_conversiontype_id` | Currency Type | numeric(10,0) | 불가 | — | — | Currency Conversion Rate Type |
| 16 | `c_conversion_rate_uu` | C_Conversion_Rate_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 6개 중 6개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_org"]
    n2["c_conversion_rate"]
    n3["c_conversiontype"]
    n4["c_currency"]
    n5["i_conversion_rate"]
    n2 -->|"ad_client_id → ad_client_id"| n0
    n2 -->|"ad_org_id → ad_org_id"| n1
    n2 -->|"c_currency_id_to → c_currency_id"| n4
    n2 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n2 -->|"c_currency_id → c_currency_id"| n4
    n5 -->|"c_conversion_rate_id → c_conversion_rate_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `c_conversion_rateclient` <!-- FK_OUT: adempiere.c_conversion_rate.c_conversion_rateclient --> | [`c_conversion_rate`](c_conversion_rate.md) | `ad_client_id` | [`ad_client`](../ad/ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_conversion_rateorg` <!-- FK_OUT: adempiere.c_conversion_rate.c_conversion_rateorg --> | [`c_conversion_rate`](c_conversion_rate.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_currencyconvrateto` <!-- FK_OUT: adempiere.c_conversion_rate.c_currencyconvrateto --> | [`c_conversion_rate`](c_conversion_rate.md) | `c_currency_id_to` | [`c_currency`](c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_cconvrate` <!-- FK_OUT: adempiere.c_conversion_rate.cconversiontype_cconvrate --> | [`c_conversion_rate`](c_conversion_rate.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_cconversionrate` <!-- FK_OUT: adempiere.c_conversion_rate.ccurrency_cconversionrate --> | [`c_conversion_rate`](c_conversion_rate.md) | `c_currency_id` | [`c_currency`](c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cconversionrate_iconvrate` <!-- FK_IN: adempiere.i_conversion_rate.cconversionrate_iconvrate --> | [`i_conversion_rate`](../i/i_conversion_rate.md) | `c_conversion_rate_id` | [`c_conversion_rate`](c_conversion_rate.md) | `c_conversion_rate_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
