# m — 제품·재고·출하/입고·원가

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 124개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`m_attribute`](m_attribute.md) | 제품 속성 | Attribute | 4 | 제품의 특성을 표현하는 속성을 정의한다. |
| [`m_attributeinstance`](m_attributeinstance.md) | 제품 속성 실값 | M_AttributeInstance | 5 | 속성 집합 인스턴스에 속한 개별 속성의 선택값·문자·숫자·날짜 값을 저장한다. |
| [`m_attributeinstanceline`](m_attributeinstanceline.md) | 속성 다중 선택값 | Attribute Instance Values | 0 | 속성 인스턴스에서 선택한 속성값들을 행 단위로 저장한다. |
| [`m_attributesearch`](m_attributesearch.md) | 공통 검색 속성 | Attribute Search | 1 | 제품 속성을 이용한 공통 검색 조건을 정의한다. |
| [`m_attributeset`](m_attributeset.md) | 제품 속성 집합 | Attribute Set | 4 | 제품에 함께 적용할 속성들의 묶음을 정의한다. |
| [`m_attributesetexclude`](m_attributesetexclude.md) | 속성 집합 입력 제외 | Exclude Attribute Set | 0 | 특정 범위에서 속성 집합 입력을 제외하는 설정을 저장한다. |
| [`m_attributesetinstance`](m_attributesetinstance.md) | 제품 속성 집합 인스턴스 | Attribute Set Instance | 4 | 제품 속성 집합이 실제 적용된 개별 인스턴스를 식별한다. |
| [`m_attributeuse`](m_attributeuse.md) | 속성 집합 구성 | M_AttributeUse | 5 | 속성 집합에 포함할 속성과 표시 순서·기본값을 연결한다. |
| [`m_attributevalue`](m_attributevalue.md) | 제품 속성 선택값 | Attribute Value | 9 | 제품 속성에서 선택할 수 있는 값을 정의한다. |
| [`m_bom`](m_bom.md) | 자재명세서 | BOM | 1 | 제품을 구성하는 자재명세서(BOM)를 정의한다. |
| [`m_bomalternative`](m_bomalternative.md) | BOM 대체 그룹 | Alternative Group | 1 | 제품 BOM에서 대체 가능한 구성품의 그룹을 정의한다. |
| [`m_bomproduct`](m_bomproduct.md) | BOM 구성품 | BOM Component | 0 | 자재명세서에 포함되는 제품 구성품을 저장한다. |
| [`m_bp_price`](m_bp_price.md) | 거래처별 제품 가격 | Business Partner Price | 0 | 일반 가격표보다 우선 적용하는 거래처별 가격을 저장한다. |
| [`m_changenotice`](m_changenotice.md) | 변경 통지 | Change Notice | 1 | 제품 변경과 관련한 통지 내용 및 승인·처리 상태를 저장한다. |
| [`m_changerequest`](m_changerequest.md) | 변경 요청 | Change Request | 0 | BOM과 관련된 변경 요청 내용 및 연계 변경 통지·승인 상태를 저장한다. |
| [`m_commodityshipment`](m_commodityshipment.md) | 출하 상품 통관 정보 | Commodity Shipment | 0 | 제품의 수출 허가 번호·품목분류 코드·제조국을 저장한다. |
| [`m_cost`](m_cost.md) | 제품 원가 | Product Cost | 267 | 제품·원가 유형·회계 스키마·원가 요소별 현재 원가와 수량 및 누적 금액을 저장한다. |
| [`m_costdetail`](m_costdetail.md) | 원가 상세 | Cost Detail | 0 | 제품 원가 계산에 사용하는 상세 원가 정보를 저장한다. |
| [`m_costelement`](m_costelement.md) | 원가 요소 | Cost Element | 9 | 원가를 구성하는 요소와 요소 유형·원가 계산 방법을 정의한다. |
| [`m_costhistory`](m_costhistory.md) | 원가 변경 이력 | Cost History | 0 | 제품 원가 테이블의 변동 이력을 기록한다. |
| [`m_costqueue`](m_costqueue.md) | 선입·후입 원가 대기열 | Cost Queue | 0 | FIFO 또는 LIFO 방식의 원가 계산에 사용하는 원가 대기열을 관리한다. |
| [`m_costtype`](m_costtype.md) | 원가 유형 | Cost Type | 1 | 제품 원가를 구분하여 관리하기 위한 원가 유형을 정의한다. |
| [`m_demand`](m_demand.md) | 자재 수요 | Demand | 0 | 자재 수요 문서의 기본 정보를 저장한다. |
| [`m_demanddetail`](m_demanddetail.md) | 자재 수요 원천 상세 | Demand Detail | 0 | 자재 수요행의 근거가 된 원천 내역을 저장한다. |
| [`m_demandline`](m_demandline.md) | 자재 수요행 | Demand Line | 0 | 자재 수요 문서의 개별 행을 저장한다. |
| [`m_discountschema`](m_discountschema.md) | 할인 규칙 | Discount Schema | 3 | 거래 할인율을 계산하는 할인 체계를 정의한다. |
| [`m_discountschemabreak`](m_discountschemabreak.md) | 구간별 할인 | Discount Schema Break | 1 | 할인 체계의 구간별 거래 할인 조건을 저장한다. |
| [`m_discountschemaline`](m_discountschemaline.md) | 가격표 할인 규칙행 | Discount Price List | 11 | 가격표에 적용하는 거래 할인 체계의 개별 행을 저장한다. |
| [`m_distributionlist`](m_distributionlist.md) | 제품 배분 대상 목록 | Distribution List | 1 | 제품을 배분할 거래처들의 목록을 정의한다. |
| [`m_distributionlistline`](m_distributionlistline.md) | 제품 배분 대상행 | Distribution List Line | 3 | 배분 목록에 속한 거래처와 수량 또는 배분 비율을 저장한다. |
| [`m_distributionrun`](m_distributionrun.md) | 제품 배분 실행 | Distribution Run | 1 | 선택한 거래처들에 제품을 배분하는 주문 생성 실행을 정의한다. |
| [`m_distributionrunline`](m_distributionrunline.md) | 제품 배분 실행행 | Distribution Run Line | 1 | 배분 실행에 사용할 대상 목록·제품·수량을 지정한다. |
| [`m_edi`](m_edi.md) | 전자문서 교환 거래 | EDI Transaction | 0 | 제품 수량·납기·가격에 대한 EDI 요청과 응답 및 송수신 상태를 저장한다. |
| [`m_edi_info`](m_edi_info.md) | 전자문서 교환 로그 | EDI Log | 0 | 개별 EDI 거래에 연결된 추가 로그 정보를 저장한다. |
| [`m_forecast`](m_forecast.md) | 자재 예측 | Forecast | 4 | 자재에 대한 예측 문서의 기본 정보를 저장한다. |
| [`m_forecastline`](m_forecastline.md) | 자재 예측행 | Forecast Line | 50 | 자재 예측 문서의 개별 행을 저장한다. |
| [`m_freight`](m_freight.md) | 운임 요율 | Freight | 3 | 제품 운송에 적용하는 운임 요율을 정의한다. |
| [`m_freightcategory`](m_freightcategory.md) | 운임 분류 | Freight Category | 2 | 운임을 구분하는 분류를 정의한다. |
| [`m_inout`](m_inout.md) | 출하·입고 문서 | Shipment/Receipt | 9 | 제품의 고객 출하 또는 공급업체 입고를 기록하는 자재 이동 문서의 헤더다. 출하와 입고를 모두 포함하므로 조회 시 거래 방향을 구분해야 한다. |
| [`m_inoutconfirm`](m_inoutconfirm.md) | 출하·입고 확인 | Ship/Receipt Confirmation | 1 | 출하 또는 입고 문서에 대한 확인 정보를 저장한다. |
| [`m_inoutline`](m_inoutline.md) | 출하·입고행 | Shipment/Receipt Line | 27 | 출하 또는 입고 문서의 제품별 상세 행을 저장한다. |
| [`m_inoutlineconfirm`](m_inoutlineconfirm.md) | 출하·입고 확인행 | Ship/Receipt Confirmation Line | 1 | 출하 또는 입고 확인 문서의 개별 자재 확인행을 저장한다. |
| [`m_inoutlinema`](m_inoutlinema.md) | 출하·입고행 속성 배분 | M_InOutLineMA | 0 | 출하·입고행의 이동 수량을 속성 집합 인스턴스와 자재 정책일별로 나누어 저장한다. |
| [`m_inventory`](m_inventory.md) | 실사 재고 문서 | Phys.Inventory | 3 | 실물 재고 실사를 위한 문서 및 매개변수를 저장한다. |
| [`m_inventoryline`](m_inventoryline.md) | 실사 재고행 | Phys.Inventory Line | 1 | 재고 실사 문서에 속하는 개별 품목 행을 저장한다. |
| [`m_inventorylinema`](m_inventorylinema.md) | 실사 재고행 속성 배분 | M_InventoryLineMA | 0 | 실사 재고행의 수량을 속성 집합 인스턴스와 자재 정책일별로 배분한다. |
| [`m_locator`](m_locator.md) | 창고 보관 위치 | Locator | 11 | 창고 안에서 재고를 보관하는 위치를 정의한다. |
| [`m_locatortype`](m_locatortype.md) | 보관 위치 유형 | Locator Type | 0 | 보관 위치의 유형과 보충·예약·출하에 사용할 수 있는지 여부를 정의한다. |
| [`m_lot`](m_lot.md) | 제품 로트 | Lot | 0 | 제품의 로트 정보를 정의한다. |
| [`m_lotctl`](m_lotctl.md) | 로트 번호 관리 | Lot Control | 1 | 제품 로트의 관리 기준을 정의한다. |
| [`m_lotctlexclude`](m_lotctlexclude.md) | 로트 생성 제외 | Exclude Lot | 0 | 속성 집합에서 로트 생성을 제외하는 설정을 저장한다. |
| [`m_matchinv`](m_matchinv.md) | 입출고·송장 대사 | Match Invoice | 18 | 출하·입고 내역과 송장 내역의 대응 관계를 저장한다. |
| [`m_matchpo`](m_matchpo.md) | 구매 주문 대사 | Match PO | 37 | 구매 주문을 출하·입고 및 송장 내역과 대응시킨다. |
| [`m_movement`](m_movement.md) | 재고 이동 문서 | Inventory Move | 1 | 보관 위치 사이의 재고 이동을 기록하는 문서다. |
| [`m_movementconfirm`](m_movementconfirm.md) | 재고 이동 확인 | Move Confirm | 0 | 재고 이동 문서의 확인 정보를 저장한다. |
| [`m_movementline`](m_movementline.md) | 재고 이동행 | Move Line | 1 | 재고 이동 문서의 개별 이동 내역을 저장한다. |
| [`m_movementlineconfirm`](m_movementlineconfirm.md) | 재고 이동 확인행 | Move Line Confirm | 0 | 재고 이동행의 확인 내역을 저장한다. |
| [`m_movementlinema`](m_movementlinema.md) | 재고 이동행 속성 배분 | M_MovementLineMA | 0 | 재고 이동행의 수량을 속성 집합 인스턴스와 자재 정책일별로 나누어 저장한다. |
| [`m_operationresource`](m_operationresource.md) | 제품 공정 자원 | Operation Resource | 0 | 제품 공정에 필요한 자원을 연결한다. |
| [`m_package`](m_package.md) | 출하 포장 | Package | 1 | 출하에 사용되는 포장 단위 정보를 저장한다. |
| [`m_packageline`](m_packageline.md) | 출하 포장 내용행 | Package Line | 1 | 포장에 포함된 상세 내용물을 저장한다. |
| [`m_packagemps`](m_packagemps.md) | 다중 포장 세부 정보 | Package MPS | 0 | 포장별 치수·중량과 개별 및 대표 추적 번호를 저장한다. |
| [`m_parttype`](m_parttype.md) | 제조 부품 유형 | Part Type | 0 | 제조에 사용하는 부품의 유형을 정의한다. |
| [`m_perpetualinv`](m_perpetualinv.md) | 순환 실사 규칙 | Perpetual Inventory | 0 | 재고 실사 문서를 생성하는 규칙을 정의한다. |
| [`m_pricelist`](m_pricelist.md) | 가격표 | Price List | 4 | 제품 가격을 관리하는 가격표를 식별한다. |
| [`m_pricelist_trl`](m_pricelist_trl.md) | 가격표 번역 | Price List | 4 | 가격표의 언어별 번역 정보를 저장한다. |
| [`m_pricelist_version`](m_pricelist_version.md) | 가격표 버전 | Price List Version | 6 | 하나의 가격표에 속한 개별 버전을 식별한다. |
| [`m_pricelist_version_trl`](m_pricelist_version_trl.md) | 가격표 버전 번역 | Price List Version Trl | 6 | 가격표 버전의 언어별 번역 정보를 저장한다. |
| [`m_product`](m_product.md) | 제품·서비스 | Product | 255 | 제품·서비스·품목의 공통 기본 정보를 관리하는 마스터다. |
| [`m_product_acct`](m_product_acct.md) | 제품별 회계 계정 | Product Acct | 110 | 제품과 회계 스키마별 매출·비용·재고·매출원가 및 제조 관련 계정을 연결한다. |
| [`m_product_bom_old`](m_product_bom_old.md) | 구형 제품 BOM | — | 20 | 제품과 하위 구성품, 구성 수량 및 BOM 유형을 저장하는 구형 명칭의 테이블이다. 현재 기능에서의 사용 여부는 확인이 필요하다. |
| [`m_product_category`](m_product_category.md) | 제품 분류 | Product Category | 14 | 제품을 묶어 관리하는 분류를 정의한다. |
| [`m_product_category_acct`](m_product_category_acct.md) | 제품 분류별 회계 설정 | Product Category Acct | 28 | 제품 분류와 회계 스키마별 기본 계정·원가 계산 방법·원가 수준을 정의한다. |
| [`m_product_category_trl`](m_product_category_trl.md) | 제품 분류 번역 | Product Category Trl | 14 | 제품 분류의 언어별 번역 정보를 저장한다. |
| [`m_product_po`](m_product_po.md) | 제품 구매 조건 | Product Purchasing | 29 | 제품과 공급업체별 구매 단가·거래 통화·공급업체 품번·최소 주문량·납기를 저장한다. |
| [`m_product_qualitytest`](m_product_qualitytest.md) | 제품별 품질 시험 | Product Quality Test | 0 | 제품에 적용할 품질 시험과 기대 결과를 연결한다. |
| [`m_product_trl`](m_product_trl.md) | 제품·서비스 번역 | Product Trl | 55 | 제품·서비스·품목의 언어별 번역 정보를 저장한다. |
| [`m_productdownload`](m_productdownload.md) | 제품 다운로드 | Product Download | 1 | 제품에 연결된 다운로드 정보를 관리한다. |
| [`m_production`](m_production.md) | 생산 문서 | Production | 0 | 제품 생산 계획을 나타내는 생산 문서의 기본 정보를 저장한다. |
| [`m_productionline`](m_productionline.md) | 생산행 | Production Line | 0 | 생산 문서에서 발생하는 개별 자재 내역을 저장한다. |
| [`m_productionlinema`](m_productionlinema.md) | 생산행 속성 배분 | Production Line MA | 0 | 생산행의 이동 수량을 속성 집합 인스턴스와 자재 정책일별로 배분한다. |
| [`m_productionplan`](m_productionplan.md) | 생산 계획 | Production Plan | 0 | 제품을 어떤 방식으로 생산할지에 대한 계획을 저장한다. |
| [`m_productoperation`](m_productoperation.md) | 제품 공정 | Product Operation | 0 | 제품에 필요한 공정과 준비·단위 실행·정리 시간을 정의한다. |
| [`m_productprice`](m_productprice.md) | 제품 가격 | Product Price | 114 | 가격표 버전별 제품의 정가·표준가·한도가를 저장한다. |
| [`m_productpricevendorbreak`](m_productpricevendorbreak.md) | 공급업체별 수량 구간 가격 | Product Price Break | 0 | 공급업체·제품·가격표 버전과 수량 구간값별 정가·표준가·한도가를 저장한다. |
| [`m_promotion`](m_promotion.md) | 판매 촉진 설정 | Promotion | 200 | 판매 촉진 행사에 적용할 기본 설정을 정의한다. |
| [`m_promotiondistribution`](m_promotiondistribution.md) | 판매 촉진 수량 배분 | Promotion Distribution | 0 | 혜택 계산을 위해 주문행의 품목을 여러 계산 묶음으로 배분하는 설정을 저장한다. |
| [`m_promotiongroup`](m_promotiongroup.md) | 판매 촉진 제품 그룹 | Promotion Group | 200 | 판매 촉진 설정에 함께 사용하는 제품 그룹을 정의한다. |
| [`m_promotiongroupline`](m_promotiongroupline.md) | 판매 촉진 그룹 구성행 | Promotion Group Line | 600 | 판매 촉진 제품 그룹에 포함된 개별 품목을 저장한다. |
| [`m_promotionline`](m_promotionline.md) | 판매 촉진 조건행 | Promotion Line | 200 | 판매 촉진을 구성하는 제품 조합을 행 단위로 정의한다. |
| [`m_promotionprecondition`](m_promotionprecondition.md) | 판매 촉진 사전 조건 | Promotion Pre Condition | 0 | 주문에 판매 촉진을 적용하기 전에 충족해야 하는 조건을 정의한다. |
| [`m_promotionreward`](m_promotionreward.md) | 판매 촉진 혜택 | Promotion Reward | 0 | 판매 촉진 조건을 충족할 때 제공할 혜택을 정의한다. |
| [`m_qualitytest`](m_qualitytest.md) | 품질 시험 | Quality Test | 0 | 품질 시험 항목의 이름과 설명을 정의한다. |
| [`m_qualitytestresult`](m_qualitytestresult.md) | 품질 시험 결과 | Quality Test Result | 0 | 제품 속성 집합 인스턴스별 시험 결과와 합격 여부를 저장한다. |
| [`m_relatedproduct`](m_relatedproduct.md) | 관련 제품 관계 | Product Related | 1 | 제품과 관련 제품을 관계 유형과 함께 연결한다. |
| [`m_replenish`](m_replenish.md) | 제품 보충 기준 | M_Replenish | 19 | 제품·창고별 보충 유형, 최소·최대 수준과 공급 창고 등을 정의한다. |
| [`m_requisition`](m_requisition.md) | 자재 요청서 | Requisition | 1 | 자재 조달 요청 문서의 기본 정보를 저장한다. |
| [`m_requisitionline`](m_requisitionline.md) | 자재 요청행 | Requisition Line | 1 | 자재 요청서의 개별 요청 내역을 저장한다. |
| [`m_rma`](m_rma.md) | 반품 승인 문서 | RMA | 1 | 반품을 승인하고 관리하는 문서다. 고객 반품과 공급업체 반품은 거래 방향에 따라 구분한다. |
| [`m_rmaline`](m_rmaline.md) | 반품 승인행 | RMA Line | 1 | 반품 승인 문서의 개별 반품 대상 내역을 저장한다. |
| [`m_rmatax`](m_rmatax.md) | 반품 승인 세금 | RMA Tax | 0 | 반품 승인 문서에 적용되는 세금 내역을 저장한다. |
| [`m_rmatype`](m_rmatype.md) | 반품 승인 유형 | RMA Type | 1 | 반품 승인 문서의 유형을 정의한다. |
| [`m_sernoctl`](m_sernoctl.md) | 일련번호 관리 | Serial No Control | 1 | 제품 일련번호의 관리 기준을 정의한다. |
| [`m_sernoctlexclude`](m_sernoctlexclude.md) | 일련번호 생성 제외 | Exclude Ser No | 0 | 속성 집합에서 일련번호 생성을 제외하는 설정을 저장한다. |
| [`m_shipper`](m_shipper.md) | 배송업체·배송 수단 | Shipper | 3 | 제품을 배송하는 업체 또는 배송 방식을 정의한다. |
| [`m_shippercfg`](m_shippercfg.md) | 배송업체 구성 | Shipper Configuration | 1 | 제품 배송 방식에 대한 구성 정의를 저장한다. |
| [`m_shipperlabels`](m_shipperlabels.md) | 배송업체 라벨 | Shipper Labels | 0 | 배송업체가 사용하는 라벨 구성과 기본값·인쇄 방식을 연결한다. |
| [`m_shipperlabelscfg`](m_shipperlabelscfg.md) | 배송 라벨 구성 | Shipper Labels Configuration | 0 | 배송 라벨의 코드·크기·인쇄 방식 등 구성 정보를 정의한다. |
| [`m_shipperpackaging`](m_shipperpackaging.md) | 배송업체 포장 | Shipper Packaging | 0 | 배송업체가 사용하는 포장 구성과 중량·기본값을 연결한다. |
| [`m_shipperpackagingcfg`](m_shipperpackagingcfg.md) | 배송 포장 구성 | Shipper Packaging Configuration | 0 | 배송 포장 유형의 코드·중량과 기본 설정을 정의한다. |
| [`m_shipperpickuptypes`](m_shipperpickuptypes.md) | 배송업체 집하 유형 | Shipper Pickup Types | 0 | 배송업체가 사용하는 집하 유형과 기본값을 연결한다. |
| [`m_shipperpickuptypescfg`](m_shipperpickuptypescfg.md) | 집하 유형 구성 | Shipper Pickup Types Configuration | 0 | 배송업체 구성에 속하는 집하 유형의 코드와 설명을 정의한다. |
| [`m_shippingprocessor`](m_shippingprocessor.md) | 배송 처리기 | Shipping Processor | 1 | 배송 처리기 구성과 서비스 연결 인증 설정을 연결한다. |
| [`m_shippingprocessorcfg`](m_shippingprocessorcfg.md) | 배송 처리기 구성 | Shipping Processor Configuration | 1 | 배송 서비스 접속 주소·프록시 및 처리 구현 클래스의 구성을 정의한다. |
| [`m_shippingtransaction`](m_shippingtransaction.md) | 배송 거래 | Shipping Transaction | 0 | 배송 서비스와 처리하는 배송 거래 정보를 저장한다. |
| [`m_shippingtransactionline`](m_shippingtransactionline.md) | 배송 거래행 | Shipping Transaction Line | 0 | 배송 거래에 속한 개별 상세 행을 저장한다. |
| [`m_storageonhand`](m_storageonhand.md) | 현재고 | M_StorageOnHand | 20 | 제품·보관 위치·속성 집합 인스턴스·자재 정책일별 현재고 수량을 저장한다. |
| [`m_storagereservation`](m_storagereservation.md) | 재고 예약·주문 수량 | M_StorageReservation | 2 | 제품·창고·속성 집합 인스턴스와 거래 방향별 수량을 저장한다. 판매 예약과 구매 주문 수량을 구분하여 해석해야 한다. |
| [`m_storagereservationlog`](m_storagereservationlog.md) | 재고 예약 변경 로그 | Storage Reservation Log | 0 | 재고 예약 수량이 바뀔 때마다 변경 전후 수량과 증감량을 기록한다. |
| [`m_substitute`](m_substitute.md) | 대체 제품 | M_Substitute | 0 | 제품과 대신 사용할 제품을 연결한다. |
| [`m_transaction`](m_transaction.md) | 재고 수불 거래 | Inventory Transaction | 28 | 입출고·이동·실사·생산 등에서 발생한 제품 수량 증감을 보관 위치 및 속성 인스턴스와 함께 기록한다. |
| [`m_transactionallocation`](m_transactionallocation.md) | 재고 거래 배분 | M_TransactionAllocation | 0 | 입고측과 출고측 재고 거래 및 관련 문서행을 배분 수량·전략과 함께 연결한다. |
| [`m_warehouse`](m_warehouse.md) | 창고·서비스 지점 | Warehouse | 11 | 재고를 보관하는 창고와 서비스 제공 지점을 정의한다. |
| [`m_warehouse_acct`](m_warehouse_acct.md) | 창고별 회계 계정 | M_Warehouse_Acct | 22 | 창고와 회계 스키마별 재고·실사 조정·차이·재평가 계정을 연결한다. |
