# 공통 사용자·거래처 연락처 — 근거 기반 분류안·공식 분류 아님

[전체 일람](../index.md)

분류 근거: 원본 사전 Name/Description + 주요 열/물리 FK 교차대조(문서 overlay 자동 규칙). 물리적 연결과 업무 의미의 확정은 구분합니다.

사전에서 시스템 사용자와 거래처 연락처를 함께 표현한 공통 객체를 탐색합니다.

관계 흐름 근거(실제 물리 FK의 자식 → 부모; 실행 시간 순서 아님):

- `ad_user.(supervisor_id)` → `ad_user.(ad_user_id)` (`aduser_supervisor`).
- `ad_user.(salesrep_id)` → `ad_user.(ad_user_id)` (`salesrep_aduser`).

[항목별 사전·열·FK 근거](../classification-evidence.md). 기존 canonical 폴더·설명은 표의 별도 열로 남깁니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| poc_idempiere | adempiere | ad_user | 사용자·거래처 담당자 (사전: User/Contact) | ad: 애플리케이션 사전·화면·권한·시스템 (기존 분류안) | 공통 사용자·거래처 연락처 | 내부 시스템 사용자와 거래처 연락 담당자를 관리한다. | [문서](../../../docs/database/idempiere/ad/ad_user.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='User/Contact'; Description='User within the system - Internal or Business Partner Contact'; 주요 열 password, email, c_bpartner_id, emailuser; FK aduser_supervisor, salesrep_aduser; 사전 의미와 열/FK가 공통 사용자·거래처 연락처를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-ad_user) | <!-- table-id: poc_idempiere.adempiere.ad_user -->
