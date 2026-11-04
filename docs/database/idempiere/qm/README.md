# qm — 품질 관리

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 2개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`qm_specification`](qm_specification.md) | 품질 규격 | Quality Specification | 0 | 제품 품질을 판정하는 규격을 정의한다. |
| [`qm_specificationline`](qm_specificationline.md) | 품질 규격 조건행 | QM Specification Line | 0 | 품질 규격에서 검사할 속성·비교 연산·기준값과 유효기간을 정의한다. |
