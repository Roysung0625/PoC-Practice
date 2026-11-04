# gl — 총계정원장·예산·분개

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 14개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`gl_budget`](gl_budget.md) | 총계정원장 예산 | Budget | 1 | 총계정원장 예산의 기준정보를 관리한다. |
| [`gl_budgetcontrol`](gl_budgetcontrol.md) | 예산 통제 | Budget Control | 0 | 회계 스키마와 예산별 통제 범위·약정 유형·승인 전 통제 여부를 정의한다. |
| [`gl_category`](gl_category.md) | 원장 분류 | GL Category | 10 | 총계정원장 문서와 분개를 분류하는 기준을 정의한다. |
| [`gl_category_trl`](gl_category_trl.md) | 원장 분류 번역 | GL Category Trl | 10 | 총계정원장 분류의 언어별 표시 내용을 저장한다. |
| [`gl_distribution`](gl_distribution.md) | 원장 배부 규칙 | GL Distribution | 1 | 총계정원장 금액을 배부하는 상위 규칙을 관리한다. |
| [`gl_distributionline`](gl_distributionline.md) | 원장 배부 명세 | GL Distribution Line | 2 | 총계정원장 배부 규칙의 개별 배부 항목을 관리한다. |
| [`gl_fund`](gl_fund.md) | 원장 자금 통제 | GL Fund | 0 | 회계 스키마별 통제 대상 자금과 금액 및 적용 기간을 정의한다. |
| [`gl_fundrestriction`](gl_fundrestriction.md) | 자금 사용 제한 | Fund Restriction | 0 | 자금 통제 항목에 계정 요소 값을 연결하여 적용 제한 범위를 지정한다. |
| [`gl_journal`](gl_journal.md) | 원장 분개 전표 | Journal | 2 | 총계정원장 분개 전표의 머리글을 관리하며 차변·대변 행은 전표 명세에 저장된다. |
| [`gl_journalbatch`](gl_journalbatch.md) | 원장 분개 배치 | Journal Batch | 1 | 총계정원장 분개 전표를 배치 단위로 묶어 관리한다. |
| [`gl_journalgenerator`](gl_journalgenerator.md) | 원장 분개 생성 규칙 | GL Journal Generator | 2 | 회계 스키마·문서 유형·원장 분류와 차대변 조정 계정 등을 지정하는 분개 생성 규칙이다. |
| [`gl_journalgeneratorline`](gl_journalgeneratorline.md) | 분개 생성 대상 규칙 | Generator Line | 6 | 생성할 차변·대변 계정, 거래처 분석 방식, 금액 배수와 반올림 기준을 정의한다. |
| [`gl_journalgeneratorsource`](gl_journalgeneratorsource.md) | 분개 생성 원천 규칙 | Generator Source | 8 | 분개 생성 행에 사용할 원천 계정·원장 분류와 금액 배수·반올림 기준을 정의한다. |
| [`gl_journalline`](gl_journalline.md) | 원장 분개 전표 명세 | Journal Line | 4 | 총계정원장 분개 전표의 개별 분개 행을 저장한다. |
