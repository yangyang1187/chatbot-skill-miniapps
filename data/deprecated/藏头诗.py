import requests
import sys

def get_acrostic(poem_head):
    """
    获取藏头诗。

    Args:
        poem_head (str): 藏头诗的头字。

    Returns:
        str: 生成的藏头诗，如果请求失败则返回错误信息。
    """
    url = f"https://api.52vmy.cn/api/ai/acrostic?msg={poem_head}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功

        # 解析JSON数据
        data = response.json()

        # 获取藏头诗
        if data.get("code") == 200:
            acrostic = data.get("data", {}).get("answer", "未获取到藏头诗")
            return f"藏头诗：\n{acrostic}"
        else:
            return f"API Error: {data.get('msg', 'Unknown error')}"
    except requests.RequestException as e:
        return f"请求失败: {str(e)}"

def main():
    if len(sys.argv) > 1:
        poem_head = ' '.join(sys.argv[1:])  # 将所有命令行参数合并为一个字符串
    else:
        poem_head = input("请输入藏头诗的头字：")

    print("-" * 20 + "藏头诗" + "-" * 20)
    print(get_acrostic(poem_head))  # 打印藏头诗

if __name__ == "__main__":
    main()
