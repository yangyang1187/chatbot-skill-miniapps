import requests
import os
import random
import sys

API_URL = os.environ.get("IDEOGRAM_API_URL", "你的api路劲")
API_KEY = os.environ.get("IDEOGRAM_API_KEY", "你的api key")


def generate_image(prompt: str):
    if "你的api" in API_URL or "你的api" in API_KEY:
        return "未配置 ideogram API：请设置环境变量 IDEOGRAM_API_URL 和 IDEOGRAM_API_KEY"
    url = API_URL
    headers = {
        'Authorization': f'Bearer {API_KEY}',  # 完整格式"Bearer sk-123...3123"
        'Content-Type': 'application/json',
    }

    request_data = {
        "image_request": {
            "prompt": f"使用日本动漫风格，{prompt}",#使用日本动漫风格为强制提示词
            "model": "V_2_TURBO",
            "magic_prompt_option": "AUTO",
            "seed": random.randint(0, 2147483647)
        }
    }

    response = requests.post(url, headers=headers, json=request_data)

    if response.status_code == 200:
        image_url = response.json()['data'][0]['url']
        return f"![图像]({image_url})"
    else:
        return f"错误信息: {response.text}"

def main():
    if len(sys.argv) < 2:
        print("请提供提示词，例如: 猫")
        return

    prompt = ' '.join(sys.argv[1:]).strip()
    markdown_output = generate_image(prompt)

    print(markdown_output)

if __name__ == "__main__":
    main()
