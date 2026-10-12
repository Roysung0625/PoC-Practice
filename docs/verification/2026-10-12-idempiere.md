# iDempiere 설치 및 챗봇 전환 검증

검증일: 2026-10-12. 설치·운영 방법은 [iDempiere 안내](../../local/IDEMPIERE_GUIDE.md), 테이블별 목록은 [912개 테이블 설명](../../local/IDEMPIERE_TABLES.md)을 참고한다.

## 실제 설치 상태

- 기존 PostgreSQL 18.6 서비스의 별도 DB `poc_idempiere`, 스키마 `adempiere`에 공식 v13 GardenWorld 시드를 복원했다.
- 테이블 912개, 뷰 161개, 외래키 3,807개, 열 18,818개. 460개 테이블에 행이 있다.
- `poc_tpch` DB와 이전 카탈로그를 보존했다. API 기본 DSN과 카탈로그를 iDempiere로 전환했다.
- 전용 조회 역할의 `transaction_read_only=on`과 쓰기 거부를 확인했다. SQL API는 912개 물리 테이블만 허용한다.
- Java iDempiere ERP 서버는 설치하지 않았다. 설치 DB는 읽기 분석용이다.

## 로컬 검증

- Python API·SQL·AWS 계약 시험: 최초 실행 64개 통과, 프로세스 수명주기 시험 1개 실패. 동시에 실행한 Vite 빌드가 manifest를 교체하는 시점과 겹쳤으며, 빌드 완료 후 해당 시험을 단독 재실행하여 1개 통과했다.
- SQL 허용 함수 조건을 모델 입력에도 전달하도록 보완한 후 관련 계획·iDempiere 시험 8개가 통과했다.
- 프런트엔드 단위 시험 5개 통과, Vite 배포 빌드 성공. 기존 Plotly 번들의 크기 경고는 남아 있다.
- 브라우저 시험 2개 통과: 현재 데이터셋의 샘플 계획·승인·실제 PostgreSQL 결과·이력 복원, 좁은 화면 및 CSRF 보호.
- 고정 샘플은 월별·통화별 3행을 반환했다. 신용 전표 차감·통화 분리·테넌트 필터는 별도 임시 DB 시험으로 확인했다.

## 실제 AWS 연결 검증

기존 도쿄 리전 스택에서 Agent 코드 아티팩트를 갱신했다. CloudFormation 결과는 `UPDATE_COMPLETE`이며, Lambda SQL Tool과 SQS·DynamoDB 전달 흐름은 유지했다. 앱은 기존 일반 IAM 역할 `poc-chatbot`·`poc-worker`를 사용했다.

사용한 모델은 **DeepSeek V3.2 (`deepseek.v3.2`)**다. 전체 912개 테이블의 요약에서 관련 테이블을 선택하고 외래키 부모를 포함한 최대 32개 테이블의 열·관계로 SQL 계획을 생성했다. 임베딩 검색을 구현하거나 검증한 작업은 아니다.

최초 브라우저 질문은 `AGENT_RESPONSE_INVALID`로 실행 전에 차단됐다. CloudWatch에는 모델의 정상 응답 종료가 기록되어 있었으나 최초 원문 SQL을 보존하지 않아 정확히 어느 표현이 로컬 검사에서 거부됐는지는 확정하지 않았다. 모델 입력에 실제 허용 함수와 날짜 집계 표현을 명시한 뒤 같은 질문을 재검증했다. 모든 자연어 질문의 성공을 보장하는 결과는 아니다.

최종 질문:

> GardenWorld의 USD 확정 판매 청구액을 월별로 집계하고 막대그래프로 보여줘.

검토한 SQL은 `ad_client_id=11`, 판매 문서, 완료·마감 상태, USD를 조건으로 사용했다. 청구액은 세전 `totallines`, 판매 대변전표는 차감하는 것으로 계획에 명시했다.

| 월 | 세전 청구액(USD) | 문서 수 |
|---|---:|---:|
| 2002-02-01 | 142.5 | 2 |
| 2002-08-01 | 152 | 1 |

- 요청 ID: `93ea4ad1-36b4-453d-993e-d2cfcc0a24f4`
- 계획 ID: `9e3966ab-c0c2-45a0-88cc-1c469e180cf8`, revision 1
- 검증 시각: `2026-10-12T14:41:46Z`
- 모델의 실제 도구 호출 확인: `native_tool_use=true`
- SQL 성공 → AWS 전달 완료 → Agent 답변 성공
- PostgreSQL 직접 재조회와 반환 열·행이 완전히 일치했고, 막대그래프의 두 데이터 값도 일치했다.
- 브라우저에서 Agent 설명·표·막대그래프 표시를 확인했다.

근거 파일은 소스 관리에서 제외한 로컬 경로에 보존한다.

| 경로 | 내용 |
|---|---|
| `.local/datasets/idempiere/manifest.json` | 시드 출처·SHA-256·실제 행 수 |
| `.local/aws-deploy/idempiere-deployment.json` | AWS 코드 갱신 및 변경 집합 결과 |
| `.local/aws-deploy/verification/idempiere-chatbot.json` | 왕복 실행·직접 조회 대조·선택 테이블·행 |
| `.local/aws-deploy/verification/idempiere-result.jpg` | 실제 최종 결과 화면 |

최종 `Check.ps1`에서 API·웹·수신기와 PostgreSQL이 실행 중이며, DB 연결·912개 테이블·웹 HTTP 200을 확인했다.

## 검증 범위의 한계

공식 시드의 주문·청구서는 각각 8건이며 회계 원장은 비어 있다. 복잡한 테이블 관계를 탐색하는 예제이고 대규모 거래량 부하 시험 결과가 아니다. 이번 변경에서 전체 912개 테이블의 모든 업무 질의, ERP 업무 쓰기, 재부팅 후 무인 복구를 검증하지 않았다. 데모는 2002~2003년의 과거 자료이며 실제 기업 실적이 아니다.
