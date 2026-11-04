# 전체 테이블 일람

[시작 안내](README.md) · [업무별 찾기](BUSINESS_GUIDE.md) · [외래키 안내](RELATIONSHIPS.md)

`poc_idempiere.adempiere`의 물리 테이블 912개입니다. 뷰 161개는 제외했습니다. 확인 시점: 2026-11-03T23:29:01+09:00.

한국어 논리명·개요는 원본 사전 또는 구조를 해석한 문서용 설명입니다. 테이블별 문서의 근거 구분을 확인하세요. 행 수는 전체 테넌트 기준이며, 0행도 구조 탐색에 필요하므로 포함합니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`a_asset`](a/a_asset.md) | 자산 | Asset | 0 | 내부에서 사용하거나 고객에게 제공한 자산을 관리한다. |
| [`a_asset_acct`](a/a_asset_acct.md) | 자산별 회계 설정 | A_Asset_Acct_ID | 0 | 개별 고정자산의 감가상각 계정과 계산 방법을 설정한다. |
| [`a_asset_addition`](a/a_asset_addition.md) | 자산 취득·증가 전표 | Asset Addition | 0 | 청구·입고 등의 원천 문서와 연결하여 자산 취득 또는 가치 증가 금액과 회계 처리 상태를 기록한다. |
| [`a_asset_change`](a/a_asset_change.md) | 자산 변경 기록 | A_Asset_Change_ID | 0 | 자산의 변경 유형·일자와 금액·내용연수·회계 설정 등 변경 관련 정보를 기록한다. |
| [`a_asset_change_amt`](a/a_asset_change_amt.md) | 자산 변경 금액 | — | 0 | 자산 변경 건에 대해 회계 스키마별 취득가액·시장가치·장부가액·감가상각누계액을 기록한다. |
| [`a_asset_class`](a/a_asset_class.md) | 자산 분류 | Asset class | 0 | 자산 분류 코드와 명칭, 내용연수 범위 등 분류 기준을 관리한다. |
| [`a_asset_delivery`](a/a_asset_delivery.md) | 자산 전달 이력 | Asset Delivery | 0 | 자산을 전달한 내역을 관리한다. |
| [`a_asset_disposed`](a/a_asset_disposed.md) | 자산 처분 전표 | Asset Disposed | 0 | 자산의 처분일·방법·사유와 처분대금·원가·감가상각 및 전표 처리 상태를 기록한다. |
| [`a_asset_group`](a/a_asset_group.md) | 자산 그룹 | Asset Group | 9 | 공통 기준으로 자산을 묶는 그룹을 정의한다. |
| [`a_asset_group_acct`](a/a_asset_group_acct.md) | 자산 그룹 회계 설정 | Asset Group Accounting | 6 | 자산 그룹에 적용할 감가상각 계정과 계산 방법을 설정한다. |
| [`a_asset_group_trl`](a/a_asset_group_trl.md) | 자산 그룹 번역 | Asset Group Trl | 9 | 자산 그룹 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`a_asset_info_fin`](a/a_asset_info_fin.md) | 자산 금융 정보 | Asset Info Financial ID | 0 | 개별 고정자산의 금융 관련 설정과 정보를 관리한다. |
| [`a_asset_info_ins`](a/a_asset_info_ins.md) | 자산 보험 정보 | A_Asset_Info_Ins_ID | 0 | 개별 고정자산의 보험 관련 설정과 정보를 관리한다. |
| [`a_asset_info_lic`](a/a_asset_info_lic.md) | 자산 라이선스 정보 | A_Asset_Info_Lic_ID | 0 | 개별 고정자산의 라이선스 관련 설정과 정보를 관리한다. |
| [`a_asset_info_oth`](a/a_asset_info_oth.md) | 자산 기타 정보 | A_Asset_Info_Oth_ID | 0 | 개별 고정자산에 대한 사용자 정의 기타 정보를 관리한다. |
| [`a_asset_info_tax`](a/a_asset_info_tax.md) | 자산 세무 정보 | Asset Info Tax | 0 | 개별 고정자산의 세무 관련 설정과 정보를 관리한다. |
| [`a_asset_product`](a/a_asset_product.md) | 자산 구성 제품 | Asset Product | 0 | 자산과 제품·속성 인스턴스·보관 위치를 연결하고 해당 수량을 기록한다. |
| [`a_asset_retirement`](a/a_asset_retirement.md) | 내부 자산 사용 종료 | Asset Retirement | 0 | 내부에서 더 이상 사용하지 않는 자산의 사용 종료를 관리한다. |
| [`a_asset_reval`](a/a_asset_reval.md) | 자산 재평가 전표 | Asset Revaluation | 0 | 자산 원가와 감가상각누계액의 재평가 변동 금액 및 회계 처리 상태를 기록한다. |
| [`a_asset_reval_entry`](a/a_asset_reval_entry.md) | 자산 재평가 처리 항목 | Asset Reval. Entry | 0 | 자산 재평가를 처리하는 데 필요한 정보를 관리한다. |
| [`a_asset_reval_index`](a/a_asset_reval_index.md) | 자산 재평가 지수 | Asset Reval Index | 0 | 자산 재평가에 사용할 지수와 계수를 관리한다. |
| [`a_asset_split`](a/a_asset_split.md) | 자산 분할 | Asset Split | 0 | 자산을 분할하는 데 필요한 처리 정보를 관리한다. |
| [`a_asset_spread`](a/a_asset_spread.md) | 기간별 감가상각 배분 | A_Asset_Spread_ID | 2 | 사용자가 정한 기간별 감가상각 배분을 관리한다. |
| [`a_asset_transfer`](a/a_asset_transfer.md) | 자산 이동 | A_Asset_Transfer_ID | 0 | 자산 이동과 이에 따른 회계 항목 생성에 필요한 정보를 관리한다. |
| [`a_asset_type`](a/a_asset_type.md) | 자산 유형 | Asset Type | 0 | 자산 유형별 소유·점유 여부와 감가상각 대상 여부를 정의한다. |
| [`a_asset_use`](a/a_asset_use.md) | 자산 사용 실적 | A_Asset_Use_ID | 0 | 자산별 사용일과 사용량을 기록한다. |
| [`a_depreciation`](a/a_depreciation.md) | 감가상각 함수 | Depreciation | 11 | 시스템에서 사용할 수 있는 감가상각 함수를 관리한다. |
| [`a_depreciation_build`](a/a_depreciation_build.md) | 감가상각 예상 계산 | Build Depreciation | 0 | 총계정원장 전기 전에 감가상각 예상치를 생성·처리하는 데 필요한 정보를 관리한다. |
| [`a_depreciation_convention`](a/a_depreciation_convention.md) | 감가상각 적용 관례 | Depreciation Convention | 6 | 감가상각 계산에서 사용할 관례 유형을 관리한다. |
| [`a_depreciation_entry`](a/a_depreciation_entry.md) | 감가상각 전표 처리 | Depreciation Entry | 0 | 감가상각 회계 항목을 처리하는 데 필요한 정보를 관리한다. |
| [`a_depreciation_exp`](a/a_depreciation_exp.md) | 감가상각 작업 항목 | A_Depreciation_Exp_ID | 0 | 고정자산 관련 회계 항목과 예상치를 생성하는 작업 데이터를 보관한다. |
| [`a_depreciation_forecast`](a/a_depreciation_forecast.md) | 감가상각 예측 실행 | Depreciation Forecast | 0 | 시작·종료 자산 범위와 문서일·전기 유형을 지정하여 감가상각 예측 처리 상태를 관리한다. |
| [`a_depreciation_method`](a/a_depreciation_method.md) | 감가상각 조정 방법 | Depreciation Method | 3 | 고정자산 잔액의 감가상각 조정을 처리하는 방법을 관리한다. |
| [`a_depreciation_table_detail`](a/a_depreciation_table_detail.md) | 감가상각률 표 상세 | Depreciation Table Detail | 2,579 | 감가상각률 표의 코드와 기간별 적용 비율을 기록한다. |
| [`a_depreciation_table_header`](a/a_depreciation_table_header.md) | 감가상각률 표 정의 | A_Depreciation_Table_Header_ID | 122 | 감가상각률 표의 코드·기간·비율 유형 등 공통 정보를 정의한다. |
| [`a_depreciation_workfile`](a/a_depreciation_workfile.md) | 자산 원가·상각 잔액 | A_Depreciation_Workfile_ID | 0 | 개별 고정자산의 원가와 감가상각 잔액을 관리한다. |
| [`a_fundingmode`](a/a_fundingmode.md) | 자산 자금조달 방식 | Asset Funding Mode | 0 | 자산 자금조달 방식을 코드와 명칭으로 관리한다. |
| [`a_fundingmode_acct`](a/a_fundingmode_acct.md) | 자금조달 방식별 계정 | Asset Funding Mode Accounting | 0 | 자산 자금조달 방식과 회계 스키마별 계정을 연결한다. |
| [`a_registration`](a/a_registration.md) | 사용자 자산 등록 | Registration | 0 | 사용자의 자산 등록 정보를 관리한다. |
| [`a_registrationattribute`](a/a_registrationattribute.md) | 자산 등록 속성 | Registration Attribute | 0 | 자산 등록 시 기록할 속성을 정의한다. |
| [`a_registrationproduct`](a/a_registrationproduct.md) | 제품별 등록 속성 | Registration Product | 0 | 제품과 자산 등록 속성을 연결한다. |
| [`a_registrationvalue`](a/a_registrationvalue.md) | 자산 등록 속성값 | A_RegistrationValue | 0 | 자산 등록 건에 지정된 등록 속성의 값을 기록한다. |
| [`ad_accesslog`](ad/ad_accesslog.md) | 시스템 접근 로그 | Access Log | 0 | 시스템에 접근한 내역을 기록한다. |
| [`ad_alert`](ad/ad_alert.md) | 알림 정의 | Alert | 1 | 시스템 알림을 정의하고 관련 처리 설정을 관리한다. |
| [`ad_alertprocessor`](ad/ad_alertprocessor.md) | 알림 처리기 | Alert Processor | 1 | 알림 처리 서버와 실행 매개변수를 관리한다. |
| [`ad_alertprocessorlog`](ad/ad_alertprocessorlog.md) | 알림 처리 로그 | Alert Processor Log | 0 | 알림 처리기의 실행 결과를 기록한다. |
| [`ad_alertrecipient`](ad/ad_alertrecipient.md) | 알림 수신 대상 | Alert Recipient | 1 | 알림 통지를 받을 수신 대상을 지정한다. |
| [`ad_alertrule`](ad/ad_alertrule.md) | 알림 규칙 | Alert Rule | 1 | 알림을 구성하는 규칙을 정의한다. |
| [`ad_archive`](ad/ad_archive.md) | 문서 보관 | Archive | 0 | 보관 대상 문서의 정보를 관리한다. |
| [`ad_archive_blob`](ad/ad_archive_blob.md) | 보관 문서 바이너리 | — | 0 | 문서 보관 항목에 연결된 바이너리 데이터를 저장한다. |
| [`ad_attachment`](ad/ad_attachment.md) | 첨부 문서 | Attachment | 1 | 문서에 연결된 첨부 정보를 관리한다. |
| [`ad_attachment_entry`](ad/ad_attachment_entry.md) | 첨부 바이너리 항목 | — | 0 | 첨부 문서에 속한 바이너리 데이터를 순번별로 저장한다. |
| [`ad_attachmentfile`](ad/ad_attachmentfile.md) | 첨부 파일 메타데이터 | Attachment File | 0 | 첨부 파일의 이름·크기·형식·경로·체크섬과 순서를 기록한다. |
| [`ad_attachmentnote`](ad/ad_attachmentnote.md) | 첨부 개인 메모 | Attachment Note | 0 | 첨부 문서에 대한 개인 메모를 관리한다. |
| [`ad_attribute`](ad/ad_attribute.md) | 시스템 확장 속성 | System Attribute | 0 | 테이블에 적용할 속성의 참조 유형·검증·기본값·입력 및 표시 규칙을 정의한다. |
| [`ad_attribute_value`](ad/ad_attribute_value.md) | 시스템 속성값 | AD_Attribute_Value | 0 | 레코드별 시스템 속성값을 숫자·날짜·문자 유형으로 저장한다. |
| [`ad_authorizationaccount`](ad/ad_authorizationaccount.md) | 외부 서비스 인가 계정 | Authorization Account | 0 | 사용자와 외부 서비스 인가 자격을 연결하고 토큰·유효시간·인가 상태를 관리한다. 실제 자격정보 값은 문서에 포함하지 않는다. |
| [`ad_authorizationcredential`](ad/ad_authorizationcredential.md) | 외부 서비스 인가 자격 설정 | Authorization Credential | 0 | 인가 제공자별 클라이언트 식별자·비밀정보·리디렉션 주소와 요청 범위를 설정한다. 실제 자격정보 값은 문서에 포함하지 않는다. |
| [`ad_authorizationprovider`](ad/ad_authorizationprovider.md) | 외부 서비스 인가 제공자 | Authorization Provider | 2 | 외부 서비스의 인가·토큰 발급·취소 주소와 인가 유형을 정의한다. |
| [`ad_authorizationscopeprov`](ad/ad_authorizationscopeprov.md) | 인가 제공자별 권한 범위 | Authorization Scope Provider | 3 | 인가 제공자에 연결된 권한 범위와 범위 주소를 정의한다. |
| [`ad_broadcastmessage`](ad/ad_broadcastmessage.md) | 전체 공지 | Broadcast Message | 0 | 시스템 사용자에게 전달할 공지 메시지를 관리한다. |
| [`ad_broadcastmessage_trl`](ad/ad_broadcastmessage_trl.md) | 전체 공지 번역 | Broadcast Message Trl | 0 | 전체 공지 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_changelog`](ad/ad_changelog.md) | 데이터 변경 로그 | Change Log | 0 | 데이터 변경 내역을 기록한다. |
| [`ad_chart`](ad/ad_chart.md) | 차트 정의 | Chart | 4 | 정보를 그래프로 표시하기 위한 차트를 정의한다. |
| [`ad_chart_trl`](ad/ad_chart_trl.md) | 차트 정의 번역 | Chart Trl | 4 | 차트 정의 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_chartdatasource`](ad/ad_chartdatasource.md) | 차트 데이터 원천 | Chart Datasource | 6 | 차트에 표시할 데이터를 조회하는 쿼리를 정의한다. |
| [`ad_chartdatasource_trl`](ad/ad_chartdatasource_trl.md) | 차트 데이터 원천 번역 | Chart Datasource Trl | 6 | 차트 데이터 원천 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_client`](ad/ad_client.md) | 테넌트 | Tenant | 2 | 하나의 설치 환경에서 구분되는 테넌트를 정의한다. |
| [`ad_clientinfo`](ad/ad_clientinfo.md) | 테넌트 상세 설정 | AD_ClientInfo | 2 | 테넌트의 회계 스키마·달력·단위·업무 트리·저장소 등 공통 설정을 관리한다. |
| [`ad_clientshare`](ad/ad_clientshare.md) | 테넌트·조직 데이터 공유 규칙 | Tenant Share | 0 | 테넌트와 조직 간 데이터 공유 또는 공유 금지 규칙을 관리한다. |
| [`ad_color`](ad/ad_color.md) | 시스템 색상 | System Color | 0 | 배경이나 상태 표시 등에 사용할 색상을 정의한다. |
| [`ad_color_trl`](ad/ad_color_trl.md) | 시스템 색상 번역 | System Color Trl | 0 | 시스템 색상 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_column`](ad/ad_column.md) | 애플리케이션 사전 열 | Column | 26,476 | 테이블 열에 대한 애플리케이션 사전 정의를 관리한다. |
| [`ad_column_access`](ad/ad_column_access.md) | 열 접근 권한 | AD_Column_Access | 0 | 역할별 테이블 열 접근 제외 여부와 읽기 전용 여부를 설정한다. |
| [`ad_column_trl`](ad/ad_column_trl.md) | 애플리케이션 사전 열 번역 | Column Trl | 26,476 | 애플리케이션 사전 열 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_ctxhelp`](ad/ad_ctxhelp.md) | 화면별 도움말 연결 | Context Help | 1 | 탭·프로세스·폼 등 화면 구성요소에 문맥 도움말을 연결한다. |
| [`ad_ctxhelpmsg`](ad/ad_ctxhelpmsg.md) | 문맥 도움말 메시지 | Context Help Message | 1 | 문맥 도움말에 속한 메시지를 줄 순서별로 관리한다. |
| [`ad_ctxhelpmsg_trl`](ad/ad_ctxhelpmsg_trl.md) | 문맥 도움말 메시지 번역 | Context Help Message Trl | 1 | 문맥 도움말 메시지 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_ctxhelpsuggestion`](ad/ad_ctxhelpsuggestion.md) | 문맥 도움말 제안 | Context Help Suggestion | 0 | 문맥 도움말 내용을 개선하기 위한 제안을 관리한다. |
| [`ad_desktop`](ad/ad_desktop.md) | 데스크톱 구성 | Desktop | 1 | 여러 작업 공간을 묶어 데스크톱 구성을 정의한다. |
| [`ad_desktop_trl`](ad/ad_desktop_trl.md) | 데스크톱 구성 번역 | Desktop Trl | 1 | 데스크톱 구성 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_desktopworkbench`](ad/ad_desktopworkbench.md) | 데스크톱 작업 공간 배치 | Desktop Workbench | 1 | 데스크톱에 포함할 작업 공간과 표시 순서를 지정한다. |
| [`ad_document_action_access`](ad/ad_document_action_access.md) | 문서 작업 권한 | Document Action Access | 2,156 | 테넌트·역할·문서 유형·문서 작업 조합에 대한 접근 규칙을 정의한다. 원본 도움말에 따르면 특정 테넌트·유형·작업 조합에 규칙이 없으면 모든 역할이 접근할 수 있다. |
| [`ad_element`](ad/ad_element.md) | 공통 데이터 요소 | System Element | 5,985 | 여러 열에서 사용하는 설명과 도움말을 중앙에서 관리한다. |
| [`ad_element_trl`](ad/ad_element_trl.md) | 공통 데이터 요소 번역 | System Element Trl | 5,985 | 공통 데이터 요소 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_entitytype`](ad/ad_entitytype.md) | 엔터티 유형 | Entity Type | 12 | 시스템 구성요소를 구분하는 엔터티 유형을 정의한다. |
| [`ad_error`](ad/ad_error.md) | 오류 코드 | Error | 0 | 언어별 오류 이름과 코드를 관리한다. |
| [`ad_field`](ad/ad_field.md) | 화면 필드 | Field | 21,281 | 데이터베이스 열을 화면 필드로 표현하기 위한 정의를 관리한다. |
| [`ad_field_trl`](ad/ad_field_trl.md) | 화면 필드 번역 | Field Trl | 21,281 | 화면 필드 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_fieldgroup`](ad/ad_fieldgroup.md) | 필드 그룹 | Field Group | 79 | 관련 필드를 논리적 그룹으로 묶는다. |
| [`ad_fieldgroup_trl`](ad/ad_fieldgroup_trl.md) | 필드 그룹 번역 | Field Group Trl | 79 | 필드 그룹 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_fieldsuggestion`](ad/ad_fieldsuggestion.md) | 필드 문구 제안 | Field Suggestions | 0 | 필드의 표시 이름·설명·도움말에 대한 개선 제안을 관리한다. |
| [`ad_find`](ad/ad_find.md) | 검색 조건 항목 | Find | 0 | 검색에 사용할 열·연산자·값과 조건 결합 방식을 기록한다. |
| [`ad_form`](ad/ad_form.md) | 특수 폼 | Special Form | 51 | 일반 데이터 창과 구분되는 특수 폼을 정의한다. |
| [`ad_form_access`](ad/ad_form_access.md) | 특수 폼 접근 권한 | AD_Form_Access | 137 | 역할별 특수 폼 접근 및 읽기·쓰기 권한을 설정한다. |
| [`ad_form_trl`](ad/ad_form_trl.md) | 특수 폼 번역 | Special Form Trl | 51 | 특수 폼 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_housekeeping`](ad/ad_housekeeping.md) | 데이터 정리 설정 | House Keeping Configuration | 10 | 테이블별 정리 조건·백업 옵션과 최근 실행·삭제 정보를 관리한다. |
| [`ad_image`](ad/ad_image.md) | 시스템 이미지 | Image | 10 | 시스템에서 사용할 이미지나 아이콘을 관리한다. |
| [`ad_image_blob`](ad/ad_image_blob.md) | 이미지 바이너리 | — | 0 | 시스템 이미지에 연결된 바이너리 데이터를 저장한다. |
| [`ad_impformat`](ad/ad_impformat.md) | 데이터 가져오기 형식 | Import Format | 15 | 가져올 데이터의 대상 테이블·형식·구분자를 정의한다. |
| [`ad_impformat_row`](ad/ad_impformat_row.md) | 가져오기 필드 매핑 | Format Field | 163 | 가져오기 형식에서 각 필드의 위치·데이터 유형·변환 규칙과 대상 열을 지정한다. |
| [`ad_importtemplate`](ad/ad_importtemplate.md) | 데이터 가져오기 템플릿 | Import Template | 0 | 창·탭별 데이터 가져오기에 사용할 문자셋·CSV 헤더·구분자 등 템플릿을 정의한다. |
| [`ad_importtemplateaccess`](ad/ad_importtemplateaccess.md) | 가져오기 템플릿 권한 | Import Template Access | 0 | 역할별 가져오기 템플릿의 삽입·병합·수정 허용 여부를 관리한다. |
| [`ad_indexcolumn`](ad/ad_indexcolumn.md) | 인덱스 구성 열 | Table Index Column | 1,537 | 테이블 인덱스를 구성하는 열의 정의를 관리한다. |
| [`ad_infocolumn`](ad/ad_infocolumn.md) | 조회 창 열 | Info Column | 198 | 조회 창에 표시할 열과 검색 조건·표현식·참조·입력 규칙을 정의한다. |
| [`ad_infocolumn_trl`](ad/ad_infocolumn_trl.md) | 조회 창 열 번역 | Info Column Trl | 198 | 조회 창 열 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_infoprocess`](ad/ad_infoprocess.md) | 조회 창 프로세스 | Info Process | 11 | 조회 창에서 사용할 프로세스를 연결한다. |
| [`ad_inforelated`](ad/ad_inforelated.md) | 연관 조회 창 | Info Related | 0 | 조회 창 사이의 연관 관계와 연결 열·표시 조건을 정의한다. |
| [`ad_infowindow`](ad/ad_infowindow.md) | 조회 창 | Info Window | 17 | 검색·선택용 조회 창의 대상 테이블·SQL 구성·정렬·페이지 설정을 정의한다. |
| [`ad_infowindow_access`](ad/ad_infowindow_access.md) | 조회 창 접근 권한 | Info Window Access | 54 | 역할에 허용되는 조회 창을 연결한다. |
| [`ad_infowindow_trl`](ad/ad_infowindow_trl.md) | 조회 창 번역 | Info Window Trl | 17 | 조회 창 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_issue`](ad/ad_issue.md) | 시스템 오류 보고 | System Issue | 0 | 오류 요약·발생 위치·실행환경·스택 추적 및 관련 요청 정보를 기록한다. |
| [`ad_label`](ad/ad_label.md) | 레코드 라벨 | Label | 0 | 레코드 분류에 사용할 라벨을 정의한다. |
| [`ad_label_trl`](ad/ad_label_trl.md) | 레코드 라벨 번역 | Label Trl | 0 | 레코드 라벨 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_labelassignment`](ad/ad_labelassignment.md) | 레코드 라벨 부여 | Label Assignment | 0 | 테이블의 특정 레코드에 라벨을 연결한다. |
| [`ad_labelcategory`](ad/ad_labelcategory.md) | 라벨 분류 | Label Category | 0 | 라벨을 묶는 분류를 정의한다. |
| [`ad_labelcategory_trl`](ad/ad_labelcategory_trl.md) | 라벨 분류 번역 | Label Category Trl | 0 | 라벨 분류 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_labelcategorytable`](ad/ad_labelcategorytable.md) | 라벨 분류 적용 테이블 | Label Category Table Access | 0 | 라벨 분류를 적용할 수 있는 테이블을 연결한다. |
| [`ad_labelprinter`](ad/ad_labelprinter.md) | 라벨 프린터 | Label printer | 0 | 라벨 출력에 사용할 프린터를 정의한다. |
| [`ad_labelprinterfunction`](ad/ad_labelprinterfunction.md) | 라벨 프린터 기능 | Label printer Function | 0 | 라벨 프린터의 기능을 정의한다. |
| [`ad_language`](ad/ad_language.md) | 언어·지역 설정 | Language ID | 109 | 언어 코드와 국가·날짜·시간·숫자 표시 방식 및 시스템 사용 여부를 관리한다. |
| [`ad_ldapaccess`](ad/ad_ldapaccess.md) | LDAP 접근 로그 | Ldap Access | 0 | LDAP 접근 내역을 기록한다. |
| [`ad_ldapprocessor`](ad/ad_ldapprocessor.md) | LDAP 처리 서버 | Ldap Processor | 1 | LDAP 서버 처리 설정을 관리한다. |
| [`ad_ldapprocessorlog`](ad/ad_ldapprocessorlog.md) | LDAP 처리 로그 | Ldap Processor Log | 0 | LDAP 서버의 처리 로그를 기록한다. |
| [`ad_menu`](ad/ad_menu.md) | 메뉴 | Menu | 813 | 시스템 메뉴 항목을 정의한다. |
| [`ad_menu_trl`](ad/ad_menu_trl.md) | 메뉴 번역 | Menu Trl | 813 | 메뉴 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_message`](ad/ad_message.md) | 시스템 메시지 | Message | 2,105 | 시스템에서 표시할 메시지를 관리한다. |
| [`ad_message_trl`](ad/ad_message_trl.md) | 시스템 메시지 번역 | Message Trl | 2,105 | 시스템 메시지 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_migrationscript`](ad/ad_migrationscript.md) | 마이그레이션 스크립트 | Migration Script | 1,341 | 시스템 마이그레이션 스크립트 정보를 관리한다. |
| [`ad_modelgeneratortemplate`](ad/ad_modelgeneratortemplate.md) | 모델 생성 템플릿 | Model Generator Template | 0 | 모델 코드 생성에 사용할 테이블·열 엔터티 범위와 패키지·출력 폴더를 설정한다. |
| [`ad_modelvalidator`](ad/ad_modelvalidator.md) | 전역 모델 검증기 | Model Validator | 3 | 시스템 전역에 적용하는 모델 검증기를 정의한다. |
| [`ad_modification`](ad/ad_modification.md) | 변경 정의 | Modification | 0 | 변경 항목의 이름·설명·엔터티 유형·버전과 순서를 기록한다. 구체적인 적용 절차는 이 메타데이터만으로 확정할 수 없다. |
| [`ad_note`](ad/ad_note.md) | 시스템 통지 | Notice | 0 | 시스템 통지 내용을 관리한다. |
| [`ad_org`](ad/ad_org.md) | 조직 | Organization | 10 | 테넌트 내부의 조직 단위를 정의한다. |
| [`ad_orginfo`](ad/ad_orginfo.md) | 조직 상세 정보 | Organization Info | 10 | 조직의 주소·세무 정보·상위 조직·창고·연락처 등 상세 설정을 관리한다. |
| [`ad_orgtype`](ad/ad_orgtype.md) | 조직 유형 | Organization Type | 3 | 조직을 분류하는 유형을 정의한다. |
| [`ad_package_exp`](ad/ad_package_exp.md) | 패키지 내보내기 | Package Exp. | 0 | 내보낼 구성 패키지의 이름·버전·파일 위치와 처리 옵션을 관리한다. |
| [`ad_package_exp_common`](ad/ad_package_exp_common.md) | 공통 내보내기 구성요소 | Common Package Exp. | 0 | 현재 인스턴스에서 만드는 모든 패키지에 공통으로 포함할 구성요소를 관리한다. |
| [`ad_package_exp_detail`](ad/ad_package_exp_detail.md) | 내보내기 패키지 상세 | Package Exp. Detail | 0 | 내보내기 패키지에 포함할 창·프로세스·테이블·파일·SQL 등 개별 구성요소를 지정한다. |
| [`ad_package_imp`](ad/ad_package_imp.md) | 패키지 가져오기 | Package Imp. | 0 | 가져온 구성 패키지의 버전·상태·생성자 및 제거 관련 정보를 관리한다. |
| [`ad_package_imp_backup`](ad/ad_package_imp_backup.md) | 패키지 적용 전 백업 | Imp. Package Backup | 0 | 패키지 가져오기와 관련된 테이블·열의 원래 값과 백업 위치를 기록한다. |
| [`ad_package_imp_detail`](ad/ad_package_imp_detail.md) | 패키지 가져오기 상세 | Imp. Package Detail | 0 | 패키지의 개별 레코드에 수행한 작업과 성공 여부·결과를 기록한다. |
| [`ad_package_imp_inst`](ad/ad_package_imp_inst.md) | 패키지 설치 정보 | Package Imp. Inst. | 0 | 패키지 설치 항목의 이름·버전·상태와 생성자 정보를 기록한다. |
| [`ad_package_imp_proc`](ad/ad_package_imp_proc.md) | 패키지 가져오기 실행 설정 | Package Imp. Proc. | 0 | 패키지 원천·디렉터리·사전 덮어쓰기 옵션과 처리일·메시지를 관리한다. |
| [`ad_package_uuid_map`](ad/ad_package_uuid_map.md) | 테넌트 간 UUID 매핑 | UUID Mapping | 0 | 테넌트 사이의 UUID 대응 관계를 관리한다. |
| [`ad_password_history`](ad/ad_password_history.md) | 비밀번호 변경 이력 | Password History ID | 0 | 일정 기간 이전 비밀번호의 재사용을 제한하기 위한 이력을 관리한다. |
| [`ad_passwordrule`](ad/ad_passwordrule.md) | 비밀번호 정책 | Password Policies | 0 | 비밀번호 길이·문자 조합·사전 단어·연속 문자열·재사용 기간 등의 규칙을 설정한다. |
| [`ad_pinstance`](ad/ad_pinstance.md) | 프로세스 실행 인스턴스 | Process Instance | 0 | 개별 프로세스 실행 인스턴스를 관리한다. |
| [`ad_pinstance_log`](ad/ad_pinstance_log.md) | 프로세스 실행 로그 | AD_PInstance_Log | 0 | 프로세스 실행 인스턴스에 연결된 로그를 기록한다. |
| [`ad_pinstance_para`](ad/ad_pinstance_para.md) | 프로세스 실행 인수 | AD_PInstance_Para | 0 | 프로세스 실행 시 전달한 문자열·숫자·날짜 인수와 범위 값을 기록한다. |
| [`ad_postit`](ad/ad_postit.md) | 레코드 메모 | Post-it | 0 | 특정 테이블의 레코드에 붙인 메모를 저장한다. |
| [`ad_preference`](ad/ad_preference.md) | 개인 환경설정 | Preference | 17 | 개인별 환경설정 값을 관리한다. |
| [`ad_printcolor`](ad/ad_printcolor.md) | 출력 색상 | Print Color | 23 | 출력과 화면 표시에 사용할 색상을 정의한다. |
| [`ad_printcolor_trl`](ad/ad_printcolor_trl.md) | 출력 색상 번역 | Print Color | 23 | 출력 색상 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_printfont`](ad/ad_printfont.md) | 출력 글꼴 | Print Font | 66 | 인쇄에 사용할 글꼴을 관리한다. |
| [`ad_printform`](ad/ad_printform.md) | 출력 서식 연결 | Print Form | 2 | 청구서·주문·송금·출하 등 문서 유형별 출력 형식과 메일 문구를 연결한다. |
| [`ad_printformat`](ad/ad_printformat.md) | 출력 형식 | Print Format | 93 | 데이터를 출력하는 형식을 정의한다. |
| [`ad_printformat_trl`](ad/ad_printformat_trl.md) | 출력 형식 번역 | Print Format Trl | 93 | 출력 형식 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_printformatitem`](ad/ad_printformatitem.md) | 출력 형식 항목 | Print Format Item | 2,780 | 출력 형식을 구성하는 개별 항목과 열을 정의한다. |
| [`ad_printformatitem_trl`](ad/ad_printformatitem_trl.md) | 출력 형식 항목 번역 | Print Format Item Trl | 2,780 | 출력 형식 항목 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_printgraph`](ad/ad_printgraph.md) | 보고서 그래프 | Graph | 0 | 보고서에 포함할 그래프를 정의한다. |
| [`ad_printheaderfooter`](ad/ad_printheaderfooter.md) | 출력 머리말·꼬리말 | Print Header/Footer | 0 | 출력 머리말·꼬리말의 이름과 구현 클래스를 정의한다. |
| [`ad_printlabel`](ad/ad_printlabel.md) | 라벨 출력 형식 | Print Label | 0 | 라벨을 인쇄하기 위한 형식을 정의한다. |
| [`ad_printlabelline`](ad/ad_printlabelline.md) | 라벨 출력 줄 | Print Label Line | 0 | 라벨 출력 형식을 구성하는 줄을 정의한다. |
| [`ad_printlabelline_trl`](ad/ad_printlabelline_trl.md) | 라벨 출력 줄 번역 | Print Label Line Trl | 0 | 라벨 출력 줄 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_printpaper`](ad/ad_printpaper.md) | 인쇄 용지 | Print Paper | 4 | 인쇄 용지 규격을 정의한다. |
| [`ad_printtableformat`](ad/ad_printtableformat.md) | 보고서 표 형식 | Print Table Format | 2 | 보고서에서 사용할 표 형식을 정의한다. |
| [`ad_private_access`](ad/ad_private_access.md) | 개인 레코드 접근 | Private Access | 0 | 사용자와 특정 테이블 레코드 사이의 개인 접근 연결을 관리한다. |
| [`ad_process`](ad/ad_process.md) | 프로세스·보고서 | Process | 472 | 실행할 프로세스 또는 보고서를 정의한다. |
| [`ad_process_access`](ad/ad_process_access.md) | 프로세스 접근 권한 | Process Access | 1,297 | 역할별 프로세스 접근 및 읽기·쓰기 권한을 설정한다. |
| [`ad_process_drillrule`](ad/ad_process_drillrule.md) | 보고서 상세 탐색 규칙 | Drill Rule | 0 | 프로세스·테이블·보고서 뷰·출력 형식을 연결하여 상세 탐색 규칙을 정의한다. |
| [`ad_process_drillrule_para`](ad/ad_process_drillrule_para.md) | 상세 탐색 인수 기본값 | Drill Rule Parameter | 0 | 상세 탐색 규칙에 적용할 프로세스 인수와 범위 기본값을 지정한다. |
| [`ad_process_drillrule_trl`](ad/ad_process_drillrule_trl.md) | 보고서 상세 탐색 규칙 번역 | Drill Rule Trl | 0 | 보고서 상세 탐색 규칙 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_process_para`](ad/ad_process_para.md) | 프로세스 입력 매개변수 | Process Parameter | 1,223 | 프로세스 입력 항목의 유형·범위·기본값·검증 및 표시 조건을 정의한다. |
| [`ad_process_para_trl`](ad/ad_process_para_trl.md) | 프로세스 입력 매개변수 번역 | Process Parameter Trl | 1,223 | 프로세스 입력 매개변수 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_process_trl`](ad/ad_process_trl.md) | 프로세스·보고서 번역 | Process Trl | 472 | 프로세스·보고서 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_recentitem`](ad/ad_recentitem.md) | 최근 사용 항목 | Recent Item | 0 | 사용자가 최근 사용한 창·탭·레코드를 역할과 함께 기록한다. |
| [`ad_record_access`](ad/ad_record_access.md) | 역할별 레코드 권한 | AD_Record_Access | 0 | 역할별 특정 레코드의 읽기 전용·제외 여부와 종속 데이터 적용 여부를 설정한다. |
| [`ad_ref_list`](ad/ad_ref_list.md) | 선택 목록 값 | Reference List | 1,529 | 참조 선택 목록을 구성하는 값을 관리한다. |
| [`ad_ref_list_trl`](ad/ad_ref_list_trl.md) | 선택 목록 값 번역 | Reference List Trl | 1,529 | 선택 목록 값 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_ref_table`](ad/ad_ref_table.md) | 테이블 기반 참조 | AD_Ref_Table | 234 | 테이블을 이용한 참조 정의를 관리한다. |
| [`ad_reference`](ad/ad_reference.md) | 참조 유형 | Reference | 591 | 시스템의 선택 목록과 참조 유형을 정의한다. |
| [`ad_reference_trl`](ad/ad_reference_trl.md) | 참조 유형 번역 | Reference Trl | 591 | 참조 유형 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_registration`](ad/ad_registration.md) | 시스템 등록 | System Registration | 0 | 시스템 등록 정보를 관리한다. 원본 도움말은 하나의 레코드만 유지하고 추가하지 않도록 명시한다. |
| [`ad_relationtype`](ad/ad_relationtype.md) | 레코드 관계 유형 | Relation Type | 6 | 레코드 쌍이 관계에 포함되기 위해 충족해야 하는 조건과 관계 집합을 정의한다. |
| [`ad_replication`](ad/ad_replication.md) | 데이터 복제 대상 | Replication | 1 | 데이터를 복제할 대상을 정의한다. |
| [`ad_replication_log`](ad/ad_replication_log.md) | 데이터 복제 상세 로그 | Replication Log | 0 | 데이터 복제 처리의 상세 로그를 기록한다. |
| [`ad_replication_run`](ad/ad_replication_run.md) | 데이터 복제 실행 | Replication Run | 0 | 데이터 복제 실행 건을 관리한다. |
| [`ad_replicationdocument`](ad/ad_replicationdocument.md) | 문서별 복제 설정 | Replication Document | 1 | 복제 전략에 문서 유형·대상 테이블·복제 유형을 연결한다. |
| [`ad_replicationstrategy`](ad/ad_replicationstrategy.md) | 데이터 복제 전략 | Replication Strategy | 2 | 데이터 복제 전략을 정의한다. |
| [`ad_replicationtable`](ad/ad_replicationtable.md) | 복제 전략 대상 테이블 | Replication Table | 473 | 복제 전략에 포함되는 테이블 정보를 관리한다. |
| [`ad_reportview`](ad/ad_reportview.md) | 보고서 조회 정의 | Report View | 102 | 보고서를 생성할 때 사용할 조회 뷰 정의를 관리한다. |
| [`ad_reportview_col`](ad/ad_reportview_col.md) | 보고서 열 함수 | Report view Column | 0 | 보고서 조회의 열에 적용할 함수와 집계 함수 여부를 정의한다. |
| [`ad_reportview_column`](ad/ad_reportview_column.md) | 보고서 선택 열 | Report View Selected column | 0 | 보고서 조회에 포함할 열을 연결한다. |
| [`ad_requiredplugin`](ad/ad_requiredplugin.md) | 필수 플러그인 | Required Plugin | 0 | 누락 시 시스템 오류나 데이터 손상을 일으킬 수 있는 필수 플러그인을 등록한다. |
| [`ad_role`](ad/ad_role.md) | 역할 | Role | 5 | 사용자의 책임과 접근 권한을 구분하는 역할을 정의한다. |
| [`ad_role_included`](ad/ad_role_included.md) | 포함 역할 | Included Role | 0 | 역할에 포함되는 다른 역할과 적용 순서를 지정한다. |
| [`ad_role_orgaccess`](ad/ad_role_orgaccess.md) | 역할별 조직 접근 | AD_Role_OrgAccess | 18 | 역할별 조직 접근과 읽기 전용 여부를 설정한다. |
| [`ad_rule`](ad/ad_rule.md) | 실행 규칙 스크립트 | Rule | 4 | 이벤트·규칙 유형에 따른 스크립트와 접근 수준을 정의한다. |
| [`ad_schedule`](ad/ad_schedule.md) | 실행 일정 | Schedule | 5 | 스케줄러가 사용할 실행 시점을 정의한다. |
| [`ad_scheduler`](ad/ad_scheduler.md) | 프로세스 스케줄러 | Scheduler | 12 | 프로세스를 일정에 따라 실행하도록 설정한다. |
| [`ad_scheduler_para`](ad/ad_scheduler_para.md) | 예약 실행 인수 | AD_Scheduler_Para | 14 | 예약 실행할 프로세스의 인수와 범위 기본값을 설정한다. |
| [`ad_schedulerlog`](ad/ad_schedulerlog.md) | 스케줄러 실행 로그 | Scheduler Log | 0 | 스케줄러 실행 결과를 기록한다. |
| [`ad_schedulerrecipient`](ad/ad_schedulerrecipient.md) | 스케줄러 통지 수신자 | Scheduler Recipient | 1 | 스케줄러 통지를 받을 대상을 지정한다. |
| [`ad_searchdefinition`](ad/ad_searchdefinition.md) | 검색 정의 | Search Definition | 2 | 테이블·열에 대한 검색 쿼리·유형과 연결 창을 정의한다. |
| [`ad_sequence`](ad/ad_sequence.md) | 문서 번호 채번 | Sequence | 1,445 | 문서 번호를 생성하는 채번 규칙을 관리한다. |
| [`ad_sequence_audit`](ad/ad_sequence_audit.md) | 문서 채번 이력 | AD_Sequence_Audit | 0 | 채번 규칙으로 생성한 문서 번호와 대상 테이블 레코드를 기록한다. |
| [`ad_sequence_no`](ad/ad_sequence_no.md) | 구분 키별 다음 번호 | AD_Sequence_No | 0 | 채번 규칙의 구분 키마다 다음에 사용할 번호를 관리한다. |
| [`ad_session`](ad/ad_session.md) | 사용자 세션 | Session | 0 | 온라인 또는 웹 사용자 세션을 관리한다. |
| [`ad_smtp`](ad/ad_smtp.md) | 메일 발송 서버 | SMTP Server | 0 | SMTP 호스트·포트·보안 및 인증 옵션과 적용 메일 범위를 설정한다. |
| [`ad_statusline`](ad/ad_statusline.md) | 상태 표시줄 정의 | Status Line | 7 | 상태 표시줄에 사용할 메시지·SQL과 표시 스타일을 정의한다. |
| [`ad_statuslineusedin`](ad/ad_statuslineusedin.md) | 상태 표시줄 적용 위치 | AD_StatusLineUsedIn | 14 | 상태 표시줄을 적용할 창·탭·테이블·조회 창과 순서를 지정한다. |
| [`ad_storageprovider`](ad/ad_storageprovider.md) | 파일 저장소 제공자 | Storage Provider | 0 | 파일 저장 방식·경로·주소와 기본 저장소 여부를 정의한다. |
| [`ad_style`](ad/ad_style.md) | 화면 스타일 | Style | 1 | 필드와 라벨에 적용할 CSS 스타일을 정의한다. |
| [`ad_styleline`](ad/ad_styleline.md) | 스타일 상세 항목 | Style Line | 1 | 화면 스타일을 구성하는 상세 항목을 관리한다. |
| [`ad_sysconfig`](ad/ad_sysconfig.md) | 시스템 설정값 | System Configurator | 213 | 설정 이름과 값, 엔터티 유형 및 설정 적용 수준을 관리한다. |
| [`ad_system`](ad/ad_system.md) | 시스템 정의 | System | 1 | 설치된 시스템의 기본 정의를 관리한다. |
| [`ad_tab`](ad/ad_tab.md) | 화면 탭 | Tab | 1,153 | 창 내부의 탭을 정의한다. |
| [`ad_tab_customization`](ad/ad_tab_customization.md) | 탭 그리드 개인화 | Tab Customization | 0 | 사용자의 탭 그리드 표시 설정을 관리한다. |
| [`ad_tab_trl`](ad/ad_tab_trl.md) | 화면 탭 번역 | Tab Trl | 1,153 | 화면 탭 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_table`](ad/ad_table.md) | 애플리케이션 사전 테이블 | Table | 1,063 | 애플리케이션에서 사용하는 테이블의 사전 정의를 관리한다. |
| [`ad_table_access`](ad/ad_table_access.md) | 테이블 접근 권한 | AD_Table_Access | 1 | 역할별 테이블 접근·읽기 전용·보고서·내보내기 허용 여부를 설정한다. |
| [`ad_table_scriptvalidator`](ad/ad_table_scriptvalidator.md) | 테이블 스크립트 검증기 | Table Script Validator | 0 | 테이블에 적용하는 스크립트 기반 모델 검증기를 정의한다. |
| [`ad_table_trl`](ad/ad_table_trl.md) | 애플리케이션 사전 테이블 번역 | Table Trl | 1,063 | 애플리케이션 사전 테이블 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_tableattribute`](ad/ad_tableattribute.md) | 레코드 확장 속성 | AD_TableAttribute_ID | 0 | 테이블의 특정 레코드에 대한 속성과 문자·숫자·날짜 값을 관리한다. |
| [`ad_tableattributeset`](ad/ad_tableattributeset.md) | 테이블 속성 집합 연결 | Table Attribute Set | 0 | 테이블과 속성 집합을 연결하여 하나의 테이블에 여러 속성 집합을 적용할 수 있게 한다. |
| [`ad_tableindex`](ad/ad_tableindex.md) | 테이블 인덱스 | Table Index | 1,192 | 테이블의 인덱스 정의를 관리한다. |
| [`ad_tablepartition`](ad/ad_tablepartition.md) | 테이블 파티션 정의 | Table Partition | 0 | 테이블 파티션의 표현식·열·상위 파티션과 연결 상태를 관리한다. |
| [`ad_tablevalrule`](ad/ad_tablevalrule.md) | 테이블별 동적 검증 | Dynamic Validation per Table | 0 | 테이블에 적용할 동적 검증 코드를 역할·사용자 조건과 함께 정의한다. |
| [`ad_task`](ad/ad_task.md) | 운영체제 작업 | OS Task | 3 | 운영체제에서 실행할 작업을 정의한다. |
| [`ad_task_access`](ad/ad_task_access.md) | 운영체제 작업 권한 | AD_Task_Access | 3 | 역할별 운영체제 작업 접근 및 읽기·쓰기 권한을 설정한다. |
| [`ad_task_trl`](ad/ad_task_trl.md) | 운영체제 작업 번역 | OS Task Trl | 3 | 운영체제 작업 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_taskinstance`](ad/ad_taskinstance.md) | 운영체제 작업 실행 | Task Instance | 0 | 운영체제 작업의 개별 실행 인스턴스를 관리한다. |
| [`ad_toolbarbutton`](ad/ad_toolbarbutton.md) | 도구 모음 버튼 | ToolBar Button | 87 | 버튼 동작·구현 클래스·단축키·표시 조건과 연결 프로세스를 정의한다. |
| [`ad_toolbarbuttonrestrict`](ad/ad_toolbarbuttonrestrict.md) | 도구 모음 버튼 제한 | ToolBar Button Restrict | 0 | 역할과 창·탭·프로세스별 도구 모음 버튼의 제외 조건을 관리한다. |
| [`ad_tree`](ad/ad_tree.md) | 계층 트리 | Tree | 23 | 계층 구조를 표현하는 트리를 정의한다. |
| [`ad_tree_favorite`](ad/ad_tree_favorite.md) | 즐겨찾기 메뉴 트리 | Favorite Tree | 4 | 대시보드에 표시할 사용자 즐겨찾기 메뉴를 관리한다. |
| [`ad_tree_favorite_node`](ad/ad_tree_favorite_node.md) | 즐겨찾기 메뉴 노드 | Favorite Node Tree | 24 | 즐겨찾기 트리의 메뉴 항목·상위 노드·순서와 로그인 시 열기 순서를 관리한다. |
| [`ad_treebar`](ad/ad_treebar.md) | 사용자 선택 트리 노드 | AD_TreeBar | 24 | 사용자가 선택한 트리 노드를 관리한다. |
| [`ad_treenode`](ad/ad_treenode.md) | 일반 트리 노드 | Tree Node | 406 | 트리의 노드·상위 노드와 표시 순서를 저장한다. |
| [`ad_treenodebp`](ad/ad_treenodebp.md) | 거래처 트리 노드 | Tree Node BP | 18 | 거래처 트리의 노드·상위 노드와 표시 순서를 저장한다. |
| [`ad_treenodecmc`](ad/ad_treenodecmc.md) | 콘텐츠 컨테이너 트리 노드 | Tree Node CM Container | 5 | 콘텐츠 컨테이너 트리의 계층과 표시 순서를 저장한다. |
| [`ad_treenodecmm`](ad/ad_treenodecmm.md) | 콘텐츠 미디어 트리 노드 | Tree Node CM Media | 3 | 콘텐츠 미디어 트리의 계층과 표시 순서를 저장한다. |
| [`ad_treenodecms`](ad/ad_treenodecms.md) | 콘텐츠 스테이지 트리 노드 | Tree Node CM Stage | 5 | 콘텐츠 스테이지 트리의 계층과 표시 순서를 저장한다. |
| [`ad_treenodecmt`](ad/ad_treenodecmt.md) | 콘텐츠 템플릿 트리 노드 | Tree Node CM Template | 4 | 콘텐츠 템플릿 트리의 계층과 표시 순서를 저장한다. |
| [`ad_treenodemm`](ad/ad_treenodemm.md) | MM 트리 노드 | Tree Node MM | 815 | MM 유형 트리의 노드·상위 노드와 표시 순서를 저장한다. MM 약어의 정확한 업무 대상은 원본 사전과 열 정보만으로 확정할 수 없다. |
| [`ad_treenodepr`](ad/ad_treenodepr.md) | PR 트리 노드 | Tree Node PR | 55 | PR 유형 트리의 노드·상위 노드와 표시 순서를 저장한다. PR 약어의 정확한 업무 대상은 원본 사전과 열 정보만으로 확정할 수 없다. |
| [`ad_treenodeu1`](ad/ad_treenodeu1.md) | 사용자 정의 트리 1 노드 | Tree Node User 1 | 0 | 사용자 정의 트리 1의 계층 노드를 관리한다. |
| [`ad_treenodeu2`](ad/ad_treenodeu2.md) | 사용자 정의 트리 2 노드 | Tree Node User 2 | 0 | 사용자 정의 트리 2의 계층 노드를 관리한다. |
| [`ad_treenodeu3`](ad/ad_treenodeu3.md) | 사용자 정의 트리 3 노드 | Tree Node User 3 | 0 | 사용자 정의 트리 3의 계층 노드를 관리한다. |
| [`ad_treenodeu4`](ad/ad_treenodeu4.md) | 사용자 정의 트리 4 노드 | Tree Node User 4 | 0 | 사용자 정의 트리 4의 계층 노드를 관리한다. |
| [`ad_user`](ad/ad_user.md) | 사용자·거래처 담당자 | User/Contact | 9 | 내부 시스템 사용자와 거래처 연락 담당자를 관리한다. |
| [`ad_user_orgaccess`](ad/ad_user_orgaccess.md) | 사용자별 조직 접근 | AD_User_OrgAccess | 0 | 사용자별 조직 접근과 읽기 전용 여부를 설정한다. |
| [`ad_user_roles`](ad/ad_user_roles.md) | 사용자 역할 부여 | AD_User_Roles | 11 | 사용자에게 부여한 역할을 연결한다. |
| [`ad_user_substitute`](ad/ad_user_substitute.md) | 사용자 대리인 | User Substitute | 0 | 사용자를 대신하는 대리인을 지정한다. |
| [`ad_userbpaccess`](ad/ad_userbpaccess.md) | 사용자의 거래처 접근 | User BP Access | 0 | 사용자 또는 연락 담당자의 거래처 정보·자원 접근을 관리한다. |
| [`ad_userdef_field`](ad/ad_userdef_field.md) | 사용자 정의 필드 설정 | User defined Field | 0 | 기존 필드의 이름·표시·입력·검증·배치를 사용자 정의 탭 안에서 재설정한다. |
| [`ad_userdef_info`](ad/ad_userdef_info.md) | 사용자 정의 조회 창 | User defined Info Window | 0 | 역할·사용자별 조회 창의 이름·도움말·대시보드 표시 등을 재설정한다. |
| [`ad_userdef_info_column`](ad/ad_userdef_info_column.md) | 사용자 정의 조회 열 | User defined Info Column | 0 | 사용자 정의 조회 창에서 열 표시·검색 조건·기본값·입력 검증을 재설정한다. |
| [`ad_userdef_info_related`](ad/ad_userdef_info_related.md) | 사용자 정의 연관 조회 | User defined Info Related | 0 | 사용자 정의 조회 창의 연관 조회 이름·표시 조건과 순서를 재설정한다. |
| [`ad_userdef_proc`](ad/ad_userdef_proc.md) | 사용자 정의 프로세스 | User defined Process | 0 | 역할·사용자별 프로세스의 이름·설명·도움말·언어 등 표시 설정을 관리한다. |
| [`ad_userdef_proc_parameter`](ad/ad_userdef_proc_parameter.md) | 사용자 정의 프로세스 인수 | AD_UserDef_Proc_Parameter_ID | 0 | 사용자 정의 프로세스에서 입력 매개변수의 표시·기본값·필수 여부·검증 및 순서를 재설정한다. |
| [`ad_userdef_tab`](ad/ad_userdef_tab.md) | 사용자 정의 탭 | User defined Tab | 0 | 사용자 정의 창에서 탭의 읽기 전용·표시·조회 조건과 배치를 재설정한다. |
| [`ad_userdef_theme`](ad/ad_userdef_theme.md) | 사용자 테마 설정 | Theme Customization | 0 | 역할·사용자별 화면 테마와 스타일시트를 관리한다. |
| [`ad_userdef_theme_detail`](ad/ad_userdef_theme_detail.md) | 사용자 테마 변경값 | Theme Customization Detail | 0 | 사용자 테마 설정에 속한 기존 값과 변경 값을 기록한다. |
| [`ad_userdef_win`](ad/ad_userdef_win.md) | 사용자 정의 창 | User defined Window | 0 | 역할·사용자별 창의 이름·언어·읽기 전용 등 설정을 관리한다. |
| [`ad_usermail`](ad/ad_usermail.md) | 사용자 발송 메일 | User Mail | 1 | 사용자에게 보낸 메일을 기록한다. |
| [`ad_userpreference`](ad/ad_userpreference.md) | 사용자 동작 환경설정 | AD_UserPreference_ID | 0 | 자동 저장·새 항목 생성·검색 결과 표시·세션 읽기 전용 등 사용자별 동작 옵션을 관리한다. |
| [`ad_userquery`](ad/ad_userquery.md) | 저장된 사용자 검색 | User Query | 2 | 사용자가 저장한 검색 조건을 관리한다. |
| [`ad_val_rule`](ad/ad_val_rule.md) | 동적 검증 규칙 | Dynamic Validation | 332 | 동적으로 적용하는 검증 규칙을 정의한다. |
| [`ad_verifymigration`](ad/ad_verifymigration.md) | 마이그레이션 검증 보조 | Verify Migration | 0 | 마이그레이션 검증을 지원하는 정보를 관리한다. |
| [`ad_viewcolumn`](ad/ad_viewcolumn.md) | 데이터베이스 뷰 열 정의 | Database View Column | 17,684 | 뷰 구성요소의 열 이름·SQL 표현식·데이터 유형과 순서를 정의한다. |
| [`ad_viewcomponent`](ad/ad_viewcomponent.md) | 데이터베이스 뷰 구성요소 | Database View Component | 229 | 뷰의 FROM·WHERE 등 SQL 구성과 참조 테이블·결합 옵션을 정의한다. |
| [`ad_wf_activity`](ad/ad_wf_activity.md) | 워크플로 활동 | Workflow Activity | 13 | 워크플로 실행에서 수행되는 활동을 관리한다. |
| [`ad_wf_activityapprover`](ad/ad_wf_activityapprover.md) | 워크플로 활동 승인자 | Workflow Activity Approver | 0 | 워크플로 활동의 승인자를 지정한다. |
| [`ad_wf_activityresult`](ad/ad_wf_activityresult.md) | 워크플로 활동 결과 | Workflow Activity Result | 0 | 워크플로 활동의 실행 결과를 기록한다. |
| [`ad_wf_block`](ad/ad_wf_block.md) | 워크플로 실행 블록 | Workflow Block | 0 | 워크플로 트랜잭션 실행 블록을 정의한다. |
| [`ad_wf_eventaudit`](ad/ad_wf_eventaudit.md) | 워크플로 이벤트 감사 | Workflow Event Audit | 13 | 워크플로 프로세스와 활동의 이벤트 감사 정보를 기록한다. |
| [`ad_wf_nextcondition`](ad/ad_wf_nextcondition.md) | 워크플로 전이 조건 | Transition Condition | 1 | 워크플로 노드 사이의 전이 조건을 정의한다. |
| [`ad_wf_node`](ad/ad_wf_node.md) | 워크플로 노드 | Node | 262 | 워크플로의 활동·단계·프로세스를 나타내는 노드를 정의한다. |
| [`ad_wf_node_para`](ad/ad_wf_node_para.md) | 워크플로 노드 실행 인수 | Workflow Node Parameter | 1 | 워크플로 노드 실행에 사용할 매개변수를 정의한다. |
| [`ad_wf_node_trl`](ad/ad_wf_node_trl.md) | 워크플로 노드 번역 | Node Trl | 262 | 워크플로 노드 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_wf_nodenext`](ad/ad_wf_nodenext.md) | 워크플로 노드 전이 | Node Transition | 207 | 워크플로 노드 사이의 다음 단계 연결을 정의한다. |
| [`ad_wf_process`](ad/ad_wf_process.md) | 워크플로 실행 인스턴스 | Workflow Process | 11 | 실제 실행되는 워크플로 프로세스 인스턴스를 관리한다. |
| [`ad_wf_processdata`](ad/ad_wf_processdata.md) | 워크플로 실행 문맥 | Workflow Process Data | 0 | 워크플로 프로세스의 실행 문맥 데이터를 관리한다. |
| [`ad_wf_responsible`](ad/ad_wf_responsible.md) | 워크플로 책임자 | Workflow Responsible | 2 | 워크플로 실행 책임 대상을 정의한다. |
| [`ad_window`](ad/ad_window.md) | 데이터 입력·조회 창 | Window | 452 | 데이터를 입력하거나 표시하는 창을 정의한다. |
| [`ad_window_access`](ad/ad_window_access.md) | 창 접근 권한 | AD_Window_Access | 1,283 | 역할별 창 접근 및 읽기·쓰기 권한을 설정한다. |
| [`ad_window_trl`](ad/ad_window_trl.md) | 데이터 입력·조회 창 번역 | Window Trl | 452 | 데이터 입력·조회 창 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_wizardprocess`](ad/ad_wizardprocess.md) | 마법사 진행 상태 | Wizard Process | 0 | 사용자와 워크플로 노드에 연결된 마법사 상태·메모를 기록한다. |
| [`ad_wlistbox_customization`](ad/ad_wlistbox_customization.md) | 목록 위젯 개인화 | Customization of the Wlistbox | 0 | 사용자별 목록 위젯의 이름과 사용자 설정을 저장한다. |
| [`ad_workbench`](ad/ad_workbench.md) | 작업 공간 | Workbench | 1 | 창과 보고서를 묶어 작업 공간을 정의한다. |
| [`ad_workbench_trl`](ad/ad_workbench_trl.md) | 작업 공간 번역 | Workbench Trl | 1 | 작업 공간 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_workbenchwindow`](ad/ad_workbenchwindow.md) | 작업 공간 구성 항목 | Workbench Window | 2 | 작업 공간에 속한 창·폼·프로세스·작업과 표시 순서를 지정한다. |
| [`ad_workflow`](ad/ad_workflow.md) | 워크플로 정의 | Workflow | 58 | 업무 흐름과 작업 조합을 정의한다. |
| [`ad_workflow_access`](ad/ad_workflow_access.md) | 워크플로 접근 권한 | AD_Workflow_Access | 177 | 역할별 워크플로 접근 및 읽기·쓰기 권한을 설정한다. |
| [`ad_workflow_trl`](ad/ad_workflow_trl.md) | 워크플로 정의 번역 | Workflow Trl | 58 | 워크플로 정의 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_workflowprocessor`](ad/ad_workflowprocessor.md) | 워크플로 처리 서버 | Workflow Processor | 1 | 워크플로 처리 서버의 설정을 관리한다. |
| [`ad_workflowprocessorlog`](ad/ad_workflowprocessorlog.md) | 워크플로 처리 로그 | Workflow Processor Log | 0 | 워크플로 처리기의 실행 결과를 기록한다. |
| [`ad_zoomcondition`](ad/ad_zoomcondition.md) | 레코드 이동 조건 | Zoom condition | 13 | 테이블에서 특정 창으로 이동할 조건과 적용 순서를 정의한다. |
| [`asp_clientexception`](asp/asp_clientexception.md) | 테넌트별 ASP 예외 | Tenant Exception | 0 | 테넌트의 화면·탭·필드·프로세스 등 구성요소별 ASP 적용 예외 상태를 관리한다. |
| [`asp_clientlevel`](asp/asp_clientlevel.md) | 테넌트별 ASP 수준 | Tenant Level | 0 | 테넌트에 연결된 ASP 수준과 모듈을 관리한다. |
| [`asp_field`](asp/asp_field.md) | ASP 필드 설정 | ASP Field | 0 | ASP 탭에 속한 필드와 적용 상태를 관리한다. |
| [`asp_form`](asp/asp_form.md) | ASP 특수 폼 설정 | ASP Form | 0 | ASP 수준별 특수 폼과 적용 상태를 관리한다. |
| [`asp_level`](asp/asp_level.md) | ASP 제공 수준 | ASP Level | 0 | ASP 모듈에 속하는 기능 제공 수준을 정의하며 창·프로세스·워크플로 등의 ASP 설정이 참조한다. |
| [`asp_module`](asp/asp_module.md) | ASP 모듈 | ASP Module | 0 | ASP 기능 제공 설정을 묶는 모듈의 코드·이름·설명을 관리한다. |
| [`asp_process`](asp/asp_process.md) | ASP 프로세스 설정 | ASP Process | 0 | ASP 제공 수준과 애플리케이션 프로세스를 연결하고 ASP 상태를 지정한다. |
| [`asp_process_para`](asp/asp_process_para.md) | ASP 프로세스 매개변수 설정 | ASP Process Parameter | 0 | ASP 프로세스에 속한 개별 실행 매개변수의 ASP 상태를 지정한다. |
| [`asp_ref_list`](asp/asp_ref_list.md) | ASP 참조 목록 설정 | ASP_Ref_List | 0 | ASP 수준별로 참조 정의·목록 항목과 그 상태를 연결한다. |
| [`asp_tab`](asp/asp_tab.md) | ASP 화면 탭 설정 | ASP Tab | 0 | ASP 창에 속한 화면 탭의 상태와 전체 필드 적용 여부를 관리한다. |
| [`asp_task`](asp/asp_task.md) | ASP 작업 설정 | ASP Task | 0 | ASP 제공 수준과 애플리케이션 작업을 연결하고 상태를 지정한다. |
| [`asp_window`](asp/asp_window.md) | ASP 창 설정 | ASP Window | 0 | ASP 제공 수준별 애플리케이션 창과 상태를 지정하며 하위 ASP 탭 설정의 기준이 된다. |
| [`asp_workflow`](asp/asp_workflow.md) | ASP 워크플로 설정 | ASP Workflow | 0 | ASP 제공 수준과 워크플로를 연결하고 해당 상태를 관리한다. |
| [`b_bid`](b/b_bid.md) | 경매 입찰 | Bid | 0 | 경매 주제에 대한 입찰을 기록한다. 일반 구매발주와 구분되는 경매 기능의 데이터다. |
| [`b_bidcomment`](b/b_bidcomment.md) | 경매 입찰 의견 | Bid Comment | 0 | 입찰 주제에 남긴 의견을 저장한다. |
| [`b_buyer`](b/b_buyer.md) | 경매 구매 참여자 | B_Buyer | 0 | 사용자와 연결되는 경매 구매 참여자의 이름·설명·유효 종료일을 관리한다. |
| [`b_buyerfunds`](b/b_buyerfunds.md) | 경매 구매자 자금 | Buyer Funds | 0 | 주제별 입찰에 사용되는 구매자의 자금 내역을 관리한다. |
| [`b_offer`](b/b_offer.md) | 경매 제안 | Offer | 0 | 경매 주제에 대한 판매 제안을 기록한다. |
| [`b_seller`](b/b_seller.md) | 경매 판매 참여자 | B_Seller | 0 | 사용자와 연결되는 경매 판매 참여자의 정보와 내부 참여자 여부를 관리한다. |
| [`b_sellerfunds`](b/b_sellerfunds.md) | 경매 판매자 자금 | Seller Funds | 0 | 주제별 판매 제안에서 발생하는 판매자의 자금 내역을 관리한다. |
| [`b_topic`](b/b_topic.md) | 경매 주제 | Topic | 0 | 입찰과 판매 제안의 대상이 되는 경매 주제를 정의한다. |
| [`b_topiccategory`](b/b_topiccategory.md) | 경매 주제 분류 | Topic Category | 0 | 경매 주제를 분류하는 범주를 관리한다. |
| [`b_topictype`](b/b_topictype.md) | 경매 주제 유형 | Topic Type | 0 | 경매 주제의 유형을 정의한다. |
| [`c_1099box`](c/c_1099box.md) | 1099 신고 항목 | 1099 Box | 0 | 1099 신고의 기재 항목을 코드·이름과 버킷 값으로 정의한다. 구체적 신고 처리 규칙은 구조만으로 확정할 수 없다. |
| [`c_acctprocessor`](c/c_acctprocessor.md) | 회계 처리기 | Accounting Processor | 1 | 회계 처리 프로세서 또는 서버의 실행 매개변수를 관리한다. |
| [`c_acctprocessorlog`](c/c_acctprocessorlog.md) | 회계 처리 실행 로그 | Accounting Processor Log | 0 | 회계 처리기의 실행 결과를 저장하여 처리 이력과 오류 점검에 사용한다. |
| [`c_acctschema`](c/c_acctschema.md) | 회계 스키마 | Accounting Schema | 2 | 회계 처리 규칙을 정의하며 계정 구성요소와 기본 계정 설정의 상위 기준이 된다. |
| [`c_acctschema_default`](c/c_acctschema_default.md) | 회계 스키마 기본 계정 | C_AcctSchema_Default | 2 | 회계 스키마별 매출·비용·재고·채권·채무·세금 등의 업무별 기본 계정 조합을 지정한다. |
| [`c_acctschema_element`](c/c_acctschema_element.md) | 회계 스키마 구성요소 | Acct.Schema Element | 12 | 회계 스키마의 계정·조직·상품·거래처 등 분석 요소와 순서·필수 여부를 정의한다. |
| [`c_acctschema_gl`](c/c_acctschema_gl.md) | 회계 스키마 원장 계정 | C_AcctSchema_GL | 2 | 회계 스키마별 가계정·환율 균형·이익잉여금·조직 간 정산 등의 원장 처리용 계정을 지정한다. |
| [`c_activity`](c/c_activity.md) | 업무 활동 | Activity | 0 | 거래와 회계를 업무 활동별로 구분하는 기준정보를 관리한다. |
| [`c_activity_trl`](c/c_activity_trl.md) | 업무 활동 번역 | Activity Trl | 0 | 업무 활동의 언어별 표시 내용을 저장한다. |
| [`c_addresstransaction`](c/c_addresstransaction.md) | 주소 검증 이력 | Address Transaction | 0 | 검증 대상 주소와 검증 서비스·유효 판정·결과 메시지를 기록한다. |
| [`c_addressvalidation`](c/c_addressvalidation.md) | 주소 검증 서비스 연결 | Address Validation | 0 | 주소 검증 구현 설정에 연결되는 서비스 이용 설정과 연결 사용자·운송사 계정 등을 관리한다. |
| [`c_addressvalidationcfg`](c/c_addressvalidationcfg.md) | 주소 검증 구현 설정 | Address Validation Configuration | 0 | 주소 검증 클래스와 서비스 호스트·경로·프록시 연결 설정을 정의한다. |
| [`c_allocationhdr`](c/c_allocationhdr.md) | 입출금 소거 전표 | Allocation | 2 | 지급·수금과 청구서 사이의 금액 배분 및 소거 처리를 묶는 전표 머리글이다. |
| [`c_allocationline`](c/c_allocationline.md) | 입출금 소거 명세 | Allocation Line | 2 | 입출금 소거 전표에서 청구서·입출금·현금 명세를 연결하고 배분 금액·할인·상각·과부족 금액을 저장한다. |
| [`c_bank`](c/c_bank.md) | 은행 | Bank | 2 | 은행의 기준정보를 관리하며 은행계좌가 개설된 금융기관을 구분한다. |
| [`c_bankaccount`](c/c_bankaccount.md) | 은행계좌 | Bank Account | 3 | 은행에 개설된 계좌 정보를 관리하며 은행명세와 입출금 처리의 계좌 기준이 된다. |
| [`c_bankaccount_acct`](c/c_bankaccount_acct.md) | 은행계좌 회계 계정 | C_BankAccount_Acct | 6 | 은행계좌와 회계 스키마별 예금·미결제·이자·은행비용·환평가 계정 조합을 설정한다. |
| [`c_bankaccount_processor`](c/c_bankaccount_processor.md) | 은행계좌 결제 처리기 | Bank Account Processor | 2 | 은행계좌에 전자결제 처리기를 연결하고 허용 결제수단·통화·최소금액과 서비스 연결 설정을 지정한다. |
| [`c_bankaccountdoc`](c/c_bankaccountdoc.md) | 은행계좌 결제 문서 | Bank Account Document | 2 | 은행계좌의 결제 문서별 지급 방식·다음 번호·수표 인쇄 서식을 관리한다. |
| [`c_bankstatement`](c/c_bankstatement.md) | 은행거래 명세서 | Bank Statement | 2 | 은행계좌의 거래 명세서 머리글을 저장하며 개별 거래는 명세서 행에서 관리한다. |
| [`c_bankstatementline`](c/c_bankstatementline.md) | 은행거래 명세 행 | Bank statement line | 2 | 은행거래 명세서에 포함된 개별 계좌 거래를 저장한다. |
| [`c_bankstatementloader`](c/c_bankstatementloader.md) | 은행명세 가져오기 정의 | Bank Statement Loader | 0 | SWIFT·OFX 등 은행거래 명세를 가져오는 로더를 정의한다. |
| [`c_bankstatementmatcher`](c/c_bankstatementmatcher.md) | 은행명세 대조 규칙 | Bank Statement Matcher | 0 | 은행명세 정보를 거래처·청구서·입출금과 연결하는 대조 알고리즘을 정의한다. |
| [`c_banktransfer`](c/c_banktransfer.md) | 은행계좌 간 이체 | Bank Transfer | 0 | 은행계좌 간 자금 이체를 관리한다. |
| [`c_bp_bankaccount`](c/c_bp_bankaccount.md) | 거래처 은행계좌 | Partner Bank Account | 1 | 거래처의 은행계좌를 관리한다. 회사 자체 계좌 기준인 c_bankaccount와 구분한다. |
| [`c_bp_customer_acct`](c/c_bp_customer_acct.md) | 고객 회계 계정 | C_BP_Customer_Acct | 36 | 거래처와 회계 스키마별 매출채권·서비스 채권·고객 선입금 계정을 지정한다. |
| [`c_bp_edi`](c/c_bp_edi.md) | 거래처 EDI 정의 | EDI Definition | 0 | 거래처와의 전자문서 교환을 위한 EDI 정의를 관리한다. |
| [`c_bp_employee_acct`](c/c_bp_employee_acct.md) | 직원 회계 계정 | C_BP_Employee_Acct | 17 | 직원으로 취급되는 거래처의 비용 및 선급금 계정을 회계 스키마별로 지정한다. |
| [`c_bp_group`](c/c_bp_group.md) | 거래처 그룹 | Business Partner Group | 3 | 고객·공급업체 등 거래처를 공통 그룹으로 분류한다. |
| [`c_bp_group_acct`](c/c_bp_group_acct.md) | 거래처 그룹 회계 계정 | Business Partner Group Acct | 6 | 거래처 그룹과 회계 스키마별 채권·채무·선수선급·할인·미청구 관련 계정을 관리한다. |
| [`c_bp_relation`](c/c_bp_relation.md) | 거래처 간 관계 | Partner Relation | 1 | 거래처 사이의 관계를 정의한다. |
| [`c_bp_shippingacct`](c/c_bp_shippingacct.md) | 거래처 배송 계정 | Business Partner Shipping Account | 0 | 거래처 또는 거래처 주소에 배송 처리기와 운임·관세 관련 운송사 계정을 연결한다. |
| [`c_bp_vendor_acct`](c/c_bp_vendor_acct.md) | 공급업체 회계 계정 | C_BP_Vendor_Acct | 36 | 거래처와 회계 스키마별 매입채무·서비스 채무·공급업체 선급금 계정을 지정한다. |
| [`c_bp_withholding`](c/c_bp_withholding.md) | 거래처 원천징수 설정 | C_BP_Withholding | 0 | 거래처에 적용할 원천징수 유형과 의무 적용·임시 면제 여부 및 면제 사유를 관리한다. |
| [`c_bpartner`](c/c_bpartner.md) | 거래처 | Business Partner | 18 | 고객·공급업체·직원 등 업무상 거래 상대방의 공통 기준정보를 관리한다. |
| [`c_bpartner_location`](c/c_bpartner_location.md) | 거래처 주소 연결 | Partner Location | 16 | 거래처의 배송지 등 주소 용도를 관리하며 공통 주소와 거래처를 연결한다. |
| [`c_bpartner_product`](c/c_bpartner_product.md) | 거래처별 상품 정보 | Product Business Partner | 1 | 거래처와 상품별 상대방 상품번호·제조사·품질 등급·최소 잔여 유통기한 조건을 관리한다. |
| [`c_calendar`](c/c_calendar.md) | 회계 달력 | Calendar | 1 | 회계 연도와 기간을 구성하는 달력 기준정보를 관리한다. |
| [`c_campaign`](c/c_campaign.md) | 마케팅 캠페인 | Campaign | 2 | 마케팅 캠페인을 정의하고 관련 영업 및 거래를 캠페인별로 구분한다. |
| [`c_campaign_trl`](c/c_campaign_trl.md) | 마케팅 캠페인 번역 | Campaign Trl | 2 | 마케팅 캠페인의 언어별 표시 내용을 저장한다. |
| [`c_cash`](c/c_cash.md) | 현금 출납 전표 | Cash Journal | 3 | 현금 출납 내역을 묶는 현금 일지의 머리글을 관리한다. |
| [`c_cashbook`](c/c_cashbook.md) | 소액현금 출납장 | Cash Book | 2 | 소액현금 거래를 기록하는 출납장의 기준정보를 관리한다. |
| [`c_cashbook_acct`](c/c_cashbook_acct.md) | 현금 출납장 회계 계정 | C_CashBook_Acct | 4 | 출납장과 회계 스키마별 현금자산·이체·차이·비용·수입 계정을 설정한다. |
| [`c_cashline`](c/c_cashline.md) | 현금 출납 명세 | Cash Journal Line | 5 | 현금 출납 전표의 개별 현금 거래를 저장한다. |
| [`c_cashplan`](c/c_cashplan.md) | 자금 계획 | Cash Plan | 0 | 예상 자금 흐름을 계획 단위로 묶어 관리한다. |
| [`c_cashplanline`](c/c_cashplanline.md) | 자금 계획 명세 | Cash Plan Line | 0 | 자금 계획의 개별 예상 자금 내역을 관리한다. |
| [`c_channel`](c/c_channel.md) | 판매 채널 | Channel | 2 | 판매 경로를 구분하는 채널 기준정보를 관리한다. |
| [`c_charge`](c/c_charge.md) | 부대 수익·비용 항목 | Charge | 3 | 거래 문서에 추가되는 요금이나 부대 수익·비용 항목을 정의한다. |
| [`c_charge_acct`](c/c_charge_acct.md) | 부대 항목 회계 계정 | C_Charge_Acct | 6 | 부대 항목과 회계 스키마별 수익 및 비용 계정을 지정한다. |
| [`c_charge_trl`](c/c_charge_trl.md) | 부대 항목 번역 | Charge Trl | 3 | 부대 수익·비용 항목의 언어별 표시 내용을 저장한다. |
| [`c_chargetype`](c/c_chargetype.md) | 부대 항목 유형 | Charge Type | 0 | 부대 수익·비용 항목을 유형별로 분류하는 기준을 관리한다. |
| [`c_chargetype_doctype`](c/c_chargetype_doctype.md) | 문서 유형별 부대 항목 유형 | Charge Type by Doc Type | 0 | 문서 유형별로 사용할 수 있는 부대 수익·비용 항목 유형을 연결한다. |
| [`c_city`](c/c_city.md) | 도시 | City | 1 | 주소에 사용하는 도시 기준정보를 관리한다. |
| [`c_commission`](c/c_commission.md) | 판매 수수료 규칙 | Commission | 1 | 판매 수수료의 산정 기준을 정의하고 세부 조건과 계산 실행 결과를 연결한다. |
| [`c_commissionamt`](c/c_commissionamt.md) | 판매 수수료 계산 금액 | Commission Amount | 0 | 수수료 계산 실행에서 산출된 금액을 저장한다. |
| [`c_commissiondetail`](c/c_commissiondetail.md) | 판매 수수료 산출 근거 | Commission Detail | 0 | 계산된 수수료 금액을 뒷받침하는 상세 근거를 저장한다. |
| [`c_commissionline`](c/c_commissionline.md) | 판매 수수료 세부 규칙 | Commission Line | 1 | 상품·거래처·영업지역 등의 적용 범위와 금액·수량의 차감값 및 배수를 지정한다. |
| [`c_commissionrun`](c/c_commissionrun.md) | 판매 수수료 계산 실행 | Commission Run | 0 | 판매 수수료의 계산 실행 단위를 관리하고 계산 금액과 근거 상세를 실행별로 묶는다. |
| [`c_contactactivity`](c/c_contactactivity.md) | 연락처 활동 | Contact Activity | 0 | 연락처와 관련된 이벤트·업무·의사소통 내역을 기록한다. |
| [`c_conversion_rate`](c/c_conversion_rate.md) | 환율 | Conversion Rate | 4 | 통화 간 금액 변환에 사용하는 환율을 관리한다. |
| [`c_conversiontype`](c/c_conversiontype.md) | 환율 유형 | Currency Type | 4 | 통화 환산에 사용할 환율의 유형을 정의한다. |
| [`c_costcenter`](c/c_costcenter.md) | 원가 중심점 | Cost Center | 0 | 비용 귀속 단위로 참조하는 원가 중심점의 코드와 이름을 관리한다. |
| [`c_country`](c/c_country.md) | 국가 | Country | 251 | 주소와 지역 구분에 사용하는 국가 기준정보를 관리한다. |
| [`c_country_trl`](c/c_country_trl.md) | 국가 번역 | Country Trl | 251 | 국가의 언어별 표시 내용을 저장한다. |
| [`c_countrygroup`](c/c_countrygroup.md) | 국가 그룹 | Country Group | 0 | 조세 협정 등 공통 조건을 공유하는 국가 집합을 정의한다. |
| [`c_countrygroup_trl`](c/c_countrygroup_trl.md) | 국가 그룹 번역 | Country Group Trl | 0 | 국가 그룹의 이름과 설명을 언어별로 저장한다. |
| [`c_countrygroupcountry`](c/c_countrygroupcountry.md) | 국가 그룹 소속 국가 | Country on Country Group | 0 | 국가와 국가 그룹의 소속 관계 및 적용 시작·종료일을 관리한다. |
| [`c_currency`](c/c_currency.md) | 통화 | Currency | 175 | 거래와 회계 금액을 표시하는 통화의 기준정보를 관리한다. |
| [`c_currency_acct`](c/c_currency_acct.md) | 통화 환차손익 계정 | C_Currency_Acct | 0 | 통화와 회계 스키마별 실현·미실현 환차익 및 환차손 계정을 지정한다. |
| [`c_currency_trl`](c/c_currency_trl.md) | 통화 번역 | Currency Trl | 175 | 통화의 언어별 표시 내용을 저장한다. |
| [`c_cycle`](c/c_cycle.md) | 프로젝트 보고 주기 | Project Cycle | 2 | 프로젝트 보고에 사용할 주기 또는 단계 체계를 정의한다. |
| [`c_cyclephase`](c/c_cyclephase.md) | 보고 주기 단계 연결 | C_CyclePhase | 10 | 프로젝트 보고 주기의 세부 단계와 표준 프로젝트 단계를 연결한다. |
| [`c_cyclestep`](c/c_cyclestep.md) | 프로젝트 보고 주기 세부 단계 | Cycle Step | 4 | 프로젝트 보고 주기 안의 개별 단계를 정의한다. |
| [`c_department`](c/c_department.md) | 부서 | Department | 0 | 거래·회계 분석에서 참조하는 부서의 코드와 이름을 관리한다. 급여 부서 hr_department와 별도 기준정보다. |
| [`c_depositbatch`](c/c_depositbatch.md) | 일괄 입금 전표 | Deposit Batch | 0 | 여러 입출금 기록을 은행계좌 입금 단위로 묶고 입금일·통화·합계금액과 문서 상태를 관리한다. |
| [`c_depositbatchline`](c/c_depositbatchline.md) | 일괄 입금 명세 | Deposit Batch Line | 0 | 일괄 입금 전표에 포함되는 입출금 기록과 해당 금액을 행 단위로 저장한다. |
| [`c_docbasegroup`](c/c_docbasegroup.md) | 문서 기본 유형 그룹 | Document Base Type Group | 0 | 회계 기간 통제에 사용할 문서 기본 유형의 그룹을 정의한다. |
| [`c_docbasegroupline`](c/c_docbasegroupline.md) | 문서 기본 유형 그룹 명세 | Document Base Type Group Line | 0 | 문서 기본 유형 그룹에 포함되는 항목을 관리한다. |
| [`c_doctype`](c/c_doctype.md) | 문서 유형 | Document Type | 52 | 업무 문서의 유형과 처리 규칙을 정의한다. |
| [`c_doctype_trl`](c/c_doctype_trl.md) | 문서 유형 번역 | Document Type Trl | 52 | 문서 유형의 언어별 표시 내용을 저장한다. |
| [`c_doctypecounter`](c/c_doctypecounter.md) | 대응 문서 관계 | Counter Document | 1 | 원 문서와 그에 대응하는 문서 유형의 관계를 정의한다. |
| [`c_dunning`](c/c_dunning.md) | 연체 독촉 규칙 | Dunning | 2 | 지급 기한이 지난 청구서에 적용할 독촉 규칙을 관리한다. |
| [`c_dunninglevel`](c/c_dunninglevel.md) | 연체 독촉 단계 | Dunning Level | 2 | 독촉 규칙별 연체 일수·독촉 간격·이자·수수료·인쇄 문구와 신용 중지 조건 등을 정의한다. |
| [`c_dunninglevel_trl`](c/c_dunninglevel_trl.md) | 연체 독촉 단계 번역 | Dunning Level Trl | 2 | 독촉 단계의 인쇄 명칭과 안내 문구를 언어별로 저장한다. |
| [`c_dunningrun`](c/c_dunningrun.md) | 연체 독촉 실행 | Dunning Run | 0 | 독촉 대상 선정과 문서 생성 등을 묶는 독촉 실행 단위를 관리한다. |
| [`c_dunningrunentry`](c/c_dunningrunentry.md) | 연체 독촉 실행 대상 | Dunning Run Entry | 0 | 독촉 실행에서 거래처·주소·담당 연락처별 독촉 금액과 단계 및 안내 문구를 묶는다. |
| [`c_dunningrunline`](c/c_dunningrunline.md) | 연체 독촉 실행 명세 | Dunning Run Line | 0 | 독촉 대상의 청구서·입출금별 미결제액·연체 일수·독촉 횟수·이자·수수료를 기록한다. |
| [`c_element`](c/c_element.md) | 계정 요소 체계 | Element | 1 | 회계 계정 요소의 체계를 정의하며 개별 요소 값의 상위 기준이 된다. |
| [`c_elementvalue`](c/c_elementvalue.md) | 계정 요소 값 | Account Element | 379 | 계정 요소 체계의 개별 값 또는 계정과목을 관리한다. |
| [`c_elementvalue_trl`](c/c_elementvalue_trl.md) | 계정 요소 값 번역 | Account Element Trl | 379 | 개별 계정 요소 값의 언어별 표시 내용을 저장한다. |
| [`c_greeting`](c/c_greeting.md) | 서신 인사말 | Greeting | 1 | 서신 등에 인쇄할 호칭이나 인사말을 정의한다. |
| [`c_greeting_trl`](c/c_greeting_trl.md) | 서신 인사말 번역 | Greeting Trl | 1 | 인쇄용 호칭·인사말의 언어별 표현을 저장한다. |
| [`c_interorg_acct`](c/c_interorg_acct.md) | 조직 간 정산 계정 | C_InterOrg_Acct | 0 | 회계 스키마와 송수신 조직 조합별 조직 간 지급·수취 계정을 지정한다. |
| [`c_invoice`](c/c_invoice.md) | 매출·매입 청구서 | Invoice | 8 | 고객 매출 청구와 공급업체 매입 청구의 머리글을 저장하며 문서 유형에 따라 신용전표도 포함한다. 판매·구매 구분, 거래처, 청구일, 통화, 합계 및 지급 상태를 관리하므로 금액 분석 시 문서 유형과 취소 관계를 함께 확인한다. |
| [`c_invoicebatch`](c/c_invoicebatch.md) | 비용 청구 일괄 입력 | Invoice Batch | 0 | 비용 청구서를 일괄 입력·처리하는 배치의 머리글을 관리한다. |
| [`c_invoicebatchline`](c/c_invoicebatchline.md) | 비용 청구 일괄 입력 명세 | Invoice Batch Line | 0 | 비용 청구 배치에 포함된 개별 입력 행을 관리한다. |
| [`c_invoiceline`](c/c_invoiceline.md) | 매출·매입 청구 명세 | Invoice Line | 24 | 청구서의 개별 상품·서비스 등 상세 행을 저장한다. 상위 청구서가 판매·구매 또는 신용전표인지 함께 확인해야 한다. |
| [`c_invoicepayschedule`](c/c_invoicepayschedule.md) | 청구서 지급 일정 | Invoice Payment Schedule | 2 | 청구서별 지급 예정 일정과 분할 납부 내역을 관리한다. |
| [`c_invoiceschedule`](c/c_invoiceschedule.md) | 청구서 생성 일정 | Invoice Schedule | 1 | 청구서를 생성할 시점과 일정 규칙을 정의한다. |
| [`c_invoicetax`](c/c_invoicetax.md) | 청구서 세금 집계 | C_InvoiceTax | 8 | 청구서와 세금별 과세표준·세액·세금 포함 여부 및 세금 계산 제공자를 저장한다. |
| [`c_job`](c/c_job.md) | 직위 | Position | 4 | 직위의 명칭·분류와 직원용 여부를 정의하며 사용자 배치와 보수 설정에서 참조한다. |
| [`c_jobassignment`](c/c_jobassignment.md) | 사용자 직위 배치 | Position Assignment | 0 | 사용자를 직위에 배치하고 배치의 유효 기간을 관리한다. |
| [`c_jobcategory`](c/c_jobcategory.md) | 직위 분류 | Position Category | 4 | 직위를 묶는 분류의 이름·설명·도움말을 관리한다. |
| [`c_jobremuneration`](c/c_jobremuneration.md) | 직위 보수 연결 | Position Remuneration | 0 | 직위에 보수 기준을 연결하고 유효 기간을 지정한다. |
| [`c_landedcost`](c/c_landedcost.md) | 취득 부대원가 배부 설정 | Landed Cost | 0 | 청구 명세의 운송비 등 취득 부대원가를 입고·상품에 연결하고 원가 요소와 배부 기준을 지정한다. |
| [`c_landedcostallocation`](c/c_landedcostallocation.md) | 취득 부대원가 배부 결과 | Landed Cost Allocation | 0 | 청구 명세의 부대원가를 상품·입출고 명세·속성 인스턴스별로 배부한 금액과 수량·기준값을 저장한다. |
| [`c_location`](c/c_location.md) | 주소 | Address | 34 | 국가·지역·도시·우편번호 등을 포함하는 공통 주소 정보를 관리한다. |
| [`c_nonbusinessday`](c/c_nonbusinessday.md) | 비영업일 | Non Business Day | 1 | 업무를 수행하지 않는 날짜를 관리한다. |
| [`c_onlinetrxhistory`](c/c_onlinetrxhistory.md) | 온라인 처리 이력 | Online Transaction History | 0 | 대상 테이블과 레코드의 온라인 처리 메시지·오류 여부·처리 상태를 기록한다. |
| [`c_opportunity`](c/c_opportunity.md) | 영업 기회 | Sales Opportunity | 0 | 거래처별 영업 기회의 예상 금액·영업 단계·성사 확률·예상 종료일과 연결 주문을 관리한다. |
| [`c_order`](c/c_order.md) | 판매 주문·구매 발주 | Order | 8 | 판매 주문과 구매 발주의 머리글을 함께 저장한다. 판매·구매 구분, 문서 유형, 거래처, 주문일, 창고, 통화 및 납품·청구 상태를 확인하여 조회 범위를 결정한다. |
| [`c_orderlandedcost`](c/c_orderlandedcost.md) | 구매 발주 예상 부대원가 | Estimated Landed Cost | 0 | 구매 발주에 대한 예상 취득 부대원가를 관리한다. |
| [`c_orderlandedcostallocation`](c/c_orderlandedcostallocation.md) | 발주 예상 부대원가 배부 | Estimated Landed Cost Allocation | 0 | 주문·발주 명세에 예상 취득 부대원가를 배부한 내역을 관리한다. |
| [`c_orderline`](c/c_orderline.md) | 판매 주문·구매 발주 명세 | Sales Order Line | 27 | 주문·발주에 포함된 개별 상품 등의 상세 행을 관리한다. 사전명은 Sales Order Line이지만 상위 c_order의 판매·구매 구분에 따라 해석해야 한다. |
| [`c_orderpayschedule`](c/c_orderpayschedule.md) | 주문·발주 지급 일정 | Order Payment Schedule | 0 | 주문·발주별 지급 예정 일정을 관리한다. |
| [`c_ordersource`](c/c_ordersource.md) | 주문 유입 경로 | Order Source | 0 | 주문이 들어온 경로를 구분하는 코드·이름·설명을 관리한다. |
| [`c_ordertax`](c/c_ordertax.md) | 주문·발주 세금 집계 | Order Tax | 8 | 주문·발주와 세금별 과세표준·세액·세금 포함 여부 및 세금 계산 제공자를 저장한다. |
| [`c_orgassignment`](c/c_orgassignment.md) | 거래 조직 배정 | Org Assignment | 0 | 사용자를 거래 조직에 배정하고 배정의 유효 시작·종료일을 관리한다. |
| [`c_payment`](c/c_payment.md) | 수금·지급 전표 | Payment | 2 | 고객 수금과 공급업체 등에 대한 지급을 함께 저장하며 isreceipt로 입출금 방향을 구분한다. 은행계좌·거래처·청구서·금액·결제수단 및 소거·대사 상태를 관리한다. |
| [`c_paymentallocate`](c/c_paymentallocate.md) | 입출금의 청구서 배분 | Allocate Payment | 0 | 입출금을 청구서에 배분하고 배분 금액·할인·상각·과부족 금액 및 소거 명세 연결을 관리한다. |
| [`c_paymentbatch`](c/c_paymentbatch.md) | 전자 자금이체 배치 | Payment Batch | 0 | 전자 자금이체(EFT)를 위한 입출금 건을 배치로 묶는다. |
| [`c_paymentprocessor`](c/c_paymentprocessor.md) | 전자결제 처리기 | Payment Processor | 2 | 전자결제를 처리하는 서비스 또는 처리기의 설정을 관리한다. |
| [`c_paymentterm`](c/c_paymentterm.md) | 지급 조건 | Payment Term | 5 | 거래에 적용할 지급 시점과 할인 등의 조건을 정의한다. |
| [`c_paymentterm_trl`](c/c_paymentterm_trl.md) | 지급 조건 번역 | Payment Term Trl | 5 | 지급 시점·할인 조건의 언어별 표시 내용을 저장한다. |
| [`c_paymenttransaction`](c/c_paymenttransaction.md) | 결제 거래 | Payment Transaction | 0 | 전자결제 등의 개별 거래에서 결제수단·금액·처리기·승인 및 취소 결과와 연결 입출금 전표를 기록한다. |
| [`c_payschedule`](c/c_payschedule.md) | 지급 일정 서식 | Payment Schedule | 2 | 분할 지급 등의 일정 생성에 사용할 기준 서식을 정의한다. |
| [`c_payselection`](c/c_payselection.md) | 지급 대상 선정 | Payment Selection | 1 | 지급 대상으로 선택한 내역을 묶는 상위 단위를 관리한다. |
| [`c_payselectioncheck`](c/c_payselectioncheck.md) | 선정 지급 수표 | Pay Selection Check | 1 | 지급 대상 선정에서 생성·관리되는 수표 단위 정보를 저장한다. |
| [`c_payselectionline`](c/c_payselectionline.md) | 지급 대상 선정 명세 | Payment Selection Line | 1 | 지급 대상 선정에 포함되는 개별 지급 예정 내역을 저장한다. |
| [`c_period`](c/c_period.md) | 회계 기간 | Period | 360 | 회계 달력 안의 개별 기간을 관리한다. |
| [`c_periodcontrol`](c/c_periodcontrol.md) | 회계 기간 통제 | Period Control | 10,464 | 회계 기간과 문서 기본 유형별 개방·마감 상태 및 상태 변경 동작을 관리한다. |
| [`c_phase`](c/c_phase.md) | 프로젝트 표준 단계 | Standard Phase | 13 | 프로젝트 유형에 정의된 표준 단계를 관리한다. |
| [`c_pos`](c/c_pos.md) | 판매시점 단말기 | POS Terminal | 1 | 매장 판매에 사용하는 POS 단말기의 기준정보를 관리한다. |
| [`c_poskey`](c/c_poskey.md) | POS 기능 키 | POS Key | 163 | POS 화면에서 사용할 개별 기능 키를 정의한다. |
| [`c_poskeylayout`](c/c_poskeylayout.md) | POS 키 배치 | POS Key Layout | 5 | POS 기능 키의 배치 구성을 정의한다. |
| [`c_pospayment`](c/c_pospayment.md) | POS 결제 내역 | POS Payment | 0 | POS 주문의 결제수단별 금액과 수표·카드 관련 정보 및 연결 입출금 전표를 저장한다. |
| [`c_postendertype`](c/c_postendertype.md) | POS 결제수단 유형 | POS Tender Type | 0 | POS 결제수단의 코드·이름·기본 수단 및 보증·후일자 여부를 정의한다. |
| [`c_project`](c/c_project.md) | 프로젝트 | Project | 2 | 재무 관리 대상 프로젝트를 정의하며 단계·작업·투입·회계 내역을 프로젝트별로 연결한다. |
| [`c_project_acct`](c/c_project_acct.md) | 프로젝트 회계 계정 | C_Project_Acct | 4 | 프로젝트와 회계 스키마별 프로젝트 자산 및 진행 중 원가 계정을 지정한다. |
| [`c_projectissue`](c/c_projectissue.md) | 프로젝트 자재·노무 투입 | Project Issue | 0 | 프로젝트에 투입되는 자재와 노무 등의 사용 내역을 관리한다. |
| [`c_projectissuema`](c/c_projectissuema.md) | 프로젝트 투입 속성 배분 | C_ProjectIssueMA | 0 | 프로젝트 투입 건의 이동 수량을 상품 속성 인스턴스별로 나누어 기록한다. |
| [`c_projectline`](c/c_projectline.md) | 프로젝트 명세 | Project Line | 1 | 프로젝트의 과업 또는 수행 단계를 명세 행으로 관리한다. |
| [`c_projectphase`](c/c_projectphase.md) | 프로젝트 단계 | Project Phase | 0 | 개별 프로젝트에 실제로 적용되는 단계를 관리한다. |
| [`c_projecttask`](c/c_projecttask.md) | 프로젝트 작업 | Project Task | 0 | 프로젝트 단계 안에서 수행하는 실제 작업을 관리한다. |
| [`c_projecttype`](c/c_projecttype.md) | 프로젝트 유형 | Project Type | 4 | 프로젝트 유형과 표준 구성의 기준을 관리한다. |
| [`c_recurring`](c/c_recurring.md) | 반복 문서 정의 | Recurring | 1 | 반복적으로 생성할 업무 문서를 정의한다. |
| [`c_recurring_run`](c/c_recurring_run.md) | 반복 문서 실행 이력 | Recurring Run | 0 | 반복 문서 정의에 따른 실행 내역을 기록한다. |
| [`c_recurringgroup`](c/c_recurringgroup.md) | 반복 문서 그룹 | Recurring Group | 0 | 반복 문서 정의를 분류할 그룹의 코드·이름·설명을 관리한다. |
| [`c_region`](c/c_region.md) | 행정 지역 | Region | 399 | 주소에 사용하는 지리적 지역 기준정보를 관리한다. |
| [`c_region_trl`](c/c_region_trl.md) | 행정 지역 번역 | Region | 399 | 행정 지역의 언어별 표시 내용을 저장한다. |
| [`c_remuneration`](c/c_remuneration.md) | 보수 기준 | Remuneration | 0 | 보수 유형·표준 근무시간·기본 보수 및 초과근무 보수와 비용 기준을 정의한다. |
| [`c_revenuerecog_service`](c/c_revenuerecog_service.md) | 서비스 수익 인식 계획 | Revenue Recognition Service | 0 | 서비스를 기준으로 수익을 인식하거나 기록하는 계획을 관리한다. |
| [`c_revenuerecognition`](c/c_revenuerecognition.md) | 수익 인식 방식 | Revenue Recognition | 2 | 수익을 기록하는 인식 방법을 정의한다. |
| [`c_revenuerecognition_plan`](c/c_revenuerecognition_plan.md) | 수익 인식 계획 | Revenue Recognition Plan | 0 | 정의된 방식에 따라 수익을 인식하거나 기록할 계획을 관리한다. |
| [`c_revenuerecognition_run`](c/c_revenuerecognition_run.md) | 수익 인식 실행 | Revenue Recognition Run | 0 | 수익 인식 계획의 실행 내역을 관리한다. |
| [`c_rfq`](c/c_rfq.md) | 견적 요청 | RfQ | 1 | 잠재 공급업체에 제시할 견적 요청의 머리글을 관리한다. |
| [`c_rfq_topic`](c/c_rfq_topic.md) | 견적 요청 주제 | RfQ Topic | 1 | 견적 요청의 대상 주제를 정의한다. |
| [`c_rfq_topicsubscriber`](c/c_rfq_topicsubscriber.md) | 견적 요청 주제 참여자 | RfQ Subscriber | 2 | 견적 요청 주제의 참여자 또는 구독 대상을 관리한다. |
| [`c_rfq_topicsubscriberonly`](c/c_rfq_topicsubscriberonly.md) | 견적 요청 참여 범위 제한 | RfQ Topic Subscriber Restriction | 0 | 참여자가 특정 상품 또는 상품 분류의 견적 요청에만 포함되도록 제한한다. |
| [`c_rfqline`](c/c_rfqline.md) | 견적 요청 명세 | RfQ Line | 2 | 견적 요청에 포함되는 개별 항목을 관리한다. |
| [`c_rfqlineqty`](c/c_rfqlineqty.md) | 견적 요청 수량 조건 | RfQ Line Quantity | 2 | 견적 요청 명세별 수량 조건을 관리한다. |
| [`c_rfqresponse`](c/c_rfqresponse.md) | 공급업체 견적 응답 | RfQ Response | 0 | 잠재 공급업체의 견적 응답을 저장하며 제안 금액·납기·순위·선정 여부 및 연결 주문을 관리한다. |
| [`c_rfqresponseline`](c/c_rfqresponseline.md) | 공급업체 견적 응답 명세 | RfQ Response Line | 0 | 공급업체 견적 응답의 개별 요청 항목별 내용을 저장한다. |
| [`c_rfqresponselineqty`](c/c_rfqresponselineqty.md) | 견적 응답 수량 조건 | RfQ Response Line Qty | 0 | 공급업체 견적 응답 명세의 수량별 제안 내용을 저장한다. |
| [`c_salesregion`](c/c_salesregion.md) | 영업 지역 | Sales Region | 2 | 영업 활동의 담당 또는 적용 지역을 정의한다. |
| [`c_salesregion_trl`](c/c_salesregion_trl.md) | 영업 지역 번역 | Sales Region Trl | 2 | 영업 지역의 언어별 표시 내용을 저장한다. |
| [`c_salesstage`](c/c_salesstage.md) | 영업 단계 | Sales Stage | 0 | 영업 프로세스가 거쳐 가는 단계를 정의한다. |
| [`c_salesstage_trl`](c/c_salesstage_trl.md) | 영업 단계 번역 | Sales Stage Trl | 0 | 영업 프로세스 단계의 언어별 표시 내용을 저장한다. |
| [`c_servicelevel`](c/c_servicelevel.md) | 서비스 이행 수준 | Service Level | 0 | 상품과 수익 인식 계획별 서비스 제공 수준 및 청구된 수준을 관리한다. |
| [`c_servicelevelline`](c/c_servicelevelline.md) | 서비스 이행 수준 명세 | Service Level Line | 0 | 서비스 이행 수준에 속하는 일자별 제공 수준과 설명을 기록한다. |
| [`c_subacct`](c/c_subacct.md) | 보조 계정 | Sub Account | 0 | 계정 요소 값에 속하는 하위 보조 계정을 정의한다. |
| [`c_subscription`](c/c_subscription.md) | 상품 구독 | Subscription | 0 | 거래처가 갱신하여 이용하는 상품 구독을 관리한다. |
| [`c_subscription_delivery`](c/c_subscription_delivery.md) | 구독 제공 이력 | Subscription Delivery | 0 | 구독에 대한 선택적인 배송·제공 기록을 저장한다. |
| [`c_subscriptiontype`](c/c_subscriptiontype.md) | 구독 유형 | Subscription Type | 0 | 상품 구독의 유형을 정의한다. |
| [`c_task`](c/c_task.md) | 프로젝트 표준 작업 | Standard Task | 9 | 프로젝트 유형에서 사용할 표준 작업을 정의한다. |
| [`c_tax`](c/c_tax.md) | 세금 | Tax | 6 | 거래에서 적용하는 세금의 기준정보를 관리한다. |
| [`c_tax_acct`](c/c_tax_acct.md) | 세금 회계 계정 | C_Tax_Acct | 12 | 세금과 회계 스키마별 납부·채무·공제·미수·비용 계정을 지정한다. |
| [`c_tax_trl`](c/c_tax_trl.md) | 세금 번역 | Tax Trl | 6 | 세금의 언어별 표시 내용을 저장한다. |
| [`c_taxbase`](c/c_taxbase.md) | 과세 기준 | Tax Base | 0 | 세액 계산에 사용하는 기준값과 적용 비율을 코드·이름으로 정의한다. |
| [`c_taxcategory`](c/c_taxcategory.md) | 세금 분류 | Tax Category | 1 | 세금 적용을 구분하는 분류를 정의한다. |
| [`c_taxcategory_trl`](c/c_taxcategory_trl.md) | 세금 분류 번역 | Tax Category Trl | 1 | 세금 분류의 언어별 표시 내용을 저장한다. |
| [`c_taxdeclaration`](c/c_taxdeclaration.md) | 세금 신고 | Tax Declaration | 0 | 세무 당국 신고 내용을 묶고 관련 문서와 회계 기록 대사의 기준을 관리한다. |
| [`c_taxdeclarationacct`](c/c_taxdeclarationacct.md) | 세금 신고 회계 대사 | Tax Declaration Accounting | 0 | 세금 신고 관련 수익·비용·세금 회계 내역을 모아 문서와 대사하고 상세 보고의 근거로 사용한다. |
| [`c_taxdeclarationline`](c/c_taxdeclarationline.md) | 세금 신고 문서 명세 | Tax Declaration Line | 0 | 생성 처리로 수집된 신고 대상 문서를 저장한다. 특정 신고에 포함하지 않을 행은 제외할 수 있다. |
| [`c_taxdefinition`](c/c_taxdefinition.md) | 세금 적용 규칙 | Tax Definition | 0 | 거래처·상품·조직 유형·과세 범위·유효 기간 등의 조건에 따른 세금과 과세 기준을 정의한다. |
| [`c_taxgroup`](c/c_taxgroup.md) | 세금 그룹 | Tax Group | 0 | 관련 세금을 묶는 그룹 기준정보를 관리한다. |
| [`c_taxpostal`](c/c_taxpostal.md) | 우편번호별 세금 범위 | Tax ZIP | 0 | 세금 적용 지역을 우편번호 기준으로 관리한다. |
| [`c_taxprovider`](c/c_taxprovider.md) | 세금 계산 서비스 연결 | Tax Provider | 0 | 세금 계산 서비스의 회사·계정·이용 설정과 처리 순서를 구현 설정에 연결한다. |
| [`c_taxprovidercfg`](c/c_taxprovidercfg.md) | 세금 계산 구현 설정 | Tax Provider Configuration | 0 | 세금 계산 제공자의 구현 클래스와 서비스 URL 등 공통 설정을 정의한다. |
| [`c_taxtype`](c/c_taxtype.md) | 세금 유형 | Tax Type | 0 | 세금 규칙에서 참조하는 유형의 코드·이름·설명을 관리한다. |
| [`c_uom`](c/c_uom.md) | 측정 단위 | UOM | 15 | 상품과 거래 수량을 표현하는 측정 단위를 정의한다. |
| [`c_uom_conversion`](c/c_uom_conversion.md) | 단위 환산 | UOM Conversion | 1 | 측정 단위 사이의 수량 환산 관계를 관리한다. |
| [`c_uom_trl`](c/c_uom_trl.md) | 측정 단위 번역 | UOM Trl | 15 | 측정 단위의 언어별 표시 내용을 저장한다. |
| [`c_userremuneration`](c/c_userremuneration.md) | 직원별 보수 조정 | Employee Remuneration | 0 | 직원 임금이나 급여의 개별 보수 재정의 값을 관리한다. |
| [`c_validcombination`](c/c_validcombination.md) | 유효 계정 조합 | Combination | 157 | 회계에서 사용할 유효한 계정 및 분석 요소 조합을 관리한다. |
| [`c_withholding`](c/c_withholding.md) | 원천징수 유형 | Withholding | 0 | 거래에서 적용할 원천징수 유형을 정의한다. |
| [`c_withholding_acct`](c/c_withholding_acct.md) | 원천징수 회계 계정 | C_Withholding_Acct | 0 | 원천징수 유형과 회계 스키마별 원천징수 계정을 지정한다. |
| [`c_year`](c/c_year.md) | 회계 연도 | Year | 30 | 회계 달력에 속하는 연도를 관리한다. |
| [`cm_accesscontainer`](cm/cm_accesscontainer.md) | 웹 콘텐츠 접근 연결 | Web Access Container | 0 | 웹 접근 프로필과 공개 콘텐츠 컨테이너를 연결한다. |
| [`cm_accesslistbpgroup`](cm/cm_accesslistbpgroup.md) | 웹 접근 거래처 그룹 | Web Access BP Group | 0 | 웹 접근 프로필에 거래처 그룹을 연결한다. |
| [`cm_accesslistrole`](cm/cm_accesslistrole.md) | 웹 접근 역할 | Web Access Role | 0 | 웹 접근 프로필에 애플리케이션 역할을 연결한다. |
| [`cm_accessmedia`](cm/cm_accessmedia.md) | 웹 미디어 접근 연결 | Web Access Media | 0 | 웹 접근 프로필과 미디어 항목을 연결한다. |
| [`cm_accessnewschannel`](cm/cm_accessnewschannel.md) | 뉴스 채널 접근 연결 | Web Access NewsChannel | 0 | 웹 접근 프로필과 뉴스 채널을 연결한다. |
| [`cm_accessprofile`](cm/cm_accessprofile.md) | 웹 접근 프로필 | Web Access Profile | 0 | 웹 콘텐츠 접근 제어를 위한 프로필을 정의한다. |
| [`cm_accessstage`](cm/cm_accessstage.md) | 준비 콘텐츠 접근 연결 | Web Access Stage | 0 | 웹 접근 프로필과 게시 준비 단계의 콘텐츠 컨테이너를 연결한다. |
| [`cm_ad`](cm/cm_ad.md) | 웹 광고 | Advertisement | 0 | 배너·제휴 정보·후원 링크 등 웹에 표시할 광고를 관리한다. |
| [`cm_ad_cat`](cm/cm_ad_cat.md) | 웹 광고 분류 | Advertisement Category | 0 | 광고 블록과 순환 표시 대상을 묶는 광고 분류를 정의한다. |
| [`cm_broadcastserver`](cm/cm_broadcastserver.md) | 웹 배포 서버 | Broadcast Server | 0 | 웹 콘텐츠 방송·배포에 사용하는 서버를 관리한다. |
| [`cm_chat`](cm/cm_chat.md) | 레코드 대화 | Chat | 0 | 대상 테이블과 레코드에 연결되는 대화 공간의 유형·공개 범위·검토 방식을 관리한다. |
| [`cm_chatentry`](cm/cm_chatentry.md) | 대화 메시지 | Chat Entry | 0 | 대화 공간의 본문·작성 사용자·제목·검토 상태와 상위 메시지 관계를 저장한다. |
| [`cm_chattype`](cm/cm_chattype.md) | 대화 유형 | Chat Type | 0 | 대화를 연결할 테이블과 검토 방식을 포함한 대화 유형을 정의한다. |
| [`cm_chattypeupdate`](cm/cm_chattypeupdate.md) | 대화 유형별 사용자 연결 | Chat Type Update | 0 | 대화 유형과 사용자의 업데이트 관련 연결 및 셀프서비스 여부를 관리한다. 실제 알림 동작은 처리 코드 확인이 필요하다. |
| [`cm_chatupdate`](cm/cm_chatupdate.md) | 대화별 사용자 연결 | Chat Update | 0 | 개별 대화와 사용자의 업데이트 관련 연결 및 셀프서비스 여부를 관리한다. 알림 방식은 구조만으로 단정하지 않는다. |
| [`cm_container`](cm/cm_container.md) | 웹 콘텐츠 컨테이너 | Web Container | 5 | 이미지·텍스트 등의 웹 콘텐츠를 담는 단위로 표시·색인·저장 방식을 정의한다. |
| [`cm_container_element`](cm/cm_container_element.md) | 웹 콘텐츠 요소 | Container Element | 6 | 제목·본문·꼬리말처럼 컨테이너를 구성하는 작은 콘텐츠 단위를 저장한다. |
| [`cm_container_element_trl`](cm/cm_container_element_trl.md) | 웹 콘텐츠 요소 번역 | Container Element Trl | 6 | 컨테이너의 제목·본문 등 개별 콘텐츠 요소 번역을 저장한다. |
| [`cm_container_trl`](cm/cm_container_trl.md) | 웹 콘텐츠 번역 | Web Container Trl | 5 | 웹 콘텐츠 컨테이너의 번역 내용을 저장한다. |
| [`cm_container_url`](cm/cm_container_url.md) | 콘텐츠 사용 URL | Container URL | 0 | 콘텐츠에서 사용하는 URL을 기록하여 접근 가능 여부 등의 점검에 활용한다. |
| [`cm_containerttable`](cm/cm_containerttable.md) | 콘텐츠 템플릿 테이블 연결 | Container T.Table | 0 | 웹 콘텐츠 컨테이너와 템플릿 테이블 사이의 연결을 관리한다. |
| [`cm_cstage`](cm/cm_cstage.md) | 게시 준비 콘텐츠 | Web Container Stage | 5 | 게시 준비 단계의 이미지·텍스트 등을 담는 컨테이너를 관리한다. |
| [`cm_cstage_element`](cm/cm_cstage_element.md) | 게시 준비 콘텐츠 요소 | Container Stage Element | 7 | 게시 준비 컨테이너의 제목·본문·꼬리말 등 개별 요소를 관리한다. |
| [`cm_cstage_element_trl`](cm/cm_cstage_element_trl.md) | 게시 준비 요소 번역 | Container Stage Element Trl | 7 | 게시 준비 단계의 개별 콘텐츠 요소 번역을 저장한다. |
| [`cm_cstage_trl`](cm/cm_cstage_trl.md) | 게시 준비 콘텐츠 번역 | Web Container Stage Trl | 5 | 게시 준비 컨테이너의 언어별 콘텐츠를 저장한다. |
| [`cm_cstagettable`](cm/cm_cstagettable.md) | 게시 준비 템플릿 테이블 연결 | Stage T.Table | 0 | 게시 준비 컨테이너와 템플릿 테이블의 연결을 관리한다. |
| [`cm_media`](cm/cm_media.md) | 웹 미디어 | Media Item | 3 | 이미지·동영상 등 웹 콘텐츠에서 사용하는 미디어 항목을 관리한다. |
| [`cm_media_server`](cm/cm_media_server.md) | 미디어 서버 | Media Server | 1 | 미디어 전송 대상 서버 목록을 관리하며 정적 서버에 미디어를 배치하는 구성에 사용한다. |
| [`cm_mediadeploy`](cm/cm_mediadeploy.md) | 미디어 배포 이력 | Media Deploy | 0 | 미디어 콘텐츠의 배포 로그를 저장한다. |
| [`cm_newschannel`](cm/cm_newschannel.md) | RSS 뉴스 채널 | News Channel | 0 | RSS 피드에 사용할 콘텐츠 범위를 정의하는 뉴스 채널을 관리한다. |
| [`cm_newsitem`](cm/cm_newsitem.md) | 뉴스 기사 항목 | News Item / Article | 0 | 뉴스나 기사의 기본 내용을 관리하며 상세 기사로 안내하는 요약 콘텐츠로 사용할 수 있다. |
| [`cm_template`](cm/cm_template.md) | 웹 콘텐츠 템플릿 | Template | 4 | 콘텐츠 표시를 위한 레이아웃과 처리 스크립트 등의 템플릿을 정의한다. |
| [`cm_template_ad_cat`](cm/cm_template_ad_cat.md) | 템플릿 광고 분류 연결 | Template Advertising Category | 0 | 웹 템플릿과 광고 분류의 대응 관계를 관리한다. |
| [`cm_templatetable`](cm/cm_templatetable.md) | 템플릿 테이블 연결 | Template Table | 0 | 콘텐츠 관리 템플릿의 테이블 연결을 관리한다. |
| [`cm_webaccesslog`](cm/cm_webaccesslog.md) | 웹 접근 로그 | Web Access Log | 0 | 웹 프로젝트의 요청 URL·접속 주소·사용자 에이전트·응답 코드·크기 등 접근 이력을 저장한다. |
| [`cm_webproject`](cm/cm_webproject.md) | 웹 콘텐츠 프로젝트 | Web Project | 1 | 콘텐츠 컨테이너·URL·광고·미디어 등을 포괄하는 웹 콘텐츠 관리 프로젝트를 정의한다. |
| [`cm_webproject_domain`](cm/cm_webproject_domain.md) | 웹 프로젝트 도메인 | WebProject Domain | 1 | 웹 프로젝트의 도메인 처리와 전달 관계를 정의한다. |
| [`cm_wikitoken`](cm/cm_wikitoken.md) | 위키 토큰 | Wiki Token | 0 | 위키 토큰의 유형과 매크로 또는 대상 테이블·조회절·조건절을 정의한다. 실제 치환·렌더링 동작은 처리 코드 확인이 필요하다. |
| [`dbreplicasyncverifier`](other/dbreplicasyncverifier.md) | DB 복제 동기화 확인 정보 | — | 1 | lastupdate 값만 가진 내부 테이블로 물리명상 DB 복제 동기화 확인 용도로 추정된다. 갱신 주체와 판정 방식은 구조만으로 확인할 수 없다. |
| [`dd_networkdistribution`](dd/dd_networkdistribution.md) | 재고 배분 네트워크 | Network Distribution | 2 | 재고 분배에 사용할 네트워크의 상위 정의를 관리한다. |
| [`dd_networkdistributionline`](dd/dd_networkdistributionline.md) | 재고 배분 네트워크 명세 | Network Distribution Line | 10 | 재고 배분 네트워크의 출발·도착 창고, 운송사, 배분 비율·이송 시간·우선순위와 유효 기간을 정의한다. |
| [`dd_order`](dd/dd_order.md) | 재고 배분 주문 | Distribution Order | 0 | 재고 배분을 지시하는 주문의 머리글을 관리한다. |
| [`dd_orderline`](dd/dd_orderline.md) | 재고 배분 주문 명세 | Distribution Order Line | 0 | 재고 배분 주문에 포함되는 개별 배분 내역을 관리한다. |
| [`exp_format`](exp/exp_format.md) | 데이터 내보내기 형식 | Export Format | 10 | 내보낼 대상 테이블·필터 조건·버전과 형식 식별자를 정의한다. |
| [`exp_formatline`](exp/exp_formatline.md) | 내보내기 형식 항목 | Format Line | 43 | 형식의 항목 순서·대상 컬럼·필수 여부·날짜 형식 및 중첩 형식을 정의한다. |
| [`exp_processor`](exp/exp_processor.md) | 데이터 내보내기 처리기 | Export Processor | 2 | 내보내기 처리기 유형에 연결되는 실행 설정과 대상 호스트·포트·계정 설정을 관리한다. |
| [`exp_processor_type`](exp/exp_processor_type.md) | 내보내기 처리기 유형 | Export Processor Type | 2 | 내보내기 처리기의 종류와 실행 Java 클래스를 정의한다. |
| [`exp_processorparameter`](exp/exp_processorparameter.md) | 내보내기 처리 매개변수 | Processor Parameter | 7 | 개별 내보내기 처리기에 전달할 이름별 매개변수 값을 관리한다. |
| [`fact_acct`](fact/fact_acct.md) | 전기 회계 분개 | Accounting Fact | 0 | 업무 문서에서 전기된 회계 분개를 계정·회계 스키마·기간 및 분석 요소별로 저장한다. 거래통화와 회계통화의 차변·대변 금액 및 원 문서 테이블·레코드·행 식별자를 포함한다. |
| [`fact_acct_summary`](fact/fact_acct_summary.md) | 회계 분개 집계 | Accounting Fact summary | 0 | 보고 큐브와 계정·기간·조직 등 분석 요소별 회계통화 차변·대변 금액 및 수량 집계를 저장한다. 원분개와 함께 합산하면 중복될 수 있다. |
| [`fact_reconciliation`](fact/fact_reconciliation.md) | 회계 분개 대사 연결 | Accounting Fact Reconciliation | 0 | 회계 분개에 대사 코드를 연결하여 대응되는 분개를 묶는 데 사용한다. |
| [`gl_budget`](gl/gl_budget.md) | 총계정원장 예산 | Budget | 1 | 총계정원장 예산의 기준정보를 관리한다. |
| [`gl_budgetcontrol`](gl/gl_budgetcontrol.md) | 예산 통제 | Budget Control | 0 | 회계 스키마와 예산별 통제 범위·약정 유형·승인 전 통제 여부를 정의한다. |
| [`gl_category`](gl/gl_category.md) | 원장 분류 | GL Category | 10 | 총계정원장 문서와 분개를 분류하는 기준을 정의한다. |
| [`gl_category_trl`](gl/gl_category_trl.md) | 원장 분류 번역 | GL Category Trl | 10 | 총계정원장 분류의 언어별 표시 내용을 저장한다. |
| [`gl_distribution`](gl/gl_distribution.md) | 원장 배부 규칙 | GL Distribution | 1 | 총계정원장 금액을 배부하는 상위 규칙을 관리한다. |
| [`gl_distributionline`](gl/gl_distributionline.md) | 원장 배부 명세 | GL Distribution Line | 2 | 총계정원장 배부 규칙의 개별 배부 항목을 관리한다. |
| [`gl_fund`](gl/gl_fund.md) | 원장 자금 통제 | GL Fund | 0 | 회계 스키마별 통제 대상 자금과 금액 및 적용 기간을 정의한다. |
| [`gl_fundrestriction`](gl/gl_fundrestriction.md) | 자금 사용 제한 | Fund Restriction | 0 | 자금 통제 항목에 계정 요소 값을 연결하여 적용 제한 범위를 지정한다. |
| [`gl_journal`](gl/gl_journal.md) | 원장 분개 전표 | Journal | 2 | 총계정원장 분개 전표의 머리글을 관리하며 차변·대변 행은 전표 명세에 저장된다. |
| [`gl_journalbatch`](gl/gl_journalbatch.md) | 원장 분개 배치 | Journal Batch | 1 | 총계정원장 분개 전표를 배치 단위로 묶어 관리한다. |
| [`gl_journalgenerator`](gl/gl_journalgenerator.md) | 원장 분개 생성 규칙 | GL Journal Generator | 2 | 회계 스키마·문서 유형·원장 분류와 차대변 조정 계정 등을 지정하는 분개 생성 규칙이다. |
| [`gl_journalgeneratorline`](gl/gl_journalgeneratorline.md) | 분개 생성 대상 규칙 | Generator Line | 6 | 생성할 차변·대변 계정, 거래처 분석 방식, 금액 배수와 반올림 기준을 정의한다. |
| [`gl_journalgeneratorsource`](gl/gl_journalgeneratorsource.md) | 분개 생성 원천 규칙 | Generator Source | 8 | 분개 생성 행에 사용할 원천 계정·원장 분류와 금액 배수·반올림 기준을 정의한다. |
| [`gl_journalline`](gl/gl_journalline.md) | 원장 분개 전표 명세 | Journal Line | 4 | 총계정원장 분개 전표의 개별 분개 행을 저장한다. |
| [`hr_attribute`](hr/hr_attribute.md) | 직원 급여 속성 | Payroll Employee Attribute | 0 | 직원·급여 항목별 적용 값과 계산 규칙·유효 기간을 관리하며 금액·수량·문자·서비스 날짜 등의 형식을 담는다. |
| [`hr_concept`](hr/hr_concept.md) | 급여 계산 항목 | Payroll Concept | 0 | 급여 항목의 유형·값 형식·분류·차대 부호 및 출력·지급 여부를 정의한다. |
| [`hr_concept_acct`](hr/hr_concept_acct.md) | 급여 항목 회계 계정 | Payroll Concept Account | 0 | 급여 항목과 회계 스키마별 수익·비용 계정 및 거래처 그룹 등의 회계 연결을 관리한다. |
| [`hr_concept_category`](hr/hr_concept_category.md) | 급여 항목 분류 | Payroll Concept Category | 0 | 급여 계산 항목의 분류와 연결 계정·기본 여부를 관리한다. |
| [`hr_contract`](hr/hr_contract.md) | 급여 계약 기준 | Payroll Contract | 0 | 급여에 연결되는 계약의 유효 기간·기준 일수와 거래처·프로젝트 등의 관련 정보를 관리한다. |
| [`hr_department`](hr/hr_department.md) | 급여 부서 | Payroll Department | 0 | 급여 부서의 코드·이름과 업무 활동 연결을 관리한다. 공통 부서 기준 c_department와 구분한다. |
| [`hr_employee`](hr/hr_employee.md) | 급여 직원 | Payroll Employee | 0 | 급여 대상 직원을 거래처와 연결하고 부서·직무·급여 체계 및 입퇴사 날짜를 관리한다. |
| [`hr_job`](hr/hr_job.md) | 급여 직무 | Payroll Job | 0 | 급여 직무와 소속 부서·상위 구조 관련 값·감독 사용자 정보를 관리한다. |
| [`hr_list`](hr/hr_list.md) | 급여 기준 목록 | Payroll List | 0 | 급여 계산 등에 참조할 목록을 유형·부서·직원·급여 체계와 연결하여 정의한다. |
| [`hr_listline`](hr/hr_listline.md) | 급여 기준 목록 행 | Payroll List Line | 0 | 급여 목록 버전의 값 구간과 여러 값 컬럼을 저장한다. 각 컬럼의 의미는 목록 설정에 따라 확인해야 한다. |
| [`hr_listtype`](hr/hr_listtype.md) | 급여 목록 유형 | Payroll List Type | 0 | 급여 기준 목록의 유형 코드·이름·설명을 관리한다. |
| [`hr_listversion`](hr/hr_listversion.md) | 급여 목록 버전 | Payroll List Version | 0 | 급여 기준 목록의 버전과 유효 기간·기준 목록 연결을 관리한다. |
| [`hr_movement`](hr/hr_movement.md) | 급여 계산 내역 | Payroll Movement | 0 | 급여 실행별 직원·급여 항목의 금액·수량·문자 값 및 계산 규칙과 분석 요소를 저장한다. |
| [`hr_payroll`](hr/hr_payroll.md) | 급여 체계 | Payroll | 0 | 급여 계산·지급 기준 체계를 정의하고 계약·지급 방식·인쇄 서식과 부대 항목을 연결한다. |
| [`hr_payrollconcept`](hr/hr_payrollconcept.md) | 급여 체계별 계산 항목 | Payroll Concept | 0 | 급여 체계에 항목과 규칙을 연결하고 계산 순서·포함·표시·인쇄 여부를 지정한다. |
| [`hr_period`](hr/hr_period.md) | 급여 기간 | Payroll Period | 0 | 급여 체계별 기간의 시작·종료일·회계일·상태를 관리하고 회계 기간 및 급여 연도와 연결한다. |
| [`hr_process`](hr/hr_process.md) | 급여 계산 실행 | Payroll Process | 0 | 급여 체계·기간·직원 또는 부서별 급여 처리 전표를 관리한다. 문서 상태·회계 전기·지급 대상 선정 연결을 포함한다. |
| [`hr_year`](hr/hr_year.md) | 급여 연도 | Payroll Year | 0 | 급여 체계별 연간 기준을 회계 연도와 연결하고 시작일·기준 일수·수량을 관리한다. |
| [`i_asset`](i/i_asset.md) | 자산 가져오기 임시 데이터 | Asset | 0 | 자산과 감가상각·계정·소재지 정보를 정식 데이터로 가져오기 전에 저장하며 가져오기 여부와 오류 메시지를 관리한다. |
| [`i_bankstatement`](i/i_bankstatement.md) | 은행명세 가져오기 임시 데이터 | Import Bank Statement | 0 | 외부 은행거래 명세를 정식 명세로 가져오기 위한 입력 데이터를 저장한다. |
| [`i_bpartner`](i/i_bpartner.md) | 거래처 가져오기 임시 데이터 | Import Business Partner | 0 | 거래처·주소·연락처와 고객·공급업체·직원 구분을 가져오기 전에 저장하며 결과 식별자와 오류 상태를 관리한다. |
| [`i_conversion_rate`](i/i_conversion_rate.md) | 환율 가져오기 임시 데이터 | Import Conversion Rate | 2 | 외부 통화 환율을 가져오기 위한 입력 데이터를 저장한다. |
| [`i_elementvalue`](i/i_elementvalue.md) | 계정과목 가져오기 | Import Account | 0 | 외부 계정 코드와 계정 유형·상위 계정 정보를 계정과목 사전으로 가져오기 위한 중간 데이터를 저장한다. |
| [`i_fajournal`](i/i_fajournal.md) | 고정자산 분개 가져오기 | FA Journal | 0 | 자산 식별자와 감가상각 여부, 분개 차대변 금액을 포함한 고정자산 관련 분개 가져오기 데이터를 저장한다. |
| [`i_fixedasset`](i/i_fixedasset.md) | 고정자산 가져오기 | Imported Fixed Asset | 0 | 취득원가·누적감가상각·사용연수 등 외부 고정자산 정보를 자산 대장으로 옮기기 위한 데이터를 저장한다. |
| [`i_gljournal`](i/i_gljournal.md) | 총계정원장 분개 가져오기 | Import GL Journal | 0 | 외부 총계정원장 분개를 가져오기 위한 입력 데이터를 보관한다. |
| [`i_hr_movement`](i/i_hr_movement.md) | 급여 변동 내역 가져오기 | Payroll Movement Import | 0 | 거래처·급여 개념·처리 건별 금액과 수량을 급여 변동 내역으로 가져오기 위한 데이터를 저장한다. |
| [`i_inoutlineconfirm`](i/i_inoutlineconfirm.md) | 출하·입고 확인행 가져오기 | Ship/Receipt Confirmation Import Line | 0 | 외부의 자재 출하 또는 입고 확인행을 시스템으로 가져오기 위한 중간 데이터다. |
| [`i_inventory`](i/i_inventory.md) | 재고 거래 가져오기 | Import Inventory | 0 | 외부 재고 거래를 시스템 재고 문서로 가져오기 위한 입력 데이터를 저장한다. |
| [`i_invoice`](i/i_invoice.md) | 송장 가져오기 | Import Invoice | 0 | 외부 송장 데이터를 시스템 송장으로 등록하기 위한 중간 데이터를 보관한다. |
| [`i_movement`](i/i_movement.md) | 재고 이동 가져오기 | I_Movement_ID | 0 | 출발·도착 보관 위치와 제품·이동 수량을 재고 이동 문서 및 행으로 가져오기 위한 데이터를 저장한다. |
| [`i_order`](i/i_order.md) | 주문 가져오기 | Import Order | 0 | 외부 주문을 시스템 주문으로 등록하기 위한 중간 데이터를 저장한다. |
| [`i_payment`](i/i_payment.md) | 지급·수금 가져오기 | Import Payment | 0 | 외부 지급 또는 수금 데이터를 결제 기록으로 가져오기 위한 입력 데이터를 저장한다. |
| [`i_pricelist`](i/i_pricelist.md) | 가격표 가져오기 | Import Price List | 0 | 가격표 및 그 버전을 외부 데이터에서 가져오기 위한 중간 데이터를 저장한다. |
| [`i_product`](i/i_product.md) | 제품·서비스 가져오기 | Import Product | 0 | 외부 품목 또는 서비스 정보를 제품 사전에 등록하기 위한 입력 데이터를 보관한다. |
| [`i_productplanning`](i/i_productplanning.md) | 제품 계획 가져오기 | Import Product Planning | 0 | 제품·창고별 보충 정책과 BOM·자원·안전재고 등을 제품 계획으로 가져오기 위한 데이터를 저장한다. |
| [`i_reportline`](i/i_reportline.md) | 보고서 행 집합 가져오기 | Import Report Line Set | 0 | 외부의 보고서 행 집합 값을 보고서 정의로 가져오기 위한 데이터를 저장한다. |
| [`imp_processor`](imp/imp_processor.md) | 가져오기 처리기 | Import Processor | 2 | 가져오기 처리기의 유형, 실행 주기와 연결 설정을 정의한다. |
| [`imp_processor_type`](imp/imp_processor_type.md) | 가져오기 처리기 유형 | Import Processor Type | 2 | 가져오기 처리기 유형과 해당 구현 클래스 정보를 정의한다. |
| [`imp_processorlog`](imp/imp_processorlog.md) | 가져오기 처리 로그 | Import Processor Log | 0 | 가져오기 처리기 실행의 요약·오류 여부와 상세 메시지를 기록한다. |
| [`imp_processorparameter`](imp/imp_processorparameter.md) | 가져오기 처리 매개변수 | Import Processor Parameter | 6 | 가져오기 처리기에 전달하는 이름별 매개변수 값을 저장한다. |
| [`k_category`](k/k_category.md) | 지식 분류 | Knowledge Category | 1 | 지식 항목을 분류하는 범주를 정의한다. |
| [`k_categoryvalue`](k/k_categoryvalue.md) | 지식 분류값 | Category Value | 0 | 지식 분류에 속하는 선택 가능한 값을 정의한다. |
| [`k_comment`](k/k_comment.md) | 지식 항목 의견 | Entry Comment | 0 | 지식 항목에 대한 의견이나 주석을 저장한다. |
| [`k_entry`](k/k_entry.md) | 지식 항목 | Entry | 0 | 지식 관리의 개별 콘텐츠 항목을 저장한다. |
| [`k_entrycategory`](k/k_entrycategory.md) | 지식 항목 분류 연결 | K_EntryCategory | 0 | 지식 항목을 분류 및 해당 분류값과 연결한다. |
| [`k_entryrelated`](k/k_entryrelated.md) | 관련 지식 항목 | Related Entry | 0 | 하나의 지식 항목과 연관된 다른 항목의 관계를 저장한다. |
| [`k_index`](k/k_index.md) | 검색 색인 | Index | 0 | 키워드·발췌문과 원본 테이블·레코드 식별자를 연결하는 검색 색인 정보를 저장한다. |
| [`k_indexlog`](k/k_indexlog.md) | 색인 검색 로그 | Index Log | 0 | 색인 검색의 질의와 결과 및 질의 출처를 기록한다. |
| [`k_indexstop`](k/k_indexstop.md) | 색인 제외 단어 | Index Stop | 0 | 색인에서 제외할 키워드와 문서 유형·웹 프로젝트·요청 유형 등의 적용 범위를 저장한다. |
| [`k_source`](k/k_source.md) | 지식 출처 | Knowledge Source | 1 | 지식 항목이 유래한 정보 출처를 정의한다. |
| [`k_synonym`](k/k_synonym.md) | 지식 검색 동의어 | Knowledge Synonym | 0 | 지식 검색에 사용하는 키워드의 동의어를 정의한다. |
| [`k_topic`](k/k_topic.md) | 지식 주제 | Knowledge Topic | 1 | 지식 콘텐츠를 구분하는 주제를 정의한다. |
| [`k_type`](k/k_type.md) | 지식 유형 | Knowledge Type | 2 | 지식 항목의 유형을 정의한다. |
| [`m_attribute`](m/m_attribute.md) | 제품 속성 | Attribute | 4 | 제품의 특성을 표현하는 속성을 정의한다. |
| [`m_attributeinstance`](m/m_attributeinstance.md) | 제품 속성 실값 | M_AttributeInstance | 5 | 속성 집합 인스턴스에 속한 개별 속성의 선택값·문자·숫자·날짜 값을 저장한다. |
| [`m_attributeinstanceline`](m/m_attributeinstanceline.md) | 속성 다중 선택값 | Attribute Instance Values | 0 | 속성 인스턴스에서 선택한 속성값들을 행 단위로 저장한다. |
| [`m_attributesearch`](m/m_attributesearch.md) | 공통 검색 속성 | Attribute Search | 1 | 제품 속성을 이용한 공통 검색 조건을 정의한다. |
| [`m_attributeset`](m/m_attributeset.md) | 제품 속성 집합 | Attribute Set | 4 | 제품에 함께 적용할 속성들의 묶음을 정의한다. |
| [`m_attributesetexclude`](m/m_attributesetexclude.md) | 속성 집합 입력 제외 | Exclude Attribute Set | 0 | 특정 범위에서 속성 집합 입력을 제외하는 설정을 저장한다. |
| [`m_attributesetinstance`](m/m_attributesetinstance.md) | 제품 속성 집합 인스턴스 | Attribute Set Instance | 4 | 제품 속성 집합이 실제 적용된 개별 인스턴스를 식별한다. |
| [`m_attributeuse`](m/m_attributeuse.md) | 속성 집합 구성 | M_AttributeUse | 5 | 속성 집합에 포함할 속성과 표시 순서·기본값을 연결한다. |
| [`m_attributevalue`](m/m_attributevalue.md) | 제품 속성 선택값 | Attribute Value | 9 | 제품 속성에서 선택할 수 있는 값을 정의한다. |
| [`m_bom`](m/m_bom.md) | 자재명세서 | BOM | 1 | 제품을 구성하는 자재명세서(BOM)를 정의한다. |
| [`m_bomalternative`](m/m_bomalternative.md) | BOM 대체 그룹 | Alternative Group | 1 | 제품 BOM에서 대체 가능한 구성품의 그룹을 정의한다. |
| [`m_bomproduct`](m/m_bomproduct.md) | BOM 구성품 | BOM Component | 0 | 자재명세서에 포함되는 제품 구성품을 저장한다. |
| [`m_bp_price`](m/m_bp_price.md) | 거래처별 제품 가격 | Business Partner Price | 0 | 일반 가격표보다 우선 적용하는 거래처별 가격을 저장한다. |
| [`m_changenotice`](m/m_changenotice.md) | 변경 통지 | Change Notice | 1 | 제품 변경과 관련한 통지 내용 및 승인·처리 상태를 저장한다. |
| [`m_changerequest`](m/m_changerequest.md) | 변경 요청 | Change Request | 0 | BOM과 관련된 변경 요청 내용 및 연계 변경 통지·승인 상태를 저장한다. |
| [`m_commodityshipment`](m/m_commodityshipment.md) | 출하 상품 통관 정보 | Commodity Shipment | 0 | 제품의 수출 허가 번호·품목분류 코드·제조국을 저장한다. |
| [`m_cost`](m/m_cost.md) | 제품 원가 | Product Cost | 267 | 제품·원가 유형·회계 스키마·원가 요소별 현재 원가와 수량 및 누적 금액을 저장한다. |
| [`m_costdetail`](m/m_costdetail.md) | 원가 상세 | Cost Detail | 0 | 제품 원가 계산에 사용하는 상세 원가 정보를 저장한다. |
| [`m_costelement`](m/m_costelement.md) | 원가 요소 | Cost Element | 9 | 원가를 구성하는 요소와 요소 유형·원가 계산 방법을 정의한다. |
| [`m_costhistory`](m/m_costhistory.md) | 원가 변경 이력 | Cost History | 0 | 제품 원가 테이블의 변동 이력을 기록한다. |
| [`m_costqueue`](m/m_costqueue.md) | 선입·후입 원가 대기열 | Cost Queue | 0 | FIFO 또는 LIFO 방식의 원가 계산에 사용하는 원가 대기열을 관리한다. |
| [`m_costtype`](m/m_costtype.md) | 원가 유형 | Cost Type | 1 | 제품 원가를 구분하여 관리하기 위한 원가 유형을 정의한다. |
| [`m_demand`](m/m_demand.md) | 자재 수요 | Demand | 0 | 자재 수요 문서의 기본 정보를 저장한다. |
| [`m_demanddetail`](m/m_demanddetail.md) | 자재 수요 원천 상세 | Demand Detail | 0 | 자재 수요행의 근거가 된 원천 내역을 저장한다. |
| [`m_demandline`](m/m_demandline.md) | 자재 수요행 | Demand Line | 0 | 자재 수요 문서의 개별 행을 저장한다. |
| [`m_discountschema`](m/m_discountschema.md) | 할인 규칙 | Discount Schema | 3 | 거래 할인율을 계산하는 할인 체계를 정의한다. |
| [`m_discountschemabreak`](m/m_discountschemabreak.md) | 구간별 할인 | Discount Schema Break | 1 | 할인 체계의 구간별 거래 할인 조건을 저장한다. |
| [`m_discountschemaline`](m/m_discountschemaline.md) | 가격표 할인 규칙행 | Discount Price List | 11 | 가격표에 적용하는 거래 할인 체계의 개별 행을 저장한다. |
| [`m_distributionlist`](m/m_distributionlist.md) | 제품 배분 대상 목록 | Distribution List | 1 | 제품을 배분할 거래처들의 목록을 정의한다. |
| [`m_distributionlistline`](m/m_distributionlistline.md) | 제품 배분 대상행 | Distribution List Line | 3 | 배분 목록에 속한 거래처와 수량 또는 배분 비율을 저장한다. |
| [`m_distributionrun`](m/m_distributionrun.md) | 제품 배분 실행 | Distribution Run | 1 | 선택한 거래처들에 제품을 배분하는 주문 생성 실행을 정의한다. |
| [`m_distributionrunline`](m/m_distributionrunline.md) | 제품 배분 실행행 | Distribution Run Line | 1 | 배분 실행에 사용할 대상 목록·제품·수량을 지정한다. |
| [`m_edi`](m/m_edi.md) | 전자문서 교환 거래 | EDI Transaction | 0 | 제품 수량·납기·가격에 대한 EDI 요청과 응답 및 송수신 상태를 저장한다. |
| [`m_edi_info`](m/m_edi_info.md) | 전자문서 교환 로그 | EDI Log | 0 | 개별 EDI 거래에 연결된 추가 로그 정보를 저장한다. |
| [`m_forecast`](m/m_forecast.md) | 자재 예측 | Forecast | 4 | 자재에 대한 예측 문서의 기본 정보를 저장한다. |
| [`m_forecastline`](m/m_forecastline.md) | 자재 예측행 | Forecast Line | 50 | 자재 예측 문서의 개별 행을 저장한다. |
| [`m_freight`](m/m_freight.md) | 운임 요율 | Freight | 3 | 제품 운송에 적용하는 운임 요율을 정의한다. |
| [`m_freightcategory`](m/m_freightcategory.md) | 운임 분류 | Freight Category | 2 | 운임을 구분하는 분류를 정의한다. |
| [`m_inout`](m/m_inout.md) | 출하·입고 문서 | Shipment/Receipt | 9 | 제품의 고객 출하 또는 공급업체 입고를 기록하는 자재 이동 문서의 헤더다. 출하와 입고를 모두 포함하므로 조회 시 거래 방향을 구분해야 한다. |
| [`m_inoutconfirm`](m/m_inoutconfirm.md) | 출하·입고 확인 | Ship/Receipt Confirmation | 1 | 출하 또는 입고 문서에 대한 확인 정보를 저장한다. |
| [`m_inoutline`](m/m_inoutline.md) | 출하·입고행 | Shipment/Receipt Line | 27 | 출하 또는 입고 문서의 제품별 상세 행을 저장한다. |
| [`m_inoutlineconfirm`](m/m_inoutlineconfirm.md) | 출하·입고 확인행 | Ship/Receipt Confirmation Line | 1 | 출하 또는 입고 확인 문서의 개별 자재 확인행을 저장한다. |
| [`m_inoutlinema`](m/m_inoutlinema.md) | 출하·입고행 속성 배분 | M_InOutLineMA | 0 | 출하·입고행의 이동 수량을 속성 집합 인스턴스와 자재 정책일별로 나누어 저장한다. |
| [`m_inventory`](m/m_inventory.md) | 실사 재고 문서 | Phys.Inventory | 3 | 실물 재고 실사를 위한 문서 및 매개변수를 저장한다. |
| [`m_inventoryline`](m/m_inventoryline.md) | 실사 재고행 | Phys.Inventory Line | 1 | 재고 실사 문서에 속하는 개별 품목 행을 저장한다. |
| [`m_inventorylinema`](m/m_inventorylinema.md) | 실사 재고행 속성 배분 | M_InventoryLineMA | 0 | 실사 재고행의 수량을 속성 집합 인스턴스와 자재 정책일별로 배분한다. |
| [`m_locator`](m/m_locator.md) | 창고 보관 위치 | Locator | 11 | 창고 안에서 재고를 보관하는 위치를 정의한다. |
| [`m_locatortype`](m/m_locatortype.md) | 보관 위치 유형 | Locator Type | 0 | 보관 위치의 유형과 보충·예약·출하에 사용할 수 있는지 여부를 정의한다. |
| [`m_lot`](m/m_lot.md) | 제품 로트 | Lot | 0 | 제품의 로트 정보를 정의한다. |
| [`m_lotctl`](m/m_lotctl.md) | 로트 번호 관리 | Lot Control | 1 | 제품 로트의 관리 기준을 정의한다. |
| [`m_lotctlexclude`](m/m_lotctlexclude.md) | 로트 생성 제외 | Exclude Lot | 0 | 속성 집합에서 로트 생성을 제외하는 설정을 저장한다. |
| [`m_matchinv`](m/m_matchinv.md) | 입출고·송장 대사 | Match Invoice | 18 | 출하·입고 내역과 송장 내역의 대응 관계를 저장한다. |
| [`m_matchpo`](m/m_matchpo.md) | 구매 주문 대사 | Match PO | 37 | 구매 주문을 출하·입고 및 송장 내역과 대응시킨다. |
| [`m_movement`](m/m_movement.md) | 재고 이동 문서 | Inventory Move | 1 | 보관 위치 사이의 재고 이동을 기록하는 문서다. |
| [`m_movementconfirm`](m/m_movementconfirm.md) | 재고 이동 확인 | Move Confirm | 0 | 재고 이동 문서의 확인 정보를 저장한다. |
| [`m_movementline`](m/m_movementline.md) | 재고 이동행 | Move Line | 1 | 재고 이동 문서의 개별 이동 내역을 저장한다. |
| [`m_movementlineconfirm`](m/m_movementlineconfirm.md) | 재고 이동 확인행 | Move Line Confirm | 0 | 재고 이동행의 확인 내역을 저장한다. |
| [`m_movementlinema`](m/m_movementlinema.md) | 재고 이동행 속성 배분 | M_MovementLineMA | 0 | 재고 이동행의 수량을 속성 집합 인스턴스와 자재 정책일별로 나누어 저장한다. |
| [`m_operationresource`](m/m_operationresource.md) | 제품 공정 자원 | Operation Resource | 0 | 제품 공정에 필요한 자원을 연결한다. |
| [`m_package`](m/m_package.md) | 출하 포장 | Package | 1 | 출하에 사용되는 포장 단위 정보를 저장한다. |
| [`m_packageline`](m/m_packageline.md) | 출하 포장 내용행 | Package Line | 1 | 포장에 포함된 상세 내용물을 저장한다. |
| [`m_packagemps`](m/m_packagemps.md) | 다중 포장 세부 정보 | Package MPS | 0 | 포장별 치수·중량과 개별 및 대표 추적 번호를 저장한다. |
| [`m_parttype`](m/m_parttype.md) | 제조 부품 유형 | Part Type | 0 | 제조에 사용하는 부품의 유형을 정의한다. |
| [`m_perpetualinv`](m/m_perpetualinv.md) | 순환 실사 규칙 | Perpetual Inventory | 0 | 재고 실사 문서를 생성하는 규칙을 정의한다. |
| [`m_pricelist`](m/m_pricelist.md) | 가격표 | Price List | 4 | 제품 가격을 관리하는 가격표를 식별한다. |
| [`m_pricelist_trl`](m/m_pricelist_trl.md) | 가격표 번역 | Price List | 4 | 가격표의 언어별 번역 정보를 저장한다. |
| [`m_pricelist_version`](m/m_pricelist_version.md) | 가격표 버전 | Price List Version | 6 | 하나의 가격표에 속한 개별 버전을 식별한다. |
| [`m_pricelist_version_trl`](m/m_pricelist_version_trl.md) | 가격표 버전 번역 | Price List Version Trl | 6 | 가격표 버전의 언어별 번역 정보를 저장한다. |
| [`m_product`](m/m_product.md) | 제품·서비스 | Product | 255 | 제품·서비스·품목의 공통 기본 정보를 관리하는 마스터다. |
| [`m_product_acct`](m/m_product_acct.md) | 제품별 회계 계정 | Product Acct | 110 | 제품과 회계 스키마별 매출·비용·재고·매출원가 및 제조 관련 계정을 연결한다. |
| [`m_product_bom_old`](m/m_product_bom_old.md) | 구형 제품 BOM | — | 20 | 제품과 하위 구성품, 구성 수량 및 BOM 유형을 저장하는 구형 명칭의 테이블이다. 현재 기능에서의 사용 여부는 확인이 필요하다. |
| [`m_product_category`](m/m_product_category.md) | 제품 분류 | Product Category | 14 | 제품을 묶어 관리하는 분류를 정의한다. |
| [`m_product_category_acct`](m/m_product_category_acct.md) | 제품 분류별 회계 설정 | Product Category Acct | 28 | 제품 분류와 회계 스키마별 기본 계정·원가 계산 방법·원가 수준을 정의한다. |
| [`m_product_category_trl`](m/m_product_category_trl.md) | 제품 분류 번역 | Product Category Trl | 14 | 제품 분류의 언어별 번역 정보를 저장한다. |
| [`m_product_po`](m/m_product_po.md) | 제품 구매 조건 | Product Purchasing | 29 | 제품과 공급업체별 구매 단가·거래 통화·공급업체 품번·최소 주문량·납기를 저장한다. |
| [`m_product_qualitytest`](m/m_product_qualitytest.md) | 제품별 품질 시험 | Product Quality Test | 0 | 제품에 적용할 품질 시험과 기대 결과를 연결한다. |
| [`m_product_trl`](m/m_product_trl.md) | 제품·서비스 번역 | Product Trl | 55 | 제품·서비스·품목의 언어별 번역 정보를 저장한다. |
| [`m_productdownload`](m/m_productdownload.md) | 제품 다운로드 | Product Download | 1 | 제품에 연결된 다운로드 정보를 관리한다. |
| [`m_production`](m/m_production.md) | 생산 문서 | Production | 0 | 제품 생산 계획을 나타내는 생산 문서의 기본 정보를 저장한다. |
| [`m_productionline`](m/m_productionline.md) | 생산행 | Production Line | 0 | 생산 문서에서 발생하는 개별 자재 내역을 저장한다. |
| [`m_productionlinema`](m/m_productionlinema.md) | 생산행 속성 배분 | Production Line MA | 0 | 생산행의 이동 수량을 속성 집합 인스턴스와 자재 정책일별로 배분한다. |
| [`m_productionplan`](m/m_productionplan.md) | 생산 계획 | Production Plan | 0 | 제품을 어떤 방식으로 생산할지에 대한 계획을 저장한다. |
| [`m_productoperation`](m/m_productoperation.md) | 제품 공정 | Product Operation | 0 | 제품에 필요한 공정과 준비·단위 실행·정리 시간을 정의한다. |
| [`m_productprice`](m/m_productprice.md) | 제품 가격 | Product Price | 114 | 가격표 버전별 제품의 정가·표준가·한도가를 저장한다. |
| [`m_productpricevendorbreak`](m/m_productpricevendorbreak.md) | 공급업체별 수량 구간 가격 | Product Price Break | 0 | 공급업체·제품·가격표 버전과 수량 구간값별 정가·표준가·한도가를 저장한다. |
| [`m_promotion`](m/m_promotion.md) | 판매 촉진 설정 | Promotion | 200 | 판매 촉진 행사에 적용할 기본 설정을 정의한다. |
| [`m_promotiondistribution`](m/m_promotiondistribution.md) | 판매 촉진 수량 배분 | Promotion Distribution | 0 | 혜택 계산을 위해 주문행의 품목을 여러 계산 묶음으로 배분하는 설정을 저장한다. |
| [`m_promotiongroup`](m/m_promotiongroup.md) | 판매 촉진 제품 그룹 | Promotion Group | 200 | 판매 촉진 설정에 함께 사용하는 제품 그룹을 정의한다. |
| [`m_promotiongroupline`](m/m_promotiongroupline.md) | 판매 촉진 그룹 구성행 | Promotion Group Line | 600 | 판매 촉진 제품 그룹에 포함된 개별 품목을 저장한다. |
| [`m_promotionline`](m/m_promotionline.md) | 판매 촉진 조건행 | Promotion Line | 200 | 판매 촉진을 구성하는 제품 조합을 행 단위로 정의한다. |
| [`m_promotionprecondition`](m/m_promotionprecondition.md) | 판매 촉진 사전 조건 | Promotion Pre Condition | 0 | 주문에 판매 촉진을 적용하기 전에 충족해야 하는 조건을 정의한다. |
| [`m_promotionreward`](m/m_promotionreward.md) | 판매 촉진 혜택 | Promotion Reward | 0 | 판매 촉진 조건을 충족할 때 제공할 혜택을 정의한다. |
| [`m_qualitytest`](m/m_qualitytest.md) | 품질 시험 | Quality Test | 0 | 품질 시험 항목의 이름과 설명을 정의한다. |
| [`m_qualitytestresult`](m/m_qualitytestresult.md) | 품질 시험 결과 | Quality Test Result | 0 | 제품 속성 집합 인스턴스별 시험 결과와 합격 여부를 저장한다. |
| [`m_relatedproduct`](m/m_relatedproduct.md) | 관련 제품 관계 | Product Related | 1 | 제품과 관련 제품을 관계 유형과 함께 연결한다. |
| [`m_replenish`](m/m_replenish.md) | 제품 보충 기준 | M_Replenish | 19 | 제품·창고별 보충 유형, 최소·최대 수준과 공급 창고 등을 정의한다. |
| [`m_requisition`](m/m_requisition.md) | 자재 요청서 | Requisition | 1 | 자재 조달 요청 문서의 기본 정보를 저장한다. |
| [`m_requisitionline`](m/m_requisitionline.md) | 자재 요청행 | Requisition Line | 1 | 자재 요청서의 개별 요청 내역을 저장한다. |
| [`m_rma`](m/m_rma.md) | 반품 승인 문서 | RMA | 1 | 반품을 승인하고 관리하는 문서다. 고객 반품과 공급업체 반품은 거래 방향에 따라 구분한다. |
| [`m_rmaline`](m/m_rmaline.md) | 반품 승인행 | RMA Line | 1 | 반품 승인 문서의 개별 반품 대상 내역을 저장한다. |
| [`m_rmatax`](m/m_rmatax.md) | 반품 승인 세금 | RMA Tax | 0 | 반품 승인 문서에 적용되는 세금 내역을 저장한다. |
| [`m_rmatype`](m/m_rmatype.md) | 반품 승인 유형 | RMA Type | 1 | 반품 승인 문서의 유형을 정의한다. |
| [`m_sernoctl`](m/m_sernoctl.md) | 일련번호 관리 | Serial No Control | 1 | 제품 일련번호의 관리 기준을 정의한다. |
| [`m_sernoctlexclude`](m/m_sernoctlexclude.md) | 일련번호 생성 제외 | Exclude Ser No | 0 | 속성 집합에서 일련번호 생성을 제외하는 설정을 저장한다. |
| [`m_shipper`](m/m_shipper.md) | 배송업체·배송 수단 | Shipper | 3 | 제품을 배송하는 업체 또는 배송 방식을 정의한다. |
| [`m_shippercfg`](m/m_shippercfg.md) | 배송업체 구성 | Shipper Configuration | 1 | 제품 배송 방식에 대한 구성 정의를 저장한다. |
| [`m_shipperlabels`](m/m_shipperlabels.md) | 배송업체 라벨 | Shipper Labels | 0 | 배송업체가 사용하는 라벨 구성과 기본값·인쇄 방식을 연결한다. |
| [`m_shipperlabelscfg`](m/m_shipperlabelscfg.md) | 배송 라벨 구성 | Shipper Labels Configuration | 0 | 배송 라벨의 코드·크기·인쇄 방식 등 구성 정보를 정의한다. |
| [`m_shipperpackaging`](m/m_shipperpackaging.md) | 배송업체 포장 | Shipper Packaging | 0 | 배송업체가 사용하는 포장 구성과 중량·기본값을 연결한다. |
| [`m_shipperpackagingcfg`](m/m_shipperpackagingcfg.md) | 배송 포장 구성 | Shipper Packaging Configuration | 0 | 배송 포장 유형의 코드·중량과 기본 설정을 정의한다. |
| [`m_shipperpickuptypes`](m/m_shipperpickuptypes.md) | 배송업체 집하 유형 | Shipper Pickup Types | 0 | 배송업체가 사용하는 집하 유형과 기본값을 연결한다. |
| [`m_shipperpickuptypescfg`](m/m_shipperpickuptypescfg.md) | 집하 유형 구성 | Shipper Pickup Types Configuration | 0 | 배송업체 구성에 속하는 집하 유형의 코드와 설명을 정의한다. |
| [`m_shippingprocessor`](m/m_shippingprocessor.md) | 배송 처리기 | Shipping Processor | 1 | 배송 처리기 구성과 서비스 연결 인증 설정을 연결한다. |
| [`m_shippingprocessorcfg`](m/m_shippingprocessorcfg.md) | 배송 처리기 구성 | Shipping Processor Configuration | 1 | 배송 서비스 접속 주소·프록시 및 처리 구현 클래스의 구성을 정의한다. |
| [`m_shippingtransaction`](m/m_shippingtransaction.md) | 배송 거래 | Shipping Transaction | 0 | 배송 서비스와 처리하는 배송 거래 정보를 저장한다. |
| [`m_shippingtransactionline`](m/m_shippingtransactionline.md) | 배송 거래행 | Shipping Transaction Line | 0 | 배송 거래에 속한 개별 상세 행을 저장한다. |
| [`m_storageonhand`](m/m_storageonhand.md) | 현재고 | M_StorageOnHand | 20 | 제품·보관 위치·속성 집합 인스턴스·자재 정책일별 현재고 수량을 저장한다. |
| [`m_storagereservation`](m/m_storagereservation.md) | 재고 예약·주문 수량 | M_StorageReservation | 2 | 제품·창고·속성 집합 인스턴스와 거래 방향별 수량을 저장한다. 판매 예약과 구매 주문 수량을 구분하여 해석해야 한다. |
| [`m_storagereservationlog`](m/m_storagereservationlog.md) | 재고 예약 변경 로그 | Storage Reservation Log | 0 | 재고 예약 수량이 바뀔 때마다 변경 전후 수량과 증감량을 기록한다. |
| [`m_substitute`](m/m_substitute.md) | 대체 제품 | M_Substitute | 0 | 제품과 대신 사용할 제품을 연결한다. |
| [`m_transaction`](m/m_transaction.md) | 재고 수불 거래 | Inventory Transaction | 28 | 입출고·이동·실사·생산 등에서 발생한 제품 수량 증감을 보관 위치 및 속성 인스턴스와 함께 기록한다. |
| [`m_transactionallocation`](m/m_transactionallocation.md) | 재고 거래 배분 | M_TransactionAllocation | 0 | 입고측과 출고측 재고 거래 및 관련 문서행을 배분 수량·전략과 함께 연결한다. |
| [`m_warehouse`](m/m_warehouse.md) | 창고·서비스 지점 | Warehouse | 11 | 재고를 보관하는 창고와 서비스 제공 지점을 정의한다. |
| [`m_warehouse_acct`](m/m_warehouse_acct.md) | 창고별 회계 계정 | M_Warehouse_Acct | 22 | 창고와 회계 스키마별 재고·실사 조정·차이·재평가 계정을 연결한다. |
| [`mfa_method`](mfa/mfa_method.md) | 다중 인증 방식 | MFA Method | 2 | 다중 요소 인증에 사용하는 인증 방식을 정의한다. |
| [`mfa_registereddevice`](mfa/mfa_registereddevice.md) | 다중 인증 등록 기기 | MFA Registered Device | 0 | 다중 요소 인증을 위해 등록한 기기를 관리한다. |
| [`mfa_registration`](mfa/mfa_registration.md) | 다중 인증 등록 | MFA Registration | 0 | 다중 요소 인증의 등록 정보를 관리한다. |
| [`mfa_rule`](mfa/mfa_rule.md) | 다중 인증 규칙 | MFA Rule | 2 | 다중 요소 인증에 적용할 규칙을 정의한다. |
| [`pa_achievement`](pa/pa_achievement.md) | 성과 달성 | Achievement | 0 | 성과 목표에 대한 달성 정보를 기록한다. |
| [`pa_benchmark`](pa/pa_benchmark.md) | 성과 비교 기준 | Benchmark | 0 | 성과를 비교하는 벤치마크 기준을 정의한다. |
| [`pa_benchmarkdata`](pa/pa_benchmarkdata.md) | 성과 비교 기준값 | Benchmark Data | 0 | 성과 벤치마크의 개별 데이터 값을 저장한다. |
| [`pa_colorschema`](pa/pa_colorschema.md) | 성과 색상 기준 | Color Schema | 2 | 성과 표시에서 사용할 색상 체계를 정의한다. |
| [`pa_dashboardcontent`](pa/pa_dashboardcontent.md) | 대시보드 콘텐츠 | Dashboard Content | 12 | 대시보드에 표시할 창·보고서·목표·차트 등의 콘텐츠와 기본 배치를 정의한다. |
| [`pa_dashboardcontent_access`](pa/pa_dashboardcontent_access.md) | 대시보드 콘텐츠 접근 | PA_DashboardContent_Access_ID | 2 | 대시보드 콘텐츠에 접근할 역할 또는 사용자를 연결한다. |
| [`pa_dashboardcontent_trl`](pa/pa_dashboardcontent_trl.md) | 대시보드 콘텐츠 번역 | Dashboard Content Trl | 12 | 대시보드 콘텐츠의 이름·설명·HTML·도움말을 언어별로 저장한다. |
| [`pa_dashboardpreference`](pa/pa_dashboardpreference.md) | 대시보드 개인 설정 | Dashboard Preference | 0 | 역할·사용자별 대시보드 콘텐츠의 위치·표시 여부·접힘 상태를 저장한다. |
| [`pa_documentstatus`](pa/pa_documentstatus.md) | 문서 상태 표시 설정 | Document Status | 16 | 테이블과 조회 조건을 기준으로 표시할 문서 상태 항목 및 연결 화면·표시 서식을 정의한다. |
| [`pa_documentstatus_trl`](pa/pa_documentstatus_trl.md) | 문서 상태 표시 번역 | Document Status Trl | 16 | 문서 상태 표시 항목의 이름·설명·도움말을 언어별로 저장한다. |
| [`pa_documentstatusaccess`](pa/pa_documentstatusaccess.md) | 문서 상태 표시 접근 | Document Status Access | 10 | 문서 상태 표시 항목에 접근할 역할 또는 사용자를 연결한다. |
| [`pa_goal`](pa/pa_goal.md) | 성과 목표 | Goal | 4 | 측정하고 관리할 성과 목표를 정의한다. |
| [`pa_goalrestriction`](pa/pa_goalrestriction.md) | 성과 목표 제한 조건 | Goal Restriction | 0 | 성과 목표의 측정 범위를 제한하는 조건을 정의한다. |
| [`pa_hierarchy`](pa/pa_hierarchy.md) | 보고 계층 | Reporting Hierarchy | 0 | 보고서에 적용할 계층 구조를 정의한다. |
| [`pa_measure`](pa/pa_measure.md) | 성과 측정값 | Measure | 4 | 실제로 측정한 개별 성과 값을 저장한다. |
| [`pa_measurecalc`](pa/pa_measurecalc.md) | 성과 측정 계산식 | Measure Calculation | 6 | 성과를 측정하는 계산 방법을 정의한다. |
| [`pa_ratio`](pa/pa_ratio.md) | 성과 비율 지표 | Ratio | 1 | 성과를 비율로 표현하는 지표를 정의한다. |
| [`pa_ratioelement`](pa/pa_ratioelement.md) | 성과 비율 구성 요소 | Ratio Element | 3 | 성과 비율 지표를 구성하는 요소를 저장한다. |
| [`pa_report`](pa/pa_report.md) | 재무 보고서 | Financial Report | 3 | 재무 보고서의 기본 정의를 저장한다. |
| [`pa_reportcolumn`](pa/pa_reportcolumn.md) | 재무 보고서 열 | Report Column | 17 | 보고서에 표시할 개별 열을 정의한다. |
| [`pa_reportcolumn_trl`](pa/pa_reportcolumn_trl.md) | 재무 보고서 열 번역 | Report Column Trl | 17 | 보고서 열의 언어별 번역 정보를 저장한다. |
| [`pa_reportcolumnset`](pa/pa_reportcolumnset.md) | 재무 보고서 열 집합 | Report Column Set | 3 | 보고서에 사용할 열들의 묶음을 정의한다. |
| [`pa_reportcube`](pa/pa_reportcube.md) | 회계 집계 큐브 | Report Cube | 0 | 선택한 달력의 기간별로 지정 차원에 따라 회계 자료를 사전 집계하는 큐브를 정의한다. |
| [`pa_reportline`](pa/pa_reportline.md) | 재무 보고서 행 | Report Line | 113 | 보고서 행의 표시 순서·상하위 관계·금액 유형과 계산식을 정의한다. |
| [`pa_reportline_trl`](pa/pa_reportline_trl.md) | 재무 보고서 행 번역 | Report Line Trl | 113 | 보고서 행의 이름과 설명을 언어별로 저장한다. |
| [`pa_reportlineset`](pa/pa_reportlineset.md) | 재무 보고서 행 집합 | Report Line Set | 3 | 재무 보고서에 사용할 행 정의들의 묶음을 관리한다. |
| [`pa_reportsource`](pa/pa_reportsource.md) | 재무 보고서 자료 조건 | Report Source | 93 | 보고서 행에 포함할 자료의 범위를 제한하는 조건을 정의한다. |
| [`pa_sla_criteria`](pa/pa_sla_criteria.md) | 서비스 수준 기준 | SLA Criteria | 2 | 서비스 수준 협약(SLA)의 평가 기준을 정의한다. |
| [`pa_sla_goal`](pa/pa_sla_goal.md) | 서비스 수준 목표 | SLA Goal | 1 | 서비스 수준 협약에서 달성할 목표를 정의한다. |
| [`pa_sla_measure`](pa/pa_sla_measure.md) | 서비스 수준 측정값 | SLA Measure | 1 | 서비스 수준 협약에 대한 측정 결과를 저장한다. |
| [`pp_cost_collector`](pp/pp_cost_collector.md) | 제조 원가 수집 문서 | Manufacturing Cost Collector | 0 | 제조 주문·공정·구성품의 실제 수량과 작업 시간을 기록하여 원가 집계에 사용하는 문서다. |
| [`pp_cost_collectorma`](pp/pp_cost_collectorma.md) | 제조 원가 수집 속성 배분 | Manufacturing Order MA | 0 | 제조 원가 수집 문서의 이동 수량을 속성 집합 인스턴스별로 배분한다. |
| [`pp_mrp`](pp/pp_mrp.md) | 자재 소요 계획 | Material Requirement Planning | 56 | 자재 소요 계획(MRP)에 사용하는 계획 내역을 저장한다. |
| [`pp_order`](pp/pp_order.md) | 제조 주문 | Manufacturing Order | 2 | 지정된 부품 또는 제품을 정해진 수량으로 제조하도록 지시하는 문서다. |
| [`pp_order_bom`](pp/pp_order_bom.md) | 제조 주문 BOM | Manufacturing Order BOM | 2 | 제조 주문에 적용한 BOM 및 배합 정보를 저장한다. 기본 정보는 제품 계획에서 가져온다. |
| [`pp_order_bom_trl`](pp/pp_order_bom_trl.md) | 제조 주문 BOM 번역 | Manufacturing Order BOM Trl | 2 | 제조 주문 BOM의 언어별 번역 정보를 저장한다. |
| [`pp_order_bomline`](pp/pp_order_bomline.md) | 제조 주문 BOM 구성행 | Manufacturing Order BOM Line | 4 | 완제품 제조에 사용할 각 구성품 정보를 주문별 BOM 행으로 저장한다. |
| [`pp_order_bomline_trl`](pp/pp_order_bomline_trl.md) | 제조 주문 BOM 구성행 번역 | Manufacturing Order BOM Line Trl | 4 | 제조 주문 BOM 구성행의 언어별 번역 정보를 저장한다. |
| [`pp_order_cost`](pp/pp_order_cost.md) | 제조 주문 원가 | Manufacturing Order Cost | 0 | 제조할 제품의 원가 요소별 원가 기록을 제조 주문에 연결한다. |
| [`pp_order_node`](pp/pp_order_node.md) | 제조 주문 공정 | Manufacturing Order Activity | 2 | 제조 주문의 작업 경로를 구성하는 개별 공정을 정의한다. |
| [`pp_order_node_asset`](pp/pp_order_node_asset.md) | 제조 주문 공정 자산 | Manufacturing Order Activity Asset | 0 | 제조 주문 공정에 사용하는 자산을 연결한다. |
| [`pp_order_node_product`](pp/pp_order_node_product.md) | 제조 주문 공정 제품 | Manufacturing Order Activity Product | 0 | 제조 주문 공정에 사용하는 제품을 연결한다. |
| [`pp_order_node_trl`](pp/pp_order_node_trl.md) | 제조 주문 공정 번역 | Manufacturing Order Activity Trl | 2 | 제조 주문의 공정 단계에 대한 언어별 번역 정보를 저장한다. |
| [`pp_order_nodenext`](pp/pp_order_nodenext.md) | 제조 주문 공정 전이 | Manufacturing Order Activity Next | 0 | 제조 주문에서 현재 공정과 다음 공정의 연결을 정의한다. |
| [`pp_order_workflow`](pp/pp_order_workflow.md) | 제조 주문 작업 흐름 | Manufacturing Order Workflow | 2 | 제조 주문에 적용한 작업 흐름을 저장한다. |
| [`pp_order_workflow_trl`](pp/pp_order_workflow_trl.md) | 제조 주문 작업 흐름 번역 | Manufacturing Order Workflow Trl | 2 | 제조 주문 작업 흐름의 언어별 번역 정보를 저장한다. |
| [`pp_product_bom`](pp/pp_product_bom.md) | 제품 BOM·배합 | BOM &amp; Formula | 7 | 제품의 자재명세서와 배합을 정의한다. |
| [`pp_product_bom_trl`](pp/pp_product_bom_trl.md) | 제품 BOM·배합 번역 | BOM &amp; Formula Trl | 7 | 제품 자재명세서와 배합의 언어별 번역 정보를 저장한다. |
| [`pp_product_bomline`](pp/pp_product_bomline.md) | 제품 BOM 구성행 | BOM Line | 21 | 완제품의 BOM 및 배합에 들어가는 개별 구성품 정보를 정의한다. |
| [`pp_product_bomline_trl`](pp/pp_product_bomline_trl.md) | 제품 BOM 구성행 번역 | BOM Line Trl | 21 | 제품 BOM 구성행의 언어별 번역 정보를 저장한다. |
| [`pp_product_planning`](pp/pp_product_planning.md) | 제품 생산·조달 계획 | Product Planning | 219 | 제품에 적용하는 생산 및 조달 계획 정보를 정의한다. |
| [`pp_wf_node_asset`](pp/pp_wf_node_asset.md) | 작업 흐름 공정 자산 | Workflow Node Asset | 0 | 작업 흐름의 공정 단계에서 사용하는 자산을 연결한다. |
| [`pp_wf_node_product`](pp/pp_wf_node_product.md) | 작업 흐름 공정 제품 | Workflow Node Product | 0 | 작업 흐름의 공정 단계에서 사용하는 제품을 연결한다. |
| [`qm_specification`](qm/qm_specification.md) | 품질 규격 | Quality Specification | 0 | 제품 품질을 판정하는 규격을 정의한다. |
| [`qm_specificationline`](qm/qm_specificationline.md) | 품질 규격 조건행 | QM Specification Line | 0 | 품질 규격에서 검사할 속성·비교 연산·기준값과 유효기간을 정의한다. |
| [`r_category`](r/r_category.md) | 요청 분류 | Category | 3 | 고객 등의 요청을 분류하는 범주를 정의한다. |
| [`r_categoryupdates`](r/r_categoryupdates.md) | 요청 분류 알림 수신자 | R_CategoryUpdates | 1 | 요청 분류에 연결된 갱신 알림 수신 사용자와 셀프서비스 여부를 저장한다. |
| [`r_contactinterest`](r/r_contactinterest.md) | 연락처 관심 분야 | R_ContactInterest | 1 | 사용자별 관심 분야와 구독 시작·해지일을 저장한다. |
| [`r_group`](r/r_group.md) | 요청 그룹 | Group | 2 | 요청을 함께 관리하는 그룹을 정의한다. |
| [`r_groupupdates`](r/r_groupupdates.md) | 요청 그룹 알림 수신자 | R_GroupUpdates | 1 | 요청 그룹에 연결된 갱신 알림 수신 사용자와 셀프서비스 여부를 저장한다. |
| [`r_interestarea`](r/r_interestarea.md) | 관심 분야 | Interest Area | 2 | 관심 분야 또는 주제를 정의한다. |
| [`r_issueknown`](r/r_issueknown.md) | 알려진 문제 | Known Issue | 0 | 이미 알려진 문제 정보를 관리한다. |
| [`r_issueproject`](r/r_issueproject.md) | 문제 관련 프로젝트 | Issue Project | 0 | 문제 보고와 관련된 프로젝트·자산 및 시스템 상태·통계 정보를 연결한다. |
| [`r_issuerecommendation`](r/r_issuerecommendation.md) | 문제 권고 사항 | Issue Recommendation | 0 | 문제에 대한 권고 사항의 이름·설명·도움말을 정의한다. |
| [`r_issuesource`](r/r_issuesource.md) | 문제 발생 출처 | — | 0 | 문제 관련 시스템·프로젝트·사용자를 통계 및 프로파일 정보와 연결한다. 상세 수집 방식은 확인이 필요하다. |
| [`r_issuestatus`](r/r_issuestatus.md) | 문제 상태 | Issue Status | 0 | 문제를 구분하는 상태의 이름과 설명을 정의한다. |
| [`r_issuesystem`](r/r_issuesystem.md) | 문제 관련 시스템 | Issue System | 0 | 문제 보고와 관련된 시스템의 자산·DB 주소·상태 및 통계 정보를 저장한다. |
| [`r_issueuser`](r/r_issueuser.md) | 문제 보고 사용자 | Issue User | 0 | 문제를 보고한 사용자의 정보를 관리한다. |
| [`r_mailtext`](r/r_mailtext.md) | 메일 본문 서식 | Mail Template | 3 | 메일 발송에 사용하는 텍스트 서식을 저장한다. |
| [`r_mailtext_trl`](r/r_mailtext_trl.md) | 메일 본문 서식 번역 | Mail Template Trl | 3 | 메일 텍스트 서식의 언어별 번역 정보를 저장한다. |
| [`r_request`](r/r_request.md) | 고객·잠재고객 요청 | Request | 1 | 거래처 또는 잠재고객이 제기한 요청을 관리하는 기본 테이블이다. |
| [`r_requestaction`](r/r_requestaction.md) | 요청 변경 이력 | Request History | 2 | 요청의 상태·담당자·분류·우선순위 및 관련 업무 문서 등의 변경 이력을 저장한다. |
| [`r_requestprocessor`](r/r_requestprocessor.md) | 요청 자동 처리기 | Request Processor | 1 | 요청 처리의 실행 주기와 기한 초과·미활동 알림 및 담당 재배정 기준을 정의한다. |
| [`r_requestprocessor_route`](r/r_requestprocessor_route.md) | 요청 자동 배정 규칙 | Request Routing | 1 | 요청을 자동으로 적절한 담당 경로에 배정하는 규칙을 정의한다. |
| [`r_requestprocessorlog`](r/r_requestprocessorlog.md) | 요청 처리 로그 | Request Processor Log | 0 | 요청 처리기의 실행 요약·오류 여부와 상세 메시지를 기록한다. |
| [`r_requesttype`](r/r_requesttype.md) | 요청 유형 | Request Type | 3 | 문의·불만 등 요청의 업무 유형을 정의한다. |
| [`r_requesttypeupdates`](r/r_requesttypeupdates.md) | 요청 유형 알림 수신자 | Request Type Updates | 1 | 요청 유형에 연결된 갱신 알림 수신 사용자와 셀프서비스 여부를 저장한다. |
| [`r_requestupdate`](r/r_requestupdate.md) | 요청 처리 기록 | Request Update | 1 | 요청의 처리 결과·작업 시간·투입 및 청구 수량을 개별 기록으로 저장한다. |
| [`r_requestupdates`](r/r_requestupdates.md) | 요청 알림 수신자 | Request Update Recipiants | 0 | 개별 요청의 갱신 알림을 받는 사용자와 셀프서비스 여부를 저장한다. |
| [`r_resolution`](r/r_resolution.md) | 요청 해결 유형 | Resolution | 3 | 요청이 어떤 방식으로 해결되었는지 구분하는 값을 정의한다. |
| [`r_standardresponse`](r/r_standardresponse.md) | 요청 표준 답변 | Standard Response | 1 | 요청에 응답할 때 사용하는 표준 답변을 정의한다. |
| [`r_status`](r/r_status.md) | 요청 상태 | Status | 4 | 요청의 진행 상태를 정의한다. |
| [`r_statuscategory`](r/r_statuscategory.md) | 요청 상태 분류 | Status Category | 1 | 요청 상태들을 묶는 분류를 정의한다. |
| [`s_expensetype`](s/s_expensetype.md) | 경비 유형 | Expense Type | 1 | 경비 보고에 사용하는 경비 유형을 정의한다. |
| [`s_resource`](s/s_resource.md) | 업무 자원 | Resource | 11 | 업무에 배정하는 자원의 기본 정보를 정의한다. |
| [`s_resourceassignment`](s/s_resourceassignment.md) | 자원 배정 | Resource Assignment | 2 | 자원에 대한 업무 배정 정보를 저장한다. |
| [`s_resourcetype`](s/s_resourcetype.md) | 자원 유형 | Resource Type | 3 | 자원 유형별 시간대·요일·단위와 단일 배정 여부 등을 정의한다. |
| [`s_resourceunavailable`](s/s_resourceunavailable.md) | 자원 사용 불가 기간 | Resource Unavailability | 2 | 자원을 사용할 수 없는 시작·종료일과 사유를 저장한다. |
| [`s_timeexpense`](s/s_timeexpense.md) | 작업 시간·경비 보고 | Expense Report | 1 | 투입 시간과 경비를 보고하는 문서의 기본 정보를 저장한다. |
| [`s_timeexpenseline`](s/s_timeexpenseline.md) | 작업 시간·경비 보고행 | Expense Line | 4 | 시간·경비 보고서의 개별 내역을 저장한다. |
| [`s_timetype`](s/s_timetype.md) | 기록 시간 유형 | Time Type | 0 | 기록한 시간을 구분하는 유형을 정의한다. |
| [`s_training`](s/s_training.md) | 교육 과정 | Training | 1 | 반복 운영하는 교육 과정의 기본 정의를 저장한다. |
| [`s_training_class`](s/s_training_class.md) | 교육 개설 회차 | Training Class | 0 | 교육 과정이 실제로 개설된 개별 회차를 저장한다. |
| [`sso_principalconfig`](sso/sso_principalconfig.md) | 통합 로그인 설정 | SSO Configuration | 0 | SSO 제공자와 애플리케이션 식별자·리디렉션 주소 등 통합 로그인 연결 설정을 저장한다. |
| [`t_1099extract`](t/t_1099extract.md) | 1099 신고 추출 자료 | 1099 Extract | 0 | 실행 건별 거래처·납세자 식별자와 연도별 금액 구간을 저장하는 1099 신고용 추출 자료다. |
| [`t_aging`](t/t_aging.md) | 채권·채무 연령 분석 자료 | T_Aging | 0 | 실행 건별 송장 미결 금액을 만기 경과 및 도래 기간 구간으로 나눈 보고용 자료다. |
| [`t_alter_column`](t/t_alter_column.md) | 열 변경 정의 | — | 0 | 테이블·열 이름과 변경할 자료형·NULL·기본값 절을 저장한다. 실제 실행 및 보관 용도는 코드 확인이 필요하다. |
| [`t_bankregister`](t/t_bankregister.md) | 은행 거래부 자료 | Bank Register | 0 | 실행 건별 은행·계정·거래처와 회계일·차대변 금액·잔액을 저장하는 거래부 보고 자료다. |
| [`t_bom_indented`](t/t_bom_indented.md) | 계층형 BOM 보고 자료 | Indented BOM Report | 0 | BOM을 계층 들여쓰기 형태로 표시하기 위한 보고 자료를 저장한다. |
| [`t_bomline`](t/t_bomline.md) | BOM 임시 전개행 | Temporal BOM Line | 0 | BOM 전개 및 역전개 결과의 계층·제품·구성 수량·원가를 실행 건별로 임시 저장한다. |
| [`t_cashflow`](t/t_cashflow.md) | 현금 흐름 보고 자료 | T_CashFlow_ID | 0 | 송장·주문·현금 계획 등을 원천으로 한 금액·거래일·확률을 실행 건별로 저장한다. |
| [`t_distributionrundetail`](t/t_distributionrundetail.md) | 배분 실행 계산 자료 | T_DistributionRunDetail | 0 | 배분 실행에서 거래처·제품별 배분 비율과 최소 수량·계산 수량을 저장한다. |
| [`t_fact_acct_history`](t/t_fact_acct_history.md) | 회계 전기 이력 자료 | Accounting Fact History | 0 | 회계 전기 레코드와 동일한 계정·차대변 금액·업무 차원 등의 이력 정보를 저장한다. 이력 생성 및 보존 조건은 확인이 필요하다. |
| [`t_inventoryvalue`](t/t_inventoryvalue.md) | 재고 평가 보고 자료 | T_InventoryValue | 0 | 실행 건별 제품·창고·속성 인스턴스의 재고 수량과 가격·원가 기준 평가 금액을 저장한다. |
| [`t_invoicegl`](t/t_invoicegl.md) | 송장 환산 손익 자료 | T_InvoiceGL | 0 | 송장과 회계 전기별 미결 금액·통화 잔액·재평가 차액을 저장한다. 사전 설명상 실제 표시 자료는 T_InvoiceGL_v에서 제공된다. |
| [`t_moveclient`](t/t_moveclient.md) | 테넌트 이동 키 대응 | — | 0 | 실행 건별 테이블의 원본 키와 대상 키 및 식별자를 저장한다. 실제 테넌트 이동 절차에서의 사용 방식은 확인이 필요하다. |
| [`t_mrp_crp`](t/t_mrp_crp.md) | 소요·능력 계획 임시 자료 | Temporal MRP &amp; CRP | 0 | MRP 및 CRP 처리의 실행 건별 순서와 설명을 임시 저장한다. |
| [`t_reconciliation`](t/t_reconciliation.md) | 계정 대사 보고 자료 | Account reconciliation report | 0 | 보고서 실행 건별 회계 전기 레코드와 대사 코드를 연결한다. |
| [`t_replenish`](t/t_replenish.md) | 재고 보충 계산 자료 | T_Replenish | 0 | 실행 건별 현재고·예약·주문 수량과 보충 수준을 바탕으로 계산한 발주 수량을 저장한다. |
| [`t_report`](t/t_report.md) | 보고서 임시 자료 | T_Report | 0 | 보고서 생성 중 사용하는 행별 임시 결과를 저장한다. |
| [`t_reportstatement`](t/t_reportstatement.md) | 계정 명세 보고 자료 | T_ReportStatement | 0 | 실행 건별 회계 전기의 일자·차대변 금액·잔액·수량을 명세서용으로 저장한다. |
| [`t_selection`](t/t_selection.md) | 처리 대상 선택값 | — | 0 | 프로세스 실행 건에 선택된 레코드 식별자와 뷰 식별자를 연결한다. |
| [`t_selection2`](t/t_selection2.md) | 질의별 처리 대상 선택값 | — | 0 | 프로세스 실행 건과 질의 식별자별로 선택된 레코드 식별자를 저장한다. |
| [`t_selection_infowindow`](t/t_selection_infowindow.md) | 정보 창 선택 자료 | — | 0 | 정보 창에서 선택한 레코드의 열별 문자·날짜·숫자 값을 실행 건과 연결한다. |
| [`t_spool`](t/t_spool.md) | 임시 출력 메시지 | T_Spool | 0 | 임시 출력에 사용하는 메시지를 저장한다. |
| [`t_transaction`](t/t_transaction.md) | 재고 수불 보고 자료 | T_Transaction | 0 | 실행 건별 재고 거래와 관련 입출고·이동·실사·생산 문서의 정보를 보고용으로 저장한다. |
| [`t_trialbalance`](t/t_trialbalance.md) | 시산표 보고 자료 | Trial Balance | 0 | 실행 건별 계정·회계 전기의 차대변 금액과 잔액을 시산표용으로 저장한다. |
| [`test`](other/test.md) | 자료형 시험 | Test ID | 2 | 문자·숫자·날짜·금액·JSON 및 업무 참조 등 여러 자료형을 시험하는 테이블이다. 업무 원장으로 해석하지 않는다. |
| [`testuu`](other/testuu.md) | UUID 기반 시험 | Test UU Based Table | 2 | UUID 기반 테이블 기능을 시험하는 이름·값·설명 데이터를 저장한다. |
| [`testuu_trl`](testuu/testuu_trl.md) | UUID 시험 번역 | Test UU Based Table Trl | 2 | UUID 기반 시험 테이블의 언어별 번역 데이터를 저장한다. |
| [`testuudet`](other/testuudet.md) | UUID 시험 상세 | Test UU Detail | 3 | UUID 기반 시험 레코드와 연결된 상세 이름을 저장한다. |
| [`u_blacklistcheque`](u/u_blacklistcheque.md) | 사용 제한 수표 | Black List Cheque | 0 | 은행 이름과 사용 제한 대상으로 등록된 수표 번호를 저장한다. |
| [`u_posterminal`](u/u_posterminal.md) | 판매시점 단말기 | POS Terminal | 1 | POS 단말기의 창고·가격표·담당자·프린터 및 현금·카드·수표 결제 연결 설정을 저장한다. |
| [`u_rolemenu`](u/u_rolemenu.md) | 역할별 웹 메뉴 | Role Menu | 74 | 사용자 역할과 접근할 웹 메뉴를 연결한다. |
| [`u_web_properties`](u/u_web_properties.md) | 웹 속성 설정 | Web Properties | 143 | 웹 기능에 사용하는 키·값 형태의 설정을 저장한다. |
| [`u_webmenu`](u/u_webmenu.md) | 웹 메뉴 | Web Menu | 143 | 웹 메뉴의 링크·상위 메뉴·표시 순서·이미지 등 탐색 구조를 정의한다. |
| [`w_advertisement`](w/w_advertisement.md) | 웹 광고 | Advertisement | 1 | 웹에 게시하는 광고 정보를 저장한다. |
| [`w_basket`](w/w_basket.md) | 웹 장바구니 | Basket | 0 | 웹 상점의 장바구니 기본 정보를 저장한다. |
| [`w_basketline`](w/w_basketline.md) | 웹 장바구니행 | Basket Line | 0 | 장바구니에 담긴 개별 품목 내역을 저장한다. |
| [`w_click`](w/w_click.md) | 웹 클릭 기록 | Web Click | 0 | 웹에서 발생한 개별 클릭을 기록한다. |
| [`w_clickcount`](w/w_clickcount.md) | 웹 클릭 집계 | Click Count | 1 | 웹 클릭 수를 관리하는 집계 정보를 저장한다. |
| [`w_counter`](w/w_counter.md) | 웹 방문 집계 원천 | Web Counter | 0 | 개별 웹 접근 횟수 기록을 저장한다. |
| [`w_countercount`](w/w_countercount.md) | 웹 방문 수 집계 | Counter Count | 1 | 웹 카운터의 누적 횟수를 관리한다. |
| [`w_mailmsg`](w/w_mailmsg.md) | 웹 상점 메일 서식 | Mail Message | 0 | 웹 상점에서 발송하는 메일 메시지의 서식을 저장한다. |
| [`w_mailmsg_trl`](w/w_mailmsg_trl.md) | 웹 상점 메일 서식 번역 | Mail Message Trl | 0 | 웹 상점 메일 메시지 서식의 언어별 번역 정보를 저장한다. |
| [`w_store`](w/w_store.md) | 웹 상점 | Web Store | 1 | 테넌트가 운영하는 웹 상점의 기본 정보를 정의한다. |
| [`w_store_trl`](w/w_store_trl.md) | 웹 상점 번역 | Web Store Trl | 1 | 웹 상점의 언어별 번역 정보를 저장한다. |
| [`ws_webservice`](ws/ws_webservice.md) | 웹 서비스 정의 | Web Service | 2 | 웹 서비스의 코드·이름·설명과 도움말을 정의한다. |
| [`ws_webservice_para`](ws/ws_webservice_para.md) | 웹 서비스 매개변수 | Web Service Parameters | 46 | 웹 서비스 유형에 속하는 매개변수 이름·유형 및 상수값을 정의한다. |
| [`ws_webservicefieldinput`](ws/ws_webservicefieldinput.md) | 웹 서비스 입력 필드 | Web Service Field Input | 45 | 웹 서비스 유형별 입력 열과 참조·식별자 판정 규칙을 정의한다. |
| [`ws_webservicefieldoutput`](ws/ws_webservicefieldoutput.md) | 웹 서비스 출력 필드 | Web Service Field Output | 8 | 웹 서비스 유형이 응답에 포함할 테이블 열을 정의한다. |
| [`ws_webservicemethod`](ws/ws_webservicemethod.md) | 웹 서비스 메서드 | Web Service Method | 9 | 웹 서비스에 속하는 개별 호출 메서드의 코드·이름·설명을 정의한다. |
| [`ws_webservicetype`](ws/ws_webservicetype.md) | 웹 서비스 유형 | Web Service Type | 16 | 서비스와 메서드를 대상 테이블 및 매개변수 삽입 설정에 연결한다. |
| [`ws_webservicetypeaccess`](ws/ws_webservicetypeaccess.md) | 웹 서비스 유형 접근 권한 | Web Service Type Access | 16 | 역할별 웹 서비스 유형 접근과 읽기·쓰기 권한을 정의한다. |
