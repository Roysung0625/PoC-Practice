# u — POS·수표 제한·웹 메뉴 설정

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 5개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`u_blacklistcheque`](u_blacklistcheque.md) | 사용 제한 수표 | Black List Cheque | 0 | 은행 이름과 사용 제한 대상으로 등록된 수표 번호를 저장한다. |
| [`u_posterminal`](u_posterminal.md) | 판매시점 단말기 | POS Terminal | 1 | POS 단말기의 창고·가격표·담당자·프린터 및 현금·카드·수표 결제 연결 설정을 저장한다. |
| [`u_rolemenu`](u_rolemenu.md) | 역할별 웹 메뉴 | Role Menu | 74 | 사용자 역할과 접근할 웹 메뉴를 연결한다. |
| [`u_web_properties`](u_web_properties.md) | 웹 속성 설정 | Web Properties | 143 | 웹 기능에 사용하는 키·값 형태의 설정을 저장한다. |
| [`u_webmenu`](u_webmenu.md) | 웹 메뉴 | Web Menu | 143 | 웹 메뉴의 링크·상위 메뉴·표시 순서·이미지 등 탐색 구조를 정의한다. |
