# ws — 웹 서비스

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 7개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`ws_webservice`](ws_webservice.md) | 웹 서비스 정의 | Web Service | 2 | 웹 서비스의 코드·이름·설명과 도움말을 정의한다. |
| [`ws_webservice_para`](ws_webservice_para.md) | 웹 서비스 매개변수 | Web Service Parameters | 46 | 웹 서비스 유형에 속하는 매개변수 이름·유형 및 상수값을 정의한다. |
| [`ws_webservicefieldinput`](ws_webservicefieldinput.md) | 웹 서비스 입력 필드 | Web Service Field Input | 45 | 웹 서비스 유형별 입력 열과 참조·식별자 판정 규칙을 정의한다. |
| [`ws_webservicefieldoutput`](ws_webservicefieldoutput.md) | 웹 서비스 출력 필드 | Web Service Field Output | 8 | 웹 서비스 유형이 응답에 포함할 테이블 열을 정의한다. |
| [`ws_webservicemethod`](ws_webservicemethod.md) | 웹 서비스 메서드 | Web Service Method | 9 | 웹 서비스에 속하는 개별 호출 메서드의 코드·이름·설명을 정의한다. |
| [`ws_webservicetype`](ws_webservicetype.md) | 웹 서비스 유형 | Web Service Type | 16 | 서비스와 메서드를 대상 테이블 및 매개변수 삽입 설정에 연결한다. |
| [`ws_webservicetypeaccess`](ws_webservicetypeaccess.md) | 웹 서비스 유형 접근 권한 | Web Service Type Access | 16 | 역할별 웹 서비스 유형 접근과 읽기·쓰기 권한을 정의한다. |
