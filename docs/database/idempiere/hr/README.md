# hr — 인사·급여

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 18개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`hr_attribute`](hr_attribute.md) | 직원 급여 속성 | Payroll Employee Attribute | 0 | 직원·급여 항목별 적용 값과 계산 규칙·유효 기간을 관리하며 금액·수량·문자·서비스 날짜 등의 형식을 담는다. |
| [`hr_concept`](hr_concept.md) | 급여 계산 항목 | Payroll Concept | 0 | 급여 항목의 유형·값 형식·분류·차대 부호 및 출력·지급 여부를 정의한다. |
| [`hr_concept_acct`](hr_concept_acct.md) | 급여 항목 회계 계정 | Payroll Concept Account | 0 | 급여 항목과 회계 스키마별 수익·비용 계정 및 거래처 그룹 등의 회계 연결을 관리한다. |
| [`hr_concept_category`](hr_concept_category.md) | 급여 항목 분류 | Payroll Concept Category | 0 | 급여 계산 항목의 분류와 연결 계정·기본 여부를 관리한다. |
| [`hr_contract`](hr_contract.md) | 급여 계약 기준 | Payroll Contract | 0 | 급여에 연결되는 계약의 유효 기간·기준 일수와 거래처·프로젝트 등의 관련 정보를 관리한다. |
| [`hr_department`](hr_department.md) | 급여 부서 | Payroll Department | 0 | 급여 부서의 코드·이름과 업무 활동 연결을 관리한다. 공통 부서 기준 c_department와 구분한다. |
| [`hr_employee`](hr_employee.md) | 급여 직원 | Payroll Employee | 0 | 급여 대상 직원을 거래처와 연결하고 부서·직무·급여 체계 및 입퇴사 날짜를 관리한다. |
| [`hr_job`](hr_job.md) | 급여 직무 | Payroll Job | 0 | 급여 직무와 소속 부서·상위 구조 관련 값·감독 사용자 정보를 관리한다. |
| [`hr_list`](hr_list.md) | 급여 기준 목록 | Payroll List | 0 | 급여 계산 등에 참조할 목록을 유형·부서·직원·급여 체계와 연결하여 정의한다. |
| [`hr_listline`](hr_listline.md) | 급여 기준 목록 행 | Payroll List Line | 0 | 급여 목록 버전의 값 구간과 여러 값 컬럼을 저장한다. 각 컬럼의 의미는 목록 설정에 따라 확인해야 한다. |
| [`hr_listtype`](hr_listtype.md) | 급여 목록 유형 | Payroll List Type | 0 | 급여 기준 목록의 유형 코드·이름·설명을 관리한다. |
| [`hr_listversion`](hr_listversion.md) | 급여 목록 버전 | Payroll List Version | 0 | 급여 기준 목록의 버전과 유효 기간·기준 목록 연결을 관리한다. |
| [`hr_movement`](hr_movement.md) | 급여 계산 내역 | Payroll Movement | 0 | 급여 실행별 직원·급여 항목의 금액·수량·문자 값 및 계산 규칙과 분석 요소를 저장한다. |
| [`hr_payroll`](hr_payroll.md) | 급여 체계 | Payroll | 0 | 급여 계산·지급 기준 체계를 정의하고 계약·지급 방식·인쇄 서식과 부대 항목을 연결한다. |
| [`hr_payrollconcept`](hr_payrollconcept.md) | 급여 체계별 계산 항목 | Payroll Concept | 0 | 급여 체계에 항목과 규칙을 연결하고 계산 순서·포함·표시·인쇄 여부를 지정한다. |
| [`hr_period`](hr_period.md) | 급여 기간 | Payroll Period | 0 | 급여 체계별 기간의 시작·종료일·회계일·상태를 관리하고 회계 기간 및 급여 연도와 연결한다. |
| [`hr_process`](hr_process.md) | 급여 계산 실행 | Payroll Process | 0 | 급여 체계·기간·직원 또는 부서별 급여 처리 전표를 관리한다. 문서 상태·회계 전기·지급 대상 선정 연결을 포함한다. |
| [`hr_year`](hr_year.md) | 급여 연도 | Payroll Year | 0 | 급여 체계별 연간 기준을 회계 연도와 연결하고 시작일·기준 일수·수량을 관리한다. |
