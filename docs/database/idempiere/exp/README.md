# exp — 데이터 내보내기 형식·처리기

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 5개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`exp_format`](exp_format.md) | 데이터 내보내기 형식 | Export Format | 10 | 내보낼 대상 테이블·필터 조건·버전과 형식 식별자를 정의한다. |
| [`exp_formatline`](exp_formatline.md) | 내보내기 형식 항목 | Format Line | 43 | 형식의 항목 순서·대상 컬럼·필수 여부·날짜 형식 및 중첩 형식을 정의한다. |
| [`exp_processor`](exp_processor.md) | 데이터 내보내기 처리기 | Export Processor | 2 | 내보내기 처리기 유형에 연결되는 실행 설정과 대상 호스트·포트·계정 설정을 관리한다. |
| [`exp_processor_type`](exp_processor_type.md) | 내보내기 처리기 유형 | Export Processor Type | 2 | 내보내기 처리기의 종류와 실행 Java 클래스를 정의한다. |
| [`exp_processorparameter`](exp_processorparameter.md) | 내보내기 처리 매개변수 | Processor Parameter | 7 | 개별 내보내기 처리기에 전달할 이름별 매개변수 값을 관리한다. |
