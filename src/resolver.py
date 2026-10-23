"""Conservative public-link resolver; no authentication bypass or private APIs."""

from pathlib import Path
from urllib.parse import urlparse


MAX_BYTES = 200 * 1024 * 1024


class UnsupportedLinkError(ValueError):
    pass


def is_wechat_share_link(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return host == "weixin.qq.com" or host.endswith(".weixin.qq.com")


def resolve_public_video(url: str, folder: str) -> Path:
    """Attempt public extraction via yt-dlp. Protected WeChat links are not supported."""
    from yt_dlp import YoutubeDL

    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Please paste a valid http(s) URL.")
    if is_wechat_share_link(url):
        raise UnsupportedLinkError(
            "WeChat Channels link extraction needs validation with a permitted sample. "
            "For now upload an MP4 you own or are authorized to process."
        )
    output = str(Path(folder) / "source.%(ext)s")
    opts = {
        "outtmpl": output,
        "format": "best[ext=mp4]/best",
        "noplaylist": True,
        "ignoreerrors": False,
        "quiet": True,
        "no_warnings": True,
        "max_filesize": MAX_BYTES,
        "socket_timeout": 20,
        "retries": 1,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if not info or info.get("is_live"):
            raise ValueError("Only accessible, non-live videos are supported.")
        if (info.get("filesize") or info.get("filesize_approx") or 0) > MAX_BYTES:
            raise ValueError("Video exceeds 200 MB limit.")
        ydl.download([url])
    files = [p for p in Path(folder).glob("source.*") if p.is_file()]
    if not files:
        raise ValueError("Could not download video from the public URL.")
    result = files[0]
    if result.stat().st_size > MAX_BYTES:
        raise ValueError("Video exceeds 200 MB limit.")
    return result
