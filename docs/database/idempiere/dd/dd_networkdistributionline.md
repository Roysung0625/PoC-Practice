# dd_networkdistributionline — 재고 배분 네트워크 명세

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.dd_networkdistributionline` |
| 한국어 논리명(문서용 해석) | 재고 배분 네트워크 명세 |
| 원본 논리명 | Network Distribution Line |
| 원본 사전 ID | 53061 |
| 분류 | `dd` — 물류 이동·분배 주문 |
| 전체 테넌트 행 수 | 10 |
| 물리 열 수 | 18 |
| 나가는 FK / 들어오는 FK | 4 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

재고 배분 네트워크의 출발·도착 창고, 운송사, 배분 비율·이송 시간·우선순위와 유효 기간을 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Network Distribution Line
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| UNIQUE | `dd_networkdistributionl_uu_idx` | `dd_networkdistributionline_uu` |
| PRIMARY KEY | `dd_networkdistributionline_key` | `dd_networkdistributionline_id` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 4 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 5 | `dd_networkdistributionline_id` | Network Distribution Line | numeric(10,0) | 불가 | 예 | — | — |
| 6 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 7 | `m_shipper_id` | Shipper | numeric(10,0) | 불가 | — | — | Method or manner of product delivery |
| 8 | `m_warehousesource_id` | Source Warehouse | numeric(10,0) | 불가 | — | — | Optional Warehouse to replenish from |
| 9 | `percent` | Percent | numeric | 허용 | — | — | Percentage |
| 10 | `transferttime` | Transfer Time | numeric(10,0) | 허용 | — | — | — |
| 11 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 12 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 13 | `validto` | Valid to | timestamp without time zone | 허용 | — | — | Valid to including this date (last day) |
| 14 | `priorityno` | Relative Priority | numeric(10,0) | 허용 | — | — | Where inventory should be picked from first |
| 15 | `dd_networkdistribution_id` | Network Distribution | numeric(10,0) | 불가 | — | — | — |
| 16 | `m_warehouse_id` | Warehouse | numeric(10,0) | 불가 | — | — | Storage Warehouse and Service Point |
| 17 | `validfrom` | Valid from | timestamp without time zone | 허용 | — | — | Valid from including this date (first day) |
| 18 | `dd_networkdistributionline_uu` | DD_NetworkDistributionLine_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["dd_networkdistribution"]
    n1["dd_networkdistributionline"]
    n2["m_shipper"]
    n3["m_warehouse"]
    n1 -->|"dd_networkdistribution_id → dd_networkdistribution_id"| n0
    n1 -->|"m_shipper_id → m_shipper_id"| n2
    n1 -->|"m_warehouse_id → m_warehouse_id"| n3
    n1 -->|"m_warehousesource_id → m_warehouse_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ddnetworkdistribution_ddnetwor` <!-- FK_OUT: adempiere.dd_networkdistributionline.ddnetworkdistribution_ddnetwor --> | [`dd_networkdistributionline`](dd_networkdistributionline.md) | `dd_networkdistribution_id` | [`dd_networkdistribution`](dd_networkdistribution.md) | `dd_networkdistribution_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mshipper_ddnetworkdistribution` <!-- FK_OUT: adempiere.dd_networkdistributionline.mshipper_ddnetworkdistribution --> | [`dd_networkdistributionline`](dd_networkdistributionline.md) | `m_shipper_id` | [`m_shipper`](../m/m_shipper.md) | `m_shipper_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_ddnetworkdistributi` <!-- FK_OUT: adempiere.dd_networkdistributionline.mwarehouse_ddnetworkdistributi --> | [`dd_networkdistributionline`](dd_networkdistributionline.md) | `m_warehouse_id` | [`m_warehouse`](../m/m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehousesource_ddnetworkdist` <!-- FK_OUT: adempiere.dd_networkdistributionline.mwarehousesource_ddnetworkdist --> | [`dd_networkdistributionline`](dd_networkdistributionline.md) | `m_warehousesource_id` | [`m_warehouse`](../m/m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
