#!/usr/bin/env python3
"""Hardened runner for XiaocxPlugin mini-apps.

Security rules (mirror the fork's main.py):
- command name whitelist: word chars / CJK / dot / hyphen / middle dot only
- resolved script path must stay inside <repo>/data
- subprocess with sys.executable, no shell, argv-style args (no injection)
- timeout, structured JSON output

Usage:
  python3 run_miniapp.py <repo_path> <command> [args...]
Output: JSON {"ok": bool, "command": str, "text": str, "images": [urls], "error": str}
"""
import json
import os
import re
import subprocess
import sys

TIMEOUT_SECONDS = 60
SAFE_COMMAND_NAME = re.compile(r'^[\w·][\w·\-.]*$', re.UNICODE)
IMAGE_PATTERN = re.compile(r'!\[.*?\]\((https?://\S+)\)')


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"ok": False, "error": "usage: run_miniapp.py <repo_path> <command> [args...]"}, ensure_ascii=False))
        return 2

    repo = os.path.realpath(sys.argv[1])
    command = sys.argv[2]
    args = " ".join(sys.argv[3:])

    if not command or not SAFE_COMMAND_NAME.match(command):
        print(json.dumps({"ok": False, "command": command, "error": "非法命令名"}, ensure_ascii=False))
        return 2

    data_dir = os.path.join(repo, "data")
    script_path = os.path.realpath(os.path.join(data_dir, f"{command}.py"))

    # 双重保险：解析后的真实路径必须仍在 data 目录内
    if not script_path.startswith(data_dir + os.sep) or not os.path.isfile(script_path):
        print(json.dumps({"ok": False, "command": command, "error": f"小程序不存在: {command}"}, ensure_ascii=False))
        return 2

    try:
        result = subprocess.run(
            [sys.executable, script_path, args],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(json.dumps({"ok": False, "command": command, "error": f"执行超时（>{TIMEOUT_SECONDS}s）"}, ensure_ascii=False))
        return 2

    out = (result.stdout or "").strip()
    if result.returncode != 0:
        err = (result.stderr or "").strip()[-300:]
        print(json.dumps({"ok": False, "command": command, "error": f"执行失败: {err or out}"}, ensure_ascii=False))
        return 2

    images = [m.group(1) for m in IMAGE_PATTERN.finditer(out)]
    text = IMAGE_PATTERN.sub("", out).strip()

    print(json.dumps({"ok": True, "command": command, "text": text, "images": images}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
