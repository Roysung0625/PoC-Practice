# 자원·시간·경비·교육 — 근거 기반 분류안·공식 분류 아님

[전체 일람](../index.md)

분류 근거: 원본 사전 Name/Description + 주요 열/물리 FK 교차대조(문서 overlay 자동 규칙). 물리적 연결과 업무 의미의 확정은 구분합니다.

자원 배정/가용성·시간/경비 보고·교육 일정의 참조를 탐색합니다.

관계 흐름 근거(실제 물리 FK의 자식 → 부모; 실행 시간 순서 아님):

- `s_resource.(s_resourcetype_id)` → `s_resourcetype.(s_resourcetype_id)` (`sresourcetype_sresource`).
- `s_resourceassignment.(s_resource_id)` → `s_resource.(s_resource_id)` (`sresource_sresourceassignment`).
- `s_resourceunavailable.(s_resource_id)` → `s_resource.(s_resource_id)` (`sresource_sresunavailable`).
- `s_training_class.(s_training_id)` → `s_training.(s_training_id)` (`straining_strainingclass`).

[항목별 사전·열·FK 근거](../classification-evidence.md). 기존 canonical 폴더·설명은 표의 별도 열로 남깁니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| poc_idempiere | adempiere | m_operationresource | 제품 공정 자원 (사전: Operation Resource) | m: 제품·재고·출하/입고·원가 (기존 분류안) | 자원·시간·경비·교육 | 제품 공정에 필요한 자원을 연결한다. | [문서](../idempiere/m/m_operationresource.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Operation Resource'; Description='Product Operation Resource'; 주요 열 setuptime, unitruntime, teardowntime; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-m_operationresource) | <!-- table-id: poc_idempiere.adempiere.m_operationresource -->
| poc_idempiere | adempiere | s_resource | 업무 자원 (사전: Resource) | s: 자원·시간·비용·교육 (기존 분류안) | 자원·시간·경비·교육 | 업무에 배정하는 자원의 기본 정보를 정의한다. | [문서](../idempiere/s/s_resource.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Resource'; Description='Resource'; 주요 열 s_resourcetype_id, chargeableqty, ismanufacturingresource, waitingtime; FK sresource_sresourceassignment, sresource_sresunavailable; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-s_resource) | <!-- table-id: poc_idempiere.adempiere.s_resource -->
| poc_idempiere | adempiere | s_resourceassignment | 자원 배정 (사전: Resource Assignment) | s: 자원·시간·비용·교육 (기존 분류안) | 자원·시간·경비·교육 | 자원에 대한 업무 배정 정보를 저장한다. | [문서](../idempiere/s/s_resourceassignment.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Resource Assignment'; Description='Resource Assignment'; 주요 열 s_resource_id, assigndatefrom, assigndateto, qty; FK sresourceassign_steline, sresource_sresourceassignment; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-s_resourceassignment) | <!-- table-id: poc_idempiere.adempiere.s_resourceassignment -->
| poc_idempiere | adempiere | s_resourcetype | 자원 유형 (사전: Resource Type) | s: 자원·시간·비용·교육 (기존 분류안) | 자원·시간·경비·교육 | 자원 유형별 시간대·요일·단위와 단일 배정 여부 등을 정의한다. | [문서](../idempiere/s/s_resourcetype.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Resource Type'; 주요 열 timeslotstart, timeslotend, istimeslot, chargeableqty; FK sresourcetype_sresource; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-s_resourcetype) | <!-- table-id: poc_idempiere.adempiere.s_resourcetype -->
| poc_idempiere | adempiere | s_resourceunavailable | 자원 사용 불가 기간 (사전: Resource Unavailability) | s: 자원·시간·비용·교육 (기존 분류안) | 자원·시간·경비·교육 | 자원을 사용할 수 없는 시작·종료일과 사유를 저장한다. | [문서](../idempiere/s/s_resourceunavailable.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Resource Unavailability'; 주요 열 s_resource_id, datefrom, dateto; FK sresource_sresunavailable; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-s_resourceunavailable) | <!-- table-id: poc_idempiere.adempiere.s_resourceunavailable -->
| poc_idempiere | adempiere | s_timetype | 기록 시간 유형 (사전: Time Type) | s: 자원·시간·비용·교육 (기존 분류안) | 자원·시간·경비·교육 | 기록한 시간을 구분하는 유형을 정의한다. | [문서](../idempiere/s/s_timetype.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Time Type'; Description='Type of time recorded'; 주요 열 근거 부족; FK stimetype_stimeexpenseline; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-s_timetype) | <!-- table-id: poc_idempiere.adempiere.s_timetype -->
| poc_idempiere | adempiere | s_training | 교육 과정 (사전: Training) | s: 자원·시간·비용·교육 (기존 분류안) | 자원·시간·경비·교육 | 반복 운영하는 교육 과정의 기본 정의를 저장한다. | [문서](../idempiere/s/s_training.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Training'; Description='Repeated Training'; 주요 열 근거 부족; FK straining_strainingclass; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-s_training) | <!-- table-id: poc_idempiere.adempiere.s_training -->
| poc_idempiere | adempiere | s_training_class | 교육 개설 회차 (사전: Training Class) | s: 자원·시간·비용·교육 (기존 분류안) | 자원·시간·경비·교육 | 교육 과정이 실제로 개설된 개별 회차를 저장한다. | [문서](../idempiere/s/s_training_class.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Training Class'; Description='The actual training class instance'; 주요 열 s_training_id; FK straining_strainingclass; 사전 의미와 열/FK가 자원·시간·경비·교육를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-s_training_class) | <!-- table-id: poc_idempiere.adempiere.s_training_class -->
