"""明日方舟十连寻访模拟（qqBot 移植，纯本地无依赖）
标准池概率：6★ 2%、5★ 8%、4★ 50%、3★ 40%（简化版，不含保底递增）。
"""
import random
import sys

STARS = {
    6: ["维什戴尔", "玛恩纳", "焰影苇草", "浊心斯卡蒂", "耀骑士临光", "棘刺",
        "史尔特尔", "银灰", "艾雅法拉", "能天使", "推进之王", "伊芙利特",
        "陈", "斯卡蒂", "闪灵", "夜莺", "星熊", "塞雷娅", "安洁莉娜",
        "麦哲伦", "莫斯提马", "傀影", "温蒂", "W", "夕", "凯尔希"],
    5: ["德克萨斯", "拉普兰德", "幽灵鲨", "蓝毒", "白金", "灰喉", "普罗旺斯",
        "食铁兽", "狮蝎", "红", "槐琥", "凛冬", "真理", "赫默", "白面鸮",
        "夜魔", "梅尔", "石棉", "暮落", "芙兰卡", "雷蛇", "星极"],
    4: ["讯使", "清道夫", "红豆", "杜宾", "缠丸", "霜叶", "慕斯", "猎蜂",
        "杰克", "流星", "杰西卡", "酸糖", "克洛丝", "安赛尔", "末药", "调香师",
        "苏苏洛", "波登可", "阿消", "暗索", "砾", "深海色", "地灵"],
    3: ["芬", "香草", "翎羽", "玫兰莎", "安德切尔", "克洛丝", "炎熔",
        "史都华德", "梓兰", "安赛尔", "芙蓉", "米格鲁", "卡缇", "黑角",
        "空爆", "泡泡"],
}

RATES = {6: 2, 5: 8, 4: 50, 3: 40}
STAR_ICON = {6: "★★★★★★", 5: "★★★★★", 4: "★★★★", 3: "★★★"}


def roll_one():
    r = random.uniform(0, 100)
    acc = 0
    for star, rate in RATES.items():
        acc += rate
        if r < acc:
            return star
    return 3


def pull(count):
    results = [roll_one() for _ in range(count)]
    lines = []
    for i, star in enumerate(results, 1):
        name = random.choice(STARS[star])
        prefix = " 👉 " if star >= 5 else "    "
        lines.append(f"{i:2d}.{prefix}{STAR_ICON[star]} {name}")
    six, five = results.count(6), results.count(5)
    summary = (f"\n📊 本轮统计：6★×{six} 5★×{five} "
               f"4★×{results.count(4)} 3★×{results.count(3)}")
    if six >= 2:
        summary += " ——欧皇出没，建议买彩票！"
    elif six == 1:
        summary += " ——不错不错，出货了！"
    elif five >= 2:
        summary += " ——小赚，不算血亏。"
    else:
        summary += " ——非酋也要求存啊。"
    return f"🎰 明日方舟{count}连寻访结果：\n" + "\n".join(lines) + summary


if __name__ == "__main__":
    count = 10
    if len(sys.argv) > 1 and sys.argv[1].strip().isdigit():
        count = min(max(int(sys.argv[1].strip()), 1), 60)
    print(pull(count))
