# fact — 회계 사실·집계

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 3개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`fact_acct`](fact_acct.md) | 전기 회계 분개 | Accounting Fact | 0 | 업무 문서에서 전기된 회계 분개를 계정·회계 스키마·기간 및 분석 요소별로 저장한다. 거래통화와 회계통화의 차변·대변 금액 및 원 문서 테이블·레코드·행 식별자를 포함한다. |
| [`fact_acct_summary`](fact_acct_summary.md) | 회계 분개 집계 | Accounting Fact summary | 0 | 보고 큐브와 계정·기간·조직 등 분석 요소별 회계통화 차변·대변 금액 및 수량 집계를 저장한다. 원분개와 함께 합산하면 중복될 수 있다. |
| [`fact_reconciliation`](fact_reconciliation.md) | 회계 분개 대사 연결 | Accounting Fact Reconciliation | 0 | 회계 분개에 대사 코드를 연결하여 대응되는 분개를 묶는 데 사용한다. |
