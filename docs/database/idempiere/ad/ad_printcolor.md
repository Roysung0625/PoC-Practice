# ad_printcolor — 출력 색상

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_printcolor` |
| 한국어 논리명(문서용 해석) | 출력 색상 |
| 원본 논리명 | Print Color |
| 원본 사전 ID | 490 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 23 |
| 물리 열 수 | 12 |
| 나가는 FK / 들어오는 FK | 0 / 22 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

출력과 화면 표시에 사용할 색상을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Color used for printing and display
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_printcolor_pkey` | `ad_printcolor_id` |
| UNIQUE | `ad_printcolor_uu_idx` | `ad_printcolor_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_printcolor_name`: `CREATE UNIQUE INDEX ad_printcolor_name ON adempiere.ad_printcolor USING btree (ad_client_id, name)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_printcolor_id` | Print Color | numeric(10,0) | 불가 | 예 | — | Color used for printing and display |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `isdefault` | Default | character(1) | 불가 | — | 'N'::bpchar | Default value |
| 11 | `code` | Validation code | character varying(2000) | 불가 | — | — | Validation Code |
| 12 | `ad_printcolor_uu` | AD_PrintColor_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 22개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_orgtype"]
    n1["ad_printcolor"]
    n2["ad_printcolor_trl"]
    n3["ad_printformat"]
    n4["ad_printformatitem"]
    n5["ad_printtableformat"]
    n0 -->|"ad_printcolor_id → ad_printcolor_id"| n1
    n2 -->|"ad_printcolor_id → ad_printcolor_id"| n1
    n3 -->|"ad_printcolor_id → ad_printcolor_id"| n1
    n4 -->|"ad_printcolor_id → ad_printcolor_id"| n1
    n5 -->|"functbg_printcolor_id → ad_printcolor_id"| n1
    n5 -->|"functfg_printcolor_id → ad_printcolor_id"| n1
    n5 -->|"hdrline_printcolor_id → ad_printcolor_id"| n1
    n5 -->|"hdrtextbg_printcolor_id → ad_printcolor_id"| n1
    n5 -->|"hdrtextfg_printcolor_id → ad_printcolor_id"| n1
    n5 -->|"line_printcolor_id → ad_printcolor_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adprintcolor_adorgtype` <!-- FK_IN: adempiere.ad_orgtype.adprintcolor_adorgtype --> | [`ad_orgtype`](ad_orgtype.md) | `ad_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_adprintcolortrl` <!-- FK_IN: adempiere.ad_printcolor_trl.adprintcolor_adprintcolortrl --> | [`ad_printcolor_trl`](ad_printcolor_trl.md) | `ad_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_adprintformat` <!-- FK_IN: adempiere.ad_printformat.adprintcolor_adprintformat --> | [`ad_printformat`](ad_printformat.md) | `ad_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_adprintformatitem` <!-- FK_IN: adempiere.ad_printformatitem.adprintcolor_adprintformatitem --> | [`ad_printformatitem`](ad_printformatitem.md) | `ad_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_tablefunctbg` <!-- FK_IN: adempiere.ad_printtableformat.adprintcolor_tablefunctbg --> | [`ad_printtableformat`](ad_printtableformat.md) | `functbg_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_tablefunctfg` <!-- FK_IN: adempiere.ad_printtableformat.adprintcolor_tablefunctfg --> | [`ad_printtableformat`](ad_printtableformat.md) | `functfg_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_tablehdrline` <!-- FK_IN: adempiere.ad_printtableformat.adprintcolor_tablehdrline --> | [`ad_printtableformat`](ad_printtableformat.md) | `hdrline_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_tablehdrtextbg` <!-- FK_IN: adempiere.ad_printtableformat.adprintcolor_tablehdrtextbg --> | [`ad_printtableformat`](ad_printtableformat.md) | `hdrtextbg_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_tablehdrtextfg` <!-- FK_IN: adempiere.ad_printtableformat.adprintcolor_tablehdrtextfg --> | [`ad_printtableformat`](ad_printtableformat.md) | `hdrtextfg_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_tableline` <!-- FK_IN: adempiere.ad_printtableformat.adprintcolor_tableline --> | [`ad_printtableformat`](ad_printtableformat.md) | `line_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_cbpgroup` <!-- FK_IN: adempiere.c_bp_group.adprintcolor_cbpgroup --> | [`c_bp_group`](../c/c_bp_group.md) | `ad_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_cchannel` <!-- FK_IN: adempiere.c_channel.adprintcolor_cchannel --> | [`c_channel`](../c/c_channel.md) | `ad_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_cposkey` <!-- FK_IN: adempiere.c_poskey.adprintcolor_cposkey --> | [`c_poskey`](../c/c_poskey.md) | `ad_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_cposkeylayout` <!-- FK_IN: adempiere.c_poskeylayout.adprintcolor_cposkeylayout --> | [`c_poskeylayout`](../c/c_poskeylayout.md) | `ad_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor_mproductcategory` <!-- FK_IN: adempiere.m_product_category.adprintcolor_mproductcategory --> | [`m_product_category`](../m/m_product_category.md) | `ad_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor1_pacolorschema` <!-- FK_IN: adempiere.pa_colorschema.adprintcolor1_pacolorschema --> | [`pa_colorschema`](../pa/pa_colorschema.md) | `ad_printcolor1_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor2_pacolorschema` <!-- FK_IN: adempiere.pa_colorschema.adprintcolor2_pacolorschema --> | [`pa_colorschema`](../pa/pa_colorschema.md) | `ad_printcolor2_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor3_pacolorschema` <!-- FK_IN: adempiere.pa_colorschema.adprintcolor3_pacolorschema --> | [`pa_colorschema`](../pa/pa_colorschema.md) | `ad_printcolor3_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintcolor4_pacolorschema` <!-- FK_IN: adempiere.pa_colorschema.adprintcolor4_pacolorschema --> | [`pa_colorschema`](../pa/pa_colorschema.md) | `ad_printcolor4_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `nameprintcolor_padocumentstatu` <!-- FK_IN: adempiere.pa_documentstatus.nameprintcolor_padocumentstatu --> | [`pa_documentstatus`](../pa/pa_documentstatus.md) | `name_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `nameprintcolorzero_padocumentstatus` <!-- FK_IN: adempiere.pa_documentstatus.nameprintcolorzero_padocumentstatus --> | [`pa_documentstatus`](../pa/pa_documentstatus.md) | `name_printcolorzero_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `numberprintcolor_padocumentsta` <!-- FK_IN: adempiere.pa_documentstatus.numberprintcolor_padocumentsta --> | [`pa_documentstatus`](../pa/pa_documentstatus.md) | `number_printcolor_id` | [`ad_printcolor`](ad_printcolor.md) | `ad_printcolor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
