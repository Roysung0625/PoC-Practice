# 지식·분류·문서 — 근거 기반 분류안·공식 분류 아님

[전체 일람](../index.md)

분류 근거: 원본 사전 Name/Description + 주요 열/물리 FK 교차대조(문서 overlay 자동 규칙). 물리적 연결과 업무 의미의 확정은 구분합니다.

지식 항목·출처·키워드/분류·연관 항목의 참조를 탐색합니다.

관계 흐름 근거(실제 물리 FK의 자식 → 부모; 실행 시간 순서 아님):

- `k_comment.(k_entry_id)` → `k_entry.(k_entry_id)` (`kentry_kcomment`).
- `k_entry.(k_source_id)` → `k_source.(k_source_id)` (`ksource_kentry`).
- `k_entry.(k_topic_id)` → `k_topic.(k_topic_id)` (`ktopic_kentry`).
- `k_topic.(k_type_id)` → `k_type.(k_type_id)` (`ktype_ktopic`).

[항목별 사전·열·FK 근거](../classification-evidence.md). 기존 canonical 폴더·설명은 표의 별도 열로 남깁니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| poc_idempiere | adempiere | k_comment | 지식 항목 의견 (사전: Entry Comment) | k: 지식·분류·문서 (기존 분류안) | 지식·분류·문서 | 지식 항목에 대한 의견이나 주석을 저장한다. | [문서](../idempiere/k/k_comment.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Entry Comment'; Description='Knowledge Entry Comment'; 주요 열 k_entry_id, textmsg; FK kentry_kcomment; 사전 의미와 열/FK가 지식·분류·문서를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-k_comment) | <!-- table-id: poc_idempiere.adempiere.k_comment -->
| poc_idempiere | adempiere | k_entry | 지식 항목 (사전: Entry) | k: 지식·분류·문서 (기존 분류안) | 지식·분류·문서 | 지식 관리의 개별 콘텐츠 항목을 저장한다. | [문서](../idempiere/k/k_entry.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Entry'; Description='Knowledge Entry'; 주요 열 k_topic_id, keywords, k_source_id, textmsg; FK kentry_kcomment, ksource_kentry; 사전 의미와 열/FK가 지식·분류·문서를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-k_entry) | <!-- table-id: poc_idempiere.adempiere.k_entry -->
| poc_idempiere | adempiere | k_source | 지식 출처 (사전: Knowledge Source) | k: 지식·분류·문서 (기존 분류안) | 지식·분류·문서 | 지식 항목이 유래한 정보 출처를 정의한다. | [문서](../idempiere/k/k_source.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Knowledge Source'; Description='Source of a Knowledge Entry'; 주요 열 근거 부족; FK ksource_kentry; 사전 의미와 열/FK가 지식·분류·문서를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-k_source) | <!-- table-id: poc_idempiere.adempiere.k_source -->
| poc_idempiere | adempiere | k_topic | 지식 주제 (사전: Knowledge Topic) | k: 지식·분류·문서 (기존 분류안) | 지식·분류·문서 | 지식 콘텐츠를 구분하는 주제를 정의한다. | [문서](../idempiere/k/k_topic.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Knowledge Topic'; Description='Knowledge Topic'; 주요 열 k_type_id; FK ktopic_kentry, ktype_ktopic; 사전 의미와 열/FK가 지식·분류·문서를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-k_topic) | <!-- table-id: poc_idempiere.adempiere.k_topic -->
| poc_idempiere | adempiere | k_type | 지식 유형 (사전: Knowledge Type) | k: 지식·분류·문서 (기존 분류안) | 지식·분류·문서 | 지식 항목의 유형을 정의한다. | [문서](../idempiere/k/k_type.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Knowledge Type'; Description='Knowledge Type'; 주요 열 근거 부족; FK ktype_ktopic; 사전 의미와 열/FK가 지식·분류·문서를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-k_type) | <!-- table-id: poc_idempiere.adempiere.k_type -->
