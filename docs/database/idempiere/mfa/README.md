# mfa — 다중 인증

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 4개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`mfa_method`](mfa_method.md) | 다중 인증 방식 | MFA Method | 2 | 다중 요소 인증에 사용하는 인증 방식을 정의한다. |
| [`mfa_registereddevice`](mfa_registereddevice.md) | 다중 인증 등록 기기 | MFA Registered Device | 0 | 다중 요소 인증을 위해 등록한 기기를 관리한다. |
| [`mfa_registration`](mfa_registration.md) | 다중 인증 등록 | MFA Registration | 0 | 다중 요소 인증의 등록 정보를 관리한다. |
| [`mfa_rule`](mfa_rule.md) | 다중 인증 규칙 | MFA Rule | 2 | 다중 요소 인증에 적용할 규칙을 정의한다. |
