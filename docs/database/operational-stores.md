# 운영 저장소의 연결과 보존

[전체 일람](index.md) · [승인·분석 원장](domains/operations-jobs.md) · [웹 대화 저장소](domains/operations-conversations.md) · [AWS 전달 저장소](dynamodb/results.md)

Python FastAPI와 기존 수신기는 `.local/jobs.sqlite` 하나를 공유합니다. SQL 승인 계획·작업·전달 outbox와 분석 실행·이벤트·결과·파일 메타데이터가 함께 들어 있습니다. Laravel 웹은 별도 `.local/analysis-chatbot/conversations.sqlite`에서 대화·질문 차례·화면 snapshot과 산출물 ID를 관리합니다. SQLite의 schema명은 `main`이며 파일 경로까지 물리 식별자에 포함합니다.

Laravel turns.run_id와 Python analysis_runs.run_id, 웹 artifacts.id와 Python analysis_artifacts.artifact_id는 파일 DB를 가로지르는 논리 연결입니다. Python 원장 내부에도 선언된 물리 FK는 없습니다. Laravel 안에서는 turns→conversations, artifacts→turns/conversations의 물리 FK 3개가 선언되어 ON DELETE CASCADE / ON UPDATE NO ACTION입니다. 이는 파일 산출물까지 삭제한다는 의미가 아닙니다.

SQLite 키·복합 순서·NULL/default는 각 개별 문서와 PRAGMA 근거를 확인합니다. TEXT PRIMARY KEY 또는 rowid 복합 PRIMARY KEY가 명시적 NOT NULL과 동일하다고 가정하지 않습니다. JSON은 TEXT 저장이며 DB가 JSON 내부 계약이나 파일 DB 간 소유권을 FK로 검사하지 않습니다. Laravel 설정은 foreign_key_constraints=true이지만 이번 작업에서 실행 중 연결의 CASCADE 동작 시험은 수행하지 않았습니다.

승인 digest·개정·기한, SQL 결과와 outbox의 원자적 보존, 이벤트 순서와 대화 소유권 검증을 유지합니다. 재시작/전송 실패가 결과를 정상으로 바꾸거나 원본 결과를 지우는 근거가 되지 않습니다. 질문·계획·결과 JSON과 로컬 파일 경로에는 사용자 내용이 포함될 수 있으므로 이 문서는 컬럼/제약/소스 계약만 다룹니다. 자동 삭제·백업 보존 기간의 공통 정책은 소스에서 확정된 것이 없어 확인 필요이며 운영 DB를 문서 검사 목적으로 변경하지 않습니다.

근거: [Journal](../../local/python/poc/journal.py), [AnalysisStore](../../local/python/poc/analysis_store.py), [Laravel migration](../../analysis-chatbot/database/migrations/2026_11_03_000001_create_conversations.php), [TurnStore](../../analysis-chatbot/app/Services/TurnStore.php), [연결 설정](../../analysis-chatbot/config/database.php).
