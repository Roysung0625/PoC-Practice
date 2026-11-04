# c_payselectionline — 지급 대상 선정 명세

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_payselectionline` |
| 한국어 논리명(문서용 해석) | 지급 대상 선정 명세 |
| 원본 논리명 | Payment Selection Line |
| 원본 사전 ID | 427 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 23 |
| 나가는 FK / 들어오는 FK | 3 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

지급 대상 선정에 포함되는 개별 지급 예정 내역을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Payment Selection Line
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_payselectionline_pkey` | `c_payselectionline_id` |
| UNIQUE | `c_payselectionline_uu_idx` | `c_payselectionline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_payselectionline_id` | Payment Selection Line | numeric(10,0) | 불가 | 예 | — | Payment Selection Line |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_payselection_id` | Payment Selection | numeric(10,0) | 불가 | — | — | Payment Selection |
| 10 | `line` | Line No | numeric(10,0) | 불가 | — | — | Unique line for this document |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `paymentrule` | Payment Rule | character(1) | 불가 | — | — | How you pay the invoice |
| 13 | `ismanual` | Manual | character(1) | 불가 | — | 'Y'::bpchar | This is a manual process |
| 14 | `c_invoice_id` | Invoice | numeric(10,0) | 불가 | — | — | Invoice Identifier |
| 15 | `payamt` | Payment amount | numeric | 불가 | — | 0 | Amount being paid |
| 16 | `differenceamt` | Difference | numeric | 불가 | — | 0 | Difference Amount |
| 17 | `c_payselectioncheck_id` | Pay Selection Check | numeric(10,0) | 허용 | — | — | Payment Selection Check |
| 18 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 19 | `discountamt` | Discount Amount | numeric | 불가 | — | 0 | Calculated amount of discount |
| 20 | `openamt` | Open Amount | numeric | 불가 | — | 0 | Open item amount |
| 21 | `issotrx` | Sales Transaction | character(1) | 불가 | — | 'N'::bpchar | This is a Sales Transaction |
| 22 | `c_payselectionline_uu` | C_PaySelectionLine_UU | uuid | 허용 | — | — | — |
| 23 | `writeoffamt` | Write-off Amount | numeric | 불가 | — | (0)::numeric | Amount to write-off |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 3개 중 3개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_invoice"]
    n1["c_payselection"]
    n2["c_payselectioncheck"]
    n3["c_payselectionline"]
    n3 -->|"c_invoice_id → c_invoice_id"| n0
    n3 -->|"c_payselection_id → c_payselection_id"| n1
    n3 -->|"c_payselectioncheck_id → c_payselectioncheck_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cinvoice_cpayselectline` <!-- FK_OUT: adempiere.c_payselectionline.cinvoice_cpayselectline --> | [`c_payselectionline`](c_payselectionline.md) | `c_invoice_id` | [`c_invoice`](c_invoice.md) | `c_invoice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaysel_cpayselline` <!-- FK_OUT: adempiere.c_payselectionline.cpaysel_cpayselline --> | [`c_payselectionline`](c_payselectionline.md) | `c_payselection_id` | [`c_payselection`](c_payselection.md) | `c_payselection_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpayselcheck_cpayselline` <!-- FK_OUT: adempiere.c_payselectionline.cpayselcheck_cpayselline --> | [`c_payselectionline`](c_payselectionline.md) | `c_payselectioncheck_id` | [`c_payselectioncheck`](c_payselectioncheck.md) | `c_payselectioncheck_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `issotrx`가 있습니다. 판매(`Y`)와 구매(`N`)를 구분해서 분석합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
