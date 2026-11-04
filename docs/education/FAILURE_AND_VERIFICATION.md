# 실제 수정 사례로 배우는 검증

[교육 안내](README.md) · [최신 검증 기록](../../analysis-chatbot/docs/VERIFICATION.md) · [독립 정답 평가 안내](../../analysis-chatbot/evaluation/README.md)

아래는 현재 프로젝트에서 다룬 오류 유형과 검증 규칙이다. 수정 소스와 회귀 시험이 있다는 사실을 최신 실제 AWS 전체 평가의 성공으로 확대하지 않는다. 설명에 등장하는 간단한 수치는 별도 표시한 학습 예시이며 실제 DB 조회 결과가 아니다. 과거 실패 턴·SQL·PNG와 평가 자료는 후속 성공으로 덮어쓰지 않는다.

## 1. 숫자가 맞는데 금액이 `건`으로 보였다

이전 실제 평가에서 금액 표는 독립 정답과 맞았지만 차트 단위가 `건`이었고 설명에도 잘못된 단위가 전파됐다. PNG 파일을 만들었다는 검사만으로 이런 의미 오류를 찾을 수 없다.

지금은 SQL AST와 물리 열 계보로 y 값의 출처를 읽는다. `COUNT`는 `건`, 금액은 해당 문서와 실제로 연결된 `c_currency.iso_code` 출력에 따라 분리한다. ISO 코드처럼 보이는 이름만 있거나 무관한 ID끼리 조인한 경우는 통화 증거가 아니다. 모델의 제목·축·범례도 검증된 중립 표기로 바꾼다.

`SUM(qtyonhand)` 같은 재고 수량은 단순히 `건`이나 특정 통화로 바꾸지 않는다. `c_uom_id`를 함께 출력했다고 실제 단위 호환성까지 증명된 것은 아니다. 단위 미검증을 표시하고 단위 간 최소·최대 비교를 관측 설명에서 제외한다.

읽을 소스: [`normalize_chart_units`](../../local/python/poc/analysis_units.py#L222), [`facts_for`](../../local/python/poc/analysis_postprocess.py#L35). 회귀: [단위 검사](../../local/python/tests/test_analysis_units.py), [표시 근거와 관측 제한](../../local/python/tests/test_analysis_postprocess_units.py).

## 2. 두 그룹이 같은 라벨로 보였다

실제 ERP08 유형은 `producttype, issold`별 `COUNT(*)` 집계다. 상품 유형 `I` 안에도 판매 여부 `N`과 `Y`가 있다. 차트에 `producttype`만 라벨로 쓰면 서로 다른 행이 같은 `I`로 보인다. 숫자 대조가 맞아도 차트가 답의 구분을 잃은 것이다.

호스트는 SQL GROUP BY의 출력 계보를 읽어 모든 그룹 차원을 `label_columns`로 만든다. 렌더러의 복합 라벨과 manifest에는 열 이름·원본 값·행 인덱스를 남기고 호스트가 원본 표와 대조한다. 같은 통화 안에서 전체 라벨이 중복돼도 임의로 합산하거나 행을 버리지 않는다.

여러 차원의 막대그래프는 가로 방향으로 전체 라벨을 줄바꿈해 표시한다. 원본 `label`과 실제 `display_label`을 구분하며, 8pt 이상으로 잘림·겹침 없이 들어가지 않으면 명시적으로 실패하고 표를 보존한다. 선그래프 방향은 임의로 바꾸지 않는다.

읽을 소스: [`normalize_chart_dimensions`](../../local/python/poc/analysis_dimensions.py#L142), [`renderer.render`](../../analysis-chatbot/visualization/src/analysis_visualization/renderer.py#L156), [`verify_manifest`](../../local/python/poc/analysis_postprocess.py#L151). 회귀: [차원 검사](../../local/python/tests/test_analysis_dimensions.py), [실제 PNG 검사](../../analysis-chatbot/visualization/tests/test_renderer.py).

## 3. 저장된 날짜 기준과 이번 SQL의 적용 여부가 달랐다

이전 질문의 `date_basis=dateinvoiced`를 후속 질문에 보존하는 일과 이번 SQL에 기간을 적용하는 일은 다르다. 날짜와 관계없는 전체 상품 분류 질문이라면 날짜 기준을 지우거나 강제로 기간을 추가하는 대신, 호스트가 시간축·시간 필터가 없음을 증명한 경우에만 `not_applicable`로 기록한다. 모델이 적은 미적용 표시를 그대로 믿지 않고 승인 시에도 다시 계산한다.

반대로 `start/end` 기간이 있으면 같은 실제 날짜 출처와 행에 두 경계가 모두 적용돼야 한다. 아래는 **구조를 설명하기 위한 SQL 조각**이다.

```sql
-- 잘못된 증거: self join의 서로 다른 청구서 행에 기간 경계가 나뉨
WHERE i.dateinvoiced >= %(start)s AND j.dateinvoiced < %(end)s

-- 같은 청구서 행에 두 경계가 적용되는 형태
WHERE i.dateinvoiced >= %(start)s AND i.dateinvoiced < %(end)s
```

두 별칭이 같은 테이블을 읽더라도 같은 원본 행 출처라는 뜻은 아니다. 시작은 청구일, 끝은 회계일인 경우도 확정한 청구일 기간의 근거가 아니다. 미사용 CTE 안에 조건을 적거나 `OR TRUE`로 우회하는 방식도 거부한다.

읽을 소스: [`Documents.inactive_date_basis`](../../local/python/poc/analysis_documents.py#L386), [`Documents.verify_conditions`](../../local/python/poc/analysis_documents.py#L569). 회귀: [미적용 날짜 기준](../../local/python/tests/test_inactive_date_basis.py), [적용 기간·self join](../../local/python/tests/test_active_date_basis.py).

## 4. 관련 문서를 너무 많이 읽어 계획이 막혔다

테이블의 FK 이웃을 모두 최종 문서로 읽으면 질문에 필요 없는 문서까지 커진다. 이 프로젝트는 후보와 읽을 상세 문서를 구분하며 필요한 추가 문서만 제한 범위에서 확장한다. 후보 12개, 상세 32개, 관계 2홉, 전달 컨텍스트 128KiB 한도를 유지한다. 도달 가능한 이웃이라는 이유만으로 읽지 않은 테이블을 SQL에 사용할 수는 없다.

문서 투영은 원본 전체 읽기·해시 확인 후 중복 FK 주석, 실제 FK 표와 일치하는 중복 그림, 링크 주소 같은 중복 표현을 줄이는 처리다. 열 정의·부모/자식 FK·조회 주의는 보존하며 실제 전달 텍스트의 해시와 크기를 남긴다. 임의로 뒷부분을 잘라 문서 근거를 빠뜨리는 방식이 아니다.

읽을 소스: [`project_document`](../../local/python/poc/analysis_documents.py#L38), [`Documents.read/verify_receipt`](../../local/python/poc/analysis_documents.py#L124). 회귀: [문서 선택](../../local/python/tests/test_document_selection.py), [문서 투영](../../local/python/tests/test_document_projection.py).

## 5. PostgreSQL에서는 가능한 EXISTS가 승인 경로에서 막혔다

DB가 실행할 수 있는 SQL 전체와 호스트가 조건·행 계보를 증명할 수 있는 SQL은 범위가 다르다. 현재 승인 경로는 EXISTS·스칼라 서브쿼리·WHERE/HAVING 서브쿼리를 지원하지 않는다. 이번 보완은 그 제약과 지원 가능한 구조를 모델에 미리 전달하는 것이며 EXISTS 자체를 지원한 것으로 설명하지 않는다.

상세 행의 존재 조건으로 헤더 금액을 집계할 때는 상세와 물리 FK로 연결하고 해당 조건을 적용한 뒤 **문서 식별자를 포함해 중복 제거한 CTE**를 최종 단일 소스로 읽는 구조를 사용한다. CTE라고 해서 항상 승인되는 것은 아니며 실제 FK·테넌트·필터·출력 계보 검사를 통과해야 한다. 호스트가 거부한 SQL을 조용히 다른 SQL로 바꿔 실행하지 않는다.

학습 예시: 금액 100인 문서에 조건에 맞는 상세 행이 2개 있다면, 단순 상세 JOIN 뒤 헤더 금액을 SUM하면 200으로 중복된다. `SUM(DISTINCT 금액)`도 금액이 같은 서로 다른 문서를 합쳐 버릴 수 있어 문서 ID 기준 중복 제거와 다르다. 이 숫자는 원리를 설명하는 가상 예시다.

읽을 소스: [`HOST_SQL_STRUCTURE_CONSTRAINTS`](../../local/python/poc/analysis_documents.py#L26), [`Documents.validate_structure`](../../local/python/poc/analysis_documents.py#L699), [Agent 문서 계획 경로](../../aws/runtime/main.py#L110). 검사 범위와 실제 후속 실행 결과는 [최신 검증 기록](../../analysis-chatbot/docs/VERIFICATION.md)을 확인한다.

## 6. 표는 돌아왔지만 차트 명세가 null이었다

실제 ERP07에서는 창고·상품별 재고 20행이 돌아왔지만 계획의 `chart:null` 때문에 `CHART_SPEC_MISSING`으로 일부 후처리가 실패했다. SQL 조회 성공을 차트 성공으로 대신할 수 없는 사례다.

차트가 누락/null일 때만 호스트가 SQL 출력의 첫 직접 SUM/COUNT와 완전한 GROUP BY 출력 차원으로 기본 막대 명세를 만들도록 보완했다. 여러 지표가 있으면 SQL 출력순 선택 규칙과 미표시 지표를 승인 계획의 `chart_default` 검증 기록에 남긴다. 첫 선택 지표의 통화·그룹 근거를 증명하지 못하면 다른 지표를 임의로 대체하지 않고 표를 보존한다. 명시적으로 전달된 잘못된 명세를 기본값으로 덮지 않는다.

기본 차트가 생겨도 재고 단위의 미검증은 그대로다. 저장 결과를 재사용할 때 현재 명세와 과거 기본선택 명세 전체가 같을 때만 그 근거를 유지한다. 사용자가 x/y/type을 바꾸면 원본 plan을 보존하면서 현재 차트의 과거 기본선택 근거를 제외한다.

ERP08의 별도 실패는 선택적 `currency_column:null`을 렌더러에 그대로 전달한 것이었다. null만 필드 생략으로 정규화한다. 빈 문자열·잘못된 타입·없는 열은 계속 거부하고, 금액에는 연결된 ISO 통화 증거를 계속 요구한다.

읽을 소스: [`default_chart`](../../local/python/poc/analysis_chart_defaults.py#L30), [`verified_chart`](../../local/python/poc/analysis_api.py#L43), [`Analysis.reuse`](../../local/python/poc/analysis_api.py#L449). 회귀: [기본 차트·봉인·재재사용](../../local/python/tests/test_analysis_chart_defaults.py). 실제20행·7행 저장 자료의 오프라인 PNG 검사는 새 소스의 렌더링 증거이며 AWS 전체 재평가를 대신하지 않는다.

## 7. 첫 SQL 초안이 거부됐을 때 한 번 보완한다

v12b의 ERP01·ERP03·ERP04에서는 CTE의 바깥에서 통화·거래처 같은 물리 테이블을 JOIN한 초안이 `JOIN_NOT_VERIFIED`로 거부됐다. 이것만으로 실제 DB에 FK가 없다고 추측하지 않는다. 모델의 SQL 구조가 현재 호스트 검증기의 지원 범위와 맞지 않은 문제를 포함할 수 있다.

후속 구현은 승인 전 초안에 한해 제한된 보완을 허용한다. 최초 거부를 지우고 성공한 응답만 남기지 않으며 최초 초안 통과와 보완 후 통과를 구분한다.

| 허용 코드 | 보완할 수 있는 범위 |
| --- | --- |
| `JOIN_NOT_VERIFIED` | 실제 읽은 FK와 호스트가 증명 가능한 지원 구조로 새 초안 제안 |
| `SQL_COLUMN_INVALID` | 문서에 있는 열·명확한 참조로 새 초안 제안 |
| `CONDITION_BINDINGS_INVALID` | 확정 조건의 근거 객체 형식 보완 |
| `CONDITION_NOT_APPLIED` | 고정된 확정 조건의 실제 적용 근거 보완 |
| `PARAMS_INVALID` | SQL placeholder와 scalar 매개변수 계약 보완 |
| `UNAPPROVED_SCOPE_FILTER` | 질문·확정 조건·승인된 이전 계획에 근거 없이 추가한 date/timestamp 범위·`isactive` 필터 제거 또는 승인 근거에 맞는 초안 제안 |

같은 문서·해석 직후 고정한 조건을 사용해 한 번만 모델에 보완을 요청한다. 호스트는 SQL을 직접 재작성하지 않고 일반 지원 제약과 거부 초안을 `catalog.host_validation_feedback`으로 전달한다. 정답 SQL·관측값·특정 문항의 모범 답안을 주입하지 않는다. 실패 초안에서 추출한 조건은 확정 상태에 반영하지 않으며 보완 초안에도 모든 검증을 다시 수행한다.

후속 미승인 범위 필터 검사로 허용 목록은 기존5종에서6종이 된다. 예를 들어 전체 기간을 요청했는데 모델이 임의로 날짜 범위를 좁히거나 요청하지 않은 `isactive='Y'`를 붙인 경우다. 호스트가 그 필터를 추출·표시하더라도 승인 근거가 새로 생기는 것은 아니다. 보완 모델에도 원래 범위·조건을 고정하며 검증을 통과한 최종 계획만 사용자에게 승인받는다.

기존6호출·모델 누적180초가 남아 있어야 하고 추가 문서 요청은 허용하지 않는다. 최초 진단 저장 실패·문서/스키마 변경·취소·기존 읽기 전용 SQL 정책의 거부이면 보완하지 않는다. 넓은 `SQL_REJECTED`, JSON 오류, AWS 오류·타임아웃, 출력 잘림을 이 여섯 코드로 바꿔 보완하지 않는다. 두 초안이 모두 검증 실패하면 더 호출하지 않고 명시적 실패로 끝낸다.

최초 원문·파생 초안은 비공개 `rejected_plan_diagnostic`에 불변으로 보존한다. 추가 거부 진단은 합산95KiB 안에서 보존하고 초과하면 해시·바이트 수만 남긴다. 공개 `plan_attempts`와 서버 이벤트에는 시도 번호·`rejected/validated/model_failed` 상태·오류 코드·해시를 기록한다. 최종 계획에도 이 시도 요약을 넣어 digest로 봉인한다. 보완 이전 digest나 바뀐 시도 이력의 digest를 최종 승인으로 사용할 수 없다.

v13용 [runtime `Agent.converse`](../../aws/runtime/main.py#L48)는 계획 단계의 출력 상한을4,096토큰으로 지정한다. [`Agent.json_object`](../../aws/runtime/main.py#L63)는 `stopReason=max_tokens`를 `MODEL_OUTPUT_TRUNCATED`로 거부한다. 겉으로 완전한 JSON이어도 잘린 응답을 승인 초안으로 쓰지 않으며 이 오류는 보완 허용 목록에 없다. 출력 상한 조정과 초안 보완은 다른 기능이고 실제로 얼마나 출력했는지와 호출 요금은 실사용 기록을 봐야 한다.

읽을 소스: [`Analysis.plan/validate_draft`](../../local/python/poc/analysis_api.py#L244), [`AnalysisStore.save_rejected_plan_diagnostic`](../../local/python/poc/analysis_store.py#L74). 회귀: [승인 전 보완·조건 고정·진단·한도·최종 승인](../../local/python/tests/test_analysis_plan_repair.py). v13 실제 보완은1회 실패·성공0회다. 후속 변경의 오프라인 검증을 실제 모델 보완 성공으로 확대하지 않으며 [최신 검증 기록](../../analysis-chatbot/docs/VERIFICATION.md)을 확인한다.

## 8. PostgreSQL 출력 이름과 통화 분할 계약을 맞춘다

v13 ERP03은 SQL의 비quoted `AS 거래처_ID`를 차트에서 그대로 썼지만 실제 출력은 `거래처_id`여서 `unknown_column`으로 실패했다. 후속 코드는 별도 SQL AST에서 PostgreSQL의 비quoted ASCII 대문자 접힘과 quoted 원형 보존을 적용한다. SQL 원문 철자나 실제 출력 이름이 한 열로 유일하게 대응할 때만 차트 필드를 정규화한다. 무조건 대소문자를 무시하지 않으며 quoted 이름 오매칭·접힘 후 중복·원문 이름의 모호성은 거부한다.

ERP04는 모델이 `x=currency_column=iso_code`로 지정해 같은 USD 안의 여러 상태를 같은 라벨로 그리려 했다. 당시 차원 검증은 `unverified`였고 렌더러의 `ambiguous_labels` 차단은 정당했다. 후속 코드는 전체 GROUP BY가 증명되고 x가 통화 분할 열일 때만 비통화 첫 그룹을 x로 선택하고 비통화 그룹 전체를 복합 라벨에 넣는다. 원본 SQL·값·행 순서·통화 분할을 보존하며 근거 없는 중복 라벨은 계속 차단한다.

ERP05·06은 호스트가 비금액 지표의 통화 분할 열을 생략해 `currency_required`로 실패했다. 실제 `c_currency.iso_code` 계보가 유일하고 전체 GROUP BY의 일부임을 증명할 때만 비금액 차트에도 통화 분할 메타데이터를 전달한다. 가짜 통화 이름·복수 ISO 후보·증명하지 못한 그룹이나 잘못된 명시적 통화 열을 임의로 대체하지 않는다. **통화 카테고리별 이미지 분리와 y 값의 단위는 별개다.** ERP06 COUNT는 `건`이고 ERP05의 `qtyentered * sign_factor`는 현재 단위 계보가 `unknown`이므로 `단위 미검증`과 수치 최소·최대 관측 제외를 유지한다. 실제 UOM이나 `sign_factor` 계보를 새로 증명한 것으로 설명하지 않는다.

후속 변경으로 저장된 ERP03·04·05·06에서 PNG를 각각2·2·2·1개 생성해 총7개를 검증했다. 같은 입력의 두 렌더가 같은 SHA를 냈고 manifest·PNG 바이트·원본12파일 및 SQL/params/result 해시 불변을 확인했다. 이는 기존 실제 결과의 오프라인 재시각화다. 원본 실패 턴을 수정하거나 실제 AWS 평가를 다시 수행한 것이 아니다. 증거 경로는 `.local/analysis-chatbot/evaluation/offline-v13-chart-contract-20261104-001/report.json`이다.

읽을 소스: [`normalize_chart_identifiers`](../../local/python/poc/analysis_identifiers.py), [`normalize_chart_units`](../../local/python/poc/analysis_units.py), [`normalize_chart_dimensions`](../../local/python/poc/analysis_dimensions.py). 회귀: [식별자·그룹·통화 분할 계약](../../local/python/tests/test_analysis_chart_contract.py). 중간 데이터는 계속 JSON이며 CSV에 관한 설명을 CSV 변환 구현으로 해석하지 않는다.

## 검증을 단계별로 읽는다

최신 원본 v13 실제10문항의 결과는 독립 수치9/10·수동 전체 기준4/10이다. run은 성공5·partial4·조회 전 실패1이었다. 첫 초안은9개 통과·1개 거부였고 실제 보완1회는 실패해 보완 성공은0회다. 이후 저장4문항의 PNG7개 오프라인 복구를 이 원본 성공률에 더하지 않는다. 원본 평가, 별도 오프라인 복구, 후속 수정의 새 실제 평가를 구분한다.

| 증거 단계 | 확인할 수 있는 것 | 이 증거만으로 확정하지 않는 것 |
| --- | --- | --- |
| 소스 읽기/형식·정적 검사 | 코드와 계약의 연결, 파일·함수 존재 | 실제 실행·통신 성공 |
| 모의/fixture 회귀 | 정해진 입력·장애 조건에서의 기대 동작 | 실제 AWS 자격 증명·DB 데이터·배포 적용 |
| 저장 실제 결과의 오프라인 검사 | 그 원본 행으로 새 차트·manifest를 만들고 대조한 결과 | 새 질문의 모델 계획·실제 SQL 재조회·웹 전송 |
| 로컬 고정 샘플 | 실제 로컬 DB 읽기·승인·표·PNG·복원 | 자연어 이해·AWS 전체 경로 |
| 실제 AWS 단건 | 그 요청의 해석·도구·Lambda·Windows 왕복 | 다른 질문·장애 상황·전체10문항 정확도 |
| 독립 정답 SQL 전후 대조 | 같은 조건의 별도 SQL 정답과 반환 행·값·중복·정렬 비교 | 업무 의미·차트 단위·관측 설명 전체 |
| 단계 종합+사람의 의미 검토 | 수치·단위·차원·실PNG·관측·질문 의도 검토 | 검토 범위를 넘는 일반화·장기 무인 운영 |

독립 정답 SQL은 [10개 고정 케이스](../../analysis-chatbot/evaluation/idempiere_cases.json)에서 읽으며 모델 생성 SQL을 정답으로 재사용하지 않는다. 실제 평가에서는 정답을 전후 캡처해 데이터가 같은지도 확인한다. 정답이 달라졌다면 모델 차이와 데이터 변화가 섞였을 수 있다. 열 이름이 달라도 실제 SELECT의 의미로 사람이 매핑하며 정답 숫자를 보고 맞아떨어지는 열을 고르지 않는다. 정렬을 요구하지 않은 질문은 중복 수를 보존하는 행 집합으로, 정렬을 요구한 질문은 순서까지 비교한다.

평가기 소스는 [`compare`](../../analysis-chatbot/scripts/evaluate_idempiere.py#L48), [`stage_checks`](../../analysis-chatbot/scripts/evaluate_idempiere.py#L269), [`automated_status`](../../analysis-chatbot/scripts/evaluate_idempiere.py#L315) 순서로 읽는다. 정답 캡처만 한 실행은 모델 정확도 미검증이다. 수치 대조와 run·PNG·단위·차원·시사점의 종합 판정은 따로 집계하며 서로 중복되는 회귀 횟수를 합산하지 않는다.

[`planning_metadata`](../../analysis-chatbot/scripts/evaluate_idempiere.py#L322)는 초안 이력도 따로 읽는다. `first_attempt_validated`는 첫 초안의 계획 검증 통과, `repaired_validated`는 최초 거부 후 보완 초안의 계획 검증 통과다. 어느 쪽도 SQL 실행 성공·독립 정답 통과를 대신하지 않는다. `completed_after_repair` 등 최종 실행 상태도 함께 확인한다. 과거 자료에 시도 메타데이터가 없다면 첫 초안이 바로 성공했다고 추정하지 않고 미검증으로 남긴다. 기존 v12b 실패 자료를 새 보완 성공 기록으로 덮어쓰지 않는다.

| 검증 표시 | 읽는 법 |
| --- | --- |
| `pass` | 이름 붙은 **그 검사**를 통과했다. 일반 질문의 업무적 정답 전체를 인증하지 않는다. |
| `mismatch` | 비교 대상과 다른 값·구조·상태가 확인됐다. 실패 증거를 읽는다. |
| `unverified` | 근거·비교·지원 범위가 부족해 확정하지 못했다. 성공으로 세지 않는다. |
| `not_applicable` | 검사할 대상이 없음을 조건에 맞게 확인했다. 정상0행의 PNG 없음, 증명된 미적용 날짜 기준 등이 해당한다. |
| `error` | 검사를 완료하지 못했다. 원본 조회 실패인지 검사·수집 실패인지 코드와 단계를 확인한다. |

특히 `chart_unit=unverified`가 재고 UOM의 정직한 표시일 수는 있어도 자동 종합 통과로 바꿀 이유는 아니다. 정상0행에서는 차트가 적용 없음일 수 있지만, 누락된 검사나 명시적 실패를 마음대로 적용 없음으로 바꾸지 않는다. 서버의 `succeeded`와 독립 정답의 `pass`도 서로 다른 상태다.

## 복습

1. 청구 금액 표가 정답과 같고 PNG가 다운로드되면 `건` 단위 오류도 해결됐는가?
2. 기간 조건이 미사용 CTE에만 있어도 SQL 텍스트에 보이므로 충분한가?
3. 차트 null을 호스트가 보완하면 재고 UOM 검증도 통과하는가?
4. SQL 자체는 정상이어도 승인 경로가 지원하지 않는 구조를 거부할 수 있는가?
5. 첫 초안이 거부되고 두 번째가 통과하면 첫 초안 통과율에 포함하는가?
6. JSON이 완전해 보여도 `stopReason=max_tokens`이면 승인해도 되는가?

<details>
<summary>답 확인</summary>

1. 아니다. SQL 값, 실제 단위·차원, PNG 표시, 설명의 의미를 각각 대조해야 한다.
2. 아니다. 실제 반환 행 계보에 적용된 조건이어야 한다. self join의 다른 행 출처에 나뉜 기간 경계도 같은 조건의 증거가 아니다.
3. 아니다. 기본 표시 명세를 만들었다는 사실과 실제 UOM이 호환된다는 증거는 다르다.
4. 그렇다. 현재 지원 계약 안에서 검증할 수 있어야 승인된다. 그 거부를 DB 문법 오류나 지원 완료로 바꿔 설명하지 않는다.
5. 아니다. 보완 후 계획 통과로 별도 기록하고 최초 거부를 보존한다. 최종 SQL 실행과 정답 대조 결과도 따로 읽는다.
6. 아니다. 출력 잘림은 별도 명시적 오류이며 자동 초안 보완 대상으로도 처리하지 않는다.

</details>
