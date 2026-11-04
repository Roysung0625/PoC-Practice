# k_index — 검색 색인

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.k_index` |
| 한국어 논리명(문서용 해석) | 검색 색인 |
| 원본 논리명 | Index |
| 원본 사전 ID | 900 |
| 분류 | `k` — 지식·분류·문서 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 17 |
| 나가는 FK / 들어오는 FK | 4 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

키워드·발췌문과 원본 테이블·레코드 식별자를 연결하는 검색 색인 정보를 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `k_index_pkey` | `k_index_id` |
| UNIQUE | `k_index_uu_idx` | `k_index_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `k_index_id` | Index | numeric(10,0) | 불가 | 예 | — | Text Search Index |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `keyword` | Keyword | character varying(255) | 불가 | — | — | Case insensitive keyword |
| 10 | `excerpt` | Excerpt | character varying(2000) | 허용 | — | — | Surrounding text of the keyword |
| 11 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 12 | `record_id` | Record ID | numeric(10,0) | 불가 | — | — | Direct internal record ID |
| 13 | `sourceupdated` | Source Updated | timestamp without time zone | 불가 | — | now() | Date the source document was updated |
| 14 | `cm_webproject_id` | Web Project | numeric(10,0) | 허용 | — | — | A web project is the main data container for Containers, URLs, Ads, Media etc. |
| 15 | `r_requesttype_id` | Request Type | numeric(10,0) | 허용 | — | — | Type of request (e.g. Inquiry, Complaint, ..) |
| 16 | `c_doctype_id` | Document Type | numeric(10,0) | 허용 | — | — | Document type or rules |
| 17 | `k_index_uu` | K_Index_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_table"]
    n1["c_doctype"]
    n2["cm_webproject"]
    n3["k_index"]
    n4["r_requesttype"]
    n3 -->|"ad_table_id → ad_table_id"| n0
    n3 -->|"c_doctype_id → c_doctype_id"| n1
    n3 -->|"cm_webproject_id → cm_webproject_id"| n2
    n3 -->|"r_requesttype_id → r_requesttype_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adtable_kindex` <!-- FK_OUT: adempiere.k_index.adtable_kindex --> | [`k_index`](k_index.md) | `ad_table_id` | [`ad_table`](../ad/ad_table.md) | `ad_table_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_kindex` <!-- FK_OUT: adempiere.k_index.cdoctype_kindex --> | [`k_index`](k_index.md) | `c_doctype_id` | [`c_doctype`](../c/c_doctype.md) | `c_doctype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cmwebproject_kindex` <!-- FK_OUT: adempiere.k_index.cmwebproject_kindex --> | [`k_index`](k_index.md) | `cm_webproject_id` | [`cm_webproject`](../cm/cm_webproject.md) | `cm_webproject_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequesttype_kindex` <!-- FK_OUT: adempiere.k_index.rrequesttype_kindex --> | [`k_index`](k_index.md) | `r_requesttype_id` | [`r_requesttype`](../r/r_requesttype.md) | `r_requesttype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `record_id`는 가리키는 테이블이 메타데이터에 따라 달라질 수 있습니다. 물리 FK 목록에 없는 대상은 별도 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
