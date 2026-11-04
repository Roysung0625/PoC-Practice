# c_dunningrunentry — 연체 독촉 실행 대상

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_dunningrunentry` |
| 한국어 논리명(문서용 해석) | 연체 독촉 실행 대상 |
| 원본 논리명 | Dunning Run Entry |
| 원본 사전 ID | 527 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 20 |
| 나가는 FK / 들어오는 FK | 7 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

독촉 실행에서 거래처·주소·담당 연락처별 독촉 금액과 단계 및 안내 문구를 묶는다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Dunning Run Entry
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_dunningrunentry_pkey` | `c_dunningrunentry_id` |
| UNIQUE | `c_dunningrunentry_uu_idx` | `c_dunningrunentry_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_dunningrunentry_id` | Dunning Run Entry | numeric(10,0) | 불가 | 예 | — | Dunning Run Entry |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_bpartner_id` | Business Partner | numeric(10,0) | 불가 | — | — | Identifies a Business Partner |
| 10 | `c_bpartner_location_id` | Partner Location | numeric(10,0) | 불가 | — | — | Identifies the (ship to) address for this Business Partner |
| 11 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | — | User within the system - Internal or Business Partner Contact |
| 12 | `c_dunningrun_id` | Dunning Run | numeric(10,0) | 불가 | — | — | Dunning Run |
| 13 | `c_currency_id` | Currency | numeric(10,0) | 불가 | — | — | The Currency for this record |
| 14 | `salesrep_id` | Sales Representative | numeric(10,0) | 불가 | — | — | Sales Representative or Company Agent |
| 15 | `amt` | Amount | numeric | 불가 | — | 0 | Amount |
| 16 | `qty` | Quantity | numeric | 불가 | — | 0 | Quantity |
| 17 | `note` | Note | character varying(2000) | 허용 | — | — | Optional additional user defined information |
| 18 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 19 | `c_dunninglevel_id` | Dunning Level | numeric(10,0) | 불가 | — | NULL::numeric | — |
| 20 | `c_dunningrunentry_uu` | C_DunningRunEntry_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_user"]
    n1["c_bpartner"]
    n2["c_bpartner_location"]
    n3["c_currency"]
    n4["c_dunninglevel"]
    n5["c_dunningrun"]
    n6["c_dunningrunentry"]
    n7["c_dunningrunline"]
    n6 -->|"ad_user_id → ad_user_id"| n0
    n6 -->|"c_bpartner_id → c_bpartner_id"| n1
    n6 -->|"c_bpartner_location_id → c_bpartner_location_id"| n2
    n6 -->|"c_currency_id → c_currency_id"| n3
    n6 -->|"c_dunninglevel_id → c_dunninglevel_id"| n4
    n6 -->|"c_dunningrun_id → c_dunningrun_id"| n5
    n6 -->|"salesrep_id → ad_user_id"| n0
    n7 -->|"c_dunningrunentry_id → c_dunningrunentry_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aduser_cdunningrunentry` <!-- FK_OUT: adempiere.c_dunningrunentry.aduser_cdunningrunentry --> | [`c_dunningrunentry`](c_dunningrunentry.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_cdunningrunentry` <!-- FK_OUT: adempiere.c_dunningrunentry.cbpartner_cdunningrunentry --> | [`c_dunningrunentry`](c_dunningrunentry.md) | `c_bpartner_id` | [`c_bpartner`](c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartnerlocation_cdunningrune` <!-- FK_OUT: adempiere.c_dunningrunentry.cbpartnerlocation_cdunningrune --> | [`c_dunningrunentry`](c_dunningrunentry.md) | `c_bpartner_location_id` | [`c_bpartner_location`](c_bpartner_location.md) | `c_bpartner_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_cdunningrunentry` <!-- FK_OUT: adempiere.c_dunningrunentry.ccurrency_cdunningrunentry --> | [`c_dunningrunentry`](c_dunningrunentry.md) | `c_currency_id` | [`c_currency`](c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdunninglevel_cdunningrunentry` <!-- FK_OUT: adempiere.c_dunningrunentry.cdunninglevel_cdunningrunentry --> | [`c_dunningrunentry`](c_dunningrunentry.md) | `c_dunninglevel_id` | [`c_dunninglevel`](c_dunninglevel.md) | `c_dunninglevel_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdunningrun_cdunningrunentry` <!-- FK_OUT: adempiere.c_dunningrunentry.cdunningrun_cdunningrunentry --> | [`c_dunningrunentry`](c_dunningrunentry.md) | `c_dunningrun_id` | [`c_dunningrun`](c_dunningrun.md) | `c_dunningrun_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `salesrep_cdunningrunentry` <!-- FK_OUT: adempiere.c_dunningrunentry.salesrep_cdunningrunentry --> | [`c_dunningrunentry`](c_dunningrunentry.md) | `salesrep_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cdunningrunentry_line` <!-- FK_IN: adempiere.c_dunningrunline.cdunningrunentry_line --> | [`c_dunningrunline`](c_dunningrunline.md) | `c_dunningrunentry_id` | [`c_dunningrunentry`](c_dunningrunentry.md) | `c_dunningrunentry_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
