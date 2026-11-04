# imp — 가져오기·프로세서 설정

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 4개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`imp_processor`](imp_processor.md) | 가져오기 처리기 | Import Processor | 2 | 가져오기 처리기의 유형, 실행 주기와 연결 설정을 정의한다. |
| [`imp_processor_type`](imp_processor_type.md) | 가져오기 처리기 유형 | Import Processor Type | 2 | 가져오기 처리기 유형과 해당 구현 클래스 정보를 정의한다. |
| [`imp_processorlog`](imp_processorlog.md) | 가져오기 처리 로그 | Import Processor Log | 0 | 가져오기 처리기 실행의 요약·오류 여부와 상세 메시지를 기록한다. |
| [`imp_processorparameter`](imp_processorparameter.md) | 가져오기 처리 매개변수 | Import Processor Parameter | 6 | 가져오기 처리기에 전달하는 이름별 매개변수 값을 저장한다. |
