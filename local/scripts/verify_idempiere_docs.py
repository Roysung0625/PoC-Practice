"""생성기와 독립적으로 테이블 문서의 완전성·FK·링크를 검사한다."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs/database/idempiere"
SNAPSHOT = ROOT / ".local/datasets/idempiere/documentation-snapshot.json"


def verify():
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    manifest = json.loads((OUTPUT / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["snapshot_sha256"] == hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest(), "스냅샷 해시"
    names = {t["physical_name"] for t in snapshot["tables"]}
    tables = {t["physical_name"]: t for t in snapshot["tables"]}
    assert len(names) == len(snapshot["tables"]), "물리명 중복"
    assert set(manifest["table_paths"]) == names, "manifest 테이블 집합"
    table_files = {p.stem: p for p in OUTPUT.glob("*/*.md") if p.name != "README.md"}
    assert len(table_files) == len(list(p for p in OUTPUT.glob("*/*.md") if p.name != "README.md")), "파일 물리명 중복"
    assert set(table_files) == names, "테이블 문서 누락 또는 초과"
    columns = defaultdict(list)
    for c in snapshot["columns"]:
        columns[c["table_name"]].append(c)
    fks = [c for c in snapshot["constraints"] if c["kind"] == "f"]
    expected = {f"{c['source_schema']}.{c['source_table']}.{c['name']}": c for c in fks}
    assert len(expected) == len(fks), "FK 식별자 중복"
    actual = {"OUT": Counter(), "IN": Counter()}
    edge_set = {(c["source_table"], tuple(c["source_columns"]), c["target_table"], tuple(c["target_columns"])) for c in fks}
    column_count = 0
    all_index = (OUTPUT / "TABLE_INDEX.md").read_text(encoding="utf-8")
    index_names = re.findall(r"^\| \[`([a-z0-9_]+)`\]\(", all_index, re.M)
    assert Counter(index_names) == Counter(names), "전체 일람 중복·누락"
    for name, path in sorted(table_files.items()):
        text = path.read_text(encoding="utf-8")
        assert path.relative_to(OUTPUT).as_posix() == manifest["table_paths"][name], f"경로 {name}"
        assert f"| 물리명 | `adempiere.{name}` |" in text, f"물리명 {name}"
        assert f"| 전체 테넌트 행 수 | {tables[name]['row_count']:,} |" in text, f"행 수 {name}"
        assert snapshot["captured_at"] in text, f"확인시점 {name}"
        assert "## 의미와 쓰임" in text and "설명 근거:" in text, f"개요 {name}"
        entries = re.findall(r"^\| (\d+) \| `([a-z0-9_]+)` \|.*$", text, re.M)
        assert entries == [(str(c["position"]),c["physical_name"]) for c in columns[name]], f"열 순서 {name}"
        column_rows = re.findall(r"^\| \d+ \| `[^`]+` \|.*$", text, re.M)
        for line, column in zip(column_rows, columns[name]):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if "column_default" in column:
                expected_default = column["column_default"] or "—"
                actual_default = html.unescape(parts[6]).replace("<br>", "\n")
                assert actual_default == expected_default.replace("\r", ""), f"기본값 {name}.{column['physical_name']}"
        for index in snapshot.get("unique_indexes", []):
            if index["table_name"] == name:
                assert index["definition"] in text, f"고유 인덱스 {index['index_name']}"
        column_count += len(entries)
        group_index = (path.parent / "README.md").read_text(encoding="utf-8")
        assert len(re.findall(rf"^\| \[`{re.escape(name)}`\]\(",group_index,re.M)) == 1, f"폴더 색인 {name}"
        for row in text.splitlines():
            marker = re.search(r"<!-- FK_(OUT|IN): ([^\n]+?) -->", row)
            if not marker:
                continue
            direction, identity = marker.groups()
            assert identity in expected, f"허위 FK {identity}"
            c = expected[identity]
            assert c["source_table" if direction == "OUT" else "target_table"] == name, f"FK 방향 {identity}"
            parts = [p.strip() for p in row.strip("|").split("|")]
            assert len(parts) == 7, f"FK 표 형식 {identity}"
            assert re.sub(r"<!--.*?-->", "", parts[0]).strip() == f"`{c['name']}`", f"제약 이름 {identity}"
            assert re.search(rf"\[`{re.escape(c['source_table'])}`\]", parts[1]), f"자식 {identity}"
            assert re.findall(r"`([^`]+)`",parts[2]) == c["source_columns"], f"자식 열/순서 {identity}"
            assert re.search(rf"\[`{re.escape(c['target_table'])}`\]", parts[3]), f"부모 {identity}"
            assert re.findall(r"`([^`]+)`",parts[4]) == c["target_columns"], f"부모 열/순서 {identity}"
            actions = {"a":"NO ACTION","r":"RESTRICT","c":"CASCADE","n":"SET NULL","d":"SET DEFAULT"}
            assert parts[5] == f"{actions[c['on_delete']]} / {actions[c['on_update']]}", f"참조 동작 {identity}"
            actual[direction][identity] += 1
        for diagram in re.findall(r"```mermaid\n(.*?)\n```",text,re.S):
            nodes = dict(re.findall(r'\b(n\d+)\["([a-z0-9_]+)"\]',diagram))
            for src,label,dst in re.findall(r'(n\d+) -->\|"([^"]+)"\| (n\d+)',diagram):
                source_columns,target_columns = label.split(" → ")
                edge = (nodes[src],tuple(source_columns.split(", ")),nodes[dst],tuple(target_columns.split(", ")))
                assert edge in edge_set, f"요약 그림 FK {name}: {edge}"
    assert column_count == len(snapshot["columns"]), "열 총수"
    assert actual["OUT"] == Counter(expected.keys()), "나가는 FK 누락·중복"
    assert actual["IN"] == Counter(expected.keys()), "들어오는 FK 누락·중복"
    # 업무 안내의 별도 편집 그림도 실제 선언된 FK인지 확인한다.
    guide = (OUTPUT / "BUSINESS_GUIDE.md").read_text(encoding="utf-8")
    for src,col,dst in re.findall(r"^    ([a-z0-9_]+) -->\|([a-z0-9_]+)\| ([a-z0-9_]+)$",guide,re.M):
        assert any(c['source_table']==src and c['source_columns']==[col] and c['target_table']==dst for c in fks), f"업무 그림 FK {src}.{col} -> {dst}"
    for relative, expected_hash in manifest["files"].items():
        assert hashlib.sha256((OUTPUT / relative).read_bytes()).hexdigest() == expected_hash, f"생성 파일 해시 {relative}"
    for relative, expected_hash in manifest["overview_sources"].items():
        assert hashlib.sha256((ROOT / 'local/schema_docs' / relative).read_bytes()).hexdigest() == expected_hash, f"개요 원본 해시 {relative}"
    markdown_files = list(OUTPUT.rglob("*.md"))
    assert {p.relative_to(OUTPUT).as_posix() for p in markdown_files} - {"VERIFICATION.md"} == set(manifest['files']), "이전 생성 파일 잔존 또는 파일 누락"
    links_checked = 0
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        assert "password=" not in text and "POC_INTERNAL_TOKEN=" not in text, f"연결 비밀 패턴 {path.name}"
        for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
            if urlparse(target).scheme or target.startswith("#"):
                continue
            destination = (path.parent / unquote(target.split("#")[0])).resolve()
            if destination == OUTPUT / "VERIFICATION.md":
                continue  # 이 실행이 성공한 후 아래에서 생성한다.
            assert destination.is_relative_to(ROOT), f"저장소 밖 링크 {path.name}"
            assert destination.is_file(), f"깨진 링크 {path.relative_to(OUTPUT)} -> {target}"
            links_checked += 1
    results = {"tables": len(names), "columns": column_count, "foreign_keys":len(fks),
               "outgoing_entries":sum(actual['OUT'].values()), "incoming_entries":sum(actual['IN'].values()),
               "self_referencing_foreign_keys":sum(c['source_table']==c['target_table'] for c in fks),
               "composite_foreign_keys":sum(len(c['source_columns'])>1 for c in fks),
               "relative_links_checked":links_checked, "generated_markdown_files":len(manifest['files']),
               "groups":len({p.parent for p in table_files.values()}), "status":"PASS"}
    report = f"""# 테이블 문서 검증 기록

[시작 안내](README.md) · [전체 일람](TABLE_INDEX.md)

검증 시점: {datetime.now(timezone(timedelta(hours=9))).isoformat(timespec='seconds')}. DB 스냅샷 수집: {snapshot['captured_at']}.

`local/scripts/verify_idempiere_docs.py`는 생성기의 렌더링 함수를 사용하지 않고 실제 문서·DB 스냅샷·manifest를 직접 대조했습니다.

| 항목 | 결과 |
|---|---:|
| 물리 테이블과 개별 문서 집합 | {len(names)}개 일치, 누락·중복 0 |
| 폴더 분류 | {results['groups']}개 |
| 열 이름·순서 | {column_count:,}개 일치 |
| 물리 FK | {len(fks):,}개 |
| 나가는 / 들어오는 FK 문서 항목 | {results['outgoing_entries']:,} / {results['incoming_entries']:,}개 일치 |
| 자기참조 / 복합 FK | {results['self_referencing_foreign_keys']} / {results['composite_foreign_keys']}개 보존 |
| 상대 링크 | {links_checked:,}개 대상 존재 |
| 테이블·업무 요약 그림 | 모든 표시 FK가 DB 스냅샷에 존재 |
| 전체·폴더 색인 / 파일 해시 | 일치 |
| 연결 문자열·내부 토큰 할당 패턴 | 검출 0 |

이번 검증은 문서의 구조·완전성·링크 검사입니다. 한국어 설명은 원본 사전·구조를 바탕으로 작성하고 불확실성을 표시했지만, 전체 ERP 업무 로직의 실행 검증이나 모든 번역의 도메인 전문가 승인을 뜻하지 않습니다. 실제 업무 데이터 행은 문서에 포함하지 않았습니다. AWS 호출·앱 재시작·Agent 문서 자동 로딩은 수행하지 않았습니다.
"""
    (OUTPUT / "VERIFICATION.md").write_text(report,encoding="utf-8",newline="\n")
    print(json.dumps(results,ensure_ascii=False))


if __name__ == "__main__":
    try:
        verify()
    except AssertionError as exc:
        print(f"검증 실패: {exc}",file=sys.stderr)
        raise SystemExit(1)
