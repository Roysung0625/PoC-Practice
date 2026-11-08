# 상품 등록·검색 반영

[전체 일람](../index.md)

분류 근거: 등록 전용 DDL과 DB 함수. 물리적 연결과 업무 의미의 확정은 구분합니다.

상품 등록은 [상품](../idempiere/m/m_product.md), [분류](../idempiere/m/m_product_category.md), [단위](../idempiere/c/c_uom.md), [세금 분류](../idempiere/c/c_taxcategory.md)를 사용합니다. [일본어 등록 실습](../../product-registration/lab.md)에서 입력·검사 순서를 확인합니다.

등록 DDL 소스 확인: 2026-11-08T16:14:18+09:00. DB 메타데이터 수집: 2026-11-08T16:14:17+09:00. 등록 스키마의 pg_catalog 실측 대조: PASS; 등록 3테이블, 물리 FK 5개, m_product 인바운드 127개. 읽기 전용 수집 결과는 [메타데이터 근거](../metadata-evidence.json)의 postgres.registration에서 구분합니다.

원본 사전의 m_product 인바운드 물리 FK는 124개이며, 등록 스키마 설치 후 정확히 3개가 추가되어 127개가 됩니다. 추가 제약조건은 아래와 같습니다. 원본 912개 canonical 문서와 124개 기준 스냅샷은 보존하고 이 영역에서 차이를 보충합니다.

- `registration_request_product_id_fkey`: `poc_registration.registration_request.(product_id)` → `adempiere.m_product.(m_product_id)`; ON DELETE/UPDATE NO ACTION.
- `registration_audit_product_id_fkey`: `poc_registration.registration_audit.(product_id)` → `adempiere.m_product.(m_product_id)`; ON DELETE/UPDATE NO ACTION.
- `indexing_job_product_id_fkey`: `poc_registration.indexing_job.(product_id)` → `adempiere.m_product.(m_product_id)`; ON DELETE/UPDATE NO ACTION.

검사기의 `--registration-only`는 DB를 읽기 전용으로 연결하여 신규 3테이블의 컬럼·기본값·키 및 FK 5개 전체와 상품 인바운드 124+3 집합을 별도 대조합니다. CHECK 정의는 수집하지만 표현식 정규화 비교는 하지 않습니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| poc_idempiere | poc_registration | indexing_job | 상품 검색 반영 작업 (추론명) | 해당 없음(신규 운영 문서) | 상품 등록·검색 반영 | 확정된 상품의 검색 반영 상태와 재시도를 관리한다. | [문서](../registration/indexing_job.md) | 등록 DDL 기준 / 수집 시점 실테이블 확인 | <!-- table-id: poc_idempiere.poc_registration.indexing_job -->
| poc_idempiere | poc_registration | registration_audit | 상품 등록 이력 (추론명) | 해당 없음(신규 운영 문서) | 상품 등록·검색 반영 | 등록 요청별 상품·규칙 버전·수행자를 기록한다. | [문서](../registration/registration_audit.md) | 등록 DDL 기준 / 수집 시점 실테이블 확인 | <!-- table-id: poc_idempiere.poc_registration.registration_audit -->
| poc_idempiere | poc_registration | registration_request | 상품 등록 요청 (추론명) | 해당 없음(신규 운영 문서) | 상품 등록·검색 반영 | 재전송을 구분하고 확정한 초안과 상품 ID를 연결한다. | [문서](../registration/registration_request.md) | 등록 DDL 기준 / 수집 시점 실테이블 확인 | <!-- table-id: poc_idempiere.poc_registration.registration_request -->
