# ws_webservicetype — 웹 서비스 유형

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ws_webservicetype` |
| 한국어 논리명(문서용 해석) | 웹 서비스 유형 |
| 원본 논리명 | Web Service Type |
| 원본 사전 ID | 53164 |
| 분류 | `ws` — 웹 서비스 |
| 전체 테넌트 행 수 | 16 |
| 물리 열 수 | 17 |
| 나가는 FK / 들어오는 FK | 3 / 4 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

서비스와 메서드를 대상 테이블 및 매개변수 삽입 설정에 연결한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ws_webservicetype_key` | `ws_webservicetype_id` |
| UNIQUE | `ws_webservicetype_uu_idx` | `ws_webservicetype_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ws_webservicetype_value_idx`: `CREATE UNIQUE INDEX ws_webservicetype_value_idx ON adempiere.ws_webservicetype USING btree (value, ad_client_id)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_table_id` | Table | numeric(10,0) | 허용 | — | — | Database Table information |
| 4 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 5 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 6 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 7 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 11 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 12 | `value` | Search Key | character varying(40) | 불가 | — | — | Search key for the record in the format required - must be unique |
| 13 | `ws_webservice_id` | Web Service | numeric(10,0) | 불가 | — | — | — |
| 14 | `ws_webservicemethod_id` | Web Service Method | numeric(10,0) | 불가 | — | — | — |
| 15 | `ws_webservicetype_id` | Web Service Type | numeric(10,0) | 불가 | 예 | — | — |
| 16 | `ws_webservicetype_uu` | WS_WebServiceType_UU | uuid | 허용 | — | — | — |
| 17 | `insertparameters` | Create Default Parameters | character(1) | 허용 | — | NULL::bpchar | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_table"]
    n1["ws_webservice"]
    n2["ws_webservice_para"]
    n3["ws_webservicefieldinput"]
    n4["ws_webservicefieldoutput"]
    n5["ws_webservicemethod"]
    n6["ws_webservicetype"]
    n7["ws_webservicetypeaccess"]
    n6 -->|"ad_table_id → ad_table_id"| n0
    n6 -->|"ws_webservice_id → ws_webservice_id"| n1
    n6 -->|"ws_webservicemethod_id → ws_webservicemethod_id"| n5
    n2 -->|"ws_webservicetype_id → ws_webservicetype_id"| n6
    n3 -->|"ws_webservicetype_id → ws_webservicetype_id"| n6
    n4 -->|"ws_webservicetype_id → ws_webservicetype_id"| n6
    n7 -->|"ws_webservicetype_id → ws_webservicetype_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adtable_wswebservicetype` <!-- FK_OUT: adempiere.ws_webservicetype.adtable_wswebservicetype --> | [`ws_webservicetype`](ws_webservicetype.md) | `ad_table_id` | [`ad_table`](../ad/ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `wswebservice_wswebservicetype` <!-- FK_OUT: adempiere.ws_webservicetype.wswebservice_wswebservicetype --> | [`ws_webservicetype`](ws_webservicetype.md) | `ws_webservice_id` | [`ws_webservice`](ws_webservice.md) | `ws_webservice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `wswebservicemethod_wswebservic` <!-- FK_OUT: adempiere.ws_webservicetype.wswebservicemethod_wswebservic --> | [`ws_webservicetype`](ws_webservicetype.md) | `ws_webservicemethod_id` | [`ws_webservicemethod`](ws_webservicemethod.md) | `ws_webservicemethod_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `wswebservicetype_wswebservicep` <!-- FK_IN: adempiere.ws_webservice_para.wswebservicetype_wswebservicep --> | [`ws_webservice_para`](ws_webservice_para.md) | `ws_webservicetype_id` | [`ws_webservicetype`](ws_webservicetype.md) | `ws_webservicetype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `wswebservicetype_wswebservicfi` <!-- FK_IN: adempiere.ws_webservicefieldinput.wswebservicetype_wswebservicfi --> | [`ws_webservicefieldinput`](ws_webservicefieldinput.md) | `ws_webservicetype_id` | [`ws_webservicetype`](ws_webservicetype.md) | `ws_webservicetype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `wswebservicetype_wswebservicfo` <!-- FK_IN: adempiere.ws_webservicefieldoutput.wswebservicetype_wswebservicfo --> | [`ws_webservicefieldoutput`](ws_webservicefieldoutput.md) | `ws_webservicetype_id` | [`ws_webservicetype`](ws_webservicetype.md) | `ws_webservicetype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `wswebservicetype_wswebservicet` <!-- FK_IN: adempiere.ws_webservicetypeaccess.wswebservicetype_wswebservicet --> | [`ws_webservicetypeaccess`](ws_webservicetypeaccess.md) | `ws_webservicetype_id` | [`ws_webservicetype`](ws_webservicetype.md) | `ws_webservicetype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
