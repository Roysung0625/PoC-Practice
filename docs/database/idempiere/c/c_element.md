# c_element — 계정 요소 체계

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_element` |
| 한국어 논리명(문서용 해석) | 계정 요소 체계 |
| 원본 논리명 | Element |
| 원본 사전 ID | 142 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 3 / 3 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

회계 계정 요소의 체계를 정의하며 개별 요소 값의 상위 기준이 된다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Accounting Element
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_element_pkey` | `c_element_id` |
| UNIQUE | `c_element_uu_idx` | `c_element_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `c_element_name`: `CREATE UNIQUE INDEX c_element_name ON adempiere.c_element USING btree (ad_client_id, name)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_element_id` | Element | numeric(10,0) | 불가 | 예 | — | Accounting Element |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `vformat` | Value Format | character varying(40) | 허용 | — | — | Format of the value; Can contain fixed format elements, Variables: "_lLoOaAcCa09", or ~regex |
| 12 | `elementtype` | Type | character(1) | 불가 | — | — | Element Type (account or user defined) |
| 13 | `isbalancing` | Balancing | character(1) | 불가 | — | 'N'::bpchar | All transactions within an element value must balance (e.g. cost centers) |
| 14 | `isnaturalaccount` | Natural Account | character(1) | 불가 | — | 'Y'::bpchar | The primary natural account |
| 15 | `ad_tree_id` | Tree | numeric(10,0) | 허용 | — | — | Identifies a Tree |
| 16 | `c_element_uu` | C_Element_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 6개 중 6개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_org"]
    n2["ad_tree"]
    n3["c_acctschema_element"]
    n4["c_element"]
    n5["c_elementvalue"]
    n6["i_elementvalue"]
    n4 -->|"ad_client_id → ad_client_id"| n0
    n4 -->|"ad_tree_id → ad_tree_id"| n2
    n4 -->|"ad_org_id → ad_org_id"| n1
    n3 -->|"c_element_id → c_element_id"| n4
    n5 -->|"c_element_id → c_element_id"| n4
    n6 -->|"c_element_id → c_element_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adclient_celement` <!-- FK_OUT: adempiere.c_element.adclient_celement --> | [`c_element`](c_element.md) | `ad_client_id` | [`ad_client`](../ad/ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtree_celement` <!-- FK_OUT: adempiere.c_element.adtree_celement --> | [`c_element`](c_element.md) | `ad_tree_id` | [`ad_tree`](../ad/ad_tree.md) | `ad_tree_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_elementorg` <!-- FK_OUT: adempiere.c_element.c_elementorg --> | [`c_element`](c_element.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `celement_caschemaelement` <!-- FK_IN: adempiere.c_acctschema_element.celement_caschemaelement --> | [`c_acctschema_element`](c_acctschema_element.md) | `c_element_id` | [`c_element`](c_element.md) | `c_element_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celement_celementvalue` <!-- FK_IN: adempiere.c_elementvalue.celement_celementvalue --> | [`c_elementvalue`](c_elementvalue.md) | `c_element_id` | [`c_element`](c_element.md) | `c_element_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `celement_ielementvalue` <!-- FK_IN: adempiere.i_elementvalue.celement_ielementvalue --> | [`i_elementvalue`](../i/i_elementvalue.md) | `c_element_id` | [`c_element`](c_element.md) | `c_element_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
