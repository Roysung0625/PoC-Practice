# ad_ref_list — 선택 목록 값

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_ref_list` |
| 한국어 논리명(문서용 해석) | 선택 목록 값 |
| 원본 논리명 | Reference List |
| 원본 사전 ID | 104 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 1,529 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 4 / 3 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

참조 선택 목록을 구성하는 값을 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Reference List based on Table
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_ref_list_pkey` | `ad_ref_list_id` |
| UNIQUE | `ad_ref_list_uu_idx` | `ad_ref_list_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_ref_list_name`: `CREATE UNIQUE INDEX ad_ref_list_name ON adempiere.ad_ref_list USING btree (ad_reference_id, name)`
- `ad_ref_list_value`: `CREATE UNIQUE INDEX ad_ref_list_value ON adempiere.ad_ref_list USING btree (ad_reference_id, value)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_ref_list_id` | Reference List | numeric(10,0) | 불가 | 예 | — | Reference List based on Table |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `value` | Search Key | character varying(60) | 불가 | — | — | Search key for the record in the format required - must be unique |
| 10 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `ad_reference_id` | Reference | numeric(10,0) | 불가 | — | — | System Reference and Validation |
| 13 | `validfrom` | Valid from | timestamp without time zone | 허용 | — | — | Valid from including this date (first day) |
| 14 | `validto` | Valid to | timestamp without time zone | 허용 | — | — | Valid to including this date (last day) |
| 15 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 16 | `ad_ref_list_uu` | AD_Ref_List_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_document_action_access"]
    n2["ad_entitytype"]
    n3["ad_org"]
    n4["ad_ref_list"]
    n5["ad_ref_list_trl"]
    n6["ad_reference"]
    n7["asp_ref_list"]
    n4 -->|"ad_reference_id → ad_reference_id"| n6
    n4 -->|"ad_client_id → ad_client_id"| n0
    n4 -->|"ad_org_id → ad_org_id"| n3
    n4 -->|"entitytype → entitytype"| n2
    n1 -->|"ad_ref_list_id → ad_ref_list_id"| n4
    n5 -->|"ad_ref_list_id → ad_ref_list_id"| n4
    n7 -->|"ad_ref_list_id → ad_ref_list_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ad_reference_reflist` <!-- FK_OUT: adempiere.ad_ref_list.ad_reference_reflist --> | [`ad_ref_list`](ad_ref_list.md) | `ad_reference_id` | [`ad_reference`](ad_reference.md) | `ad_reference_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_reflist_client` <!-- FK_OUT: adempiere.ad_ref_list.ad_reflist_client --> | [`ad_ref_list`](ad_ref_list.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_reflist_org` <!-- FK_OUT: adempiere.ad_ref_list.ad_reflist_org --> | [`ad_ref_list`](ad_ref_list.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adreflist` <!-- FK_OUT: adempiere.ad_ref_list.entityt_adreflist --> | [`ad_ref_list`](ad_ref_list.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adreflist_addocumentactionacce` <!-- FK_IN: adempiere.ad_document_action_access.adreflist_addocumentactionacce --> | [`ad_document_action_access`](ad_document_action_access.md) | `ad_ref_list_id` | [`ad_ref_list`](ad_ref_list.md) | `ad_ref_list_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_reflisttrl` <!-- FK_IN: adempiere.ad_ref_list_trl.ad_reflisttrl --> | [`ad_ref_list_trl`](ad_ref_list_trl.md) | `ad_ref_list_id` | [`ad_ref_list`](ad_ref_list.md) | `ad_ref_list_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adreflist_aspreflist` <!-- FK_IN: adempiere.asp_ref_list.adreflist_aspreflist --> | [`asp_ref_list`](../asp/asp_ref_list.md) | `ad_ref_list_id` | [`ad_ref_list`](ad_ref_list.md) | `ad_ref_list_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
