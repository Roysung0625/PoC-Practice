"""Download CPython 3.13 ARM64 wheels and write reproducible Linux ZIP archives."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / ".local/aws-deploy"


def cached_dependencies():
    """Reuse only our hash-verified prior ARM64 package when the SDK version matches."""
    package, manifest = DEST / "agent.zip", DEST / "packages.json"
    if not package.exists() or not manifest.exists():
        return None
    value = json.loads(manifest.read_text(encoding="utf-8"))
    digest = hashlib.sha256(package.read_bytes()).hexdigest()
    if value.get("AgentKey") != f"runtime/{digest}/agent.zip" or value.get("platform") != "manylinux2014_aarch64":
        return None
    with zipfile.ZipFile(package) as source:
        if "boto3-1.43.111.dist-info/METADATA" not in source.namelist():
            return None
        return {name: source.read(name) for name in source.namelist() if name not in ("main.py", "contract.py")}


def package_cached(dependencies):
    for name in ("main.py", "contract.py"):
        dependencies[name] = (ROOT / "aws/runtime" / name).read_bytes()
    path = DEST / "agent.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as output:
        for name, data in sorted(dependencies.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 12, 0, 0, 0))
            info.create_system, info.external_attr, info.compress_type = 3, 0o100644 << 16, zipfile.ZIP_DEFLATED
            output.writestr(info, data)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archive(path, files):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as output:
        for source, name in sorted(files, key=lambda pair: pair[1]):
            info = zipfile.ZipInfo(name, (2026, 10, 12, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            output.writestr(info, source.read_bytes())
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    dependencies = cached_dependencies()
    if dependencies is not None:
        agent_hash = package_cached(dependencies)
    else:
        with tempfile.TemporaryDirectory(prefix="arm64-", dir=DEST) as directory:
            target = Path(directory)
            subprocess.run([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--no-compile",
                "--platform", "manylinux2014_aarch64", "--python-version", "3.13", "--implementation", "cp",
                "--only-binary=:all:", "--target", str(target), "boto3==1.43.111"], check=True)
            for name in ("main.py", "contract.py"):
                shutil.copy2(ROOT / "aws/runtime" / name, target / name)
            agent_hash = archive(DEST / "agent.zip", [(p, p.relative_to(target).as_posix()) for p in target.rglob("*") if p.is_file()])
    lambda_hash = archive(DEST / "sql-tool.zip", [(ROOT / "aws/runtime" / name, name) for name in ("sql_tool.py", "contract.py")])
    manifest = {"AgentKey": f"runtime/{agent_hash}/agent.zip", "LambdaKey": f"runtime/{lambda_hash}/sql-tool.zip", "python": "3.13", "platform": "manylinux2014_aarch64"}
    (DEST / "packages.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest))


if __name__ == "__main__":
    main()
