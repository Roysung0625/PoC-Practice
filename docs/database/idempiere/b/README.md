# b — 입찰·토픽·구매자/판매자 연결

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 10개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`b_bid`](b_bid.md) | 경매 입찰 | Bid | 0 | 경매 주제에 대한 입찰을 기록한다. 일반 구매발주와 구분되는 경매 기능의 데이터다. |
| [`b_bidcomment`](b_bidcomment.md) | 경매 입찰 의견 | Bid Comment | 0 | 입찰 주제에 남긴 의견을 저장한다. |
| [`b_buyer`](b_buyer.md) | 경매 구매 참여자 | B_Buyer | 0 | 사용자와 연결되는 경매 구매 참여자의 이름·설명·유효 종료일을 관리한다. |
| [`b_buyerfunds`](b_buyerfunds.md) | 경매 구매자 자금 | Buyer Funds | 0 | 주제별 입찰에 사용되는 구매자의 자금 내역을 관리한다. |
| [`b_offer`](b_offer.md) | 경매 제안 | Offer | 0 | 경매 주제에 대한 판매 제안을 기록한다. |
| [`b_seller`](b_seller.md) | 경매 판매 참여자 | B_Seller | 0 | 사용자와 연결되는 경매 판매 참여자의 정보와 내부 참여자 여부를 관리한다. |
| [`b_sellerfunds`](b_sellerfunds.md) | 경매 판매자 자금 | Seller Funds | 0 | 주제별 판매 제안에서 발생하는 판매자의 자금 내역을 관리한다. |
| [`b_topic`](b_topic.md) | 경매 주제 | Topic | 0 | 입찰과 판매 제안의 대상이 되는 경매 주제를 정의한다. |
| [`b_topiccategory`](b_topiccategory.md) | 경매 주제 분류 | Topic Category | 0 | 경매 주제를 분류하는 범주를 관리한다. |
| [`b_topictype`](b_topictype.md) | 경매 주제 유형 | Topic Type | 0 | 경매 주제의 유형을 정의한다. |
