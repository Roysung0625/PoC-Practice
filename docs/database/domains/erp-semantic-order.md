# 주문·수주·발주 — 근거 기반 분류안·공식 분류 아님

[전체 일람](../index.md)

분류 근거: 원본 사전 Name/Description + 주요 열/물리 FK 교차대조(문서 overlay 자동 규칙). 물리적 연결과 업무 의미의 확정은 구분합니다.

주문/발주·요청 헤더와 상세의 거래처·상품·일자 참조를 탐색합니다. 판매/구매 방향은 별도 필드를 확인합니다.

관계 흐름 근거(실제 물리 FK의 자식 → 부모; 실행 시간 순서 아님):

- `c_order.(c_ordersource_id)` → `c_ordersource.(c_ordersource_id)` (`c_order__c_orders_c_ordersou`).
- `c_order.(ref_order_id)` → `c_order.(c_order_id)` (`corder_ref`).
- `c_order.(link_order_id)` → `c_order.(c_order_id)` (`linkorder_corder`).
- `c_order.(quotationorder_id)` → `c_order.(c_order_id)` (`quotationorder_corder`).
- `c_orderlandedcost.(c_order_id)` → `c_order.(c_order_id)` (`corder_corderlandedcost`).
- `c_orderlandedcostallocation.(c_orderlandedcost_id)` → `c_orderlandedcost.(c_orderlandedcost_id)` (`corderlandedcost_corderlandedc`).
- `c_orderlandedcostallocation.(c_orderline_id)` → `c_orderline.(c_orderline_id)` (`corderline_corderlandedcostall`).
- `c_orderline.(c_order_id)` → `c_order.(c_order_id)` (`corder_corderline`).

[항목별 사전·열·FK 근거](../classification-evidence.md). 기존 canonical 폴더·설명은 표의 별도 열로 남깁니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| poc_idempiere | adempiere | c_order | 판매 주문·구매 발주 (사전: Order) | c: 거래처·주문·청구·결제·회계 기준 (기존 분류안) | 주문·수주·발주 | 판매 주문과 구매 발주의 머리글을 함께 저장한다. 판매·구매 구분, 문서 유형, 거래처, 주문일, 창고, 통화 및 납품·청구 상태를 확인하여 조회 범위를 결정한다. | [문서](../idempiere/c/c_order.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Order'; Description='Order'; 주요 열 issotrx, dateordered, c_bpartner_id, c_bpartner_location_id; FK corder_corderlandedcost, corder_corderline; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-c_order) | <!-- table-id: poc_idempiere.adempiere.c_order -->
| poc_idempiere | adempiere | c_orderlandedcost | 구매 발주 예상 부대원가 (사전: Estimated Landed Cost) | c: 거래처·주문·청구·결제·회계 기준 (기존 분류안) | 주문·수주·발주 | 구매 발주에 대한 예상 취득 부대원가를 관리한다. | [문서](../idempiere/c/c_orderlandedcost.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Estimated Landed Cost'; Description='Estimated Landed Cost for Purchase Order'; 주요 열 c_order_id; FK corderlandedcost_corderlandedc, corder_corderlandedcost; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-c_orderlandedcost) | <!-- table-id: poc_idempiere.adempiere.c_orderlandedcost -->
| poc_idempiere | adempiere | c_orderlandedcostallocation | 발주 예상 부대원가 배부 (사전: Estimated Landed Cost Allocation) | c: 거래처·주문·청구·결제·회계 기준 (기존 분류안) | 주문·수주·발주 | 주문·발주 명세에 예상 취득 부대원가를 배부한 내역을 관리한다. | [문서](../idempiere/c/c_orderlandedcostallocation.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Estimated Landed Cost Allocation'; Description='Estimate landed cost allocation for order line'; 주요 열 c_orderlandedcost_id, c_orderline_id; FK corderlandedcost_corderlandedc, corderline_corderlandedcostall; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-c_orderlandedcostallocation) | <!-- table-id: poc_idempiere.adempiere.c_orderlandedcostallocation -->
| poc_idempiere | adempiere | c_orderline | 판매 주문·구매 발주 명세 (사전: Sales Order Line) | c: 거래처·주문·청구·결제·회계 기준 (기존 분류안) | 주문·수주·발주 | 주문·발주에 포함된 개별 상품 등의 상세 행을 관리한다. 사전명은 Sales Order Line이지만 상위 c_order의 판매·구매 구분에 따라 해석해야 한다. | [문서](../idempiere/c/c_orderline.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Sales Order Line'; Description='Sales Order Line'; 주요 열 c_order_id, c_bpartner_id, c_bpartner_location_id, dateordered; FK corderline_corderlandedcostall, corderline_iorder; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-c_orderline) | <!-- table-id: poc_idempiere.adempiere.c_orderline -->
| poc_idempiere | adempiere | c_ordersource | 주문 유입 경로 (사전: Order Source) | c: 거래처·주문·청구·결제·회계 기준 (기존 분류안) | 주문·수주·발주 | 주문이 들어온 경로를 구분하는 코드·이름·설명을 관리한다. | [문서](../idempiere/c/c_ordersource.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Order Source'; 주요 열 근거 부족; FK c_order__c_orders_c_ordersou, cordersource_iorder; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-c_ordersource) | <!-- table-id: poc_idempiere.adempiere.c_ordersource -->
| poc_idempiere | adempiere | m_requisition | 자재 요청서 (사전: Requisition) | m: 제품·재고·출하/입고·원가 (기존 분류안) | 주문·수주·발주 | 자재 조달 요청 문서의 기본 정보를 저장한다. | [문서](../idempiere/m/m_requisition.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Requisition'; Description='Material Requisition'; 주요 열 m_pricelist_id; FK mrequisition_mrequisitionline; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-m_requisition) | <!-- table-id: poc_idempiere.adempiere.m_requisition -->
| poc_idempiere | adempiere | m_requisitionline | 자재 요청행 (사전: Requisition Line) | m: 제품·재고·출하/입고·원가 (기존 분류안) | 주문·수주·발주 | 자재 요청서의 개별 요청 내역을 저장한다. | [문서](../idempiere/m/m_requisitionline.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Requisition Line'; Description='Material Requisition Line'; 주요 열 m_requisition_id, c_orderline_id, c_bpartner_id; FK corderline_mrequisitionline, mrequisition_mrequisitionline; 사전 의미와 열/FK가 주문·수주·발주를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-m_requisitionline) | <!-- table-id: poc_idempiere.adempiere.m_requisitionline -->
