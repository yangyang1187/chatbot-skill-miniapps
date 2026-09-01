"""以图搜图（qqBot 搜图功能移植）
用法：搜图 <图片URL>
源 1：trace.moe（免 key，动漫场景识别，返回番剧标题/集数/相似度）
源 2：saucenao（需环境变量 SAUCENAO_API_KEY，支持 pixiv/游戏 CG 等更广来源）
注：ascii2d 已被 Cloudflare 盾拦截，暂不可用。
"""
import os
import sys

from _multisource import emit, try_sources


def _get(url, params=None, timeout=30):
    import httpx
    headers = {"User-Agent": "Mozilla/5.0 chatbot-miniapp/1.0"}
    with httpx.Client(timeout=timeout, follow_redirects=True, headers=headers) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        return resp


def src_tracemoe(image_url):
    data = _get("https://api.trace.moe/search", params={
        "url": image_url, "anilistInfo": "",
    }).json()
    results = data.get("result") or []
    lines = []
    for r in results[:3]:
        sim = round(r.get("similarity", 0) * 100, 1)
        if sim < 60:
            continue
        anilist = r.get("anilist") or {}
        title = anilist.get("title", {})
        name = (title.get("romaji") or title.get("english")
                or title.get("native") or "未知番剧")
        ep = r.get("episode") or (anilist.get("nextAiringEpisode") or {}).get("episode", "?")
        lines.append((sim, f"相似度 {sim}%｜《{name}》第 {ep} 集\n![命中画面]({r.get('image')})"))
    if not lines:
        return None
    lines.sort(key=lambda x: -x[0])
    return "\n\n".join(text for _, text in lines)


def src_saucenao(image_url):
    api_key = os.environ.get("SAUCENAO_API_KEY")
    if not api_key:
        return None
    data = _get("https://saucenao.com/search.php", params={
        "db": 999, "output_type": 2, "numres": 3,
        "api_key": api_key, "url": image_url,
    }).json()
    results = data.get("results") or []
    lines = []
    for r in results[:3]:
        h = r.get("header", {})
        m = r.get("data", {})
        title = m.get("title") or m.get("material") or m.get("eng_name") or "未知标题"
        url = m.get("ext_urls", [""])[0]
        sim = round(h.get("similarity", 0), 1)
        member = m.get("member_name") or m.get("author") or ""
        lines.append(f"相似度 {sim}%｜{title}" + (f"｜作者 {member}" if member else "") + f"\n{url}")
    return "\n\n".join(lines) if lines else None


if __name__ == "__main__":
    image_url = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else ""
    if not image_url.startswith(("http://", "https://")):
        print("用法：搜图 <图片URL>，例如 搜图 https://example.com/pic.jpg")
        sys.exit(2)
    result = try_sources([
        lambda: src_tracemoe(image_url),
        lambda: src_saucenao(image_url),
    ])
    emit(result)
