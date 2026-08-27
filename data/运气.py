import random
import sys

# 运势本地生成（无外部依赖）：签文 + 运势短语，均内置语料
SIGNS = [
    ("上上签·紫气东来", "今日诸事皆宜，贵人相助，放手去做。"),
    ("上签·风生水起", "机遇就在眼前，大胆行动会有意外收获。"),
    ("上签·否极泰来", "困扰已久的事今天会有转机。"),
    ("中签·稳中有进", "按部就班即是进步，不宜冒进。"),
    ("中签·静水流深", "表面平静，暗中积累，适合学习沉淀。"),
    ("中签·以退为进", "今日宜退不宜进，休息也是生产力。"),
    ("下签·韬光养晦", "少说话多做事，避免口舌是非。"),
    ("下签·守拙待时", "时机未到，保存实力，明天会更好。"),
]

LUCKY = [
    "幸运色：{}\n幸运数字：{}\n贵人星座：{}",
]
COLORS = ["红色", "橙色", "黄色", "绿色", "青色", "蓝色", "紫色", "白色", "金色", "粉色"]
CONSTELLATIONS = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
                  "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]


def draw():
    sign, desc = random.choice(SIGNS)
    color = random.choice(COLORS)
    num = random.randint(1, 99)
    friend = random.choice(CONSTELLATIONS)
    return f"今日签文：{sign}\n签语：{desc}\n幸运色：{color}\n幸运数字：{num}\n贵人星座：{friend}"


if __name__ == "__main__":
    constellation = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else None
    result = draw()
    if constellation:
        result = f"【{constellation}】今日运势：\n" + result
    print(result)
