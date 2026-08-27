"""骚话/随机一句话（多源）：hitokoto → 60s 一言"""
from _multisource import try_sources, fetch_text, fetch_json, emit


def src_hitokoto():
    return fetch_text("https://v1.hitokoto.cn/", {"encode": "text"}) or None


def src_60s_yiyan():
    data = fetch_json("https://60s-api.viki.moe/v2/yiyan")
    if data.get("code") == 200:
        return data["data"].get("hitokoto")


if __name__ == "__main__":
    emit(try_sources([src_hitokoto, src_60s_yiyan]))
