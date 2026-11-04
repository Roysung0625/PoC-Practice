# r_requesttype — 요청 유형

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.r_requesttype` |
| 한국어 논리명(문서용 해석) | 요청 유형 |
| 원본 논리명 | Request Type |
| 원본 사전 ID | 529 |
| 분류 | `r` — 요청·지원·상태 관리 |
| 전체 테넌트 행 수 | 3 |
| 물리 열 수 | 25 |
| 나가는 FK / 들어오는 FK | 1 / 9 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

문의·불만 등 요청의 업무 유형을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Type of request (e.g. Inquiry, Complaint, ..)
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `r_requesttype_pkey` | `r_requesttype_id` |
| UNIQUE | `r_requesttype_uu_idx` | `r_requesttype_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `r_requesttype_id` | Request Type | numeric(10,0) | 불가 | 예 | — | Type of request (e.g. Inquiry, Complaint, ..) |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `isdefault` | Default | character(1) | 불가 | — | 'N'::bpchar | Default value |
| 12 | `isselfservice` | Self-Service | character(1) | 불가 | — | 'Y'::bpchar | This is a Self-Service entry or this entry can be changed via Self-Service |
| 13 | `duedatetolerance` | Due Date Tolerance | numeric(10,0) | 불가 | — | 7 | Tolerance in days between the Date Next Action and the date the request is regarded as overdue |
| 14 | `isemailwhenoverdue` | EMail when Overdue | character(1) | 불가 | — | 'N'::bpchar | Send EMail when Request becomes overdue |
| 15 | `isemailwhendue` | EMail when Due | character(1) | 불가 | — | 'N'::bpchar | Send EMail when Request becomes due |
| 16 | `isinvoiced` | Invoiced | character(1) | 허용 | — | — | Is this invoiced? |
| 17 | `autoduedatedays` | Auto Due Date Days | numeric(10,0) | 허용 | — | — | Automatic Due Date Days |
| 18 | `confidentialtype` | Confidentiality | character(1) | 불가 | — | 'C'::bpchar | Type of Confidentiality |
| 19 | `isautochangerequest` | Create Change Request | character(1) | 불가 | — | 'N'::bpchar | Automatically create BOM (Engineering) Change Request |
| 20 | `isconfidentialinfo` | Confidential Info | character(1) | 불가 | — | 'N'::bpchar | Can enter confidential information |
| 21 | `r_statuscategory_id` | Status Category | numeric(10,0) | 불가 | — | — | Request Status Category |
| 22 | `isindexed` | Indexed | character(1) | 불가 | — | 'Y'::bpchar | Index the document for the internal search engine |
| 23 | `r_requesttype_uu` | R_RequestType_UU | uuid | 허용 | — | — | — |
| 24 | `headercolor` | Header Color | character varying(7) | 허용 | — | NULL::character varying | Header color of calendar dashlet |
| 25 | `contentcolor` | Content Color | character varying(7) | 허용 | — | NULL::character varying | Content color of calendar dashlet |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 10개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_userbpaccess"]
    n1["k_index"]
    n2["k_indexstop"]
    n3["pa_measure"]
    n4["r_request"]
    n5["r_requestaction"]
    n6["r_requestprocessor"]
    n7["r_requestprocessor_route"]
    n8["r_requesttype"]
    n9["r_requesttypeupdates"]
    n10["r_statuscategory"]
    n8 -->|"r_statuscategory_id → r_statuscategory_id"| n10
    n0 -->|"r_requesttype_id → r_requesttype_id"| n8
    n1 -->|"r_requesttype_id → r_requesttype_id"| n8
    n2 -->|"r_requesttype_id → r_requesttype_id"| n8
    n3 -->|"r_requesttype_id → r_requesttype_id"| n8
    n4 -->|"r_requesttype_id → r_requesttype_id"| n8
    n5 -->|"r_requesttype_id → r_requesttype_id"| n8
    n6 -->|"r_requesttype_id → r_requesttype_id"| n8
    n7 -->|"r_requesttype_id → r_requesttype_id"| n8
    n9 -->|"r_requesttype_id → r_requesttype_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `rstatuscategory_rrequesttype` <!-- FK_OUT: adempiere.r_requesttype.rstatuscategory_rrequesttype --> | [`r_requesttype`](r_requesttype.md) | `r_statuscategory_id` | [`r_statuscategory`](r_statuscategory.md) | `r_statuscategory_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `rrequesttype_aduserbpaccess` <!-- FK_IN: adempiere.ad_userbpaccess.rrequesttype_aduserbpaccess --> | [`ad_userbpaccess`](../ad/ad_userbpaccess.md) | `r_requesttype_id` | [`r_requesttype`](r_requesttype.md) | `r_requesttype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequesttype_kindex` <!-- FK_IN: adempiere.k_index.rrequesttype_kindex --> | [`k_index`](../k/k_index.md) | `r_requesttype_id` | [`r_requesttype`](r_requesttype.md) | `r_requesttype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequesttype_kindexstop` <!-- FK_IN: adempiere.k_indexstop.rrequesttype_kindexstop --> | [`k_indexstop`](../k/k_indexstop.md) | `r_requesttype_id` | [`r_requesttype`](r_requesttype.md) | `r_requesttype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequesttype_pameasure` <!-- FK_IN: adempiere.pa_measure.rrequesttype_pameasure --> | [`pa_measure`](../pa/pa_measure.md) | `r_requesttype_id` | [`r_requesttype`](r_requesttype.md) | `r_requesttype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequesttype_rrequest` <!-- FK_IN: adempiere.r_request.rrequesttype_rrequest --> | [`r_request`](r_request.md) | `r_requesttype_id` | [`r_requesttype`](r_requesttype.md) | `r_requesttype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequesttype_rrequestaction` <!-- FK_IN: adempiere.r_requestaction.rrequesttype_rrequestaction --> | [`r_requestaction`](r_requestaction.md) | `r_requesttype_id` | [`r_requesttype`](r_requesttype.md) | `r_requesttype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequesttype_rrequestprocessor` <!-- FK_IN: adempiere.r_requestprocessor.rrequesttype_rrequestprocessor --> | [`r_requestprocessor`](r_requestprocessor.md) | `r_requesttype_id` | [`r_requesttype`](r_requesttype.md) | `r_requesttype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequesttype_rprocessorrule` <!-- FK_IN: adempiere.r_requestprocessor_route.rrequesttype_rprocessorrule --> | [`r_requestprocessor_route`](r_requestprocessor_route.md) | `r_requesttype_id` | [`r_requesttype`](r_requesttype.md) | `r_requesttype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequesttype_rrtupdates` <!-- FK_IN: adempiere.r_requesttypeupdates.rrequesttype_rrtupdates --> | [`r_requesttypeupdates`](r_requesttypeupdates.md) | `r_requesttype_id` | [`r_requesttype`](r_requesttype.md) | `r_requesttype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
