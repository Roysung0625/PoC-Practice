# m_storagereservationlog — 재고 예약 변경 로그

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_storagereservationlog` |
| 한국어 논리명(문서용 해석) | 재고 예약 변경 로그 |
| 원본 논리명 | Storage Reservation Log |
| 원본 사전 ID | 200281 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 21 |
| 나가는 FK / 들어오는 FK | 9 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

재고 예약 수량이 바뀔 때마다 변경 전후 수량과 증감량을 기록한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Log for every storage reservation quantity change
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_storagereservationlog_key` | `m_storagereservationlog_id` |
| UNIQUE | `m_storagereservationlog_uu_idx` | `m_storagereservationlog_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 4 | `c_doctype_id` | Document Type | numeric(10,0) | 허용 | — | — | Document type or rules |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | — | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `documentno` | Document No | character varying(255) | 허용 | — | — | Document sequence number of the document |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `issotrx` | Sales Transaction | character(1) | 불가 | — | — | This is a Sales Transaction |
| 10 | `lineno` | Line | numeric(10,0) | 허용 | — | NULL::numeric | Line No |
| 11 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 불가 | — | — | Product Attribute Set Instance |
| 12 | `m_product_id` | Product | numeric(10,0) | 불가 | — | — | Product, Service, Item |
| 13 | `m_storagereservationlog_id` | Storage Reservation Log | numeric(10,0) | 불가 | 예 | — | Log for every storage reservation quantity change |
| 14 | `m_storagereservationlog_uu` | M_StorageReservationLog_UU | uuid | 불가 | — | — | — |
| 15 | `m_warehouse_id` | Warehouse | numeric(10,0) | 불가 | — | — | Storage Warehouse and Service Point |
| 16 | `record_id` | Record ID | numeric(10,0) | 불가 | — | — | Direct internal record ID |
| 17 | `updated` | Updated | timestamp without time zone | 불가 | — | — | Date this record was updated |
| 18 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 19 | `deltaqty` | Delta Quantity | numeric | 불가 | — | — | Quantity Difference |
| 20 | `oldqty` | Old Current Quantity | numeric | 불가 | — | — | Old current quantity before the processing of M_CostDetail |
| 21 | `newqty` | New Current Quantity | numeric | 불가 | — | — | New current quantity after processing of M_CostDetail |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 9개 중 9개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_org"]
    n2["ad_table"]
    n3["ad_user"]
    n4["c_doctype"]
    n5["m_attributesetinstance"]
    n6["m_product"]
    n7["m_storagereservationlog"]
    n8["m_warehouse"]
    n7 -->|"ad_client_id → ad_client_id"| n0
    n7 -->|"ad_org_id → ad_org_id"| n1
    n7 -->|"ad_table_id → ad_table_id"| n2
    n7 -->|"c_doctype_id → c_doctype_id"| n4
    n7 -->|"createdby → ad_user_id"| n3
    n7 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n5
    n7 -->|"m_product_id → m_product_id"| n6
    n7 -->|"m_warehouse_id → m_warehouse_id"| n8
    n7 -->|"updatedby → ad_user_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adclient_mstoragereservationlo` <!-- FK_OUT: adempiere.m_storagereservationlog.adclient_mstoragereservationlo --> | [`m_storagereservationlog`](m_storagereservationlog.md) | `ad_client_id` | [`ad_client`](../ad/ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorg_mstoragereservationlog` <!-- FK_OUT: adempiere.m_storagereservationlog.adorg_mstoragereservationlog --> | [`m_storagereservationlog`](m_storagereservationlog.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtable_mstoragereservationlog` <!-- FK_OUT: adempiere.m_storagereservationlog.adtable_mstoragereservationlog --> | [`m_storagereservationlog`](m_storagereservationlog.md) | `ad_table_id` | [`ad_table`](../ad/ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_mstoragereservationlo` <!-- FK_OUT: adempiere.m_storagereservationlog.cdoctype_mstoragereservationlo --> | [`m_storagereservationlog`](m_storagereservationlog.md) | `c_doctype_id` | [`c_doctype`](../c/c_doctype.md) | `c_doctype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `createdby_mstoragereservationl` <!-- FK_OUT: adempiere.m_storagereservationlog.createdby_mstoragereservationl --> | [`m_storagereservationlog`](m_storagereservationlog.md) | `createdby` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattributesetinstance_mstorage` <!-- FK_OUT: adempiere.m_storagereservationlog.mattributesetinstance_mstorage --> | [`m_storagereservationlog`](m_storagereservationlog.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mstoragereservationlo` <!-- FK_OUT: adempiere.m_storagereservationlog.mproduct_mstoragereservationlo --> | [`m_storagereservationlog`](m_storagereservationlog.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwh_mstoragereservationlog` <!-- FK_OUT: adempiere.m_storagereservationlog.mwh_mstoragereservationlog --> | [`m_storagereservationlog`](m_storagereservationlog.md) | `m_warehouse_id` | [`m_warehouse`](m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `updatedby_mstoragereservationl` <!-- FK_OUT: adempiere.m_storagereservationlog.updatedby_mstoragereservationl --> | [`m_storagereservationlog`](m_storagereservationlog.md) | `updatedby` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `issotrx`가 있습니다. 판매(`Y`)와 구매(`N`)를 구분해서 분석합니다.
- `record_id`는 가리키는 테이블이 메타데이터에 따라 달라질 수 있습니다. 물리 FK 목록에 없는 대상은 별도 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
