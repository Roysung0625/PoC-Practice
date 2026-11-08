# 승인·분석 원장

[전체 일람](../index.md)

분류 근거: 현재 소스의 생성·조회·갱신 흐름. 물리적 연결과 업무 의미의 확정은 구분합니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| .local/jobs.sqlite | main | analysis_artifacts | 분석 산출물 원장 (추론명) | 해당 없음(신규 운영 문서) | 승인·분석 원장 | 대화에 속하는 로컬 파일 산출물 한 건 | [문서](../sqlite/jobs/analysis_artifacts.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/jobs.sqlite#main.analysis_artifacts -->
| .local/jobs.sqlite | main | analysis_events | 분석 진행 이벤트 (추론명) | 해당 없음(신규 운영 문서) | 승인·분석 원장 | 한 실행의 순번별 진행 이벤트 한 건 | [문서](../sqlite/jobs/analysis_events.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/jobs.sqlite#main.analysis_events -->
| .local/jobs.sqlite | main | analysis_results | 저장 분석 결과 (추론명) | 해당 없음(신규 운영 문서) | 승인·분석 원장 | 재해석·재시각화에 재사용할 결과 한 건 | [문서](../sqlite/jobs/analysis_results.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/jobs.sqlite#main.analysis_results -->
| .local/jobs.sqlite | main | analysis_runs | 비동기 분석 실행 (추론명) | 해당 없음(신규 운영 문서) | 승인·분석 원장 | 대화의 질문/재처리에 대응하는 실행 상태 한 건 | [문서](../sqlite/jobs/analysis_runs.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/jobs.sqlite#main.analysis_runs -->
| .local/jobs.sqlite | main | jobs | SQL 승인·실행 작업 (추론명) | 해당 없음(신규 운영 문서) | 승인·분석 원장 | 승인된 계획에 대한 실행 요청 한 건 | [문서](../sqlite/jobs/jobs.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/jobs.sqlite#main.jobs -->
| .local/jobs.sqlite | main | outbox | 결과 전달 재시도함 (추론명) | 해당 없음(신규 운영 문서) | 승인·분석 원장 | DynamoDB 전달이 필요한 요청 결과 한 건 | [문서](../sqlite/jobs/outbox.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/jobs.sqlite#main.outbox -->
| .local/jobs.sqlite | main | plans | 승인 SQL 계획 (추론명) | 해당 없음(신규 운영 문서) | 승인·분석 원장 | 계획 ID와 개정별 봉인 SQL 계획 한 건 | [문서](../sqlite/jobs/plans.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/jobs.sqlite#main.plans -->
