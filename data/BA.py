"""BA logo 生成（单源 + 友好提示）：oiapi 是唯一图源"""
import sys

import requests


def generate_logo(start_text="Blue", end_text="Archive"):
    url = "https://oiapi.net/API/BlueArchive"
    params = {"startText": start_text, "x": -18, "y": 0, "color": "white"}
    if end_text:
        params["endText"] = end_text
    # oiapi 直接返回图片（302 重定向），校验响应类型
    resp = requests.get(url, params=params, timeout=15, allow_redirects=True)
    resp.raise_for_status()
    if "image" in resp.headers.get("Content-Type", ""):
        return resp.url
    return None


if __name__ == "__main__":
    start_text, end_text = "Blue", "Archive"
    if len(sys.argv) > 1 and sys.argv[1].strip():
        parts = sys.argv[1].split(" ", 1)
        start_text = parts[0]
        end_text = parts[1] if len(parts) > 1 else ""

    try:
        url = generate_logo(start_text, end_text)
    except Exception:
        url = None

    if url:
        print(f"![Blue Archive Logo]({url})")
    else:
        print("BA logo 生成失败（图源暂不可用）~请稍后再试")
        sys.exit(1)
