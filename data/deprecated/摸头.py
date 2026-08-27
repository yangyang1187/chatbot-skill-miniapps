import requests
import sys

def get_motou_image_url(qq=None):
    api_url = f"https://uapis.cn/api/mt?qq={qq}"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return api_url
        else:
            print("获取摸头图片失败,输入的格式是:/摸头 1234567890")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

def main():
    # 从命令行参数中解析输入
    if len(sys.argv) > 1:
        qq_number = sys.argv[1]  # 获取用户输入的QQ号
    else:
        # 未输入QQ号，默认使用调用命令的账号
        qq_number = "10001"

    motou_image_url = get_motou_image_url(qq=qq_number)
    if motou_image_url:
        markdown_image_link = f"![摸头]({motou_image_url})"
        print(markdown_image_link)

if __name__ == "__main__":
    main()