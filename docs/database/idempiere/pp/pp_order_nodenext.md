# pp_order_nodenext — 제조 주문 공정 전이

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.pp_order_nodenext` |
| 한국어 논리명(문서용 해석) | 제조 주문 공정 전이 |
| 원본 논리명 | Manufacturing Order Activity Next |
| 원본 사전 ID | 53023 |
| 분류 | `pp` — 제조·생산 계획·제품 구성 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 19 |
| 나가는 FK / 들어오는 FK | 6 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제조 주문에서 현재 공정과 다음 공정의 연결을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Manufacturing Order Activity Next
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `pp_order_nodenext_key` | `pp_order_nodenext_id` |
| UNIQUE | `pp_order_nodenext_uu_idx` | `pp_order_nodenext_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_wf_next_id` | Next Node | numeric(10,0) | 허용 | — | — | Next Node in workflow |
| 4 | `ad_wf_node_id` | Node | numeric(10,0) | 불가 | — | — | Workflow Node (activity), step or process |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 허용 | — | — | User who created this records |
| 7 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 8 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 9 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 10 | `isstduserworkflow` | Std User Workflow | character(1) | 허용 | — | — | Standard Manual User Approval Workflow |
| 11 | `pp_order_id` | Manufacturing Order | numeric(10,0) | 불가 | — | — | Manufacturing Order |
| 12 | `pp_order_next_id` | Manufacturing Order Activity Next | numeric(10,0) | 허용 | — | — | — |
| 13 | `pp_order_nodenext_id` | Manufacturing Order Activity Next | numeric(10,0) | 불가 | 예 | — | — |
| 14 | `pp_order_node_id` | Manufacturing Order Activity | numeric(10,0) | 불가 | — | — | Workflow Node (activity), step or process |
| 15 | `seqno` | Sequence | numeric(10,0) | 불가 | — | (10)::numeric | Method of ordering records; lowest number comes first |
| 16 | `transitioncode` | Transition Code | character varying(2000) | 허용 | — | — | Code resulting in TRUE of FALSE |
| 17 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 18 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 19 | `pp_order_nodenext_uu` | PP_Order_NodeNext_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 6개 중 6개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_entitytype"]
    n1["ad_wf_node"]
    n2["pp_order"]
    n3["pp_order_node"]
    n4["pp_order_nodenext"]
    n4 -->|"ad_wf_next_id → ad_wf_node_id"| n1
    n4 -->|"ad_wf_node_id → ad_wf_node_id"| n1
    n4 -->|"entitytype → entitytype"| n0
    n4 -->|"pp_order_id → pp_order_id"| n2
    n4 -->|"pp_order_next_id → pp_order_node_id"| n3
    n4 -->|"pp_order_node_id → pp_order_node_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adwfnext_ppordernodenext` <!-- FK_OUT: adempiere.pp_order_nodenext.adwfnext_ppordernodenext --> | [`pp_order_nodenext`](pp_order_nodenext.md) | `ad_wf_next_id` | [`ad_wf_node`](../ad/ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_ppordernodenext` <!-- FK_OUT: adempiere.pp_order_nodenext.adwfnode_ppordernodenext --> | [`pp_order_nodenext`](pp_order_nodenext.md) | `ad_wf_node_id` | [`ad_wf_node`](../ad/ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_ppordernodenext` <!-- FK_OUT: adempiere.pp_order_nodenext.entityt_ppordernodenext --> | [`pp_order_nodenext`](pp_order_nodenext.md) | `entitytype` | [`ad_entitytype`](../ad/ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pporder_ppordernodenext` <!-- FK_OUT: adempiere.pp_order_nodenext.pporder_ppordernodenext --> | [`pp_order_nodenext`](pp_order_nodenext.md) | `pp_order_id` | [`pp_order`](pp_order.md) | `pp_order_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ppordernext_ppordernodenext` <!-- FK_OUT: adempiere.pp_order_nodenext.ppordernext_ppordernodenext --> | [`pp_order_nodenext`](pp_order_nodenext.md) | `pp_order_next_id` | [`pp_order_node`](pp_order_node.md) | `pp_order_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ppordernode_ppordernodenext` <!-- FK_OUT: adempiere.pp_order_nodenext.ppordernode_ppordernodenext --> | [`pp_order_nodenext`](pp_order_nodenext.md) | `pp_order_node_id` | [`pp_order_node`](pp_order_node.md) | `pp_order_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
