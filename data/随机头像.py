"""随机头像（多源）：qlogo → jitsu"""
import random

from _multisource import try_sources, emit_image


def src_qlogo():
    qq = random.randint(10000, 999999999)
    return f"https://q.qlogo.cn/g?b=qq&nk={qq}&s=640"


def src_jitsu():
    return "https://moe.jitsu.top/img/"


if __name__ == "__main__":
    emit_image(try_sources([src_qlogo, src_jitsu]), "Anime Avatar")
