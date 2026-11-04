# s — 자원·시간·비용·교육

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 10개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`s_expensetype`](s_expensetype.md) | 경비 유형 | Expense Type | 1 | 경비 보고에 사용하는 경비 유형을 정의한다. |
| [`s_resource`](s_resource.md) | 업무 자원 | Resource | 11 | 업무에 배정하는 자원의 기본 정보를 정의한다. |
| [`s_resourceassignment`](s_resourceassignment.md) | 자원 배정 | Resource Assignment | 2 | 자원에 대한 업무 배정 정보를 저장한다. |
| [`s_resourcetype`](s_resourcetype.md) | 자원 유형 | Resource Type | 3 | 자원 유형별 시간대·요일·단위와 단일 배정 여부 등을 정의한다. |
| [`s_resourceunavailable`](s_resourceunavailable.md) | 자원 사용 불가 기간 | Resource Unavailability | 2 | 자원을 사용할 수 없는 시작·종료일과 사유를 저장한다. |
| [`s_timeexpense`](s_timeexpense.md) | 작업 시간·경비 보고 | Expense Report | 1 | 투입 시간과 경비를 보고하는 문서의 기본 정보를 저장한다. |
| [`s_timeexpenseline`](s_timeexpenseline.md) | 작업 시간·경비 보고행 | Expense Line | 4 | 시간·경비 보고서의 개별 내역을 저장한다. |
| [`s_timetype`](s_timetype.md) | 기록 시간 유형 | Time Type | 0 | 기록한 시간을 구분하는 유형을 정의한다. |
| [`s_training`](s_training.md) | 교육 과정 | Training | 1 | 반복 운영하는 교육 과정의 기본 정의를 저장한다. |
| [`s_training_class`](s_training_class.md) | 교육 개설 회차 | Training Class | 0 | 교육 과정이 실제로 개설된 개별 회차를 저장한다. |
