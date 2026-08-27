"""看妹妹（多源）：3650000(mode=3) → jitsu → dmoe"""
from _multisource import try_sources, fetch_json, emit_image


def src_3650000():
    data = fetch_json("https://3650000.xyz/api/", {"type": "json", "mode": 3})
    if data.get("code") == 200 and data.get("url"):
        return data["url"]


def src_jitsu():
    return "https://moe.jitsu.top/img/"


def src_dmoe():
    return "https://www.dmoe.cc/random.php"


if __name__ == "__main__":
    emit_image(try_sources([src_3650000, src_jitsu, src_dmoe]), "Anime Image")
