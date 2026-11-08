# Discover 아이콘과 Product 필드별 저장 방식

확인일: 2026-11-04 (Asia/Tokyo). OpenSearch·Dashboards 3.9.0의 현재 화면, 실제 `_mapping`, 실제 문서 GET, 저장된 인덱스 패턴을 읽어 확인했습니다. DB 열의 의미는 2026-11-03 수집한 [원본 상품 사전](../database/idempiere/m/m_product.md)을 기준으로 해석했습니다. 사전에 설명이 없는 항목은 추측으로 확정하지 않습니다.

[검색 실습](opensearch-lab.md) · [운영 안내](../../local/opensearch/README.md) · [문서 안내](../README.md)

## 아이콘은 필드 타입을 나타냅니다

| 화면 기호 | 의미 | 현재 예시 |
|---|---|---|
| `t` | 문자열(String). text와 keyword 모두 해당 | name, value, isactive |
| `#` | 숫자(Number). long·integer·double을 포함 | m_product_id, related_count, weight |
| 달력 | 날짜(Date) | created, updated, discontinuedat, discontinuedby |
| `?` | Discover의 Unknown field 표시. 화면이 사용할 타입 정보가 없다는 뜻 | _id, _index, _score, _type, parent_refs, promotions |

`?`는 값이 null이라는 뜻도, 저장 실패라는 뜻도 아닙니다. 현재 저장된 인덱스 패턴의 fields에는 위 메타 필드와 nested 배열의 루트가 빠져 있습니다. 실제 인덱스 매핑에는 parent_refs와 promotions가 nested로 존재하며 하위 필드도 선언되어 있습니다. 화면의 노란 삼각형은 이 필드의 캐시 매핑 정보가 없다는 안내입니다. DB 값이나 서버 매핑을 이번 설명 작업에서 변경하지 않았습니다.

`t`만으로 text와 keyword를 구별할 수 없습니다. 이름·설명의 text는 kuromoji 분석을 거쳐 검색되며, value·sku·Y/N 플래그의 keyword는 문자열 전체를 하나의 값으로 색인합니다. 따라서 isactive의 Y는 JSON true가 아니라 문자열입니다. [text 공식 설명](https://docs.opensearch.org/latest/mappings/supported-field-types/text/) · [keyword 공식 설명](https://docs.opensearch.org/latest/mappings/supported-field-types/keyword/)

## 어디에 저장되나요?

PostgreSQL m_product 한 행과 관계 테이블을 읽어, OpenSearch poc-product 인덱스에 JSON 문서 하나를 저장합니다. Discover는 저장된 문서를 보여 주는 조회 화면입니다. 현재 선택 문서는 `_id="1000042"`, 상품명은 `アジサイ コンパクト`, 코드는 `POCJA-0043`입니다.

문서 본문 `_source`에는 원본 73개 컬럼과 검색용 추가 필드 5개, 총 78개 최상위 필드가 있습니다. `_id` 같은 메타 정보는 이 78개에 포함하지 않습니다. 화면의 선택된 5개 열은 표시할 항목만 고른 것이며 나머지 데이터도 저장되어 있습니다.

`_source`는 전달한 JSON 값을 보존하고, 매핑은 검색·정렬·집계를 위해 그 값을 어떻게 처리할지 정합니다. name.keyword는 같은 name을 정확 일치·정렬용으로 색인한 하위 필드입니다. `_source`에 name.keyword라는 별도 값을 중복 입력한 것은 아닙니다.

## OpenSearch가 제공하는 관리 정보

| 항목 | 현재 화면 / 의미 |
|---|---|
| _id | "1000042". 문서 ID 문자열. 원본 m_product_id는 숫자 1000042 |
| _index | poc-product. 이 문서가 들어 있는 인덱스 |
| _score | 검색 조건에 대한 관련도 점수. 원본 상품의 저장 컬럼이 아님. 현재 이름 정렬 화면에서는 - 표시 |
| _type | 과거 매핑 타입 관련 항목. 현재 화면에서는 -이며 product/promotion 구분에 사용하지 않음 |
| _source | 상품 본문 JSON. 아래의 78개 필드를 포함 |

Product/Promotion 구분은 인덱스 이름과 entity_type으로 합니다.

## 원본 상품 컬럼 73개

아래 값은 현재 선택한 상품 한 건의 실제 `_source`입니다. 다른 상품의 값은 다릅니다. null은 값이 없는 상태이고 Discover 표에서는 보통 -로 표시됩니다. null도 매핑은 선언되어 있으므로 숫자·날짜 아이콘이 표시될 수 있습니다. 0, "N", 빈 문자열, null은 서로 다른 값입니다.

한국어 설명은 문서용 해석이며 원본 사전 명칭도 함께 보존합니다. Y/N은 해당 옵션의 예/아니오를 뜻합니다. 이 플래그와 수치는 더미이며 실제 재고·판매 실적이나 할인 계산 결과가 아닙니다.

| 필드 | 원본 사전 명칭 | 의미 | OpenSearch 타입 | 선택 상품의 저장 값 |
|---|---|---|---|---|
| `m_product_id` | Product | 상품 기본키. 이 값을 문자열로 바꿔 OpenSearch 문서 _id에도 사용 | `long` | `1000042` |
| `ad_client_id` | Tenant | 테넌트 ID. 11은 GardenWorld | `long` | `11` |
| `ad_org_id` | Organization | 조직 ID. 11은 HQ | `long` | `11` |
| `isactive` | Active | 사용 가능한 레코드인지 여부 | `keyword` | `"Y"` |
| `created` | Created | DB 레코드 생성 시각. 시간대 주의사항 참고 | `date` | `"2026-11-03T23:23:40.347538"` |
| `createdby` | Created By | 생성 사용자 ID. 101은 GardenAdmin | `long` | `101` |
| `updated` | Updated | DB 레코드 최종 수정 시각. 검색 색인 갱신 시각과 다름 | `date` | `"2026-11-03T23:23:40.347538"` |
| `updatedby` | Updated By | 수정 사용자 ID. 101은 GardenAdmin | `long` | `101` |
| `value` | Search Key | 상품 검색 코드. 금액이나 가격을 뜻하지 않음 | `keyword` | `"POCJA-0043"` |
| `name` | Name | 일본어 상품명 | `text` | `"アジサイ コンパクト"` |
| `description` | Description | 상품의 짧은 설명 | `text` | `"庭で使える草花のデモ商品。アジサイ コンパクト。手入れしやすく、日々の園芸を楽しめます。"` |
| `documentnote` | Document Note | 문서에 사용할 부가 설명. 이번 데이터는 가상 상품이라는 안내 | `text` | `"検索検証用の架空商品です。実際の販売・在庫を表しません。"` |
| `help` | Comment/Help | 추가 도움말 또는 주석 | `text` | `null` |
| `upc` | UPC/EAN | UPC/EAN 바코드 | `keyword` | `null` |
| `sku` | SKU | 재고 관리용 상품 코드 | `keyword` | `"POCJA-0043"` |
| `c_uom_id` | UOM | 수량 단위 ID. 100은 Each | `long` | `100` |
| `salesrep_id` | Sales Representative | 영업 담당자 ID. 103은 Joe Sales | `long` | `103` |
| `issummary` | Summary Level | 개별 상품 대신 상위 집계 항목인지 여부 | `keyword` | `"N"` |
| `isstocked` | Stocked | 재고 관리 대상인지 여부. 실제 재고 수량은 아님 | `keyword` | `"Y"` |
| `ispurchased` | Purchased | 구매 대상 상품인지 여부. 실제 구매 실적은 아님 | `keyword` | `"Y"` |
| `issold` | Sold | 판매 대상 상품인지 여부. 실제 판매 실적은 아님 | `keyword` | `"Y"` |
| `isbom` | Bill of Materials | BOM(구성 부품 명세) 상품인지 여부 | `keyword` | `"N"` |
| `isinvoiceprintdetails` | Print detail records on invoice | 청구서에 BOM 상세를 인쇄하는지 여부 | `keyword` | `"N"` |
| `ispicklistprintdetails` | Print detail records on pick list | 피킹 목록에 BOM 상세를 인쇄하는지 여부 | `keyword` | `"N"` |
| `isverified` | Verified | BOM 구성이 검증되었는지 여부 | `keyword` | `"N"` |
| `c_revenuerecognition_id` | Revenue Recognition | 수익 인식 방식 ID | `long` | `null` |
| `m_product_category_id` | Product Category | 상품 분류 ID. 107은 기존 분류 Bushes | `long` | `107` |
| `classification` | Classification | 상품 분류용 보조 코드. 이번 배치는 POC-DEMO | `keyword` | `"POC-DEMO"` |
| `volume` | Volume | 상품 부피의 예시 수치. 이 문서만으로 단위 확정 불가 | `double` | `0.03` |
| `weight` | Weight | 상품 무게의 예시 수치. 이 문서만으로 kg 등 단위 확정 불가 | `double` | `0.3` |
| `shelfwidth` | Shelf Width | 진열 공간에 필요한 너비 | `long` | `null` |
| `shelfheight` | Shelf Height | 진열 공간에 필요한 높이 | `double` | `null` |
| `shelfdepth` | Shelf Depth | 진열 공간에 필요한 깊이 | `long` | `null` |
| `unitsperpallet` | Units Per Pallet | 팔레트당 수량 | `double` | `null` |
| `c_taxcategory_id` | Tax Category | 세금 분류 ID. 107은 Standard | `long` | `107` |
| `s_resource_id` | Resource | 자원(Resource) 연결 ID | `long` | `null` |
| `discontinued` | Discontinued | 상품 공급 중단 여부 | `keyword` | `"N"` |
| `discontinuedby` | — | 원본 사전 설명이 없는 날짜 컬럼. 사용자 ID로 해석하지 않음; 정확한 업무 의미 확인 필요 | `date` | `null` |
| `processing` | Process Now | 원본 사전 명칭 Process Now의 처리용 값. 상세 동작은 미확인 | `keyword` | `null` |
| `s_expensetype_id` | Expense Type | 경비 유형 ID | `long` | `null` |
| `producttype` | Product Type | 상품 유형 코드. 이번 실습은 I(품목) | `keyword` | `"I"` |
| `imageurl` | Image URL | 상품 이미지 URL | `keyword` | `null` |
| `descriptionurl` | Description URL | 상품 설명 페이지 URL | `keyword` | `null` |
| `guaranteedays` | Guarantee Days | 보증 또는 유효 일수 | `long` | `null` |
| `r_mailtext_id` | Mail Template | 메일 템플릿 ID | `long` | `null` |
| `versionno` | Version No | 상품 버전 번호 | `keyword` | `null` |
| `m_attributeset_id` | Attribute Set | 상품 속성 집합 ID | `long` | `null` |
| `m_attributesetinstance_id` | Attribute Set Instance | 구체적인 속성 집합 인스턴스 ID. 현재 0도 null과 구별하여 보존 | `long` | `0` |
| `downloadurl` | — | 다운로드 URL로 해석. 원본 사전 설명은 없음 | `keyword` | `null` |
| `m_freightcategory_id` | Freight Category | 운임 분류 ID | `long` | `null` |
| `m_locator_id` | Locator | 창고 내 보관 위치 ID | `long` | `null` |
| `guaranteedaysmin` | Min Guarantee Days | 최소 보증 일수 | `long` | `null` |
| `iswebstorefeatured` | Featured in Web Store | 웹 상점의 대표 상품 표시 여부 | `keyword` | `"N"` |
| `isselfservice` | Self-Service | 셀프서비스 항목 또는 셀프서비스 수정 허용 여부 | `keyword` | `"Y"` |
| `c_subscriptiontype_id` | Subscription Type | 구독 유형 ID | `long` | `null` |
| `isdropship` | Drop Shipment | 직송 상품인지 여부 | `keyword` | `"N"` |
| `isexcludeautodelivery` | Exclude Auto Delivery | 자동 배송 처리에서 제외하는지 여부 | `keyword` | `"N"` |
| `group1` | Group1 | 보조 그룹 1. 이번 실습에서는 일본어 상품 종류 | `text` | `"草花"` |
| `group2` | Group2 | 보조 그룹 2. 이번 실습에서는 사용 장소 | `text` | `"庭"` |
| `istoformule` | — | 원본 사전 명칭과 설명이 없는 플래그. 정확한 업무 의미 확인 필요 | `keyword` | `null` |
| `lowlevel` | Low Level | 자재 계획 계산용 하위 수준 코드 | `long` | `0` |
| `unitsperpack` | Units Per Pack | 포장당 수량 | `long` | `3` |
| `discontinuedat` | Discontinued At | 공급 중단 일시 | `date` | `null` |
| `copyfrom` | Copy From | 다른 레코드에서 복사하는 처리용 항목 | `keyword` | `null` |
| `m_product_uu` | M_Product_UU | 상품 UUID. 고정 배치의 재현 가능한 UUID | `keyword` | `"7894f58b-9983-5a0b-b492-b6c80726b920"` |
| `m_parttype_id` | Part Type | 부품 유형 ID | `long` | `null` |
| `iskanban` | Kanban controlled | 간판(Kanban) 방식 관리 대상인지 여부 | `keyword` | `"N"` |
| `ismanufactured` | Manufactured | 제조 대상 상품인지 여부 | `keyword` | `"N"` |
| `isphantom` | Phantom | 가상 조립품(Phantom) 구성요소 여부 | `keyword` | `"N"` |
| `isownbox` | Own Box | 원본 명칭 Own Box의 플래그. 상세 포장 업무 규칙은 미확인 | `keyword` | `"N"` |
| `customstariffnumber` | Customs Tariff Number | 세관 관세 번호. 일반적으로 HS 코드 | `keyword` | `null` |
| `isautoproduce` | Auto Produce | 출하를 충족하기 위해 생산을 자동 생성하는지 여부 | `keyword` | `"N"` |
| `isbompriceoverride` | Calculate BOM price if Zero | 원본 명칭 Calculate BOM price if Zero의 플래그. 0 가격일 때 BOM 가격 계산 관련 | `keyword` | `"Y"` |

## 검색용 추가 필드 5개

| 필드 | 의미 | 타입 | 선택 상품의 저장 값 |
|---|---|---|---|
| `entity_type` | 문서 종류. 상품 문서는 product | `keyword` | `"product"` |
| `seed_batch` | 더미 생성 배치 식별자. 재실행 시 같은 배치를 구별 | `keyword` | `"poc-search-ja-v1"` |
| `related_count` | 이 문서의 promotions 배열 항목 수. 현재 상품은 서로 다른 프로모션 3개와 연결 | `integer` | `3` |
| `parent_refs` | 참조한 부모의 필드명·테이블명·ID·이름 배열. 현재 문서에는 8개 | `nested` | 배열 8개 |
| `promotions` | 연결 프로모션 및 연결 테이블 ID 배열. 현재 문서에는 3개 | `nested` | 배열 3개 |

## 관계 배열의 하위 항목

`parent_refs`와 `promotions`는 JSON 객체의 배열이며 nested로 매핑합니다. 동일한 배열 항목 안의 ID와 이름 조건을 함께 검사하기 위해서입니다. 물리 FK·검증한 논리 참조를 적재 시 읽어 복사하며, OpenSearch가 원본 DB를 실시간 JOIN하거나 FK를 강제하지 않습니다. [nested 공식 설명](https://docs.opensearch.org/latest/mappings/supported-field-types/nested/)

| 필드 | 의미 | 타입 | 첫 배열 항목의 예시 |
|---|---|---|---|
| `parent_refs.field` | 원본 상품의 참조 컬럼명 | `keyword` | `"ad_client_id"` |
| `parent_refs.id` | 참조 대상 레코드 ID | `long` | `11` |
| `parent_refs.name` | 참조 대상의 이름 | `text` | `"GardenWorld"` |
| `parent_refs.table` | 참조 대상 테이블명 | `keyword` | `"ad_client"` |
| `promotions.group_name` | 상품 그룹 이름 | `text` | `"草花 対象商品グループ 042"` |
| `promotions.m_product_id` | 이 상품의 ID | `long` | `1000042` |
| `promotions.m_promotion_id` | 연결 프로모션 ID | `long` | `1000041` |
| `promotions.m_promotiongroup_id` | 상품 그룹 ID | `long` | `1000041` |
| `promotions.m_promotiongroupline_id` | 그룹과 상품을 잇는 연결 행 ID | `long` | `1000122` |
| `promotions.m_promotionline_id` | 프로모션과 상품 그룹을 잇는 상세 행 ID | `long` | `1000041` |
| `promotions.name` | 프로모션 이름 | `text` | `"草花 家庭菜園応援フェア 042"` |
| `promotions.value` | 공통 관계 매핑에 선언한 코드 필드. 선택한 상품의 프로모션 항목에는 저장되지 않음 | `keyword` | 필드 미포함 |

점 표기 parent_refs.name은 parent_refs 객체 안의 name을 뜻합니다. 여러 참조 이름이 있어도 각각의 배열 항목에는 field·table·id·name이 함께 저장됩니다. 예를 들어 상품 분류 참조는 107/Bushes, 세금 분류 참조도 107/Standard입니다. 숫자 ID가 같아도 테이블이 다르면 서로 다른 대상입니다.

현재 상품에는 프로모션 1000041, 1000042, 1000079가 연결되어 있어 related_count가 3입니다. Product와 Promotion의 ID 숫자가 같더라도 인덱스가 다르면 별개의 문서입니다.

## 실제 JSON 구조 일부

전체 78개 필드 중 일부를 발췌했습니다. parent_refs와 promotions도 각각 첫 항목만 표시하므로 아래 배열 길이와 related_count를 비교하지 마세요.

```json
{
  "_index": "poc-product",
  "_id": "1000042",
  "_source": {
    "m_product_id": 1000042,
    "value": "POCJA-0043",
    "name": "アジサイ コンパクト",
    "isactive": "Y",
    "weight": 0.3,
    "entity_type": "product",
    "related_count": 3,
    "parent_refs": [
      {
        "field": "ad_client_id",
        "id": 11,
        "name": "GardenWorld",
        "table": "ad_client"
      }
    ],
    "promotions": [
      {
        "group_name": "草花 対象商品グループ 042",
        "m_product_id": 1000042,
        "m_promotion_id": 1000041,
        "m_promotiongroup_id": 1000041,
        "m_promotiongroupline_id": 1000122,
        "m_promotionline_id": 1000041,
        "name": "草花 家庭菜園応援フェア 042"
      }
    ]
  }
}
```

## 날짜 표시와 확인 범위

created의 실제 `_source`는 `2026-11-03T23:23:40.347538`이고 화면에서는 `Nov 4, 2026 @ 08:23:40.347`로 보입니다. 원본 DB 컬럼은 timestamp without time zone이며 적재 문자열에도 시간대가 없습니다. 현재 표시에는 9시간 차이가 있으므로 원본 업무 시각과 UTC/JST 변환 기준을 정리해야 합니다. 화면 시각과 JSON 원문이 같다고 설명하지 않습니다. 이번 작업에서는 시간 값을 수정하거나 재색인하지 않았습니다.

일반 date 타입의 검색용 내부 표현은 epoch 기준 밀리초입니다. 원문에는 마이크로초 6자리가 남아 있지만 기본 date 타입이 그 정밀도로 검색한다는 뜻은 아닙니다. [date 공식 설명](https://docs.opensearch.org/latest/mappings/supported-field-types/date/)

이번 확인은 현재 Product 화면의 문서 1건, 실제 매핑, 인덱스 패턴의 필드 정보와 DB 사전 73개 컬럼의 대응입니다. 전체 배치와 FK의 이전 검증은 [검증 기록](../../local/opensearch/VERIFICATION.md)을 참고하세요. 실시간 동기화·AWS 배포·할인 계산 검증을 이번 확인에 포함하지 않습니다.
