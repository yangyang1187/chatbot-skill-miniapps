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

echo "==> 安装依赖 (requests, httpx)"
python3 -m pip install -q requests httpx || pip3 install -q requests httpx

echo "==> 冒烟测试"
OUT="$(python3 "$DEST/tools/run_miniapp.py" "$DEST" --list)"
echo "可用命令: $OUT"
TEST="$(python3 "$DEST/tools/run_miniapp.py" "$DEST" 今天吃什么)"
echo "测试输出: $TEST"

echo ""
echo "✅ 安装完成！"
echo "调用方式（Agent 请这样运行并把 JSON 的 text 发给用户、images 图片发出来）："
echo "  python3 $DEST/tools/run_miniapp.py $DEST <命令名> [参数]"
echo "  命令列表: python3 $DEST/tools/run_miniapp.py $DEST --list"
echo "  例: python3 $DEST/tools/run_miniapp.py $DEST 天气 北京"
