"""塔罗牌（多源）：oiapi → 本地 22 张大阿卡纳语料"""
import random

from _multisource import try_sources, fetch_json, emit

# 22 张大阿卡纳：名称、含义池
MAJOR_ARCANA = [
    ("愚者", ["新的开始", "冒险", "自由", "保持初心"]),
    ("魔术师", ["创造力", "行动力", "掌握资源", "意志坚定"]),
    ("女祭司", ["直觉", "神秘", "内在智慧", "静观其变"]),
    ("女皇", ["丰饶", "关怀", "感性", "收获"]),
    ("皇帝", ["权威", "秩序", "稳定", "领导力"]),
    ("教皇", ["传统", "指引", "学习", "贵人相助"]),
    ("恋人", ["选择", "和谐", "感情", "价值观"]),
    ("战车", ["前进", "意志", "胜利", "掌控方向"]),
    ("力量", ["勇气", "耐心", "内在力量", "以柔克刚"]),
    ("隐士", ["内省", "寻求答案", "独处", "智慧"]),
    ("命运之轮", ["转机", "机遇", "顺势而为", "变化"]),
    ("正义", ["公正", "平衡", "因果", "理性判断"]),
    ("倒吊人", ["换位思考", "牺牲", "等待时机", "换个角度"]),
    ("死神", ["结束与新生", "转变", "放下过去", "重生"]),
    ("节制", ["调和", "耐心", "适度", "循序渐进"]),
    ("恶魔", ["诱惑", "束缚", "直面欲望", "挣脱执念"]),
    ("高塔", ["突变", "打破旧局", "觉醒", "置之死地而后生"]),
    ("星星", ["希望", "疗愈", "灵感", "光明前景"]),
    ("月亮", ["不安", "潜意识", "迷雾", "看清真相"]),
    ("太阳", ["成功", "活力", "喜悦", "万事顺遂"]),
    ("审判", ["觉醒", "反思", "重新出发", "好消息"]),
    ("世界", ["圆满", "达成", "旅程完成", "功德圆满"]),
]

ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]


def src_oiapi():
    data = fetch_json("https://oiapi.net/API/Tarot", {"type": "today"})
    if not (data and data.get("code") == 1):
        return None
    parts = []
    for card in data["data"]:
        pos = card.get("type", "")
        meaning = card.get(pos, "")
        parts.append(f"{card.get('name_cn', '')} | {card.get('name_en', '')}\n{pos}：{meaning}")
        if card.get("pic"):
            parts.append(f"![Tarot]({card['pic']})")
    return "\n\n".join(parts)


def src_local():
    cards = random.sample(range(22), 4)
    parts = []
    for idx in cards:
        name, meanings = MAJOR_ARCANA[idx]
        pos = random.choice(["正位", "逆位"])
        meaning = random.choice(meanings)
        parts.append(f"{name} {ROMAN[idx]}（{pos}）\n{meaning}")
    return "今日塔罗（本地牌库）：\n\n" + "\n\n".join(parts)


if __name__ == "__main__":
    emit(try_sources([src_oiapi, src_local]))
