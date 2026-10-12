# 챗봇 Q-A 평가

TPC-H SF1에 대한 질문 10개를 3회씩 실행한다. `cases.json`의 독립 SQL을 읽기 전용 PostgreSQL 연결로 먼저 조회하고 기준값을 저장한다. 생성된 SQL을 정답 SQL로 사용하지 않는다. 평가 도구는 기존 Laravel 세션·CSRF·계획·승인·작업 API를 사용한다. 앱·모델·프롬프트·AWS 권한은 변경하지 않는다.

## 실행

프로젝트 루트의 PowerShell에서 기존 앱과 수신기가 실행 중인지 확인한다. 다른 사용자가 동시에 분석하지 않는 시간대에 실행한다.

```powershell
.\local\scripts\Check.ps1
.\.venv\Scripts\python.exe -m pytest aws/tests/test_evaluation.py -q
.\.venv\Scripts\python.exe aws/scripts/evaluate_chatbot.py --live --repeats 3 --output .local/evaluation/새로운-실행-ID
```

`--live`는 실제 유료 AWS 호출을 수행한다. 지정된 일반 IAM 역할과 기존 비용 정책을 사용한다. 실행 폴더에 `run.json`이 있으면 기본적으로 재실행을 거부한다. 실패한 모델 요청은 자동 재시도하지 않는다. 승인·실행 응답이 불명확하면 이후 사례를 차단 상태로 남기고 실제 요청 상태부터 확인한다.

평가 도구 자체의 승인 전 검증 오류를 수정했을 때만 `--continue-unsubmitted`로 명시적으로 복구할 수 있다. Python·Laravel 양쪽 실행 기록이 0건이고 저장된 계획 digest가 같은지 검증한 후 기존 계획을 승인한다. 이미 완료·실패한 모델 호출은 반복하지 않고, 미호출 사례만 진행한다. 네트워크 오류 등 제출 여부가 불명확한 요청은 이 방식으로 재승인할 수 없다. 복구 전 오류는 사례의 `harness_events`에 보존한다.

Q3와 Q4는 회차별 같은 대화에서 계획 수정으로 실행한다. Q3 계획이 없으면 Q4는 차단으로 기록한다. Q9·Q10은 화면에 표시되는 계획의 데이터 한계 설명을 평가하며, 대체 지표 SQL을 승인하지 않는다. 일반 API 오류는 적절한 설명으로 인정하지 않는다.

## 채점

- 실행 전에 `golden.json`, 종료 후 `golden-after.json`을 생성한다. 두 결과가 다르거나 종료 검증이 없으면 데이터 유효성을 확인한 평가로 보고하지 않는다.
- 선언된 의미별 열 별칭과 `Decimal`, `YYYY-MM` 정규화로 원본 결과를 비교한다. 별칭이 모호하면 `needs_review`로 남긴다. 예상 값이나 열 위치가 같다는 이유로 자동 매핑하지 않는다.
- 금액의 임의 반올림, 다른 기간, 잘못된 조인, 행 누락, 질문에서 요구한 정렬 위반을 오답으로 판별한다. 그래프 값은 원본을 float로 변환한 값과 비교한다.
- 설명은 사람이 질문·계획·정답·표와 대조한다. 수치의 표시 반올림은 별도로 확인하며 실제 순이익·판매자 계정·통화·인과를 근거 없이 만들지 않았는지 평가한다. 다른 LLM을 판정자로 호출하지 않는다.

출력 폴더의 `reviews.json`에 사례별 근거를 작성한다. 키는 `r1-Q1` 같은 시도 ID다. 예:

```json
{
  "r1-Q1": {
    "plan_correct": true,
    "answer_correct": true,
    "evidence": ["국가 0/1/2와 ALGERIA/ARGENTINA/BRAZIL을 정확히 설명"],
    "column_mapping": {"nation_id": "country_number", "nation": "country_name"}
  }
}
```

`column_mapping`은 필요한 경우에만 작성하고, 이름 및 SQL 표현식에 근거한 매핑 이유도 `evidence`에 남긴다. 계획·답변 정답 여부는 분리하며 답변 오류가 있으면 인용과 실제 기준값을 적는다. Q9·Q10은 `answer_correct`로 화면에 보이는 산출 불가 설명을 채점한다.

월이 숫자이고 연도가 별도 열이면 `{"month":{"column":"month","year_column":"year"}}`로 매핑한다. 연도 열이 없다면 SQL 날짜 조건을 확인한 뒤 `year` 정수로 기록한다. 기대값에 맞추어 연도를 추정하지 않는다. 결과가 배송일 기준이면 표현 형식은 정규화하되 주문일 기준 정답과의 차이는 그대로 남긴다.

```powershell
.\.venv\Scripts\python.exe aws/scripts/evaluate_chatbot.py --summarize --output .local/evaluation/실행-ID
```

요약은 네트워크 호출 없이 반복할 수 있다. 전체 예정 건수의 정답·오답·오류·차단을 유지하고 숫자 비교·설명 정확도는 별도 집계한다. 표본 3회의 결과를 일반화된 모델 정확도나 SLA로 해석하지 않는다.

실행이 끝난 뒤 아래 명령으로 CloudWatch 사용량과 저장된 대화의 브라우저 표시를 확인할 수 있다. 두 명령은 새 모델 질문이나 SQL 승인을 생성하지 않는다.

```powershell
.\.venv\Scripts\python.exe aws/scripts/collect_evaluation_usage.py --output .local/evaluation/실행-ID
$env:PLAYWRIGHT_BROWSERS_PATH = "$PWD/.local/playwright-browsers"
.\.local\runtime\node-v24.20.0-win-x64\node.exe aws/evaluation/verify_browser.cjs .local/evaluation/실행-ID
```

브라우저 스크립트는 3회차의 Q4·Q7·Q8·Q9·Q10을 열어 검사한다. 1~2회만 실행한 평가에서는 이 스크립트를 그대로 사용하지 않는다. CloudWatch 조회는 기본 관리 프로필 `poc-practice`를 읽기 전용으로 사용하며, 추론·수신기 인증은 일반 IAM 역할로 유지한다.

## 증거와 검증 경계

`attempts/`에 질문, 계획, 승인, 요청 ID, SQL/전달/Agent 상태, 원본 표, 차트, 답변, 소요 시간을 보존한다. 브라우저에서 대표 결과·빈 결과·이력 복원을 확인하고 별도 기록한다. 기존 로컬·모의 시험 결과 및 실제 Lambda·Titan probe도 구분한다.

현재 Agent 로그의 계획 단계 `request_id`는 null이다. 실행 단계 토큰은 요청 ID로 연결할 수 있지만 계획 단계는 시간대 집계이며, 동시 호출이 있으면 귀속 불명으로 표시해야 한다. 호출 토큰은 확정 청구액이 아니다. 자격증명·DSN·내부 인증 토큰은 평가 출력에 넣지 않는다.
