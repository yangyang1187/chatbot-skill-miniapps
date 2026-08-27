import requests
import json

def get_ruo_zhi_ba_article():
    """
    获取若知吧的文章内容。

    Returns:
        str: 若知吧的文章内容，如果请求失败则返回错误信息。
    """
    url = "https://tools.mgtv100.com/external/v1/pear/ruoZhiBa"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        data = response.json()
        
        # 获取文章内容
        if data.get("code") == 200:
            instruction = data.get("data", {}).get("instruction", "未获取到问题")
            output = data.get("data", {}).get("output", "未获取到回答")
            return f"问题：{instruction}\n回答：{output}"
        else:
            return f"API Error: {data.get('msg', 'Unknown error')}"
    except requests.RequestException as e:
        return f"请求失败: {str(e)}"

if __name__ == "__main__":
    print(get_ruo_zhi_ba_article())
