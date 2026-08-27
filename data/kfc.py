"""kfc 疯狂星期四文案（多源）：ahfi → qqsuu → 本地语料"""
import random

from _multisource import try_sources, fetch_json, fetch_text, emit

LOCAL_KFC = [
    "今天疯狂星期四，谁请我吃？",
    "今天是疯狂星期四，我看到你朋友圈发的旅游照片了，很漂亮，我这边建议你直接V我50，我帮你去现场看。",
    "疯狂星期四，转发这条消息给你的朋友，你就会失去这个朋友。",
    "听说今天是疯狂星期四，我掐指一算，你五行缺我，命里缺50。",
    "今天是疯狂星期四，别问我为什么知道，因为肯德基已经给我发了请柬。",
    "疯狂星期四到了，我看了看我的钱包，又看了看我的胃，最后决定：去你那里吃。",
    "世情薄，人情恶，雨送黄昏花易落。今天是疯狂星期四，V我50，抚慰我脆弱的心。",
    "我本是显赫世家的公子，却被诡计多端的奸人所害！家人弃我！师门逐我！甚至断我灵脉！重生一世，今天肯德基疯狂星期四！谁请我吃？",
]


def src_ahfi():
    text = fetch_text("https://api.ahfi.cn/api/kfcv50")
    if text and "疯狂" in text:
        return text


def src_qqsuu():
    data = fetch_json("https://api.qqsuu.cn/api/dm-kfc")
    if data.get("code") == 200:
        return data["data"].get("content")


def src_local():
    return random.choice(LOCAL_KFC)


if __name__ == "__main__":
    emit(try_sources([src_ahfi, src_qqsuu, src_local]))
