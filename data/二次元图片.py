import requests


def get_anime_image_url():
    # dmoe.cc 直接返回随机二次元图片，URL 本身就是图片地址
    return "https://www.dmoe.cc/random.php"


def main():
    image_url = get_anime_image_url()
    if image_url:
        print(f"![Anime Image]({image_url})")


if __name__ == "__main__":
    main()
