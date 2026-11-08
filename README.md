# PoC-Practice

Windows 로컬 챗봇과 AWS Agent를 연결해 로컬 PostgreSQL의 데이터를 자연어로 조회하는 PoC입니다.
챗봇의 질문·답변 흐름과 Windows–AWS 사이의 실제 연결 환경을 함께 구축합니다.

같은 웹에서 사용하는 **GardenWorld 상품 등록**은 [전용 기능 폴더](product-registration/README.md)에 있습니다. 처음 사용하는 담당자는 [라벤더 한국어 실습서](docs/product-registration/lab.md)에서 시작하세요.

[프로젝트 문서 안내](docs/README.md)에서 [현재 구조](docs/architecture.md)와 [지속 적용할 프로젝트 지침서](docs/project-guidelines.md)를 확인합니다. 기존 구성요소 문서는 원래 경로에서 유지합니다. [로컬 OpenSearch 검색 실습](local/opensearch/README.md) · [OpenSearch 교육 문서](docs/learning/opensearch-lab.md)

새 대화형 분석 웹은 [analysis-chatbot](analysis-chatbot/README.md)에 있습니다. Laravel 13.39.0·PHP 8.5.12·Vue 3.5.44와 별도 Matplotlib PNG 모듈을 사용하며 `127.0.0.1:8010`에서 실행합니다. 기존 Python API·SQL 승인 원장·SQS 수신기를 공유합니다. v13 실제10문항은 독립 수치9/10·수동 전체4/10으로 종료됐고, 사후 저장 차트4사례7PNG 복구와 API 단독 재시작 복원은 별도로 확인했습니다. 문제별 수정 효과와 한계는 [검증 기록](analysis-chatbot/docs/VERIFICATION.md), 학습 흐름은 [SQL 챗봇 교육](docs/education/README.md)에서 확인합니다.

## Mac으로 가져오기

비공개 저장소: [Roysung0625/PoC-Practice](https://github.com/Roysung0625/PoC-Practice).
Mac에 Homebrew와 GitHub CLI를 준비한 뒤 저장소 접근 권한이 있는 계정으로 로그인합니다.

```bash
brew install gh
gh auth login --hostname github.com --git-protocol https --web
mkdir -p "$HOME/Projects"
gh repo clone Roysung0625/PoC-Practice "$HOME/Projects/PoC-Practice"
cd "$HOME/Projects/PoC-Practice"
```

[Mac 최초 설치 지침서](docs/MACOS_SETUP.md)에서 Homebrew 설치부터 현재 GardenWorld DB 복원, AWS 인증·SQS 설정, 실행·검증까지 진행합니다.
이 저장소에는 소스·테스트·설정 예시·잠금 파일·문서만 포함합니다. DB·설치 파일·의존성·실제 환경설정은 포함하지 않습니다. [제외 파일의 다운로드·재생성 방법](docs/SOURCE_DOWNLOADS.md)을 참고하세요.

## 전체 흐름

```text
Windows 로컬 챗봇 -> AWS Agent -> Lambda SQL Tool -> Windows 로컬 SQL 실행
Windows 로컬 SQL 결과 -> Lambda Tool 응답 -> AWS Agent -> Windows 로컬 챗봇
```

Agent는 AgentCore와 Bedrock으로 구성합니다. Lambda가 SQL 조회 도구 역할을 맡고 로컬 실행 결과를 Agent에 반환합니다.
Lambda와 Windows 사이에서는 SQS로 요청을 전달하고 DynamoDB로 결과를 전달합니다. Windows 수신기가 로컬 FastAPI와 PostgreSQL을 호출합니다.

## 적용 모델

| 용도 | 모델 | Bedrock 모델 ID |
| --- | --- | --- |
| 질문 해석·SQL 생성·결과 설명 | DeepSeek V3.2 | `deepseek.v3.2` |
| 텍스트 임베딩 | Amazon Titan Text Embeddings V2 | `amazon.titan-embed-text-v2:0` |

기본 리전은 도쿄이며, Titan은 1,024차원과 정규화를 사용합니다.
공통 기본값은 [모델 설정](aws/config/models.json)에 반영했습니다. 로컬 앱이 이 설정을 읽으며, 실제 추론·임베딩·AWS 왕복 검증은 별도 기록을 확인해야 합니다. 로컬 샘플 실행은 모델 호출을 사용하지 않습니다.

## 프로젝트 구성

```text
PoC-Practice/
├── AGENTS.md                 # 프로젝트 전체 작업 지침
├── README.md                 # 전체 개요와 현재 상태
├── .gitignore                # 공통 환경설정·인증정보·생성 파일 제외
├── .agents/
│   ├── README.md             # Superpowers 설치 정보와 사용 방법
│   └── skills/               # 프로젝트 전용 Superpowers 스킬 15개
├── aws/
│   ├── README.md             # AWS 구축·연결 가이드
│   ├── config/               # 모델 기본값·계정 전체 예산 정책
│   ├── costs/                # 비용 가정과 이전 Calculator 견적
│   ├── budget_guard/         # 월 25 USD 초과 자동 차단 코드·IaC·복구 절차
│   ├── infra/                # 연결 인프라 정의
│   ├── runtime/              # Agent 런타임과 SQL 도구
│   ├── plans/                # AWS 구축 계획
│   └── scripts/              # AWS 로그인·배포·상태 및 복구
├── local/
│   ├── README.md             # 로컬 설치·실행·복구 가이드
│   ├── python/               # SQL API·수신기·DB 적재·시험
│   ├── web/                  # Laravel·Vue 챗봇과 시험
│   └── scripts/              # 설치·시작·중지·상태·브라우저 검증
├── analysis-chatbot/         # 대화 세션 유지·조사 이벤트·승인·PNG 분석 웹
│   ├── visualization/        # 별도 Python 이미지 생성 패키지
│   ├── evaluation/           # iDempiere 독립 정답 SQL 10개
│   └── scripts/              # 독립 실행환경·시작·중지·상태 확인
└── docs/
    ├── README.md             # 공통 문서 안내와 읽는 순서
    ├── architecture.md       # 전체 구조와 데이터 흐름
    ├── project-guidelines.md # 지속 적용할 지침과 결정 이력
    ├── database/             # DB 전체 색인·검사기와 iDempiere 원본 사전
    ├── education/            # SQL 챗봇 교육
    ├── learning/             # OpenSearch 실습
    ├── superpowers/          # 설계와 세부 구현 계획
    └── verification/         # 검증 결과와 미검증 범위
```

- [프로젝트 전체 지침](AGENTS.md)
- [Superpowers 스킬 설치 정보와 사용 방법](.agents/README.md)
- [AWS 구축·연결 가이드](aws/README.md)
- [AWS 연결 스크립트](aws/scripts/Connect-Aws.ps1)
- [새 Mac 설치 지침서 — GardenWorld DB·AWS 인증·SQS 일괄 설정](docs/MACOS_SETUP.md)

`local/`에 Vue·Laravel 챗봇, Python SQL API·작업 수신기, iDempiere와 TPC-H 구성 및 운영 스크립트가 있습니다. [로컬 실행·설정 가이드](local/README.md)를 참고하세요.

이전 TPC-H 데이터의 구성은 [TPC-H 테이블 설명서](local/DATABASE_GUIDE.md)에서 확인할 수 있습니다. 분석용 8개 테이블과 관리용 1개 테이블의 역할, 컬럼, 관계 및 SQL 예제를 설명합니다.

**현재 기본 조회 데이터는 iDempiere 13 GardenWorld입니다.** 별도 `poc_idempiere` DB에 912개 테이블·161개 뷰를 설치하고, 챗봇의 카탈로그·SQL 검사·샘플을 전환했습니다. 기존 TPC-H DB는 보존했습니다. [iDempiere 사용 안내](local/IDEMPIERE_GUIDE.md) · [전체 912개 테이블 목록](local/IDEMPIERE_TABLES.md). 기본 데모의 주문·청구서는 각각 8건으로, 복잡한 스키마를 학습하는 용도이며 대량 거래 성능 데이터는 아닙니다.

[iDempiere 실제 AWS 왕복 검증](docs/verification/2026-10-12-idempiere.md)에서 자연어 질문·SQL 승인·로컬 DB 조회·Agent 답변·표와 그래프의 일치를 확인했습니다.

[AI용 iDempiere 테이블 사전](docs/database/idempiere/README.md)은 실제 DB 구조를 기준으로 전체 912개 테이블을 28개 접두사 폴더에 정리합니다. [전체 일람](docs/database/idempiere/TABLE_INDEX.md)과 [업무별 개요](docs/database/idempiere/BUSINESS_GUIDE.md)에서 개별 테이블의 물리명·원본 논리명·한국어 해석·열·양방향 외래키 흐름을 찾아볼 수 있습니다. 새 [분석 챗봇](analysis-chatbot/README.md)은 이 원문을 읽어 해시·실제 열·FK 근거를 계획과 승인에 연결합니다. 벡터 검색 구현과는 별개이며 실제 정확도는 실행별 검증 기록을 따릅니다.

[구성도를 먼저 읽는 조회 흐름 설계](docs/design/2026-11-03-schema-guided-query.md)는 **명령 → 테이블 문서·관계 탐색 → 조합 계획 → 사용자 승인 → 데이터 조회** 순서를 정의합니다. 문서 읽기 증거·양방향 관계 탐색·확인 질문·계획 검증·기존 AWS 왕복 연결의 설계 근거입니다. 새 분석 웹의 구현·실제 왕복·남은 실패는 [최신 검증 기록](analysis-chatbot/docs/VERIFICATION.md)에서 설계 문서와 구분해 확인합니다.

```powershell
.\local\scripts\Start.ps1
# http://127.0.0.1:8000 에서 고정 샘플 계획 검토 → 승인 → 실제 DB 조회
# AWS 자연어 분석에는 Windows 수신기도 함께 시작
.\local\scripts\Start.ps1 -Receiver
```

[세부 구현 계획](docs/superpowers/plans/2026-10-12-local-chatbot.md) · [로컬 검증 기록](docs/verification/2026-10-12-local.md)

## 현재 상태

- **추가 Q-A 평가(2026-10-12):** 10개 질문을 3회씩 시험했다. 실제 SQL 왕복 24/24 성공, 사전 주문일 기준 원본 수치 16/24 일치, 계획·수치·설명 전체 충족 10/30이었다. 날짜 해석, 판매자 계정의 잘못된 매핑, 설명의 단위·산술 오류를 확인했다. [상세 평가 보고서](docs/verification/2026-10-12-chatbot-qa.md) · [평가 도구 사용법](aws/evaluation/README.md)

- AWS CLI 설치와 `poc-practice` 프로필의 최초 브라우저 인증·STS 계정 조회를 확인했습니다.
- 기본 리전은 도쿄 `ap-northeast-1`입니다.
- AWS 구축 파일은 `aws/`에서 관리합니다.
- 2026-10-12에 DeepSeek V3.2의 실제 계획 생성·도구 호출·SQL 결과 설명과 Titan V2의 1,024차원·정규화를 검증했습니다. 벡터 검색은 이번 범위에서 제외합니다.
- `poc-practice-bootstrap`·`poc-practice-app` 스택을 배포했습니다. 전용 IAM 사용자 `poc-local-login`과 실행 역할 `poc-chatbot`·`poc-worker`를 사용하며 장기 액세스 키는 없습니다.
- 챗봇에서 자연어 질문 → 계획 승인 → 동일 Lambda 호출의 PostgreSQL 결과 반환 → Agent 설명·표·막대그래프 표시까지 성공했습니다. 1995년 STANDARD 제품군 월별 12행을 직접 SQL 조회와 대조했습니다. [AWS 검증 기록](aws/verification-2026-10-12.md) · [배포·운영](aws/DEPLOYMENT.md)
- 로컬 앱과 PostgreSQL TPC-H SF1 적재를 구성했습니다. 승인한 샘플 SQL의 실제 조회·표·그래프를 검증했습니다. AWS 구성은 [AWS 가이드](aws/README.md), 로컬 시험은 [검증 기록](docs/verification/2026-10-12-local.md)에서 구분합니다.
- 계정 전체 실제 집계액 **월 25 USD 초과 시 자동 차단**을 배포했습니다. 기존 10 USD 알림은 유지하며 SNS와 15분 점검으로 동작합니다. 집계 지연·root·잔여 저장 비용 때문에 정확한 청구 상한은 보장하지 않습니다. [차단 범위와 복구](aws/budget_guard/README.md)

현재 인증 상태를 확인하려면 프로젝트 루트의 PowerShell에서 실행합니다.

```powershell
.\aws\scripts\Connect-Aws.ps1 -Profile poc-local-login -Mode Check -ExpectedAccountId 551013419462
```

인증이 만료되었다면 같은 스크립트를 옵션 없이 실행해 브라우저에서 다시 로그인합니다.

```powershell
.\aws\scripts\Connect-Aws.ps1 -Profile poc-local-login -ExpectedAccountId 551013419462
```

사용자 홈의 AWS 프로필과 인증 캐시는 기존 위치에 유지합니다. 상세 설정과 문제 해결은 [AWS 가이드](aws/README.md)를 참고합니다.

분석 웹의 일본어 메뉴 `商品登録`에서 새 GardenWorld 상품을 등록합니다. 등록 화면·백엔드·DB 설치 코드는 [product-registration/](product-registration/README.md)에 모았습니다. [설치와 복구](docs/product-registration/README.md) · [한국어 실습서](docs/product-registration/lab.md) · [검증 기록](docs/product-registration/verification.md)
