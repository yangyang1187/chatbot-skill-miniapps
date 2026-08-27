import requests


def get_random_sexy_text():
    # 原 vvhan 骚话接口已失效，改用一言 API 随机句子
    url = "https://v1.hitokoto.cn/?encode=text"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"请求失败: {e}"


def main():
    print(get_random_sexy_text())


if __name__ == "__main__":
    main()
