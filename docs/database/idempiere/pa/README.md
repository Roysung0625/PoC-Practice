# pa — 성과·보고서·대시보드

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 30개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`pa_achievement`](pa_achievement.md) | 성과 달성 | Achievement | 0 | 성과 목표에 대한 달성 정보를 기록한다. |
| [`pa_benchmark`](pa_benchmark.md) | 성과 비교 기준 | Benchmark | 0 | 성과를 비교하는 벤치마크 기준을 정의한다. |
| [`pa_benchmarkdata`](pa_benchmarkdata.md) | 성과 비교 기준값 | Benchmark Data | 0 | 성과 벤치마크의 개별 데이터 값을 저장한다. |
| [`pa_colorschema`](pa_colorschema.md) | 성과 색상 기준 | Color Schema | 2 | 성과 표시에서 사용할 색상 체계를 정의한다. |
| [`pa_dashboardcontent`](pa_dashboardcontent.md) | 대시보드 콘텐츠 | Dashboard Content | 12 | 대시보드에 표시할 창·보고서·목표·차트 등의 콘텐츠와 기본 배치를 정의한다. |
| [`pa_dashboardcontent_access`](pa_dashboardcontent_access.md) | 대시보드 콘텐츠 접근 | PA_DashboardContent_Access_ID | 2 | 대시보드 콘텐츠에 접근할 역할 또는 사용자를 연결한다. |
| [`pa_dashboardcontent_trl`](pa_dashboardcontent_trl.md) | 대시보드 콘텐츠 번역 | Dashboard Content Trl | 12 | 대시보드 콘텐츠의 이름·설명·HTML·도움말을 언어별로 저장한다. |
| [`pa_dashboardpreference`](pa_dashboardpreference.md) | 대시보드 개인 설정 | Dashboard Preference | 0 | 역할·사용자별 대시보드 콘텐츠의 위치·표시 여부·접힘 상태를 저장한다. |
| [`pa_documentstatus`](pa_documentstatus.md) | 문서 상태 표시 설정 | Document Status | 16 | 테이블과 조회 조건을 기준으로 표시할 문서 상태 항목 및 연결 화면·표시 서식을 정의한다. |
| [`pa_documentstatus_trl`](pa_documentstatus_trl.md) | 문서 상태 표시 번역 | Document Status Trl | 16 | 문서 상태 표시 항목의 이름·설명·도움말을 언어별로 저장한다. |
| [`pa_documentstatusaccess`](pa_documentstatusaccess.md) | 문서 상태 표시 접근 | Document Status Access | 10 | 문서 상태 표시 항목에 접근할 역할 또는 사용자를 연결한다. |
| [`pa_goal`](pa_goal.md) | 성과 목표 | Goal | 4 | 측정하고 관리할 성과 목표를 정의한다. |
| [`pa_goalrestriction`](pa_goalrestriction.md) | 성과 목표 제한 조건 | Goal Restriction | 0 | 성과 목표의 측정 범위를 제한하는 조건을 정의한다. |
| [`pa_hierarchy`](pa_hierarchy.md) | 보고 계층 | Reporting Hierarchy | 0 | 보고서에 적용할 계층 구조를 정의한다. |
| [`pa_measure`](pa_measure.md) | 성과 측정값 | Measure | 4 | 실제로 측정한 개별 성과 값을 저장한다. |
| [`pa_measurecalc`](pa_measurecalc.md) | 성과 측정 계산식 | Measure Calculation | 6 | 성과를 측정하는 계산 방법을 정의한다. |
| [`pa_ratio`](pa_ratio.md) | 성과 비율 지표 | Ratio | 1 | 성과를 비율로 표현하는 지표를 정의한다. |
| [`pa_ratioelement`](pa_ratioelement.md) | 성과 비율 구성 요소 | Ratio Element | 3 | 성과 비율 지표를 구성하는 요소를 저장한다. |
| [`pa_report`](pa_report.md) | 재무 보고서 | Financial Report | 3 | 재무 보고서의 기본 정의를 저장한다. |
| [`pa_reportcolumn`](pa_reportcolumn.md) | 재무 보고서 열 | Report Column | 17 | 보고서에 표시할 개별 열을 정의한다. |
| [`pa_reportcolumn_trl`](pa_reportcolumn_trl.md) | 재무 보고서 열 번역 | Report Column Trl | 17 | 보고서 열의 언어별 번역 정보를 저장한다. |
| [`pa_reportcolumnset`](pa_reportcolumnset.md) | 재무 보고서 열 집합 | Report Column Set | 3 | 보고서에 사용할 열들의 묶음을 정의한다. |
| [`pa_reportcube`](pa_reportcube.md) | 회계 집계 큐브 | Report Cube | 0 | 선택한 달력의 기간별로 지정 차원에 따라 회계 자료를 사전 집계하는 큐브를 정의한다. |
| [`pa_reportline`](pa_reportline.md) | 재무 보고서 행 | Report Line | 113 | 보고서 행의 표시 순서·상하위 관계·금액 유형과 계산식을 정의한다. |
| [`pa_reportline_trl`](pa_reportline_trl.md) | 재무 보고서 행 번역 | Report Line Trl | 113 | 보고서 행의 이름과 설명을 언어별로 저장한다. |
| [`pa_reportlineset`](pa_reportlineset.md) | 재무 보고서 행 집합 | Report Line Set | 3 | 재무 보고서에 사용할 행 정의들의 묶음을 관리한다. |
| [`pa_reportsource`](pa_reportsource.md) | 재무 보고서 자료 조건 | Report Source | 93 | 보고서 행에 포함할 자료의 범위를 제한하는 조건을 정의한다. |
| [`pa_sla_criteria`](pa_sla_criteria.md) | 서비스 수준 기준 | SLA Criteria | 2 | 서비스 수준 협약(SLA)의 평가 기준을 정의한다. |
| [`pa_sla_goal`](pa_sla_goal.md) | 서비스 수준 목표 | SLA Goal | 1 | 서비스 수준 협약에서 달성할 목표를 정의한다. |
| [`pa_sla_measure`](pa_sla_measure.md) | 서비스 수준 측정값 | SLA Measure | 1 | 서비스 수준 협약에 대한 측정 결과를 저장한다. |
