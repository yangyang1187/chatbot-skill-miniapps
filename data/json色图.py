"""json色图（多源）：jitsu JSON → dmoe"""
from _multisource import try_sources, fetch_json, emit_image


def src_jitsu():
    data = fetch_json("https://moe.jitsu.top/img/",
                      {"size": "original", "type": "json", "num": 1})
    if data.get("code") == 200:
        pics = data.get("pics", [])
        if pics:
            return pics[0]


def src_dmoe():
    return "https://www.dmoe.cc/random.php"


if __name__ == "__main__":
    emit_image(try_sources([src_jitsu, src_dmoe]), "Anime Image")
