import httpx
import sys
import asyncio

async def fetch_color_image(keyword: str = None, num: int = 1, r18: int = 0, size: str = "regular"):
    api_url = "https://image.anosu.top/pixiv/json"  # 图片API地址
    params = {
        "keyword": keyword,
        "num": 1,
        "r18":  "0",
        "size": "regular",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        return data  # 返回请求的完整数据

async def is_url_valid(url: str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.head(url)
            return response.status_code == 200
        except httpx.RequestError:
            return False

async def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else None  
    attempt = 0
    max_attempts = 5

    while attempt < max_attempts:
        images = await fetch_color_image(keyword)  # 调用获取色图的函数
        if isinstance(images, list) and images:
            image_url = images[0]["url"]  # 获取第一个图片链接

            # 核对URL是否有效
            if await is_url_valid(image_url):
                markdown_image_link = f"![Anime Image]({image_url})"  # 转换为 Markdown 格式
                print(markdown_image_link, end='')  # 打印 Markdown 图片链接
                return  # 成功获取有效链接，退出

        attempt += 1

    print("某站服务器卡了，或者没有这个关键词标签，重新试一下吧~")  # 提示用户

if __name__ == "__main__":
    asyncio.run(main())  # 运行主函数
