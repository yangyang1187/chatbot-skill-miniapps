"""必应壁纸（多源）：Bing 官方接口(重试) → biturl 镜像"""
import sys

from _multisource import try_sources, fetch_json, emit_image


def src_bing_official(day=0):
    for _ in range(2):  # 偶发超时，重试 2 次
        try:
            data = fetch_json("https://cn.bing.com/HPImageArchive.aspx",
                              {"format": "js", "idx": day, "n": 1, "mkt": "zh-CN"})
            images = data.get("images", [])
            if images:
                return "https://cn.bing.com" + images[0]["urlbase"] + "_1920x1080.jpg"
        except Exception:
            continue
    return None


def src_biturl():
    data = fetch_json("https://bing.biturl.top/",
                      {"resolution": 1920, "format": "json"})
    if data and data.get("data", {}).get("url"):
        return data["data"]["url"]
    return None


if __name__ == "__main__":
    day = 0
    if len(sys.argv) > 1:
        try:
            day = int(sys.argv[1])
        except ValueError:
            pass
    emit_image(try_sources([
        lambda: src_bing_official(day),
        src_biturl,
    ]), "Bing Wallpaper")
