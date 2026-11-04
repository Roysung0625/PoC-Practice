# a — 자산·감가상각

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 42개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`a_asset`](a_asset.md) | 자산 | Asset | 0 | 내부에서 사용하거나 고객에게 제공한 자산을 관리한다. |
| [`a_asset_acct`](a_asset_acct.md) | 자산별 회계 설정 | A_Asset_Acct_ID | 0 | 개별 고정자산의 감가상각 계정과 계산 방법을 설정한다. |
| [`a_asset_addition`](a_asset_addition.md) | 자산 취득·증가 전표 | Asset Addition | 0 | 청구·입고 등의 원천 문서와 연결하여 자산 취득 또는 가치 증가 금액과 회계 처리 상태를 기록한다. |
| [`a_asset_change`](a_asset_change.md) | 자산 변경 기록 | A_Asset_Change_ID | 0 | 자산의 변경 유형·일자와 금액·내용연수·회계 설정 등 변경 관련 정보를 기록한다. |
| [`a_asset_change_amt`](a_asset_change_amt.md) | 자산 변경 금액 | — | 0 | 자산 변경 건에 대해 회계 스키마별 취득가액·시장가치·장부가액·감가상각누계액을 기록한다. |
| [`a_asset_class`](a_asset_class.md) | 자산 분류 | Asset class | 0 | 자산 분류 코드와 명칭, 내용연수 범위 등 분류 기준을 관리한다. |
| [`a_asset_delivery`](a_asset_delivery.md) | 자산 전달 이력 | Asset Delivery | 0 | 자산을 전달한 내역을 관리한다. |
| [`a_asset_disposed`](a_asset_disposed.md) | 자산 처분 전표 | Asset Disposed | 0 | 자산의 처분일·방법·사유와 처분대금·원가·감가상각 및 전표 처리 상태를 기록한다. |
| [`a_asset_group`](a_asset_group.md) | 자산 그룹 | Asset Group | 9 | 공통 기준으로 자산을 묶는 그룹을 정의한다. |
| [`a_asset_group_acct`](a_asset_group_acct.md) | 자산 그룹 회계 설정 | Asset Group Accounting | 6 | 자산 그룹에 적용할 감가상각 계정과 계산 방법을 설정한다. |
| [`a_asset_group_trl`](a_asset_group_trl.md) | 자산 그룹 번역 | Asset Group Trl | 9 | 자산 그룹 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`a_asset_info_fin`](a_asset_info_fin.md) | 자산 금융 정보 | Asset Info Financial ID | 0 | 개별 고정자산의 금융 관련 설정과 정보를 관리한다. |
| [`a_asset_info_ins`](a_asset_info_ins.md) | 자산 보험 정보 | A_Asset_Info_Ins_ID | 0 | 개별 고정자산의 보험 관련 설정과 정보를 관리한다. |
| [`a_asset_info_lic`](a_asset_info_lic.md) | 자산 라이선스 정보 | A_Asset_Info_Lic_ID | 0 | 개별 고정자산의 라이선스 관련 설정과 정보를 관리한다. |
| [`a_asset_info_oth`](a_asset_info_oth.md) | 자산 기타 정보 | A_Asset_Info_Oth_ID | 0 | 개별 고정자산에 대한 사용자 정의 기타 정보를 관리한다. |
| [`a_asset_info_tax`](a_asset_info_tax.md) | 자산 세무 정보 | Asset Info Tax | 0 | 개별 고정자산의 세무 관련 설정과 정보를 관리한다. |
| [`a_asset_product`](a_asset_product.md) | 자산 구성 제품 | Asset Product | 0 | 자산과 제품·속성 인스턴스·보관 위치를 연결하고 해당 수량을 기록한다. |
| [`a_asset_retirement`](a_asset_retirement.md) | 내부 자산 사용 종료 | Asset Retirement | 0 | 내부에서 더 이상 사용하지 않는 자산의 사용 종료를 관리한다. |
| [`a_asset_reval`](a_asset_reval.md) | 자산 재평가 전표 | Asset Revaluation | 0 | 자산 원가와 감가상각누계액의 재평가 변동 금액 및 회계 처리 상태를 기록한다. |
| [`a_asset_reval_entry`](a_asset_reval_entry.md) | 자산 재평가 처리 항목 | Asset Reval. Entry | 0 | 자산 재평가를 처리하는 데 필요한 정보를 관리한다. |
| [`a_asset_reval_index`](a_asset_reval_index.md) | 자산 재평가 지수 | Asset Reval Index | 0 | 자산 재평가에 사용할 지수와 계수를 관리한다. |
| [`a_asset_split`](a_asset_split.md) | 자산 분할 | Asset Split | 0 | 자산을 분할하는 데 필요한 처리 정보를 관리한다. |
| [`a_asset_spread`](a_asset_spread.md) | 기간별 감가상각 배분 | A_Asset_Spread_ID | 2 | 사용자가 정한 기간별 감가상각 배분을 관리한다. |
| [`a_asset_transfer`](a_asset_transfer.md) | 자산 이동 | A_Asset_Transfer_ID | 0 | 자산 이동과 이에 따른 회계 항목 생성에 필요한 정보를 관리한다. |
| [`a_asset_type`](a_asset_type.md) | 자산 유형 | Asset Type | 0 | 자산 유형별 소유·점유 여부와 감가상각 대상 여부를 정의한다. |
| [`a_asset_use`](a_asset_use.md) | 자산 사용 실적 | A_Asset_Use_ID | 0 | 자산별 사용일과 사용량을 기록한다. |
| [`a_depreciation`](a_depreciation.md) | 감가상각 함수 | Depreciation | 11 | 시스템에서 사용할 수 있는 감가상각 함수를 관리한다. |
| [`a_depreciation_build`](a_depreciation_build.md) | 감가상각 예상 계산 | Build Depreciation | 0 | 총계정원장 전기 전에 감가상각 예상치를 생성·처리하는 데 필요한 정보를 관리한다. |
| [`a_depreciation_convention`](a_depreciation_convention.md) | 감가상각 적용 관례 | Depreciation Convention | 6 | 감가상각 계산에서 사용할 관례 유형을 관리한다. |
| [`a_depreciation_entry`](a_depreciation_entry.md) | 감가상각 전표 처리 | Depreciation Entry | 0 | 감가상각 회계 항목을 처리하는 데 필요한 정보를 관리한다. |
| [`a_depreciation_exp`](a_depreciation_exp.md) | 감가상각 작업 항목 | A_Depreciation_Exp_ID | 0 | 고정자산 관련 회계 항목과 예상치를 생성하는 작업 데이터를 보관한다. |
| [`a_depreciation_forecast`](a_depreciation_forecast.md) | 감가상각 예측 실행 | Depreciation Forecast | 0 | 시작·종료 자산 범위와 문서일·전기 유형을 지정하여 감가상각 예측 처리 상태를 관리한다. |
| [`a_depreciation_method`](a_depreciation_method.md) | 감가상각 조정 방법 | Depreciation Method | 3 | 고정자산 잔액의 감가상각 조정을 처리하는 방법을 관리한다. |
| [`a_depreciation_table_detail`](a_depreciation_table_detail.md) | 감가상각률 표 상세 | Depreciation Table Detail | 2,579 | 감가상각률 표의 코드와 기간별 적용 비율을 기록한다. |
| [`a_depreciation_table_header`](a_depreciation_table_header.md) | 감가상각률 표 정의 | A_Depreciation_Table_Header_ID | 122 | 감가상각률 표의 코드·기간·비율 유형 등 공통 정보를 정의한다. |
| [`a_depreciation_workfile`](a_depreciation_workfile.md) | 자산 원가·상각 잔액 | A_Depreciation_Workfile_ID | 0 | 개별 고정자산의 원가와 감가상각 잔액을 관리한다. |
| [`a_fundingmode`](a_fundingmode.md) | 자산 자금조달 방식 | Asset Funding Mode | 0 | 자산 자금조달 방식을 코드와 명칭으로 관리한다. |
| [`a_fundingmode_acct`](a_fundingmode_acct.md) | 자금조달 방식별 계정 | Asset Funding Mode Accounting | 0 | 자산 자금조달 방식과 회계 스키마별 계정을 연결한다. |
| [`a_registration`](a_registration.md) | 사용자 자산 등록 | Registration | 0 | 사용자의 자산 등록 정보를 관리한다. |
| [`a_registrationattribute`](a_registrationattribute.md) | 자산 등록 속성 | Registration Attribute | 0 | 자산 등록 시 기록할 속성을 정의한다. |
| [`a_registrationproduct`](a_registrationproduct.md) | 제품별 등록 속성 | Registration Product | 0 | 제품과 자산 등록 속성을 연결한다. |
| [`a_registrationvalue`](a_registrationvalue.md) | 자산 등록 속성값 | A_RegistrationValue | 0 | 자산 등록 건에 지정된 등록 속성의 값을 기록한다. |
