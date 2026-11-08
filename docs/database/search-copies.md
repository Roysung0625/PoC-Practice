# 별도 검색 사본 정의 — 핵심 DB 집합에서 제외

[DB 전체 일람](index.md) · [검색 실습 운영 안내](../../local/opensearch/README.md) · [검색 정의 소스](../../local/opensearch/search_lab.py) · [상품 등록 실습](../product-registration/lab.md) · [등록 검증](../product-registration/verification.md) · [등록 웹 구조](../product-registration/web.md)

기존 검색 실습용 두 인덱스와 상품 등록 전용 인덱스의 원본 및 사용처를 구분합니다.

| 정의 | 원본 | 성격 | 확인 상태 |
|---|---|---|---|
| poc-product | PostgreSQL m_product | 상품 검색 사본; 원본 필드와 parent_refs/promotions 관계 표현 | 소스 정의 존재, 실행/현재 상태 미검증 |
| poc-promotion | PostgreSQL m_promotion | 프로모션 검색 사본; 원본 필드와 parent_refs/products 관계 표현 | 소스 정의 존재, 실행/현재 상태 미검증 |
| poc-registration-product-v1 | GardenWorld 활성 실물 상품 및 사용 가능한 마스터 | 일본어 전문·Titan 1,024차원 벡터 검색 | [구성 및 운영](../../aws/registration/README.md) |

원본 상품의 선택 가능 여부는 검색이 끝난 후 PostgreSQL에서 다시 확인합니다. 세 검색 사본은 관계형 테이블 수에서 제외합니다.

이 문서 검사기는 소스 정의를 대조하고 OpenSearch에 연결하지 않습니다. 등록용 정의는 metadata-evidence.json의 supplemental_source_evidence.registration_search에 소스 SHA256으로 기록합니다. 실제 매핑·색인·Titan 호출 결과는 상품 등록의 별도 검증 보고를 확인합니다.
