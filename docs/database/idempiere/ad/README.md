# ad — 애플리케이션 사전·화면·권한·시스템

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 258개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`ad_accesslog`](ad_accesslog.md) | 시스템 접근 로그 | Access Log | 0 | 시스템에 접근한 내역을 기록한다. |
| [`ad_alert`](ad_alert.md) | 알림 정의 | Alert | 1 | 시스템 알림을 정의하고 관련 처리 설정을 관리한다. |
| [`ad_alertprocessor`](ad_alertprocessor.md) | 알림 처리기 | Alert Processor | 1 | 알림 처리 서버와 실행 매개변수를 관리한다. |
| [`ad_alertprocessorlog`](ad_alertprocessorlog.md) | 알림 처리 로그 | Alert Processor Log | 0 | 알림 처리기의 실행 결과를 기록한다. |
| [`ad_alertrecipient`](ad_alertrecipient.md) | 알림 수신 대상 | Alert Recipient | 1 | 알림 통지를 받을 수신 대상을 지정한다. |
| [`ad_alertrule`](ad_alertrule.md) | 알림 규칙 | Alert Rule | 1 | 알림을 구성하는 규칙을 정의한다. |
| [`ad_archive`](ad_archive.md) | 문서 보관 | Archive | 0 | 보관 대상 문서의 정보를 관리한다. |
| [`ad_archive_blob`](ad_archive_blob.md) | 보관 문서 바이너리 | — | 0 | 문서 보관 항목에 연결된 바이너리 데이터를 저장한다. |
| [`ad_attachment`](ad_attachment.md) | 첨부 문서 | Attachment | 1 | 문서에 연결된 첨부 정보를 관리한다. |
| [`ad_attachment_entry`](ad_attachment_entry.md) | 첨부 바이너리 항목 | — | 0 | 첨부 문서에 속한 바이너리 데이터를 순번별로 저장한다. |
| [`ad_attachmentfile`](ad_attachmentfile.md) | 첨부 파일 메타데이터 | Attachment File | 0 | 첨부 파일의 이름·크기·형식·경로·체크섬과 순서를 기록한다. |
| [`ad_attachmentnote`](ad_attachmentnote.md) | 첨부 개인 메모 | Attachment Note | 0 | 첨부 문서에 대한 개인 메모를 관리한다. |
| [`ad_attribute`](ad_attribute.md) | 시스템 확장 속성 | System Attribute | 0 | 테이블에 적용할 속성의 참조 유형·검증·기본값·입력 및 표시 규칙을 정의한다. |
| [`ad_attribute_value`](ad_attribute_value.md) | 시스템 속성값 | AD_Attribute_Value | 0 | 레코드별 시스템 속성값을 숫자·날짜·문자 유형으로 저장한다. |
| [`ad_authorizationaccount`](ad_authorizationaccount.md) | 외부 서비스 인가 계정 | Authorization Account | 0 | 사용자와 외부 서비스 인가 자격을 연결하고 토큰·유효시간·인가 상태를 관리한다. 실제 자격정보 값은 문서에 포함하지 않는다. |
| [`ad_authorizationcredential`](ad_authorizationcredential.md) | 외부 서비스 인가 자격 설정 | Authorization Credential | 0 | 인가 제공자별 클라이언트 식별자·비밀정보·리디렉션 주소와 요청 범위를 설정한다. 실제 자격정보 값은 문서에 포함하지 않는다. |
| [`ad_authorizationprovider`](ad_authorizationprovider.md) | 외부 서비스 인가 제공자 | Authorization Provider | 2 | 외부 서비스의 인가·토큰 발급·취소 주소와 인가 유형을 정의한다. |
| [`ad_authorizationscopeprov`](ad_authorizationscopeprov.md) | 인가 제공자별 권한 범위 | Authorization Scope Provider | 3 | 인가 제공자에 연결된 권한 범위와 범위 주소를 정의한다. |
| [`ad_broadcastmessage`](ad_broadcastmessage.md) | 전체 공지 | Broadcast Message | 0 | 시스템 사용자에게 전달할 공지 메시지를 관리한다. |
| [`ad_broadcastmessage_trl`](ad_broadcastmessage_trl.md) | 전체 공지 번역 | Broadcast Message Trl | 0 | 전체 공지 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_changelog`](ad_changelog.md) | 데이터 변경 로그 | Change Log | 0 | 데이터 변경 내역을 기록한다. |
| [`ad_chart`](ad_chart.md) | 차트 정의 | Chart | 4 | 정보를 그래프로 표시하기 위한 차트를 정의한다. |
| [`ad_chart_trl`](ad_chart_trl.md) | 차트 정의 번역 | Chart Trl | 4 | 차트 정의 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_chartdatasource`](ad_chartdatasource.md) | 차트 데이터 원천 | Chart Datasource | 6 | 차트에 표시할 데이터를 조회하는 쿼리를 정의한다. |
| [`ad_chartdatasource_trl`](ad_chartdatasource_trl.md) | 차트 데이터 원천 번역 | Chart Datasource Trl | 6 | 차트 데이터 원천 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_client`](ad_client.md) | 테넌트 | Tenant | 2 | 하나의 설치 환경에서 구분되는 테넌트를 정의한다. |
| [`ad_clientinfo`](ad_clientinfo.md) | 테넌트 상세 설정 | AD_ClientInfo | 2 | 테넌트의 회계 스키마·달력·단위·업무 트리·저장소 등 공통 설정을 관리한다. |
| [`ad_clientshare`](ad_clientshare.md) | 테넌트·조직 데이터 공유 규칙 | Tenant Share | 0 | 테넌트와 조직 간 데이터 공유 또는 공유 금지 규칙을 관리한다. |
| [`ad_color`](ad_color.md) | 시스템 색상 | System Color | 0 | 배경이나 상태 표시 등에 사용할 색상을 정의한다. |
| [`ad_color_trl`](ad_color_trl.md) | 시스템 색상 번역 | System Color Trl | 0 | 시스템 색상 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_column`](ad_column.md) | 애플리케이션 사전 열 | Column | 26,476 | 테이블 열에 대한 애플리케이션 사전 정의를 관리한다. |
| [`ad_column_access`](ad_column_access.md) | 열 접근 권한 | AD_Column_Access | 0 | 역할별 테이블 열 접근 제외 여부와 읽기 전용 여부를 설정한다. |
| [`ad_column_trl`](ad_column_trl.md) | 애플리케이션 사전 열 번역 | Column Trl | 26,476 | 애플리케이션 사전 열 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_ctxhelp`](ad_ctxhelp.md) | 화면별 도움말 연결 | Context Help | 1 | 탭·프로세스·폼 등 화면 구성요소에 문맥 도움말을 연결한다. |
| [`ad_ctxhelpmsg`](ad_ctxhelpmsg.md) | 문맥 도움말 메시지 | Context Help Message | 1 | 문맥 도움말에 속한 메시지를 줄 순서별로 관리한다. |
| [`ad_ctxhelpmsg_trl`](ad_ctxhelpmsg_trl.md) | 문맥 도움말 메시지 번역 | Context Help Message Trl | 1 | 문맥 도움말 메시지 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_ctxhelpsuggestion`](ad_ctxhelpsuggestion.md) | 문맥 도움말 제안 | Context Help Suggestion | 0 | 문맥 도움말 내용을 개선하기 위한 제안을 관리한다. |
| [`ad_desktop`](ad_desktop.md) | 데스크톱 구성 | Desktop | 1 | 여러 작업 공간을 묶어 데스크톱 구성을 정의한다. |
| [`ad_desktop_trl`](ad_desktop_trl.md) | 데스크톱 구성 번역 | Desktop Trl | 1 | 데스크톱 구성 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_desktopworkbench`](ad_desktopworkbench.md) | 데스크톱 작업 공간 배치 | Desktop Workbench | 1 | 데스크톱에 포함할 작업 공간과 표시 순서를 지정한다. |
| [`ad_document_action_access`](ad_document_action_access.md) | 문서 작업 권한 | Document Action Access | 2,156 | 테넌트·역할·문서 유형·문서 작업 조합에 대한 접근 규칙을 정의한다. 원본 도움말에 따르면 특정 테넌트·유형·작업 조합에 규칙이 없으면 모든 역할이 접근할 수 있다. |
| [`ad_element`](ad_element.md) | 공통 데이터 요소 | System Element | 5,985 | 여러 열에서 사용하는 설명과 도움말을 중앙에서 관리한다. |
| [`ad_element_trl`](ad_element_trl.md) | 공통 데이터 요소 번역 | System Element Trl | 5,985 | 공통 데이터 요소 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_entitytype`](ad_entitytype.md) | 엔터티 유형 | Entity Type | 12 | 시스템 구성요소를 구분하는 엔터티 유형을 정의한다. |
| [`ad_error`](ad_error.md) | 오류 코드 | Error | 0 | 언어별 오류 이름과 코드를 관리한다. |
| [`ad_field`](ad_field.md) | 화면 필드 | Field | 21,281 | 데이터베이스 열을 화면 필드로 표현하기 위한 정의를 관리한다. |
| [`ad_field_trl`](ad_field_trl.md) | 화면 필드 번역 | Field Trl | 21,281 | 화면 필드 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_fieldgroup`](ad_fieldgroup.md) | 필드 그룹 | Field Group | 79 | 관련 필드를 논리적 그룹으로 묶는다. |
| [`ad_fieldgroup_trl`](ad_fieldgroup_trl.md) | 필드 그룹 번역 | Field Group Trl | 79 | 필드 그룹 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_fieldsuggestion`](ad_fieldsuggestion.md) | 필드 문구 제안 | Field Suggestions | 0 | 필드의 표시 이름·설명·도움말에 대한 개선 제안을 관리한다. |
| [`ad_find`](ad_find.md) | 검색 조건 항목 | Find | 0 | 검색에 사용할 열·연산자·값과 조건 결합 방식을 기록한다. |
| [`ad_form`](ad_form.md) | 특수 폼 | Special Form | 51 | 일반 데이터 창과 구분되는 특수 폼을 정의한다. |
| [`ad_form_access`](ad_form_access.md) | 특수 폼 접근 권한 | AD_Form_Access | 137 | 역할별 특수 폼 접근 및 읽기·쓰기 권한을 설정한다. |
| [`ad_form_trl`](ad_form_trl.md) | 특수 폼 번역 | Special Form Trl | 51 | 특수 폼 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_housekeeping`](ad_housekeeping.md) | 데이터 정리 설정 | House Keeping Configuration | 10 | 테이블별 정리 조건·백업 옵션과 최근 실행·삭제 정보를 관리한다. |
| [`ad_image`](ad_image.md) | 시스템 이미지 | Image | 10 | 시스템에서 사용할 이미지나 아이콘을 관리한다. |
| [`ad_image_blob`](ad_image_blob.md) | 이미지 바이너리 | — | 0 | 시스템 이미지에 연결된 바이너리 데이터를 저장한다. |
| [`ad_impformat`](ad_impformat.md) | 데이터 가져오기 형식 | Import Format | 15 | 가져올 데이터의 대상 테이블·형식·구분자를 정의한다. |
| [`ad_impformat_row`](ad_impformat_row.md) | 가져오기 필드 매핑 | Format Field | 163 | 가져오기 형식에서 각 필드의 위치·데이터 유형·변환 규칙과 대상 열을 지정한다. |
| [`ad_importtemplate`](ad_importtemplate.md) | 데이터 가져오기 템플릿 | Import Template | 0 | 창·탭별 데이터 가져오기에 사용할 문자셋·CSV 헤더·구분자 등 템플릿을 정의한다. |
| [`ad_importtemplateaccess`](ad_importtemplateaccess.md) | 가져오기 템플릿 권한 | Import Template Access | 0 | 역할별 가져오기 템플릿의 삽입·병합·수정 허용 여부를 관리한다. |
| [`ad_indexcolumn`](ad_indexcolumn.md) | 인덱스 구성 열 | Table Index Column | 1,537 | 테이블 인덱스를 구성하는 열의 정의를 관리한다. |
| [`ad_infocolumn`](ad_infocolumn.md) | 조회 창 열 | Info Column | 198 | 조회 창에 표시할 열과 검색 조건·표현식·참조·입력 규칙을 정의한다. |
| [`ad_infocolumn_trl`](ad_infocolumn_trl.md) | 조회 창 열 번역 | Info Column Trl | 198 | 조회 창 열 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_infoprocess`](ad_infoprocess.md) | 조회 창 프로세스 | Info Process | 11 | 조회 창에서 사용할 프로세스를 연결한다. |
| [`ad_inforelated`](ad_inforelated.md) | 연관 조회 창 | Info Related | 0 | 조회 창 사이의 연관 관계와 연결 열·표시 조건을 정의한다. |
| [`ad_infowindow`](ad_infowindow.md) | 조회 창 | Info Window | 17 | 검색·선택용 조회 창의 대상 테이블·SQL 구성·정렬·페이지 설정을 정의한다. |
| [`ad_infowindow_access`](ad_infowindow_access.md) | 조회 창 접근 권한 | Info Window Access | 54 | 역할에 허용되는 조회 창을 연결한다. |
| [`ad_infowindow_trl`](ad_infowindow_trl.md) | 조회 창 번역 | Info Window Trl | 17 | 조회 창 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_issue`](ad_issue.md) | 시스템 오류 보고 | System Issue | 0 | 오류 요약·발생 위치·실행환경·스택 추적 및 관련 요청 정보를 기록한다. |
| [`ad_label`](ad_label.md) | 레코드 라벨 | Label | 0 | 레코드 분류에 사용할 라벨을 정의한다. |
| [`ad_label_trl`](ad_label_trl.md) | 레코드 라벨 번역 | Label Trl | 0 | 레코드 라벨 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_labelassignment`](ad_labelassignment.md) | 레코드 라벨 부여 | Label Assignment | 0 | 테이블의 특정 레코드에 라벨을 연결한다. |
| [`ad_labelcategory`](ad_labelcategory.md) | 라벨 분류 | Label Category | 0 | 라벨을 묶는 분류를 정의한다. |
| [`ad_labelcategory_trl`](ad_labelcategory_trl.md) | 라벨 분류 번역 | Label Category Trl | 0 | 라벨 분류 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_labelcategorytable`](ad_labelcategorytable.md) | 라벨 분류 적용 테이블 | Label Category Table Access | 0 | 라벨 분류를 적용할 수 있는 테이블을 연결한다. |
| [`ad_labelprinter`](ad_labelprinter.md) | 라벨 프린터 | Label printer | 0 | 라벨 출력에 사용할 프린터를 정의한다. |
| [`ad_labelprinterfunction`](ad_labelprinterfunction.md) | 라벨 프린터 기능 | Label printer Function | 0 | 라벨 프린터의 기능을 정의한다. |
| [`ad_language`](ad_language.md) | 언어·지역 설정 | Language ID | 109 | 언어 코드와 국가·날짜·시간·숫자 표시 방식 및 시스템 사용 여부를 관리한다. |
| [`ad_ldapaccess`](ad_ldapaccess.md) | LDAP 접근 로그 | Ldap Access | 0 | LDAP 접근 내역을 기록한다. |
| [`ad_ldapprocessor`](ad_ldapprocessor.md) | LDAP 처리 서버 | Ldap Processor | 1 | LDAP 서버 처리 설정을 관리한다. |
| [`ad_ldapprocessorlog`](ad_ldapprocessorlog.md) | LDAP 처리 로그 | Ldap Processor Log | 0 | LDAP 서버의 처리 로그를 기록한다. |
| [`ad_menu`](ad_menu.md) | 메뉴 | Menu | 813 | 시스템 메뉴 항목을 정의한다. |
| [`ad_menu_trl`](ad_menu_trl.md) | 메뉴 번역 | Menu Trl | 813 | 메뉴 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_message`](ad_message.md) | 시스템 메시지 | Message | 2,105 | 시스템에서 표시할 메시지를 관리한다. |
| [`ad_message_trl`](ad_message_trl.md) | 시스템 메시지 번역 | Message Trl | 2,105 | 시스템 메시지 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_migrationscript`](ad_migrationscript.md) | 마이그레이션 스크립트 | Migration Script | 1,341 | 시스템 마이그레이션 스크립트 정보를 관리한다. |
| [`ad_modelgeneratortemplate`](ad_modelgeneratortemplate.md) | 모델 생성 템플릿 | Model Generator Template | 0 | 모델 코드 생성에 사용할 테이블·열 엔터티 범위와 패키지·출력 폴더를 설정한다. |
| [`ad_modelvalidator`](ad_modelvalidator.md) | 전역 모델 검증기 | Model Validator | 3 | 시스템 전역에 적용하는 모델 검증기를 정의한다. |
| [`ad_modification`](ad_modification.md) | 변경 정의 | Modification | 0 | 변경 항목의 이름·설명·엔터티 유형·버전과 순서를 기록한다. 구체적인 적용 절차는 이 메타데이터만으로 확정할 수 없다. |
| [`ad_note`](ad_note.md) | 시스템 통지 | Notice | 0 | 시스템 통지 내용을 관리한다. |
| [`ad_org`](ad_org.md) | 조직 | Organization | 10 | 테넌트 내부의 조직 단위를 정의한다. |
| [`ad_orginfo`](ad_orginfo.md) | 조직 상세 정보 | Organization Info | 10 | 조직의 주소·세무 정보·상위 조직·창고·연락처 등 상세 설정을 관리한다. |
| [`ad_orgtype`](ad_orgtype.md) | 조직 유형 | Organization Type | 3 | 조직을 분류하는 유형을 정의한다. |
| [`ad_package_exp`](ad_package_exp.md) | 패키지 내보내기 | Package Exp. | 0 | 내보낼 구성 패키지의 이름·버전·파일 위치와 처리 옵션을 관리한다. |
| [`ad_package_exp_common`](ad_package_exp_common.md) | 공통 내보내기 구성요소 | Common Package Exp. | 0 | 현재 인스턴스에서 만드는 모든 패키지에 공통으로 포함할 구성요소를 관리한다. |
| [`ad_package_exp_detail`](ad_package_exp_detail.md) | 내보내기 패키지 상세 | Package Exp. Detail | 0 | 내보내기 패키지에 포함할 창·프로세스·테이블·파일·SQL 등 개별 구성요소를 지정한다. |
| [`ad_package_imp`](ad_package_imp.md) | 패키지 가져오기 | Package Imp. | 0 | 가져온 구성 패키지의 버전·상태·생성자 및 제거 관련 정보를 관리한다. |
| [`ad_package_imp_backup`](ad_package_imp_backup.md) | 패키지 적용 전 백업 | Imp. Package Backup | 0 | 패키지 가져오기와 관련된 테이블·열의 원래 값과 백업 위치를 기록한다. |
| [`ad_package_imp_detail`](ad_package_imp_detail.md) | 패키지 가져오기 상세 | Imp. Package Detail | 0 | 패키지의 개별 레코드에 수행한 작업과 성공 여부·결과를 기록한다. |
| [`ad_package_imp_inst`](ad_package_imp_inst.md) | 패키지 설치 정보 | Package Imp. Inst. | 0 | 패키지 설치 항목의 이름·버전·상태와 생성자 정보를 기록한다. |
| [`ad_package_imp_proc`](ad_package_imp_proc.md) | 패키지 가져오기 실행 설정 | Package Imp. Proc. | 0 | 패키지 원천·디렉터리·사전 덮어쓰기 옵션과 처리일·메시지를 관리한다. |
| [`ad_package_uuid_map`](ad_package_uuid_map.md) | 테넌트 간 UUID 매핑 | UUID Mapping | 0 | 테넌트 사이의 UUID 대응 관계를 관리한다. |
| [`ad_password_history`](ad_password_history.md) | 비밀번호 변경 이력 | Password History ID | 0 | 일정 기간 이전 비밀번호의 재사용을 제한하기 위한 이력을 관리한다. |
| [`ad_passwordrule`](ad_passwordrule.md) | 비밀번호 정책 | Password Policies | 0 | 비밀번호 길이·문자 조합·사전 단어·연속 문자열·재사용 기간 등의 규칙을 설정한다. |
| [`ad_pinstance`](ad_pinstance.md) | 프로세스 실행 인스턴스 | Process Instance | 0 | 개별 프로세스 실행 인스턴스를 관리한다. |
| [`ad_pinstance_log`](ad_pinstance_log.md) | 프로세스 실행 로그 | AD_PInstance_Log | 0 | 프로세스 실행 인스턴스에 연결된 로그를 기록한다. |
| [`ad_pinstance_para`](ad_pinstance_para.md) | 프로세스 실행 인수 | AD_PInstance_Para | 0 | 프로세스 실행 시 전달한 문자열·숫자·날짜 인수와 범위 값을 기록한다. |
| [`ad_postit`](ad_postit.md) | 레코드 메모 | Post-it | 0 | 특정 테이블의 레코드에 붙인 메모를 저장한다. |
| [`ad_preference`](ad_preference.md) | 개인 환경설정 | Preference | 17 | 개인별 환경설정 값을 관리한다. |
| [`ad_printcolor`](ad_printcolor.md) | 출력 색상 | Print Color | 23 | 출력과 화면 표시에 사용할 색상을 정의한다. |
| [`ad_printcolor_trl`](ad_printcolor_trl.md) | 출력 색상 번역 | Print Color | 23 | 출력 색상 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_printfont`](ad_printfont.md) | 출력 글꼴 | Print Font | 66 | 인쇄에 사용할 글꼴을 관리한다. |
| [`ad_printform`](ad_printform.md) | 출력 서식 연결 | Print Form | 2 | 청구서·주문·송금·출하 등 문서 유형별 출력 형식과 메일 문구를 연결한다. |
| [`ad_printformat`](ad_printformat.md) | 출력 형식 | Print Format | 93 | 데이터를 출력하는 형식을 정의한다. |
| [`ad_printformat_trl`](ad_printformat_trl.md) | 출력 형식 번역 | Print Format Trl | 93 | 출력 형식 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_printformatitem`](ad_printformatitem.md) | 출력 형식 항목 | Print Format Item | 2,780 | 출력 형식을 구성하는 개별 항목과 열을 정의한다. |
| [`ad_printformatitem_trl`](ad_printformatitem_trl.md) | 출력 형식 항목 번역 | Print Format Item Trl | 2,780 | 출력 형식 항목 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_printgraph`](ad_printgraph.md) | 보고서 그래프 | Graph | 0 | 보고서에 포함할 그래프를 정의한다. |
| [`ad_printheaderfooter`](ad_printheaderfooter.md) | 출력 머리말·꼬리말 | Print Header/Footer | 0 | 출력 머리말·꼬리말의 이름과 구현 클래스를 정의한다. |
| [`ad_printlabel`](ad_printlabel.md) | 라벨 출력 형식 | Print Label | 0 | 라벨을 인쇄하기 위한 형식을 정의한다. |
| [`ad_printlabelline`](ad_printlabelline.md) | 라벨 출력 줄 | Print Label Line | 0 | 라벨 출력 형식을 구성하는 줄을 정의한다. |
| [`ad_printlabelline_trl`](ad_printlabelline_trl.md) | 라벨 출력 줄 번역 | Print Label Line Trl | 0 | 라벨 출력 줄 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_printpaper`](ad_printpaper.md) | 인쇄 용지 | Print Paper | 4 | 인쇄 용지 규격을 정의한다. |
| [`ad_printtableformat`](ad_printtableformat.md) | 보고서 표 형식 | Print Table Format | 2 | 보고서에서 사용할 표 형식을 정의한다. |
| [`ad_private_access`](ad_private_access.md) | 개인 레코드 접근 | Private Access | 0 | 사용자와 특정 테이블 레코드 사이의 개인 접근 연결을 관리한다. |
| [`ad_process`](ad_process.md) | 프로세스·보고서 | Process | 472 | 실행할 프로세스 또는 보고서를 정의한다. |
| [`ad_process_access`](ad_process_access.md) | 프로세스 접근 권한 | Process Access | 1,297 | 역할별 프로세스 접근 및 읽기·쓰기 권한을 설정한다. |
| [`ad_process_drillrule`](ad_process_drillrule.md) | 보고서 상세 탐색 규칙 | Drill Rule | 0 | 프로세스·테이블·보고서 뷰·출력 형식을 연결하여 상세 탐색 규칙을 정의한다. |
| [`ad_process_drillrule_para`](ad_process_drillrule_para.md) | 상세 탐색 인수 기본값 | Drill Rule Parameter | 0 | 상세 탐색 규칙에 적용할 프로세스 인수와 범위 기본값을 지정한다. |
| [`ad_process_drillrule_trl`](ad_process_drillrule_trl.md) | 보고서 상세 탐색 규칙 번역 | Drill Rule Trl | 0 | 보고서 상세 탐색 규칙 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_process_para`](ad_process_para.md) | 프로세스 입력 매개변수 | Process Parameter | 1,223 | 프로세스 입력 항목의 유형·범위·기본값·검증 및 표시 조건을 정의한다. |
| [`ad_process_para_trl`](ad_process_para_trl.md) | 프로세스 입력 매개변수 번역 | Process Parameter Trl | 1,223 | 프로세스 입력 매개변수 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_process_trl`](ad_process_trl.md) | 프로세스·보고서 번역 | Process Trl | 472 | 프로세스·보고서 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_recentitem`](ad_recentitem.md) | 최근 사용 항목 | Recent Item | 0 | 사용자가 최근 사용한 창·탭·레코드를 역할과 함께 기록한다. |
| [`ad_record_access`](ad_record_access.md) | 역할별 레코드 권한 | AD_Record_Access | 0 | 역할별 특정 레코드의 읽기 전용·제외 여부와 종속 데이터 적용 여부를 설정한다. |
| [`ad_ref_list`](ad_ref_list.md) | 선택 목록 값 | Reference List | 1,529 | 참조 선택 목록을 구성하는 값을 관리한다. |
| [`ad_ref_list_trl`](ad_ref_list_trl.md) | 선택 목록 값 번역 | Reference List Trl | 1,529 | 선택 목록 값 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_ref_table`](ad_ref_table.md) | 테이블 기반 참조 | AD_Ref_Table | 234 | 테이블을 이용한 참조 정의를 관리한다. |
| [`ad_reference`](ad_reference.md) | 참조 유형 | Reference | 591 | 시스템의 선택 목록과 참조 유형을 정의한다. |
| [`ad_reference_trl`](ad_reference_trl.md) | 참조 유형 번역 | Reference Trl | 591 | 참조 유형 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_registration`](ad_registration.md) | 시스템 등록 | System Registration | 0 | 시스템 등록 정보를 관리한다. 원본 도움말은 하나의 레코드만 유지하고 추가하지 않도록 명시한다. |
| [`ad_relationtype`](ad_relationtype.md) | 레코드 관계 유형 | Relation Type | 6 | 레코드 쌍이 관계에 포함되기 위해 충족해야 하는 조건과 관계 집합을 정의한다. |
| [`ad_replication`](ad_replication.md) | 데이터 복제 대상 | Replication | 1 | 데이터를 복제할 대상을 정의한다. |
| [`ad_replication_log`](ad_replication_log.md) | 데이터 복제 상세 로그 | Replication Log | 0 | 데이터 복제 처리의 상세 로그를 기록한다. |
| [`ad_replication_run`](ad_replication_run.md) | 데이터 복제 실행 | Replication Run | 0 | 데이터 복제 실행 건을 관리한다. |
| [`ad_replicationdocument`](ad_replicationdocument.md) | 문서별 복제 설정 | Replication Document | 1 | 복제 전략에 문서 유형·대상 테이블·복제 유형을 연결한다. |
| [`ad_replicationstrategy`](ad_replicationstrategy.md) | 데이터 복제 전략 | Replication Strategy | 2 | 데이터 복제 전략을 정의한다. |
| [`ad_replicationtable`](ad_replicationtable.md) | 복제 전략 대상 테이블 | Replication Table | 473 | 복제 전략에 포함되는 테이블 정보를 관리한다. |
| [`ad_reportview`](ad_reportview.md) | 보고서 조회 정의 | Report View | 102 | 보고서를 생성할 때 사용할 조회 뷰 정의를 관리한다. |
| [`ad_reportview_col`](ad_reportview_col.md) | 보고서 열 함수 | Report view Column | 0 | 보고서 조회의 열에 적용할 함수와 집계 함수 여부를 정의한다. |
| [`ad_reportview_column`](ad_reportview_column.md) | 보고서 선택 열 | Report View Selected column | 0 | 보고서 조회에 포함할 열을 연결한다. |
| [`ad_requiredplugin`](ad_requiredplugin.md) | 필수 플러그인 | Required Plugin | 0 | 누락 시 시스템 오류나 데이터 손상을 일으킬 수 있는 필수 플러그인을 등록한다. |
| [`ad_role`](ad_role.md) | 역할 | Role | 5 | 사용자의 책임과 접근 권한을 구분하는 역할을 정의한다. |
| [`ad_role_included`](ad_role_included.md) | 포함 역할 | Included Role | 0 | 역할에 포함되는 다른 역할과 적용 순서를 지정한다. |
| [`ad_role_orgaccess`](ad_role_orgaccess.md) | 역할별 조직 접근 | AD_Role_OrgAccess | 18 | 역할별 조직 접근과 읽기 전용 여부를 설정한다. |
| [`ad_rule`](ad_rule.md) | 실행 규칙 스크립트 | Rule | 4 | 이벤트·규칙 유형에 따른 스크립트와 접근 수준을 정의한다. |
| [`ad_schedule`](ad_schedule.md) | 실행 일정 | Schedule | 5 | 스케줄러가 사용할 실행 시점을 정의한다. |
| [`ad_scheduler`](ad_scheduler.md) | 프로세스 스케줄러 | Scheduler | 12 | 프로세스를 일정에 따라 실행하도록 설정한다. |
| [`ad_scheduler_para`](ad_scheduler_para.md) | 예약 실행 인수 | AD_Scheduler_Para | 14 | 예약 실행할 프로세스의 인수와 범위 기본값을 설정한다. |
| [`ad_schedulerlog`](ad_schedulerlog.md) | 스케줄러 실행 로그 | Scheduler Log | 0 | 스케줄러 실행 결과를 기록한다. |
| [`ad_schedulerrecipient`](ad_schedulerrecipient.md) | 스케줄러 통지 수신자 | Scheduler Recipient | 1 | 스케줄러 통지를 받을 대상을 지정한다. |
| [`ad_searchdefinition`](ad_searchdefinition.md) | 검색 정의 | Search Definition | 2 | 테이블·열에 대한 검색 쿼리·유형과 연결 창을 정의한다. |
| [`ad_sequence`](ad_sequence.md) | 문서 번호 채번 | Sequence | 1,445 | 문서 번호를 생성하는 채번 규칙을 관리한다. |
| [`ad_sequence_audit`](ad_sequence_audit.md) | 문서 채번 이력 | AD_Sequence_Audit | 0 | 채번 규칙으로 생성한 문서 번호와 대상 테이블 레코드를 기록한다. |
| [`ad_sequence_no`](ad_sequence_no.md) | 구분 키별 다음 번호 | AD_Sequence_No | 0 | 채번 규칙의 구분 키마다 다음에 사용할 번호를 관리한다. |
| [`ad_session`](ad_session.md) | 사용자 세션 | Session | 0 | 온라인 또는 웹 사용자 세션을 관리한다. |
| [`ad_smtp`](ad_smtp.md) | 메일 발송 서버 | SMTP Server | 0 | SMTP 호스트·포트·보안 및 인증 옵션과 적용 메일 범위를 설정한다. |
| [`ad_statusline`](ad_statusline.md) | 상태 표시줄 정의 | Status Line | 7 | 상태 표시줄에 사용할 메시지·SQL과 표시 스타일을 정의한다. |
| [`ad_statuslineusedin`](ad_statuslineusedin.md) | 상태 표시줄 적용 위치 | AD_StatusLineUsedIn | 14 | 상태 표시줄을 적용할 창·탭·테이블·조회 창과 순서를 지정한다. |
| [`ad_storageprovider`](ad_storageprovider.md) | 파일 저장소 제공자 | Storage Provider | 0 | 파일 저장 방식·경로·주소와 기본 저장소 여부를 정의한다. |
| [`ad_style`](ad_style.md) | 화면 스타일 | Style | 1 | 필드와 라벨에 적용할 CSS 스타일을 정의한다. |
| [`ad_styleline`](ad_styleline.md) | 스타일 상세 항목 | Style Line | 1 | 화면 스타일을 구성하는 상세 항목을 관리한다. |
| [`ad_sysconfig`](ad_sysconfig.md) | 시스템 설정값 | System Configurator | 213 | 설정 이름과 값, 엔터티 유형 및 설정 적용 수준을 관리한다. |
| [`ad_system`](ad_system.md) | 시스템 정의 | System | 1 | 설치된 시스템의 기본 정의를 관리한다. |
| [`ad_tab`](ad_tab.md) | 화면 탭 | Tab | 1,153 | 창 내부의 탭을 정의한다. |
| [`ad_tab_customization`](ad_tab_customization.md) | 탭 그리드 개인화 | Tab Customization | 0 | 사용자의 탭 그리드 표시 설정을 관리한다. |
| [`ad_tab_trl`](ad_tab_trl.md) | 화면 탭 번역 | Tab Trl | 1,153 | 화면 탭 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_table`](ad_table.md) | 애플리케이션 사전 테이블 | Table | 1,063 | 애플리케이션에서 사용하는 테이블의 사전 정의를 관리한다. |
| [`ad_table_access`](ad_table_access.md) | 테이블 접근 권한 | AD_Table_Access | 1 | 역할별 테이블 접근·읽기 전용·보고서·내보내기 허용 여부를 설정한다. |
| [`ad_table_scriptvalidator`](ad_table_scriptvalidator.md) | 테이블 스크립트 검증기 | Table Script Validator | 0 | 테이블에 적용하는 스크립트 기반 모델 검증기를 정의한다. |
| [`ad_table_trl`](ad_table_trl.md) | 애플리케이션 사전 테이블 번역 | Table Trl | 1,063 | 애플리케이션 사전 테이블 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_tableattribute`](ad_tableattribute.md) | 레코드 확장 속성 | AD_TableAttribute_ID | 0 | 테이블의 특정 레코드에 대한 속성과 문자·숫자·날짜 값을 관리한다. |
| [`ad_tableattributeset`](ad_tableattributeset.md) | 테이블 속성 집합 연결 | Table Attribute Set | 0 | 테이블과 속성 집합을 연결하여 하나의 테이블에 여러 속성 집합을 적용할 수 있게 한다. |
| [`ad_tableindex`](ad_tableindex.md) | 테이블 인덱스 | Table Index | 1,192 | 테이블의 인덱스 정의를 관리한다. |
| [`ad_tablepartition`](ad_tablepartition.md) | 테이블 파티션 정의 | Table Partition | 0 | 테이블 파티션의 표현식·열·상위 파티션과 연결 상태를 관리한다. |
| [`ad_tablevalrule`](ad_tablevalrule.md) | 테이블별 동적 검증 | Dynamic Validation per Table | 0 | 테이블에 적용할 동적 검증 코드를 역할·사용자 조건과 함께 정의한다. |
| [`ad_task`](ad_task.md) | 운영체제 작업 | OS Task | 3 | 운영체제에서 실행할 작업을 정의한다. |
| [`ad_task_access`](ad_task_access.md) | 운영체제 작업 권한 | AD_Task_Access | 3 | 역할별 운영체제 작업 접근 및 읽기·쓰기 권한을 설정한다. |
| [`ad_task_trl`](ad_task_trl.md) | 운영체제 작업 번역 | OS Task Trl | 3 | 운영체제 작업 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_taskinstance`](ad_taskinstance.md) | 운영체제 작업 실행 | Task Instance | 0 | 운영체제 작업의 개별 실행 인스턴스를 관리한다. |
| [`ad_toolbarbutton`](ad_toolbarbutton.md) | 도구 모음 버튼 | ToolBar Button | 87 | 버튼 동작·구현 클래스·단축키·표시 조건과 연결 프로세스를 정의한다. |
| [`ad_toolbarbuttonrestrict`](ad_toolbarbuttonrestrict.md) | 도구 모음 버튼 제한 | ToolBar Button Restrict | 0 | 역할과 창·탭·프로세스별 도구 모음 버튼의 제외 조건을 관리한다. |
| [`ad_tree`](ad_tree.md) | 계층 트리 | Tree | 23 | 계층 구조를 표현하는 트리를 정의한다. |
| [`ad_tree_favorite`](ad_tree_favorite.md) | 즐겨찾기 메뉴 트리 | Favorite Tree | 4 | 대시보드에 표시할 사용자 즐겨찾기 메뉴를 관리한다. |
| [`ad_tree_favorite_node`](ad_tree_favorite_node.md) | 즐겨찾기 메뉴 노드 | Favorite Node Tree | 24 | 즐겨찾기 트리의 메뉴 항목·상위 노드·순서와 로그인 시 열기 순서를 관리한다. |
| [`ad_treebar`](ad_treebar.md) | 사용자 선택 트리 노드 | AD_TreeBar | 24 | 사용자가 선택한 트리 노드를 관리한다. |
| [`ad_treenode`](ad_treenode.md) | 일반 트리 노드 | Tree Node | 406 | 트리의 노드·상위 노드와 표시 순서를 저장한다. |
| [`ad_treenodebp`](ad_treenodebp.md) | 거래처 트리 노드 | Tree Node BP | 18 | 거래처 트리의 노드·상위 노드와 표시 순서를 저장한다. |
| [`ad_treenodecmc`](ad_treenodecmc.md) | 콘텐츠 컨테이너 트리 노드 | Tree Node CM Container | 5 | 콘텐츠 컨테이너 트리의 계층과 표시 순서를 저장한다. |
| [`ad_treenodecmm`](ad_treenodecmm.md) | 콘텐츠 미디어 트리 노드 | Tree Node CM Media | 3 | 콘텐츠 미디어 트리의 계층과 표시 순서를 저장한다. |
| [`ad_treenodecms`](ad_treenodecms.md) | 콘텐츠 스테이지 트리 노드 | Tree Node CM Stage | 5 | 콘텐츠 스테이지 트리의 계층과 표시 순서를 저장한다. |
| [`ad_treenodecmt`](ad_treenodecmt.md) | 콘텐츠 템플릿 트리 노드 | Tree Node CM Template | 4 | 콘텐츠 템플릿 트리의 계층과 표시 순서를 저장한다. |
| [`ad_treenodemm`](ad_treenodemm.md) | MM 트리 노드 | Tree Node MM | 815 | MM 유형 트리의 노드·상위 노드와 표시 순서를 저장한다. MM 약어의 정확한 업무 대상은 원본 사전과 열 정보만으로 확정할 수 없다. |
| [`ad_treenodepr`](ad_treenodepr.md) | PR 트리 노드 | Tree Node PR | 55 | PR 유형 트리의 노드·상위 노드와 표시 순서를 저장한다. PR 약어의 정확한 업무 대상은 원본 사전과 열 정보만으로 확정할 수 없다. |
| [`ad_treenodeu1`](ad_treenodeu1.md) | 사용자 정의 트리 1 노드 | Tree Node User 1 | 0 | 사용자 정의 트리 1의 계층 노드를 관리한다. |
| [`ad_treenodeu2`](ad_treenodeu2.md) | 사용자 정의 트리 2 노드 | Tree Node User 2 | 0 | 사용자 정의 트리 2의 계층 노드를 관리한다. |
| [`ad_treenodeu3`](ad_treenodeu3.md) | 사용자 정의 트리 3 노드 | Tree Node User 3 | 0 | 사용자 정의 트리 3의 계층 노드를 관리한다. |
| [`ad_treenodeu4`](ad_treenodeu4.md) | 사용자 정의 트리 4 노드 | Tree Node User 4 | 0 | 사용자 정의 트리 4의 계층 노드를 관리한다. |
| [`ad_user`](ad_user.md) | 사용자·거래처 담당자 | User/Contact | 9 | 내부 시스템 사용자와 거래처 연락 담당자를 관리한다. |
| [`ad_user_orgaccess`](ad_user_orgaccess.md) | 사용자별 조직 접근 | AD_User_OrgAccess | 0 | 사용자별 조직 접근과 읽기 전용 여부를 설정한다. |
| [`ad_user_roles`](ad_user_roles.md) | 사용자 역할 부여 | AD_User_Roles | 11 | 사용자에게 부여한 역할을 연결한다. |
| [`ad_user_substitute`](ad_user_substitute.md) | 사용자 대리인 | User Substitute | 0 | 사용자를 대신하는 대리인을 지정한다. |
| [`ad_userbpaccess`](ad_userbpaccess.md) | 사용자의 거래처 접근 | User BP Access | 0 | 사용자 또는 연락 담당자의 거래처 정보·자원 접근을 관리한다. |
| [`ad_userdef_field`](ad_userdef_field.md) | 사용자 정의 필드 설정 | User defined Field | 0 | 기존 필드의 이름·표시·입력·검증·배치를 사용자 정의 탭 안에서 재설정한다. |
| [`ad_userdef_info`](ad_userdef_info.md) | 사용자 정의 조회 창 | User defined Info Window | 0 | 역할·사용자별 조회 창의 이름·도움말·대시보드 표시 등을 재설정한다. |
| [`ad_userdef_info_column`](ad_userdef_info_column.md) | 사용자 정의 조회 열 | User defined Info Column | 0 | 사용자 정의 조회 창에서 열 표시·검색 조건·기본값·입력 검증을 재설정한다. |
| [`ad_userdef_info_related`](ad_userdef_info_related.md) | 사용자 정의 연관 조회 | User defined Info Related | 0 | 사용자 정의 조회 창의 연관 조회 이름·표시 조건과 순서를 재설정한다. |
| [`ad_userdef_proc`](ad_userdef_proc.md) | 사용자 정의 프로세스 | User defined Process | 0 | 역할·사용자별 프로세스의 이름·설명·도움말·언어 등 표시 설정을 관리한다. |
| [`ad_userdef_proc_parameter`](ad_userdef_proc_parameter.md) | 사용자 정의 프로세스 인수 | AD_UserDef_Proc_Parameter_ID | 0 | 사용자 정의 프로세스에서 입력 매개변수의 표시·기본값·필수 여부·검증 및 순서를 재설정한다. |
| [`ad_userdef_tab`](ad_userdef_tab.md) | 사용자 정의 탭 | User defined Tab | 0 | 사용자 정의 창에서 탭의 읽기 전용·표시·조회 조건과 배치를 재설정한다. |
| [`ad_userdef_theme`](ad_userdef_theme.md) | 사용자 테마 설정 | Theme Customization | 0 | 역할·사용자별 화면 테마와 스타일시트를 관리한다. |
| [`ad_userdef_theme_detail`](ad_userdef_theme_detail.md) | 사용자 테마 변경값 | Theme Customization Detail | 0 | 사용자 테마 설정에 속한 기존 값과 변경 값을 기록한다. |
| [`ad_userdef_win`](ad_userdef_win.md) | 사용자 정의 창 | User defined Window | 0 | 역할·사용자별 창의 이름·언어·읽기 전용 등 설정을 관리한다. |
| [`ad_usermail`](ad_usermail.md) | 사용자 발송 메일 | User Mail | 1 | 사용자에게 보낸 메일을 기록한다. |
| [`ad_userpreference`](ad_userpreference.md) | 사용자 동작 환경설정 | AD_UserPreference_ID | 0 | 자동 저장·새 항목 생성·검색 결과 표시·세션 읽기 전용 등 사용자별 동작 옵션을 관리한다. |
| [`ad_userquery`](ad_userquery.md) | 저장된 사용자 검색 | User Query | 2 | 사용자가 저장한 검색 조건을 관리한다. |
| [`ad_val_rule`](ad_val_rule.md) | 동적 검증 규칙 | Dynamic Validation | 332 | 동적으로 적용하는 검증 규칙을 정의한다. |
| [`ad_verifymigration`](ad_verifymigration.md) | 마이그레이션 검증 보조 | Verify Migration | 0 | 마이그레이션 검증을 지원하는 정보를 관리한다. |
| [`ad_viewcolumn`](ad_viewcolumn.md) | 데이터베이스 뷰 열 정의 | Database View Column | 17,684 | 뷰 구성요소의 열 이름·SQL 표현식·데이터 유형과 순서를 정의한다. |
| [`ad_viewcomponent`](ad_viewcomponent.md) | 데이터베이스 뷰 구성요소 | Database View Component | 229 | 뷰의 FROM·WHERE 등 SQL 구성과 참조 테이블·결합 옵션을 정의한다. |
| [`ad_wf_activity`](ad_wf_activity.md) | 워크플로 활동 | Workflow Activity | 13 | 워크플로 실행에서 수행되는 활동을 관리한다. |
| [`ad_wf_activityapprover`](ad_wf_activityapprover.md) | 워크플로 활동 승인자 | Workflow Activity Approver | 0 | 워크플로 활동의 승인자를 지정한다. |
| [`ad_wf_activityresult`](ad_wf_activityresult.md) | 워크플로 활동 결과 | Workflow Activity Result | 0 | 워크플로 활동의 실행 결과를 기록한다. |
| [`ad_wf_block`](ad_wf_block.md) | 워크플로 실행 블록 | Workflow Block | 0 | 워크플로 트랜잭션 실행 블록을 정의한다. |
| [`ad_wf_eventaudit`](ad_wf_eventaudit.md) | 워크플로 이벤트 감사 | Workflow Event Audit | 13 | 워크플로 프로세스와 활동의 이벤트 감사 정보를 기록한다. |
| [`ad_wf_nextcondition`](ad_wf_nextcondition.md) | 워크플로 전이 조건 | Transition Condition | 1 | 워크플로 노드 사이의 전이 조건을 정의한다. |
| [`ad_wf_node`](ad_wf_node.md) | 워크플로 노드 | Node | 262 | 워크플로의 활동·단계·프로세스를 나타내는 노드를 정의한다. |
| [`ad_wf_node_para`](ad_wf_node_para.md) | 워크플로 노드 실행 인수 | Workflow Node Parameter | 1 | 워크플로 노드 실행에 사용할 매개변수를 정의한다. |
| [`ad_wf_node_trl`](ad_wf_node_trl.md) | 워크플로 노드 번역 | Node Trl | 262 | 워크플로 노드 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_wf_nodenext`](ad_wf_nodenext.md) | 워크플로 노드 전이 | Node Transition | 207 | 워크플로 노드 사이의 다음 단계 연결을 정의한다. |
| [`ad_wf_process`](ad_wf_process.md) | 워크플로 실행 인스턴스 | Workflow Process | 11 | 실제 실행되는 워크플로 프로세스 인스턴스를 관리한다. |
| [`ad_wf_processdata`](ad_wf_processdata.md) | 워크플로 실행 문맥 | Workflow Process Data | 0 | 워크플로 프로세스의 실행 문맥 데이터를 관리한다. |
| [`ad_wf_responsible`](ad_wf_responsible.md) | 워크플로 책임자 | Workflow Responsible | 2 | 워크플로 실행 책임 대상을 정의한다. |
| [`ad_window`](ad_window.md) | 데이터 입력·조회 창 | Window | 452 | 데이터를 입력하거나 표시하는 창을 정의한다. |
| [`ad_window_access`](ad_window_access.md) | 창 접근 권한 | AD_Window_Access | 1,283 | 역할별 창 접근 및 읽기·쓰기 권한을 설정한다. |
| [`ad_window_trl`](ad_window_trl.md) | 데이터 입력·조회 창 번역 | Window Trl | 452 | 데이터 입력·조회 창 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_wizardprocess`](ad_wizardprocess.md) | 마법사 진행 상태 | Wizard Process | 0 | 사용자와 워크플로 노드에 연결된 마법사 상태·메모를 기록한다. |
| [`ad_wlistbox_customization`](ad_wlistbox_customization.md) | 목록 위젯 개인화 | Customization of the Wlistbox | 0 | 사용자별 목록 위젯의 이름과 사용자 설정을 저장한다. |
| [`ad_workbench`](ad_workbench.md) | 작업 공간 | Workbench | 1 | 창과 보고서를 묶어 작업 공간을 정의한다. |
| [`ad_workbench_trl`](ad_workbench_trl.md) | 작업 공간 번역 | Workbench Trl | 1 | 작업 공간 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_workbenchwindow`](ad_workbenchwindow.md) | 작업 공간 구성 항목 | Workbench Window | 2 | 작업 공간에 속한 창·폼·프로세스·작업과 표시 순서를 지정한다. |
| [`ad_workflow`](ad_workflow.md) | 워크플로 정의 | Workflow | 58 | 업무 흐름과 작업 조합을 정의한다. |
| [`ad_workflow_access`](ad_workflow_access.md) | 워크플로 접근 권한 | AD_Workflow_Access | 177 | 역할별 워크플로 접근 및 읽기·쓰기 권한을 설정한다. |
| [`ad_workflow_trl`](ad_workflow_trl.md) | 워크플로 정의 번역 | Workflow Trl | 58 | 워크플로 정의 항목의 언어별 표시 문구를 관리한다. 원본 항목과 언어를 기준으로 번역을 연결한다. |
| [`ad_workflowprocessor`](ad_workflowprocessor.md) | 워크플로 처리 서버 | Workflow Processor | 1 | 워크플로 처리 서버의 설정을 관리한다. |
| [`ad_workflowprocessorlog`](ad_workflowprocessorlog.md) | 워크플로 처리 로그 | Workflow Processor Log | 0 | 워크플로 처리기의 실행 결과를 기록한다. |
| [`ad_zoomcondition`](ad_zoomcondition.md) | 레코드 이동 조건 | Zoom condition | 13 | 테이블에서 특정 창으로 이동할 조건과 적용 순서를 정의한다. |
