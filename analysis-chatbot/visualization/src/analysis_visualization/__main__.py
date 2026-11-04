"""Single JSON stdout protocol. No source rows are logged."""

import argparse
import json
import os
import sys
from pathlib import Path

from .renderer import ChartError, render


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ChartError("invalid_arguments", "--input 및 --output-dir 인수를 확인하세요.")


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ChartError("invalid_json", "중복 JSON 키를 허용하지 않습니다.")
        result[key] = value
    return result


def _constant(_):
    raise ChartError("invalid_json", "비유한 JSON 숫자를 허용하지 않습니다.")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        parser = Parser(description="검증된 조회 결과의 독립 PNG 가시화")
        parser.add_argument("--input", required=True, type=Path)
        parser.add_argument("--output-dir", required=True, type=Path)
        args = parser.parse_args(argv)
        if args.input.stat().st_size > 2 * 1024 * 1024:
            raise ChartError("input_too_large", "입력 파일은 최대 2MiB입니다.")
        raw = args.input.read_bytes()
        if len(raw) > 2 * 1024 * 1024:
            raise ChartError("input_too_large", "입력 파일은 최대 2MiB입니다.")
        payload = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_object, parse_constant=_constant)
        # Matplotlib cache stays in host-selected task output, not a home directory.
        os.environ["MPLCONFIGDIR"] = str(args.output_dir.resolve() / ".mpl-cache")
        result = render(payload, args.output_dir)
        code = 0
    except ChartError as error:
        result = {"status": "failed", "error": {"code": error.code, "message": str(error)}}
        code = 2
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError):
        result = {"status": "failed", "error": {"code": "invalid_json", "message": "올바른 UTF-8 JSON 입력이 필요합니다."}}
        code = 2
    except OSError:
        result = {"status": "failed", "error": {"code": "io_error", "message": "호스트 입력 또는 출력 파일에 접근할 수 없습니다."}}
        code = 3
    except Exception:
        result = {"status": "failed", "error": {"code": "render_failed", "message": "차트 렌더링에 실패했습니다."}}
        code = 3
    if code:
        print(result["error"]["code"], file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False, allow_nan=False, separators=(",", ":")))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
