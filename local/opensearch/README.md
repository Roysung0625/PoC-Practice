# 로컬 OpenSearch 검색 실습

GardenWorld의 일본어 상품 200건과 프로모션 200건을 Windows 로컬 OpenSearch에 적재하고 OpenSearch Dashboards에서 검색합니다. PostgreSQL이 원본이며 OpenSearch는 이 실습 배치의 검색용 사본입니다. 기존 챗봇의 SQL 승인·AWS 요청 흐름과 별도로 실행합니다.

[교육용 설명과 조회 실습](../../docs/learning/opensearch-lab.md) · [검증 기록](VERIFICATION.md) · [전체 구조](../../doc/architecture.md) · [프로젝트 지속 지침](../../doc/project-guidelines.md) · [DB 전체 안내](../../doc/database/index.md)

## 구성과 접속

| 구성 | 설정 | 역할 |
| --- | --- | --- |
| OpenSearch | Windows ZIP 3.9.0, 단일 노드, JVM 최소·최대 1GiB | 일본어 문서 저장·검색 |
| OpenSearch HTTP | `http://127.0.0.1:9200` | 조회·Bulk API |
| OpenSearch transport | `127.0.0.1:9300` | 노드 내부 통신 |
| OpenSearch Dashboards | Windows ZIP 3.9.0, `http://127.0.0.1:5601` | Discover와 Dev Tools |
| 일본어 분석 | `analysis-kuromoji` 플러그인, `kuromoji` analyzer | 상품명·설명 등의 일본어 분석 |

사용자가 선택한 로컬 실습 설정에 따라 인증을 사용하지 않습니다. 세 포트는 `127.0.0.1`에 바인딩하며, 외부 접속을 위해 주소나 방화벽을 변경하는 작업은 포함하지 않습니다. Dashboards 보안 플러그인은 제거하고 OpenSearch 보안 플러그인은 비활성화합니다.

설치 위치는 `.local/os`, `.local/osd`이며 원본 ZIP은 `.local/downloads/opensearch`에 보관합니다. 시작 스크립트는 OpenSearch에 포함된 JDK와 Dashboards에 포함된 Node 경로를 지정하며 전역 PATH를 변경하지 않습니다. 설치 스크립트가 기록한 SHA-256은 내려받은 파일의 재사용 확인용이며 배포 서명 검증을 뜻하지 않습니다.

## 실행 순서

기존 프로젝트 `.venv`와 iDempiere 환경을 사용합니다. 최초 환경 준비는 [로컬 실행 가이드](../README.md)와 [iDempiere 안내](../IDEMPIERE_GUIDE.md)를 따릅니다. DB 생성이 끝난 뒤 프로젝트 루트의 **PowerShell 7 (`pwsh`)**에서 실행합니다. 중지 스크립트의 프로세스 트리 종료는 PowerShell 7의 .NET API를 사용합니다.

```powershell
# 최초 한 번: 공식 배포 파일 설치와 설정 생성
.\local\opensearch\Install.ps1

# 로컬 OpenSearch와 Dashboards 시작
.\local\opensearch\Start.ps1
.\local\opensearch\Status.ps1

# 일본어 더미 생성 → 검색 인덱스 적재 → 조회 화면 생성
.\local\opensearch\Load.ps1
.\local\opensearch\Verify.ps1
```

`Install.ps1`은 실행 중인 서버의 설정을 바꾸는 명령으로 사용하지 않습니다. 설치를 다시 실행해야 한다면 먼저 `Stop.ps1`로 이 실습 프로세스를 중지합니다. 설치 폴더의 소유권 표식·버전이 다르거나 포트를 다른 프로세스가 사용하면 스크립트가 중단됩니다.

적재가 끝나면 다음 저장 조회를 엽니다.

- [상품 200건](http://127.0.0.1:5601/app/discover#/view/poc-product-view)
- [프로모션 200건](http://127.0.0.1:5601/app/discover#/view/poc-promotion-view)

Discover에서 행을 펼치면 원본 필드와 관련 상품·프로모션 배열을 볼 수 있습니다. 일반 텍스트 검색은 화면 검색창에서, 같은 관계 항목에 여러 조건을 적용하는 `nested` 조회는 [교육 문서](../../docs/learning/opensearch-lab.md)의 Dev Tools 예제로 연습합니다.

작업을 나눠 실행할 수도 있습니다.

```powershell
.\local\opensearch\Load.ps1 -Action seed       # PostgreSQL 더미만 생성/확인
.\local\opensearch\Load.ps1 -Action index      # DB 읽기 → 검색 인덱스 적재
.\local\opensearch\Load.ps1 -Action dashboards # 기존 인덱스의 조회 화면 생성
```

`load`가 기본 동작입니다. 이후 DB를 바꿔도 자동으로 검색 인덱스에 반영되지는 않습니다. 이 스크립트는 승인한 고정 실습 배치를 다루며 일반 데이터 동기화 도구가 아닙니다.

## DB 데이터와 보존 기준

대상은 PostgreSQL `127.0.0.1:5432`의 `poc_idempiere.adempiere`입니다. 기존 상품 55건은 보존하고 다음 배치만 추가합니다. 기존 스키마·제약조건을 사용하며 테이블이나 컬럼을 추가하지 않습니다.

| 테이블 | 신규 행 | 의미 |
| --- | ---: | --- |
| `m_product` | 200 | 일본어 가상 원예 상품 |
| `m_promotion` | 200 | 상품을 묶어 검색하는 가상 프로모션 |
| `m_promotiongroup` | 200 | 프로모션별 대상 상품 그룹 |
| `m_promotionline` | 200 | 프로모션과 그룹의 연결 |
| `m_promotiongroupline` | 600 | 그룹과 상품의 연결, 프로모션별 상품 1~5개 |

상품은 5개 분류의 일본어 이름·설명·용도·변형으로 구성합니다. 판매·재고·할인 실적을 의미하지 않습니다. 클라이언트·조직·사용자·단위·세금 분류·상품 분류·캠페인은 기존 부모 행을 재사용합니다.

`seed_data.py`는 배치 `poc-search-ja-v1`과 고정 UUID로 자신의 행을 식별합니다. 트랜잭션 단위 advisory lock과 `AD_Sequence` 행 잠금으로 ID를 할당하고, 한 DB 트랜잭션 안에서 생성·FK 검사·기존 행 보존 검사를 수행합니다. 재실행은 동일한 배치를 재사용하며 불완전한 배치나 내용 충돌은 오류로 종료합니다.

`baseline.json`은 기존 대상 테이블의 배치 외 행과 사용한 부모 행의 개수·SHA-256만 저장합니다. 재실행 시 기준과 다르면 자동 덮어쓰지 않습니다. 이것은 해당 범위의 보존 확인이며 DB 전체 백업은 아닙니다. 생성 시에는 기존 로컬 관리자 비밀 파일을 사용해 소유 역할로 전환하고, 내보내기는 기존 앱의 읽기 전용 연결을 사용합니다. 앱의 읽기 전용 권한을 확대하지 않습니다.

## 검색 문서 구조

| 인덱스 | 루트 문서 | 원본 필드 | 추가 필드 |
| --- | ---: | --- | --- |
| `poc-product` | 200 | `m_product` 전체 73개 컬럼 | `entity_type`, `seed_batch`, `related_count`, `parent_refs`, `promotions` |
| `poc-promotion` | 200 | `m_promotion` 전체 13개 컬럼 | `entity_type`, `seed_batch`, `related_count`, `parent_refs`, `products` |

원본 PK를 문서 `_id`로 사용합니다. `parent_refs`에는 물리 FK 및 검증한 논리참조의 필드·부모 테이블·ID·이름을 묶고, `promotions` 또는 `products`에는 연결 테이블의 ID·이름 등을 담습니다. 세 관계 배열은 `nested` 매핑입니다. 조회할 때 관계를 다시 SQL로 조인하는 대신 적재 시 함께 만든 사본을 검색합니다. 참조 정보를 저장한다고 OpenSearch가 PostgreSQL FK 제약을 대신 검사하는 것은 아닙니다.

예를 들어 `createdby`·`updatedby`의 사용자 참조와 프로모션의 `ad_client_id`·`ad_org_id`는 DB에 물리 FK가 선언되지 않은 논리참조입니다. `parent_refs`는 `REF_FIELDS`에 지정한 비NULL 참조만 포함하며 각 ID의 부모 존재를 확인합니다. 상품의 물리 FK 16개·프로모션의 물리 FK 1개를 포함한 대상 5테이블의 물리 FK 21개 검사와 이 논리참조 확인을 구분합니다.

매핑은 DB 컬럼 메타데이터로 생성합니다. 정수형 수치는 `long`, 소수형 수치는 `double`, 날짜는 `date`, 지정한 설명·이름 필드는 일본어 `text`, 나머지는 `keyword`로 매핑합니다. 원본 SQL 타입의 정밀도와 JSON 검색 타입은 다를 수 있으므로 정확한 원본 수치는 PostgreSQL에서 확인합니다. 각 인덱스는 샤드 1개·복제본 0개이며 미정의 필드는 `dynamic: strict`로 거부합니다.

기존 인덱스가 있으면 배치 소유권·매핑·문서 ID를 먼저 검사합니다. 다른 소유자의 문서를 자동으로 삭제하지 않습니다. Bulk 항목에 실패가 있으면 오류로 처리하고 `bulk-failures.json`에 결과를 저장합니다. 같은 ID로 다시 적재할 수 있으나 DB seed·색인·Dashboards까지 하나의 통합 트랜잭션은 아니므로 실패 단계부터 상태를 확인해야 합니다.

## 상태·중지·복구

```powershell
.\local\opensearch\Status.ps1
.\local\opensearch\Stop.ps1
.\local\opensearch\Start.ps1
```

`Status.ps1`은 기록한 프로세스의 PID·실행 파일 경로·시작 시각, 로컬 HTTP 응답, 문서 수와 수신 주소를 표시합니다. `Stop.ps1`은 같은 식별 조건을 확인한 실습 프로세스 트리만 종료합니다. 데이터와 인덱스는 남으므로 평소 재시작에 `Load.ps1`을 실행할 필요는 없습니다.

| 증상 | 확인·조치 |
| --- | --- |
| 포트 충돌 | `Status.ps1`과 오류의 포트를 확인하고 기존 프로세스를 식별합니다. 다른 서비스를 임의 종료하지 않습니다. |
| 시작 준비 실패 | `.local/opensearch/logs`의 해당 시각 `out.log`·`err.log`와 OpenSearch 로그를 읽고 `Stop.ps1` 후 복구합니다. |
| PostgreSQL 연결 실패 | PostgreSQL 서비스·5432 수신·기존 앱 설정을 확인합니다. 비밀번호를 명령행이나 로그에 출력하지 않습니다. |
| 기존 행/부모 보존 검사 실패 | 의도한 DB 변경인지 확인합니다. 기준 파일을 삭제하거나 자동 재생성해 검사를 우회하지 않습니다. |
| 매핑·소유권 충돌 | 대상 클러스터·인덱스·배치를 확인합니다. 기존 인덱스를 자동 삭제하지 않습니다. |
| Bulk 실패 | `bulk-failures.json`과 오류를 확인한 뒤 `Load.ps1 -Action index`를 재실행합니다. |
| 조회 화면이 없음 | 인덱스 적재 성공을 확인한 뒤 `Load.ps1 -Action dashboards`를 실행합니다. |

## 생성 파일과 검증 범위

생성 파일은 Git 제외 경로 `.local/opensearch`에 둡니다.

| 위치 | 내용 |
| --- | --- |
| `installation.json` | 설치 버전·공식 다운로드 URL·로컬 ZIP SHA-256 |
| `baseline.json` | 기존 행·선택 부모 행의 개수와 해시 |
| `seed-manifest.json` | 배치 이름·재사용 여부·생성 대상 수·ID |
| `processes.json` | 이 스크립트가 시작한 프로세스 식별 정보 |
| `logs/` | 프로세스 표준 출력·오류·OpenSearch 로그 |
| `data/`, `dashboards-data/` | 검색 서버·Dashboards 데이터 |
| `export/` | 읽어 온 배치 행·완성 문서·매핑 JSON·Bulk NDJSON |
| `last-load.json` | 마지막 명령의 `action`·`started_at`·`status`, 단계별 결과. 성공 시 `completed_at`, 실패 시 `error_type` |
| `verification.json` | 별도 검증을 실행했을 때의 점검 결과 |
| `verification-faults.json` | 의도한 FK/Bulk 실패와 복구를 포함한 점검 결과 |
| `listeners.json` | 검증 실행 때 확인한 세 포트의 실제 수신 주소 |
| `product-screen.png`, `promotion-screen.png` | 실제 브라우저에서 확인한 두 조회 화면 |

```powershell
# DB·검색 문서·독립 SQL JOIN·일본어 검색·nested·저장 조회·수신 주소 검사
.\local\opensearch\Verify.ps1

# 추가 실패 시험: 잘못된 DB FK의 전체 롤백과 Bulk 일부 실패 후 재적재 복구
.\local\opensearch\Verify.ps1 -Faults
```

기본 검증은 원본 행·부모 해시, 앱 읽기 전용 권한, 배치 FK, 전체 `_source`, 독립 SQL JOIN으로 만든 600개 관계, 일본어 검색과 nested 관계 조회, 서로 다른 관계 항목의 조건 혼합 거부, 1GiB JVM·플러그인·루프백 수신·Dashboards 저장 조회를 확인합니다. `-Faults`는 별도 시험 ID로 DB 삽입을 시도해 FK 오류와 롤백을 확인하고, 상품 2문서를 Bulk 적재하면서 한 문서에 잘못된 타입을 넣어 일부 실패를 확인한 뒤 정상 문서로 복구합니다. 기본 검증과 실패 시험의 결과 파일을 구분합니다.

`last-load.json`은 실행 시작부터 기록하며 `status`가 `running`·`failed`이면 전체 성공이 아닙니다. `action: seed`의 `PASS`는 DB 단계만, `action: load`의 `PASS`는 DB·색인·화면 구성까지의 성공을 뜻합니다. 단계별 결과와 `started_at`·`completed_at`을 함께 읽고 DB 결과만으로 색인·화면 성공을 추정하지 않습니다. `verification.json` 또는 `verification-faults.json`은 Python 검사가 끝난 뒤 저장하고, `listeners.json`은 그 이후 PowerShell 포트 검사가 끝난 뒤 저장하므로 **명령 전체 종료 결과와 기록 시점**도 확인합니다. API의 저장 조회 검사와 실제 브라우저 표시·재시작 검사는 별도로 구분합니다.

이 문서는 실행 방법과 검사 기준을 설명하며, 재부팅 후 자동 실행·무인 복구·성능·대량 데이터 품질을 검증했다는 뜻은 아닙니다. 이번 실습은 AWS OpenSearch 배포, 챗봇의 검색 연결, 임베딩·벡터·하이브리드 검색을 포함하지 않습니다.

## 2026-11-03 실제 확인 결과

실패·복구 시험은 `verification-faults.json`의 `verified_at: 2026-11-03T14:26:20.286341+00:00`, 최신 기본 검증은 `verification.json`의 `verified_at: 2026-11-03T14:34:40.294771+00:00` 기록을 기준으로 합니다. 중지·재시작 검증과 실제 브라우저 확인도 별도로 수행했습니다. 최신 `last-load.json`은 `action: load`, `status: PASS`, 배치 `reused`를 기록합니다. 새 실행에서는 최신 파일과 명령 종료 결과를 다시 확인합니다.

| 확인 대상 | 결과 |
| --- | --- |
| DB 전체/실습 배치 | 상품 총 255행, 프로모션 200행. 실습 상품·프로모션 각 200건 |
| 보존·권한 | 기존 대상 행·사용한 부모 해시 일치, 앱 읽기 전용 유지 |
| FK·관계 | 대상 5테이블 물리 FK 21개 검사, 배치의 고아 참조 0건. 독립 SQL JOIN 600관계가 양쪽 인덱스와 일치 |
| 검색 문서 | 각 200문서, 전체 원본 필드·부모·관계 일치 |
| 일본어 검색 | 상품 `ジョウロ` 5건, 프로모션 `園芸工具` 40건, 원본의 기대 ID 집합과 일치 |
| nested | 양방향 관계 조회 통과, 서로 다른 항목의 ID·이름을 섞은 조건은 0건 |
| 실패·복구 | 잘못된 FK 삽입의 트랜잭션 전체 롤백, 의도한 Bulk 응답 `[200, 400]` 확인 후 정상 재적재 복구 |
| 실행·화면 API | 1GiB 힙·kuromoji·루프백 바인딩·저장 조회·필드 타입 확인 통과 |
| 실제 브라우저 | 상품 200건·프로모션 200건 표시, DQL `name: ジョウロ` 5건·`name: 園芸工具` 40건 확인. 두 화면 PNG 보관 |
| 실제 중지·재시작 | `Stop.ps1` → `Start.ps1` → `Verify.ps1` 전체 종료코드 0. 각 200문서와 전체 기본 검사 통과, 세 포트 모두 `127.0.0.1` 수신 |

브라우저 점검 중 발견한 Dashboards의 필드 메타데이터 누락은 `dashboards()`가 실제 인덱스 필드 목록을 조회해 저장하도록 보완했습니다. 최초 화면 구성이 그대로 성공한 결과와 구분하며, 보완 후의 저장 조회 API 검증 결과를 위에 기록했습니다.
