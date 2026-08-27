"""二次元图片（多源）：dmoe → jitsu 重定向"""
from _multisource import try_sources, emit_image


def src_dmoe():
    # dmoe 直接返回图片，URL 即图片地址
    return "https://www.dmoe.cc/random.php"


def src_jitsu():
    # jitsu 也是直出图片
    return "https://moe.jitsu.top/img/"


if __name__ == "__main__":
    emit_image(try_sources([src_dmoe, src_jitsu]), "Anime Image")
