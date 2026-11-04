# c_bp_group_acct — 거래처 그룹 회계 계정

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_bp_group_acct` |
| 한국어 논리명(문서용 해석) | 거래처 그룹 회계 계정 |
| 원본 논리명 | Business Partner Group Acct |
| 원본 사전 ID | 395 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 6 |
| 물리 열 수 | 24 |
| 나가는 FK / 들어오는 FK | 15 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

거래처 그룹과 회계 스키마별 채권·채무·선수선급·할인·미청구 관련 계정을 관리한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_bp_group_acct_pkey` | `c_acctschema_id`, `c_bp_group_id` |
| UNIQUE | `c_bp_group_acct_uu_idx` | `c_bp_group_acct_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 불가 | 예 | — | Rules for accounting |
| 2 | `c_bp_group_id` | Business Partner Group | numeric(10,0) | 불가 | 예 | — | Business Partner Group |
| 3 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 4 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 5 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 8 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 9 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 10 | `c_receivable_acct` | Customer Receivables | numeric(10,0) | 불가 | — | — | Account for Customer Receivables |
| 11 | `c_prepayment_acct` | Customer Prepayment | numeric(10,0) | 불가 | — | — | Account for customer prepayments |
| 12 | `v_liability_acct` | Vendor Liability | numeric(10,0) | 불가 | — | — | Account for Vendor Liability |
| 13 | `v_liability_services_acct` | Vendor Service Liability | numeric(10,0) | 허용 | — | — | Account for Vendor Service Liability |
| 14 | `v_prepayment_acct` | Vendor Prepayment | numeric(10,0) | 불가 | — | — | Account for Vendor Prepayments |
| 15 | `paydiscount_exp_acct` | Payment Discount Expense | numeric(10,0) | 불가 | — | — | Payment Discount Expense Account |
| 16 | `paydiscount_rev_acct` | Payment Discount Revenue | numeric(10,0) | 불가 | — | — | Payment Discount Revenue Account |
| 17 | `writeoff_acct` | Write-off | numeric(10,0) | 불가 | — | — | Account for Receivables write-off |
| 18 | `notinvoicedreceipts_acct` | Not-invoiced Receipts | numeric(10,0) | 불가 | — | — | Account for not-invoiced Material Receipts |
| 19 | `unearnedrevenue_acct` | Unearned Revenue | numeric(10,0) | 허용 | — | — | Account for unearned revenue |
| 20 | `notinvoicedrevenue_acct` | Not-invoiced Revenue | numeric(10,0) | 허용 | — | — | Account for not invoiced Revenue |
| 21 | `notinvoicedreceivables_acct` | Not-invoiced Receivables | numeric(10,0) | 허용 | — | — | Account for not invoiced Receivables |
| 22 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 23 | `c_receivable_services_acct` | Receivable Services | numeric(10,0) | 허용 | — | — | Customer Accounts Receivables Services Account |
| 24 | `c_bp_group_acct_uu` | C_BP_Group_Acct_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 15개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_acctschema"]
    n1["c_bp_group"]
    n2["c_bp_group_acct"]
    n3["c_validcombination"]
    n2 -->|"c_acctschema_id → c_acctschema_id"| n0
    n2 -->|"c_bp_group_id → c_bp_group_id"| n1
    n2 -->|"c_receivable_services_acct → c_validcombination_id"| n3
    n2 -->|"c_prepayment_acct → c_validcombination_id"| n3
    n2 -->|"c_receivable_acct → c_validcombination_id"| n3
    n2 -->|"notinvoicedreceivables_acct → c_validcombination_id"| n3
    n2 -->|"notinvoicedreceipts_acct → c_validcombination_id"| n3
    n2 -->|"notinvoicedrevenue_acct → c_validcombination_id"| n3
    n2 -->|"paydiscount_exp_acct → c_validcombination_id"| n3
    n2 -->|"paydiscount_rev_acct → c_validcombination_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cacctschema_cbpgroupacct` <!-- FK_OUT: adempiere.c_bp_group_acct.cacctschema_cbpgroupacct --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `c_acctschema_id` | [`c_acctschema`](c_acctschema.md) | `c_acctschema_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpgroup_cbpgroupacct` <!-- FK_OUT: adempiere.c_bp_group_acct.cbpgroup_cbpgroupacct --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `c_bp_group_id` | [`c_bp_group`](c_bp_group.md) | `c_bp_group_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `creceivableservices_cbpgroupac` <!-- FK_OUT: adempiere.c_bp_group_acct.creceivableservices_cbpgroupac --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `c_receivable_services_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_cprepayment_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_cprepayment_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `c_prepayment_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_creceivable_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_creceivable_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `c_receivable_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_notinvoicedrec_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_notinvoicedrec_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `notinvoicedreceivables_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_notinvoicedreceipts_cbpgrou` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_notinvoicedreceipts_cbpgrou --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `notinvoicedreceipts_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_notinvoicedrevenue_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_notinvoicedrevenue_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `notinvoicedrevenue_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_paydiscountexp_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_paydiscountexp_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `paydiscount_exp_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_paydiscountrev_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_paydiscountrev_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `paydiscount_rev_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_unearnedrevenue_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_unearnedrevenue_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `unearnedrevenue_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_vliability_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_vliability_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `v_liability_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_vliabilityservices_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_vliabilityservices_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `v_liability_services_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_vprepayment_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_vprepayment_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `v_prepayment_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `vc_writeoff_cbpgroup` <!-- FK_OUT: adempiere.c_bp_group_acct.vc_writeoff_cbpgroup --> | [`c_bp_group_acct`](c_bp_group_acct.md) | `writeoff_acct` | [`c_validcombination`](c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
