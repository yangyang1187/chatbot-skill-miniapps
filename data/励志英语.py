"""励志英语（多源）：zenquotes → qqsuu"""
from _multisource import try_sources, fetch_json, emit


def src_zenquotes():
    data = fetch_json("https://zenquotes.io/api/today")
    if data:
        item = data[0]
        return f"英文: {item.get('q', '')}\n作者: {item.get('a', '')}"


def src_qqsuu():
    data = fetch_json("https://api.qqsuu.cn/api/dm-yiyan")
    if data.get("code") == 200:
        d = data.get("data", {})
        return f"英文: {d.get('content', '')}"


if __name__ == "__main__":
    emit(try_sources([src_zenquotes, src_qqsuu]))
