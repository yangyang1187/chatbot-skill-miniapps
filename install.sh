#!/usr/bin/env bash
# chatbot-skill-miniapps 一键安装
# 用法: bash install.sh [安装目录]   默认 ~/chatbot-skill-miniapps
set -e

REPO_URL="https://github.com/yangyang1187/chatbot-skill-miniapps.git"
DEST="${1:-$HOME/chatbot-skill-miniapps}"

echo "==> 安装 chatbot-skill-miniapps 到 $DEST"

if [ -d "$DEST/.git" ]; then
  echo "==> 已存在，更新中..."
  git -C "$DEST" pull --ff-only
else
  git clone "$REPO_URL" "$DEST"
fi

# 安装依赖：优先装进系统 python3；遇到 PEP 668 externally-managed 等限制时退回项目内 .venv
if python3 -c "import requests, httpx" 2>/dev/null; then
  echo "==> 依赖已存在，跳过安装"
  PY="python3"
else
  if ! python3 -m pip install -q requests httpx Pillow 2>/dev/null; then
    echo "==> 系统 python3 不允许直接 pip 安装（PEP 668），改用项目内虚拟环境 $DEST/.venv"
    python3 -m venv "$DEST/.venv"
    "$DEST/.venv/bin/pip" install -q requests httpx Pillow
    PY="$DEST/.venv/bin/python"
  else
    PY="python3"
  fi
fi

echo "==> 冒烟测试"
OUT="$($PY "$DEST/tools/run_miniapp.py" "$DEST" --list)"
echo "可用命令: $OUT"
TEST="$($PY "$DEST/tools/run_miniapp.py" "$DEST" 今天吃什么)"
echo "测试输出: $TEST"

# 安装通用 Agent 技能（ZCode / Claude Code 等客户端自动发现 ~/.agents/skills）
SKILL_SRC="$DEST/skills/xiaocx-miniapp"
if [ -d "$SKILL_SRC" ]; then
  mkdir -p "$HOME/.agents/skills"
  rm -rf "$HOME/.agents/skills/xiaocx-miniapp"
  cp -R "$SKILL_SRC" "$HOME/.agents/skills/xiaocx-miniapp"
  echo "==> 已安装 Agent 技能到 ~/.agents/skills/xiaocx-miniapp"
fi

echo ""
echo "✅ 安装完成！"
echo "调用方式（Agent 请这样运行并把 JSON 的 text 发给用户、images 图片发出来）："
echo "  bash $SKILL_SRC/scripts/runner.sh <命令名> [参数]   # 通用入口，自动选解释器"
echo "  命令列表: bash $SKILL_SRC/scripts/runner.sh --list"
echo "  例: bash $SKILL_SRC/scripts/runner.sh 天气 北京"
