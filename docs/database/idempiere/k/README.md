# k — 지식·분류·문서

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 13개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`k_category`](k_category.md) | 지식 분류 | Knowledge Category | 1 | 지식 항목을 분류하는 범주를 정의한다. |
| [`k_categoryvalue`](k_categoryvalue.md) | 지식 분류값 | Category Value | 0 | 지식 분류에 속하는 선택 가능한 값을 정의한다. |
| [`k_comment`](k_comment.md) | 지식 항목 의견 | Entry Comment | 0 | 지식 항목에 대한 의견이나 주석을 저장한다. |
| [`k_entry`](k_entry.md) | 지식 항목 | Entry | 0 | 지식 관리의 개별 콘텐츠 항목을 저장한다. |
| [`k_entrycategory`](k_entrycategory.md) | 지식 항목 분류 연결 | K_EntryCategory | 0 | 지식 항목을 분류 및 해당 분류값과 연결한다. |
| [`k_entryrelated`](k_entryrelated.md) | 관련 지식 항목 | Related Entry | 0 | 하나의 지식 항목과 연관된 다른 항목의 관계를 저장한다. |
| [`k_index`](k_index.md) | 검색 색인 | Index | 0 | 키워드·발췌문과 원본 테이블·레코드 식별자를 연결하는 검색 색인 정보를 저장한다. |
| [`k_indexlog`](k_indexlog.md) | 색인 검색 로그 | Index Log | 0 | 색인 검색의 질의와 결과 및 질의 출처를 기록한다. |
| [`k_indexstop`](k_indexstop.md) | 색인 제외 단어 | Index Stop | 0 | 색인에서 제외할 키워드와 문서 유형·웹 프로젝트·요청 유형 등의 적용 범위를 저장한다. |
| [`k_source`](k_source.md) | 지식 출처 | Knowledge Source | 1 | 지식 항목이 유래한 정보 출처를 정의한다. |
| [`k_synonym`](k_synonym.md) | 지식 검색 동의어 | Knowledge Synonym | 0 | 지식 검색에 사용하는 키워드의 동의어를 정의한다. |
| [`k_topic`](k_topic.md) | 지식 주제 | Knowledge Topic | 1 | 지식 콘텐츠를 구분하는 주제를 정의한다. |
| [`k_type`](k_type.md) | 지식 유형 | Knowledge Type | 2 | 지식 항목의 유형을 정의한다. |
