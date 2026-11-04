# m_bomproduct — BOM 구성품

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_bomproduct` |
| 한국어 논리명(문서용 해석) | BOM 구성품 |
| 원본 논리명 | BOM Component |
| 원본 사전 ID | 801 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 23 |
| 나가는 FK / 들어오는 FK | 6 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

자재명세서에 포함되는 제품 구성품을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Bill of Material Component (Product)
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_bomproduct_pkey` | `m_bomproduct_id` |
| UNIQUE | `m_bomproduct_uu_idx` | `m_bomproduct_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_bomproduct_id` | BOM Component | numeric(10,0) | 불가 | 예 | — | Bill of Material Component (Product) |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `line` | Line No | numeric(10,0) | 불가 | — | 0 | Unique line for this document |
| 10 | `m_bom_id` | BOM | numeric(10,0) | 불가 | — | — | Bill of Material |
| 11 | `bomproducttype` | Component Type | character(1) | 불가 | — | — | BOM Product Type |
| 12 | `isphantom` | Phantom | character(1) | 불가 | — | 'N'::bpchar | Phantom Component |
| 13 | `m_productbom_id` | BOM Product | numeric(10,0) | 허용 | — | — | Bill of Material Component Product |
| 14 | `m_changenotice_id` | Change Notice | numeric(10,0) | 허용 | — | — | Bill of Materials (Engineering) Change Notice (Version) |
| 15 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 허용 | — | — | Product Attribute Set Instance |
| 16 | `m_bomalternative_id` | Alternative Group | numeric(10,0) | 허용 | — | — | Product BOM Alternative Group |
| 17 | `bomqty` | BOM Quantity | numeric | 불가 | — | 0 | Bill of Materials Quantity |
| 18 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 19 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 20 | `m_productoperation_id` | Product Operation | numeric(10,0) | 허용 | — | — | Product Manufacturing Operation |
| 21 | `seqno` | Sequence | numeric(10,0) | 허용 | — | 0 | Method of ordering records; lowest number comes first |
| 22 | `leadtimeoffset` | Lead Time Offset | numeric(10,0) | 불가 | — | 0 | Optional Lead Time offset before starting production |
| 23 | `m_bomproduct_uu` | M_BOMProduct_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 6개 중 6개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["m_attributesetinstance"]
    n1["m_bom"]
    n2["m_bomalternative"]
    n3["m_bomproduct"]
    n4["m_changenotice"]
    n5["m_product"]
    n6["m_productoperation"]
    n3 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n0
    n3 -->|"m_bom_id → m_bom_id"| n1
    n3 -->|"m_bomalternative_id → m_bomalternative_id"| n2
    n3 -->|"m_changenotice_id → m_changenotice_id"| n4
    n3 -->|"m_productbom_id → m_product_id"| n5
    n3 -->|"m_productoperation_id → m_productoperation_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `masi_mbomproduct` <!-- FK_OUT: adempiere.m_bomproduct.masi_mbomproduct --> | [`m_bomproduct`](m_bomproduct.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mbom_mbomproduct` <!-- FK_OUT: adempiere.m_bomproduct.mbom_mbomproduct --> | [`m_bomproduct`](m_bomproduct.md) | `m_bom_id` | [`m_bom`](m_bom.md) | `m_bom_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mbomalternative_mbomproduct` <!-- FK_OUT: adempiere.m_bomproduct.mbomalternative_mbomproduct --> | [`m_bomproduct`](m_bomproduct.md) | `m_bomalternative_id` | [`m_bomalternative`](m_bomalternative.md) | `m_bomalternative_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcn_mbomproduct` <!-- FK_OUT: adempiere.m_bomproduct.mcn_mbomproduct --> | [`m_bomproduct`](m_bomproduct.md) | `m_changenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mbomproduct` <!-- FK_OUT: adempiere.m_bomproduct.mproduct_mbomproduct --> | [`m_bomproduct`](m_bomproduct.md) | `m_productbom_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductop_mbomproduct` <!-- FK_OUT: adempiere.m_bomproduct.mproductop_mbomproduct --> | [`m_bomproduct`](m_bomproduct.md) | `m_productoperation_id` | [`m_productoperation`](m_productoperation.md) | `m_productoperation_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
