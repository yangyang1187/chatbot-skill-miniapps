import requests
import sys

def get_personal_luck():
    """获取个人运势信息"""
    url = "https://api.52vmy.cn/api/wl/s/draw"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["code"] == 200:
            luck_info = data["data"]
            return f"今日签文：{luck_info['text']}\n"
        else:
            return "获取个人运势失败，请稍后再试。"
    except Exception as e:
        print(f"发生错误: {e}")
        return "获取个人运势信息出错"

def get_horoscope_luck(constellation):
    """获取星座运势信息"""
    url = f"https://api.leafone.cn/api/horoscope?name={constellation}"
    response = requests.get(url)
    response.raise_for_status()  

    data = response.json()
    if data["code"] == 200:
        horoscope_info = data["data"]
        return f"今日{horoscope_info['horoscope']}运势：\n" \
               f"{horoscope_info['shorts']}\n" \
               f"整体运势：{horoscope_info['contentAll']}\n" \
               f"事业运势：{horoscope_info['contentCareer']}\n" \
               f"财富运势：{horoscope_info['contentFortune']}\n" \
               f"爱情运势：{horoscope_info['contentLove']}"
    else:
        return "获取星座运势失败，请稍后再试"

def main():
    if len(sys.argv) > 1:
        constellation = sys.argv[1]
    else:
        constellation = input("请输入星座名称：")

    print("-" * 20 + "个人运势" + "-" * 20)
    print(get_personal_luck())  # 打印个人运势

    print("-" * 20 + "星座运势" + "-" * 20)
    print(get_horoscope_luck(constellation))  # 打印星座运势

if __name__ == "__main__":
    main()

