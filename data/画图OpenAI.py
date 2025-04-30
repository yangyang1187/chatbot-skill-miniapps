import requests  # 导入 requests 库用于发送 HTTP 请求
import json  # 导入 json 库用于处理 JSON 数据
import os  # 导入 os 库用于文件和路径操作
import sys  # 导入 sys 库用于访问命令行参数

# 调用OpenAI格式API优化提示词和生成图片

HOST = "http://127.0.0.1:3001" # 设置 API 主机地址
API_KEY = "sk-xxx" # 你的 API 密钥
IMAGE_MODEL = "FLUX.1-dev" #生图模型
PROMPT_MODEL = "deepseek-chat" #提示词优化模型

def generate_image(prompt, size, steps):
    prompt = generate_prompt(prompt)
    # 定义生成图像的函数
    url = HOST + "/v1/images/generations"  # 设置 API 端点 URL
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # 添加授权头，包含 API 密钥
        "Content-Type": "application/json"  # 指定请求体的内容类型为 JSON
    }

    body = {
        "model": IMAGE_MODEL,  # 设置使用的模型名称
        "prompt": f"{prompt}",
        "size": size,  # 图像尺寸
        "steps": steps,  # 生成步骤数
    }

    # 发送 POST 请求到 API
    response = requests.post(url, headers=headers, data=json.dumps(body))

    # 检查响应状态
    if response.status_code == 200:
        response_data = response.json()  # 将响应内容解析为 JSON 格式
        image_url = response_data['data'][0]['url']  # 获取生成的图像 URL
        markdown_image_link = f"![生成的图像]({image_url})"  # 转换为 Markdown 格式
        print(markdown_image_link)  # 打印 Markdown 图片链接
    else:
        error_message = f"Error: {response.status_code} - {response.text}"  # 构建错误信息
        print(error_message)  # 输出错误信息
        
def generate_prompt(prompt):
    # 定义生成提示词的函数
    url = HOST + "/v1/chat/completions"  # 设置 API 端点 URL
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # 添加授权头，包含 API 密钥
        "Content-Type": "application/json"  # 指定请求体的内容类型为 JSON
    }

    body = {
        "model": PROMPT_MODEL,
        "messages": [
            {
                "role": "user",
                "content": f"### Task:\nPlease create an image generation prompt to fit this brief:\n\"[{prompt}]\"\nPlease add more detail and nuance to the prompt and please ONLY reply with the prompt and nothing else. DO NOT include \"Prompt: \" or any other precursor, just the prompt itself, otherwise your comments also get used in the image generation."
            }
        ],
        "params": {
            "temperature": 0.6,
            "max_tokens": 2048
        },
        "stream": False
    }

    # 发送 POST 请求到 API
    response = requests.post(url, headers=headers, data=json.dumps(body))
    # 检查响应状态
    if response.status_code == 200:
        response_data = response.json()  # 将响应内容解析为 JSON 格式
        gen_prompt = response_data['choices'][0]['message']['content']
        print(f"生图提示词：{gen_prompt}")
        return gen_prompt
    else:
        error_message = f"Error: {response.status_code} - {response.text}"  # 构建错误信息
        print(error_message)  # 输出错误信息
        return prompt

# 从命令行获取提示词
if len(sys.argv) < 2:  # 检查是否提供了提示词
    print("请提供提示词")  # 提示用户输入格式
    sys.exit(1)  # 退出程序

prompt = sys.argv[1]  # 获取命令行参数中的提示词

# 示例调用
generate_image(
    prompt=prompt,  # 使用命令行传入的提示词
    size="1024x1024",  # 图像尺寸设置为 768x1024
    steps=25,  # 设置生成步骤数为 50
)