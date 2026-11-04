# iDempiere 13 전체 테이블 목록

실제 설치한 `poc_idempiere.adempiere`의 물리 테이블 912개다. 뷰 161개는 이 목록에 포함하지 않는다. 행 수는 2026-10-12 설치 시점 전체 테넌트 기준이며, 0은 해당 업무의 샘플 데이터가 없음을 뜻한다. 원본 업무 명칭·설명을 함께 실었다.

[설치·사용 안내](IDEMPIERE_GUIDE.md) · 전체 열/외래키: `.local/datasets/idempiere/catalog.json`

**새 AI 참조 문서:** [전체 테이블 일람·한국어 개요](../docs/database/idempiere/TABLE_INDEX.md) · [업무별 안내](../docs/database/idempiere/BUSINESS_GUIDE.md) · [폴더별 테이블 문서](../docs/database/idempiere/README.md). 개별 문서에는 물리명·원본 논리명·한국어 해석·열·양방향 외래키 흐름을 수록했다. 이 페이지의 기존 행 수는 아래에 명시한 2026-10-12 기록을 유지한다.

| 테이블 | 원본 업무 명칭 | 행 수 | 열 수 | 설명 |
|---|---|---:|---:|---|
| `a_asset` | Asset | 0 | 69 | Asset used internally or by customers |
| `a_asset_acct` | A_Asset_Acct_ID | 0 | 50 |  |
| `a_asset_addition` | Asset Addition | 0 | 54 |  |
| `a_asset_change` | A_Asset_Change_ID | 0 | 79 |  |
| `a_asset_change_amt` | a_asset_change_amt | 0 | 13 |  |
| `a_asset_class` | Asset class | 0 | 20 |  |
| `a_asset_delivery` | Asset Delivery | 0 | 25 | Delivery of Asset |
| `a_asset_disposed` | Asset Disposed | 0 | 41 |  |
| `a_asset_group` | Asset Group | 9 | 21 | Group of Assets |
| `a_asset_group_acct` | Asset Group Accounting | 6 | 53 |  |
| `a_asset_group_trl` | Asset Group Trl | 9 | 14 | Group of Assets |
| `a_asset_info_fin` | Asset Info Financial ID | 0 | 22 |  |
| `a_asset_info_ins` | A_Asset_Info_Ins_ID | 0 | 17 |  |
| `a_asset_info_lic` | A_Asset_Info_Lic_ID | 0 | 17 |  |
| `a_asset_info_oth` | A_Asset_Info_Oth_ID | 0 | 26 |  |
| `a_asset_info_tax` | Asset Info Tax | 0 | 16 |  |
| `a_asset_product` | Asset Product | 0 | 15 |  |
| `a_asset_retirement` | Asset Retirement | 0 | 13 | Internally used asset is not longer used. |
| `a_asset_reval` | Asset Revaluation | 0 | 26 |  |
| `a_asset_reval_entry` | Asset Reval. Entry | 0 | 26 |  |
| `a_asset_reval_index` | Asset Reval Index | 0 | 13 |  |
| `a_asset_split` | Asset Split | 0 | 26 |  |
| `a_asset_spread` | A_Asset_Spread_ID | 2 | 25 |  |
| `a_asset_transfer` | A_Asset_Transfer_ID | 0 | 54 |  |
| `a_asset_type` | Asset Type | 0 | 15 |  |
| `a_asset_use` | A_Asset_Use_ID | 0 | 13 |  |
| `a_depreciation` | Depreciation | 11 | 15 |  |
| `a_depreciation_build` | Build Depreciation | 0 | 18 |  |
| `a_depreciation_convention` | Depreciation Convention | 6 | 15 |  |
| `a_depreciation_entry` | Depreciation Entry | 0 | 29 |  |
| `a_depreciation_exp` | A_Depreciation_Exp_ID | 0 | 38 |  |
| `a_depreciation_forecast` | Depreciation Forecast | 0 | 15 |  |
| `a_depreciation_method` | Depreciation Method | 3 | 14 |  |
| `a_depreciation_table_detail` | Depreciation Table Detail | 2,579 | 14 |  |
| `a_depreciation_table_header` | A_Depreciation_Table_Header_ID | 122 | 14 |  |
| `a_depreciation_workfile` | A_Depreciation_Workfile_ID | 0 | 45 |  |
| `a_fundingmode` | Asset Funding Mode | 0 | 12 |  |
| `a_fundingmode_acct` | Asset Funding Mode Accounting | 0 | 11 |  |
| `a_registration` | Registration | 0 | 24 | User Asset Registration |
| `a_registrationattribute` | Registration Attribute | 0 | 16 | Asset Registration Attribute |
| `a_registrationproduct` | Registration Product | 0 | 11 |  |
| `a_registrationvalue` | A_RegistrationValue | 0 | 12 |  |
| `ad_accesslog` | Access Log | 0 | 17 | Log of Access to the System |
| `ad_alert` | Alert | 1 | 18 | iDempiere Alert |
| `ad_alertprocessor` | Alert Processor | 1 | 19 | Alert Processor/Server Parameter |
| `ad_alertprocessorlog` | Alert Processor Log | 0 | 16 | Result of the execution of the Alert Processor |
| `ad_alertrecipient` | Alert Recipient | 1 | 12 | Recipient of the Alert Notification |
| `ad_alertrule` | Alert Rule | 1 | 20 | Definition of the alert element |
| `ad_archive` | Archive | 0 | 20 | Document Archive |
| `ad_archive_blob` | ad_archive_blob | 0 | 2 |  |
| `ad_attachment` | Attachment | 1 | 16 | Attachment for the document |
| `ad_attachment_entry` | ad_attachment_entry | 0 | 3 |  |
| `ad_attachmentfile` | Attachment File | 0 | 15 |  |
| `ad_attachmentnote` | Attachment Note | 0 | 13 | Personal Attachment Note |
| `ad_attribute` | System Attribute | 0 | 32 |  |
| `ad_attribute_value` | AD_Attribute_Value | 0 | 6 |  |
| `ad_authorizationaccount` | Authorization Account | 0 | 22 |  |
| `ad_authorizationcredential` | Authorization Credential | 0 | 16 |  |
| `ad_authorizationprovider` | Authorization Provider | 2 | 16 |  |
| `ad_authorizationscopeprov` | Authorization Scope Provider | 3 | 12 |  |
| `ad_broadcastmessage` | Broadcast Message | 0 | 25 | Broadcast Messages for system users |
| `ad_broadcastmessage_trl` | Broadcast Message Trl | 0 | 13 | Broadcast Message |
| `ad_changelog` | Change Log | 0 | 22 | Log of data changes |
| `ad_chart` | Chart | 4 | 21 | Chart definition |
| `ad_chart_trl` | Chart Trl | 4 | 15 |  |
| `ad_chartdatasource` | Chart Datasource | 6 | 22 | Chart data definition |
| `ad_chartdatasource_trl` | Chart Datasource Trl | 6 | 12 |  |
| `ad_client` | Tenant | 2 | 42 | Tenant for this installation. |
| `ad_clientinfo` | AD_ClientInfo | 2 | 37 |  |
| `ad_clientshare` | Tenant Share | 0 | 13 | Force (not) sharing of tenant/org entities |
| `ad_color` | System Color | 0 | 26 | Color for backgrounds or indicators |
| `ad_color_trl` | System Color Trl | 0 | 12 | Color for backgrounds or indicators |
| `ad_column` | Column | 26,476 | 63 | Column in the table |
| `ad_column_access` | AD_Column_Access | 0 | 13 |  |
| `ad_column_trl` | Column Trl | 26,476 | 13 | Column in the table |
| `ad_ctxhelp` | Context Help | 1 | 19 |  |
| `ad_ctxhelpmsg` | Context Help Message | 1 | 12 |  |
| `ad_ctxhelpmsg_trl` | Context Help Message Trl | 1 | 12 |  |
| `ad_ctxhelpsuggestion` | Context Help Suggestion | 0 | 21 | Suggestion for context help content |
| `ad_desktop` | Desktop | 1 | 14 | Collection of Workbenches |
| `ad_desktop_trl` | Desktop Trl | 1 | 14 | Collection of Workbenches |
| `ad_desktopworkbench` | Desktop Workbench | 1 | 12 |  |
| `ad_document_action_access` | Document Action Access | 2,156 | 11 | Define access to document type / document action / role combinations. |
| `ad_element` | System Element | 5,985 | 20 | System Element enables the central maintenance of column description and help. |
| `ad_element_trl` | System Element Trl | 5,985 | 20 | System Element enables the central maintenance of column description and help. |
| `ad_entitytype` | Entity Type | 12 | 17 | System Entity Type |
| `ad_error` | Error | 0 | 12 |  |
| `ad_field` | Field | 21,281 | 60 | Field on a database table |
| `ad_field_trl` | Field Trl | 21,281 | 15 | Field on a database table |
| `ad_fieldgroup` | Field Group | 79 | 13 | Logical grouping of fields |
| `ad_fieldgroup_trl` | Field Group Trl | 79 | 12 | Logical grouping of fields |
| `ad_fieldsuggestion` | Field Suggestions | 0 | 23 | Suggestions for field label, description and help |
| `ad_find` | Find | 0 | 15 |  |
| `ad_form` | Special Form | 51 | 19 | Special Form |
| `ad_form_access` | AD_Form_Access | 137 | 11 |  |
| `ad_form_trl` | Special Form Trl | 51 | 14 | Special Form |
| `ad_housekeeping` | House Keeping Configuration | 10 | 22 |  |
| `ad_image` | Image | 10 | 15 | System Image or Icon |
| `ad_image_blob` | ad_image_blob | 0 | 2 |  |
| `ad_impformat` | Import Format | 15 | 15 |  |
| `ad_impformat_row` | Format Field | 163 | 23 |  |
| `ad_importtemplate` | Import Template | 0 | 19 |  |
| `ad_importtemplateaccess` | Import Template Access | 0 | 14 |  |
| `ad_indexcolumn` | Table Index Column | 1,537 | 14 | Index definition for column |
| `ad_infocolumn` | Info Column | 198 | 41 |  |
| `ad_infocolumn_trl` | Info Column Trl | 198 | 16 | Info Window Column |
| `ad_infoprocess` | Info Process | 11 | 17 | define process for info window |
| `ad_inforelated` | Info Related | 0 | 19 |  |
| `ad_infowindow` | Info Window | 17 | 32 |  |
| `ad_infowindow_access` | Info Window Access | 54 | 10 |  |
| `ad_infowindow_trl` | Info Window Trl | 17 | 14 | Info and search/select Window |
| `ad_issue` | System Issue | 0 | 50 |  |
| `ad_label` | Label | 0 | 13 | Record Label |
| `ad_label_trl` | Label Trl | 0 | 13 | Record Label |
| `ad_labelassignment` | Label Assignment | 0 | 14 |  |
| `ad_labelcategory` | Label Category | 0 | 13 | Category of a Label |
| `ad_labelcategory_trl` | Label Category Trl | 0 | 13 | Category of a Label |
| `ad_labelcategorytable` | Label Category Table Access | 0 | 12 |  |
| `ad_labelprinter` | Label printer | 0 | 11 | Label Printer Definition |
| `ad_labelprinterfunction` | Label printer Function | 0 | 16 | Function of Label Printer |
| `ad_language` | Language ID | 109 | 22 |  |
| `ad_ldapaccess` | Ldap Access | 0 | 15 | Ldap Access Log |
| `ad_ldapprocessor` | Ldap Processor | 1 | 17 | LDAP Server |
| `ad_ldapprocessorlog` | Ldap Processor Log | 0 | 16 | LDAP Server Log |
| `ad_menu` | Menu | 813 | 25 | Identifies a Menu |
| `ad_menu_trl` | Menu Trl | 813 | 13 | Identifies a Menu |
| `ad_message` | Message | 2,105 | 14 | System Message |
| `ad_message_trl` | Message Trl | 2,105 | 13 | System Message |
| `ad_migrationscript` | Migration Script | 1,341 | 21 | Migration Scripts for the System |
| `ad_modelgeneratortemplate` | Model Generator Template | 0 | 15 |  |
| `ad_modelvalidator` | Model Validator | 3 | 15 | Global Model Validator |
| `ad_modification` | Modification | 0 | 15 |  |
| `ad_note` | Notice | 0 | 20 | System Notice |
| `ad_org` | Organization | 10 | 13 | Organizational entity within client |
| `ad_orginfo` | Organization Info | 10 | 27 |  |
| `ad_orgtype` | Organization Type | 3 | 12 | Organization Type allows you to categorize your organizations |
| `ad_package_exp` | Package Exp. | 0 | 24 |  |
| `ad_package_exp_common` | Common Package Exp. | 0 | 32 |  |
| `ad_package_exp_detail` | Package Exp. Detail | 0 | 44 |  |
| `ad_package_imp` | Package Imp. | 0 | 24 |  |
| `ad_package_imp_backup` | Imp. Package Backup | 0 | 18 |  |
| `ad_package_imp_detail` | Imp. Package Detail | 0 | 22 |  |
| `ad_package_imp_inst` | Package Imp. Inst. | 0 | 23 |  |
| `ad_package_imp_proc` | Package Imp. Proc. | 0 | 17 |  |
| `ad_package_uuid_map` | UUID Mapping | 0 | 12 | UUID Mapping between client |
| `ad_password_history` | Password History ID | 0 | 13 |  |
| `ad_passwordrule` | Password Policies | 0 | 27 |  |
| `ad_pinstance` | Process Instance | 0 | 26 | Instance of the process |
| `ad_pinstance_log` | AD_PInstance_Log | 0 | 11 | (Non Standard Table) |
| `ad_pinstance_para` | AD_PInstance_Para | 0 | 20 |  |
| `ad_postit` | Post-it | 0 | 13 |  |
| `ad_preference` | Preference | 17 | 17 | Personal Preference |
| `ad_printcolor` | Print Color | 23 | 12 | Color used for printing and display |
| `ad_printcolor_trl` | Print Color | 23 | 12 | Color used for printing and display |
| `ad_printfont` | Print Font | 66 | 12 | Maintain Print Font |
| `ad_printform` | Print Form | 2 | 25 | Form |
| `ad_printformat` | Print Format | 93 | 32 | Data Print Format |
| `ad_printformat_trl` | Print Format Trl | 93 | 14 | Data Print Format |
| `ad_printformatitem` | Print Format Item | 2,780 | 69 | Item/Column in the Print format |
| `ad_printformatitem_trl` | Print Format Item Trl | 2,780 | 14 | Item/Column in the Print format |
| `ad_printgraph` | Graph | 0 | 19 | Graph included in Reports |
| `ad_printheaderfooter` | Print Header/Footer | 0 | 11 |  |
| `ad_printlabel` | Print Label | 0 | 17 | Label Format to print |
| `ad_printlabelline` | Print Label Line | 0 | 18 | Print Label Line Format |
| `ad_printlabelline_trl` | Print Label Line Trl | 0 | 12 | Print Label Line Format |
| `ad_printpaper` | Print Paper | 4 | 22 | Printer paper definition |
| `ad_printtableformat` | Print Table Format | 2 | 39 | Table Format in Reports |
| `ad_private_access` | Private Access | 0 | 11 |  |
| `ad_process` | Process | 472 | 35 | Process or Report |
| `ad_process_access` | Process Access | 1,297 | 11 |  |
| `ad_process_drillrule` | Drill Rule | 0 | 18 |  |
| `ad_process_drillrule_para` | Drill Rule Parameter | 0 | 13 |  |
| `ad_process_drillrule_trl` | Drill Rule Trl | 0 | 13 |  |
| `ad_process_para` | Process Parameter | 1,223 | 40 |  |
| `ad_process_para_trl` | Process Parameter Trl | 1,223 | 16 |  |
| `ad_process_trl` | Process Trl | 472 | 14 | Process or Report |
| `ad_recentitem` | Recent Item | 0 | 16 |  |
| `ad_record_access` | AD_Record_Access | 0 | 14 |  |
| `ad_ref_list` | Reference List | 1,529 | 16 | Reference List based on Table |
| `ad_ref_list_trl` | Reference List Trl | 1,529 | 13 | Reference List based on Table |
| `ad_ref_table` | AD_Ref_Table | 234 | 20 | Reference Table Definitions |
| `ad_reference` | Reference | 591 | 18 | System Reference (Pick List) |
| `ad_reference_trl` | Reference Trl | 591 | 14 | System Reference and Validation |
| `ad_registration` | System Registration | 0 | 26 | System Registration |
| `ad_relationtype` | Relation Type | 6 | 18 | Defines the sets of record pairs (and the conditions a given pair must fulfill to be part of one) |
| `ad_replication` | Replication | 1 | 24 | Data Replication Target |
| `ad_replication_log` | Replication Log | 0 | 13 | Data Replication Log Details |
| `ad_replication_run` | Replication Run | 0 | 13 | Data Replication Run |
| `ad_replicationdocument` | Replication Document | 1 | 14 |  |
| `ad_replicationstrategy` | Replication Strategy | 2 | 15 | Data Replication Strategy |
| `ad_replicationtable` | Replication Table | 473 | 14 | Data Replication Strategy Table Info |
| `ad_reportview` | Report View | 102 | 15 | View used to generate this report |
| `ad_reportview_col` | Report view Column | 0 | 13 |  |
| `ad_reportview_column` | Report View Selected column | 0 | 10 |  |
| `ad_requiredplugin` | Required Plugin | 0 | 11 | Register of plugins that are required when running the System |
| `ad_role` | Role | 5 | 56 | Responsibility Role |
| `ad_role_included` | Included Role | 0 | 11 |  |
| `ad_role_orgaccess` | AD_Role_OrgAccess | 18 | 10 |  |
| `ad_rule` | Rule | 4 | 18 |  |
| `ad_schedule` | Schedule | 5 | 20 | Times for the Scheduler |
| `ad_scheduler` | Scheduler | 12 | 30 | Schedule Processes |
| `ad_scheduler_para` | AD_Scheduler_Para | 14 | 13 |  |
| `ad_schedulerlog` | Scheduler Log | 0 | 16 | Result of the execution of the Scheduler |
| `ad_schedulerrecipient` | Scheduler Recipient | 1 | 15 | Recipient of the Scheduler Notification |
| `ad_searchdefinition` | Search Definition | 2 | 23 |  |
| `ad_sequence` | Sequence | 1,445 | 27 | Document Sequence |
| `ad_sequence_audit` | AD_Sequence_Audit | 0 | 12 |  |
| `ad_sequence_no` | AD_Sequence_No | 0 | 11 |  |
| `ad_session` | Session | 0 | 17 | User Session Online or Web |
| `ad_smtp` | SMTP Server | 0 | 18 |  |
| `ad_statusline` | Status Line | 7 | 14 |  |
| `ad_statuslineusedin` | AD_StatusLineUsedIn | 14 | 17 |  |
| `ad_storageprovider` | Storage Provider | 0 | 16 |  |
| `ad_style` | Style | 1 | 13 | CSS style for field and label |
| `ad_styleline` | Style Line | 1 | 15 | Style Line |
| `ad_sysconfig` | System Configurator | 213 | 14 |  |
| `ad_system` | System | 1 | 43 | System Definition |
| `ad_tab` | Tab | 1,153 | 47 | Tab within a Window |
| `ad_tab_customization` | Tab Customization | 0 | 15 | Grid user customization |
| `ad_tab_trl` | Tab Trl | 1,153 | 15 | Tab within a Window |
| `ad_table` | Table | 1,063 | 35 | Table for the Fields |
| `ad_table_access` | AD_Table_Access | 1 | 15 |  |
| `ad_table_scriptvalidator` | Table Script Validator | 0 | 13 | Script model validator for tables |
| `ad_table_trl` | Table Trl | 1,063 | 12 | Database Table information |
| `ad_tableattribute` | AD_TableAttribute_ID | 0 | 16 |  |
| `ad_tableattributeset` | Table Attribute Set | 0 | 11 | Creates a link between tables and attribute sets for flexible extensions. A table can have multiple attribute sets. |
| `ad_tableindex` | Table Index | 1,192 | 20 | Index definition for table |
| `ad_tablepartition` | Table Partition | 0 | 16 |  |
| `ad_tablevalrule` | Dynamic Validation per Table | 0 | 13 |  |
| `ad_task` | OS Task | 3 | 17 | Operation System Task |
| `ad_task_access` | AD_Task_Access | 3 | 11 |  |
| `ad_task_trl` | OS Task Trl | 3 | 14 | Operation System Task |
| `ad_taskinstance` | Task Instance | 0 | 10 |  |
| `ad_toolbarbutton` | ToolBar Button | 87 | 28 |  |
| `ad_toolbarbuttonrestrict` | ToolBar Button Restrict | 0 | 16 |  |
| `ad_tree` | Tree | 23 | 20 | Identifies a Tree |
| `ad_tree_favorite` | Favorite Tree | 4 | 10 | Show user favorite menu on dashboard |
| `ad_tree_favorite_node` | Favorite Node Tree | 24 | 18 |  |
| `ad_treebar` | AD_TreeBar | 24 | 13 | User Selected tree nodes |
| `ad_treenode` | Tree Node | 406 | 12 |  |
| `ad_treenodebp` | Tree Node BP | 18 | 12 |  |
| `ad_treenodecmc` | Tree Node CM Container | 5 | 12 |  |
| `ad_treenodecmm` | Tree Node CM Media | 3 | 12 |  |
| `ad_treenodecms` | Tree Node CM Stage | 5 | 12 |  |
| `ad_treenodecmt` | Tree Node CM Template | 4 | 12 |  |
| `ad_treenodemm` | Tree Node MM | 815 | 12 |  |
| `ad_treenodepr` | Tree Node PR | 55 | 12 |  |
| `ad_treenodeu1` | Tree Node User 1 | 0 | 12 | User defined tree 1 |
| `ad_treenodeu2` | Tree Node User 2 | 0 | 12 | User defined tree 2 |
| `ad_treenodeu3` | Tree Node User 3 | 0 | 12 | User defined tree 3 |
| `ad_treenodeu4` | Tree Node User 4 | 0 | 12 | User defined tree 4 |
| `ad_user` | User/Contact | 9 | 71 | User within the system - Internal or Business Partner Contact |
| `ad_user_orgaccess` | AD_User_OrgAccess | 0 | 10 |  |
| `ad_user_roles` | AD_User_Roles | 11 | 10 |  |
| `ad_user_substitute` | User Substitute | 0 | 15 | Substitute of the user |
| `ad_userbpaccess` | User BP Access | 0 | 13 | User/concat access to Business Partner information and resources |
| `ad_userdef_field` | User defined Field | 0 | 47 |  |
| `ad_userdef_info` | User defined Info Window | 0 | 21 |  |
| `ad_userdef_info_column` | User defined Info Column | 0 | 32 |  |
| `ad_userdef_info_related` | User defined Info Related | 0 | 16 |  |
| `ad_userdef_proc` | User defined Process | 0 | 17 | Primary Key : User defined Process |
| `ad_userdef_proc_parameter` | AD_UserDef_Proc_Parameter_ID | 0 | 32 | Primary Key : User defined Process Parameter |
| `ad_userdef_tab` | User defined Tab | 0 | 27 |  |
| `ad_userdef_theme` | Theme Customization | 0 | 15 |  |
| `ad_userdef_theme_detail` | Theme Customization Detail | 0 | 12 |  |
| `ad_userdef_win` | User defined Window | 0 | 19 |  |
| `ad_usermail` | User Mail | 1 | 21 | Mail sent to the user |
| `ad_userpreference` | AD_UserPreference_ID | 0 | 21 |  |
| `ad_userquery` | User Query | 2 | 18 | Saved User Query |
| `ad_val_rule` | Dynamic Validation | 332 | 14 | Dynamic Validation Rule |
| `ad_verifymigration` | Verify Migration | 0 | 21 | Verify Migration Helper |
| `ad_viewcolumn` | Database View Column | 17,684 | 17 |  |
| `ad_viewcomponent` | Database View Component | 229 | 21 |  |
| `ad_wf_activity` | Workflow Activity | 13 | 25 | Workflow Activity |
| `ad_wf_activityapprover` | Workflow Activity Approver | 0 | 11 | Approvers of the Workflow Process Activity |
| `ad_wf_activityresult` | Workflow Activity Result | 0 | 14 | Result of the Workflow Process Activity |
| `ad_wf_block` | Workflow Block | 0 | 12 | Workflow Transaction Execution Block |
| `ad_wf_eventaudit` | Workflow Event Audit | 13 | 23 | Workflow Process Activity Event Audit Information |
| `ad_wf_nextcondition` | Transition Condition | 1 | 18 | Workflow Node Transition Condition |
| `ad_wf_node` | Node | 262 | 63 | Workflow Node (activity) step or process |
| `ad_wf_node_para` | Workflow Node Parameter | 1 | 15 | Workflow Node Execution Parameter |
| `ad_wf_node_trl` | Node Trl | 262 | 14 | Workflow Node (activity), step or process |
| `ad_wf_nodenext` | Node Transition | 207 | 16 | Workflow Node Transition |
| `ad_wf_process` | Workflow Process | 11 | 20 | Actual Workflow Process Instance |
| `ad_wf_processdata` | Workflow Process Data | 0 | 12 | Workflow Process Context |
| `ad_wf_responsible` | Workflow Responsible | 2 | 16 | Responsible for Workflow Execution |
| `ad_window` | Window | 452 | 24 | Data entry or display window |
| `ad_window_access` | AD_Window_Access | 1,283 | 11 |  |
| `ad_window_trl` | Window Trl | 452 | 14 | Data entry or display window |
| `ad_wizardprocess` | Wizard Process | 0 | 13 |  |
| `ad_wlistbox_customization` | Customization of the Wlistbox | 0 | 12 |  |
| `ad_workbench` | Workbench | 1 | 16 | Collection of windows, reports |
| `ad_workbench_trl` | Workbench Trl | 1 | 14 | Collection of windows, reports |
| `ad_workbenchwindow` | Workbench Window | 2 | 17 |  |
| `ad_workflow` | Workflow | 58 | 48 | Workflow or combination of tasks |
| `ad_workflow_access` | AD_Workflow_Access | 177 | 11 |  |
| `ad_workflow_trl` | Workflow Trl | 58 | 14 | Workflow or combination of tasks |
| `ad_workflowprocessor` | Workflow Processor | 1 | 22 | Workflow Processor Server |
| `ad_workflowprocessorlog` | Workflow Processor Log | 0 | 16 | Result of the execution of the Workflow Processor |
| `ad_zoomcondition` | Zoom condition | 13 | 17 |  |
| `asp_clientexception` | Tenant Exception | 0 | 19 |  |
| `asp_clientlevel` | Tenant Level | 0 | 12 |  |
| `asp_field` | ASP Field | 0 | 12 |  |
| `asp_form` | ASP Form | 0 | 12 |  |
| `asp_level` | ASP Level | 0 | 15 |  |
| `asp_module` | ASP Module | 0 | 13 |  |
| `asp_process` | ASP Process | 0 | 12 |  |
| `asp_process_para` | ASP Process Parameter | 0 | 12 |  |
| `asp_ref_list` | ASP_Ref_List | 0 | 13 |  |
| `asp_tab` | ASP Tab | 0 | 14 |  |
| `asp_task` | ASP Task | 0 | 12 |  |
| `asp_window` | ASP Window | 0 | 12 |  |
| `asp_workflow` | ASP Workflow | 0 | 12 |  |
| `b_bid` | Bid | 0 | 16 | Bid for a Topic |
| `b_bidcomment` | Bid Comment | 0 | 12 | Make a comment to a Bid Topic |
| `b_buyer` | B_Buyer | 0 | 12 |  |
| `b_buyerfunds` | Buyer Funds | 0 | 14 | Buyer Funds for Bids on Topics |
| `b_offer` | Offer | 0 | 16 | Offer for a Topic |
| `b_seller` | B_Seller | 0 | 13 |  |
| `b_sellerfunds` | Seller Funds | 0 | 14 | Seller Funds from Offers on Topics |
| `b_topic` | Topic | 0 | 22 | Auction Topic |
| `b_topiccategory` | Topic Category | 0 | 12 | Auction Topic Category |
| `b_topictype` | Topic Type | 0 | 16 | Auction Topic Type |
| `c_1099box` | 1099 Box | 0 | 14 |  |
| `c_acctprocessor` | Accounting Processor | 1 | 21 | Accounting Processor/Server Parameters |
| `c_acctprocessorlog` | Accounting Processor Log | 0 | 16 | Result of the execution of the Accounting Processor |
| `c_acctschema` | Accounting Schema | 2 | 38 | Rules for accounting |
| `c_acctschema_default` | C_AcctSchema_Default | 2 | 84 |  |
| `c_acctschema_element` | Acct.Schema Element | 12 | 34 |  |
| `c_acctschema_gl` | C_AcctSchema_GL | 2 | 22 |  |
| `c_activity` | Activity | 0 | 14 | Business Activity |
| `c_activity_trl` | Activity Trl | 0 | 14 | Business Activity |
| `c_addresstransaction` | Address Transaction | 0 | 24 |  |
| `c_addressvalidation` | Address Validation | 0 | 17 |  |
| `c_addressvalidationcfg` | Address Validation Configuration | 0 | 19 |  |
| `c_allocationhdr` | Allocation | 2 | 25 | Payment allocation |
| `c_allocationline` | Allocation Line | 2 | 24 | Allocation Line |
| `c_bank` | Bank | 2 | 15 | Bank |
| `c_bankaccount` | Bank Account | 3 | 22 | Account at the Bank |
| `c_bankaccount_acct` | C_BankAccount_Acct | 6 | 22 |  |
| `c_bankaccount_processor` | Bank Account Processor | 2 | 27 |  |
| `c_bankaccountdoc` | Bank Account Document | 2 | 15 | Checks, Transfers, etc. |
| `c_bankstatement` | Bank Statement | 2 | 33 | Bank Statement of account |
| `c_bankstatementline` | Bank statement line | 2 | 43 | Line on a statement from this Bank |
| `c_bankstatementloader` | Bank Statement Loader | 0 | 28 | Definition of Bank Statement Loader (SWIFT, OFX) |
| `c_bankstatementmatcher` | Bank Statement Matcher | 0 | 13 | Algorithm to match Bank Statement Info to Business Partners, Invoices and Payments |
| `c_banktransfer` | Bank Transfer | 0 | 34 | Bank Transfer |
| `c_bp_bankaccount` | Partner Bank Account | 1 | 36 | Bank Account of the Business Partner |
| `c_bp_customer_acct` | C_BP_Customer_Acct | 36 | 13 |  |
| `c_bp_edi` | EDI Definition | 0 | 28 | Electronic Data Interchange |
| `c_bp_employee_acct` | C_BP_Employee_Acct | 17 | 12 |  |
| `c_bp_group` | Business Partner Group | 3 | 23 | Business Partner Group |
| `c_bp_group_acct` | Business Partner Group Acct | 6 | 24 |  |
| `c_bp_relation` | Partner Relation | 1 | 19 | Business Partner Relation |
| `c_bp_shippingacct` | Business Partner Shipping Account | 0 | 15 |  |
| `c_bp_vendor_acct` | C_BP_Vendor_Acct | 36 | 13 |  |
| `c_bp_withholding` | C_BP_Withholding | 0 | 13 |  |
| `c_bpartner` | Business Partner | 18 | 74 | Identifies a Business Partner |
| `c_bpartner_location` | Partner Location | 16 | 23 | Identifies the (ship to) address for this Business Partner |
| `c_bpartner_product` | Product Business Partner | 1 | 18 |  |
| `c_calendar` | Calendar | 1 | 11 | Accounting Calendar Name |
| `c_campaign` | Campaign | 2 | 17 | Marketing Campaign |
| `c_campaign_trl` | Campaign Trl | 2 | 13 | Marketing Campaign |
| `c_cash` | Cash Journal | 3 | 30 | Cash Journal |
| `c_cashbook` | Cash Book | 2 | 13 | Cash Book for recording petty cash transactions |
| `c_cashbook_acct` | C_CashBook_Acct | 4 | 15 |  |
| `c_cashline` | Cash Journal Line | 5 | 23 | Cash Journal Line |
| `c_cashplan` | Cash Plan | 0 | 26 | Cash Plan |
| `c_cashplanline` | Cash Plan Line | 0 | 29 | Cash Plan Line |
| `c_channel` | Channel | 2 | 12 | Sales Channel |
| `c_charge` | Charge | 3 | 19 | Additional document charges |
| `c_charge_acct` | C_Charge_Acct | 6 | 12 |  |
| `c_charge_trl` | Charge Trl | 3 | 13 | Additional document charges |
| `c_chargetype` | Charge Type | 0 | 13 | Charge Type |
| `c_chargetype_doctype` | Charge Type by Doc Type | 0 | 12 | Configuration table for charges to be used by document type |
| `c_city` | City | 1 | 16 | City |
| `c_commission` | Commission | 1 | 21 | Commission |
| `c_commissionamt` | Commission Amount | 0 | 14 | Generated Commission Amount  |
| `c_commissiondetail` | Commission Detail | 0 | 18 | Supporting information for Commission Amounts |
| `c_commissionline` | Commission Line | 1 | 25 | Commission Line |
| `c_commissionrun` | Commission Run | 0 | 17 | Commission Run or Process |
| `c_contactactivity` | Contact Activity | 0 | 18 | Events, tasks, communications related to a contact |
| `c_conversion_rate` | Conversion Rate | 4 | 16 | Rate used for converting currencies |
| `c_conversiontype` | Currency Type | 4 | 13 | Currency Conversion Rate Type |
| `c_costcenter` | Cost Center | 0 | 11 |  |
| `c_country` | Country | 251 | 45 | Country  |
| `c_country_trl` | Country Trl | 251 | 23 | Country  |
| `c_countrygroup` | Country Group | 0 | 15 | Group of countries that share common needs like tax agreements |
| `c_countrygroup_trl` | Country Group Trl | 0 | 13 |  |
| `c_countrygroupcountry` | Country on Country Group | 0 | 13 |  |
| `c_currency` | Currency | 175 | 19 | The Currency for this record |
| `c_currency_acct` | C_Currency_Acct | 0 | 14 |  |
| `c_currency_trl` | Currency Trl | 175 | 13 | The Currency for this record |
| `c_cycle` | Project Cycle | 2 | 12 | Identifier for this Project Reporting Cycle |
| `c_cyclephase` | C_CyclePhase | 10 | 10 |  |
| `c_cyclestep` | Cycle Step | 4 | 13 | The step for this Cycle |
| `c_department` | Department | 0 | 11 |  |
| `c_depositbatch` | Deposit Batch | 0 | 22 |  |
| `c_depositbatchline` | Deposit Batch Line | 0 | 15 |  |
| `c_docbasegroup` | Document Base Type Group | 0 | 12 | Group of Document Base Type for Period Control |
| `c_docbasegroupline` | Document Base Type Group Line | 0 | 11 | Line Items of a Document Base Type Group |
| `c_doctype` | Document Type | 52 | 46 | Document type or rules |
| `c_doctype_trl` | Document Type Trl | 52 | 14 | Document type or rules |
| `c_doctypecounter` | Counter Document | 1 | 17 | Counter Document Relationship |
| `c_dunning` | Dunning | 2 | 14 | Dunning Rules for overdue invoices |
| `c_dunninglevel` | Dunning Level | 2 | 28 |  |
| `c_dunninglevel_trl` | Dunning Level Trl | 2 | 13 |  |
| `c_dunningrun` | Dunning Run | 0 | 16 | Dunning Run |
| `c_dunningrunentry` | Dunning Run Entry | 0 | 20 | Dunning Run Entry |
| `c_dunningrunline` | Dunning Run Line | 0 | 23 | Dunning Run Line |
| `c_element` | Element | 1 | 16 | Accounting Element |
| `c_elementvalue` | Account Element | 379 | 30 | Account Element |
| `c_elementvalue_trl` | Account Element Trl | 379 | 13 | Account Element |
| `c_greeting` | Greeting | 1 | 13 | Greeting to print on correspondence |
| `c_greeting_trl` | Greeting Trl | 1 | 13 | Greeting to print on correspondence |
| `c_interorg_acct` | C_InterOrg_Acct | 0 | 12 |  |
| `c_invoice` | Invoice | 8 | 75 | Invoice Identifier |
| `c_invoicebatch` | Invoice Batch | 0 | 20 | Expense Invoice Batch Header |
| `c_invoicebatchline` | Invoice Batch Line | 0 | 37 | Expense Invoice Batch Line |
| `c_invoiceline` | Invoice Line | 24 | 54 | Invoice Detail Line |
| `c_invoicepayschedule` | Invoice Payment Schedule | 2 | 18 | Invoice Payment Schedule |
| `c_invoiceschedule` | Invoice Schedule | 1 | 20 | Schedule for generating Invoices |
| `c_invoicetax` | C_InvoiceTax | 8 | 15 |  |
| `c_job` | Position | 4 | 14 |  |
| `c_jobassignment` | Position Assignment | 0 | 14 |  |
| `c_jobcategory` | Position Category | 4 | 12 |  |
| `c_jobremuneration` | Position Remuneration | 0 | 14 |  |
| `c_landedcost` | Landed Cost | 0 | 17 |  |
| `c_landedcostallocation` | Landed Cost Allocation | 0 | 16 |  |
| `c_location` | Address | 34 | 26 | Location or Address |
| `c_nonbusinessday` | Non Business Day | 1 | 13 | Day on which business is not transacted |
| `c_onlinetrxhistory` | Online Transaction History | 0 | 14 |  |
| `c_opportunity` | Sales Opportunity | 0 | 24 |  |
| `c_order` | Order | 8 | 94 | Order |
| `c_orderlandedcost` | Estimated Landed Cost | 0 | 15 | Estimated Landed Cost for Purchase Order |
| `c_orderlandedcostallocation` | Estimated Landed Cost Allocation | 0 | 15 | Estimate landed cost allocation for order line |
| `c_orderline` | Sales Order Line | 27 | 61 | Sales Order Line |
| `c_orderpayschedule` | Order Payment Schedule | 0 | 18 | Order Payment Schedule |
| `c_ordersource` | Order Source | 0 | 13 |  |
| `c_ordertax` | Order Tax | 8 | 15 |  |
| `c_orgassignment` | Org Assignment | 0 | 13 | Assigment to (transaction) Organization |
| `c_payment` | Payment | 2 | 105 | Payment identifier |
| `c_paymentallocate` | Allocate Payment | 0 | 17 | Allocate Payment to Invoices |
| `c_paymentbatch` | Payment Batch | 0 | 15 | Payment batch for EFT |
| `c_paymentprocessor` | Payment Processor | 2 | 36 | Payment processor for electronic payments |
| `c_paymentterm` | Payment Term | 5 | 30 | The terms for Payment of this transaction |
| `c_paymentterm_trl` | Payment Term Trl | 5 | 14 | The terms of Payment (timing, discount) |
| `c_paymenttransaction` | Payment Transaction | 0 | 81 | Payment Transaction |
| `c_payschedule` | Payment Schedule | 2 | 17 | Payment Schedule Template |
| `c_payselection` | Payment Selection | 1 | 20 | Payment Selection |
| `c_payselectioncheck` | Pay Selection Check | 1 | 23 | Payment Selection Check |
| `c_payselectionline` | Payment Selection Line | 1 | 23 | Payment Selection Line |
| `c_period` | Period | 360 | 16 | Period of the Calendar |
| `c_periodcontrol` | Period Control | 10,464 | 14 |  |
| `c_phase` | Standard Phase | 13 | 16 | Standard Phase of the Project Type |
| `c_pos` | POS Terminal | 1 | 26 | Point of Sales Terminal |
| `c_poskey` | POS Key | 163 | 22 | POS Function Key |
| `c_poskeylayout` | POS Key Layout | 5 | 16 | POS Function Key Layout |
| `c_pospayment` | POS Payment | 0 | 30 |  |
| `c_postendertype` | POS Tender Type | 0 | 16 |  |
| `c_project` | Project | 2 | 48 | Financial Project |
| `c_project_acct` | C_Project_Acct | 4 | 12 |  |
| `c_projectissue` | Project Issue | 0 | 27 | Project Issues (Material, Labor) |
| `c_projectissuema` | C_ProjectIssueMA | 0 | 11 |  |
| `c_projectline` | Project Line | 1 | 31 | Task or step in a project |
| `c_projectphase` | Project Phase | 0 | 27 | Phase of a Project |
| `c_projecttask` | Project Task | 0 | 20 | Actual Project Task in a Phase |
| `c_projecttype` | Project Type | 4 | 13 | Type of the project |
| `c_recurring` | Recurring | 1 | 26 | Recurring Document |
| `c_recurring_run` | Recurring Run | 0 | 16 | Recurring Document Run |
| `c_recurringgroup` | Recurring Group | 0 | 13 |  |
| `c_region` | Region | 399 | 13 | Identifies a geographical Region |
| `c_region_trl` | Region | 399 | 12 | Identifies a geographical Region |
| `c_remuneration` | Remuneration | 0 | 18 |  |
| `c_revenuerecog_service` | Revenue Recognition Service | 0 | 13 | Plan for recognizing or recording revenue based on service |
| `c_revenuerecognition` | Revenue Recognition | 2 | 15 | Method for recording revenue |
| `c_revenuerecognition_plan` | Revenue Recognition Plan | 0 | 17 | Plan for recognizing or recording revenue |
| `c_revenuerecognition_run` | Revenue Recognition Run | 0 | 14 | Revenue Recognition Run or Process |
| `c_rfq` | RfQ | 1 | 38 | Request for Quotation |
| `c_rfq_topic` | RfQ Topic | 1 | 13 | Topic for Request for Quotations |
| `c_rfq_topicsubscriber` | RfQ Subscriber | 2 | 15 | Request for Quotation Topic Subscriber |
| `c_rfq_topicsubscriberonly` | RfQ Topic Subscriber Restriction | 0 | 13 | Include Subscriber only for certain products or product categories |
| `c_rfqline` | RfQ Line | 2 | 18 | Request for Quotation Line |
| `c_rfqlineqty` | RfQ Line Quantity | 2 | 19 | Request for Quotation Line Quantity |
| `c_rfqresponse` | RfQ Response | 0 | 31 | Request for Quotation Response from a potential Vendor |
| `c_rfqresponseline` | RfQ Response Line | 0 | 18 | Request for Quotation Response Line |
| `c_rfqresponselineqty` | RfQ Response Line Qty | 0 | 14 | Request for Quotation Response Line Quantity |
| `c_salesregion` | Sales Region | 2 | 15 | Sales coverage region |
| `c_salesregion_trl` | Sales Region Trl | 2 | 13 | Sales coverage region |
| `c_salesstage` | Sales Stage | 0 | 15 | Stages of the sales process |
| `c_salesstage_trl` | Sales Stage Trl | 0 | 13 | Stages of the sales process |
| `c_servicelevel` | Service Level | 0 | 16 | Product Revenue Recognition Service Level  |
| `c_servicelevelline` | Service Level Line | 0 | 14 | Product Revenue Recognition Service Level Line |
| `c_subacct` | Sub Account | 0 | 14 | Sub account for Element Value |
| `c_subscription` | Subscription | 0 | 17 | Subscription of a Business Partner of a Product to renew |
| `c_subscription_delivery` | Subscription Delivery | 0 | 10 | Optional Delivery Record for a Subscription |
| `c_subscriptiontype` | Subscription Type | 0 | 13 | Type of subscription |
| `c_task` | Standard Task | 9 | 16 | Standard Project Type Task |
| `c_tax` | Tax | 6 | 32 | Tax identifier |
| `c_tax_acct` | C_Tax_Acct | 12 | 15 |  |
| `c_tax_trl` | Tax Trl | 6 | 14 | Tax identifier |
| `c_taxbase` | Tax Base | 0 | 15 |  |
| `c_taxcategory` | Tax Category | 1 | 13 | Tax Category |
| `c_taxcategory_trl` | Tax Category Trl | 1 | 13 | Tax Category |
| `c_taxdeclaration` | Tax Declaration | 0 | 16 | Define the declaration to the tax authorities |
| `c_taxdeclarationacct` | Tax Declaration Accounting | 0 | 14 | Tax Accounting Reconciliation  |
| `c_taxdeclarationline` | Tax Declaration Line | 0 | 22 | Tax Declaration Document Information |
| `c_taxdefinition` | Tax Definition | 0 | 29 |  |
| `c_taxgroup` | Tax Group | 0 | 13 | Tax Group |
| `c_taxpostal` | Tax ZIP | 0 | 12 | Tax Postal/ZIP |
| `c_taxprovider` | Tax Provider | 0 | 16 |  |
| `c_taxprovidercfg` | Tax Provider Configuration | 0 | 13 |  |
| `c_taxtype` | Tax Type | 0 | 13 |  |
| `c_uom` | UOM | 15 | 18 | Unit of Measure |
| `c_uom_conversion` | UOM Conversion | 1 | 14 | Unit of Measure Conversion |
| `c_uom_trl` | UOM Trl | 15 | 14 | Unit of Measure |
| `c_userremuneration` | Employee Remuneration | 0 | 18 | Employee Wage or Salary Overwrite |
| `c_validcombination` | Combination | 157 | 29 | Valid Account Combination |
| `c_withholding` | Withholding | 0 | 23 | Withholding type defined |
| `c_withholding_acct` | C_Withholding_Acct | 0 | 11 |  |
| `c_year` | Year | 30 | 13 | Calendar Year |
| `cm_accesscontainer` | Web Access Container | 0 | 10 |  |
| `cm_accesslistbpgroup` | Web Access BP Group | 0 | 10 |  |
| `cm_accesslistrole` | Web Access Role | 0 | 10 |  |
| `cm_accessmedia` | Web Access Media | 0 | 10 |  |
| `cm_accessnewschannel` | Web Access NewsChannel | 0 | 10 |  |
| `cm_accessprofile` | Web Access Profile | 0 | 13 | Web Access Profile |
| `cm_accessstage` | Web Access Stage | 0 | 10 |  |
| `cm_ad` | Advertisement | 0 | 26 | An Advertisement is something like a banner |
| `cm_ad_cat` | Advertisement Category | 0 | 13 | Advertisement Categories define rotations and ad blocks |
| `cm_broadcastserver` | Broadcast Server | 0 | 15 | Web Broadcast Server |
| `cm_chat` | Chat | 0 | 16 |  |
| `cm_chatentry` | Chat Entry | 0 | 18 |  |
| `cm_chattype` | Chat Type | 0 | 13 |  |
| `cm_chattypeupdate` | Chat Type Update | 0 | 11 |  |
| `cm_chatupdate` | Chat Update | 0 | 11 |  |
| `cm_container` | Web Container | 5 | 35 | Web Container contains content like images, text etc. |
| `cm_container_element` | Container Element | 6 | 15 | Container element i.e. Headline, Content, Footer etc. |
| `cm_container_element_trl` | Container Element Trl | 6 | 15 | Container element i.e. Headline, Content, Footer etc. |
| `cm_container_trl` | Web Container Trl | 5 | 17 | Web Container contains content like images, text etc. |
| `cm_container_url` | Container URL | 0 | 13 | Contains info on used URLs |
| `cm_containerttable` | Container T.Table | 0 | 16 | Container Template Table |
| `cm_cstage` | Web Container Stage | 5 | 37 | Container Stage contains the staging content like images, text etc. |
| `cm_cstage_element` | Container Stage Element | 7 | 15 | Container element i.e. Headline, Content, Footer etc. |
| `cm_cstage_element_trl` | Container Stage Element Trl | 7 | 15 | Container element i.e. Headline, Content, Footer etc. |
| `cm_cstage_trl` | Web Container Stage Trl | 5 | 17 | Web Container Stage contains the staging content like images, text etc. |
| `cm_cstagettable` | Stage T.Table | 0 | 16 | Containet Stage Template Table |
| `cm_media` | Media Item | 3 | 18 | Contains media content like images, flash movies etc. |
| `cm_media_server` | Media Server | 1 | 19 | Media Server list to which content should get transfered |
| `cm_mediadeploy` | Media Deploy | 0 | 14 | Media Deployment Log |
| `cm_newschannel` | News Channel | 0 | 15 | News channel for rss feed |
| `cm_newsitem` | News Item / Article | 0 | 16 | News item or article defines base content |
| `cm_template` | Template | 4 | 22 | Template defines how content is displayed |
| `cm_template_ad_cat` | Template Advertising Category | 0 | 12 | Get together the Template and the Advertising Category |
| `cm_templatetable` | Template Table | 0 | 15 | CM Template Table Link |
| `cm_webaccesslog` | Web Access Log | 0 | 27 |  |
| `cm_webproject` | Web Project | 1 | 21 | A web project is the main data container for Containers, URLs, Ads, Media etc. |
| `cm_webproject_domain` | WebProject Domain | 1 | 15 | Web Project Domain handling |
| `cm_wikitoken` | Wiki Token | 0 | 16 | Wiki Token |
| `dbreplicasyncverifier` | dbreplicasyncverifier | 1 | 1 |  |
| `dd_networkdistribution` | Network Distribution | 2 | 20 | Network Distribution |
| `dd_networkdistributionline` | Network Distribution Line | 10 | 18 | Network Distribution Line |
| `dd_order` | Distribution Order | 0 | 64 | Distribution Order |
| `dd_orderline` | Distribution Order Line | 0 | 43 | Distribution Order Line |
| `exp_format` | Export Format | 10 | 19 |  |
| `exp_formatline` | Format Line | 43 | 21 |  |
| `exp_processor` | Export Processor | 2 | 18 |  |
| `exp_processor_type` | Export Processor Type | 2 | 14 |  |
| `exp_processorparameter` | Processor Parameter | 7 | 15 |  |
| `fact_acct` | Accounting Fact | 0 | 57 |  |
| `fact_acct_summary` | Accounting Fact summary | 0 | 45 |  |
| `fact_reconciliation` | Accounting Fact Reconciliation | 0 | 11 |  |
| `gl_budget` | Budget | 1 | 13 | General Ledger Budget |
| `gl_budgetcontrol` | Budget Control | 0 | 17 | Budget Control |
| `gl_category` | GL Category | 10 | 16 | General Ledger Category |
| `gl_category_trl` | GL Category Trl | 10 | 13 | General Ledger Category |
| `gl_distribution` | GL Distribution | 1 | 62 | General Ledger Distribution |
| `gl_distributionline` | GL Distribution Line | 2 | 53 | General Ledger Distribution Line |
| `gl_fund` | GL Fund | 0 | 16 | General Ledger Funds Control |
| `gl_fundrestriction` | Fund Restriction | 0 | 13 | Restriction of Funds |
| `gl_journal` | Journal | 2 | 36 | General Ledger Journal |
| `gl_journalbatch` | Journal Batch | 1 | 28 | General Ledger Journal Batch |
| `gl_journalgenerator` | GL Journal Generator | 2 | 19 |  |
| `gl_journalgeneratorline` | Generator Line | 6 | 22 |  |
| `gl_journalgeneratorsource` | Generator Source | 8 | 15 |  |
| `gl_journalline` | Journal Line | 4 | 50 | General Ledger Journal Line |
| `hr_attribute` | Payroll Employee Attribute | 0 | 28 |  |
| `hr_concept` | Payroll Concept | 0 | 30 |  |
| `hr_concept_acct` | Payroll Concept Account | 0 | 17 |  |
| `hr_concept_category` | Payroll Concept Category | 0 | 14 |  |
| `hr_contract` | Payroll Contract | 0 | 18 |  |
| `hr_department` | Payroll Department | 0 | 13 |  |
| `hr_employee` | Payroll Employee | 0 | 22 |  |
| `hr_job` | Payroll Job | 0 | 17 |  |
| `hr_list` | Payroll List | 0 | 18 |  |
| `hr_listline` | Payroll List Line | 0 | 21 |  |
| `hr_listtype` | Payroll List Type | 0 | 12 |  |
| `hr_listversion` | Payroll List Version | 0 | 15 |  |
| `hr_movement` | Payroll Movement | 0 | 39 |  |
| `hr_payroll` | Payroll | 0 | 18 |  |
| `hr_payrollconcept` | Payroll Concept | 0 | 17 |  |
| `hr_period` | Payroll Period | 0 | 23 |  |
| `hr_process` | Payroll Process | 0 | 32 |  |
| `hr_year` | Payroll Year | 0 | 16 |  |
| `i_asset` | Asset | 0 | 83 |  |
| `i_bankstatement` | Import Bank Statement | 0 | 60 | Import of the Bank Statement |
| `i_bpartner` | Import Business Partner | 0 | 51 |  |
| `i_conversion_rate` | Import Conversion Rate | 2 | 25 | Import Currency Conversion Rate |
| `i_elementvalue` | Import Account | 0 | 31 | Import Account Value |
| `i_fajournal` | FA Journal | 0 | 72 |  |
| `i_fixedasset` | Imported Fixed Asset | 0 | 54 |  |
| `i_gljournal` | Import GL Journal | 0 | 70 | Import General Ledger Journal |
| `i_hr_movement` | Payroll Movement Import | 0 | 26 |  |
| `i_inoutlineconfirm` | Ship/Receipt Confirmation Import Line | 0 | 19 | Material Shipment or Receipt Confirmation Import Line |
| `i_inventory` | Import Inventory | 0 | 38 | Import Inventory Transactions |
| `i_invoice` | Import Invoice | 0 | 65 | Import Invoice |
| `i_movement` | I_Movement_ID | 0 | 44 |  |
| `i_order` | Import Order | 0 | 68 | Import Orders |
| `i_payment` | Import Payment | 0 | 74 | Import Payment |
| `i_pricelist` | Import Price List | 0 | 34 | Import Price List and Versions |
| `i_product` | Import Product | 0 | 59 | Import Item or Service |
| `i_productplanning` | Import Product Planning | 0 | 52 |  |
| `i_reportline` | Import Report Line Set | 0 | 30 | Import Report Line Set values |
| `imp_processor` | Import Processor | 2 | 24 |  |
| `imp_processor_type` | Import Processor Type | 2 | 14 |  |
| `imp_processorlog` | Import Processor Log | 0 | 17 |  |
| `imp_processorparameter` | Import Processor Parameter | 6 | 15 |  |
| `k_category` | Knowledge Category | 1 | 12 | Knowledge Category |
| `k_categoryvalue` | Category Value | 0 | 12 | The value of the category |
| `k_comment` | Entry Comment | 0 | 14 | Knowledge Entry Comment |
| `k_entry` | Entry | 0 | 19 | Knowledge Entry |
| `k_entrycategory` | K_EntryCategory | 0 | 11 |  |
| `k_entryrelated` | Related Entry | 0 | 11 | Related Entry for this Enntry |
| `k_index` | Index | 0 | 17 |  |
| `k_indexlog` | Index Log | 0 | 12 |  |
| `k_indexstop` | Index Stop | 0 | 14 |  |
| `k_source` | Knowledge Source | 1 | 11 | Source of a Knowledge Entry |
| `k_synonym` | Knowledge Synonym | 0 | 12 | Knowlege Keyword Synonym |
| `k_topic` | Knowledge Topic | 1 | 15 | Knowledge Topic |
| `k_type` | Knowledge Type | 2 | 14 | Knowledge Type |
| `m_attribute` | Attribute | 4 | 21 | Product Attribute |
| `m_attributeinstance` | M_AttributeInstance | 5 | 15 |  |
| `m_attributeinstanceline` | Attribute Instance Values | 0 | 12 | Selected attribute values of an attribute instance |
| `m_attributesearch` | Attribute Search | 1 | 11 | Common Search Attribute  |
| `m_attributeset` | Attribute Set | 4 | 30 | Product Attribute Set |
| `m_attributesetexclude` | Exclude Attribute Set | 0 | 12 | Exclude the ability to enter Attribute Sets |
| `m_attributesetinstance` | Attribute Set Instance | 4 | 15 | Product Attribute Set Instance |
| `m_attributeuse` | M_AttributeUse | 5 | 13 |  |
| `m_attributevalue` | Attribute Value | 9 | 14 | Product Attribute Value |
| `m_bom` | BOM | 1 | 17 | Bill of Material |
| `m_bomalternative` | Alternative Group | 1 | 12 | Product BOM Alternative Group |
| `m_bomproduct` | BOM Component | 0 | 23 | Bill of Material Component (Product) |
| `m_bp_price` | Business Partner Price | 0 | 22 | Business Partner specific pricing that will override the price list |
| `m_changenotice` | Change Notice | 1 | 16 |  |
| `m_changerequest` | Change Request | 0 | 19 |  |
| `m_commodityshipment` | Commodity Shipment | 0 | 14 |  |
| `m_cost` | Product Cost | 267 | 23 |  |
| `m_costdetail` | Cost Detail | 0 | 37 | Cost Detail Information |
| `m_costelement` | Cost Element | 9 | 14 |  |
| `m_costhistory` | Cost History | 0 | 25 | Movement history for M_Cost |
| `m_costqueue` | Cost Queue | 0 | 16 | FiFo/LiFo Cost Queue |
| `m_costtype` | Cost Type | 1 | 12 | Type of Cost |
| `m_demand` | Demand | 0 | 16 | Material Demand |
| `m_demanddetail` | Demand Detail | 0 | 13 | Material Demand Line Source Detail |
| `m_demandline` | Demand Line | 0 | 14 | Material Demand Line |
| `m_discountschema` | Discount Schema | 3 | 19 | Schema to calculate the trade discount percentage |
| `m_discountschemabreak` | Discount Schema Break | 1 | 17 | Trade Discount Break |
| `m_discountschemaline` | Discount Price List | 11 | 43 | Line of the price list trade discount schema |
| `m_distributionlist` | Distribution List | 1 | 14 | Distribution Lists allow to distribute products to a selected list of partners |
| `m_distributionlistline` | Distribution List Line | 3 | 15 | Distribution List Line with Business Partner and Quantity/Percentage |
| `m_distributionrun` | Distribution Run | 1 | 15 | Distribution Run create Orders to distribute products to a selected list of partners |
| `m_distributionrunline` | Distribution Run Line | 1 | 16 | Distribution Run Lines define Distribution List, the Product and Quantiries |
| `m_edi` | EDI Transaction | 0 | 27 |  |
| `m_edi_info` | EDI Log | 0 | 10 |  |
| `m_forecast` | Forecast | 4 | 17 | Material Forecast |
| `m_forecastline` | Forecast Line | 50 | 17 | Forecast Line |
| `m_freight` | Freight | 3 | 20 | Freight Rate |
| `m_freightcategory` | Freight Category | 2 | 13 | Category of the Freight |
| `m_inout` | Shipment/Receipt | 9 | 80 | Material Shipment Document |
| `m_inoutconfirm` | Ship/Receipt Confirmation | 1 | 25 | Material Shipment or Receipt Confirmation |
| `m_inoutline` | Shipment/Receipt Line | 27 | 42 | Line on Shipment or Receipt document |
| `m_inoutlineconfirm` | Ship/Receipt Confirmation Line | 1 | 20 | Material Shipment or Receipt Confirmation Line |
| `m_inoutlinema` | M_InOutLineMA | 0 | 13 |  |
| `m_inventory` | Phys.Inventory | 3 | 37 | Parameters for a Physical Inventory |
| `m_inventoryline` | Phys.Inventory Line | 1 | 27 | Unique line in an Inventory document |
| `m_inventorylinema` | M_InventoryLineMA | 0 | 13 |  |
| `m_locator` | Locator | 11 | 17 | Warehouse Locator |
| `m_locatortype` | Locator Type | 0 | 15 |  |
| `m_lot` | Lot | 0 | 16 | Product Lot Definition |
| `m_lotctl` | Lot Control | 1 | 16 | Product Lot Control |
| `m_lotctlexclude` | Exclude Lot | 0 | 12 | Exclude the ability to create Lots in Attribute Sets |
| `m_matchinv` | Match Invoice | 18 | 24 | Match Shipment/Receipt to Invoice |
| `m_matchpo` | Match PO | 37 | 27 | Match Purchase Order to Shipment/Receipt and Invoice |
| `m_movement` | Inventory Move | 1 | 49 | Movement of Inventory |
| `m_movementconfirm` | Move Confirm | 0 | 19 | Inventory Move Confirmation |
| `m_movementline` | Move Line | 1 | 28 | Inventory Move document Line |
| `m_movementlineconfirm` | Move Line Confirm | 0 | 18 | Inventory Move Line Confirmation |
| `m_movementlinema` | M_MovementLineMA | 0 | 13 |  |
| `m_operationresource` | Operation Resource | 0 | 18 | Product Operation Resource |
| `m_package` | Package | 1 | 72 | Shipment Package |
| `m_packageline` | Package Line | 1 | 15 | The detail content of the Package |
| `m_packagemps` | Package MPS | 0 | 23 |  |
| `m_parttype` | Part Type | 0 | 11 | Manufacturing part type |
| `m_perpetualinv` | Perpetual Inventory | 0 | 20 | Rules for generating physical inventory |
| `m_pricelist` | Price List | 4 | 20 | Unique identifier of a Price List |
| `m_pricelist_trl` | Price List | 4 | 13 | Unique identifier of a Price List |
| `m_pricelist_version` | Price List Version | 6 | 16 | Identifies a unique instance of a Price List |
| `m_pricelist_version_trl` | Price List Version Trl | 6 | 12 | Identifies a unique instance of a Price List |
| `m_product` | Product | 255 | 73 | Product Service Item |
| `m_product_acct` | Product Acct | 110 | 34 |  |
| `m_product_bom_old` | m_product_bom_old | 20 | 15 |  |
| `m_product_category` | Product Category | 14 | 19 | Category of a Product |
| `m_product_category_acct` | Product Category Acct | 28 | 37 |  |
| `m_product_category_trl` | Product Category Trl | 14 | 13 | Category of a Product |
| `m_product_po` | Product Purchasing | 29 | 32 |  |
| `m_product_qualitytest` | Product Quality Test | 0 | 12 |  |
| `m_product_trl` | Product Trl | 55 | 14 | Product, Service, Item |
| `m_productdownload` | Product Download | 1 | 12 | Product downloads |
| `m_production` | Production | 0 | 43 | Plan for producing a product |
| `m_productionline` | Production Line | 0 | 23 | Document Line representing a production |
| `m_productionlinema` | Production Line MA | 0 | 12 |  |
| `m_productionplan` | Production Plan | 0 | 16 | Plan for how a product is produced |
| `m_productoperation` | Product Operation | 0 | 16 |  |
| `m_productprice` | Product Price | 114 | 14 |  |
| `m_productpricevendorbreak` | Product Price Break | 0 | 16 |  |
| `m_promotion` | Promotion | 200 | 13 | Promotion setup |
| `m_promotiondistribution` | Promotion Distribution | 0 | 16 | Distribute order line items into multiple bucket for reward calculation |
| `m_promotiongroup` | Promotion Group | 200 | 11 | Grouping of product for promotion setup |
| `m_promotiongroupline` | Promotion Group Line | 600 | 11 | Line items of a promotion group |
| `m_promotionline` | Promotion Line | 200 | 13 | Promotion line items |
| `m_promotionprecondition` | Promotion Pre Condition | 0 | 21 | Pre condition for promotion |
| `m_promotionreward` | Promotion Reward | 0 | 20 | Setup reward for the promotion |
| `m_qualitytest` | Quality Test | 0 | 12 |  |
| `m_qualitytestresult` | Quality Test Result | 0 | 14 |  |
| `m_relatedproduct` | Product Related | 1 | 13 |  |
| `m_replenish` | M_Replenish | 19 | 16 |  |
| `m_requisition` | Requisition | 1 | 27 | Material Requisition |
| `m_requisitionline` | Requisition Line | 1 | 21 | Material Requisition Line |
| `m_rma` | RMA | 1 | 31 | Return Material Authorization |
| `m_rmaline` | RMA Line | 1 | 25 | Return Material Authorization Line |
| `m_rmatax` | RMA Tax | 0 | 15 | Return Material Authorization Tax |
| `m_rmatype` | RMA Type | 1 | 12 | Return Material Authorization Type |
| `m_sernoctl` | Serial No Control | 1 | 16 | Product Serial Number Control |
| `m_sernoctlexclude` | Exclude Ser No | 0 | 12 | Exclude the ability to create Serial Numbers in Attribute Sets |
| `m_shipper` | Shipper | 3 | 14 | Method or manner of product delivery |
| `m_shippercfg` | Shipper Configuration | 1 | 19 | Method or manner of product delivery |
| `m_shipperlabels` | Shipper Labels | 0 | 14 |  |
| `m_shipperlabelscfg` | Shipper Labels Configuration | 0 | 17 |  |
| `m_shipperpackaging` | Shipper Packaging | 0 | 14 |  |
| `m_shipperpackagingcfg` | Shipper Packaging Configuration | 0 | 15 |  |
| `m_shipperpickuptypes` | Shipper Pickup Types | 0 | 13 |  |
| `m_shipperpickuptypescfg` | Shipper Pickup Types Configuration | 0 | 14 |  |
| `m_shippingprocessor` | Shipping Processor | 1 | 14 |  |
| `m_shippingprocessorcfg` | Shipping Processor Configuration | 1 | 19 |  |
| `m_shippingtransaction` | Shipping Transaction | 0 | 89 | Shipping Transaction |
| `m_shippingtransactionline` | Shipping Transaction Line | 0 | 23 | Shipping Transaction Line |
| `m_storageonhand` | M_StorageOnHand | 20 | 14 |  |
| `m_storagereservation` | M_StorageReservation | 2 | 14 |  |
| `m_storagereservationlog` | Storage Reservation Log | 0 | 21 | Log for every storage reservation quantity change |
| `m_substitute` | M_Substitute | 0 | 12 |  |
| `m_transaction` | Inventory Transaction | 28 | 21 |  |
| `m_transactionallocation` | M_TransactionAllocation | 0 | 22 |  |
| `m_warehouse` | Warehouse | 11 | 20 | Storage Warehouse and Service Point |
| `m_warehouse_acct` | M_Warehouse_Acct | 22 | 14 |  |
| `mfa_method` | MFA Method | 2 | 21 | Multi-factor Authentication Method |
| `mfa_registereddevice` | MFA Registered Device | 0 | 13 | Multi-factor Authentication Registered Device |
| `mfa_registration` | MFA Registration | 0 | 24 | Multi-factor Authentication Registration |
| `mfa_rule` | MFA Rule | 2 | 11 | Multi-factor Authentication Rule |
| `pa_achievement` | Achievement | 0 | 17 | Performance Achievement |
| `pa_benchmark` | Benchmark | 0 | 13 | Performance Benchmark |
| `pa_benchmarkdata` | Benchmark Data | 0 | 14 | Performance Benchmark Data Point |
| `pa_colorschema` | Color Schema | 2 | 20 | Performance Color Schema |
| `pa_dashboardcontent` | Dashboard Content | 12 | 33 |  |
| `pa_dashboardcontent_access` | PA_DashboardContent_Access_ID | 2 | 12 |  |
| `pa_dashboardcontent_trl` | Dashboard Content Trl | 12 | 15 |  |
| `pa_dashboardpreference` | Dashboard Preference | 0 | 17 |  |
| `pa_documentstatus` | Document Status | 16 | 30 |  |
| `pa_documentstatus_trl` | Document Status Trl | 16 | 14 |  |
| `pa_documentstatusaccess` | Document Status Access | 10 | 12 |  |
| `pa_goal` | Goal | 4 | 29 | Performance Goal |
| `pa_goalrestriction` | Goal Restriction | 0 | 17 | Performance Goal Restriction |
| `pa_hierarchy` | Reporting Hierarchy | 0 | 20 | Reporting Hierarchy |
| `pa_measure` | Measure | 4 | 22 | Concrete Performance Measurement |
| `pa_measurecalc` | Measure Calculation | 6 | 20 | Calculation method for measuring performance |
| `pa_ratio` | Ratio | 1 | 13 | Performace Ratio |
| `pa_ratioelement` | Ratio Element | 3 | 20 | Performance Ratio Element |
| `pa_report` | Financial Report | 3 | 24 | Financial Report |
| `pa_reportcolumn` | Report Column | 17 | 59 | Column in Report |
| `pa_reportcolumn_trl` | Report Column Trl | 17 | 13 | Column in Report |
| `pa_reportcolumnset` | Report Column Set | 3 | 12 | Collection of Columns for Report |
| `pa_reportcube` | Report Cube | 0 | 31 | Define reporting cube for pre-calculation of summary accounting data. |
| `pa_reportline` | Report Line | 113 | 31 |  |
| `pa_reportline_trl` | Report Line Trl | 113 | 13 |  |
| `pa_reportlineset` | Report Line Set | 3 | 12 |  |
| `pa_reportsource` | Report Source | 93 | 36 | Restriction of what will be shown in Report Line |
| `pa_sla_criteria` | SLA Criteria | 2 | 14 | Service Level Agreement Criteria |
| `pa_sla_goal` | SLA Goal | 1 | 21 | Service Level Agreement Goal |
| `pa_sla_measure` | SLA Measure | 1 | 17 | Service Level Agreement Measure |
| `pp_cost_collector` | Manufacturing Cost Collector | 0 | 47 |  |
| `pp_cost_collectorma` | Manufacturing Order MA | 0 | 12 |  |
| `pp_mrp` | Material Requirement Planning | 56 | 41 | Material Requirement Planning |
| `pp_order` | Manufacturing Order | 2 | 68 | Manufacturing Order |
| `pp_order_bom` | Manufacturing Order BOM | 2 | 26 |  |
| `pp_order_bom_trl` | Manufacturing Order BOM Trl | 2 | 14 |  |
| `pp_order_bomline` | Manufacturing Order BOM Line | 4 | 44 |  |
| `pp_order_bomline_trl` | Manufacturing Order BOM Line Trl | 4 | 13 |  |
| `pp_order_cost` | Manufacturing Order Cost | 0 | 24 |  |
| `pp_order_node` | Manufacturing Order Activity | 2 | 70 | Manufacturing Order Activity |
| `pp_order_node_asset` | Manufacturing Order Activity Asset | 0 | 13 | Manufacturing Order Activity Asset |
| `pp_order_node_product` | Manufacturing Order Activity Product | 0 | 17 | Manufacturing Order Activity Product |
| `pp_order_node_trl` | Manufacturing Order Activity Trl | 2 | 14 | Workflow Node (activity), step or process |
| `pp_order_nodenext` | Manufacturing Order Activity Next | 0 | 19 | Manufacturing Order Activity Next |
| `pp_order_workflow` | Manufacturing Order Workflow | 2 | 47 | Manufacturing Order Workflow |
| `pp_order_workflow_trl` | Manufacturing Order Workflow Trl | 2 | 14 |  |
| `pp_product_bom` | BOM & Formula | 7 | 25 | BOM & Formula |
| `pp_product_bom_trl` | BOM & Formula Trl | 7 | 14 | BOM & Formula |
| `pp_product_bomline` | BOM Line | 21 | 32 | BOM Line |
| `pp_product_bomline_trl` | BOM Line Trl | 21 | 13 | BOM Line |
| `pp_product_planning` | Product Planning | 219 | 34 | Product Planning |
| `pp_wf_node_asset` | Workflow Node Asset | 0 | 12 | Workflow Node Asset |
| `pp_wf_node_product` | Workflow Node Product | 0 | 17 | Workflow Node Product |
| `qm_specification` | Quality Specification | 0 | 18 | Quality Specification |
| `qm_specificationline` | QM Specification Line | 0 | 17 |  |
| `r_category` | Category | 3 | 13 | Request Category |
| `r_categoryupdates` | R_CategoryUpdates | 1 | 11 |  |
| `r_contactinterest` | R_ContactInterest | 1 | 12 |  |
| `r_group` | Group | 2 | 15 | Request Group |
| `r_groupupdates` | R_GroupUpdates | 1 | 11 |  |
| `r_interestarea` | Interest Area | 2 | 13 | Interest Area or Topic |
| `r_issueknown` | Known Issue | 0 | 21 | Known Issue |
| `r_issueproject` | Issue Project | 0 | 16 |  |
| `r_issuerecommendation` | Issue Recommendation | 0 | 12 |  |
| `r_issuesource` | r_issuesource | 0 | 13 |  |
| `r_issuestatus` | Issue Status | 0 | 11 |  |
| `r_issuesystem` | Issue System | 0 | 14 |  |
| `r_issueuser` | Issue User | 0 | 12 | User who reported issues |
| `r_mailtext` | Mail Template | 3 | 15 | Text templates for mailings |
| `r_mailtext_trl` | Mail Template Trl | 3 | 16 | Text templates for mailings |
| `r_request` | Request | 1 | 68 | Request from a Business Partner or Prospect |
| `r_requestaction` | Request History | 2 | 46 |  |
| `r_requestprocessor` | Request Processor | 1 | 24 |  |
| `r_requestprocessor_route` | Request Routing | 1 | 14 | Automatic routing of requests |
| `r_requestprocessorlog` | Request Processor Log | 0 | 16 |  |
| `r_requesttype` | Request Type | 3 | 25 | Type of request (e.g. Inquiry, Complaint, ..) |
| `r_requesttypeupdates` | Request Type Updates | 1 | 11 |  |
| `r_requestupdate` | Request Update | 1 | 17 |  |
| `r_requestupdates` | Request Update Recipiants | 0 | 11 |  |
| `r_resolution` | Resolution | 3 | 12 | Request Resolution |
| `r_standardresponse` | Standard Response | 1 | 11 | Request Standard Response  |
| `r_status` | Status | 4 | 23 | Request Status |
| `r_statuscategory` | Status Category | 1 | 13 | Request Status Category |
| `s_expensetype` | Expense Type | 1 | 16 | Expense report type |
| `s_resource` | Resource | 11 | 24 | Resource |
| `s_resourceassignment` | Resource Assignment | 2 | 16 | Resource Assignment |
| `s_resourcetype` | Resource Type | 3 | 29 |  |
| `s_resourceunavailable` | Resource Unavailability | 2 | 13 |  |
| `s_timeexpense` | Expense Report | 1 | 21 | Time and Expense Report |
| `s_timeexpenseline` | Expense Line | 4 | 39 | Time and Expense Report Line |
| `s_timetype` | Time Type | 0 | 12 | Type of time recorded |
| `s_training` | Training | 1 | 19 | Repeated Training |
| `s_training_class` | Training Class | 0 | 13 | The actual training class instance |
| `sso_principalconfig` | SSO Configuration | 0 | 21 |  |
| `t_1099extract` | 1099 Extract | 0 | 32 |  |
| `t_aging` | T_Aging | 0 | 46 |  |
| `t_alter_column` | t_alter_column | 0 | 5 |  |
| `t_bankregister` | Bank Register | 0 | 14 |  |
| `t_bom_indented` | Indented BOM Report | 0 | 25 | Indented BOM Report |
| `t_bomline` | Temporal BOM Line | 0 | 30 | Temporal BOM Line |
| `t_cashflow` | T_CashFlow_ID | 0 | 30 |  |
| `t_distributionrundetail` | T_DistributionRunDetail | 0 | 18 |  |
| `t_fact_acct_history` | Accounting Fact History | 0 | 57 |  |
| `t_inventoryvalue` | T_InventoryValue | 0 | 24 |  |
| `t_invoicegl` | T_InvoiceGL | 0 | 25 | Gain/Loss - actual data shown id T_InvoiceGL_v |
| `t_moveclient` | t_moveclient | 0 | 5 |  |
| `t_mrp_crp` | Temporal MRP & CRP | 0 | 12 | Temporal MRP & CRP |
| `t_reconciliation` | Account reconciliation report | 0 | 11 |  |
| `t_replenish` | T_Replenish | 0 | 21 |  |
| `t_report` | T_Report | 0 | 40 | Temporary Reporting Table |
| `t_reportstatement` | T_ReportStatement | 0 | 11 |  |
| `t_selection` | t_selection | 0 | 4 |  |
| `t_selection2` | t_selection2 | 0 | 3 |  |
| `t_selection_infowindow` | t_selection_infowindow | 0 | 9 |  |
| `t_spool` | T_Spool | 0 | 3 | Temporary Spool Table |
| `t_transaction` | T_Transaction | 0 | 29 |  |
| `t_trialbalance` | Trial Balance | 0 | 46 |  |
| `test` | Test ID | 2 | 36 |  |
| `testuu` | Test UU Based Table | 2 | 12 |  |
| `testuu_trl` | Test UU Based Table Trl | 2 | 14 |  |
| `testuudet` | Test UU Detail | 3 | 12 |  |
| `u_blacklistcheque` | Black List Cheque | 0 | 11 |  |
| `u_posterminal` | POS Terminal | 1 | 37 |  |
| `u_rolemenu` | Role Menu | 74 | 11 |  |
| `u_web_properties` | Web Properties | 143 | 11 |  |
| `u_webmenu` | Web Menu | 143 | 20 |  |
| `w_advertisement` | Advertisement | 1 | 28 | Web Advertisement |
| `w_basket` | Basket | 0 | 14 | Web Basket |
| `w_basketline` | Basket Line | 0 | 16 | Web Basket Line |
| `w_click` | Web Click | 0 | 19 | Individual Web Click |
| `w_clickcount` | Click Count | 1 | 13 | Web Click Management |
| `w_counter` | Web Counter | 0 | 19 | Individual Count hit |
| `w_countercount` | Counter Count | 1 | 13 | Web Counter Count Management |
| `w_mailmsg` | Mail Message | 0 | 17 | Web Store Mail Message Template |
| `w_mailmsg_trl` | Mail Message Trl | 0 | 15 | Web Store Mail Message Template |
| `w_store` | Web Store | 1 | 43 | A Web Store of the Client |
| `w_store_trl` | Web Store Trl | 1 | 20 | A Web Store of the Tenant |
| `ws_webservice` | Web Service | 2 | 13 |  |
| `ws_webservice_para` | Web Service Parameters | 46 | 13 |  |
| `ws_webservicefieldinput` | Web Service Field Input | 45 | 17 |  |
| `ws_webservicefieldoutput` | Web Service Field Output | 8 | 11 |  |
| `ws_webservicemethod` | Web Service Method | 9 | 14 |  |
| `ws_webservicetype` | Web Service Type | 16 | 17 |  |
| `ws_webservicetypeaccess` | Web Service Type Access | 16 | 11 |  |

OpenSearch 더미 적재 후 행 수(2026-11-03T23:29:01+09:00): Product 255, Promotion 200, PromotionGroup 200, PromotionLine 200, PromotionGroupLine 600. [현재 전체 색인](../doc/database/index.md).
