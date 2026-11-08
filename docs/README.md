# 프로젝트 문서 안내

프로젝트 공통 문서의 저장 위치는 저장소 루트의 `docs/`입니다. 여기에서 전체 구조, 지속 지침, DB 목록, 교육 자료와 구성요소별 운영 가이드를 찾을 수 있습니다.

## 읽는 순서

1. [전체 구조와 데이터 흐름](architecture.md)에서 앱·AWS·DB·로컬 검색의 역할을 확인합니다.
2. [프로젝트 지속 지침](project-guidelines.md)에서 현재 유효한 사용자 결정과 재발 방지 기준을 읽습니다.
3. [DB 전체 안내와 목록](database/index.md)에서 대상 DB·전체 테이블과 확인 근거를 찾습니다.
4. 구성요소의 운영 문서에서 설치·시작·중지·복구 절차를 따릅니다.

## 구성요소별 안내

| 목적 | 문서 |
| --- | --- |
| 프로젝트 개요·현재 상태 | [루트 README](../README.md) |
| 작업 지침의 진입점 | [AGENTS.md](../AGENTS.md) |
| 기존 로컬 웹·SQL API·수신기 | [로컬 실행·설정 가이드](../local/README.md) |
| 대화형 분석 웹 | [분석 챗봇 안내](../analysis-chatbot/README.md) · [검증 기록](../analysis-chatbot/docs/VERIFICATION.md) |
| GardenWorld 상품 등록 | [기능 안내·운영](product-registration/README.md) · [한국어 실습서](product-registration/lab.md) · [검증 기록](product-registration/verification.md) · [실제 등록 완료 화면](product-registration/verification.md#실제-등록-완료-화면) |
| AWS 구성·인증·운영 | [AWS 가이드](../aws/README.md) · [배포·운영](../aws/DEPLOYMENT.md) |
| 계정 전체 비용 차단 | [Budget guard](../aws/budget_guard/README.md) |
| SQL 챗봇 학습 | [질문·승인부터 결과 확인까지](education/README.md) · [Laravel과 Vue.js의 구조](education/LARAVEL_AND_VUE.md) |
| iDempiere 전체 테이블 문서 | [사전 안내](database/idempiere/README.md) · [912개 테이블 일람](database/idempiere/TABLE_INDEX.md) · [업무별 찾기](database/idempiere/BUSINESS_GUIDE.md) |
| 로컬 OpenSearch 설치·운영 | [검색 실습 운영 가이드](../local/opensearch/README.md) · [검증 기록](../local/opensearch/VERIFICATION.md) |
| OpenSearch 학습 | [DB 관계부터 일본어 검색까지](learning/opensearch-lab.md) · [Discover 아이콘·필드별 저장 값](learning/opensearch-discover-fields.md) |
| 새 PC·Mac 준비 | [Mac 설치 안내](MACOS_SETUP.md) · [소스 외 파일 준비](SOURCE_DOWNLOADS.md) |

## 문서와 검증을 읽는 기준

구조 설명, 소스 구현, 로컬 모의 시험, 실제 로컬 서비스 연결, 실제 AWS 왕복 검증은 서로 다른 근거입니다. 각 기록의 날짜·환경·대상 버전·미검증 범위를 함께 읽습니다. 과거의 실제 AWS 성공 기록이 새 구현이나 모든 질문의 정확성을 보장하지 않습니다.

DB 테이블 구조 문서는 `docs/database/idempiere/`의 원본 사전을 사용합니다. [DB 전체 목록](database/index.md)은 각 테이블을 해당 원본 또는 운영 저장소 문서로 연결합니다.

[통합 DB index](database/index.md)의 핵심 대상 928개는 ERP 912개·등록 전용 PostgreSQL 3개·로컬 SQLite 12개·DynamoDB 1개를 합친 범위입니다. ERP 원본 사전의 912개 테이블 구조 검증과 통합 대상 전체의 확인 상태를 구분합니다. 등록 DDL과 실제 DB 설치 확인, SQLite의 읽기 전용 구조 대조, DynamoDB의 코드·기존 배포 근거와 최신 실제 구조 미검증 범위는 통합 index와 각 운영 저장소 문서를 기준으로 읽습니다.


## SQL 챗봇 교육과 지속 규칙

[SQL 챗봇 교육 문서](education/README.md)에서 화면·승인·AWS 왕복·로컬 PostgreSQL·저장 결과 재사용을 학습합니다. 기존 OpenSearch 교육은 별도 범위로 유지합니다. [프로젝트 지침서](project-guidelines.md)의 CHAT-001~014는 감독/작업 에이전트 역할, 실제 sol/xhigh 설정, 로컬 웹·승인된 AI 검증, 독립 정답·실패 보존과 사후 로컬 검증 경계입니다. 최신 실제 검증 판정과 문제별 개선 효과는 [분석 웹 검증 기록](../analysis-chatbot/docs/VERIFICATION.md)을 확인합니다.


[DB 전체 안내](database/index.md)는 핵심 대상 928개(PG ERP912·등록 DDL3·SQLite12·DynamoDB 정의1)의 식별자 집합 검사와 의미 분류를 구분합니다. 의미 분류는 근거 기반 제안730개·확인 필요182개·사람 승인0개이며, 등록 스키마의 현재 실측과 최신 DynamoDB 실제 구조의 미검증도 별도로 표시합니다. 이 문서 분류를 앱의 SQL 권한이나 사용자 승인으로 간주하지 않습니다.
