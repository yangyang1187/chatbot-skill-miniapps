"""轮盘赌（qqBot 移植，纯本地无依赖，支持跨调用续局）
左轮 6 弹仓 1 颗子弹。开局随机定子弹弹仓，之后「继续」在同一把枪上依次推进，
直到命中或 6 枪全空。状态持久化到临时文件，跨会话可续。
"""
import json
import os
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

STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".roulette_state.json")


def load_state():
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_state(s):
    try:
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False)
    except Exception:
        pass


def clear_state():
    try:
        os.remove(STATE_PATH)
    except Exception:
        pass


def shot(state):
    """扣一枪：state = {bullet, fired}，fired 为已开枪数，返回本枪结果文本或 None(未结束)。"""
    bullet = state["bullet"]
    fired = state["fired"] + 1
    state["fired"] = fired

    lines = [f"\n第 {fired} 枪：{random.choice(TAUNTS)}……"]
    if fired == bullet:
        lines.append(f"\n💀 {random.choice(DEAD_LINES).format(n=fired)}")
        if fired > 1:
            lines.append(f"生存 {fired - 1} 枪，虽败犹荣。")
        clear_state()
        return "\n".join(lines)
    if fired >= 6:
        clear_state()
        lines.append("\n" + random.choice(WIN_LINES).format(n=6))
        return "\n".join(lines)
    lines.append("咔——空枪！")
    save_state(state)
    lines.append("\n👉 回复「轮盘赌 继续」接着扣扳机，或就此收手认怂。")
    return "\n".join(lines)


def play(mode=None):
    if mode and "继续" in mode:
        state = load_state()
        if not state:
            return "🎰 没有进行中的对局。先回复「轮盘赌」开一把。"
        return shot(state)

    # 开局：随机定子弹弹仓
    state = {"bullet": random.randint(1, 6), "fired": 0}
    return "🎰 轮盘赌开始：6 个弹仓，1 颗子弹。" + shot(state)


if __name__ == "__main__":
    mode = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else None
    print(play(mode))
