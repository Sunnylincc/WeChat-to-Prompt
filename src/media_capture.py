"""First-party browser-assisted capture: no third-party resolver or credentials.

Inspect a HAR captured by the user while they legitimately play a video, or
listen for network responses from a dedicated Playwright browser session.
Never persist cookies or authorization headers.
"""
import json
from pathlib import Path
from urllib.parse import urlparse

MEDIA_HOSTS = {"finder.video.qq.com", "video.qq.com"}
MEDIA_SUFFIXES = (".mp4", ".m4v", ".mov", ".webm")


def is_media_url(url: str, mime: str = "") -> bool:
    p = urlparse(url)
    if p.scheme != "https" or not p.hostname or p.username or p.password:
        return False
    host = p.hostname.lower()
    if host not in MEDIA_HOSTS and not host.endswith(".video.qq.com"):
        return False
    return p.path.lower().endswith(MEDIA_SUFFIXES) or mime.lower().split(";")[0] in {
        "video/mp4", "video/webm", "video/quicktime", "application/octet-stream"
    }


def extract_media_urls(har: dict) -> list[str]:
    entries = har.get("log", {}).get("entries", [])
    if not isinstance(entries, list):
        raise ValueError("Invalid HAR entries")
    urls: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        request = entry.get("request", {})
        response = entry.get("response", {})
        headers = response.get("headers", [])
        mime = response.get("content", {}).get("mimeType", "")
        if isinstance(headers, list):
            for h in headers:
                if str(h.get("name", "")).lower() == "content-type":
                    mime = str(h.get("value", mime))
        url = request.get("url", "")
        if isinstance(url, str) and is_media_url(url, mime) and url not in urls:
            urls.append(url)
    return urls


def inspect_har(path: str) -> list[str]:
    # A HAR can contain private credentials. Read only in memory; do not upload.
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return extract_media_urls(data)
