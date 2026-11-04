# w — 웹 상점·카운터

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 11개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`w_advertisement`](w_advertisement.md) | 웹 광고 | Advertisement | 1 | 웹에 게시하는 광고 정보를 저장한다. |
| [`w_basket`](w_basket.md) | 웹 장바구니 | Basket | 0 | 웹 상점의 장바구니 기본 정보를 저장한다. |
| [`w_basketline`](w_basketline.md) | 웹 장바구니행 | Basket Line | 0 | 장바구니에 담긴 개별 품목 내역을 저장한다. |
| [`w_click`](w_click.md) | 웹 클릭 기록 | Web Click | 0 | 웹에서 발생한 개별 클릭을 기록한다. |
| [`w_clickcount`](w_clickcount.md) | 웹 클릭 집계 | Click Count | 1 | 웹 클릭 수를 관리하는 집계 정보를 저장한다. |
| [`w_counter`](w_counter.md) | 웹 방문 집계 원천 | Web Counter | 0 | 개별 웹 접근 횟수 기록을 저장한다. |
| [`w_countercount`](w_countercount.md) | 웹 방문 수 집계 | Counter Count | 1 | 웹 카운터의 누적 횟수를 관리한다. |
| [`w_mailmsg`](w_mailmsg.md) | 웹 상점 메일 서식 | Mail Message | 0 | 웹 상점에서 발송하는 메일 메시지의 서식을 저장한다. |
| [`w_mailmsg_trl`](w_mailmsg_trl.md) | 웹 상점 메일 서식 번역 | Mail Message Trl | 0 | 웹 상점 메일 메시지 서식의 언어별 번역 정보를 저장한다. |
| [`w_store`](w_store.md) | 웹 상점 | Web Store | 1 | 테넌트가 운영하는 웹 상점의 기본 정보를 정의한다. |
| [`w_store_trl`](w_store_trl.md) | 웹 상점 번역 | Web Store Trl | 1 | 웹 상점의 언어별 번역 정보를 저장한다. |
