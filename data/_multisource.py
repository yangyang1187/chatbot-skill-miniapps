"""多源 fallback 共享库。

用法：
    from _multisource import try_sources, fetch_json, fetch_text, emit, emit_image

    emit(try_sources([source_a, source_b, lambda: "本地兜底内容"]))

每个 source 函数返回 str（成功）或 None（失败），try_sources 按顺序尝试。
"""
import json
import sys

try:
    import httpx
except ImportError:
    httpx = None

try:
    import requests
except ImportError:
    requests = None

DEFAULT_TIMEOUT = 12


def try_sources(sources):
    """按顺序尝试各数据源，返回第一个成功的结果；全部失败返回 None。"""
    for fn in sources:
        try:
            result = fn()
            if result:
                return result
        except Exception:
            continue
    return None


def fetch_json(url, params=None, timeout=DEFAULT_TIMEOUT):
    """GET 请求返回 JSON，失败返回 None。"""
    if requests is not None:
        r = requests.get(url, params=params, timeout=timeout,
                         headers={"User-Agent": "Mozilla/5.0 chatbot-miniapp/1.0"})
        r.raise_for_status()
        return r.json()
    if httpx is not None:
        r = httpx.get(url, params=params, timeout=timeout, follow_redirects=True,
                      headers={"User-Agent": "Mozilla/5.0 chatbot-miniapp/1.0"})
        r.raise_for_status()
        return r.json()
    raise RuntimeError("需要 requests 或 httpx 库")


def fetch_text(url, params=None, timeout=DEFAULT_TIMEOUT):
    """GET 请求返回文本，失败返回 None。"""
    if requests is not None:
        r = requests.get(url, params=params, timeout=timeout,
                         headers={"User-Agent": "Mozilla/5.0 chatbot-miniapp/1.0"})
        r.raise_for_status()
        return r.text.strip()
    if httpx is not None:
        r = httpx.get(url, params=params, timeout=timeout, follow_redirects=True,
                      headers={"User-Agent": "Mozilla/5.0 chatbot-miniapp/1.0"})
        r.raise_for_status()
        return r.text.strip()
    raise RuntimeError("需要 requests 或 httpx 库")


def valid_image(url, timeout=DEFAULT_TIMEOUT):
    """HEAD 校验图片 URL 可访问，返回 bool。"""
    try:
        if requests is not None:
            r = requests.head(url, timeout=timeout, allow_redirects=True)
            return r.status_code == 200
        if httpx is not None:
            r = httpx.head(url, timeout=timeout, follow_redirects=True)
            return r.status_code == 200
        return True  # 无 HTTP 库时跳过校验
    except Exception:
        return False


def emit(text):
    """输出文本结果；为 None 时输出失败提示。"""
    if text:
        print(text)
    else:
        print("所有数据源都失败了~请稍后再试")
        sys.exit(1)


def emit_image(url, alt="Image"):
    """输出图片结果（Markdown 格式）。"""
    if url:
        print(f"![{alt}]({url})")
    else:
        print("所有图片源都失败了~请稍后再试")
        sys.exit(1)
