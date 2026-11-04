# c_revenuerecog_service — 서비스 수익 인식 계획

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_revenuerecog_service` |
| 한국어 논리명(문서용 해석) | 서비스 수익 인식 계획 |
| 원본 논리명 | Revenue Recognition Service |
| 원본 사전 ID | 53888 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 13 |
| 나가는 FK / 들어오는 FK | 5 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

서비스를 기준으로 수익을 인식하거나 기록하는 계획을 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Plan for recognizing or recording revenue based on service
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_revenuerecog_service_key` | `c_revenuerecog_service_id` |
| UNIQUE | `c_revenuerecog_service_uu_idx` | `c_revenuerecog_service_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `created` | Created | timestamp without time zone | 불가 | — | — | Date this record was created |
| 4 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 5 | `c_revenuerecognition_id` | Revenue Recognition | numeric(10,0) | 불가 | — | — | Method for recording revenue |
| 6 | `c_revenuerecog_service_id` | Revenue Recognition Service | numeric(10,0) | 불가 | 예 | — | — |
| 7 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 8 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 9 | `line` | Line No | numeric(10,0) | 허용 | — | NULL::numeric | Unique line for this document |
| 10 | `percent` | Percent | numeric | 허용 | — | — | Percentage |
| 11 | `updated` | Updated | timestamp without time zone | 불가 | — | — | Date this record was updated |
| 12 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 13 | `c_revenuerecog_service_uu` | C_RevenueRecog_Service_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 6개 중 6개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_org"]
    n2["ad_user"]
    n3["c_revenuerecog_service"]
    n4["c_revenuerecognition"]
    n5["c_revenuerecognition_run"]
    n3 -->|"ad_client_id → ad_client_id"| n0
    n3 -->|"ad_org_id → ad_org_id"| n1
    n3 -->|"createdby → ad_user_id"| n2
    n3 -->|"c_revenuerecognition_id → c_revenuerecognition_id"| n4
    n3 -->|"updatedby → ad_user_id"| n2
    n5 -->|"c_revenuerecog_service_id → c_revenuerecog_service_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adclient_crevenuerecogservice` <!-- FK_OUT: adempiere.c_revenuerecog_service.adclient_crevenuerecogservice --> | [`c_revenuerecog_service`](c_revenuerecog_service.md) | `ad_client_id` | [`ad_client`](../ad/ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorg_crevenuerecogservice` <!-- FK_OUT: adempiere.c_revenuerecog_service.adorg_crevenuerecogservice --> | [`c_revenuerecog_service`](c_revenuerecog_service.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `createdby_crevenuerecogservice` <!-- FK_OUT: adempiere.c_revenuerecog_service.createdby_crevenuerecogservice --> | [`c_revenuerecog_service`](c_revenuerecog_service.md) | `createdby` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `crevenuerecognition_crevenuere` <!-- FK_OUT: adempiere.c_revenuerecog_service.crevenuerecognition_crevenuere --> | [`c_revenuerecog_service`](c_revenuerecog_service.md) | `c_revenuerecognition_id` | [`c_revenuerecognition`](c_revenuerecognition.md) | `c_revenuerecognition_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `updatedby_crevenuerecogservice` <!-- FK_OUT: adempiere.c_revenuerecog_service.updatedby_crevenuerecogservice --> | [`c_revenuerecog_service`](c_revenuerecog_service.md) | `updatedby` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `crevenuerecogservice_crevenuer` <!-- FK_IN: adempiere.c_revenuerecognition_run.crevenuerecogservice_crevenuer --> | [`c_revenuerecognition_run`](c_revenuerecognition_run.md) | `c_revenuerecog_service_id` | [`c_revenuerecog_service`](c_revenuerecog_service.md) | `c_revenuerecog_service_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
