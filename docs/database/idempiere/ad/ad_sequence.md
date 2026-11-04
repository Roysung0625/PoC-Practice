# ad_sequence — 문서 번호 채번

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_sequence` |
| 한국어 논리명(문서용 해석) | 문서 번호 채번 |
| 원본 논리명 | Sequence |
| 원본 사전 ID | 115 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 1,445 |
| 물리 열 수 | 27 |
| 나가는 FK / 들어오는 FK | 2 / 6 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

문서 번호를 생성하는 채번 규칙을 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Document Sequence
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_sequence_pkey` | `ad_sequence_id` |
| UNIQUE | `ad_sequence_uu_idx` | `ad_sequence_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_sequence_name`: `CREATE UNIQUE INDEX ad_sequence_name ON adempiere.ad_sequence USING btree (ad_client_id, name)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_sequence_id` | Sequence | numeric(10,0) | 불가 | 예 | — | Document Sequence |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 허용 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `vformat` | Value Format | character varying(40) | 허용 | — | — | Format of the value; Can contain fixed format elements, Variables: "_lLoOaAcCa09", or ~regex |
| 12 | `isautosequence` | Auto numbering | character(1) | 불가 | — | 'Y'::bpchar | Automatically assign the next number |
| 13 | `incrementno` | Increment | numeric(10,0) | 불가 | — | — | The number to increment the last document number by |
| 14 | `startno` | Start No | numeric(10,0) | 불가 | — | — | Starting number/position |
| 15 | `currentnext` | Current Next | numeric(10,0) | 불가 | — | — | The next number to be used |
| 16 | `currentnextsys` | Current Next (System) | numeric(10,0) | 불가 | — | — | Next sequence for system use |
| 17 | `isaudited` | Activate Audit | character(1) | 허용 | — | 'N'::bpchar | Activate Audit Trail of what numbers are generated |
| 18 | `istableid` | Used for Record ID | character(1) | 허용 | — | 'N'::bpchar | The document number  will be used as the record key |
| 19 | `prefix` | Prefix | character varying(255) | 허용 | — | — | Prefix before the sequence number |
| 20 | `suffix` | Suffix | character varying(255) | 허용 | — | — | Suffix after the number |
| 21 | `startnewyear` | Restart sequence every Year | character(1) | 허용 | — | 'N'::bpchar | Restart the sequence with Start on every 1/1 |
| 22 | `datecolumn` | Date Column | character varying(124) | 허용 | — | — | Fully qualified date column |
| 23 | `decimalpattern` | Decimal Pattern | character varying(40) | 허용 | — | — | Java Decimal Pattern |
| 24 | `ad_sequence_uu` | AD_Sequence_UU | uuid | 허용 | — | — | — |
| 25 | `startnewmonth` | Restart sequence every month | character(1) | 불가 | — | 'N'::bpchar | — |
| 26 | `isorglevelsequence` | Organization level | character(1) | 불가 | — | 'N'::bpchar | This sequence can be defined for each organization |
| 27 | `orgcolumn` | Org Column | character varying(124) | 허용 | — | — | Fully qualified Organization column (AD_Org_ID) |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_org"]
    n2["ad_sequence"]
    n3["ad_sequence_audit"]
    n4["ad_sequence_no"]
    n5["c_bp_edi"]
    n6["c_doctype"]
    n7["c_paymentprocessor"]
    n2 -->|"ad_client_id → ad_client_id"| n0
    n2 -->|"ad_org_id → ad_org_id"| n1
    n3 -->|"ad_sequence_id → ad_sequence_id"| n2
    n4 -->|"ad_sequence_id → ad_sequence_id"| n2
    n5 -->|"ad_sequence_id → ad_sequence_id"| n2
    n6 -->|"docnosequence_id → ad_sequence_id"| n2
    n6 -->|"definitesequence_id → ad_sequence_id"| n2
    n7 -->|"ad_sequence_id → ad_sequence_id"| n2
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `sequenceclient` <!-- FK_OUT: adempiere.ad_sequence.sequenceclient --> | [`ad_sequence`](ad_sequence.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sequenceorg` <!-- FK_OUT: adempiere.ad_sequence.sequenceorg --> | [`ad_sequence`](ad_sequence.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ad_sequence_sequenceaudit` <!-- FK_IN: adempiere.ad_sequence_audit.ad_sequence_sequenceaudit --> | [`ad_sequence_audit`](ad_sequence_audit.md) | `ad_sequence_id` | [`ad_sequence`](ad_sequence.md) | `ad_sequence_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_sequence_sequenceno` <!-- FK_IN: adempiere.ad_sequence_no.ad_sequence_sequenceno --> | [`ad_sequence_no`](ad_sequence_no.md) | `ad_sequence_id` | [`ad_sequence`](ad_sequence.md) | `ad_sequence_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adsequence_cbpedi` <!-- FK_IN: adempiere.c_bp_edi.adsequence_cbpedi --> | [`c_bp_edi`](../c/c_bp_edi.md) | `ad_sequence_id` | [`ad_sequence`](ad_sequence.md) | `ad_sequence_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_sequence_doctypedoc` <!-- FK_IN: adempiere.c_doctype.ad_sequence_doctypedoc --> | [`c_doctype`](../c/c_doctype.md) | `docnosequence_id` | [`ad_sequence`](ad_sequence.md) | `ad_sequence_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `definitesequence_cdoctype` <!-- FK_IN: adempiere.c_doctype.definitesequence_cdoctype --> | [`c_doctype`](../c/c_doctype.md) | `definitesequence_id` | [`ad_sequence`](ad_sequence.md) | `ad_sequence_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adsequence_cpaymentprocessor` <!-- FK_IN: adempiere.c_paymentprocessor.adsequence_cpaymentprocessor --> | [`c_paymentprocessor`](../c/c_paymentprocessor.md) | `ad_sequence_id` | [`ad_sequence`](ad_sequence.md) | `ad_sequence_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
