"""舔狗日记（多源）：60s API → qqsuu"""
from _multisource import try_sources, fetch_json, emit


def src_60s():
    data = fetch_json("https://60s-api.viki.moe/v2/duanzi")
    if data.get("code") == 200:
        return data["data"].get("duanzi")


def src_qqsuu():
    data = fetch_json("https://api.qqsuu.cn/api/dm-tiangou")
    if data.get("code") == 200:
        return data["data"].get("content")


if __name__ == "__main__":
    emit(try_sources([src_60s, src_qqsuu]))
