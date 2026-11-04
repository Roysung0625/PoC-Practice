# ad_statuslineusedin — 상태 표시줄 적용 위치

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_statuslineusedin` |
| 한국어 논리명(문서용 해석) | 상태 표시줄 적용 위치 |
| 원본 논리명 | AD_StatusLineUsedIn |
| 원본 사전 ID | 200108 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 14 |
| 물리 열 수 | 17 |
| 나가는 FK / 들어오는 FK | 10 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

상태 표시줄을 적용할 창·탭·테이블·조회 창과 순서를 지정한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_statuslineusedin_key` | `ad_statuslineusedin_id` |
| UNIQUE | `ad_statuslineusedin_uu_idx` | `ad_statuslineusedin_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_statuslineusedin_id` | AD_StatusLineUsedIn | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `ad_statuslineusedin_uu` | AD_StatusLineUsedIn_UU | uuid | 허용 | — | — | — |
| 5 | `ad_statusline_id` | Status Line | numeric(10,0) | 불가 | — | — | — |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | — | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `updated` | Updated | timestamp without time zone | 불가 | — | — | Date this record was updated |
| 10 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 11 | `ad_window_id` | Window | numeric(10,0) | 허용 | — | NULL::numeric | Data entry or display window |
| 12 | `ad_tab_id` | Tab | numeric(10,0) | 허용 | — | NULL::numeric | Tab within a Window |
| 13 | `isstatusline` | Status Line | character(1) | 불가 | — | 'Y'::bpchar | Defines if this record refers to a status line or to a help widget |
| 14 | `seqno` | Sequence | numeric(10,0) | 허용 | — | NULL::numeric | Method of ordering records; lowest number comes first |
| 15 | `ad_table_id` | Table | numeric(10,0) | 허용 | — | NULL::numeric | Database Table information |
| 16 | `entitytype` | Entity Type | character varying(40) | 허용 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 17 | `ad_infowindow_id` | Info Window | numeric(10,0) | 허용 | — | NULL::numeric | Info and search/select Window |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 10개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_entitytype"]
    n2["ad_infowindow"]
    n3["ad_org"]
    n4["ad_statusline"]
    n5["ad_statuslineusedin"]
    n6["ad_tab"]
    n7["ad_table"]
    n8["ad_user"]
    n9["ad_window"]
    n5 -->|"ad_client_id → ad_client_id"| n0
    n5 -->|"ad_infowindow_id → ad_infowindow_id"| n2
    n5 -->|"ad_org_id → ad_org_id"| n3
    n5 -->|"ad_statusline_id → ad_statusline_id"| n4
    n5 -->|"ad_tab_id → ad_tab_id"| n6
    n5 -->|"ad_table_id → ad_table_id"| n7
    n5 -->|"ad_window_id → ad_window_id"| n9
    n5 -->|"createdby → ad_user_id"| n8
    n5 -->|"entitytype → entitytype"| n1
    n5 -->|"updatedby → ad_user_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adclient_adstatuslineusedin` <!-- FK_OUT: adempiere.ad_statuslineusedin.adclient_adstatuslineusedin --> | [`ad_statuslineusedin`](ad_statuslineusedin.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adinfowindow_adstatuslineusedi` <!-- FK_OUT: adempiere.ad_statuslineusedin.adinfowindow_adstatuslineusedi --> | [`ad_statuslineusedin`](ad_statuslineusedin.md) | `ad_infowindow_id` | [`ad_infowindow`](ad_infowindow.md) | `ad_infowindow_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorg_adstatuslineusedin` <!-- FK_OUT: adempiere.ad_statuslineusedin.adorg_adstatuslineusedin --> | [`ad_statuslineusedin`](ad_statuslineusedin.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adstatusline_adstatuslineusedi` <!-- FK_OUT: adempiere.ad_statuslineusedin.adstatusline_adstatuslineusedi --> | [`ad_statuslineusedin`](ad_statuslineusedin.md) | `ad_statusline_id` | [`ad_statusline`](ad_statusline.md) | `ad_statusline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtab_adstatuslineusedin` <!-- FK_OUT: adempiere.ad_statuslineusedin.adtab_adstatuslineusedin --> | [`ad_statuslineusedin`](ad_statuslineusedin.md) | `ad_tab_id` | [`ad_tab`](ad_tab.md) | `ad_tab_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtable_adstatuslineusedin` <!-- FK_OUT: adempiere.ad_statuslineusedin.adtable_adstatuslineusedin --> | [`ad_statuslineusedin`](ad_statuslineusedin.md) | `ad_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwindow_adstatuslineusedin` <!-- FK_OUT: adempiere.ad_statuslineusedin.adwindow_adstatuslineusedin --> | [`ad_statuslineusedin`](ad_statuslineusedin.md) | `ad_window_id` | [`ad_window`](ad_window.md) | `ad_window_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `createdby_adstatuslineusedin` <!-- FK_OUT: adempiere.ad_statuslineusedin.createdby_adstatuslineusedin --> | [`ad_statuslineusedin`](ad_statuslineusedin.md) | `createdby` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entitytype_adstatuslineusedin` <!-- FK_OUT: adempiere.ad_statuslineusedin.entitytype_adstatuslineusedin --> | [`ad_statuslineusedin`](ad_statuslineusedin.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `updatedby_adstatuslineusedin` <!-- FK_OUT: adempiere.ad_statuslineusedin.updatedby_adstatuslineusedin --> | [`ad_statuslineusedin`](ad_statuslineusedin.md) | `updatedby` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
