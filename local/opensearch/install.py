"""공식 Windows 배포판 설치. 생성 파일은 모두 .local 아래에 둔다."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".local/opensearch"
VERSION = "3.9.0"


def install():
    STATE.mkdir(parents=True, exist_ok=True)
    downloads = ROOT / ".local/downloads/opensearch"
    downloads.mkdir(parents=True, exist_ok=True)
    manifest_path = STATE / "installation.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for component, folder in (("opensearch", "os"), ("opensearch-dashboards", "osd")):
        target = ROOT / ".local" / folder
        marker = target / ".poc-install.json"
        name = f"{component}-{VERSION}-windows-x64.zip"
        url = f"https://artifacts.opensearch.org/releases/bundle/{component}/{VERSION}/{name}"
        archive = downloads / name
        if target.exists() and not marker.exists():
            raise RuntimeError(f"소유권이 확인되지 않은 설치 폴더: {target}")
        if marker.exists():
            owner = json.loads(marker.read_text())
            if owner != {"project": str(ROOT), "component": component, "version": VERSION}:
                raise RuntimeError("기존 설치 버전 또는 소유권이 다릅니다.")
        if not archive.exists():
            print(f"다운로드: {url}", flush=True)
            partial = archive.with_suffix(".partial")
            with urllib.request.urlopen(url, timeout=120) as src, partial.open("wb") as dst:
                total = 0
                next_report = 100 * 1024 * 1024
                while chunk := src.read(1024 * 1024):
                    dst.write(chunk)
                    total += len(chunk)
                    if total >= next_report:
                        print(f"{component}: {total // 1024 // 1024} MiB", flush=True)
                        next_report += 100 * 1024 * 1024
            with zipfile.ZipFile(partial) as z:
                if not any(n.endswith(f"bin/{component}.bat") for n in z.namelist()):
                    raise RuntimeError("올바른 Windows 배포판이 아닙니다.")
            partial.replace(archive)
        with archive.open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest()
        previous = manifest.get(component)
        if previous and previous["sha256"] != digest:
            raise RuntimeError("이전에 기록한 설치 파일 SHA-256과 다릅니다.")
        if not (target / ".extracted").exists():
            target.mkdir(parents=True, exist_ok=True)
            marker.write_text(json.dumps({"project": str(ROOT), "component": component, "version": VERSION}))
            print(f"압축 해제: {target}", flush=True)
            subprocess.run(["tar.exe", "-xf", str(archive), "--strip-components", "1", "-C", str(target)], check=True)
            (target / ".extracted").write_text(digest)
        manifest[component] = {"version": VERSION, "url": url, "sha256": digest, "directory": str(target),
                               "hash_note": "HTTPS 공식 배포 파일의 로컬 SHA-256; 서명 검증을 의미하지 않음"}
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    os_home = ROOT / ".local/os"
    osd_home = ROOT / ".local/osd"
    env = {**os.environ, "OPENSEARCH_JAVA_HOME": str(os_home / "jdk"), "OSD_NODE_HOME": str(osd_home / "node")}
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    if not (os_home / "plugins/analysis-kuromoji/plugin-descriptor.properties").exists():
        subprocess.run([str(os_home / "bin/opensearch-plugin.bat"), "install", "--batch", "analysis-kuromoji"],
                       cwd=os_home, env=env, check=True, creationflags=flags)
    if (osd_home / "plugins/securityDashboards").exists():
        subprocess.run([str(osd_home / "bin/opensearch-dashboards-plugin.bat"), "remove", "securityDashboards"],
                       cwd=osd_home, env=env, check=True, creationflags=flags)
    for directory in ("data", "logs", "dashboards-data"):
        (STATE / directory).mkdir(exist_ok=True)
    os_settings = {
        "cluster.name": "poc-local-search", "node.name": "poc-local-node",
        "network.host": "127.0.0.1", "http.port": 9200, "transport.port": 9300,
        "discovery.type": "single-node", "plugins.security.disabled": True,
        "path.data": (STATE / "data").as_posix(), "path.logs": (STATE / "logs").as_posix(),
    }
    osd_settings = {
        "server.name": "poc-search-dashboards", "server.host": "127.0.0.1", "server.port": 5601,
        "opensearch.hosts": ["http://127.0.0.1:9200"], "path.data": (STATE / "dashboards-data").as_posix(),
    }
    for path, settings in ((os_home / "config/opensearch.yml", os_settings),
                           (osd_home / "config/opensearch_dashboards.yml", osd_settings)):
        path.write_text("\n".join(f"{k}: {json.dumps(v)}" for k, v in settings.items()) + "\n", encoding="utf-8")
    options = os_home / "config/jvm.options"
    lines = options.read_text().splitlines()
    options.write_text("\n".join("-Xms1g" if s.startswith("-Xms") else "-Xmx1g" if s.startswith("-Xmx") else s for s in lines) + "\n")
    print("설치 완료. Start.ps1로 시작하세요.", flush=True)


if __name__ == "__main__":
    install()
