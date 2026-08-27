import io
import math
import os
import sys
import tempfile

import requests
from PIL import Image, ImageDraw

CANVAS = 256  # petpet 经典尺寸
FRAMES = 12

# Pillow >=9.1 用 Resampling，老版本回退到常量
try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.LANCZOS


def fetch_avatar(qq):
    url = f"https://q.qlogo.cn/g?b=qq&nk={qq}&s=640"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content)).convert("RGBA")


def circle_crop(img, size):
    img = img.resize((size, size), RESAMPLE)
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def draw_hand(draw, cx, cy, scale, angle=0):
    """画一只卡通手（掌心朝下拍头）。"""
    skin = (255, 224, 196, 255)
    edge = (235, 195, 160, 255)
    # 手掌（大椭圆）
    pw, ph = int(70 * scale), int(46 * scale)
    draw.ellipse((cx - pw, cy - ph, cx + pw, cy + ph), fill=skin, outline=edge, width=3)
    # 四根手指（朝下的小椭圆）
    for i in range(4):
        fx = cx - pw + int((i + 0.5) * (2 * pw / 4))
        fy = cy + ph - int(10 * scale)
        fw, fh = int(16 * scale), int(26 * scale)
        draw.ellipse((fx - fw, fy - fh, fx + fw, fy + fh), fill=skin, outline=edge, width=2)


def make_gif(avatar, out_path):
    frames = []
    head_size = int(CANVAS * 0.62)
    head = circle_crop(avatar, head_size)
    for i in range(FRAMES):
        t = i / FRAMES
        # 拍头节奏：手向下→头像被压扁→回弹
        phase = math.sin(t * math.pi * 2)
        press = max(0.0, phase)  # 0~1 下压程度
        squash = 1.0 - 0.18 * press
        hand_y = int(30 + 26 * press)

        frame = Image.new("RGBA", (CANVAS, CANVAS), (255, 255, 255, 255))
        # 头像（被压扁）
        hw = head_size
        hh = int(head_size * squash)
        squashed = head.resize((hw, hh), Image.LANCZOS)
        hx = (CANVAS - hw) // 2
        hy = CANVAS - hh - int(CANVAS * 0.06)
        frame.paste(squashed, (hx, hy), squashed)
        # 手
        d = ImageDraw.Draw(frame)
        draw_hand(d, CANVAS // 2, hand_y, scale=1.0)
        frames.append(frame.convert("RGB"))

    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        optimize=True,
    )


def main():
    qq = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else "10001"
    if not qq.isdigit():
        print("用法：/摸头 <QQ号>，例如 /摸头 123456")
        return
    try:
        avatar = fetch_avatar(qq)
    except Exception as e:
        print(f"获取头像失败: {e}")
        return

    # 输出到临时文件，打印本地路径（运行器会把它作为图片发送）
    out_path = os.path.join(tempfile.gettempdir(), f"petpet_{qq}.gif")
    make_gif(avatar, out_path)
    print(f"![摸头]({out_path})")


if __name__ == "__main__":
    main()
