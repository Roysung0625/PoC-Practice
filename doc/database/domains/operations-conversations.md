# 웹 대화·화면 상태

[전체 일람](../index.md)

분류 근거: 현재 소스의 생성·조회·갱신 흐름. 물리적 연결과 업무 의미의 확정은 구분합니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| .local/analysis-chatbot/conversations.sqlite | main | artifacts | 웹 산출물 연결 (추론명) | 해당 없음(신규 운영 문서) | 웹 대화·화면 상태 | 웹 질문에 표시하는 산출물 ID·해시 한 건 | [문서](../sqlite/conversations/artifacts.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/analysis-chatbot/conversations.sqlite#main.artifacts -->
| .local/analysis-chatbot/conversations.sqlite | main | conversations | 웹 대화 (추론명) | 해당 없음(신규 운영 문서) | 웹 대화·화면 상태 | 웹 대화방 한 건 | [문서](../sqlite/conversations/conversations.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/analysis-chatbot/conversations.sqlite#main.conversations -->
| .local/analysis-chatbot/conversations.sqlite | main | migrations | Laravel migration 적용 이력 (추론명) | 해당 없음(신규 운영 문서) | 웹 대화·화면 상태 | framework가 관리하는 적용 migration 한 건 | [문서](../sqlite/conversations/migrations.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/analysis-chatbot/conversations.sqlite#main.migrations -->
| .local/analysis-chatbot/conversations.sqlite | main | sqlite_sequence | SQLite 자동 증가 상태 (추론명) | 해당 없음(신규 운영 문서) | 웹 대화·화면 상태 | AUTOINCREMENT 테이블의 내부 증가값 한 건 | [문서](../sqlite/conversations/sqlite_sequence.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/analysis-chatbot/conversations.sqlite#main.sqlite_sequence -->
| .local/analysis-chatbot/conversations.sqlite | main | turns | 웹 질문 차례 (추론명) | 해당 없음(신규 운영 문서) | 웹 대화·화면 상태 | 대화의 순번별 사용자 요청과 마지막 분석 상태 한 건 | [문서](../sqlite/conversations/turns.md) | 현재 PRAGMA / 소스 대조 완료; 논리명은 추론 | <!-- table-id: sqlite:.local/analysis-chatbot/conversations.sqlite#main.turns -->
