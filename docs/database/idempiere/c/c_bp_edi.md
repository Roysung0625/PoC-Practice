# c_bp_edi — 거래처 EDI 정의

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_bp_edi` |
| 한국어 논리명(문서용 해석) | 거래처 EDI 정의 |
| 원본 논리명 | EDI Definition |
| 원본 사전 ID | 366 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 28 |
| 나가는 FK / 들어오는 FK | 3 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

거래처와의 전자문서 교환을 위한 EDI 정의를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Electronic Data Interchange
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_bp_edi_pkey` | `c_bp_edi_id` |
| UNIQUE | `c_bp_edi_uu_idx` | `c_bp_edi_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_bp_edi_id` | EDI Definition | numeric(10,0) | 불가 | 예 | — | Electronic Data Interchange |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `c_bpartner_id` | Business Partner | numeric(10,0) | 불가 | — | — | Identifies a Business Partner |
| 12 | `m_warehouse_id` | Warehouse | numeric(10,0) | 불가 | — | — | Storage Warehouse and Service Point |
| 13 | `editype` | EDI Type | character(1) | 불가 | — | — | — |
| 14 | `isaudited` | Activate Audit | character(1) | 불가 | — | 'N'::bpchar | Activate Audit Trail of what numbers are generated |
| 15 | `customerno` | Customer No | character varying(20) | 불가 | — | — | EDI Identification Number  |
| 16 | `ad_sequence_id` | Sequence | numeric(10,0) | 불가 | — | — | Document Sequence |
| 17 | `email_to` | To EMail | character varying(60) | 허용 | — | — | EMail address to send requests to - e.g. edi@manufacturer.com  |
| 18 | `email_from` | From EMail | character varying(60) | 허용 | — | — | Full EMail address used to send requests - e.g. edi@organization.com |
| 19 | `email_from_uid` | From EMail User ID | character varying(20) | 허용 | — | — | User ID of the sending EMail address (on default SMTP Host) - e.g. edi |
| 20 | `email_from_pwd` | From EMail Password | character varying(20) | 허용 | — | — | Password of the sending EMail address |
| 21 | `email_error_to` | Error EMail | character varying(60) | 불가 | — | — | Email address to send error messages to |
| 22 | `isinfosent` | Send Info | character(1) | 불가 | — | 'N'::bpchar | Send informational messages and copies |
| 23 | `email_info_to` | Info EMail | character varying(60) | 불가 | — | — | EMail address to send informational messages and copies |
| 24 | `sendinquiry` | Send Inquiry | character(1) | 불가 | — | 'Y'::bpchar | Quantity Availability Inquiry |
| 25 | `receiveinquiryreply` | Received Inquiry Reply | character(1) | 불가 | — | 'Y'::bpchar | — |
| 26 | `sendorder` | Send Order | character(1) | 불가 | — | 'Y'::bpchar | — |
| 27 | `receiveorderreply` | Receive Order Reply | character(1) | 불가 | — | 'Y'::bpchar | — |
| 28 | `c_bp_edi_uu` | C_BP_EDI_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_sequence"]
    n1["c_bp_edi"]
    n2["c_bpartner"]
    n3["m_edi"]
    n4["m_warehouse"]
    n1 -->|"ad_sequence_id → ad_sequence_id"| n0
    n1 -->|"c_bpartner_id → c_bpartner_id"| n2
    n1 -->|"m_warehouse_id → m_warehouse_id"| n4
    n3 -->|"c_bp_edi_id → c_bp_edi_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adsequence_cbpedi` <!-- FK_OUT: adempiere.c_bp_edi.adsequence_cbpedi --> | [`c_bp_edi`](c_bp_edi.md) | `ad_sequence_id` | [`ad_sequence`](../ad/ad_sequence.md) | `ad_sequence_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_bpartner_cbpedi` <!-- FK_OUT: adempiere.c_bp_edi.c_bpartner_cbpedi --> | [`c_bp_edi`](c_bp_edi.md) | `c_bpartner_id` | [`c_bpartner`](c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_cbpedi` <!-- FK_OUT: adempiere.c_bp_edi.mwarehouse_cbpedi --> | [`c_bp_edi`](c_bp_edi.md) | `m_warehouse_id` | [`m_warehouse`](../m/m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cbpedi_medi` <!-- FK_IN: adempiere.m_edi.cbpedi_medi --> | [`m_edi`](../m/m_edi.md) | `c_bp_edi_id` | [`c_bp_edi`](c_bp_edi.md) | `c_bp_edi_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
