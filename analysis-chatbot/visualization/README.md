# 독립 PNG 가시화 모듈

Python 3.13의 별도 가상환경에서 검증된 조회 결과 JSON을 읽고 PNG와 검증용 manifest를 반환한다. DB, AWS, 원장, 웹에 의존하지 않는다. Matplotlib 3.11.2의 Agg/Figure API와 Windows 맑은 고딕(`C:/Windows/Fonts/malgun.ttf`)을 사용하며 폰트가 없으면 실패한다.

현재 설치된 맑은 고딕에는 Unicode minus(U+2212)가 없어 숫자 눈금에 ASCII `-`를 사용한다. 음수 부호가 네모로 깨지는 현상을 방지하며 manifest에도 사용한 부호를 기록한다.

`chart_spec.value_unit`에는 선택적으로 1~40자 단위 문자열을 지정할 수 있다. 통화별 문서 수는 `value_unit:"건"`으로 지정한다. `currency_column`에 따라 통화별 이미지를 계속 분리하되 값·축·범례의 단위는 `건`을 사용한다. 명시하지 않으면 통화 코드가 기본 단위이며, 통화도 없으면 `y_label`을 단위로 보존한다. manifest의 `currency`는 이미지 분할 통화, `unit`과 `series[].unit`은 실제 값의 단위다.

위 규칙은 독립 렌더러의 표시 계약이다. 분석 호스트는 SQL AST·물리 열 계보로 단위를 먼저 검증하고 금액은 연결된 통화, COUNT는 건으로 정규화한다. 모델의 잘못된 단위가 제목·축·범례에 남지 않도록 중립적인 표기를 사용한다. 실제 수량 UOM이나 복잡한 단위가 증명되지 않으면 미검증 단위를 명시하고 최소·최대 통계 설명을 제외한다. 렌더링 성공만으로 업무 단위 검증이 완료된 것은 아니다.

프로젝트 루트 PowerShell에서 설치한다.

```powershell
.venv/Scripts/python.exe -m venv analysis-chatbot/visualization/.venv
analysis-chatbot/visualization/.venv/Scripts/python.exe -m pip install -r analysis-chatbot/visualization/requirements.lock
analysis-chatbot/visualization/.venv/Scripts/python.exe -m pip install --no-build-isolation --no-deps -e analysis-chatbot/visualization
```

격리된 실행환경에서 TEMP 쓰기 권한 오류가 나면 프로젝트 안에 임시 디렉터리를 만든 뒤 같은 PowerShell 세션에서 다시 실행한다.

```powershell
New-Item -ItemType Directory -Force analysis-chatbot/visualization/.tmp | Out-Null
$env:TEMP = (Resolve-Path analysis-chatbot/visualization/.tmp).Path
$env:TMP = $env:TEMP
```

```powershell
analysis-chatbot/visualization/.venv/Scripts/python.exe -m analysis_visualization --input <호스트가 생성한 JSON 경로> --output-dir <호스트의 새 출력 디렉터리>
analysis-chatbot/visualization/.venv/Scripts/python.exe -m pytest analysis-chatbot/visualization/tests -q
```

입출력은 [공통 계약](../docs/API_CONTRACT.md)을 따른다. stdout은 단일 UTF-8 JSON이며 오류 진단 코드만 stderr에 기록한다. 원본 행을 로그로 남기지 않는다. 정상 종료 코드는 0, 입력 검증 오류는 2, 파일/렌더링 오류는 3이다. 실행 시간 제한 15초는 호출 호스트가 적용한다. 별도 서비스가 아니므로 시작은 CLI 호출, 중지는 호스트 프로세스 종료이며 재시도는 새 작업 출력 폴더로 실행한다.

허용 차트 키는 `type`, `x`, `y`, `title`, `x_label`, `y_label`, `currency_column`, `value_unit`, `label_columns`이다. `type`, `x`, `y`는 필수이고 bar/line만 지원한다. 코드·경로·URL 실행 옵션은 없다. 모든 문자는 일반 텍스트로 렌더링하여 수식 문법도 실행하지 않는다. 파일명은 `chart-001.png`부터 모듈이 정하고 기존 파일을 덮어쓰지 않는다. 입력 파일은 2MiB, 결과는 500행, 열은 200개, 표시 문자열은 200자로 제한한다. row_count/열 개수/중복 열/유한 숫자를 검증하고 잘린 결과는 거부한다. 빈 결과는 no_data다. 안정적인 그래프 축 계산을 위해 0 또는 절댓값 1e-100~1e100의 숫자를 허용한다.

통화 열을 지정하면 대문자 3자리 코드별로 이미지를 분리하며 통화끼리 합산하지 않는다. 일반 통화 열 이름(currency, currency_code, iso_code, isocode)이 있으면 currency_column 누락도 거부한다. 행은 원래 순서대로 보존하고 집계하지 않는다. 같은 통화 안에서 완성된 라벨이 중복되면 거부한다. 기본 세로 차트의 긴 계열은 최대 20개 x 눈금을 표시하지만 모든 점은 렌더링·manifest에 남긴다. 각 PNG는 정확히 1200×720이다.

`label_columns`는 1~12개 실제 출력 열 이름이며 중복을 금지한다. x를 포함하고 y·별도 통화 분할 열은 제외한다. 단, `x=currency_column`이며 그 통화가 유일한 라벨인 집계는 허용한다. 생략 시 `[x]`다. 복합 그룹은 열 이름과 원래 값을 담은 JSON 객체 문자열 라벨로 구분한다. 호스트가 SQL GROUP BY 계보로 라벨 열을 증명하며, 독립 렌더러는 SQL을 읽거나 모델이 고른 그룹의 의미를 인증하지 않는다.

여러 `label_columns`를 사용하는 막대그래프는 가로 방향으로 표시하고 모든 행의 전체 JSON 라벨에 120자마다 줄바꿈만 삽입한다. 가로축은 값·검증 단위, 세로축은 구분이다. 실제 Agg 텍스트 영역으로 잘림·겹침을 검사하고 9pt 또는 8pt에서도 맞지 않으면 `label_layout_unreadable`로 실패한다. 라벨을 축약하거나 행을 숨기지 않으며 호스트의 원본 표를 보존한다. 선그래프의 방향은 변경하지 않는다. manifest의 `layout`은 방향·줄바꿈 길이·폰트 크기·실제 두 축 표기를, `series[].display_label`은 실제 줄바꿈된 라벨을 기록한다. 호스트는 전체 원본 `label`·행 값과 표시 라벨·축 표기를 함께 대조한다.

차트 명세가 누락되거나 null이면 분석 호스트가 SQL SELECT의 첫 직접 SUM/COUNT 출력과 완전한 GROUP BY 출력 계보를 증명해 기본 막대 명세를 만들 수 있다. 다른 집계 열의 미표시 사실과 선택 규칙은 승인 전 `chart_validation`의 `chart_default`에 봉인한다. 통화 연결·그룹 차원을 증명하지 못하면 기본 차트를 만들지 않으며, 명시적으로 전달된 잘못된 명세를 기본값으로 대체하지 않는다. 수량 단위 미검증은 유지한다. 선택적 `currency_column:null`만 필드 생략으로 정규화하며 금액의 연결된 ISO 통화 검증은 계속 적용한다.

manifest는 result_id, currency, font/font_file/font_sha256, x_label/y_label/legend, minus_sign, row_count와 series를 포함한다. 각 series 항목은 원본 `label`, `value`, 정확한 `decimal_value`, Matplotlib에 전달한 `rendered_value`, `unit`, 원본 `row_index`를 기록한다. 이는 원본과 그래프 입력의 대조 근거이며 데이터 자체의 업무적 정답을 증명하지 않는다. 호스트는 파일의 SHA-256·크기·소유권과 manifest 값을 원본 결과에 대조한 뒤 게시해야 한다. 원본 십진수는 그대로 보존하되 화면 좌표에는 유한 float가 사용된다.

manifest의 `label_columns`와 각 series의 `label_columns`·`label_values`는 복합 라벨에 사용한 열·원래 값을 보존한다. 호스트는 완성된 label 문자열까지 원본 행과 대조한다. 최신 독립 패키지 시험은 **61개 통과 / 16.73초**이며 이전 58개·42개 통과 기록과 구분한다. 실제20행 재고형 복합 라벨의 전체 표시·영역·폰트 크기, 과밀 명시 실패와 선그래프 방향 유지가 포함된다. 이 시험은 실제 AWS 전체 평가 통과를 뜻하지 않는다.

모듈은 출력 폴더의 `.mpl-cache`에 Matplotlib 캐시를 만들 수 있다. PNG·입력 JSON·캐시의 보존과 정리는 호출 호스트 책임이다. `requirements.lock`은 Windows Python 3.13에서 실제 설치·검증한 전체 버전을 고정한다. 실제 DB/AWS 연결 검증은 이 패키지의 테스트 범위가 아니다.
