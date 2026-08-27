import requests
import sys


def get_bing_image_url(day=0):
    """从必应官方接口获取每日壁纸（URL 本身就是图片地址）。"""
    api_url = "https://cn.bing.com/HPImageArchive.aspx"
    params = {"format": "js", "idx": day, "n": 1, "mkt": "zh-CN"}
    for _ in range(3):  # 偶发超时，重试 3 次
        try:
            response = requests.get(api_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            images = data.get("images", [])
            if images:
                return "https://cn.bing.com" + images[0]["urlbase"] + "_1920x1080.jpg"
            return None
        except Exception:
            continue
    return None


def main():
    day = 0
    if len(sys.argv) > 1:
        try:
            day = int(sys.argv[1])
        except ValueError:
            pass
    image_url = get_bing_image_url(day)
    if image_url:
        print(f"![Bing Wallpaper]({image_url})")
    else:
        print("获取Bing壁纸失败")


if __name__ == "__main__":
    main()
