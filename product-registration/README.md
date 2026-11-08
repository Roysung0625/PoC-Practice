# GardenWorld 상품 등록

분석 웹의 [商品登録](http://127.0.0.1:8010/products/new)에서 일본어로 상품을 설명하고, 유사 상품을 참고해 입력한 뒤 GardenWorld에 등록한다. 이 폴더가 등록 기능의 소스 진입점이다. 화면과 API는 기존 분석 웹·FastAPI 프로세스에서 실행한다.

| 작업 | 소스 |
|---|---|
| 입력 화면, 참고 상품 복사, 도움말, 오류 위치 복귀 | [frontend/](frontend/) |
| 정규화, 검색, 규칙 검사, 트랜잭션 호출, 검색 반영 | [backend/product_registration/](backend/product_registration/) |
| PostgreSQL 역할·스키마 설치, 등록 함수, 검색 평가 | [database/](database/) |
| 웹 경로·세션·CSRF 및 내부 API 연결 | 호스트의 [Laravel 경로](../analysis-chatbot/routes/web.php), [컨트롤러](../analysis-chatbot/app/Http/Controllers/ProductRegistrationController.php), [FastAPI 진입점](../local/python/poc/api.py) |
| S3 규칙 원본, 게시 도구, IAM·버킷 정의 | [aws/registration/](../aws/registration/README.md) |

처음 사용하는 담당자는 [라벤더 상품 등록 실습](../docs/product-registration/lab.md)부터, 운영자는 [설치·실행·복구 안내](../docs/product-registration/README.md)부터 읽는다. [검증 기록](../docs/product-registration/verification.md)에서 실제 원본 등록 결과와 모의 시험을 구분해 확인할 수 있다.

등록 화면 모델의 [단위 시험](frontend/model.test.ts)은 화면 코드와 함께 둔다. 공용 FastAPI의 [등록 API 시험](../local/python/tests/test_registration_flow_api.py)과 [격리 DB 저장 시험](../local/python/tests/test_registration_store.py), Laravel의 [프록시 시험](../analysis-chatbot/tests/ProductRegistrationTest.php)과 [브라우저 시험](../analysis-chatbot/e2e/product-registration.spec.ts)은 각 호스트의 기존 시험 명령으로 실행한다.
