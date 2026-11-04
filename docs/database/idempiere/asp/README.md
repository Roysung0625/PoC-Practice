# asp — ASP 구독·기능 제공 설정

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 13개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`asp_clientexception`](asp_clientexception.md) | 테넌트별 ASP 예외 | Tenant Exception | 0 | 테넌트의 화면·탭·필드·프로세스 등 구성요소별 ASP 적용 예외 상태를 관리한다. |
| [`asp_clientlevel`](asp_clientlevel.md) | 테넌트별 ASP 수준 | Tenant Level | 0 | 테넌트에 연결된 ASP 수준과 모듈을 관리한다. |
| [`asp_field`](asp_field.md) | ASP 필드 설정 | ASP Field | 0 | ASP 탭에 속한 필드와 적용 상태를 관리한다. |
| [`asp_form`](asp_form.md) | ASP 특수 폼 설정 | ASP Form | 0 | ASP 수준별 특수 폼과 적용 상태를 관리한다. |
| [`asp_level`](asp_level.md) | ASP 제공 수준 | ASP Level | 0 | ASP 모듈에 속하는 기능 제공 수준을 정의하며 창·프로세스·워크플로 등의 ASP 설정이 참조한다. |
| [`asp_module`](asp_module.md) | ASP 모듈 | ASP Module | 0 | ASP 기능 제공 설정을 묶는 모듈의 코드·이름·설명을 관리한다. |
| [`asp_process`](asp_process.md) | ASP 프로세스 설정 | ASP Process | 0 | ASP 제공 수준과 애플리케이션 프로세스를 연결하고 ASP 상태를 지정한다. |
| [`asp_process_para`](asp_process_para.md) | ASP 프로세스 매개변수 설정 | ASP Process Parameter | 0 | ASP 프로세스에 속한 개별 실행 매개변수의 ASP 상태를 지정한다. |
| [`asp_ref_list`](asp_ref_list.md) | ASP 참조 목록 설정 | ASP_Ref_List | 0 | ASP 수준별로 참조 정의·목록 항목과 그 상태를 연결한다. |
| [`asp_tab`](asp_tab.md) | ASP 화면 탭 설정 | ASP Tab | 0 | ASP 창에 속한 화면 탭의 상태와 전체 필드 적용 여부를 관리한다. |
| [`asp_task`](asp_task.md) | ASP 작업 설정 | ASP Task | 0 | ASP 제공 수준과 애플리케이션 작업을 연결하고 상태를 지정한다. |
| [`asp_window`](asp_window.md) | ASP 창 설정 | ASP Window | 0 | ASP 제공 수준별 애플리케이션 창과 상태를 지정하며 하위 ASP 탭 설정의 기준이 된다. |
| [`asp_workflow`](asp_workflow.md) | ASP 워크플로 설정 | ASP Workflow | 0 | ASP 제공 수준과 워크플로를 연결하고 해당 상태를 관리한다. |
