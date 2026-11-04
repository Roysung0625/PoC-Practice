# c_countrygroup — 국가 그룹

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.c_countrygroup` |
| 한국어 논리명(문서용 해석) | 국가 그룹 |
| 원본 논리명 | Country Group |
| 원본 사전 ID | 200146 |
| 분류 | `c` — 거래처·주문·청구·결제·회계 기준 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 15 |
| 나가는 FK / 들어오는 FK | 4 / 4 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

조세 협정 등 공통 조건을 공유하는 국가 집합을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Group of countries that share common needs like tax agreements
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `c_countrygroup_key` | `c_countrygroup_id` |
| UNIQUE | `c_countrygroup_uu_idx` | `c_countrygroup_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `c_countrygroup_id` | Country Group | numeric(10,0) | 불가 | 예 | — | — |
| 4 | `c_countrygroup_uu` | C_CountryGroup_UU | uuid | 허용 | — | — | — |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `datefrom` | Date From | timestamp without time zone | 허용 | — | — | Starting date for a range |
| 8 | `dateto` | Date To | timestamp without time zone | 허용 | — | — | End date of a date range |
| 9 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 10 | `help` | Comment/Help | character varying(2000) | 허용 | — | NULL::character varying | Comment or Hint |
| 11 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 12 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 13 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 14 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 15 | `value` | Search Key | character varying(40) | 불가 | — | — | Search key for the record in the format required - must be unique |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 8개 중 8개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_org"]
    n2["ad_user"]
    n3["c_countrygroup"]
    n4["c_countrygroup_trl"]
    n5["c_countrygroupcountry"]
    n6["c_tax"]
    n3 -->|"ad_client_id → ad_client_id"| n0
    n3 -->|"ad_org_id → ad_org_id"| n1
    n3 -->|"createdby → ad_user_id"| n2
    n3 -->|"updatedby → ad_user_id"| n2
    n4 -->|"c_countrygroup_id → c_countrygroup_id"| n3
    n5 -->|"c_countrygroup_id → c_countrygroup_id"| n3
    n6 -->|"c_countrygroupfrom_id → c_countrygroup_id"| n3
    n6 -->|"c_countrygroupto_id → c_countrygroup_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adclient_ccountrygroup` <!-- FK_OUT: adempiere.c_countrygroup.adclient_ccountrygroup --> | [`c_countrygroup`](c_countrygroup.md) | `ad_client_id` | [`ad_client`](../ad/ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorg_ccountrygroup` <!-- FK_OUT: adempiere.c_countrygroup.adorg_ccountrygroup --> | [`c_countrygroup`](c_countrygroup.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `createdby_ccountrygroup` <!-- FK_OUT: adempiere.c_countrygroup.createdby_ccountrygroup --> | [`c_countrygroup`](c_countrygroup.md) | `createdby` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `updatedby_ccountrygroup` <!-- FK_OUT: adempiere.c_countrygroup.updatedby_ccountrygroup --> | [`c_countrygroup`](c_countrygroup.md) | `updatedby` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccountrygroup_ccountrygrouptrl` <!-- FK_IN: adempiere.c_countrygroup_trl.ccountrygroup_ccountrygrouptrl --> | [`c_countrygroup_trl`](c_countrygroup_trl.md) | `c_countrygroup_id` | [`c_countrygroup`](c_countrygroup.md) | `c_countrygroup_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccountrygroup_ccountrygroupcou` <!-- FK_IN: adempiere.c_countrygroupcountry.ccountrygroup_ccountrygroupcou --> | [`c_countrygroupcountry`](c_countrygroupcountry.md) | `c_countrygroup_id` | [`c_countrygroup`](c_countrygroup.md) | `c_countrygroup_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccountrygroupfrom_ctax` <!-- FK_IN: adempiere.c_tax.ccountrygroupfrom_ctax --> | [`c_tax`](c_tax.md) | `c_countrygroupfrom_id` | [`c_countrygroup`](c_countrygroup.md) | `c_countrygroup_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccountrygroupto_ctax` <!-- FK_IN: adempiere.c_tax.ccountrygroupto_ctax --> | [`c_tax`](c_tax.md) | `c_countrygroupto_id` | [`c_countrygroup`](c_countrygroup.md) | `c_countrygroup_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
