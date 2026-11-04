# iDempiere 한국어 설명 원본

`overviews_1.json` ~ `overviews_3.json`은 AI 참조용 테이블 문서의 한국어 논리명·개요를 관리한다. 각 파일은 304개, 총 912개 물리 테이블을 포함한다. 원본 논리명은 실제 DB의 `AD_Table` 값을 생성기가 별도로 보존한다.

| 필드 | 의미 |
|---|---|
| JSON 키 | 소문자 물리 테이블명 |
| `logical_name_ko` | 독자를 위한 한국어 논리명 해석. 공식 번역이 아님 |
| `overview_ko` | 그 테이블의 의미와 쓰임 개요 |
| `basis` | `dictionary`: 사전 근거, `structure`: 구조 근거, `uncertain`: 추가 확인 필요 |

실제 구조·사전·행 수는 생성 시점의 읽기 전용 스냅샷에서 가져온다. 한국어 해석에는 당시 구조를 바탕으로 한 설명이 포함되므로 버전·열·업무 의미가 변경되면 설명도 재검토한다. 생성기는 물리 테이블 집합과 설명 키 집합이 정확하게 일치해야 진행한다.

프로젝트 루트에서:

```powershell
.\.venv\Scripts\python.exe .\local\scripts\export_idempiere_docs.py --refresh
.\.venv\Scripts\python.exe .\local\scripts\verify_idempiere_docs.py
```

결과는 [AI 참조용 테이블 사전](../../docs/database/idempiere/README.md)에 생성한다. 현재 앱의 카탈로그·Agent 실행 코드를 변경하는 과정은 아니다. 스냅샷은 `.local/datasets/idempiere/documentation-snapshot.json`에 저장하고, 접속 비밀번호와 실제 업무 데이터 행은 문서에 내보내지 않는다.
