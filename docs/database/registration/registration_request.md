# registration_request — 상품 등록 요청·멱등성 원장

<!-- table-id: poc_idempiere.poc_registration.registration_request -->

[DB 전체 목록](../index.md) · [상품 등록 실습](../../product-registration/lab.md) · [실제 검증](../../product-registration/verification.md) · [웹 구조](../../product-registration/web.md) · [감사 기록](registration_audit.md) · [색인 작업](indexing_job.md)

## 기본 정보와 업무 역할

물리명은 `poc_idempiere.poc_registration.registration_request`다. 논리명은 이번 로컬 PoC 구현의 문서용 명칭이며 iDempiere 원본 사전 테이블이 아니다. 근거는 [schema.sql](../../../product-registration/database/schema.sql)의 실제 DDL 및 등록 함수이며, 2026-11-08 기준으로 작성했다. 원본 `adempiere` 스키마는 변경하지 않는다. 원본 DB 설치 여부와 별도 PostgreSQL 통합시험은 전체 검증 보고에서 구분한다.

한 행은 성공적으로 커밋된 상품 등록 요청 하나다. 새 분류·단위·세금 분류, 상품, 이 원장, 감사 기록, 색인 작업을 같은 트랜잭션에서 생성한다. 실패한 요청은 성공 원장으로 남지 않는다. 같은 UUID·동일 초안 SHA-256·동일 규칙 버전은 기존 결과를 반환하고, 다른 초안 또는 버전에 같은 UUID를 재사용하면 충돌한다. 재전송 확인은 S3 재조회보다 먼저 수행하므로 이미 성공한 요청은 규칙 저장소 장애 중에도 상태를 조회할 수 있다.

## 컬럼과 키

| 물리명 | 문서용 의미 | 타입 | NULL | 기본값 | 해석·단위 |
| --- | --- | --- | --- | --- | --- |
| request_id | 등록 요청 UUID | uuid | 불가 | 없음 | PK. 클라이언트가 확인 요청마다 생성하고 재전송 시 유지 |
| payload_sha256 | 확정 입력 지문 | text | 불가 | 없음 | 정렬 키·UTF-8 JSON의 SHA-256, 소문자 16진수 64자리 CHECK |
| rule_version | 검증 규칙 버전 | text | 불가 | 없음 | S3 객체 버전 등을 포함한 식별자, 1~1024자 CHECK |
| product_id | 생성 상품 ID | numeric(10,0) | 불가 | 없음 | UNIQUE, 상품 물리 PK와 같은 식별자 |
| draft | 확정 입력 원문 | jsonb | 불가 | 없음 | JSON 객체 CHECK. code/name/description/category/uom/tax/usage/weight/pack |
| created_masters | 함께 생성한 마스터 ID | jsonb | 불가 | `'{}'::jsonb` | category/uom/tax 중 새로 만든 ID만 기록 |
| actor_id | 등록 실행 사용자 | numeric(10,0) | 불가 | `101` | `actor_id=101` CHECK, GardenWorld 고정 실행 사용자 |
| created_at | 커밋 요청 생성 시각 | timestamptz | 불가 | `now()` | 트랜잭션 시각, 저장 단위는 시각 |

PK는 `registration_request_pkey(request_id)`, 고유 제약은 `registration_request_product_id_key(product_id)`다. 복합키는 없다.

## 물리 외래키와 양방향 참조

모든 FK의 삭제·갱신 규칙은 `NO ACTION / NO ACTION`, 기본 즉시 검사다. 상품 및 운영 원장을 삭제해 연결을 자동 제거하지 않는다.

| 방향 | FK 제약조건 | 자식 컬럼 → 부모 컬럼 | 업무 의미 |
| --- | --- | --- | --- |
| 나감 | registration_request_product_id_fkey | registration_request.product_id → [adempiere.m_product](../idempiere/m/m_product.md).m_product_id | 이 요청으로 생성한 상품 |
| 들어옴 | registration_audit_request_id_fkey | [registration_audit](registration_audit.md).request_id → registration_request.request_id | 성공 요청의 감사 기록 |
| 들어옴 | indexing_job_request_id_fkey | [indexing_job](indexing_job.md).request_id → registration_request.request_id | 같은 커밋에서 만든 색인 작업 |

`actor_id`는 고정 사용자 정책으로 검증하지만 물리 FK를 선언하지 않았다. `created_masters` 내부 ID도 JSON이며 FK가 아니다. 물리 FK가 없는 것과 검사하지 않은 관계를 구별한다.

## 조회·해석 주의사항

상품은 GardenWorld 테넌트 11·조직 11·사용자 101로 생성한다. 공통 마스터는 테넌트 0/조직 0 또는 테넌트 11/조직 0·11의 활성 행만 사용한다. 신규 마스터는 테넌트 11/조직 11에 생성한다. `weight=null`은 미확인 무게이며 0으로 바꾸지 않는다. `pack`은 기본 단위당 포장 수량으로 1 이상의 정수다. 예를 들어 `PKG / 1鉢`를 기본 단위로 새로 등록할 때도 포장 수량은 기본 단위와 별도 필드다.

`registered_product_provenance` 뷰는 요청·감사·색인 작업·상품을 연결한 최소 식별자만 공개한다. 기존 OpenSearch 실습은 이 뷰로 입증된 신규 상품만 최초 상품 해시의 비교 대상에서 제외한다. 코드 접두사만으로 미등록 추가 행을 제외하지 않는다. [Python 저장소](../../../product-registration/backend/product_registration/store.py)는 SQL 챗봇 읽기 계정 대신 전용 API 자격정보를 사용한다.
