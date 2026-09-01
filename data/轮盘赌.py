"""轮盘赌（qqBot 移植，纯本地无依赖）
左轮 6 弹仓 1 颗子弹，第一枪空仓可继续"扣扳机"或"认输"。
"""
import random
import sys

TAUNTS = [
    "手别抖啊",
    "你行的",
    "深呼吸……",
    "周围一片安静",
    "大家都盯着你的手",
    "枪口还冒着热气吗？",
]

WIN_LINES = [
    "连开{n}枪都安然无恙，你就是天命之人！",
    "{n} 声空响之后，你还站着，了不起。",
    " godlike！{n} 连空枪，今晚彩票买起来。",
]

DEAD_LINES = [
    "砰——第 {n} 枪正中红心，你被抬走了。",
    "咔……砰！第 {n} 枪，游戏结束。",
    "第 {n} 枪，子弹没有留情，一路走好。",
]


def play(continue_after_miss=False):
    bullet = random.randint(1, 6)
    lines = ["🎰 轮盘赌开始：6 个弹仓，1 颗子弹。"]
    for n in range(1, 7):
        lines.append(f"\n第 {n} 枪：{random.choice(TAUNTS)}……")
        if n == bullet:
            lines.append(f"\n💀 {random.choice(DEAD_LINES).format(n=n)}")
            if n > 1:
                lines.append("生存 {n} 枪，虽败犹荣。".format(n=n - 1))
            return "\n".join(lines)
        lines.append("咔——空枪！")
        if not continue_after_miss:
            lines.append("\n👉 回复「轮盘赌 继续」接着扣扳机，或就此收手认怂。")
            return "\n".join(lines)
    lines.append("\n" + random.choice(WIN_LINES).format(n=6))
    return "\n".join(lines)


if __name__ == "__main__":
    mode = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else None
    print(play(continue_after_miss=bool(mode)))
