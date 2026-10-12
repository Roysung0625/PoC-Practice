# 프로젝트 Superpowers 스킬

현재 프로젝트에서 사용하는 Superpowers 스킬 원본과 보조 파일을 `skills/`에 설치했습니다.

- 출처: https://github.com/obra/superpowers
- 버전: 7.0.0
- 고정 커밋: `bb92a77741419a4ab5f06e711a283343f1ada0c3`
- 설치일: 2026-10-12
- 설치 범위: `D:\Projects\PoC-Practice\.agents\skills`의 스킬 15개
- 라이선스: [MIT 원문](SUPERPOWERS-LICENSE.txt)

Codex는 프로젝트의 `.agents/skills`에서 스킬을 탐색합니다. 다음 대화 턴부터 사용할 수 있으며, 목록에 나타나지 않으면 Codex를 다시 시작합니다.

예: `$brainstorming`으로 요구사항을 정리하거나 `$systematic-debugging`으로 문제 원인을 조사할 수 있습니다. 완료 보고 전에는 `$verification-before-completion`을 사용합니다.

사용자의 최신 지시와 프로젝트 `AGENTS.md`가 일반 스킬 지침보다 우선합니다. 실제 AWS 호출, 로컬 실행, 모의 시험의 검증 결과를 구분하는 프로젝트 규칙도 유지합니다.

## 설치 및 관리

`skill-installer`의 `install-skill-from-github.py`에 `--repo obra/superpowers`, 위 고정 커밋을 지정하는 `--ref`, 프로젝트 경로를 지정하는 `--dest .agents/skills`, 각 `skills/<스킬명>`을 지정하는 `--path`를 전달해 설치했습니다. 스킬 폴더 안의 참조 문서와 보조 스크립트를 함께 보존합니다.

현재는 원본을 프로젝트에 직접 복사한 설치이므로 자동 업데이트되지 않습니다. 업데이트할 때는 새 커밋과 변경 내용을 확인하고 설치 정보를 함께 갱신합니다. 프로젝트를 공유할 때 이 폴더도 포함해야 합니다.

이 설치는 스킬 파일 설치입니다. 개별 보조 스크립트 실행에 필요한 Bash 등은 해당 기능을 사용할 때 확인합니다.

공식 탐색 규칙: https://learn.chatgpt.com/docs/build-skills
