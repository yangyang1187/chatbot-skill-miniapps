"""色图/二次元角色图（多源）
- 带关键词：safebooru 标签搜索（支持中文角色名映射）→ jitsu 随机兜底
- 无关键词：jitsu 随机 → dmoe 随机兜底
"""
import sys

import httpx

from _multisource import emit_image, try_sources

# 常见中文角色名 → safebooru 标签映射
TAG_MAP = {
    "蒂法": "tifa_lockhart",
    "爱丽丝": "aerith_gainsborough",
    "刻晴": "keqing_(genshin_impact)",
    "甘雨": "ganyu_(genshin_impact)",
    "雷电将军": "raiden_shogun",
    "原神": "genshin_impact",
    "初音": "hatsune_miku",
    "初音未来": "hatsune_miku",
    "明日方舟": "arknights",
    "碧蓝档案": "blue_archive",
    "最终幻想": "final_fantasy",
}

HEADERS = {"User-Agent": "Mozilla/5.0 chatbot-miniapp/1.0"}


def _get(url, params=None, timeout=15):
    with httpx.Client(timeout=timeout, follow_redirects=True, headers=HEADERS) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        return resp


def src_safebooru(keyword):
    tag = TAG_MAP.get(keyword, keyword.replace(" ", "_").lower())
    params = {"page": "dapi", "s": "post", "q": "index", "json": 1,
              "limit": 10, "tags": tag}
    resp = _get("https://safebooru.org/index.php", params)
    data = resp.json()
    if isinstance(data, dict):
        data = data.get("post", [])
    if data:
        import random
        item = random.choice(data)
        return item.get("sample_url") or item.get("file_url")
    return None


def src_jitsu():
    resp = _get("https://moe.jitsu.top/img/", {"type": "json", "num": 1})
    data = resp.json()
    if data.get("code") == 200:
        pics = data.get("pics", [])
        if pics:
            return pics[0]
    return None


def src_dmoe():
    return "https://www.dmoe.cc/random.php"


if __name__ == "__main__":
    keyword = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else None

    if keyword:
        # 关键词搜索：safebooru 优先，找不到图才兜底随机
        emit_image(try_sources([
            lambda: src_safebooru(keyword),
            src_jitsu,
            src_dmoe,
        ]), "Anime Image")
    else:
        emit_image(try_sources([src_jitsu, src_dmoe]), "Anime Image")
