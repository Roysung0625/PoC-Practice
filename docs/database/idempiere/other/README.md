# other — 접두사 공통 분류 없음

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 4개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`dbreplicasyncverifier`](dbreplicasyncverifier.md) | DB 복제 동기화 확인 정보 | — | 1 | lastupdate 값만 가진 내부 테이블로 물리명상 DB 복제 동기화 확인 용도로 추정된다. 갱신 주체와 판정 방식은 구조만으로 확인할 수 없다. |
| [`test`](test.md) | 자료형 시험 | Test ID | 2 | 문자·숫자·날짜·금액·JSON 및 업무 참조 등 여러 자료형을 시험하는 테이블이다. 업무 원장으로 해석하지 않는다. |
| [`testuu`](testuu.md) | UUID 기반 시험 | Test UU Based Table | 2 | UUID 기반 테이블 기능을 시험하는 이름·값·설명 데이터를 저장한다. |
| [`testuudet`](testuudet.md) | UUID 시험 상세 | Test UU Detail | 3 | UUID 기반 시험 레코드와 연결된 상세 이름을 저장한다. |
