# iDempiere 테이블 사전 — AI 참조용

현재 프로젝트의 `poc_idempiere.adempiere`를 읽기 전용으로 조회해 만든 문서입니다. 물리 테이블 **912개**, 열 **18,818개**, 물리 FK **3,807개**를 포함합니다.

## 읽는 순서

1. [업무별 개요](BUSINESS_GUIDE.md)에서 질문과 관련된 업무·출발 테이블을 찾습니다.
2. [전체 테이블 일람](TABLE_INDEX.md)에서 물리명·한국어 논리명·원본 논리명·간단한 쓰임을 검색합니다.
3. 테이블 문서에서 열·기본키·나가는 FK·들어오는 FK를 읽고 필요한 테이블만 추가로 엽니다.
4. [외래키 안내](RELATIONSHIPS.md)의 방향·복합키·집계 주의사항을 확인한 뒤 SQL을 작성합니다.

## 출처와 범위

- 구조·행 수 수집 시점: **2026-11-03T23:29:01+09:00**. 현재 연결된 DB에서 일관된 읽기 전용 스냅샷으로 수집했습니다.
- 물리 구조: PostgreSQL `pg_class`, `pg_attribute`, `pg_constraint`. 제약조건의 열 순서와 삭제·갱신 규칙을 보존합니다.
- 원본 논리명·업무 설명: `adempiere.ad_table`; 열 사전: `adempiere.ad_column`. 원본에 없는 설명은 `—`로 남깁니다.
- 한국어 이름·개요는 문서용 해석입니다. 현재 DB의 테이블 번역 언어는 es_CO이며 공식 한국어 사전을 가져온 것이 아닙니다.
- 설명 근거: 사전 해석 504개 / 구조 해석 400개 / 확인 필요 8개. 각 문서에 구분을 적었습니다.
- 행 수는 **전체 테넌트** 기준입니다. 업무 데이터 행·개인정보·접속 비밀번호는 내보내지 않았습니다.
- 뷰 161개는 이 테이블 문서에서 제외했습니다. 현재 앱의 조회 허용 대상도 물리 테이블입니다.
- UNIQUE 절에는 PostgreSQL 제약조건만 표시합니다. 별도 고유 인덱스·애플리케이션 로직·사전 참조 정의로만 정해진 관계 전체를 보장하지 않습니다.
- 이 문서는 AI에 파일로 제공할 참조 자료입니다. 앱의 기존 JSON 카탈로그나 Agent 입력을 Markdown 자동 로딩으로 변경하지 않았습니다.

## AI가 지켜야 할 해석 기준

- 알려진 물리명만 SQL에 사용하고, 명칭이 비슷하다는 이유로 FK·업무 지표를 만들지 않습니다.
- FK 화살표는 **자식 → 부모**입니다. 업무 처리 순서와 구분합니다. 자기참조와 복합 FK도 일반 FK와 같은 기준으로 읽습니다.
- `createdby`, `updatedby`, `ad_client_id`, `ad_org_id` 등 시스템·감사 관계가 업무 금액의 조인 경로를 대신하지 않습니다.
- 빈 테이블의 실적, 존재하지 않는 판매자 개념·통화·수익 지표를 추정하지 않습니다.
- 주문일·청구일·회계일, 판매/구매, 테넌트, 문서 상태, 통화를 먼저 정의합니다. 부모 합계가 상세 조인으로 중복되지 않게 합니다.

## 폴더별 일람

| 폴더 | 개요 | 테이블 수 |
|---|---|---:|
| [a/](a/README.md) | 자산·감가상각 | 42 |
| [ad/](ad/README.md) | 애플리케이션 사전·화면·권한·시스템 | 258 |
| [asp/](asp/README.md) | ASP 구독·기능 제공 설정 | 13 |
| [b/](b/README.md) | 입찰·토픽·구매자/판매자 연결 | 10 |
| [c/](c/README.md) | 거래처·주문·청구·결제·회계 기준 | 198 |
| [cm/](cm/README.md) | 웹 콘텐츠 관리 | 38 |
| [dd/](dd/README.md) | 물류 이동·분배 주문 | 4 |
| [exp/](exp/README.md) | 데이터 내보내기 형식·처리기 | 5 |
| [fact/](fact/README.md) | 회계 사실·집계 | 3 |
| [gl/](gl/README.md) | 총계정원장·예산·분개 | 14 |
| [hr/](hr/README.md) | 인사·급여 | 18 |
| [i/](i/README.md) | 데이터 가져오기 준비 | 19 |
| [imp/](imp/README.md) | 가져오기·프로세서 설정 | 4 |
| [k/](k/README.md) | 지식·분류·문서 | 13 |
| [m/](m/README.md) | 제품·재고·출하/입고·원가 | 124 |
| [mfa/](mfa/README.md) | 다중 인증 | 4 |
| [other/](other/README.md) | 접두사 공통 분류 없음 | 4 |
| [pa/](pa/README.md) | 성과·보고서·대시보드 | 30 |
| [pp/](pp/README.md) | 제조·생산 계획·제품 구성 | 23 |
| [qm/](qm/README.md) | 품질 관리 | 2 |
| [r/](r/README.md) | 요청·지원·상태 관리 | 28 |
| [s/](s/README.md) | 자원·시간·비용·교육 | 10 |
| [sso/](sso/README.md) | 통합 로그인 | 1 |
| [t/](t/README.md) | 작업·보고서용 보조 테이블 | 23 |
| [testuu/](testuu/README.md) | 시험용 UUID 관련 | 1 |
| [u/](u/README.md) | POS·수표 제한·웹 메뉴 설정 | 5 |
| [w/](w/README.md) | 웹 상점·카운터 | 11 |
| [ws/](ws/README.md) | 웹 서비스 | 7 |

## 갱신과 검증

프로젝트 루트의 PowerShell에서 실행합니다. 실행 환경은 기존 프로젝트 Python 가상환경이며 AWS 호출이나 DB 변경은 없습니다.

```powershell
.\.venv\Scripts\python.exe .\local\scripts\export_idempiere_docs.py --refresh
.\.venv\Scripts\python.exe .\local\scripts\verify_idempiere_docs.py
```

DB를 다시 읽지 않고 마지막 스냅샷에서 재생성하려면 `--refresh`를 생략합니다. 스냅샷은 Git 제외 경로 `.local/datasets/idempiere/documentation-snapshot.json`, 한국어 설명 원본은 `local/schema_docs/overviews_*.json`입니다. 테이블이 추가·삭제되면 설명 집합과 구조 집합 불일치로 생성을 멈추므로 설명 파일도 갱신해야 합니다. 이전 생성 결과에만 존재하는 파일은 자동 삭제하지 않습니다.

검증 결과는 [검증 기록](VERIFICATION.md), 생성 파일 목록·SHA-256은 [manifest.json](manifest.json)에 있습니다.
