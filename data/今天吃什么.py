"""今天吃什么（多源）：aa1 → 本地菜库"""
import random

from _multisource import try_sources, fetch_json, emit

LOCAL_MEALS = [
    "火锅", "麻辣烫", "烧烤", "饺子", "面条", "盖浇饭", "黄焖鸡米饭", "螺蛳粉",
    "兰州拉面", "沙县小吃", "肯德基", "麦当劳", "寿司", "韩式炸鸡", "酸菜鱼",
    "小龙虾", "冒菜", "串串香", "过桥米线", "肉夹馍", "煎饼果子", "炒饭", "披萨",
]


def src_aa1():
    data = fetch_json("https://zj.v.api.aa1.cn/api/eats/")
    if data.get("code") == 200:
        return f"今天吃什么？ {data.get('mealwhat', '')}"


def src_local():
    meal = random.choice(LOCAL_MEALS)
    return f"今天吃什么？ 今天吃{meal}！"


if __name__ == "__main__":
    emit(try_sources([src_aa1, src_local]))
