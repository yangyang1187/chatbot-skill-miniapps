import random
import sys

# 藏头诗本地生成（无外部依赖）：每行以输入的字开头，接一段诗意短语
PATTERNS = [
    "{}似春风拂柳丝",
    "{}如明月照江心",
    "{}若青山横北郭",
    "{}同流水向东行",
    "{}随白云归远岫",
    "{}伴落花听雨声",
    "{}映星河入梦来",
    "{}藏幽谷自芳菲",
    "{}渡关山千万重",
    "{}染霜林万叶红",
    "{}落窗前灯一盏",
    "{}浮沧海月明珠",
]


def make_acrostic(text):
    chars = [c for c in text if c.strip()][:4] or ["你", "好", "世", "界"]
    lines = []
    for c in chars:
        pattern = random.choice(PATTERNS)
        lines.append(pattern.format(c))
    return "\n".join(lines)


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "你好世界"
    poem = make_acrostic(text)
    print(f"藏头诗（{text[:4]}）：\n{poem}")
