import json
import subprocess
import shutil
import tempfile
import uuid
from pathlib import Path

from poc.config import ROOT


def test_start_status_stop_from_another_directory_preserves_unrelated_process():
    scripts = ROOT / "local/scripts"
    assert (scripts / "Start.ps1").exists(), "어느 작업 폴더에서든 실행할 수 있는 시작 스크립트가 필요합니다."
    shell = shutil.which("pwsh") or shutil.which("powershell")
    instance = "ops-test-" + uuid.uuid4().hex[:8]
    def run(name):
        # 백그라운드 자식이 Windows 파이프 핸들을 상속해 EOF를 지연시키지 않도록 파일로 캡처한다.
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as output, tempfile.TemporaryFile(mode="w+", encoding="utf-8") as errors:
            args = [shell, "-NoProfile", "-File", str(scripts / name), "-Instance", instance]
            if name == 'Start.ps1':
                args.extend(['-ApiPort', '18001', '-WebPort', '18000'])
            reply = subprocess.run(args, cwd=ROOT.parent, stdout=output, stderr=errors, timeout=45)
            errors.seek(0); output.seek(0)
            assert reply.returncode == 0, errors.read()
            return output.read()
    outsider = subprocess.Popen([shell, "-NoProfile", "-Command", "Start-Sleep -Seconds 180"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        run("Start.ps1")
        run("Start.ps1")
        state = json.loads(run("Status.ps1"))
        assert state["api"]["running"] is True
        assert state["web"]["running"] is True
        run("Stop.ps1")
        state = json.loads(run("Status.ps1"))
        assert state["api"]["running"] is False
        assert state["web"]["running"] is False
        assert outsider.poll() is None
    finally:
        if (scripts / "Stop.ps1").exists():
            run("Stop.ps1")
        outsider.terminate()
        outsider.wait(timeout=10)
