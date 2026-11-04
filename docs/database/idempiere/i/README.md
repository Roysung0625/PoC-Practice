# i — 데이터 가져오기 준비

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 19개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`i_asset`](i_asset.md) | 자산 가져오기 임시 데이터 | Asset | 0 | 자산과 감가상각·계정·소재지 정보를 정식 데이터로 가져오기 전에 저장하며 가져오기 여부와 오류 메시지를 관리한다. |
| [`i_bankstatement`](i_bankstatement.md) | 은행명세 가져오기 임시 데이터 | Import Bank Statement | 0 | 외부 은행거래 명세를 정식 명세로 가져오기 위한 입력 데이터를 저장한다. |
| [`i_bpartner`](i_bpartner.md) | 거래처 가져오기 임시 데이터 | Import Business Partner | 0 | 거래처·주소·연락처와 고객·공급업체·직원 구분을 가져오기 전에 저장하며 결과 식별자와 오류 상태를 관리한다. |
| [`i_conversion_rate`](i_conversion_rate.md) | 환율 가져오기 임시 데이터 | Import Conversion Rate | 2 | 외부 통화 환율을 가져오기 위한 입력 데이터를 저장한다. |
| [`i_elementvalue`](i_elementvalue.md) | 계정과목 가져오기 | Import Account | 0 | 외부 계정 코드와 계정 유형·상위 계정 정보를 계정과목 사전으로 가져오기 위한 중간 데이터를 저장한다. |
| [`i_fajournal`](i_fajournal.md) | 고정자산 분개 가져오기 | FA Journal | 0 | 자산 식별자와 감가상각 여부, 분개 차대변 금액을 포함한 고정자산 관련 분개 가져오기 데이터를 저장한다. |
| [`i_fixedasset`](i_fixedasset.md) | 고정자산 가져오기 | Imported Fixed Asset | 0 | 취득원가·누적감가상각·사용연수 등 외부 고정자산 정보를 자산 대장으로 옮기기 위한 데이터를 저장한다. |
| [`i_gljournal`](i_gljournal.md) | 총계정원장 분개 가져오기 | Import GL Journal | 0 | 외부 총계정원장 분개를 가져오기 위한 입력 데이터를 보관한다. |
| [`i_hr_movement`](i_hr_movement.md) | 급여 변동 내역 가져오기 | Payroll Movement Import | 0 | 거래처·급여 개념·처리 건별 금액과 수량을 급여 변동 내역으로 가져오기 위한 데이터를 저장한다. |
| [`i_inoutlineconfirm`](i_inoutlineconfirm.md) | 출하·입고 확인행 가져오기 | Ship/Receipt Confirmation Import Line | 0 | 외부의 자재 출하 또는 입고 확인행을 시스템으로 가져오기 위한 중간 데이터다. |
| [`i_inventory`](i_inventory.md) | 재고 거래 가져오기 | Import Inventory | 0 | 외부 재고 거래를 시스템 재고 문서로 가져오기 위한 입력 데이터를 저장한다. |
| [`i_invoice`](i_invoice.md) | 송장 가져오기 | Import Invoice | 0 | 외부 송장 데이터를 시스템 송장으로 등록하기 위한 중간 데이터를 보관한다. |
| [`i_movement`](i_movement.md) | 재고 이동 가져오기 | I_Movement_ID | 0 | 출발·도착 보관 위치와 제품·이동 수량을 재고 이동 문서 및 행으로 가져오기 위한 데이터를 저장한다. |
| [`i_order`](i_order.md) | 주문 가져오기 | Import Order | 0 | 외부 주문을 시스템 주문으로 등록하기 위한 중간 데이터를 저장한다. |
| [`i_payment`](i_payment.md) | 지급·수금 가져오기 | Import Payment | 0 | 외부 지급 또는 수금 데이터를 결제 기록으로 가져오기 위한 입력 데이터를 저장한다. |
| [`i_pricelist`](i_pricelist.md) | 가격표 가져오기 | Import Price List | 0 | 가격표 및 그 버전을 외부 데이터에서 가져오기 위한 중간 데이터를 저장한다. |
| [`i_product`](i_product.md) | 제품·서비스 가져오기 | Import Product | 0 | 외부 품목 또는 서비스 정보를 제품 사전에 등록하기 위한 입력 데이터를 보관한다. |
| [`i_productplanning`](i_productplanning.md) | 제품 계획 가져오기 | Import Product Planning | 0 | 제품·창고별 보충 정책과 BOM·자원·안전재고 등을 제품 계획으로 가져오기 위한 데이터를 저장한다. |
| [`i_reportline`](i_reportline.md) | 보고서 행 집합 가져오기 | Import Report Line Set | 0 | 외부의 보고서 행 집합 값을 보고서 정의로 가져오기 위한 데이터를 저장한다. |
