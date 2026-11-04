# ad_broadcastmessage — 전체 공지

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_broadcastmessage` |
| 한국어 논리명(문서용 해석) | 전체 공지 |
| 원본 논리명 | Broadcast Message |
| 원본 사전 ID | 200038 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 25 |
| 나가는 FK / 들어오는 FK | 3 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

시스템 사용자에게 전달할 공지 메시지를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Broadcast Messages for system users
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_broadcastmessage_key` | `ad_broadcastmessage_id` |
| UNIQUE | `ad_broadcastmessage_uu_idx` | `ad_broadcastmessage_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 4 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 5 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 6 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 7 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 8 | `broadcastfrequency` | Broadcast Frequency | character varying(60) | 불가 | — | NULL::character varying | How Many Times Message Should be Broadcasted |
| 9 | `broadcastmessage` | Broadcast Message | text | 불가 | — | — | Broadcast Message |
| 10 | `broadcasttype` | Broadcast Type | character varying(32) | 불가 | — | NULL::character varying | Type of Broadcast |
| 11 | `expiration` | Expire On | timestamp without time zone | 허용 | — | — | Expire On |
| 12 | `logacknowledge` | Log Acknowledge | character(1) | 허용 | — | 'N'::bpchar | Want to Log the Acknowledgment of Message? |
| 13 | `target` | Target | character varying(60) | 불가 | — | NULL::character varying | Target tenant |
| 14 | `ad_role_id` | Role | numeric(10,0) | 허용 | — | NULL::numeric | Responsibility Role |
| 15 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | NULL::numeric | User within the system - Internal or Business Partner Contact |
| 16 | `testmessage` | Test Message | character(1) | 허용 | — | NULL::bpchar | Test broadcast message |
| 17 | `publish` | Publish | character(1) | 허용 | — | NULL::bpchar | Publish Broadcast Message |
| 18 | `expirenow` | Expire Now | character(1) | 허용 | — | — | Expire the broadcast message |
| 19 | `ad_broadcastmessage_id` | Broadcast Message | numeric(10,0) | 불가 | 예 | NULL::numeric | Broadcast Message |
| 20 | `ispublished` | Published | character(1) | 허용 | — | 'N'::bpchar | The Topic is published and can be viewed |
| 21 | `processed` | Processed | character(1) | 허용 | — | 'N'::bpchar | The document has been processed |
| 22 | `expired` | Expired | character(1) | 허용 | — | 'N'::bpchar | — |
| 23 | `ad_broadcastmessage_uu` | AD_BroadcastMessage_UU | uuid | 허용 | — | — | — |
| 24 | `notification_client_id` | Notification Tenant | numeric(10,0) | 허용 | — | — | Notification Tenant |
| 25 | `title` | Title | character varying(60) | 허용 | — | NULL::character varying | Name this entity is referred to as |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_broadcastmessage"]
    n1["ad_broadcastmessage_trl"]
    n2["ad_client"]
    n3["ad_note"]
    n4["ad_role"]
    n5["ad_user"]
    n0 -->|"ad_role_id → ad_role_id"| n4
    n0 -->|"ad_user_id → ad_user_id"| n5
    n0 -->|"notification_client_id → ad_client_id"| n2
    n1 -->|"ad_broadcastmessage_id → ad_broadcastmessage_id"| n0
    n3 -->|"ad_broadcastmessage_id → ad_broadcastmessage_id"| n0
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adrole_adbroadcastmessage` <!-- FK_OUT: adempiere.ad_broadcastmessage.adrole_adbroadcastmessage --> | [`ad_broadcastmessage`](ad_broadcastmessage.md) | `ad_role_id` | [`ad_role`](ad_role.md) | `ad_role_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduser_adbroadcastmessage` <!-- FK_OUT: adempiere.ad_broadcastmessage.aduser_adbroadcastmessage --> | [`ad_broadcastmessage`](ad_broadcastmessage.md) | `ad_user_id` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `notificationclient_adbroadcast` <!-- FK_OUT: adempiere.ad_broadcastmessage.notificationclient_adbroadcast --> | [`ad_broadcastmessage`](ad_broadcastmessage.md) | `notification_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adbroadcastmessage_adbroadcast` <!-- FK_IN: adempiere.ad_broadcastmessage_trl.adbroadcastmessage_adbroadcast --> | [`ad_broadcastmessage_trl`](ad_broadcastmessage_trl.md) | `ad_broadcastmessage_id` | [`ad_broadcastmessage`](ad_broadcastmessage.md) | `ad_broadcastmessage_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adbroadcastmessage_adnote` <!-- FK_IN: adempiere.ad_note.adbroadcastmessage_adnote --> | [`ad_note`](ad_note.md) | `ad_broadcastmessage_id` | [`ad_broadcastmessage`](ad_broadcastmessage.md) | `ad_broadcastmessage_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
