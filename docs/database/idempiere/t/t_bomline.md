# t_bomline — BOM 임시 전개행

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.t_bomline` |
| 한국어 논리명(문서용 해석) | BOM 임시 전개행 |
| 원본 논리명 | Temporal BOM Line |
| 원본 사전 ID | 53045 |
| 분류 | `t` — 작업·보고서용 보조 테이블 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 30 |
| 나가는 FK / 들어오는 FK | 0 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

BOM 전개 및 역전개 결과의 계층·제품·구성 수량·원가를 실행 건별로 임시 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Temporal BOM Line
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `t_bomline_key` | `t_bomline_id` |
| UNIQUE | `t_bomline_uu_idx` | `t_bomline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_pinstance_id` | Process Instance | numeric(10,0) | 허용 | — | — | Instance of the process |
| 4 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 5 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 6 | `isactive` | Active | character(1) | 허용 | — | — | The record is active in the system |
| 7 | `levelno` | Level no | numeric(10,0) | 허용 | — | — | — |
| 8 | `levels` | Levels | character varying(250) | 허용 | — | — | — |
| 9 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 10 | `pp_product_bomline_id` | BOM Line | numeric(10,0) | 허용 | — | — | BOM Line |
| 11 | `pp_product_bom_id` | BOM &amp; Formula | numeric(10,0) | 허용 | — | — | BOM &amp; Formula |
| 12 | `seqno` | Sequence | numeric(10,0) | 허용 | — | — | Method of ordering records; lowest number comes first |
| 13 | `t_bomline_id` | Temporal BOM Line | numeric(10,0) | 불가 | 예 | — | — |
| 14 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 15 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 16 | `sel_product_id` | Selected Product | numeric(10,0) | 불가 | — | — | — |
| 17 | `implosion` | Implosion | character(1) | 허용 | — | 'N'::bpchar | Implosion of a Bill of Materials refers to finding all the BOM''s in which a component is used. |
| 18 | `m_costelement_id` | Cost Element | numeric(10,0) | 허용 | — | — | Product Cost Element |
| 19 | `currentcostprice` | Current Cost Price | numeric | 허용 | — | — | The currently used cost price |
| 20 | `currentcostpricell` | Current Cost Price Lower Level | numeric | 허용 | — | — | Current Price Lower Level Is the sum of the costs of the components of this product manufactured for this level. |
| 21 | `qtybom` | Quantity | numeric | 허용 | — | — | Indicate the Quantity use in this BOM |
| 22 | `cost` | Cost | character varying(22) | 허용 | — | — | Cost information |
| 23 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 허용 | — | — | Rules for accounting |
| 24 | `costingmethod` | Costing Method | character(1) | 허용 | — | NULL::bpchar | Indicates how Costs will be calculated |
| 25 | `m_costtype_id` | Cost Type | numeric(10,0) | 허용 | — | NULL::numeric | Type of Cost (e.g. Current, Plan, Future) |
| 26 | `futurecostprice` | Future Cost Price | numeric | 허용 | — | — | — |
| 27 | `futurecostpricell` | Future Cost Price Lower Level | numeric | 허용 | — | — | — |
| 28 | `iscostfrozen` | Cost Frozen | character(1) | 허용 | — | NULL::bpchar | Indicated that the Standard Cost is frozen |
| 29 | `coststandard` | Standard Cost | numeric | 허용 | — | — | Standard Costs |
| 30 | `t_bomline_uu` | T_BOMLine_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

### 이 테이블이 참조하는 부모 — 나가는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
