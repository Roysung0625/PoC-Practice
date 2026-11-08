# 경매·입찰·판매 제안 — 근거 기반 분류안·공식 분류 아님

[전체 일람](../index.md)

분류 근거: 원본 사전 Name/Description + 주요 열/물리 FK 교차대조(문서 overlay 자동 규칙). 물리적 연결과 업무 의미의 확정은 구분합니다.

사전이 명시한 경매 토픽·입찰/판매 제안·참여자 자금의 참조를 탐색합니다.

관계 흐름 근거(실제 물리 FK의 자식 → 부모; 실행 시간 순서 아님):

- `b_bid.(b_buyerfunds_id)` → `b_buyerfunds.(b_buyerfunds_id)` (`bbuyerfunds_bbid`).
- `b_bid.(b_topic_id)` → `b_topic.(b_topic_id)` (`btopic_bbid`).
- `b_bidcomment.(b_topic_id)` → `b_topic.(b_topic_id)` (`btopic_bbidcomment`).
- `b_offer.(b_sellerfunds_id)` → `b_sellerfunds.(b_sellerfunds_id)` (`bsellerfunds_boffer`).
- `b_offer.(b_topic_id)` → `b_topic.(b_topic_id)` (`btopic_boffer`).
- `b_topic.(b_topiccategory_id)` → `b_topiccategory.(b_topiccategory_id)` (`btopiccategory_btopic`).
- `b_topic.(b_topictype_id)` → `b_topictype.(b_topictype_id)` (`btopictype_btopic`).
- `b_topiccategory.(b_topictype_id)` → `b_topictype.(b_topictype_id)` (`btopictype_btopiccategory`).

[항목별 사전·열·FK 근거](../classification-evidence.md). 기존 canonical 폴더·설명은 표의 별도 열로 남깁니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| poc_idempiere | adempiere | b_bid | 경매 입찰 (사전: Bid) | b: 입찰·토픽·구매자/판매자 연결 (기존 분류안) | 경매·입찰·판매 제안 | 경매 주제에 대한 입찰을 기록한다. 일반 구매발주와 구분되는 경매 기능의 데이터다. | [문서](../idempiere/b/b_bid.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Bid'; Description='Bid for a Topic'; 주요 열 b_topic_id, b_buyerfunds_id; FK bbuyerfunds_bbid, btopic_bbid; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-b_bid) | <!-- table-id: poc_idempiere.adempiere.b_bid -->
| poc_idempiere | adempiere | b_bidcomment | 경매 입찰 의견 (사전: Bid Comment) | b: 입찰·토픽·구매자/판매자 연결 (기존 분류안) | 경매·입찰·판매 제안 | 입찰 주제에 남긴 의견을 저장한다. | [문서](../idempiere/b/b_bidcomment.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Bid Comment'; Description='Make a comment to a Bid Topic'; 주요 열 근거 부족; FK btopic_bbidcomment; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-b_bidcomment) | <!-- table-id: poc_idempiere.adempiere.b_bidcomment -->
| poc_idempiere | adempiere | b_buyerfunds | 경매 구매자 자금 (사전: Buyer Funds) | b: 입찰·토픽·구매자/판매자 연결 (기존 분류안) | 경매·입찰·판매 제안 | 주제별 입찰에 사용되는 구매자의 자금 내역을 관리한다. | [문서](../idempiere/b/b_buyerfunds.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Buyer Funds'; Description='Buyer Funds for Bids on Topics'; 주요 열 근거 부족; FK bbuyerfunds_bbid; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-b_buyerfunds) | <!-- table-id: poc_idempiere.adempiere.b_buyerfunds -->
| poc_idempiere | adempiere | b_offer | 경매 제안 (사전: Offer) | b: 입찰·토픽·구매자/판매자 연결 (기존 분류안) | 경매·입찰·판매 제안 | 경매 주제에 대한 판매 제안을 기록한다. | [문서](../idempiere/b/b_offer.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Offer'; Description='Offer for a Topic'; 주요 열 b_topic_id, b_sellerfunds_id; FK bsellerfunds_boffer, btopic_boffer; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-b_offer) | <!-- table-id: poc_idempiere.adempiere.b_offer -->
| poc_idempiere | adempiere | b_sellerfunds | 경매 판매자 자금 (사전: Seller Funds) | b: 입찰·토픽·구매자/판매자 연결 (기존 분류안) | 경매·입찰·판매 제안 | 주제별 판매 제안에서 발생하는 판매자의 자금 내역을 관리한다. | [문서](../idempiere/b/b_sellerfunds.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Seller Funds'; Description='Seller Funds from Offers on Topics'; 주요 열 근거 부족; FK bsellerfunds_boffer; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-b_sellerfunds) | <!-- table-id: poc_idempiere.adempiere.b_sellerfunds -->
| poc_idempiere | adempiere | b_topic | 경매 주제 (사전: Topic) | b: 입찰·토픽·구매자/판매자 연결 (기존 분류안) | 경매·입찰·판매 제안 | 입찰과 판매 제안의 대상이 되는 경매 주제를 정의한다. | [문서](../idempiere/b/b_topic.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Topic'; Description='Auction Topic'; 주요 열 b_topictype_id, b_topiccategory_id; FK btopic_bbid, btopic_bbidcomment; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-b_topic) | <!-- table-id: poc_idempiere.adempiere.b_topic -->
| poc_idempiere | adempiere | b_topiccategory | 경매 주제 분류 (사전: Topic Category) | b: 입찰·토픽·구매자/판매자 연결 (기존 분류안) | 경매·입찰·판매 제안 | 경매 주제를 분류하는 범주를 관리한다. | [문서](../idempiere/b/b_topiccategory.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Topic Category'; Description='Auction Topic Category'; 주요 열 b_topictype_id; FK btopiccategory_btopic, btopictype_btopiccategory; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-b_topiccategory) | <!-- table-id: poc_idempiere.adempiere.b_topiccategory -->
| poc_idempiere | adempiere | b_topictype | 경매 주제 유형 (사전: Topic Type) | b: 입찰·토픽·구매자/판매자 연결 (기존 분류안) | 경매·입찰·판매 제안 | 경매 주제의 유형을 정의한다. | [문서](../idempiere/b/b_topictype.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Topic Type'; Description='Auction Topic Type'; 주요 열 m_pricelist_id; FK btopictype_btopic, btopictype_btopiccategory; 사전 의미와 열/FK가 경매·입찰·판매 제안를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-b_topictype) | <!-- table-id: poc_idempiere.adempiere.b_topictype -->
