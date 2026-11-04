# r — 요청·지원·상태 관리

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 28개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`r_category`](r_category.md) | 요청 분류 | Category | 3 | 고객 등의 요청을 분류하는 범주를 정의한다. |
| [`r_categoryupdates`](r_categoryupdates.md) | 요청 분류 알림 수신자 | R_CategoryUpdates | 1 | 요청 분류에 연결된 갱신 알림 수신 사용자와 셀프서비스 여부를 저장한다. |
| [`r_contactinterest`](r_contactinterest.md) | 연락처 관심 분야 | R_ContactInterest | 1 | 사용자별 관심 분야와 구독 시작·해지일을 저장한다. |
| [`r_group`](r_group.md) | 요청 그룹 | Group | 2 | 요청을 함께 관리하는 그룹을 정의한다. |
| [`r_groupupdates`](r_groupupdates.md) | 요청 그룹 알림 수신자 | R_GroupUpdates | 1 | 요청 그룹에 연결된 갱신 알림 수신 사용자와 셀프서비스 여부를 저장한다. |
| [`r_interestarea`](r_interestarea.md) | 관심 분야 | Interest Area | 2 | 관심 분야 또는 주제를 정의한다. |
| [`r_issueknown`](r_issueknown.md) | 알려진 문제 | Known Issue | 0 | 이미 알려진 문제 정보를 관리한다. |
| [`r_issueproject`](r_issueproject.md) | 문제 관련 프로젝트 | Issue Project | 0 | 문제 보고와 관련된 프로젝트·자산 및 시스템 상태·통계 정보를 연결한다. |
| [`r_issuerecommendation`](r_issuerecommendation.md) | 문제 권고 사항 | Issue Recommendation | 0 | 문제에 대한 권고 사항의 이름·설명·도움말을 정의한다. |
| [`r_issuesource`](r_issuesource.md) | 문제 발생 출처 | — | 0 | 문제 관련 시스템·프로젝트·사용자를 통계 및 프로파일 정보와 연결한다. 상세 수집 방식은 확인이 필요하다. |
| [`r_issuestatus`](r_issuestatus.md) | 문제 상태 | Issue Status | 0 | 문제를 구분하는 상태의 이름과 설명을 정의한다. |
| [`r_issuesystem`](r_issuesystem.md) | 문제 관련 시스템 | Issue System | 0 | 문제 보고와 관련된 시스템의 자산·DB 주소·상태 및 통계 정보를 저장한다. |
| [`r_issueuser`](r_issueuser.md) | 문제 보고 사용자 | Issue User | 0 | 문제를 보고한 사용자의 정보를 관리한다. |
| [`r_mailtext`](r_mailtext.md) | 메일 본문 서식 | Mail Template | 3 | 메일 발송에 사용하는 텍스트 서식을 저장한다. |
| [`r_mailtext_trl`](r_mailtext_trl.md) | 메일 본문 서식 번역 | Mail Template Trl | 3 | 메일 텍스트 서식의 언어별 번역 정보를 저장한다. |
| [`r_request`](r_request.md) | 고객·잠재고객 요청 | Request | 1 | 거래처 또는 잠재고객이 제기한 요청을 관리하는 기본 테이블이다. |
| [`r_requestaction`](r_requestaction.md) | 요청 변경 이력 | Request History | 2 | 요청의 상태·담당자·분류·우선순위 및 관련 업무 문서 등의 변경 이력을 저장한다. |
| [`r_requestprocessor`](r_requestprocessor.md) | 요청 자동 처리기 | Request Processor | 1 | 요청 처리의 실행 주기와 기한 초과·미활동 알림 및 담당 재배정 기준을 정의한다. |
| [`r_requestprocessor_route`](r_requestprocessor_route.md) | 요청 자동 배정 규칙 | Request Routing | 1 | 요청을 자동으로 적절한 담당 경로에 배정하는 규칙을 정의한다. |
| [`r_requestprocessorlog`](r_requestprocessorlog.md) | 요청 처리 로그 | Request Processor Log | 0 | 요청 처리기의 실행 요약·오류 여부와 상세 메시지를 기록한다. |
| [`r_requesttype`](r_requesttype.md) | 요청 유형 | Request Type | 3 | 문의·불만 등 요청의 업무 유형을 정의한다. |
| [`r_requesttypeupdates`](r_requesttypeupdates.md) | 요청 유형 알림 수신자 | Request Type Updates | 1 | 요청 유형에 연결된 갱신 알림 수신 사용자와 셀프서비스 여부를 저장한다. |
| [`r_requestupdate`](r_requestupdate.md) | 요청 처리 기록 | Request Update | 1 | 요청의 처리 결과·작업 시간·투입 및 청구 수량을 개별 기록으로 저장한다. |
| [`r_requestupdates`](r_requestupdates.md) | 요청 알림 수신자 | Request Update Recipiants | 0 | 개별 요청의 갱신 알림을 받는 사용자와 셀프서비스 여부를 저장한다. |
| [`r_resolution`](r_resolution.md) | 요청 해결 유형 | Resolution | 3 | 요청이 어떤 방식으로 해결되었는지 구분하는 값을 정의한다. |
| [`r_standardresponse`](r_standardresponse.md) | 요청 표준 답변 | Standard Response | 1 | 요청에 응답할 때 사용하는 표준 답변을 정의한다. |
| [`r_status`](r_status.md) | 요청 상태 | Status | 4 | 요청의 진행 상태를 정의한다. |
| [`r_statuscategory`](r_statuscategory.md) | 요청 상태 분류 | Status Category | 1 | 요청 상태들을 묶는 분류를 정의한다. |
