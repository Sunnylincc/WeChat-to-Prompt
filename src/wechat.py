"""Opt-in experimental WeChat Channels share-link parser.

This calls an unaffiliated third-party endpoint. Only use for content you are
authorized to process. No credentials, cookies, DRM or access controls bypassed.
"""
import ipaddress
import os
import socket
from pathlib import Path
from urllib.parse import urlparse

import requests

PARSER = os.getenv("WECHAT_RESOLVER_ENDPOINT", "").strip()
MAX_BYTES = 200 * 1024 * 1024


def validate_share_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme != "https" or parsed.hostname != "weixin.qq.com":
        raise ValueError("Expected https://weixin.qq.com/sph/<share-id>")
    if not parsed.path.startswith("/sph/") or not parsed.path[5:].strip("/"):
        raise ValueError("Invalid WeChat Channels share URL")
    return url.strip()


def resolve_and_download(url: str, folder: str, consent: bool = False) -> Path:
    """Experimental resolver. The user must explicitly allow third-party disclosure."""
    url = validate_share_url(url)
    if not consent:
        raise ValueError("Enable the third-party parser consent checkbox first.")
    if not PARSER:\n        raise ValueError("No authorized WeChat parser is configured. The previously free public parser now requires authentication. Upload a video you are authorized to analyze instead.")\n    parser_url = urlparse(PARSER)\n    if parser_url.scheme != "https" or not parser_url.hostname or parser_url.username or parser_url.password or parser_url.port:\n        raise ValueError("WECHAT_RESOLVER_ENDPOINT must be a valid HTTPS endpoint.")\n    token = os.getenv("WECHAT_RESOLVER_TOKEN", "").strip()\n    headers = {"Authorization": f"Bearer {token}"} if token else {}\n    response = requests.post(PARSER, json={"url": url}, headers=headers, timeout=20)
    if response.status_code == 401:\n        raise ValueError("WeChat resolver requires authorization. Set an authorized resolver token or upload a video.")\n    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("Unexpected parser response")
    data = payload.get("data") or payload.get("result") or payload
    if not isinstance(data, dict):
        raise ValueError("Parser did not provide video metadata")
    media_url = None
    for field in ("h264_url", "h264Url", "video_url", "videoUrl", "h265_url"):
        if isinstance(data.get(field), str) and data[field].startswith("https://"):
            media_url = data[field]
            break
    if not media_url:
        raise ValueError("Parser returned no accessible video URL; the link may be expired or unsupported.")
    parsed = urlparse(media_url)
    if parsed.username or parsed.password or not parsed.hostname:
        raise ValueError("Unsafe media URL")
    # Restrict local-network targets. Check the resolved address again on each
    # request by disabling redirects; public hosting needs a stronger proxy.
    addresses = socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(item[4][0]).is_global for item in addresses):
        raise ValueError("Media host is not public")
    output = Path(folder) / "wechat-video.mp4"
    with requests.get(media_url, stream=True, timeout=30, allow_redirects=False) as stream:
        stream.raise_for_status()
        if 300 <= stream.status_code < 400:
            raise ValueError("Media redirect is not supported")
        size = 0
        with output.open("wb") as dest:
            for chunk in stream.iter_content(1024 * 512):
                size += len(chunk)
                if size > MAX_BYTES:
                    raise ValueError("Video exceeds 200 MB")
                dest.write(chunk)
    if not output.stat().st_size:
        raise ValueError("Empty video")
    return output
