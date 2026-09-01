"""B 站直播间查询（qqBot B 站监控功能的轻量单发版）
用法：B站直播 <房间号或主播 UID>
源 1：room/v1/Room/get_info（房间标题/分区/人气/开播状态）
源 2：room/v1/Room/room_playing 兜底
"""
import sys

from _multisource import emit, fetch_json, try_sources

STATUS = {0: "未开播", 1: "🔴 直播中", 2: "轮播中"}


def _fmt(info):
    live_status = info.get("live_status", 0)
    watched = info.get("watched_show") or {}
    parts = [
        f"📺 {info.get('title', '未知标题')}",
        f"状态：{STATUS.get(live_status, '未知')}",
    ]
    if watched.get("num"):
        parts.append(f"人气：{watched['num']} 人观看")
    parts.append(f"分区：{info.get('parent_area_name', '')}·{info.get('area_name', '')}")
    parts.append(f"直播间：https://live.bilibili.com/{info.get('room_id', '')}")
    if live_status == 1 and info.get("keyframe"):
        parts.append(f"![直播画面截图]({info['keyframe']})")
    return "\n".join(parts)


def src_room_api(room_id):
    data = fetch_json(
        "https://api.live.bilibili.com/room/v1/Room/get_info",
        params={"room_id": room_id},
    )
    if data.get("code") != 0:
        return None
    return _fmt(data.get("data", {}))


def src_room_playing(room_id):
    data = fetch_json(
        "https://api.live.bilibili.com/room/v1/Room/room_playing",
        params={"room_id": room_id},
    )
    if data.get("code") != 0:
        return None
    d = data.get("data", {})
    return (f"📺 {d.get('title', '未知标题')}\n"
            f"状态：{STATUS.get(d.get('live_status', 0), '未知')}\n"
            f"直播间：https://live.bilibili.com/{d.get('room_id', room_id)}")


if __name__ == "__main__":
    room_id = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else ""
    if not room_id.isdigit():
        print("用法：B站直播 <房间号>，例如 B站直播 21452505")
        sys.exit(2)
    emit(try_sources([
        lambda: src_room_api(room_id),
        lambda: src_room_playing(room_id),
    ]))
