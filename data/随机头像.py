import requests


def get_anime_avatar_url():
    # 用随机 QQ 号从 QQ 头像服务取动漫头像（URL 本身就是图片地址）
    import random
    qq = random.randint(10000, 999999999)
    return f"https://q.qlogo.cn/g?b=qq&nk={qq}&s=640"


def main():
    avatar_url = get_anime_avatar_url()
    if avatar_url:
        print(f"![Anime Avatar]({avatar_url})")


if __name__ == "__main__":
    main()
