# r_group — 요청 그룹

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.r_group` |
| 한국어 논리명(문서용 해석) | 요청 그룹 |
| 원본 논리명 | Group |
| 원본 사전 ID | 773 |
| 분류 | `r` — 요청·지원·상태 관리 |
| 전체 테넌트 행 수 | 2 |
| 물리 열 수 | 15 |
| 나가는 FK / 들어오는 FK | 3 / 3 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

요청을 함께 관리하는 그룹을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Request Group
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `r_group_pkey` | `r_group_id` |
| UNIQUE | `r_group_uu_idx` | `r_group_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `r_group_id` | Group | numeric(10,0) | 불가 | 예 | — | Request Group |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 12 | `m_bom_id` | — | numeric(10,0) | 허용 | — | — | — |
| 13 | `m_changenotice_id` | Change Notice | numeric(10,0) | 허용 | — | — | Bill of Materials (Engineering) Change Notice (Version) |
| 14 | `pp_product_bom_id` | BOM &amp; Formula | numeric(10,0) | 허용 | — | — | BOM &amp; Formula |
| 15 | `r_group_uu` | R_Group_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 6개 중 6개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["m_bom"]
    n1["m_changenotice"]
    n2["pp_product_bom"]
    n3["r_group"]
    n4["r_groupupdates"]
    n5["r_request"]
    n6["r_requestaction"]
    n3 -->|"m_bom_id → m_bom_id"| n0
    n3 -->|"m_changenotice_id → m_changenotice_id"| n1
    n3 -->|"pp_product_bom_id → pp_product_bom_id"| n2
    n4 -->|"r_group_id → r_group_id"| n3
    n5 -->|"r_group_id → r_group_id"| n3
    n6 -->|"r_group_id → r_group_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mbom_rgroup` <!-- FK_OUT: adempiere.r_group.mbom_rgroup --> | [`r_group`](r_group.md) | `m_bom_id` | [`m_bom`](../m/m_bom.md) | `m_bom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mchangenotice_rgroup` <!-- FK_OUT: adempiere.r_group.mchangenotice_rgroup --> | [`r_group`](r_group.md) | `m_changenotice_id` | [`m_changenotice`](../m/m_changenotice.md) | `m_changenotice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ppproductbom_rgroup` <!-- FK_OUT: adempiere.r_group.ppproductbom_rgroup --> | [`r_group`](r_group.md) | `pp_product_bom_id` | [`pp_product_bom`](../pp/pp_product_bom.md) | `pp_product_bom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `rgroup_rgroupupdates` <!-- FK_IN: adempiere.r_groupupdates.rgroup_rgroupupdates --> | [`r_groupupdates`](r_groupupdates.md) | `r_group_id` | [`r_group`](r_group.md) | `r_group_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rgroup_rrequest` <!-- FK_IN: adempiere.r_request.rgroup_rrequest --> | [`r_request`](r_request.md) | `r_group_id` | [`r_group`](r_group.md) | `r_group_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rgroup_rrequestaction` <!-- FK_IN: adempiere.r_requestaction.rgroup_rrequestaction --> | [`r_requestaction`](r_requestaction.md) | `r_group_id` | [`r_group`](r_group.md) | `r_group_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
