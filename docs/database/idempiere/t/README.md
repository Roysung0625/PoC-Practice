# t — 작업·보고서용 보조 테이블

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 23개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`t_1099extract`](t_1099extract.md) | 1099 신고 추출 자료 | 1099 Extract | 0 | 실행 건별 거래처·납세자 식별자와 연도별 금액 구간을 저장하는 1099 신고용 추출 자료다. |
| [`t_aging`](t_aging.md) | 채권·채무 연령 분석 자료 | T_Aging | 0 | 실행 건별 송장 미결 금액을 만기 경과 및 도래 기간 구간으로 나눈 보고용 자료다. |
| [`t_alter_column`](t_alter_column.md) | 열 변경 정의 | — | 0 | 테이블·열 이름과 변경할 자료형·NULL·기본값 절을 저장한다. 실제 실행 및 보관 용도는 코드 확인이 필요하다. |
| [`t_bankregister`](t_bankregister.md) | 은행 거래부 자료 | Bank Register | 0 | 실행 건별 은행·계정·거래처와 회계일·차대변 금액·잔액을 저장하는 거래부 보고 자료다. |
| [`t_bom_indented`](t_bom_indented.md) | 계층형 BOM 보고 자료 | Indented BOM Report | 0 | BOM을 계층 들여쓰기 형태로 표시하기 위한 보고 자료를 저장한다. |
| [`t_bomline`](t_bomline.md) | BOM 임시 전개행 | Temporal BOM Line | 0 | BOM 전개 및 역전개 결과의 계층·제품·구성 수량·원가를 실행 건별로 임시 저장한다. |
| [`t_cashflow`](t_cashflow.md) | 현금 흐름 보고 자료 | T_CashFlow_ID | 0 | 송장·주문·현금 계획 등을 원천으로 한 금액·거래일·확률을 실행 건별로 저장한다. |
| [`t_distributionrundetail`](t_distributionrundetail.md) | 배분 실행 계산 자료 | T_DistributionRunDetail | 0 | 배분 실행에서 거래처·제품별 배분 비율과 최소 수량·계산 수량을 저장한다. |
| [`t_fact_acct_history`](t_fact_acct_history.md) | 회계 전기 이력 자료 | Accounting Fact History | 0 | 회계 전기 레코드와 동일한 계정·차대변 금액·업무 차원 등의 이력 정보를 저장한다. 이력 생성 및 보존 조건은 확인이 필요하다. |
| [`t_inventoryvalue`](t_inventoryvalue.md) | 재고 평가 보고 자료 | T_InventoryValue | 0 | 실행 건별 제품·창고·속성 인스턴스의 재고 수량과 가격·원가 기준 평가 금액을 저장한다. |
| [`t_invoicegl`](t_invoicegl.md) | 송장 환산 손익 자료 | T_InvoiceGL | 0 | 송장과 회계 전기별 미결 금액·통화 잔액·재평가 차액을 저장한다. 사전 설명상 실제 표시 자료는 T_InvoiceGL_v에서 제공된다. |
| [`t_moveclient`](t_moveclient.md) | 테넌트 이동 키 대응 | — | 0 | 실행 건별 테이블의 원본 키와 대상 키 및 식별자를 저장한다. 실제 테넌트 이동 절차에서의 사용 방식은 확인이 필요하다. |
| [`t_mrp_crp`](t_mrp_crp.md) | 소요·능력 계획 임시 자료 | Temporal MRP &amp; CRP | 0 | MRP 및 CRP 처리의 실행 건별 순서와 설명을 임시 저장한다. |
| [`t_reconciliation`](t_reconciliation.md) | 계정 대사 보고 자료 | Account reconciliation report | 0 | 보고서 실행 건별 회계 전기 레코드와 대사 코드를 연결한다. |
| [`t_replenish`](t_replenish.md) | 재고 보충 계산 자료 | T_Replenish | 0 | 실행 건별 현재고·예약·주문 수량과 보충 수준을 바탕으로 계산한 발주 수량을 저장한다. |
| [`t_report`](t_report.md) | 보고서 임시 자료 | T_Report | 0 | 보고서 생성 중 사용하는 행별 임시 결과를 저장한다. |
| [`t_reportstatement`](t_reportstatement.md) | 계정 명세 보고 자료 | T_ReportStatement | 0 | 실행 건별 회계 전기의 일자·차대변 금액·잔액·수량을 명세서용으로 저장한다. |
| [`t_selection`](t_selection.md) | 처리 대상 선택값 | — | 0 | 프로세스 실행 건에 선택된 레코드 식별자와 뷰 식별자를 연결한다. |
| [`t_selection2`](t_selection2.md) | 질의별 처리 대상 선택값 | — | 0 | 프로세스 실행 건과 질의 식별자별로 선택된 레코드 식별자를 저장한다. |
| [`t_selection_infowindow`](t_selection_infowindow.md) | 정보 창 선택 자료 | — | 0 | 정보 창에서 선택한 레코드의 열별 문자·날짜·숫자 값을 실행 건과 연결한다. |
| [`t_spool`](t_spool.md) | 임시 출력 메시지 | T_Spool | 0 | 임시 출력에 사용하는 메시지를 저장한다. |
| [`t_transaction`](t_transaction.md) | 재고 수불 보고 자료 | T_Transaction | 0 | 실행 건별 재고 거래와 관련 입출고·이동·실사·생산 문서의 정보를 보고용으로 저장한다. |
| [`t_trialbalance`](t_trialbalance.md) | 시산표 보고 자료 | Trial Balance | 0 | 실행 건별 계정·회계 전기의 차대변 금액과 잔액을 시산표용으로 저장한다. |
