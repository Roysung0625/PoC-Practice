# dd — 물류 이동·분배 주문

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 4개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`dd_networkdistribution`](dd_networkdistribution.md) | 재고 배분 네트워크 | Network Distribution | 2 | 재고 분배에 사용할 네트워크의 상위 정의를 관리한다. |
| [`dd_networkdistributionline`](dd_networkdistributionline.md) | 재고 배분 네트워크 명세 | Network Distribution Line | 10 | 재고 배분 네트워크의 출발·도착 창고, 운송사, 배분 비율·이송 시간·우선순위와 유효 기간을 정의한다. |
| [`dd_order`](dd_order.md) | 재고 배분 주문 | Distribution Order | 0 | 재고 배분을 지시하는 주문의 머리글을 관리한다. |
| [`dd_orderline`](dd_orderline.md) | 재고 배분 주문 명세 | Distribution Order Line | 0 | 재고 배분 주문에 포함되는 개별 배분 내역을 관리한다. |
