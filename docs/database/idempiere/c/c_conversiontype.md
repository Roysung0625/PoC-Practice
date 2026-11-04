# c_conversiontype — 환율 유형

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_conversiontype` |
| 한국어 논리명(문서용 해석) | 환율 유형 |
| 원본 논리명 | Currency Type |
| 원본 사전 ID | 637 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 4 |
| 물리 열 수 | 13 |
| 나가는 FK / 들어오는 FK | 0 / 15 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

통화 환산에 사용할 환율의 유형을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Currency Conversion Rate Type
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_conversiontype_pkey` | `c_conversiontype_id` |
| UNIQUE | `c_conversiontype_uu_idx` | `c_conversiontype_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_conversiontype_id` | Currency Type | numeric(10,0) | 불가 | 예 | — | Currency Conversion Rate Type |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `value` | Search Key | character varying(40) | 불가 | — | — | Search key for the record in the format required - must be unique |
| 10 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `isdefault` | Default | character(1) | 불가 | — | 'N'::bpchar | Default value |
| 13 | `c_conversiontype_uu` | C_ConversionType_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 15개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset_addition"]
    n1["c_banktransfer"]
    n2["c_conversion_rate"]
    n3["c_conversiontype"]
    n4["c_invoice"]
    n5["c_invoicebatch"]
    n6["c_order"]
    n7["c_payment"]
    n8["c_paymenttransaction"]
    n9["gl_journal"]
    n10["gl_journalline"]
    n0 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n1 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n2 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n4 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n5 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n6 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n7 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n8 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n9 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n10 -->|"c_conversiontype_id → c_conversiontype_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cconversiontype_aassetaddition` <!-- FK_IN: adempiere.a_asset_addition.cconversiontype_aassetaddition --> | [`a_asset_addition`](../a/a_asset_addition.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_cbanktransfer` <!-- FK_IN: adempiere.c_banktransfer.cconversiontype_cbanktransfer --> | [`c_banktransfer`](c_banktransfer.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_cconvrate` <!-- FK_IN: adempiere.c_conversion_rate.cconversiontype_cconvrate --> | [`c_conversion_rate`](c_conversion_rate.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_cinvoice` <!-- FK_IN: adempiere.c_invoice.cconversiontype_cinvoice --> | [`c_invoice`](c_invoice.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconventiontype_cinvoicebatch` <!-- FK_IN: adempiere.c_invoicebatch.cconventiontype_cinvoicebatch --> | [`c_invoicebatch`](c_invoicebatch.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_corder` <!-- FK_IN: adempiere.c_order.cconversiontype_corder --> | [`c_order`](c_order.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_cpayment` <!-- FK_IN: adempiere.c_payment.cconversiontype_cpayment --> | [`c_payment`](c_payment.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_cpaymenttransa` <!-- FK_IN: adempiere.c_paymenttransaction.cconversiontype_cpaymenttransa --> | [`c_paymenttransaction`](c_paymenttransaction.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_gljournal` <!-- FK_IN: adempiere.gl_journal.cconversiontype_gljournal --> | [`gl_journal`](../gl/gl_journal.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_gljournalline` <!-- FK_IN: adempiere.gl_journalline.cconversiontype_gljournalline --> | [`gl_journalline`](../gl/gl_journalline.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconvtype_iconvrate` <!-- FK_IN: adempiere.i_conversion_rate.cconvtype_iconvrate --> | [`i_conversion_rate`](../i/i_conversion_rate.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_igljournal` <!-- FK_IN: adempiere.i_gljournal.cconversiontype_igljournal --> | [`i_gljournal`](../i/i_gljournal.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_mdiscschline` <!-- FK_IN: adempiere.m_discountschemaline.cconversiontype_mdiscschline --> | [`m_discountschemaline`](../m/m_discountschemaline.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_minventory` <!-- FK_IN: adempiere.m_inventory.cconversiontype_minventory --> | [`m_inventory`](../m/m_inventory.md) | `c_conversiontype_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_tinvoicegl` <!-- FK_IN: adempiere.t_invoicegl.cconversiontype_tinvoicegl --> | [`t_invoicegl`](../t/t_invoicegl.md) | `c_conversiontypereval_id` | [`c_conversiontype`](c_conversiontype.md) | `c_conversiontype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
