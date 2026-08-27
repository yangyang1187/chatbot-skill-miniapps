"""猫猫图片（多源）：thecatapi → cataas"""
from _multisource import try_sources, fetch_json, emit_image


def src_thecatapi():
    data = fetch_json("https://api.thecatapi.com/v1/images/search", {"limit": 1})
    if data:
        return data[0].get("url")


def src_cataas():
    return "https://cataas.com/cat"


if __name__ == "__main__":
    emit_image(try_sources([src_thecatapi, src_cataas]), "Cat Image")
