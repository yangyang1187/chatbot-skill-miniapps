"""色图 = Pixiv 随机图（v2，2026-09 起替代旧 safebooru/jitsu/dmoe 多源）
- 带关键词：lolicon tag 搜索（r18=1）
- 无关键词：lolicon 随机 r18
- 复用 data/pixiv图.py 的 fetch_random 逻辑（同一 lolicon 源）
"""
import importlib.util
import os
import sys

from _multisource import emit, try_sources


def _load_pixiv():
    """动态加载 pixiv图.py，复用其 fetch_random 逻辑。"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pixiv图.py")
    spec = importlib.util.spec_from_file_location("pixiv_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    raw = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else ""
    pixiv = _load_pixiv()

    # 提取关键词：去掉色图/随机 等命令词，剩下的当标签
    tag = None
    for kw in ["色图", "随机", "random", "r18", "随"]:
        raw = raw.replace(kw, "")
    tag = raw.strip() if raw.strip() else None

    # R-18 优先，失败回退普通
    emit(try_sources([
        lambda: pixiv.fetch_random(1, tag),
        lambda: pixiv.fetch_random(0, tag),
        lambda: pixiv.fetch_random(1, None),
    ]))
