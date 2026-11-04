# 청구·대변 문서 — 근거 기반 분류안·공식 분류 아님

[전체 일람](../index.md)

분류 근거: 원본 사전 Name/Description + 주요 열/물리 FK 교차대조(문서 overlay 자동 규칙). 물리적 연결과 업무 의미의 확정은 구분합니다.

청구 헤더·상세·세금·문서 유형의 연결을 탐색합니다. 금액의 세금 처리나 집계식은 별도 업무 규칙입니다.

관계 흐름 근거(실제 물리 FK의 자식 → 부모; 실행 시간 순서 아님):

- `c_invoice.(ref_invoice_id)` → `c_invoice.(c_invoice_id)` (`cinvoice_ref`).
- `c_invoice.(relatedinvoice_id)` → `c_invoice.(c_invoice_id)` (`relatedinvoice_cinvoice`).
- `c_invoice.(reversal_id)` → `c_invoice.(c_invoice_id)` (`reversal_cinvoice`).
- `c_invoicebatchline.(c_invoice_id)` → `c_invoice.(c_invoice_id)` (`cinvoice_cinvoicebatchline`).
- `c_invoicebatchline.(c_invoicebatch_id)` → `c_invoicebatch.(c_invoicebatch_id)` (`cinvoicebatch_cinvoicebline`).
- `c_invoicebatchline.(c_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` (`cinvoiceline_cinvoicebline`).
- `c_invoiceline.(c_invoice_id)` → `c_invoice.(c_invoice_id)` (`cinvoice_cinvoiceline`).
- `c_invoiceline.(ref_invoiceline_id)` → `c_invoiceline.(c_invoiceline_id)` (`convoiceline_ref`).

[항목별 사전·열·FK 근거](../classification-evidence.md). 기존 canonical 폴더·설명은 표의 별도 열로 남깁니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| poc_idempiere | adempiere | c_invoice | 매출·매입 청구서 (사전: Invoice) | c: 거래처·주문·청구·결제·회계 기준 (기존 분류안) | 청구·대변 문서 | 고객 매출 청구와 공급업체 매입 청구의 머리글을 저장하며 문서 유형에 따라 신용전표도 포함한다. 판매·구매 구분, 거래처, 청구일, 통화, 합계 및 지급 상태를 관리하므로 금액 분석 시 문서 유형과 취소 관계를 함께 확인한다. | [문서](../../../docs/database/idempiere/c/c_invoice.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Invoice'; Description='Invoice Identifier'; 주요 열 dateinvoiced, totallines, grandtotal; FK cinvoice_cinvoicebatchline, cinvoice_cinvoiceline; 사전 의미와 열/FK가 청구·대변 문서를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-c_invoice) | <!-- table-id: poc_idempiere.adempiere.c_invoice -->
| poc_idempiere | adempiere | c_invoicebatch | 비용 청구 일괄 입력 (사전: Invoice Batch) | c: 거래처·주문·청구·결제·회계 기준 (기존 분류안) | 청구·대변 문서 | 비용 청구서를 일괄 입력·처리하는 배치의 머리글을 관리한다. | [문서](../../../docs/database/idempiere/c/c_invoicebatch.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Invoice Batch'; Description='Expense Invoice Batch Header'; 주요 열 근거 부족; FK cinvoicebatch_cinvoicebline; 사전 의미와 열/FK가 청구·대변 문서를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-c_invoicebatch) | <!-- table-id: poc_idempiere.adempiere.c_invoicebatch -->
| poc_idempiere | adempiere | c_invoicebatchline | 비용 청구 일괄 입력 명세 (사전: Invoice Batch Line) | c: 거래처·주문·청구·결제·회계 기준 (기존 분류안) | 청구·대변 문서 | 비용 청구 배치에 포함된 개별 입력 행을 관리한다. | [문서](../../../docs/database/idempiere/c/c_invoicebatchline.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Invoice Batch Line'; Description='Expense Invoice Batch Line'; 주요 열 c_invoicebatch_id, dateinvoiced, c_invoice_id, c_invoiceline_id; FK cinvoice_cinvoicebatchline, cinvoicebatch_cinvoicebline; 사전 의미와 열/FK가 청구·대변 문서를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-c_invoicebatchline) | <!-- table-id: poc_idempiere.adempiere.c_invoicebatchline -->
| poc_idempiere | adempiere | c_invoiceline | 매출·매입 청구 명세 (사전: Invoice Line) | c: 거래처·주문·청구·결제·회계 기준 (기존 분류안) | 청구·대변 문서 | 청구서의 개별 상품·서비스 등 상세 행을 저장한다. 상위 청구서가 판매·구매 또는 신용전표인지 함께 확인해야 한다. | [문서](../../../docs/database/idempiere/c/c_invoiceline.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Invoice Line'; Description='Invoice Detail Line'; 주요 열 c_invoice_id, qtyinvoiced, ref_invoiceline_id; FK cinvliceline_iinvoice, cinvoiceline_cinvoicebline; 사전 의미와 열/FK가 청구·대변 문서를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-c_invoiceline) | <!-- table-id: poc_idempiere.adempiere.c_invoiceline -->
| poc_idempiere | adempiere | m_matchinv | 입출고·송장 대사 (사전: Match Invoice) | m: 제품·재고·출하/입고·원가 (기존 분류안) | 청구·대변 문서 | 출하·입고 내역과 송장 내역의 대응 관계를 저장한다. | [문서](../../../docs/database/idempiere/m/m_matchinv.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Match Invoice'; Description='Match Shipment/Receipt to Invoice'; 주요 열 c_invoiceline_id; FK convoiceline_mmatchinv, refmatchinv_mmatchinv; 사전 의미와 열/FK가 청구·대변 문서를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-m_matchinv) | <!-- table-id: poc_idempiere.adempiere.m_matchinv -->
