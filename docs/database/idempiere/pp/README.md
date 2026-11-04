# pp — 제조·생산 계획·제품 구성

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 23개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`pp_cost_collector`](pp_cost_collector.md) | 제조 원가 수집 문서 | Manufacturing Cost Collector | 0 | 제조 주문·공정·구성품의 실제 수량과 작업 시간을 기록하여 원가 집계에 사용하는 문서다. |
| [`pp_cost_collectorma`](pp_cost_collectorma.md) | 제조 원가 수집 속성 배분 | Manufacturing Order MA | 0 | 제조 원가 수집 문서의 이동 수량을 속성 집합 인스턴스별로 배분한다. |
| [`pp_mrp`](pp_mrp.md) | 자재 소요 계획 | Material Requirement Planning | 56 | 자재 소요 계획(MRP)에 사용하는 계획 내역을 저장한다. |
| [`pp_order`](pp_order.md) | 제조 주문 | Manufacturing Order | 2 | 지정된 부품 또는 제품을 정해진 수량으로 제조하도록 지시하는 문서다. |
| [`pp_order_bom`](pp_order_bom.md) | 제조 주문 BOM | Manufacturing Order BOM | 2 | 제조 주문에 적용한 BOM 및 배합 정보를 저장한다. 기본 정보는 제품 계획에서 가져온다. |
| [`pp_order_bom_trl`](pp_order_bom_trl.md) | 제조 주문 BOM 번역 | Manufacturing Order BOM Trl | 2 | 제조 주문 BOM의 언어별 번역 정보를 저장한다. |
| [`pp_order_bomline`](pp_order_bomline.md) | 제조 주문 BOM 구성행 | Manufacturing Order BOM Line | 4 | 완제품 제조에 사용할 각 구성품 정보를 주문별 BOM 행으로 저장한다. |
| [`pp_order_bomline_trl`](pp_order_bomline_trl.md) | 제조 주문 BOM 구성행 번역 | Manufacturing Order BOM Line Trl | 4 | 제조 주문 BOM 구성행의 언어별 번역 정보를 저장한다. |
| [`pp_order_cost`](pp_order_cost.md) | 제조 주문 원가 | Manufacturing Order Cost | 0 | 제조할 제품의 원가 요소별 원가 기록을 제조 주문에 연결한다. |
| [`pp_order_node`](pp_order_node.md) | 제조 주문 공정 | Manufacturing Order Activity | 2 | 제조 주문의 작업 경로를 구성하는 개별 공정을 정의한다. |
| [`pp_order_node_asset`](pp_order_node_asset.md) | 제조 주문 공정 자산 | Manufacturing Order Activity Asset | 0 | 제조 주문 공정에 사용하는 자산을 연결한다. |
| [`pp_order_node_product`](pp_order_node_product.md) | 제조 주문 공정 제품 | Manufacturing Order Activity Product | 0 | 제조 주문 공정에 사용하는 제품을 연결한다. |
| [`pp_order_node_trl`](pp_order_node_trl.md) | 제조 주문 공정 번역 | Manufacturing Order Activity Trl | 2 | 제조 주문의 공정 단계에 대한 언어별 번역 정보를 저장한다. |
| [`pp_order_nodenext`](pp_order_nodenext.md) | 제조 주문 공정 전이 | Manufacturing Order Activity Next | 0 | 제조 주문에서 현재 공정과 다음 공정의 연결을 정의한다. |
| [`pp_order_workflow`](pp_order_workflow.md) | 제조 주문 작업 흐름 | Manufacturing Order Workflow | 2 | 제조 주문에 적용한 작업 흐름을 저장한다. |
| [`pp_order_workflow_trl`](pp_order_workflow_trl.md) | 제조 주문 작업 흐름 번역 | Manufacturing Order Workflow Trl | 2 | 제조 주문 작업 흐름의 언어별 번역 정보를 저장한다. |
| [`pp_product_bom`](pp_product_bom.md) | 제품 BOM·배합 | BOM &amp; Formula | 7 | 제품의 자재명세서와 배합을 정의한다. |
| [`pp_product_bom_trl`](pp_product_bom_trl.md) | 제품 BOM·배합 번역 | BOM &amp; Formula Trl | 7 | 제품 자재명세서와 배합의 언어별 번역 정보를 저장한다. |
| [`pp_product_bomline`](pp_product_bomline.md) | 제품 BOM 구성행 | BOM Line | 21 | 완제품의 BOM 및 배합에 들어가는 개별 구성품 정보를 정의한다. |
| [`pp_product_bomline_trl`](pp_product_bomline_trl.md) | 제품 BOM 구성행 번역 | BOM Line Trl | 21 | 제품 BOM 구성행의 언어별 번역 정보를 저장한다. |
| [`pp_product_planning`](pp_product_planning.md) | 제품 생산·조달 계획 | Product Planning | 219 | 제품에 적용하는 생산 및 조달 계획 정보를 정의한다. |
| [`pp_wf_node_asset`](pp_wf_node_asset.md) | 작업 흐름 공정 자산 | Workflow Node Asset | 0 | 작업 흐름의 공정 단계에서 사용하는 자산을 연결한다. |
| [`pp_wf_node_product`](pp_wf_node_product.md) | 작업 흐름 공정 제품 | Workflow Node Product | 0 | 작업 흐름의 공정 단계에서 사용하는 제품을 연결한다. |
