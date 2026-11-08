# indexing_job — 상품 검색 색인의 재시도 작업

<!-- table-id: poc_idempiere.poc_registration.indexing_job -->

[DB 전체 목록](../index.md) · [상품 등록 실습](../../product-registration/lab.md) · [실제 검증](../../product-registration/verification.md) · [웹 구조](../../product-registration/web.md) · [등록 원장](registration_request.md) · [감사 기록](registration_audit.md)

## 기본 정보와 업무 역할

물리명은 `poc_idempiere.poc_registration.indexing_job`다. 논리명은 이번 로컬 PoC의 문서용 명칭이며 원본 iDempiere 데이터 사전에는 없다. 근거는 [schema.sql](../../../product-registration/database/schema.sql)의 DDL·작업 선점 및 완료 함수, 작성 기준일은 2026-11-08이다. 원본 DB에 실제 설치했는지와 분리된 PostgreSQL 테스트 결과는 전체 검증 기록에서 구분한다.

한 행은 등록 상품 한 건을 검색 인덱스에 반영하는 작업이다. 등록 트랜잭션이 상품과 이 작업을 함께 커밋하므로 색인 서버 장애가 있어도 DB 등록 결과와 재시도 필요 상태가 남는다. 상품 ID를 OpenSearch 문서 ID로 사용하는 쓰기는 재시도 시 같은 문서를 갱신한다. DB 등록 성공과 색인 완료를 서로 다른 상태로 표시한다.

## 컬럼과 키

| 물리명 | 문서용 의미 | 타입 | NULL | 기본값 | 해석·단위 |
| --- | --- | --- | --- | --- | --- |
| product_id | 색인 대상 상품 ID | numeric(10,0) | 불가 | 없음 | PK, 상품마다 1작업 |
| request_id | 등록 요청 UUID | uuid | 불가 | 없음 | UNIQUE, 등록 요청마다 1작업 |
| status | 검색 반영 상태 | text | 불가 | `'pending'` | pending / indexed CHECK |
| attempts | 작업 선점 횟수 | integer | 불가 | `0` | 0 이상 CHECK. HTTP·모델 호출 수와 구별 |
| last_error | 최근 실패 분류 | text | 허용 | 없음 | 영대문자로 시작하는 대문자·숫자·밑줄 1~64자 CHECK. 비밀·응답 본문 저장 금지 |
| lease_token | 작업 선점 토큰 | uuid | 허용 | 없음 | 작업자별 임의 토큰 |
| lease_until | 선점 만료 시각 | timestamptz | 허용 | 없음 | 선점 시 실제 시각 + 2분 |
| indexed_at | 마지막 색인 완료 시각 | timestamptz | 허용 | 없음 | 성공 처리 시 실제 시각 |
| updated_at | 작업 상태 변경 시각 | timestamptz | 불가 | `now()` | 선점·성공·실패 처리 시 실제 시각으로 갱신 |

PK는 `indexing_job_pkey(product_id)`, 고유 제약은 `indexing_job_request_id_key(request_id)`다. 복합키는 없다. `attempts`는 작업을 선점할 때 증가하므로 색인 성공 건수와 같지 않다.

## 물리 외래키와 양방향 참조

| 방향 | FK 제약조건 | 자식 컬럼 → 부모 컬럼 | 삭제 / 갱신 | 업무 의미 |
| --- | --- | --- | --- | --- |
| 나감 | indexing_job_product_id_fkey | indexing_job.product_id → [adempiere.m_product](../idempiere/m/m_product.md).m_product_id | NO ACTION / NO ACTION | 검색에 반영할 원본 상품 |
| 나감 | indexing_job_request_id_fkey | indexing_job.request_id → [registration_request](registration_request.md).request_id | NO ACTION / NO ACTION | 작업을 발생시킨 등록 요청 |
| 들어옴 | 없음 | 이 신규 스키마에서 이 테이블을 참조하는 FK 없음 | 해당 없음 | DDL 기준 확인 |

모든 FK는 기본 즉시 검사다. 요청과 상품이 같은 등록을 가리키는 조건은 등록 함수와 provenance 뷰로 검증하며 별도 복합 FK로 선언하지 않는다.

## 조회·해석 주의사항

`claim_indexing`은 `FOR UPDATE SKIP LOCKED`와 토큰으로 여러 작업자의 중복 선점을 막는다. 실패하면 `pending`으로 유지하고 선점을 해제하며, 프로세스가 종료되면 2분 뒤 다른 작업자가 선점할 수 있다. 토큰이 다른 오래된 작업자는 최신 작업의 상태를 갱신할 수 없다. `indexed` 성공 뒤 늦게 도착한 실패 통지는 성공 상태를 덮어쓰지 않는다.

`pending`은 상품 등록 실패가 아니다. [원장](registration_request.md)과 상품이 존재하면 같은 요청 ID로 재등록하지 않고 남은 색인을 재시도한다. 중지된 프로세스·OpenSearch 오류·외부 통신 실패의 원문 대신 제한된 오류 분류만 저장한다. 이 테이블의 등록 API 권한도 직접 DML이 아닌 고정 범위 함수 실행으로 제한한다.
