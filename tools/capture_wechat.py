"""Capture accessible WeChat video media requests using a local browser.

Install: pip install playwright && python -m playwright install chromium
Usage: python tools/capture_wechat.py https://weixin.qq.com/sph/ABAYvs0amf
The browser is interactive: play only videos you can legitimately access.
No cookies, HAR files, passwords or tokens are saved.
"""
import sys
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

sys.path.insert(0, ".")
from src.media_capture import is_media_url


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/capture_wechat.py <https://weixin.qq.com/sph/...>")
    url = sys.argv[1]
    p = urlparse(url)
    if p.scheme != "https" or p.hostname != "weixin.qq.com" or not p.path.startswith("/sph/"):
        raise SystemExit("Expected a WeChat Channels HTTPS share link")
    found = set()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        def record(response):
            mime = response.headers.get("content-type", "")
            if is_media_url(response.url, mime) and response.url not in found:
                found.add(response.url)
                # Query strings may include temporary access tokens; print only host and path.
                parts = urlparse(response.url)
                print(f"Media response observed: {parts.scheme}://{parts.netloc}{parts.path}")
        page.on("response", record)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
        except Exception as error:
            print("Page navigation failed:", type(error).__name__)
        print("Play the video in this browser window if accessible, then press Enter here.")
        input()
        print(f"Media responses detected: {len(found)}")
        if found:
            print("Browser-assisted capture is feasible for this link.")
        else:
            print("No accessible media response detected; the share page may require the WeChat app.")
        browser.close()


if __name__ == "__main__":
    main()
