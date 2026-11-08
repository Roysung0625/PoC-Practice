# registration_audit — 성공한 상품 등록의 감사 기록

<!-- table-id: poc_idempiere.poc_registration.registration_audit -->

[DB 전체 목록](../index.md) · [상품 등록 실습](../../product-registration/lab.md) · [실제 검증](../../product-registration/verification.md) · [웹 구조](../../product-registration/web.md) · [등록 원장](registration_request.md) · [색인 작업](indexing_job.md)

## 기본 정보와 업무 역할

물리명은 `poc_idempiere.poc_registration.registration_audit`다. 논리명은 로컬 PoC 문서용 해석이며 원본 iDempiere 사전에는 없는 운영 테이블이다. 근거는 [schema.sql](../../../product-registration/database/schema.sql)의 DDL·`finish_registration` 함수, 작성 기준일은 2026-11-08이다. 실제 원본 DB 반영과 별도 테스트 DB 검증은 전체 검증 기록에서 구분한다.

한 행은 성공적으로 생성한 상품 한 건의 감사 사건이다. 등록 원장·상품·색인 작업과 같은 트랜잭션에서만 추가된다. 요청 UUID, 상품 ID, 규칙 버전, 확정 입력 지문, 실행 사용자를 기록하여 어떤 검증 기준의 입력이 저장되었는지 추적한다. 실패·취소된 요청의 전체 기록이나 사용자의 대화 전문을 저장하는 테이블은 아니다.

## 컬럼과 키

| 물리명 | 문서용 의미 | 타입 | NULL | 기본값 | 해석·단위 |
| --- | --- | --- | --- | --- | --- |
| audit_id | 감사 사건 ID | bigint | 불가 | GENERATED ALWAYS AS IDENTITY | PK, DB가 생성한 기술 식별자 |
| request_id | 등록 요청 UUID | uuid | 불가 | 없음 | UNIQUE, 성공 요청당 감사 기록 1행 |
| product_id | 생성 상품 ID | numeric(10,0) | 불가 | 없음 | 원본 상품 PK |
| rule_version | 적용 규칙 버전 | text | 불가 | 없음 | 등록 원장의 규칙 버전 사본 |
| payload_sha256 | 입력 SHA-256 | text | 불가 | 없음 | 등록 원장의 UTF-8 정규 JSON 지문 사본 |
| event | 사건 종류 | text | 불가 | `'product_registered'` | 동일 값만 허용하는 CHECK |
| actor_id | 실행 사용자 ID | numeric(10,0) | 불가 | `101` | `actor_id=101` CHECK |
| created_at | 사건 시각 | timestamptz | 불가 | `now()` | 등록 트랜잭션 시각 |

PK는 `registration_audit_pkey(audit_id)`, 고유 제약은 `registration_audit_request_id_key(request_id)`다. 복합키는 없다. 감사 ID는 연속 업무 번호가 아니며 트랜잭션 실패로 결번이 생길 수 있다.

## 물리 외래키와 양방향 참조

| 방향 | FK 제약조건 | 자식 컬럼 → 부모 컬럼 | 삭제 / 갱신 | 업무 의미 |
| --- | --- | --- | --- | --- |
| 나감 | registration_audit_request_id_fkey | registration_audit.request_id → [registration_request](registration_request.md).request_id | NO ACTION / NO ACTION | 성공 요청의 근거 |
| 나감 | registration_audit_product_id_fkey | registration_audit.product_id → [adempiere.m_product](../idempiere/m/m_product.md).m_product_id | NO ACTION / NO ACTION | 감사 대상 상품 |
| 들어옴 | 없음 | 이 신규 스키마에서 이 테이블을 참조하는 FK 없음 | 해당 없음 | DDL 기준 확인 |

모든 물리 FK는 기본 즉시 검사다. 사용자 101은 고정 실행 정책으로 검증하며 `actor_id`에는 물리 FK가 없다. 감사 행의 상품 ID·규칙 버전·지문과 원장 값의 일치는 등록 함수 및 provenance 뷰가 검증하는 논리 조건이다. 별도 복합 FK로 선언된 것은 아니다.

## 조회·해석 주의사항

등록 API 로그인은 이 테이블에 직접 INSERT·UPDATE·DELETE할 수 없다. NOLOGIN 전용 소유자의 고정 범위 함수만 사건을 추가한다. 기존 SQL 챗봇 읽기 역할에 감사 테이블 조회·쓰기 권한을 추가하지 않는다. 상태 조회에는 [색인 작업](indexing_job.md)의 상태를 별도로 확인한다. 감사 사건의 존재는 OpenSearch 색인이 완료되었다는 뜻이 아니다.
