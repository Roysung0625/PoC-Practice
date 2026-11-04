# c_taxdeclarationline — 세금 신고 문서 명세

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_taxdeclarationline` |
| 한국어 논리명(문서용 해석) | 세금 신고 문서 명세 |
| 원본 논리명 | Tax Declaration Line |
| 원본 사전 ID | 819 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 22 |
| 나가는 FK / 들어오는 FK | 7 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

생성 처리로 수집된 신고 대상 문서를 저장한다. 특정 신고에 포함하지 않을 행은 제외할 수 있다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Tax Declaration Document Information
- 원본 도움말: The lines are created by the create process. You can delete them if you do not want to include them in a particular declaration. 
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_taxdeclarationline_pkey` | `c_taxdeclarationline_id` |
| UNIQUE | `c_taxdeclarationline_uu_idx` | `c_taxdeclarationline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_taxdeclarationline_id` | Tax Declaration Line | numeric(10,0) | 불가 | 예 | — | Tax Declaration Document Information |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `line` | Line No | numeric(10,0) | 불가 | — | 0 | Unique line for this document |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `ismanual` | Manual | character(1) | 불가 | — | 'N'::bpchar | This is a manual process |
| 12 | `c_taxdeclaration_id` | Tax Declaration | numeric(10,0) | 불가 | — | — | Define the declaration to the tax authorities |
| 13 | `c_bpartner_id` | Business Partner | numeric(10,0) | 불가 | — | — | Identifies a Business Partner |
| 14 | `c_tax_id` | Tax | numeric(10,0) | 불가 | — | — | Tax identifier |
| 15 | `c_invoice_id` | Invoice | numeric(10,0) | 허용 | — | — | Invoice Identifier |
| 16 | `c_invoiceline_id` | Invoice Line | numeric(10,0) | 허용 | — | — | Invoice Detail Line |
| 17 | `c_allocationline_id` | Allocation Line | numeric(10,0) | 허용 | — | — | Allocation Line |
| 18 | `c_currency_id` | Currency | numeric(10,0) | 불가 | — | — | The Currency for this record |
| 19 | `taxbaseamt` | Tax base Amount | numeric | 불가 | — | 0 | Base for calculating the tax amount |
| 20 | `taxamt` | Tax Amount | numeric | 불가 | — | 0 | Tax Amount for a document |
| 21 | `dateacct` | Account Date | timestamp without time zone | 불가 | — | — | Accounting Date |
| 22 | `c_taxdeclarationline_uu` | C_TaxDeclarationLine_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_allocationline"]
    n1["c_bpartner"]
    n2["c_currency"]
    n3["c_invoice"]
    n4["c_invoiceline"]
    n5["c_tax"]
    n6["c_taxdeclaration"]
    n7["c_taxdeclarationline"]
    n7 -->|"c_allocationline_id → c_allocationline_id"| n0
    n7 -->|"c_bpartner_id → c_bpartner_id"| n1
    n7 -->|"c_currency_id → c_currency_id"| n2
    n7 -->|"c_invoice_id → c_invoice_id"| n3
    n7 -->|"c_invoiceline_id → c_invoiceline_id"| n4
    n7 -->|"c_tax_id → c_tax_id"| n5
    n7 -->|"c_taxdeclaration_id → c_taxdeclaration_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `callocationline_ctaxdeclline` <!-- FK_OUT: adempiere.c_taxdeclarationline.callocationline_ctaxdeclline --> | [`c_taxdeclarationline`](c_taxdeclarationline.md) | `c_allocationline_id` | [`c_allocationline`](c_allocationline.md) | `c_allocationline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_ctaxdeclline` <!-- FK_OUT: adempiere.c_taxdeclarationline.cbpartner_ctaxdeclline --> | [`c_taxdeclarationline`](c_taxdeclarationline.md) | `c_bpartner_id` | [`c_bpartner`](c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_ctaxdeclline` <!-- FK_OUT: adempiere.c_taxdeclarationline.ccurrency_ctaxdeclline --> | [`c_taxdeclarationline`](c_taxdeclarationline.md) | `c_currency_id` | [`c_currency`](c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoice_ctaxdeclline` <!-- FK_OUT: adempiere.c_taxdeclarationline.cinvoice_ctaxdeclline --> | [`c_taxdeclarationline`](c_taxdeclarationline.md) | `c_invoice_id` | [`c_invoice`](c_invoice.md) | `c_invoice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoiceline_ctaxdeclline` <!-- FK_OUT: adempiere.c_taxdeclarationline.cinvoiceline_ctaxdeclline --> | [`c_taxdeclarationline`](c_taxdeclarationline.md) | `c_invoiceline_id` | [`c_invoiceline`](c_invoiceline.md) | `c_invoiceline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ctax_ctaxdeclline` <!-- FK_OUT: adempiere.c_taxdeclarationline.ctax_ctaxdeclline --> | [`c_taxdeclarationline`](c_taxdeclarationline.md) | `c_tax_id` | [`c_tax`](c_tax.md) | `c_tax_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ctaxdeclaration_ctaxdeclline` <!-- FK_OUT: adempiere.c_taxdeclarationline.ctaxdeclaration_ctaxdeclline --> | [`c_taxdeclarationline`](c_taxdeclarationline.md) | `c_taxdeclaration_id` | [`c_taxdeclaration`](c_taxdeclaration.md) | `c_taxdeclaration_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
