# c_withholding — 원천징수 유형

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_withholding` |
| 한국어 논리명(문서용 해석) | 원천징수 유형 |
| 원본 논리명 | Withholding |
| 원본 사전 ID | 304 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 23 |
| 나가는 FK / 들어오는 FK | 2 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

거래에서 적용할 원천징수 유형을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Withholding type defined
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_withholding_pkey` | `c_withholding_id` |
| UNIQUE | `c_withholding_uu_idx` | `c_withholding_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_withholding_id` | Withholding | numeric(10,0) | 불가 | 예 | — | Withholding type defined |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `c_paymentterm_id` | Payment Term | numeric(10,0) | 불가 | — | — | The terms of Payment (timing, discount) |
| 12 | `istaxwithholding` | Tax withholding | character(1) | 불가 | — | 'Y'::bpchar | This is a tax related withholding |
| 13 | `istaxprorated` | Prorate tax | character(1) | 불가 | — | 'N'::bpchar | Tax is Prorated |
| 14 | `ispaidto3party` | Paid to third party | character(1) | 불가 | — | 'Y'::bpchar | Amount paid to someone other than the Business Partner |
| 15 | `beneficiary` | Beneficiary | numeric(10,0) | 허용 | — | — | Business Partner to whom payment is made |
| 16 | `ispercentwithholding` | Percent withholding | character(1) | 불가 | — | 'Y'::bpchar | Withholding amount is a percentage of the invoice amount |
| 17 | `percent` | Percent | numeric | 허용 | — | 0 | Percentage |
| 18 | `fixamt` | Fix amount | numeric | 허용 | — | 0 | Fix amounted amount to be levied or paid |
| 19 | `thresholdmin` | Threshold min | numeric | 허용 | — | 0 | Minimum gross amount for withholding calculation |
| 20 | `thresholdmax` | Threshold max | numeric | 허용 | — | 0 | Maximum gross amount for withholding calculation  (0=no limit) |
| 21 | `minamt` | Min Amount | numeric | 허용 | — | 0 | Minimum Amount in invoice currency |
| 22 | `maxamt` | Max Amount | numeric | 허용 | — | 0 | Maximum Amount in invoice currency |
| 23 | `c_withholding_uu` | C_Withholding_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_bp_withholding"]
    n1["c_bpartner"]
    n2["c_paymentterm"]
    n3["c_withholding"]
    n4["c_withholding_acct"]
    n3 -->|"beneficiary → c_bpartner_id"| n1
    n3 -->|"c_paymentterm_id → c_paymentterm_id"| n2
    n0 -->|"c_withholding_id → c_withholding_id"| n3
    n4 -->|"c_withholding_id → c_withholding_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `benefici_cwithholding` <!-- FK_OUT: adempiere.c_withholding.benefici_cwithholding --> | [`c_withholding`](c_withholding.md) | `beneficiary` | [`c_bpartner`](c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_cwithholding` <!-- FK_OUT: adempiere.c_withholding.cpaymentterm_cwithholding --> | [`c_withholding`](c_withholding.md) | `c_paymentterm_id` | [`c_paymentterm`](c_paymentterm.md) | `c_paymentterm_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cwithholding_cbpwithholding` <!-- FK_IN: adempiere.c_bp_withholding.cwithholding_cbpwithholding --> | [`c_bp_withholding`](c_bp_withholding.md) | `c_withholding_id` | [`c_withholding`](c_withholding.md) | `c_withholding_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cwithholding_cwithholdingacct` <!-- FK_IN: adempiere.c_withholding_acct.cwithholding_cwithholdingacct --> | [`c_withholding_acct`](c_withholding_acct.md) | `c_withholding_id` | [`c_withholding`](c_withholding.md) | `c_withholding_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
