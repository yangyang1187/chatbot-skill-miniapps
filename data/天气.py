"""天气查询（多源）：alapi(需token) → wttr.in → open-meteo(免key)"""
import sys
import os
import urllib.parse

from _multisource import try_sources, fetch_json, fetch_text, emit

ALAPI_TOKEN = os.environ.get("ALAPI_TOKEN", "")

WMO_CODES = {0: "晴", 1: "大部晴朗", 2: "多云", 3: "阴", 45: "雾", 48: "冻雾",
             51: "毛毛雨", 53: "毛毛雨", 55: "强毛毛雨", 61: "小雨", 63: "中雨",
             65: "大雨", 66: "冻雨", 67: "强冻雨", 71: "小雪", 73: "中雪", 75: "大雪",
             77: "雪粒", 80: "阵雨", 81: "强阵雨", 82: "暴雨", 85: "阵雪", 86: "强阵雪",
             95: "雷暴", 96: "雷暴伴冰雹", 99: "强雷暴伴冰雹"}


def src_alapi(city):
    if not ALAPI_TOKEN:
        return None
    data = fetch_json("https://v3.alapi.cn/api/tianqi", {"city": city, "token": ALAPI_TOKEN})
    if data.get("code") != 200:
        return None
    d = data["data"]
    aqi = d.get("aqi", {})
    return (f"城市：{d.get('city', city)}\n日期：{d.get('date', 'N/A')}\n"
            f"天气：{d.get('weather', 'N/A')} {d.get('temp', 'N/A')}℃\n"
            f"温度范围：{d.get('min_temp', 'N/A')} - {d.get('max_temp', 'N/A')}℃\n"
            f"湿度：{d.get('humidity', 'N/A')}%  风：{d.get('wind', '')}{d.get('wind_power', '')}级\n"
            f"空气质量：{aqi.get('air_level', 'N/A')} (AQI {aqi.get('air', 'N/A')})")


def src_wttr(city):
    text = fetch_text(f"https://wttr.in/{urllib.parse.quote(city)}",
                      {"format": "%l: %C %t (体感 %f) 湿度 %h 风 %w", "lang": "zh"})
    return text if text and text != "Sorry" else None


def src_open_meteo(city):
    geo = fetch_json("https://geocoding-api.open-meteo.com/v1/search",
                     {"name": city, "count": 1, "language": "zh"})
    results = geo.get("results")
    if not results:
        return None
    loc = results[0]
    wx = fetch_json("https://api.open-meteo.com/v1/forecast", {
        "latitude": loc["latitude"], "longitude": loc["longitude"],
        "current": "temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m",
        "timezone": "auto"})
    cur = wx["current"]
    desc = WMO_CODES.get(cur.get("weather_code"), "未知")
    return (f"{loc.get('name', city)}: {desc} {cur['temperature_2m']}°C "
            f"湿度 {cur['relative_humidity_2m']}% 风速 {cur['wind_speed_10m']}km/h")


if __name__ == "__main__":
    city = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else "北京"
    emit(try_sources([
        lambda: src_alapi(city),
        lambda: src_wttr(city),
        lambda: src_open_meteo(city),
    ]))
