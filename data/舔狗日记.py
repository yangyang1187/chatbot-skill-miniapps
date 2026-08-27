import requests


def get_dog_diary():
    # 原 vvhan 舔狗日记接口已失效，改用 60s API 的段子接口
    url = "https://60s-api.viki.moe/v2/duanzi"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get("code") == 200:
            return data["data"].get("duanzi", "今天没有日记~")
        return "获取舔狗日记失败"
    except Exception as e:
        return f"请求失败: {e}"


if __name__ == "__main__":
    print(get_dog_diary())
