# PostgreSQL 관계를 OpenSearch 일본어 검색으로 옮겨 보기

이 실습은 원본 DB의 상품·프로모션 관계를 읽어 검색 문서로 만드는 과정을 학습합니다. [설치·시작·중지 안내](../../local/opensearch/README.md)를 PowerShell 7에서 먼저 실행한 뒤 같은 PC의 [Dashboards](http://127.0.0.1:5601)를 엽니다. 설치와 적재가 완료되지 않았다면 아래 조회가 실패하거나 인덱스가 없을 수 있습니다.

[문서 안내](../../doc/README.md) · [전체 구조](../../doc/architecture.md) · [DB 전체 목록](../../doc/database/index.md)

Discover의 `?`, `t`, `#` 아이콘과 원본 73개 컬럼·검색용 추가 5개 필드의 실제 저장 값은 [Discover 필드별 해설](opensearch-discover-fields.md)을 참고하세요.

## 1. 원본 DB와 검색 사본은 각각 무엇을 하나요?

PostgreSQL은 상품 한 행, 프로모션 한 행, 두 대상을 연결하는 행을 별도 테이블에 저장합니다. 기본키(PK)는 각 행을 구별하고 외래키(FK)는 다른 테이블의 행을 참조합니다. 예를 들어 그룹 상품 연결의 `m_product_id`는 실제 상품을 가리킵니다. DB는 선언된 FK에 맞지 않는 참조를 거부합니다.

OpenSearch는 JSON 문서를 인덱스에 저장합니다. 이 실습에서는 상품 한 행을 상품 문서 하나로 만들고, 검색에 필요한 부모 이름과 프로모션 목록도 문서 안에 담습니다. 인덱스는 같은 유형의 문서를 모아 검색하는 공간이며, 매핑은 각 필드를 텍스트·정수·날짜 등으로 해석하는 규칙입니다.

| PostgreSQL에서 배울 것 | OpenSearch에서 대응하는 것 | 이번 구현 |
| --- | --- | --- |
| 테이블·행 | 인덱스·문서 | `m_product` → `poc-product`, 상품 한 행 → 문서 하나 |
| PK | 문서 `_id` | `m_product_id` 또는 `m_promotion_id`를 문자열 ID로 사용 |
| 컬럼과 SQL 타입 | 필드와 매핑 | 이름은 `text`, ID는 `long`, 날짜는 `date` 등 |
| 물리 FK·검증한 논리관계와 JOIN | 문서 안에 복사한 관계 배열 | `parent_refs`, `promotions`, `products` |
| 원본 정합성 검사 | 검색 사본의 적재·검증 | DB FK 검사 후 내보내고 문서 수·필드·관계를 검사 |

OpenSearch의 관계 필드는 FK 제약이 아닙니다. 원본 부모 이름을 바꿔도 이미 만든 검색 문서는 자동으로 바뀌지 않으므로 필요한 경우 다시 내보내고 색인해야 합니다. 원본의 정확한 수치·상태·권한 판단은 PostgreSQL을 기준으로 합니다.

## 2. 현재 실습 데이터가 만들어지는 과정

```text
기존 GardenWorld: 상품 55행과 기존 부모 데이터 보존
  ↓ 고정 배치 poc-search-ja-v1, 한 DB 트랜잭션
일본어 상품 200 + 프로모션 200
  + 그룹 200 + 프로모션-그룹 연결 200 + 그룹-상품 연결 600
  ↓ 배치 행과 부모 이름을 읽기 전용으로 내보내기
상품 JSON 200 + 프로모션 JSON 200
  ↓ 명시적 매핑과 Bulk 적재
poc-product 200문서 + poc-promotion 200문서
  ↓
Dashboards의 목록 확인 / Dev Tools 검색 실습
```

연결은 `m_promotion → m_promotionline → m_promotiongroup → m_promotiongroupline → m_product` 순서로 읽을 수 있습니다. 이 화살표는 실습의 탐색 순서를 뜻하며, 물리 FK는 참조하는 자식에서 부모 방향입니다. 예를 들어 `m_promotionline`이 프로모션과 그룹을 참조하고 `m_promotiongroupline`이 그룹과 상품을 참조합니다.

프로모션마다 상품을 1~5개 연결해 합계 600개의 그룹-상품 연결을 만듭니다. 원예 상품은 일본어 5개 분류와 이름·용도·변형으로 구성한 가상 데이터입니다. 연결이 있다고 실제 할인 계산·판매·재고 실적이 생긴 것은 아닙니다.

DB 전체 상품이 **255행**인데 상품 검색은 **200문서**인 이유는 기존 55행을 보존하고 새 실습 배치 200행만 색인하기 때문입니다. 255개 상품을 모두 적재하는 로직이 아닙니다. 프로모션도 이번 배치 200행만 검색합니다.

## 3. 문서 안의 관계를 읽어 보기

[상품 목록](http://127.0.0.1:5601/app/discover#/view/poc-product-view)에서 한 행을 펼칩니다. `m_product_id`, `name`, `description` 같은 원본 컬럼과 아래 추가 필드를 찾습니다.

| 필드 | 읽는 방법 |
| --- | --- |
| `seed_batch` | 이 문서를 만든 실습 배치, `poc-search-ja-v1` |
| `entity_type` | `product` 또는 `promotion` |
| `parent_refs` | 원본의 물리 FK 및 검증한 논리참조의 필드명·부모 테이블·ID·이름 목록 |
| 상품의 `promotions` | 이 상품에 연결된 프로모션과 연결 테이블 ID 목록 |
| 프로모션의 `products` | 이 프로모션에 연결된 상품 이름·코드·관계 ID 목록 |
| `related_count` | 해당 문서의 관계 배열 항목 수 |

상품은 원본 73컬럼, 프로모션은 원본 13컬럼을 모두 복사합니다. `null` 필드도 원본 문서에 남을 수 있습니다. 아래 Dev Tools 예제에서는 읽기 쉽게 일부 필드만 응답에 표시합니다. `_source`에서 숨기는 것과 원본 문서에 없는 것은 다릅니다.

예를 들어 `createdby`·`updatedby`와 프로모션의 `ad_client_id`·`ad_org_id`는 물리 FK가 선언되지 않은 논리참조이며, 이 실습은 부모 행 존재를 확인해 이름을 복사합니다. `parent_refs`는 지정한 비NULL 참조의 목록이므로 원본의 물리 FK 전체 목록과 같지 않습니다. DB에 선언한 FK 검사와 애플리케이션이 확인한 논리관계를 구분해 읽습니다.

## 4. Dev Tools에서 문서 수와 매핑 확인

Dashboards 메뉴의 **Dev Tools**를 열고 Console에 요청 하나씩 붙여 넣어 실행합니다. 이 절의 요청은 조회용입니다.

```http
GET poc-product/_count

GET poc-promotion/_count
```

적재 성공 후 각 응답의 `count`가 `200`인지 확인합니다. 인덱스 내부의 nested 항목은 여기서 별도 상품·프로모션 문서로 세지 않습니다. `related_count`가 5인 프로모션도 루트 문서는 하나입니다.

```http
GET poc-product/_mapping
```

응답에서 `m_product_id.type`이 `long`, `name.type`이 `text`, `name.analyzer`가 `kuromoji`, `parent_refs.type`과 `promotions.type`이 `nested`인지 찾습니다. 프로모션은 `GET poc-promotion/_mapping`으로 보고 관계 필드가 `products`인지 확인합니다.

## 5. 일본어 이름으로 검색

```http
GET poc-product/_search
{
  "size": 5,
  "_source": ["m_product_id", "value", "name", "description", "related_count"],
  "query": {
    "match": {
      "name": "ラベンダー"
    }
  }
}
```

`hits.total.value`는 일치 문서 수, `hits.hits`는 이번에 받은 문서들입니다. `size: 5`는 최대 5개만 보여 달라는 뜻입니다. `_score`는 이 검색어와 문서의 텍스트가 얼마나 잘 맞는지를 계산한 검색 점수이며 상품 품질이나 판매 순위가 아닙니다.

kuromoji는 띄어쓰기가 적은 일본어를 검색 단위로 분석하는 데 사용합니다. 다음 요청으로 실제 분석 결과를 직접 확인합니다.

```http
GET poc-product/_analyze
{
  "analyzer": "kuromoji",
  "text": "家庭菜園で使えるラベンダー"
}
```

응답의 `tokens`를 읽어 봅니다. 모든 부분 문자열·동의어·오타가 자동으로 검색된다는 뜻은 아닙니다. 사전과 분석 규칙에 따라 단어가 나뉘므로 검색 결과를 보고 확인해야 합니다. `name.keyword`는 분석한 단어 대신 이름 전체를 정확한 값으로 다룰 때 사용합니다.

## 6. nested로 같은 부모 관계에 조건 적용

`parent_refs`는 여러 항목을 가진 배열입니다. 각 항목에 필드명·부모 테이블·부모 ID·부모 이름이 함께 들어 있습니다. `nested` 쿼리는 조건을 **배열의 같은 항목**에 적용하도록 합니다.

아래 요청은 부모 관계 중 `m_product_category` 테이블의 ID `106`을 가리키는 상품을 찾습니다. `106`은 이번 배치가 재사용한 상품 분류 ID입니다.

```http
GET poc-product/_search
{
  "size": 5,
  "_source": ["value", "name", "parent_refs"],
  "query": {
    "nested": {
      "path": "parent_refs",
      "query": {
        "bool": {
          "filter": [
            {"term": {"parent_refs.table": "m_product_category"}},
            {"term": {"parent_refs.id": 106}}
          ]
        }
      },
      "inner_hits": {}
    }
  }
}
```

`term`은 정확한 값 조건이고 `match`는 텍스트 분석을 사용하는 조건입니다. `inner_hits`에서는 어떤 관계 항목이 일치했는지 볼 수 있습니다. 부모 테이블 조건은 한 항목에서, ID 조건은 다른 항목에서 맞는 결과를 의도치 않게 섞지 않도록 배열의 한 묶음으로 조회하는 것입니다.

## 7. 프로모션에 연결된 상품명으로 검색

```http
GET poc-promotion/_search
{
  "size": 5,
  "_source": ["m_promotion_id", "name", "related_count", "products"],
  "query": {
    "nested": {
      "path": "products",
      "query": {
        "match": {
          "products.name": "ラベンダー"
        }
      },
      "inner_hits": {}
    }
  }
}
```

이 요청은 프로모션 이름 대신 그 안의 연결 상품 이름으로 프로모션을 찾습니다. 응답의 루트 `name`은 프로모션 이름이며 `products`의 `name`은 상품 이름입니다. 관계에 저장한 `m_promotionline_id`, `m_promotiongroup_id`, `m_promotiongroupline_id`로 원본 연결 행을 추적할 수 있습니다. 원본 테이블의 정확한 FK는 [전체 사전](../database/idempiere/TABLE_INDEX.md)에서 확인합니다.

상품 문서에서 반대로 프로모션을 검색하려면 `poc-product`의 `promotions` 경로를 사용합니다. `products`는 프로모션 인덱스, `promotions`는 상품 인덱스에 있으므로 인덱스와 경로를 함께 확인합니다.

## 8. 실습을 마친 뒤 확인할 것

| 확인 항목 | 관찰할 결과 |
| --- | --- |
| 원본과 사본 | DB 상품 총 255행, `poc-product` 실습 배치 200문서의 차이를 설명할 수 있음 |
| 일본어 분석 | `match` 결과와 `_analyze` 토큰을 직접 확인함 |
| 관계 검색 | `parent_refs`와 `products`의 nested 조회에서 일치 항목을 찾음 |
| 재실행 | 운영 가이드의 같은 배치를 다시 실행해도 중복 생성하지 않도록 설계됨. 실제 성공은 검증 기록으로 확인 |
| 중지와 재시작 | 운영 스크립트로 종료·시작하고 저장 문서를 확인. 데이터 삭제 명령은 사용하지 않음 |

검증 파일 `.local/opensearch/verification.json`이 있다면 실제 실행 시점·통과/실패 항목을 함께 읽습니다. 코드·문서의 존재만으로 브라우저 표시나 재시작 검증 성공을 추정하지 않습니다.

이번 실습은 Windows 로컬 검색입니다. AWS OpenSearch Service, 기존 챗봇의 검색 연동, 임베딩 생성, 벡터·하이브리드 검색, 검색 품질 점수·부하 성능 평가를 포함하지 않습니다. 기존 앱의 DeepSeek·Titan 설정과 AWS SQL 왕복 흐름은 별도의 구성입니다.
