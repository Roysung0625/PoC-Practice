# m_packagemps — 다중 포장 세부 정보

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_packagemps` |
| 한국어 논리명(문서용 해석) | 다중 포장 세부 정보 |
| 원본 논리명 | Package MPS |
| 원본 사전 ID | 200044 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 23 |
| 나가는 FK / 들어오는 FK | 3 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

포장별 치수·중량과 개별 및 대표 추적 번호를 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_packagemps_key` | `m_packagemps_id` |
| UNIQUE | `m_packagemps_uu_idx` | `m_packagemps_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `c_uom_length_id` | UOM for Length | numeric(10,0) | 허용 | — | NULL::numeric | Standard Unit of Measure for Length |
| 4 | `c_uom_weight_id` | UOM for Weight | numeric(10,0) | 허용 | — | NULL::numeric | Standard Unit of Measure for Weight |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `createfrom` | Create lines from | character(1) | 허용 | — | NULL::bpchar | Process which will generate a new document lines based on an existing document |
| 8 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 9 | `height` | Height | numeric | 허용 | — | — | — |
| 10 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 11 | `length` | Length | numeric | 허용 | — | — | — |
| 12 | `m_package_id` | Package | numeric(10,0) | 불가 | — | — | Shipment Package |
| 13 | `m_packagemps_id` | Package MPS | numeric(10,0) | 불가 | 예 | — | — |
| 14 | `m_packagemps_uu` | M_PackageMPS_UU | uuid | 허용 | — | — | — |
| 15 | `mastertrackingno` | Master Tracking No | character varying(255) | 허용 | — | NULL::character varying | — |
| 16 | `price` | Price | numeric | 허용 | — | — | Price |
| 17 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 18 | `seqno` | Sequence | numeric(10,0) | 허용 | — | NULL::numeric | Method of ordering records; lowest number comes first |
| 19 | `trackingno` | Tracking No | character varying(255) | 허용 | — | NULL::character varying | Number to track the shipment |
| 20 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 21 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 22 | `weight` | Weight | numeric | 허용 | — | — | Weight of a product |
| 23 | `width` | Width | numeric | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_uom"]
    n1["m_package"]
    n2["m_packageline"]
    n3["m_packagemps"]
    n4["m_shippingtransactionline"]
    n3 -->|"c_uom_length_id → c_uom_id"| n0
    n3 -->|"c_uom_weight_id → c_uom_id"| n0
    n3 -->|"m_package_id → m_package_id"| n1
    n2 -->|"m_packagemps_id → m_packagemps_id"| n3
    n4 -->|"m_packagemps_id → m_packagemps_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cuomlength_mpackagemps` <!-- FK_OUT: adempiere.m_packagemps.cuomlength_mpackagemps --> | [`m_packagemps`](m_packagemps.md) | `c_uom_length_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cuomweight_mpackagemps` <!-- FK_OUT: adempiere.m_packagemps.cuomweight_mpackagemps --> | [`m_packagemps`](m_packagemps.md) | `c_uom_weight_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpackage_mpackagemps` <!-- FK_OUT: adempiere.m_packagemps.mpackage_mpackagemps --> | [`m_packagemps`](m_packagemps.md) | `m_package_id` | [`m_package`](m_package.md) | `m_package_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mpackagemps_mpackageline` <!-- FK_IN: adempiere.m_packageline.mpackagemps_mpackageline --> | [`m_packageline`](m_packageline.md) | `m_packagemps_id` | [`m_packagemps`](m_packagemps.md) | `m_packagemps_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpackagemps_mshippingtransacti` <!-- FK_IN: adempiere.m_shippingtransactionline.mpackagemps_mshippingtransacti --> | [`m_shippingtransactionline`](m_shippingtransactionline.md) | `m_packagemps_id` | [`m_packagemps`](m_packagemps.md) | `m_packagemps_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
