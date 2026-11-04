# 별도 검색 사본 정의 — 핵심 DB 집합에서 제외

[DB 전체 일람](index.md) · [검색 실습 운영 안내](../../local/opensearch/README.md) · [검색 정의 소스](../../local/opensearch/search_lab.py)

현재 소스에는 `poc-product`와 `poc-promotion` 검색 인덱스 2개 정의가 존재합니다. 다른 동시 작업에 속할 수 있으므로 이번 DB 문서 작업은 해당 파일·데이터·매핑을 수정하지 않았습니다. 설치·seed·색인·OpenSearch API 호출을 수행하지 않았고 실행 여부·현재 인덱스 존재·현재 매핑·건수는 미검증입니다.

| 정의 | 원본 | 성격 | 확인 상태 |
|---|---|---|---|
| poc-product | PostgreSQL m_product | 상품 검색 사본; 원본 필드와 parent_refs/promotions 관계 표현 | 소스 정의 존재, 실행/현재 상태 미검증 |
| poc-promotion | PostgreSQL m_promotion | 프로모션 검색 사본; 원본 필드와 parent_refs/products 관계 표현 | 소스 정의 존재, 실행/현재 상태 미검증 |

검색 문서의 `_id`, nested 관계와 검색 필드 타입은 PostgreSQL의 PK/FK·정밀 SQL 타입을 대신하지 않습니다. 정의 수 2개를 관계형 테이블 수나 실제 DB 확인 수로 합산하지 않습니다. 핵심 대상/전체 index/개별 문서의 925 집합과 별도 범위입니다.
