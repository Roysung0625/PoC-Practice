# r_mailtext — 메일 본문 서식

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.r_mailtext` |
| 한국어 논리명(문서용 해석) | 메일 본문 서식 |
| 원본 논리명 | Mail Template |
| 원본 사전 ID | 416 |
| 분류 | `r` — 요청·지원·상태 관리 |
| 전체 테넌트 행 수 | 3 |
| 물리 열 수 | 15 |
| 나가는 FK / 들어오는 FK | 0 / 15 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

메일 발송에 사용하는 텍스트 서식을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Text templates for mailings
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `r_mailtext_pkey` | `r_mailtext_id` |
| UNIQUE | `r_mailtext_uu_idx` | `r_mailtext_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `r_mailtext_id` | Mail Template | numeric(10,0) | 불가 | 예 | — | Text templates for mailings |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `ishtml` | HTML | character(1) | 불가 | — | 'N'::bpchar | Text has HTML tags |
| 11 | `mailheader` | Subject | character varying(2000) | 허용 | — | — | Mail Header (Subject) |
| 12 | `mailtext` | Mail Text | text | 불가 | — | — | Text used for Mail message |
| 13 | `mailtext2` | Mail Text 2 | character varying(2000) | 허용 | — | — | Optional second text part used for Mail message |
| 14 | `mailtext3` | Mail Text 3 | character varying(2000) | 허용 | — | — | Optional third text part used for Mail message |
| 15 | `r_mailtext_uu` | R_MailText_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 15개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_printform"]
    n1["ad_scheduler"]
    n2["ad_user"]
    n3["ad_usermail"]
    n4["r_mailtext"]
    n0 -->|"distrib_order_mailtext_id → r_mailtext_id"| n4
    n0 -->|"manuf_order_mailtext_id → r_mailtext_id"| n4
    n0 -->|"invoice_mailtext_id → r_mailtext_id"| n4
    n0 -->|"order_mailtext_id → r_mailtext_id"| n4
    n0 -->|"project_mailtext_id → r_mailtext_id"| n4
    n0 -->|"remittance_mailtext_id → r_mailtext_id"| n4
    n0 -->|"shipment_mailtext_id → r_mailtext_id"| n4
    n1 -->|"r_mailtext_id → r_mailtext_id"| n4
    n2 -->|"r_defaultmailtext_id → r_mailtext_id"| n4
    n3 -->|"r_mailtext_id → r_mailtext_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `distribordermailtext_adprintfo` <!-- FK_IN: adempiere.ad_printform.distribordermailtext_adprintfo --> | [`ad_printform`](../ad/ad_printform.md) | `distrib_order_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `manufordermailtext_adprintform` <!-- FK_IN: adempiere.ad_printform.manufordermailtext_adprintform --> | [`ad_printform`](../ad/ad_printform.md) | `manuf_order_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_invoiceadprintform` <!-- FK_IN: adempiere.ad_printform.rmailtext_invoiceadprintform --> | [`ad_printform`](../ad/ad_printform.md) | `invoice_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_orderadprintform` <!-- FK_IN: adempiere.ad_printform.rmailtext_orderadprintform --> | [`ad_printform`](../ad/ad_printform.md) | `order_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_projectadprintform` <!-- FK_IN: adempiere.ad_printform.rmailtext_projectadprintform --> | [`ad_printform`](../ad/ad_printform.md) | `project_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_remitadprintform` <!-- FK_IN: adempiere.ad_printform.rmailtext_remitadprintform --> | [`ad_printform`](../ad/ad_printform.md) | `remittance_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_shipadprintform` <!-- FK_IN: adempiere.ad_printform.rmailtext_shipadprintform --> | [`ad_printform`](../ad/ad_printform.md) | `shipment_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_adscheduler` <!-- FK_IN: adempiere.ad_scheduler.rmailtext_adscheduler --> | [`ad_scheduler`](../ad/ad_scheduler.md) | `r_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rdefaultmailtext_aduser` <!-- FK_IN: adempiere.ad_user.rdefaultmailtext_aduser --> | [`ad_user`](../ad/ad_user.md) | `r_defaultmailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_adusermail` <!-- FK_IN: adempiere.ad_usermail.rmailtext_adusermail --> | [`ad_usermail`](../ad/ad_usermail.md) | `r_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_adwfnode` <!-- FK_IN: adempiere.ad_wf_node.rmailtext_adwfnode --> | [`ad_wf_node`](../ad/ad_wf_node.md) | `r_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_mproduct` <!-- FK_IN: adempiere.m_product.rmailtext_mproduct --> | [`m_product`](../m/m_product.md) | `r_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_mfamethod` <!-- FK_IN: adempiere.mfa_method.rmailtext_mfamethod --> | [`mfa_method`](../mfa/mfa_method.md) | `r_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_rmailtexttrl` <!-- FK_IN: adempiere.r_mailtext_trl.rmailtext_rmailtexttrl --> | [`r_mailtext_trl`](r_mailtext_trl.md) | `r_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_rrequest` <!-- FK_IN: adempiere.r_request.rmailtext_rrequest --> | [`r_request`](r_request.md) | `r_mailtext_id` | [`r_mailtext`](r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
