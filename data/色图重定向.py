"""色图重定向（多源）：anosu重定向 → jitsu → dmoe"""
from _multisource import try_sources, emit_image

try:
    import httpx
except ImportError:
    httpx = None


def src_anosu():
    if httpx is None:
        return None
    with httpx.Client(timeout=15, follow_redirects=False) as client:
        resp = client.get("https://api.anosu.top/img/")
        if resp.is_redirect:
            return resp.headers.get("Location")
        return str(resp.url)


def src_jitsu():
    return "https://moe.jitsu.top/img/"


def src_dmoe():
    return "https://www.dmoe.cc/random.php"


if __name__ == "__main__":
    emit_image(try_sources([src_anosu, src_jitsu, src_dmoe]), "Anime Image")
