import requests  # 导入 requests 库用于发送 HTTP 请求
import json  # 导入 json 库用于处理 JSON 数据
import os  # 导入 os 库用于文件和路径操作
import sys  # 导入 sys 库用于访问命令行参数

def generate_image(api_key, prompt, size, steps, prompt_upsampling, seed, guidance, safety_tolerance, interval):
    # 定义生成图像的函数
    url = "设置 API 端点 URL"  # 设置 API 端点 URL
    headers = {
        "Authorization": f"Bearer {api_key}",  # 添加授权头，包含 API 密钥
        "Content-Type": "application/json"  # 指定请求体的内容类型为 JSON
    }

    body = {
        "model": "dall-e-3",  # 设置使用的模型名称
        "prompt": f"日本动漫风格 {prompt}",  # 在提示词前添加“日本动漫风格”
        "size": size,  # 图像尺寸
        "steps": steps,  # 生成步骤数
        "prompt_upsampling": prompt_upsampling,  # 是否进行提示词上采样
        "seed": seed,  # 随机种子，用于生成的可重复性
        "guidance": int(guidance),  # 指导参数，确保为整数
        "safety_tolerance": safety_tolerance,  # 安全容忍度
        "interval": interval  # 请求间隔
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

# 从命令行获取提示词
if len(sys.argv) < 2:  # 检查是否提供了提示词
    print("请提供提示词")  # 提示用户输入格式
    sys.exit(1)  # 退出程序

prompt = sys.argv[1]  # 获取命令行参数中的提示词

# 从环境变量读取 API 配置
api_key = os.environ.get("DALLE_API_KEY", "你的 API 密钥")
api_url = os.environ.get("DALLE_API_URL", "设置 API 端点 URL")
if "你的 API 密钥" in api_key or "设置 API 端点" in api_url:
    print("未配置 DALL·E API：请设置环境变量 DALLE_API_KEY 和 DALLE_API_URL")
    sys.exit(0)

# 示例调用
generate_image(
    api_key=api_key,  # 传入 API 密钥
    prompt=prompt,  # 使用命令行传入的提示词
    size="1024x1792",  # 图像尺寸设置为 768x1024
    steps=50,  # 设置生成步骤数为 50
    prompt_upsampling=True,  # 设置提示词上采样为 True
    seed=42,  # 设置随机种子为 42
    guidance=7,  # 指导参数设置为 7
    safety_tolerance=5,  # 安全容忍度设置为 5
    interval=10  # 请求间隔设置为 10
)
