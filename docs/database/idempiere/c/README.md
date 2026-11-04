# c — 거래처·주문·청구·결제·회계 기준

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 198개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`c_1099box`](c_1099box.md) | 1099 신고 항목 | 1099 Box | 0 | 1099 신고의 기재 항목을 코드·이름과 버킷 값으로 정의한다. 구체적 신고 처리 규칙은 구조만으로 확정할 수 없다. |
| [`c_acctprocessor`](c_acctprocessor.md) | 회계 처리기 | Accounting Processor | 1 | 회계 처리 프로세서 또는 서버의 실행 매개변수를 관리한다. |
| [`c_acctprocessorlog`](c_acctprocessorlog.md) | 회계 처리 실행 로그 | Accounting Processor Log | 0 | 회계 처리기의 실행 결과를 저장하여 처리 이력과 오류 점검에 사용한다. |
| [`c_acctschema`](c_acctschema.md) | 회계 스키마 | Accounting Schema | 2 | 회계 처리 규칙을 정의하며 계정 구성요소와 기본 계정 설정의 상위 기준이 된다. |
| [`c_acctschema_default`](c_acctschema_default.md) | 회계 스키마 기본 계정 | C_AcctSchema_Default | 2 | 회계 스키마별 매출·비용·재고·채권·채무·세금 등의 업무별 기본 계정 조합을 지정한다. |
| [`c_acctschema_element`](c_acctschema_element.md) | 회계 스키마 구성요소 | Acct.Schema Element | 12 | 회계 스키마의 계정·조직·상품·거래처 등 분석 요소와 순서·필수 여부를 정의한다. |
| [`c_acctschema_gl`](c_acctschema_gl.md) | 회계 스키마 원장 계정 | C_AcctSchema_GL | 2 | 회계 스키마별 가계정·환율 균형·이익잉여금·조직 간 정산 등의 원장 처리용 계정을 지정한다. |
| [`c_activity`](c_activity.md) | 업무 활동 | Activity | 0 | 거래와 회계를 업무 활동별로 구분하는 기준정보를 관리한다. |
| [`c_activity_trl`](c_activity_trl.md) | 업무 활동 번역 | Activity Trl | 0 | 업무 활동의 언어별 표시 내용을 저장한다. |
| [`c_addresstransaction`](c_addresstransaction.md) | 주소 검증 이력 | Address Transaction | 0 | 검증 대상 주소와 검증 서비스·유효 판정·결과 메시지를 기록한다. |
| [`c_addressvalidation`](c_addressvalidation.md) | 주소 검증 서비스 연결 | Address Validation | 0 | 주소 검증 구현 설정에 연결되는 서비스 이용 설정과 연결 사용자·운송사 계정 등을 관리한다. |
| [`c_addressvalidationcfg`](c_addressvalidationcfg.md) | 주소 검증 구현 설정 | Address Validation Configuration | 0 | 주소 검증 클래스와 서비스 호스트·경로·프록시 연결 설정을 정의한다. |
| [`c_allocationhdr`](c_allocationhdr.md) | 입출금 소거 전표 | Allocation | 2 | 지급·수금과 청구서 사이의 금액 배분 및 소거 처리를 묶는 전표 머리글이다. |
| [`c_allocationline`](c_allocationline.md) | 입출금 소거 명세 | Allocation Line | 2 | 입출금 소거 전표에서 청구서·입출금·현금 명세를 연결하고 배분 금액·할인·상각·과부족 금액을 저장한다. |
| [`c_bank`](c_bank.md) | 은행 | Bank | 2 | 은행의 기준정보를 관리하며 은행계좌가 개설된 금융기관을 구분한다. |
| [`c_bankaccount`](c_bankaccount.md) | 은행계좌 | Bank Account | 3 | 은행에 개설된 계좌 정보를 관리하며 은행명세와 입출금 처리의 계좌 기준이 된다. |
| [`c_bankaccount_acct`](c_bankaccount_acct.md) | 은행계좌 회계 계정 | C_BankAccount_Acct | 6 | 은행계좌와 회계 스키마별 예금·미결제·이자·은행비용·환평가 계정 조합을 설정한다. |
| [`c_bankaccount_processor`](c_bankaccount_processor.md) | 은행계좌 결제 처리기 | Bank Account Processor | 2 | 은행계좌에 전자결제 처리기를 연결하고 허용 결제수단·통화·최소금액과 서비스 연결 설정을 지정한다. |
| [`c_bankaccountdoc`](c_bankaccountdoc.md) | 은행계좌 결제 문서 | Bank Account Document | 2 | 은행계좌의 결제 문서별 지급 방식·다음 번호·수표 인쇄 서식을 관리한다. |
| [`c_bankstatement`](c_bankstatement.md) | 은행거래 명세서 | Bank Statement | 2 | 은행계좌의 거래 명세서 머리글을 저장하며 개별 거래는 명세서 행에서 관리한다. |
| [`c_bankstatementline`](c_bankstatementline.md) | 은행거래 명세 행 | Bank statement line | 2 | 은행거래 명세서에 포함된 개별 계좌 거래를 저장한다. |
| [`c_bankstatementloader`](c_bankstatementloader.md) | 은행명세 가져오기 정의 | Bank Statement Loader | 0 | SWIFT·OFX 등 은행거래 명세를 가져오는 로더를 정의한다. |
| [`c_bankstatementmatcher`](c_bankstatementmatcher.md) | 은행명세 대조 규칙 | Bank Statement Matcher | 0 | 은행명세 정보를 거래처·청구서·입출금과 연결하는 대조 알고리즘을 정의한다. |
| [`c_banktransfer`](c_banktransfer.md) | 은행계좌 간 이체 | Bank Transfer | 0 | 은행계좌 간 자금 이체를 관리한다. |
| [`c_bp_bankaccount`](c_bp_bankaccount.md) | 거래처 은행계좌 | Partner Bank Account | 1 | 거래처의 은행계좌를 관리한다. 회사 자체 계좌 기준인 c_bankaccount와 구분한다. |
| [`c_bp_customer_acct`](c_bp_customer_acct.md) | 고객 회계 계정 | C_BP_Customer_Acct | 36 | 거래처와 회계 스키마별 매출채권·서비스 채권·고객 선입금 계정을 지정한다. |
| [`c_bp_edi`](c_bp_edi.md) | 거래처 EDI 정의 | EDI Definition | 0 | 거래처와의 전자문서 교환을 위한 EDI 정의를 관리한다. |
| [`c_bp_employee_acct`](c_bp_employee_acct.md) | 직원 회계 계정 | C_BP_Employee_Acct | 17 | 직원으로 취급되는 거래처의 비용 및 선급금 계정을 회계 스키마별로 지정한다. |
| [`c_bp_group`](c_bp_group.md) | 거래처 그룹 | Business Partner Group | 3 | 고객·공급업체 등 거래처를 공통 그룹으로 분류한다. |
| [`c_bp_group_acct`](c_bp_group_acct.md) | 거래처 그룹 회계 계정 | Business Partner Group Acct | 6 | 거래처 그룹과 회계 스키마별 채권·채무·선수선급·할인·미청구 관련 계정을 관리한다. |
| [`c_bp_relation`](c_bp_relation.md) | 거래처 간 관계 | Partner Relation | 1 | 거래처 사이의 관계를 정의한다. |
| [`c_bp_shippingacct`](c_bp_shippingacct.md) | 거래처 배송 계정 | Business Partner Shipping Account | 0 | 거래처 또는 거래처 주소에 배송 처리기와 운임·관세 관련 운송사 계정을 연결한다. |
| [`c_bp_vendor_acct`](c_bp_vendor_acct.md) | 공급업체 회계 계정 | C_BP_Vendor_Acct | 36 | 거래처와 회계 스키마별 매입채무·서비스 채무·공급업체 선급금 계정을 지정한다. |
| [`c_bp_withholding`](c_bp_withholding.md) | 거래처 원천징수 설정 | C_BP_Withholding | 0 | 거래처에 적용할 원천징수 유형과 의무 적용·임시 면제 여부 및 면제 사유를 관리한다. |
| [`c_bpartner`](c_bpartner.md) | 거래처 | Business Partner | 18 | 고객·공급업체·직원 등 업무상 거래 상대방의 공통 기준정보를 관리한다. |
| [`c_bpartner_location`](c_bpartner_location.md) | 거래처 주소 연결 | Partner Location | 16 | 거래처의 배송지 등 주소 용도를 관리하며 공통 주소와 거래처를 연결한다. |
| [`c_bpartner_product`](c_bpartner_product.md) | 거래처별 상품 정보 | Product Business Partner | 1 | 거래처와 상품별 상대방 상품번호·제조사·품질 등급·최소 잔여 유통기한 조건을 관리한다. |
| [`c_calendar`](c_calendar.md) | 회계 달력 | Calendar | 1 | 회계 연도와 기간을 구성하는 달력 기준정보를 관리한다. |
| [`c_campaign`](c_campaign.md) | 마케팅 캠페인 | Campaign | 2 | 마케팅 캠페인을 정의하고 관련 영업 및 거래를 캠페인별로 구분한다. |
| [`c_campaign_trl`](c_campaign_trl.md) | 마케팅 캠페인 번역 | Campaign Trl | 2 | 마케팅 캠페인의 언어별 표시 내용을 저장한다. |
| [`c_cash`](c_cash.md) | 현금 출납 전표 | Cash Journal | 3 | 현금 출납 내역을 묶는 현금 일지의 머리글을 관리한다. |
| [`c_cashbook`](c_cashbook.md) | 소액현금 출납장 | Cash Book | 2 | 소액현금 거래를 기록하는 출납장의 기준정보를 관리한다. |
| [`c_cashbook_acct`](c_cashbook_acct.md) | 현금 출납장 회계 계정 | C_CashBook_Acct | 4 | 출납장과 회계 스키마별 현금자산·이체·차이·비용·수입 계정을 설정한다. |
| [`c_cashline`](c_cashline.md) | 현금 출납 명세 | Cash Journal Line | 5 | 현금 출납 전표의 개별 현금 거래를 저장한다. |
| [`c_cashplan`](c_cashplan.md) | 자금 계획 | Cash Plan | 0 | 예상 자금 흐름을 계획 단위로 묶어 관리한다. |
| [`c_cashplanline`](c_cashplanline.md) | 자금 계획 명세 | Cash Plan Line | 0 | 자금 계획의 개별 예상 자금 내역을 관리한다. |
| [`c_channel`](c_channel.md) | 판매 채널 | Channel | 2 | 판매 경로를 구분하는 채널 기준정보를 관리한다. |
| [`c_charge`](c_charge.md) | 부대 수익·비용 항목 | Charge | 3 | 거래 문서에 추가되는 요금이나 부대 수익·비용 항목을 정의한다. |
| [`c_charge_acct`](c_charge_acct.md) | 부대 항목 회계 계정 | C_Charge_Acct | 6 | 부대 항목과 회계 스키마별 수익 및 비용 계정을 지정한다. |
| [`c_charge_trl`](c_charge_trl.md) | 부대 항목 번역 | Charge Trl | 3 | 부대 수익·비용 항목의 언어별 표시 내용을 저장한다. |
| [`c_chargetype`](c_chargetype.md) | 부대 항목 유형 | Charge Type | 0 | 부대 수익·비용 항목을 유형별로 분류하는 기준을 관리한다. |
| [`c_chargetype_doctype`](c_chargetype_doctype.md) | 문서 유형별 부대 항목 유형 | Charge Type by Doc Type | 0 | 문서 유형별로 사용할 수 있는 부대 수익·비용 항목 유형을 연결한다. |
| [`c_city`](c_city.md) | 도시 | City | 1 | 주소에 사용하는 도시 기준정보를 관리한다. |
| [`c_commission`](c_commission.md) | 판매 수수료 규칙 | Commission | 1 | 판매 수수료의 산정 기준을 정의하고 세부 조건과 계산 실행 결과를 연결한다. |
| [`c_commissionamt`](c_commissionamt.md) | 판매 수수료 계산 금액 | Commission Amount | 0 | 수수료 계산 실행에서 산출된 금액을 저장한다. |
| [`c_commissiondetail`](c_commissiondetail.md) | 판매 수수료 산출 근거 | Commission Detail | 0 | 계산된 수수료 금액을 뒷받침하는 상세 근거를 저장한다. |
| [`c_commissionline`](c_commissionline.md) | 판매 수수료 세부 규칙 | Commission Line | 1 | 상품·거래처·영업지역 등의 적용 범위와 금액·수량의 차감값 및 배수를 지정한다. |
| [`c_commissionrun`](c_commissionrun.md) | 판매 수수료 계산 실행 | Commission Run | 0 | 판매 수수료의 계산 실행 단위를 관리하고 계산 금액과 근거 상세를 실행별로 묶는다. |
| [`c_contactactivity`](c_contactactivity.md) | 연락처 활동 | Contact Activity | 0 | 연락처와 관련된 이벤트·업무·의사소통 내역을 기록한다. |
| [`c_conversion_rate`](c_conversion_rate.md) | 환율 | Conversion Rate | 4 | 통화 간 금액 변환에 사용하는 환율을 관리한다. |
| [`c_conversiontype`](c_conversiontype.md) | 환율 유형 | Currency Type | 4 | 통화 환산에 사용할 환율의 유형을 정의한다. |
| [`c_costcenter`](c_costcenter.md) | 원가 중심점 | Cost Center | 0 | 비용 귀속 단위로 참조하는 원가 중심점의 코드와 이름을 관리한다. |
| [`c_country`](c_country.md) | 국가 | Country | 251 | 주소와 지역 구분에 사용하는 국가 기준정보를 관리한다. |
| [`c_country_trl`](c_country_trl.md) | 국가 번역 | Country Trl | 251 | 국가의 언어별 표시 내용을 저장한다. |
| [`c_countrygroup`](c_countrygroup.md) | 국가 그룹 | Country Group | 0 | 조세 협정 등 공통 조건을 공유하는 국가 집합을 정의한다. |
| [`c_countrygroup_trl`](c_countrygroup_trl.md) | 국가 그룹 번역 | Country Group Trl | 0 | 국가 그룹의 이름과 설명을 언어별로 저장한다. |
| [`c_countrygroupcountry`](c_countrygroupcountry.md) | 국가 그룹 소속 국가 | Country on Country Group | 0 | 국가와 국가 그룹의 소속 관계 및 적용 시작·종료일을 관리한다. |
| [`c_currency`](c_currency.md) | 통화 | Currency | 175 | 거래와 회계 금액을 표시하는 통화의 기준정보를 관리한다. |
| [`c_currency_acct`](c_currency_acct.md) | 통화 환차손익 계정 | C_Currency_Acct | 0 | 통화와 회계 스키마별 실현·미실현 환차익 및 환차손 계정을 지정한다. |
| [`c_currency_trl`](c_currency_trl.md) | 통화 번역 | Currency Trl | 175 | 통화의 언어별 표시 내용을 저장한다. |
| [`c_cycle`](c_cycle.md) | 프로젝트 보고 주기 | Project Cycle | 2 | 프로젝트 보고에 사용할 주기 또는 단계 체계를 정의한다. |
| [`c_cyclephase`](c_cyclephase.md) | 보고 주기 단계 연결 | C_CyclePhase | 10 | 프로젝트 보고 주기의 세부 단계와 표준 프로젝트 단계를 연결한다. |
| [`c_cyclestep`](c_cyclestep.md) | 프로젝트 보고 주기 세부 단계 | Cycle Step | 4 | 프로젝트 보고 주기 안의 개별 단계를 정의한다. |
| [`c_department`](c_department.md) | 부서 | Department | 0 | 거래·회계 분석에서 참조하는 부서의 코드와 이름을 관리한다. 급여 부서 hr_department와 별도 기준정보다. |
| [`c_depositbatch`](c_depositbatch.md) | 일괄 입금 전표 | Deposit Batch | 0 | 여러 입출금 기록을 은행계좌 입금 단위로 묶고 입금일·통화·합계금액과 문서 상태를 관리한다. |
| [`c_depositbatchline`](c_depositbatchline.md) | 일괄 입금 명세 | Deposit Batch Line | 0 | 일괄 입금 전표에 포함되는 입출금 기록과 해당 금액을 행 단위로 저장한다. |
| [`c_docbasegroup`](c_docbasegroup.md) | 문서 기본 유형 그룹 | Document Base Type Group | 0 | 회계 기간 통제에 사용할 문서 기본 유형의 그룹을 정의한다. |
| [`c_docbasegroupline`](c_docbasegroupline.md) | 문서 기본 유형 그룹 명세 | Document Base Type Group Line | 0 | 문서 기본 유형 그룹에 포함되는 항목을 관리한다. |
| [`c_doctype`](c_doctype.md) | 문서 유형 | Document Type | 52 | 업무 문서의 유형과 처리 규칙을 정의한다. |
| [`c_doctype_trl`](c_doctype_trl.md) | 문서 유형 번역 | Document Type Trl | 52 | 문서 유형의 언어별 표시 내용을 저장한다. |
| [`c_doctypecounter`](c_doctypecounter.md) | 대응 문서 관계 | Counter Document | 1 | 원 문서와 그에 대응하는 문서 유형의 관계를 정의한다. |
| [`c_dunning`](c_dunning.md) | 연체 독촉 규칙 | Dunning | 2 | 지급 기한이 지난 청구서에 적용할 독촉 규칙을 관리한다. |
| [`c_dunninglevel`](c_dunninglevel.md) | 연체 독촉 단계 | Dunning Level | 2 | 독촉 규칙별 연체 일수·독촉 간격·이자·수수료·인쇄 문구와 신용 중지 조건 등을 정의한다. |
| [`c_dunninglevel_trl`](c_dunninglevel_trl.md) | 연체 독촉 단계 번역 | Dunning Level Trl | 2 | 독촉 단계의 인쇄 명칭과 안내 문구를 언어별로 저장한다. |
| [`c_dunningrun`](c_dunningrun.md) | 연체 독촉 실행 | Dunning Run | 0 | 독촉 대상 선정과 문서 생성 등을 묶는 독촉 실행 단위를 관리한다. |
| [`c_dunningrunentry`](c_dunningrunentry.md) | 연체 독촉 실행 대상 | Dunning Run Entry | 0 | 독촉 실행에서 거래처·주소·담당 연락처별 독촉 금액과 단계 및 안내 문구를 묶는다. |
| [`c_dunningrunline`](c_dunningrunline.md) | 연체 독촉 실행 명세 | Dunning Run Line | 0 | 독촉 대상의 청구서·입출금별 미결제액·연체 일수·독촉 횟수·이자·수수료를 기록한다. |
| [`c_element`](c_element.md) | 계정 요소 체계 | Element | 1 | 회계 계정 요소의 체계를 정의하며 개별 요소 값의 상위 기준이 된다. |
| [`c_elementvalue`](c_elementvalue.md) | 계정 요소 값 | Account Element | 379 | 계정 요소 체계의 개별 값 또는 계정과목을 관리한다. |
| [`c_elementvalue_trl`](c_elementvalue_trl.md) | 계정 요소 값 번역 | Account Element Trl | 379 | 개별 계정 요소 값의 언어별 표시 내용을 저장한다. |
| [`c_greeting`](c_greeting.md) | 서신 인사말 | Greeting | 1 | 서신 등에 인쇄할 호칭이나 인사말을 정의한다. |
| [`c_greeting_trl`](c_greeting_trl.md) | 서신 인사말 번역 | Greeting Trl | 1 | 인쇄용 호칭·인사말의 언어별 표현을 저장한다. |
| [`c_interorg_acct`](c_interorg_acct.md) | 조직 간 정산 계정 | C_InterOrg_Acct | 0 | 회계 스키마와 송수신 조직 조합별 조직 간 지급·수취 계정을 지정한다. |
| [`c_invoice`](c_invoice.md) | 매출·매입 청구서 | Invoice | 8 | 고객 매출 청구와 공급업체 매입 청구의 머리글을 저장하며 문서 유형에 따라 신용전표도 포함한다. 판매·구매 구분, 거래처, 청구일, 통화, 합계 및 지급 상태를 관리하므로 금액 분석 시 문서 유형과 취소 관계를 함께 확인한다. |
| [`c_invoicebatch`](c_invoicebatch.md) | 비용 청구 일괄 입력 | Invoice Batch | 0 | 비용 청구서를 일괄 입력·처리하는 배치의 머리글을 관리한다. |
| [`c_invoicebatchline`](c_invoicebatchline.md) | 비용 청구 일괄 입력 명세 | Invoice Batch Line | 0 | 비용 청구 배치에 포함된 개별 입력 행을 관리한다. |
| [`c_invoiceline`](c_invoiceline.md) | 매출·매입 청구 명세 | Invoice Line | 24 | 청구서의 개별 상품·서비스 등 상세 행을 저장한다. 상위 청구서가 판매·구매 또는 신용전표인지 함께 확인해야 한다. |
| [`c_invoicepayschedule`](c_invoicepayschedule.md) | 청구서 지급 일정 | Invoice Payment Schedule | 2 | 청구서별 지급 예정 일정과 분할 납부 내역을 관리한다. |
| [`c_invoiceschedule`](c_invoiceschedule.md) | 청구서 생성 일정 | Invoice Schedule | 1 | 청구서를 생성할 시점과 일정 규칙을 정의한다. |
| [`c_invoicetax`](c_invoicetax.md) | 청구서 세금 집계 | C_InvoiceTax | 8 | 청구서와 세금별 과세표준·세액·세금 포함 여부 및 세금 계산 제공자를 저장한다. |
| [`c_job`](c_job.md) | 직위 | Position | 4 | 직위의 명칭·분류와 직원용 여부를 정의하며 사용자 배치와 보수 설정에서 참조한다. |
| [`c_jobassignment`](c_jobassignment.md) | 사용자 직위 배치 | Position Assignment | 0 | 사용자를 직위에 배치하고 배치의 유효 기간을 관리한다. |
| [`c_jobcategory`](c_jobcategory.md) | 직위 분류 | Position Category | 4 | 직위를 묶는 분류의 이름·설명·도움말을 관리한다. |
| [`c_jobremuneration`](c_jobremuneration.md) | 직위 보수 연결 | Position Remuneration | 0 | 직위에 보수 기준을 연결하고 유효 기간을 지정한다. |
| [`c_landedcost`](c_landedcost.md) | 취득 부대원가 배부 설정 | Landed Cost | 0 | 청구 명세의 운송비 등 취득 부대원가를 입고·상품에 연결하고 원가 요소와 배부 기준을 지정한다. |
| [`c_landedcostallocation`](c_landedcostallocation.md) | 취득 부대원가 배부 결과 | Landed Cost Allocation | 0 | 청구 명세의 부대원가를 상품·입출고 명세·속성 인스턴스별로 배부한 금액과 수량·기준값을 저장한다. |
| [`c_location`](c_location.md) | 주소 | Address | 34 | 국가·지역·도시·우편번호 등을 포함하는 공통 주소 정보를 관리한다. |
| [`c_nonbusinessday`](c_nonbusinessday.md) | 비영업일 | Non Business Day | 1 | 업무를 수행하지 않는 날짜를 관리한다. |
| [`c_onlinetrxhistory`](c_onlinetrxhistory.md) | 온라인 처리 이력 | Online Transaction History | 0 | 대상 테이블과 레코드의 온라인 처리 메시지·오류 여부·처리 상태를 기록한다. |
| [`c_opportunity`](c_opportunity.md) | 영업 기회 | Sales Opportunity | 0 | 거래처별 영업 기회의 예상 금액·영업 단계·성사 확률·예상 종료일과 연결 주문을 관리한다. |
| [`c_order`](c_order.md) | 판매 주문·구매 발주 | Order | 8 | 판매 주문과 구매 발주의 머리글을 함께 저장한다. 판매·구매 구분, 문서 유형, 거래처, 주문일, 창고, 통화 및 납품·청구 상태를 확인하여 조회 범위를 결정한다. |
| [`c_orderlandedcost`](c_orderlandedcost.md) | 구매 발주 예상 부대원가 | Estimated Landed Cost | 0 | 구매 발주에 대한 예상 취득 부대원가를 관리한다. |
| [`c_orderlandedcostallocation`](c_orderlandedcostallocation.md) | 발주 예상 부대원가 배부 | Estimated Landed Cost Allocation | 0 | 주문·발주 명세에 예상 취득 부대원가를 배부한 내역을 관리한다. |
| [`c_orderline`](c_orderline.md) | 판매 주문·구매 발주 명세 | Sales Order Line | 27 | 주문·발주에 포함된 개별 상품 등의 상세 행을 관리한다. 사전명은 Sales Order Line이지만 상위 c_order의 판매·구매 구분에 따라 해석해야 한다. |
| [`c_orderpayschedule`](c_orderpayschedule.md) | 주문·발주 지급 일정 | Order Payment Schedule | 0 | 주문·발주별 지급 예정 일정을 관리한다. |
| [`c_ordersource`](c_ordersource.md) | 주문 유입 경로 | Order Source | 0 | 주문이 들어온 경로를 구분하는 코드·이름·설명을 관리한다. |
| [`c_ordertax`](c_ordertax.md) | 주문·발주 세금 집계 | Order Tax | 8 | 주문·발주와 세금별 과세표준·세액·세금 포함 여부 및 세금 계산 제공자를 저장한다. |
| [`c_orgassignment`](c_orgassignment.md) | 거래 조직 배정 | Org Assignment | 0 | 사용자를 거래 조직에 배정하고 배정의 유효 시작·종료일을 관리한다. |
| [`c_payment`](c_payment.md) | 수금·지급 전표 | Payment | 2 | 고객 수금과 공급업체 등에 대한 지급을 함께 저장하며 isreceipt로 입출금 방향을 구분한다. 은행계좌·거래처·청구서·금액·결제수단 및 소거·대사 상태를 관리한다. |
| [`c_paymentallocate`](c_paymentallocate.md) | 입출금의 청구서 배분 | Allocate Payment | 0 | 입출금을 청구서에 배분하고 배분 금액·할인·상각·과부족 금액 및 소거 명세 연결을 관리한다. |
| [`c_paymentbatch`](c_paymentbatch.md) | 전자 자금이체 배치 | Payment Batch | 0 | 전자 자금이체(EFT)를 위한 입출금 건을 배치로 묶는다. |
| [`c_paymentprocessor`](c_paymentprocessor.md) | 전자결제 처리기 | Payment Processor | 2 | 전자결제를 처리하는 서비스 또는 처리기의 설정을 관리한다. |
| [`c_paymentterm`](c_paymentterm.md) | 지급 조건 | Payment Term | 5 | 거래에 적용할 지급 시점과 할인 등의 조건을 정의한다. |
| [`c_paymentterm_trl`](c_paymentterm_trl.md) | 지급 조건 번역 | Payment Term Trl | 5 | 지급 시점·할인 조건의 언어별 표시 내용을 저장한다. |
| [`c_paymenttransaction`](c_paymenttransaction.md) | 결제 거래 | Payment Transaction | 0 | 전자결제 등의 개별 거래에서 결제수단·금액·처리기·승인 및 취소 결과와 연결 입출금 전표를 기록한다. |
| [`c_payschedule`](c_payschedule.md) | 지급 일정 서식 | Payment Schedule | 2 | 분할 지급 등의 일정 생성에 사용할 기준 서식을 정의한다. |
| [`c_payselection`](c_payselection.md) | 지급 대상 선정 | Payment Selection | 1 | 지급 대상으로 선택한 내역을 묶는 상위 단위를 관리한다. |
| [`c_payselectioncheck`](c_payselectioncheck.md) | 선정 지급 수표 | Pay Selection Check | 1 | 지급 대상 선정에서 생성·관리되는 수표 단위 정보를 저장한다. |
| [`c_payselectionline`](c_payselectionline.md) | 지급 대상 선정 명세 | Payment Selection Line | 1 | 지급 대상 선정에 포함되는 개별 지급 예정 내역을 저장한다. |
| [`c_period`](c_period.md) | 회계 기간 | Period | 360 | 회계 달력 안의 개별 기간을 관리한다. |
| [`c_periodcontrol`](c_periodcontrol.md) | 회계 기간 통제 | Period Control | 10,464 | 회계 기간과 문서 기본 유형별 개방·마감 상태 및 상태 변경 동작을 관리한다. |
| [`c_phase`](c_phase.md) | 프로젝트 표준 단계 | Standard Phase | 13 | 프로젝트 유형에 정의된 표준 단계를 관리한다. |
| [`c_pos`](c_pos.md) | 판매시점 단말기 | POS Terminal | 1 | 매장 판매에 사용하는 POS 단말기의 기준정보를 관리한다. |
| [`c_poskey`](c_poskey.md) | POS 기능 키 | POS Key | 163 | POS 화면에서 사용할 개별 기능 키를 정의한다. |
| [`c_poskeylayout`](c_poskeylayout.md) | POS 키 배치 | POS Key Layout | 5 | POS 기능 키의 배치 구성을 정의한다. |
| [`c_pospayment`](c_pospayment.md) | POS 결제 내역 | POS Payment | 0 | POS 주문의 결제수단별 금액과 수표·카드 관련 정보 및 연결 입출금 전표를 저장한다. |
| [`c_postendertype`](c_postendertype.md) | POS 결제수단 유형 | POS Tender Type | 0 | POS 결제수단의 코드·이름·기본 수단 및 보증·후일자 여부를 정의한다. |
| [`c_project`](c_project.md) | 프로젝트 | Project | 2 | 재무 관리 대상 프로젝트를 정의하며 단계·작업·투입·회계 내역을 프로젝트별로 연결한다. |
| [`c_project_acct`](c_project_acct.md) | 프로젝트 회계 계정 | C_Project_Acct | 4 | 프로젝트와 회계 스키마별 프로젝트 자산 및 진행 중 원가 계정을 지정한다. |
| [`c_projectissue`](c_projectissue.md) | 프로젝트 자재·노무 투입 | Project Issue | 0 | 프로젝트에 투입되는 자재와 노무 등의 사용 내역을 관리한다. |
| [`c_projectissuema`](c_projectissuema.md) | 프로젝트 투입 속성 배분 | C_ProjectIssueMA | 0 | 프로젝트 투입 건의 이동 수량을 상품 속성 인스턴스별로 나누어 기록한다. |
| [`c_projectline`](c_projectline.md) | 프로젝트 명세 | Project Line | 1 | 프로젝트의 과업 또는 수행 단계를 명세 행으로 관리한다. |
| [`c_projectphase`](c_projectphase.md) | 프로젝트 단계 | Project Phase | 0 | 개별 프로젝트에 실제로 적용되는 단계를 관리한다. |
| [`c_projecttask`](c_projecttask.md) | 프로젝트 작업 | Project Task | 0 | 프로젝트 단계 안에서 수행하는 실제 작업을 관리한다. |
| [`c_projecttype`](c_projecttype.md) | 프로젝트 유형 | Project Type | 4 | 프로젝트 유형과 표준 구성의 기준을 관리한다. |
| [`c_recurring`](c_recurring.md) | 반복 문서 정의 | Recurring | 1 | 반복적으로 생성할 업무 문서를 정의한다. |
| [`c_recurring_run`](c_recurring_run.md) | 반복 문서 실행 이력 | Recurring Run | 0 | 반복 문서 정의에 따른 실행 내역을 기록한다. |
| [`c_recurringgroup`](c_recurringgroup.md) | 반복 문서 그룹 | Recurring Group | 0 | 반복 문서 정의를 분류할 그룹의 코드·이름·설명을 관리한다. |
| [`c_region`](c_region.md) | 행정 지역 | Region | 399 | 주소에 사용하는 지리적 지역 기준정보를 관리한다. |
| [`c_region_trl`](c_region_trl.md) | 행정 지역 번역 | Region | 399 | 행정 지역의 언어별 표시 내용을 저장한다. |
| [`c_remuneration`](c_remuneration.md) | 보수 기준 | Remuneration | 0 | 보수 유형·표준 근무시간·기본 보수 및 초과근무 보수와 비용 기준을 정의한다. |
| [`c_revenuerecog_service`](c_revenuerecog_service.md) | 서비스 수익 인식 계획 | Revenue Recognition Service | 0 | 서비스를 기준으로 수익을 인식하거나 기록하는 계획을 관리한다. |
| [`c_revenuerecognition`](c_revenuerecognition.md) | 수익 인식 방식 | Revenue Recognition | 2 | 수익을 기록하는 인식 방법을 정의한다. |
| [`c_revenuerecognition_plan`](c_revenuerecognition_plan.md) | 수익 인식 계획 | Revenue Recognition Plan | 0 | 정의된 방식에 따라 수익을 인식하거나 기록할 계획을 관리한다. |
| [`c_revenuerecognition_run`](c_revenuerecognition_run.md) | 수익 인식 실행 | Revenue Recognition Run | 0 | 수익 인식 계획의 실행 내역을 관리한다. |
| [`c_rfq`](c_rfq.md) | 견적 요청 | RfQ | 1 | 잠재 공급업체에 제시할 견적 요청의 머리글을 관리한다. |
| [`c_rfq_topic`](c_rfq_topic.md) | 견적 요청 주제 | RfQ Topic | 1 | 견적 요청의 대상 주제를 정의한다. |
| [`c_rfq_topicsubscriber`](c_rfq_topicsubscriber.md) | 견적 요청 주제 참여자 | RfQ Subscriber | 2 | 견적 요청 주제의 참여자 또는 구독 대상을 관리한다. |
| [`c_rfq_topicsubscriberonly`](c_rfq_topicsubscriberonly.md) | 견적 요청 참여 범위 제한 | RfQ Topic Subscriber Restriction | 0 | 참여자가 특정 상품 또는 상품 분류의 견적 요청에만 포함되도록 제한한다. |
| [`c_rfqline`](c_rfqline.md) | 견적 요청 명세 | RfQ Line | 2 | 견적 요청에 포함되는 개별 항목을 관리한다. |
| [`c_rfqlineqty`](c_rfqlineqty.md) | 견적 요청 수량 조건 | RfQ Line Quantity | 2 | 견적 요청 명세별 수량 조건을 관리한다. |
| [`c_rfqresponse`](c_rfqresponse.md) | 공급업체 견적 응답 | RfQ Response | 0 | 잠재 공급업체의 견적 응답을 저장하며 제안 금액·납기·순위·선정 여부 및 연결 주문을 관리한다. |
| [`c_rfqresponseline`](c_rfqresponseline.md) | 공급업체 견적 응답 명세 | RfQ Response Line | 0 | 공급업체 견적 응답의 개별 요청 항목별 내용을 저장한다. |
| [`c_rfqresponselineqty`](c_rfqresponselineqty.md) | 견적 응답 수량 조건 | RfQ Response Line Qty | 0 | 공급업체 견적 응답 명세의 수량별 제안 내용을 저장한다. |
| [`c_salesregion`](c_salesregion.md) | 영업 지역 | Sales Region | 2 | 영업 활동의 담당 또는 적용 지역을 정의한다. |
| [`c_salesregion_trl`](c_salesregion_trl.md) | 영업 지역 번역 | Sales Region Trl | 2 | 영업 지역의 언어별 표시 내용을 저장한다. |
| [`c_salesstage`](c_salesstage.md) | 영업 단계 | Sales Stage | 0 | 영업 프로세스가 거쳐 가는 단계를 정의한다. |
| [`c_salesstage_trl`](c_salesstage_trl.md) | 영업 단계 번역 | Sales Stage Trl | 0 | 영업 프로세스 단계의 언어별 표시 내용을 저장한다. |
| [`c_servicelevel`](c_servicelevel.md) | 서비스 이행 수준 | Service Level | 0 | 상품과 수익 인식 계획별 서비스 제공 수준 및 청구된 수준을 관리한다. |
| [`c_servicelevelline`](c_servicelevelline.md) | 서비스 이행 수준 명세 | Service Level Line | 0 | 서비스 이행 수준에 속하는 일자별 제공 수준과 설명을 기록한다. |
| [`c_subacct`](c_subacct.md) | 보조 계정 | Sub Account | 0 | 계정 요소 값에 속하는 하위 보조 계정을 정의한다. |
| [`c_subscription`](c_subscription.md) | 상품 구독 | Subscription | 0 | 거래처가 갱신하여 이용하는 상품 구독을 관리한다. |
| [`c_subscription_delivery`](c_subscription_delivery.md) | 구독 제공 이력 | Subscription Delivery | 0 | 구독에 대한 선택적인 배송·제공 기록을 저장한다. |
| [`c_subscriptiontype`](c_subscriptiontype.md) | 구독 유형 | Subscription Type | 0 | 상품 구독의 유형을 정의한다. |
| [`c_task`](c_task.md) | 프로젝트 표준 작업 | Standard Task | 9 | 프로젝트 유형에서 사용할 표준 작업을 정의한다. |
| [`c_tax`](c_tax.md) | 세금 | Tax | 6 | 거래에서 적용하는 세금의 기준정보를 관리한다. |
| [`c_tax_acct`](c_tax_acct.md) | 세금 회계 계정 | C_Tax_Acct | 12 | 세금과 회계 스키마별 납부·채무·공제·미수·비용 계정을 지정한다. |
| [`c_tax_trl`](c_tax_trl.md) | 세금 번역 | Tax Trl | 6 | 세금의 언어별 표시 내용을 저장한다. |
| [`c_taxbase`](c_taxbase.md) | 과세 기준 | Tax Base | 0 | 세액 계산에 사용하는 기준값과 적용 비율을 코드·이름으로 정의한다. |
| [`c_taxcategory`](c_taxcategory.md) | 세금 분류 | Tax Category | 1 | 세금 적용을 구분하는 분류를 정의한다. |
| [`c_taxcategory_trl`](c_taxcategory_trl.md) | 세금 분류 번역 | Tax Category Trl | 1 | 세금 분류의 언어별 표시 내용을 저장한다. |
| [`c_taxdeclaration`](c_taxdeclaration.md) | 세금 신고 | Tax Declaration | 0 | 세무 당국 신고 내용을 묶고 관련 문서와 회계 기록 대사의 기준을 관리한다. |
| [`c_taxdeclarationacct`](c_taxdeclarationacct.md) | 세금 신고 회계 대사 | Tax Declaration Accounting | 0 | 세금 신고 관련 수익·비용·세금 회계 내역을 모아 문서와 대사하고 상세 보고의 근거로 사용한다. |
| [`c_taxdeclarationline`](c_taxdeclarationline.md) | 세금 신고 문서 명세 | Tax Declaration Line | 0 | 생성 처리로 수집된 신고 대상 문서를 저장한다. 특정 신고에 포함하지 않을 행은 제외할 수 있다. |
| [`c_taxdefinition`](c_taxdefinition.md) | 세금 적용 규칙 | Tax Definition | 0 | 거래처·상품·조직 유형·과세 범위·유효 기간 등의 조건에 따른 세금과 과세 기준을 정의한다. |
| [`c_taxgroup`](c_taxgroup.md) | 세금 그룹 | Tax Group | 0 | 관련 세금을 묶는 그룹 기준정보를 관리한다. |
| [`c_taxpostal`](c_taxpostal.md) | 우편번호별 세금 범위 | Tax ZIP | 0 | 세금 적용 지역을 우편번호 기준으로 관리한다. |
| [`c_taxprovider`](c_taxprovider.md) | 세금 계산 서비스 연결 | Tax Provider | 0 | 세금 계산 서비스의 회사·계정·이용 설정과 처리 순서를 구현 설정에 연결한다. |
| [`c_taxprovidercfg`](c_taxprovidercfg.md) | 세금 계산 구현 설정 | Tax Provider Configuration | 0 | 세금 계산 제공자의 구현 클래스와 서비스 URL 등 공통 설정을 정의한다. |
| [`c_taxtype`](c_taxtype.md) | 세금 유형 | Tax Type | 0 | 세금 규칙에서 참조하는 유형의 코드·이름·설명을 관리한다. |
| [`c_uom`](c_uom.md) | 측정 단위 | UOM | 15 | 상품과 거래 수량을 표현하는 측정 단위를 정의한다. |
| [`c_uom_conversion`](c_uom_conversion.md) | 단위 환산 | UOM Conversion | 1 | 측정 단위 사이의 수량 환산 관계를 관리한다. |
| [`c_uom_trl`](c_uom_trl.md) | 측정 단위 번역 | UOM Trl | 15 | 측정 단위의 언어별 표시 내용을 저장한다. |
| [`c_userremuneration`](c_userremuneration.md) | 직원별 보수 조정 | Employee Remuneration | 0 | 직원 임금이나 급여의 개별 보수 재정의 값을 관리한다. |
| [`c_validcombination`](c_validcombination.md) | 유효 계정 조합 | Combination | 157 | 회계에서 사용할 유효한 계정 및 분석 요소 조합을 관리한다. |
| [`c_withholding`](c_withholding.md) | 원천징수 유형 | Withholding | 0 | 거래에서 적용할 원천징수 유형을 정의한다. |
| [`c_withholding_acct`](c_withholding_acct.md) | 원천징수 회계 계정 | C_Withholding_Acct | 0 | 원천징수 유형과 회계 스키마별 원천징수 계정을 지정한다. |
| [`c_year`](c_year.md) | 회계 연도 | Year | 30 | 회계 달력에 속하는 연도를 관리한다. |
