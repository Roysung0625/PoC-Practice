# m_changenotice — 변경 통지

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_changenotice` |
| 한국어 논리명(문서용 해석) | 변경 통지 |
| 원본 논리명 | Change Notice |
| 원본 사전 ID | 799 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 0 / 11 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제품 변경과 관련한 통지 내용 및 승인·처리 상태를 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_changenotice_pkey` | `m_changenotice_id` |
| UNIQUE | `m_changenotice_uu_idx` | `m_changenotice_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_changenotice_id` | Change Notice | numeric(10,0) | 불가 | 예 | — | Bill of Materials (Engineering) Change Notice (Version) |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 12 | `detailinfo` | Detail Information | text | 허용 | — | — | Additional Detail Information |
| 13 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 14 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 15 | `isapproved` | Approved | character(1) | 불가 | — | 'N'::bpchar | Indicates if this document requires approval |
| 16 | `m_changenotice_uu` | M_ChangeNotice_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 11개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["dd_networkdistribution"]
    n1["m_bom"]
    n2["m_bomproduct"]
    n3["m_changenotice"]
    n4["m_changerequest"]
    n5["pp_order_bom"]
    n6["pp_order_bomline"]
    n7["pp_product_bom"]
    n8["pp_product_bomline"]
    n9["r_group"]
    n0 -->|"m_changenotice_id → m_changenotice_id"| n3
    n1 -->|"m_changenotice_id → m_changenotice_id"| n3
    n2 -->|"m_changenotice_id → m_changenotice_id"| n3
    n4 -->|"m_changenotice_id → m_changenotice_id"| n3
    n4 -->|"m_fixchangenotice_id → m_changenotice_id"| n3
    n5 -->|"m_changenotice_id → m_changenotice_id"| n3
    n6 -->|"m_changenotice_id → m_changenotice_id"| n3
    n7 -->|"m_changenotice_id → m_changenotice_id"| n3
    n8 -->|"m_changenotice_id → m_changenotice_id"| n3
    n9 -->|"m_changenotice_id → m_changenotice_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mchangenotice_ddnetworkdistrib` <!-- FK_IN: adempiere.dd_networkdistribution.mchangenotice_ddnetworkdistrib --> | [`dd_networkdistribution`](../dd/dd_networkdistribution.md) | `m_changenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcn_mbom` <!-- FK_IN: adempiere.m_bom.mcn_mbom --> | [`m_bom`](m_bom.md) | `m_changenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcn_mbomproduct` <!-- FK_IN: adempiere.m_bomproduct.mcn_mbomproduct --> | [`m_bomproduct`](m_bomproduct.md) | `m_changenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcn_mcr` <!-- FK_IN: adempiere.m_changerequest.mcn_mcr --> | [`m_changerequest`](m_changerequest.md) | `m_changenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mfixchangenotice_mchangereques` <!-- FK_IN: adempiere.m_changerequest.mfixchangenotice_mchangereques --> | [`m_changerequest`](m_changerequest.md) | `m_fixchangenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mchangenotice_pporderbom` <!-- FK_IN: adempiere.pp_order_bom.mchangenotice_pporderbom --> | [`pp_order_bom`](../pp/pp_order_bom.md) | `m_changenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mchangenotice_pporderbomline` <!-- FK_IN: adempiere.pp_order_bomline.mchangenotice_pporderbomline --> | [`pp_order_bomline`](../pp/pp_order_bomline.md) | `m_changenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mchangenotice_ppproductbom` <!-- FK_IN: adempiere.pp_product_bom.mchangenotice_ppproductbom --> | [`pp_product_bom`](../pp/pp_product_bom.md) | `m_changenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mchangenotice_ppproductbomline` <!-- FK_IN: adempiere.pp_product_bomline.mchangenotice_ppproductbomline --> | [`pp_product_bomline`](../pp/pp_product_bomline.md) | `m_changenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mchangenotice_rgroup` <!-- FK_IN: adempiere.r_group.mchangenotice_rgroup --> | [`r_group`](../r/r_group.md) | `m_changenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mfixchangenotice_rrequest` <!-- FK_IN: adempiere.r_request.mfixchangenotice_rrequest --> | [`r_request`](../r/r_request.md) | `m_fixchangenotice_id` | [`m_changenotice`](m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
