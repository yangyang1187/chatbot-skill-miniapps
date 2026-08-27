import httpx
import asyncio
import json
import random
import sys

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


async def fetch_by_tag(keyword):
    """safebooru 标签搜索（支持关键词）。"""
    tag = TAG_MAP.get(keyword, keyword.replace(" ", "_").lower())
    url = "https://safebooru.org/index.php"
    params = {"page": "dapi", "s": "post", "q": "index", "json": 1, "limit": 10, "tags": tag}
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            data = data.get("post", [])
        if data:
            item = random.choice(data)
            return item.get("sample_url") or item.get("file_url"), tag
    return None, tag


async def fetch_random():
    """无关键词时从 jitsu.top 随机取图。"""
    params = {"type": "json", "num": 1}
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        response = await client.get("https://moe.jitsu.top/img/", params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("code") == 200:
            pics = data.get("pics", [])
            if pics:
                return pics[0]
    return None


async def main():
    keyword = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else None
    if keyword:
        image_url, tag = await fetch_by_tag(keyword)
        if image_url:
            print(f"![{tag}]({image_url})")
        else:
            print(f"没找到「{keyword}」相关的图~换个关键词试试（支持中文角色名/英文标签）")
    else:
        image_url = await fetch_random()
        if image_url:
            print(f"![Anime Image]({image_url})")
        else:
            print("没找到图片~再试试吧")


if __name__ == "__main__":
    asyncio.run(main())
