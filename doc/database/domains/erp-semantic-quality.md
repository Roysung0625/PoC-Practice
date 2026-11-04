# 품질 시험·규격 — 근거 기반 분류안·공식 분류 아님

[전체 일람](../index.md)

분류 근거: 원본 사전 Name/Description + 주요 열/물리 FK 교차대조(문서 overlay 자동 규칙). 물리적 연결과 업무 의미의 확정은 구분합니다.

상품의 품질 시험·시험 결과·규격 조건 참조를 탐색합니다.

관계 흐름 근거(실제 물리 FK의 자식 → 부모; 실행 시간 순서 아님):

- `m_product_qualitytest.(m_qualitytest_id)` → `m_qualitytest.(m_qualitytest_id)` (`mqualitytest_mproductqualityte`).
- `m_qualitytestresult.(m_qualitytest_id)` → `m_qualitytest.(m_qualitytest_id)` (`mqualitytest_mqualitytestresul`).
- `qm_specificationline.(qm_specification_id)` → `qm_specification.(qm_specification_id)` (`qmspecification_qmspecificatio`).

[항목별 사전·열·FK 근거](../classification-evidence.md). 기존 canonical 폴더·설명은 표의 별도 열로 남깁니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| poc_idempiere | adempiere | m_product_qualitytest | 제품별 품질 시험 (사전: Product Quality Test) | m: 제품·재고·출하/입고·원가 (기존 분류안) | 품질 시험·규격 | 제품에 적용할 품질 시험과 기대 결과를 연결한다. | [문서](../../../docs/database/idempiere/m/m_product_qualitytest.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Product Quality Test'; 주요 열 m_product_id, m_qualitytest_id, expectedresult; FK mqualitytest_mproductqualityte; 사전 의미와 열/FK가 품질 시험·규격를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-m_product_qualitytest) | <!-- table-id: poc_idempiere.adempiere.m_product_qualitytest -->
| poc_idempiere | adempiere | m_qualitytest | 품질 시험 (사전: Quality Test) | m: 제품·재고·출하/입고·원가 (기존 분류안) | 품질 시험·규격 | 품질 시험 항목의 이름과 설명을 정의한다. | [문서](../../../docs/database/idempiere/m/m_qualitytest.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Quality Test'; 주요 열 근거 부족; FK mqualitytest_mproductqualityte, mqualitytest_mqualitytestresul; 사전 의미와 열/FK가 품질 시험·규격를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-m_qualitytest) | <!-- table-id: poc_idempiere.adempiere.m_qualitytest -->
| poc_idempiere | adempiere | m_qualitytestresult | 품질 시험 결과 (사전: Quality Test Result) | m: 제품·재고·출하/입고·원가 (기존 분류안) | 품질 시험·규격 | 제품 속성 집합 인스턴스별 시험 결과와 합격 여부를 저장한다. | [문서](../../../docs/database/idempiere/m/m_qualitytestresult.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Quality Test Result'; 주요 열 m_qualitytest_id, result; FK mqualitytest_mqualitytestresul; 사전 의미와 열/FK가 품질 시험·규격를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-m_qualitytestresult) | <!-- table-id: poc_idempiere.adempiere.m_qualitytestresult -->
| poc_idempiere | adempiere | qm_specification | 품질 규격 (사전: Quality Specification) | qm: 품질 관리 (기존 분류안) | 품질 시험·규격 | 제품 품질을 판정하는 규격을 정의한다. | [문서](../../../docs/database/idempiere/qm/qm_specification.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Quality Specification'; Description='Quality Specification'; 주요 열 m_product_id, validfrom; FK qmspecification_qmspecificatio; 사전 의미와 열/FK가 품질 시험·규격를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-qm_specification) | <!-- table-id: poc_idempiere.adempiere.qm_specification -->
| poc_idempiere | adempiere | qm_specificationline | 품질 규격 조건행 (사전: QM Specification Line) | qm: 품질 관리 (기존 분류안) | 품질 시험·규격 | 품질 규격에서 검사할 속성·비교 연산·기준값과 유효기간을 정의한다. | [문서](../../../docs/database/idempiere/qm/qm_specificationline.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='QM Specification Line'; 주요 열 validfrom, qm_specification_id; FK qmspecification_qmspecificatio; 사전 의미와 열/FK가 품질 시험·규격를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-qm_specificationline) | <!-- table-id: poc_idempiere.adempiere.qm_specificationline -->
