import httpx
import asyncio
import sys


async def fetch_color_image(keyword=None):
    # 原 image.anosu.top 已失效，改用 moe.jitsu.top（支持 JSON 返回与标签搜索）
    params = {"type": "json", "num": 1}
    if keyword:
        params["keyword"] = keyword
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
    image_url = await fetch_color_image(keyword)
    if image_url:
        print(f"![Anime Image]({image_url})")
    else:
        print("没找到图片~换个标签试试吧")


if __name__ == "__main__":
    asyncio.run(main())
