#!/usr/bin/env bash
# 通用调用入口：任何 Agent / 客户端都以这个脚本调用小程序
# 用法: runner.sh <命令名> [参数...]
# 自动定位仓库路径与可用解释器（优先项目内 .venv）
set -e

REPO=""
for base in "${XIAOCX_HOME:-}" "$HOME/chatbot-skill-miniapps" \
            "$HOME/Documents/workspace/chatbot-skill-miniapps"; do
  if [ -n "$base" ] && [ -f "$base/tools/run_miniapp.py" ]; then
    REPO="$base"
    break
  fi
done
if [ -z "$REPO" ]; then
  echo '{"ok": false, "error": "未找到 chatbot-skill-miniapps 仓库，请先运行 install.sh 或设置 XIAOCX_HOME"}'
  exit 2
fi

PY="python3"
if [ -x "$REPO/.venv/bin/python" ]; then
  PY="$REPO/.venv/bin/python"
elif ! python3 -c "import requests, httpx" 2>/dev/null; then
  echo '{"ok": false, "error": "python3 缺少 requests/httpx 且无 .venv，请重新运行 install.sh"}'
  exit 2
fi

exec "$PY" "$REPO/tools/run_miniapp.py" "$REPO" "$@"
