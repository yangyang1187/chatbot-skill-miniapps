"""看腿（多源）：3650000(mode=7) → jitsu → dmoe"""
from _multisource import try_sources, fetch_json, emit_image


def src_3650000():
    data = fetch_json("http://3650000.xyz/api/", {"type": "json", "mode": 7})
    if data.get("code") == 200 and data.get("url"):
        return data["url"]


def src_jitsu():
    return "https://moe.jitsu.top/img/"


def src_dmoe():
    return "https://www.dmoe.cc/random.php"


if __name__ == "__main__":
    emit_image(try_sources([src_3650000, src_jitsu, src_dmoe]), "Anime Image")
