# OpenSearch 실습 검증 기록

검증일: 2026-11-03, Windows 11 x64 / PowerShell 7 / PostgreSQL 18 / OpenSearch·Dashboards 3.9.0.

[운영 안내](README.md) · [교육 실습](../../docs/learning/opensearch-lab.md) · [전체 구조](../../docs/architecture.md)

## 실제 결과

| 항목 | 결과 |
|---|---|
| 설치 | 공식 Windows ZIP 두 개 다운로드·버전·로컬 SHA-256 기록, 포함 JDK 사용. 공식 서명 검증은 수행하지 않음 |
| DB | 기존 상품 55개 보존 + 신규 상품 200개, 프로모션 200개 |
| 연결 데이터 | 그룹 200개, 상세 200개, 그룹별 상품 연결 600개. 프로모션별 상품 1~5개 |
| 보존 | 기존 5개 대상 테이블의 비배치 행과 재사용한 부모 7개 테이블의 선택 행 개수·해시 일치 |
| 무결성 | 대상 5개 테이블의 실제 FK 21개 검사, 신규 배치 고아 참조 0건 |
| 계정 | 앱 조회 계정의 읽기 전용 트랜잭션 및 INSERT 권한 없음 확인 |
| 색인 | `poc-product`, `poc-promotion` 각각 `_count=200`; 서로 다른 인덱스·entity_type |
| 원본 일치 | 상품 원본 73열·프로모션 원본 13열 전체와 문서 `_source` 일치 |
| 관계 일치 | 독립 SQL JOIN의 600개 연결과 양쪽 색인의 nested 연결 집합 일치 |
| 일본어 검색 | `ジョウロ` 상품 5개, `園芸工具` 프로모션 40개. 원본 기대 ID 집합 일치 |
| nested 조건 | 양방향 ID 검색 통과, 서로 다른 배열 객체의 ID·이름을 섞은 조건은 0건 |
| 재실행 | 전체 Load 명령 반복 성공, `action=reused`, DB 및 색인 수량 불변 |
| FK 실패 | 별도 트랜잭션에 정상·잘못된 FK 행을 함께 삽입, 오류 발생 후 둘 다 롤백 확인 |
| Bulk 실패 | 정상 문서와 잘못된 숫자 타입 문서를 함께 전송해 `[200,400]` 확인, 같은 원본 ID로 복구 성공 |
| 재시작 | `Stop.ps1 → Start.ps1 → Verify.ps1` 실제 종료 코드 0. 문서·저장 조회 유지 |
| 수신 주소 | 9200·9300·5601 모두 `127.0.0.1`; 다른 인터페이스 수신 없음 |
| 프로세스 설정 | 단일 노드, JVM 1GiB, kuromoji 플러그인 확인 |
| 브라우저 | 무로그인으로 Product·Promotion 각각 200개 표시. DQL 일본어 검색 5개/40개 확인 |
| DB 사전 | 최신 DB 읽기 전용 수집, 정본 테이블 문서 912개·18,818열 기본값·3,807 FK·20,873 상대 링크 검증 통과 |

## 검증 과정에서 수정한 문제

첫 전체 적재는 Dashboards 최초 시작이 끝나기 전에 관리 화면 API를 호출해 실패했다. DB·색인 단계는 완료돼 있었으며 같은 배치를 재실행해 중복 없이 복구했다. 현재 `load`는 Dashboards 상태를 먼저 확인한다.

첫 브라우저 검사에서는 저장된 index pattern에 필드 메타데이터가 없어 열이 Unknown field로 표시됐다. 실제 필드 목록을 Dashboards API로 조회해 함께 저장하도록 수정했고, 이후 브라우저의 열 타입·일본어 검색과 검증 명령이 통과했다. 최초 실행부터 모든 검증이 통과한 결과로 해석하지 않는다.

## 재현과 증거

```powershell
.\local\opensearch\Load.ps1
.\local\opensearch\Load.ps1
.\local\opensearch\Verify.ps1 -Faults
.\local\opensearch\Stop.ps1
.\local\opensearch\Start.ps1
.\local\opensearch\Verify.ps1
```

Git 제외 `.local/opensearch/`에 `installation.json`, `baseline.json`, `seed-manifest.json`, `last-load.json`, `verification-faults.json`, `verification.json`, `listeners.json`, `product-screen.png`, `promotion-screen.png`가 있다. 재시작 직후 검증의 UTC 시각은 `2026-11-03T14:30:42.715362+00:00`이다. 로컬 SHA-256은 다운로드의 재현·변경 탐지용이며 공식 배포 서명 검증과 구분한다.

외부 AWS·Bedrock 호출, 벡터/하이브리드 검색, 챗봇 연결, 할인 계산 엔진, 대량 부하 시험, Windows 재부팅 후 무인 자동 복구는 이번 검증 범위에 포함하지 않았다. DB의 가격·재고·할인 금액 실적으로 이 가상 데이터의 이름·설명을 해석하지 않는다.
