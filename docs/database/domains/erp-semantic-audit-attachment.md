# 변경 기록·첨부·보관 — 근거 기반 분류안·공식 분류 아님

[전체 일람](../index.md)

분류 근거: 원본 사전 Name/Description + 주요 열/물리 FK 교차대조(문서 overlay 자동 규칙). 물리적 연결과 업무 의미의 확정은 구분합니다.

문서 첨부/보관·변경 전후 값·시스템 접근 기록의 참조를 탐색합니다.

관계 흐름 근거(실제 물리 FK의 자식 → 부모; 실행 시간 순서 아님):

- `ad_attachmentfile.(ad_attachment_id)` → `ad_attachment.(ad_attachment_id)` (`adattachment_adattachmentfile`).
- `ad_attachmentnote.(ad_attachment_id)` → `ad_attachment.(ad_attachment_id)` (`adattachment_note`).

[항목별 사전·열·FK 근거](../classification-evidence.md). 기존 canonical 폴더·설명은 표의 별도 열로 남깁니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| poc_idempiere | adempiere | ad_archive | 문서 보관 (사전: Archive) | ad: 애플리케이션 사전·화면·권한·시스템 (기존 분류안) | 변경 기록·첨부·보관 | 보관 대상 문서의 정보를 관리한다. | [문서](../idempiere/ad/ad_archive.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Archive'; Description='Document Archive'; 주요 열 ad_table_id, record_id, binarydata; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-ad_archive) | <!-- table-id: poc_idempiere.adempiere.ad_archive -->
| poc_idempiere | adempiere | ad_attachment | 첨부 문서 (사전: Attachment) | ad: 애플리케이션 사전·화면·권한·시스템 (기존 분류안) | 변경 기록·첨부·보관 | 문서에 연결된 첨부 정보를 관리한다. | [문서](../idempiere/ad/ad_attachment.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Attachment'; Description='Attachment for the document'; 주요 열 ad_table_id, record_id, binarydata; FK adattachment_adattachmentfile, adattachment_note; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-ad_attachment) | <!-- table-id: poc_idempiere.adempiere.ad_attachment -->
| poc_idempiere | adempiere | ad_attachmentfile | 첨부 파일 메타데이터 (사전: Attachment File) | ad: 애플리케이션 사전·화면·권한·시스템 (기존 분류안) | 변경 기록·첨부·보관 | 첨부 파일의 이름·크기·형식·경로·체크섬과 순서를 기록한다. | [문서](../idempiere/ad/ad_attachmentfile.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Attachment File'; 주요 열 ad_attachment_id, filename; FK adattachment_adattachmentfile; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-ad_attachmentfile) | <!-- table-id: poc_idempiere.adempiere.ad_attachmentfile -->
| poc_idempiere | adempiere | ad_attachmentnote | 첨부 개인 메모 (사전: Attachment Note) | ad: 애플리케이션 사전·화면·권한·시스템 (기존 분류안) | 변경 기록·첨부·보관 | 첨부 문서에 대한 개인 메모를 관리한다. | [문서](../idempiere/ad/ad_attachmentnote.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Attachment Note'; Description='Personal Attachment Note'; 주요 열 ad_attachment_id; FK adattachment_note; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-ad_attachmentnote) | <!-- table-id: poc_idempiere.adempiere.ad_attachmentnote -->
| poc_idempiere | adempiere | ad_changelog | 데이터 변경 로그 (사전: Change Log) | ad: 애플리케이션 사전·화면·권한·시스템 (기존 분류안) | 변경 기록·첨부·보관 | 데이터 변경 내역을 기록한다. | [문서](../idempiere/ad/ad_changelog.md) | 물리 구조 현재 일치 / 공식 사전 해석 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='Change Log'; Description='Log of data changes'; 주요 열 ad_table_id, record_id, oldvalue, newvalue; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-ad_changelog) | <!-- table-id: poc_idempiere.adempiere.ad_changelog -->
| poc_idempiere | adempiere | ad_sequence_audit | 문서 채번 이력 (사전: AD_Sequence_Audit) | ad: 애플리케이션 사전·화면·권한·시스템 (기존 분류안) | 변경 기록·첨부·보관 | 채번 규칙으로 생성한 문서 번호와 대상 테이블 레코드를 기록한다. | [문서](../idempiere/ad/ad_sequence_audit.md) | 물리 구조 현재 일치 / 구조 추론 / 근거 기반 분류안(공식 분류 아님) / 사전 Name='AD_Sequence_Audit'; 주요 열 ad_table_id, record_id; FK 합치하는 참조 근거 없음; 사전 의미와 열/FK가 변경 기록·첨부·보관를 함께 가리켜 제안. [상세 근거](../classification-evidence.md#t-ad_sequence_audit) | <!-- table-id: poc_idempiere.adempiere.ad_sequence_audit -->
