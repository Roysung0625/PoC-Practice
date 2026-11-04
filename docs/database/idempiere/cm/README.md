# cm — 웹 콘텐츠 관리

[시작 안내](../README.md) · [전체 테이블 일람](../TABLE_INDEX.md) · [업무별 찾기](../BUSINESS_GUIDE.md)

물리명 접두사 기준으로 묶은 38개 테이블입니다. 같은 업무가 여러 접두사에 걸칠 수 있으며, 폴더 이름만으로 거래 종류를 판정하지 않습니다.

| 물리명 | 한국어 논리명(해석) | 원본 논리명 | 행 수 | 의미·쓰임 개요 |
|---|---|---|---:|---|
| [`cm_accesscontainer`](cm_accesscontainer.md) | 웹 콘텐츠 접근 연결 | Web Access Container | 0 | 웹 접근 프로필과 공개 콘텐츠 컨테이너를 연결한다. |
| [`cm_accesslistbpgroup`](cm_accesslistbpgroup.md) | 웹 접근 거래처 그룹 | Web Access BP Group | 0 | 웹 접근 프로필에 거래처 그룹을 연결한다. |
| [`cm_accesslistrole`](cm_accesslistrole.md) | 웹 접근 역할 | Web Access Role | 0 | 웹 접근 프로필에 애플리케이션 역할을 연결한다. |
| [`cm_accessmedia`](cm_accessmedia.md) | 웹 미디어 접근 연결 | Web Access Media | 0 | 웹 접근 프로필과 미디어 항목을 연결한다. |
| [`cm_accessnewschannel`](cm_accessnewschannel.md) | 뉴스 채널 접근 연결 | Web Access NewsChannel | 0 | 웹 접근 프로필과 뉴스 채널을 연결한다. |
| [`cm_accessprofile`](cm_accessprofile.md) | 웹 접근 프로필 | Web Access Profile | 0 | 웹 콘텐츠 접근 제어를 위한 프로필을 정의한다. |
| [`cm_accessstage`](cm_accessstage.md) | 준비 콘텐츠 접근 연결 | Web Access Stage | 0 | 웹 접근 프로필과 게시 준비 단계의 콘텐츠 컨테이너를 연결한다. |
| [`cm_ad`](cm_ad.md) | 웹 광고 | Advertisement | 0 | 배너·제휴 정보·후원 링크 등 웹에 표시할 광고를 관리한다. |
| [`cm_ad_cat`](cm_ad_cat.md) | 웹 광고 분류 | Advertisement Category | 0 | 광고 블록과 순환 표시 대상을 묶는 광고 분류를 정의한다. |
| [`cm_broadcastserver`](cm_broadcastserver.md) | 웹 배포 서버 | Broadcast Server | 0 | 웹 콘텐츠 방송·배포에 사용하는 서버를 관리한다. |
| [`cm_chat`](cm_chat.md) | 레코드 대화 | Chat | 0 | 대상 테이블과 레코드에 연결되는 대화 공간의 유형·공개 범위·검토 방식을 관리한다. |
| [`cm_chatentry`](cm_chatentry.md) | 대화 메시지 | Chat Entry | 0 | 대화 공간의 본문·작성 사용자·제목·검토 상태와 상위 메시지 관계를 저장한다. |
| [`cm_chattype`](cm_chattype.md) | 대화 유형 | Chat Type | 0 | 대화를 연결할 테이블과 검토 방식을 포함한 대화 유형을 정의한다. |
| [`cm_chattypeupdate`](cm_chattypeupdate.md) | 대화 유형별 사용자 연결 | Chat Type Update | 0 | 대화 유형과 사용자의 업데이트 관련 연결 및 셀프서비스 여부를 관리한다. 실제 알림 동작은 처리 코드 확인이 필요하다. |
| [`cm_chatupdate`](cm_chatupdate.md) | 대화별 사용자 연결 | Chat Update | 0 | 개별 대화와 사용자의 업데이트 관련 연결 및 셀프서비스 여부를 관리한다. 알림 방식은 구조만으로 단정하지 않는다. |
| [`cm_container`](cm_container.md) | 웹 콘텐츠 컨테이너 | Web Container | 5 | 이미지·텍스트 등의 웹 콘텐츠를 담는 단위로 표시·색인·저장 방식을 정의한다. |
| [`cm_container_element`](cm_container_element.md) | 웹 콘텐츠 요소 | Container Element | 6 | 제목·본문·꼬리말처럼 컨테이너를 구성하는 작은 콘텐츠 단위를 저장한다. |
| [`cm_container_element_trl`](cm_container_element_trl.md) | 웹 콘텐츠 요소 번역 | Container Element Trl | 6 | 컨테이너의 제목·본문 등 개별 콘텐츠 요소 번역을 저장한다. |
| [`cm_container_trl`](cm_container_trl.md) | 웹 콘텐츠 번역 | Web Container Trl | 5 | 웹 콘텐츠 컨테이너의 번역 내용을 저장한다. |
| [`cm_container_url`](cm_container_url.md) | 콘텐츠 사용 URL | Container URL | 0 | 콘텐츠에서 사용하는 URL을 기록하여 접근 가능 여부 등의 점검에 활용한다. |
| [`cm_containerttable`](cm_containerttable.md) | 콘텐츠 템플릿 테이블 연결 | Container T.Table | 0 | 웹 콘텐츠 컨테이너와 템플릿 테이블 사이의 연결을 관리한다. |
| [`cm_cstage`](cm_cstage.md) | 게시 준비 콘텐츠 | Web Container Stage | 5 | 게시 준비 단계의 이미지·텍스트 등을 담는 컨테이너를 관리한다. |
| [`cm_cstage_element`](cm_cstage_element.md) | 게시 준비 콘텐츠 요소 | Container Stage Element | 7 | 게시 준비 컨테이너의 제목·본문·꼬리말 등 개별 요소를 관리한다. |
| [`cm_cstage_element_trl`](cm_cstage_element_trl.md) | 게시 준비 요소 번역 | Container Stage Element Trl | 7 | 게시 준비 단계의 개별 콘텐츠 요소 번역을 저장한다. |
| [`cm_cstage_trl`](cm_cstage_trl.md) | 게시 준비 콘텐츠 번역 | Web Container Stage Trl | 5 | 게시 준비 컨테이너의 언어별 콘텐츠를 저장한다. |
| [`cm_cstagettable`](cm_cstagettable.md) | 게시 준비 템플릿 테이블 연결 | Stage T.Table | 0 | 게시 준비 컨테이너와 템플릿 테이블의 연결을 관리한다. |
| [`cm_media`](cm_media.md) | 웹 미디어 | Media Item | 3 | 이미지·동영상 등 웹 콘텐츠에서 사용하는 미디어 항목을 관리한다. |
| [`cm_media_server`](cm_media_server.md) | 미디어 서버 | Media Server | 1 | 미디어 전송 대상 서버 목록을 관리하며 정적 서버에 미디어를 배치하는 구성에 사용한다. |
| [`cm_mediadeploy`](cm_mediadeploy.md) | 미디어 배포 이력 | Media Deploy | 0 | 미디어 콘텐츠의 배포 로그를 저장한다. |
| [`cm_newschannel`](cm_newschannel.md) | RSS 뉴스 채널 | News Channel | 0 | RSS 피드에 사용할 콘텐츠 범위를 정의하는 뉴스 채널을 관리한다. |
| [`cm_newsitem`](cm_newsitem.md) | 뉴스 기사 항목 | News Item / Article | 0 | 뉴스나 기사의 기본 내용을 관리하며 상세 기사로 안내하는 요약 콘텐츠로 사용할 수 있다. |
| [`cm_template`](cm_template.md) | 웹 콘텐츠 템플릿 | Template | 4 | 콘텐츠 표시를 위한 레이아웃과 처리 스크립트 등의 템플릿을 정의한다. |
| [`cm_template_ad_cat`](cm_template_ad_cat.md) | 템플릿 광고 분류 연결 | Template Advertising Category | 0 | 웹 템플릿과 광고 분류의 대응 관계를 관리한다. |
| [`cm_templatetable`](cm_templatetable.md) | 템플릿 테이블 연결 | Template Table | 0 | 콘텐츠 관리 템플릿의 테이블 연결을 관리한다. |
| [`cm_webaccesslog`](cm_webaccesslog.md) | 웹 접근 로그 | Web Access Log | 0 | 웹 프로젝트의 요청 URL·접속 주소·사용자 에이전트·응답 코드·크기 등 접근 이력을 저장한다. |
| [`cm_webproject`](cm_webproject.md) | 웹 콘텐츠 프로젝트 | Web Project | 1 | 콘텐츠 컨테이너·URL·광고·미디어 등을 포괄하는 웹 콘텐츠 관리 프로젝트를 정의한다. |
| [`cm_webproject_domain`](cm_webproject_domain.md) | 웹 프로젝트 도메인 | WebProject Domain | 1 | 웹 프로젝트의 도메인 처리와 전달 관계를 정의한다. |
| [`cm_wikitoken`](cm_wikitoken.md) | 위키 토큰 | Wiki Token | 0 | 위키 토큰의 유형과 매크로 또는 대상 테이블·조회절·조건절을 정의한다. 실제 치환·렌더링 동작은 처리 코드 확인이 필요하다. |
