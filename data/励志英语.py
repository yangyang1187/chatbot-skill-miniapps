import requests


def get_daily_english():
    url = "https://zenquotes.io/api/today"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()[0]
        en_content = data.get("q", "未获取到英文内容")
        author = data.get("a", "")
        return f"英文: {en_content}\n作者: {author}"
    except requests.RequestException as e:
        return f"请求失败: {str(e)}"


if __name__ == "__main__":
    print(get_daily_english())
