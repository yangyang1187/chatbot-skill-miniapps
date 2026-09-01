"""Pixiv 插画查询（qqBot 色图(Pixiv版) 的轻量移植）
用法：pixiv图 <插画ID或URL> [页码(从1开始)]
- 信息接口：pixiv web ajax（公开作品免登录；R-18 需环境变量 PIXIV_PHPSESSID）
- 图片输出：i.pximg.net 有防盗链，走反代 i.pixiv.re / i.pixiv.cat，
  反代失效时回退原始 pximg 链接（部分客户端需要带 Referer 才能显示）
"""
import os
import re
import sys

from _multisource import emit, try_sources, fetch_json

AJAX_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Referer": "https://www.pixiv.net/",
}
PROXY_HOSTS = ["i.pixiv.re", "i.pixiv.cat"]


def parse_args(raw):
    """从参数里提取插画 ID 和可选页码（1 开始）。

    支持形式：121292560、121292560 2、https://www.pixiv.net/artworks/121292560、
    ...artworks/121292560#3、...artworks/121292560?p=2、... 第3页
    """
    m = re.search(r"(?:artworks/|illust_id=)(\d+)", raw)
    if m:
        illust_id, rest = m.group(1), raw[m.end():]
    else:
        m = re.search(r"\b(\d{4,12})\b", raw)
        if not m:
            return None, 0
        illust_id, rest = m.group(1), raw[m.end():]
    page = 0
    pm = (re.search(r"#(\d+)", rest) or re.search(r"[?&]p=(\d+)", rest)
          or re.search(r"第\s*(\d+)\s*页", rest) or re.search(r"^\s*(\d+)\s*$", rest))
    if pm:
        page = max(int(pm.group(1)) - 1, 0)
    return illust_id, page


def fetch_illust(illust_id):
    import httpx
    headers = dict(AJAX_HEADERS)
    sess = os.environ.get("PIXIV_PHPSESSID")
    if sess:
        headers["Cookie"] = f"PHPSESSID={sess}"
    with httpx.Client(timeout=20, follow_redirects=True, headers=headers) as client:
        resp = client.get(f"https://www.pixiv.net/ajax/illust/{illust_id}")
        resp.raise_for_status()
        return resp.json()


def proxy_image(pximg_url, page_count):
    """pximg 原图 → 反代链 HEAD 校验 → 全部失效时返回原始链接并提示。"""
    original = pximg_url.replace("_p0", f"_p{page_count}") if page_count else pximg_url
    for host in PROXY_HOSTS:
        proxied = original.replace("i.pximg.net", host)
        if _head_ok(proxied):
            return proxied
    return original


def _head_ok(url):
    try:
        import httpx
        r = httpx.head(url, headers={"User-Agent": AJAX_HEADERS["User-Agent"]},
                       follow_redirects=True, timeout=15)
        return r.status_code == 200 and "image" in r.headers.get("content-type", "")
    except Exception:
        return False


def format_illust(body, page):
    title = body.get("title") or body.get("illustTitle") or "无标题"
    author = body.get("userName") or "未知作者"
    pages = body.get("pageCount", 1)
    tags = "、".join(t.get("tag", "") for t in (body.get("tags", {}).get("tags") or [])[:8])
    url = body.get("urls", {}).get("original") or body.get("urls", {}).get("regular")
    if not url:
        return None
    img = proxy_image(url, page if page < pages else 0)
    xrestrict = body.get("xRestrict", 0)
    r18 = " 🔞R-18" if xrestrict == 1 else (" 🔞R-18G" if xrestrict == 2 else "")
    lines = [
        f"🎨 {title}{r18}",
        f"作者：{author}｜共 {pages} 页" + (f"（当前第 {page + 1} 页）" if page and pages > 1 else ""),
    ]
    if tags:
        lines.append(f"标签：{tags}")
    lines.append(f"原地址：https://www.pixiv.net/artworks/{body.get('id', '')}")
    lines.append(f"![{title}]({img})")
    if page >= pages:
        lines.insert(1, f"⚠️ 页码超出范围，已返回第 1 页（共 {pages} 页）")
    return "\n".join(lines)


def fetch_random(r18):
    """无参数时：从 lolicon(Pixiv原图反代) 随机取一张。r18: 0=非R18, 1=R18, 2=混。"""
    import random
    params = {"num": 1, "r18": r18}
    # 随机切换代理域名，提高存活率
    api_hosts = ["https://api.lolicon.app/setu/v2",
                 "https://api.lolicon.app/setu/v2"]
    data = None
    for host in api_hosts:
        try:
            data = fetch_json(host, params=params)
            if data and not data.get("error"):
                break
        except Exception:
            continue
    if not data or not data.get("data"):
        return None
    it = data["data"][0]
    tags = "、".join((it.get("tags") or [])[:8])
    url = (it.get("urls") or {}).get("original") or (it.get("urls") or {}).get("regular")
    if not url:
        return None
    # 统一保证走反代，客户端不带 Referer 也能显示
    url = url.replace("i.pximg.net", "i.pixiv.re")
    r18flag = " 🔞R-18" if it.get("r18") else ""
    lines = [
        f"🎨 {it.get('title', '无标题')}{r18flag}",
        f"作者：{it.get('author', '未知')}",
    ]
    if tags:
        lines.append(f"标签：{tags}")
    lines.append(f"原地址：https://www.pixiv.net/artworks/{it.get('pid', '')}")
    lines.append(f"![{it.get('title', '')}]({url})")
    return "\n".join(lines)


if __name__ == "__main__":
    raw = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else ""
    if not raw or re.match(r"(随机|random|随)", raw, re.IGNORECASE):
        # 随机模式：无参或「随机」开头；跟上 r18/黄/色 字眼则抽 R-18
        r18 = 1 if re.search(r"r18|黄|色", raw, re.IGNORECASE) else 0
        emit(try_sources([lambda: fetch_random(r18), lambda: fetch_random(0)]))
        sys.exit(0)
    illust_id, page = parse_args(raw)
    if not illust_id:
        print("没能从参数里解析出插画 ID，请给数字 ID 或 pixiv 作品链接，或直接输入「pixiv图 随机」")
        sys.exit(2)
    if not illust_id:
        print("没能从参数里解析出插画 ID，请给数字 ID 或 pixiv 作品链接")
        sys.exit(2)

    def run():
        data = fetch_illust(illust_id)
        if data.get("error"):
            msg = data.get("message", "")
            hint = "（R-18 作品需要配置环境变量 PIXIV_PHPSESSID 才能查看）" if "r-18" in msg.lower() or "該作品" in msg else ""
            return f"Pixiv 返回错误：{msg}{hint}" if msg else None
        body = data.get("body") or {}
        return format_illust(body, page)

    emit(try_sources([run]))
