# c_pos — 판매시점 단말기

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_pos` |
| 한국어 논리명(문서용 해석) | 판매시점 단말기 |
| 원본 논리명 | POS Terminal |
| 원본 사전 ID | 748 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 26 |
| 나가는 FK / 들어오는 FK | 10 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

매장 판매에 사용하는 POS 단말기의 기준정보를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Point of Sales Terminal
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_pos_pkey` | `c_pos_id` |
| UNIQUE | `c_pos_uu_idx` | `c_pos_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_pos_id` | POS Terminal | numeric(10,0) | 불가 | 예 | — | Point of Sales Terminal |
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
| 12 | `salesrep_id` | Sales Representative | numeric(10,0) | 불가 | — | — | Sales Representative or Company Agent |
| 13 | `m_pricelist_id` | Price List | numeric(10,0) | 불가 | — | — | Unique identifier of a Price List |
| 14 | `c_cashbook_id` | Cash Book | numeric(10,0) | 허용 | — | — | Cash Book for recording petty cash transactions |
| 15 | `m_warehouse_id` | Warehouse | numeric(10,0) | 불가 | — | — | Storage Warehouse and Service Point |
| 16 | `printername` | Printer Name | character varying(60) | 허용 | — | — | Name of the Printer |
| 17 | `c_poskeylayout_id` | POS Key Layout | numeric(10,0) | 허용 | — | — | POS Function Key Layout |
| 18 | `ismodifyprice` | Modify Price | character(1) | 불가 | — | 'N'::bpchar | Allow modifying the price |
| 19 | `c_bpartnercashtrx_id` | Template B.Partner | numeric(10,0) | 허용 | — | — | Business Partner used for creating new Business Partners on the fly |
| 20 | `c_doctype_id` | Document Type | numeric(10,0) | 허용 | — | — | Document type or rules |
| 21 | `cashdrawer` | Cash Drawer | character varying(120) | 허용 | — | — | — |
| 22 | `c_bankaccount_id` | Bank Account | numeric(10,0) | 허용 | — | — | Account at the Bank |
| 23 | `c_pos_uu` | C_POS_UU | uuid | 허용 | — | — | — |
| 24 | `osk_keylayout_id` | On Screen Keyboard layout | numeric(10,0) | 허용 | — | NULL::numeric | The key layout to use for on screen keyboard for text fields. |
| 25 | `osnp_keylayout_id` | On Screen Number Pad layout | numeric(10,0) | 허용 | — | NULL::numeric | The key layout to use for on screen number pad for numeric fields. |
| 26 | `autologoutdelay` | Auto Logout Delay | numeric(10,0) | 허용 | — | NULL::numeric | Automatically logout if terminal inactive for this period |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 11개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_user"]
    n1["c_bankaccount"]
    n2["c_bpartner"]
    n3["c_cashbook"]
    n4["c_doctype"]
    n5["c_pos"]
    n6["c_poskeylayout"]
    n7["m_pricelist"]
    n8["m_warehouse"]
    n5 -->|"salesrep_id → ad_user_id"| n0
    n5 -->|"c_bankaccount_id → c_bankaccount_id"| n1
    n5 -->|"c_bpartnercashtrx_id → c_bpartner_id"| n2
    n5 -->|"c_cashbook_id → c_cashbook_id"| n3
    n5 -->|"c_doctype_id → c_doctype_id"| n4
    n5 -->|"c_poskeylayout_id → c_poskeylayout_id"| n6
    n5 -->|"m_pricelist_id → m_pricelist_id"| n7
    n5 -->|"m_warehouse_id → m_warehouse_id"| n8
    n5 -->|"osk_keylayout_id → c_poskeylayout_id"| n6
    n5 -->|"osnp_keylayout_id → c_poskeylayout_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aduser_cpos` <!-- FK_OUT: adempiere.c_pos.aduser_cpos --> | [`c_pos`](c_pos.md) | `salesrep_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbankaccount_cpos` <!-- FK_OUT: adempiere.c_pos.cbankaccount_cpos --> | [`c_pos`](c_pos.md) | `c_bankaccount_id` | [`c_bankaccount`](c_bankaccount.md) | `c_bankaccount_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartnercashtrx_cpos` <!-- FK_OUT: adempiere.c_pos.cbpartnercashtrx_cpos --> | [`c_pos`](c_pos.md) | `c_bpartnercashtrx_id` | [`c_bpartner`](c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccashbook_cpos` <!-- FK_OUT: adempiere.c_pos.ccashbook_cpos --> | [`c_pos`](c_pos.md) | `c_cashbook_id` | [`c_cashbook`](c_cashbook.md) | `c_cashbook_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_cpos` <!-- FK_OUT: adempiere.c_pos.cdoctype_cpos --> | [`c_pos`](c_pos.md) | `c_doctype_id` | [`c_doctype`](c_doctype.md) | `c_doctype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cposkeylayout_cpos` <!-- FK_OUT: adempiere.c_pos.cposkeylayout_cpos --> | [`c_pos`](c_pos.md) | `c_poskeylayout_id` | [`c_poskeylayout`](c_poskeylayout.md) | `c_poskeylayout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpricelist_cpos` <!-- FK_OUT: adempiere.c_pos.mpricelist_cpos --> | [`c_pos`](c_pos.md) | `m_pricelist_id` | [`m_pricelist`](../m/m_pricelist.md) | `m_pricelist_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_cpos` <!-- FK_OUT: adempiere.c_pos.mwarehouse_cpos --> | [`c_pos`](c_pos.md) | `m_warehouse_id` | [`m_warehouse`](../m/m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `oskkeylayout_cpos` <!-- FK_OUT: adempiere.c_pos.oskkeylayout_cpos --> | [`c_pos`](c_pos.md) | `osk_keylayout_id` | [`c_poskeylayout`](c_poskeylayout.md) | `c_poskeylayout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `osnpkeylayout_cpos` <!-- FK_OUT: adempiere.c_pos.osnpkeylayout_cpos --> | [`c_pos`](c_pos.md) | `osnp_keylayout_id` | [`c_poskeylayout`](c_poskeylayout.md) | `c_poskeylayout_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cpos_corder` <!-- FK_IN: adempiere.c_order.cpos_corder --> | [`c_order`](c_order.md) | `c_pos_id` | [`c_pos`](c_pos.md) | `c_pos_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
