from src.media_capture import extract_media_urls, is_media_url


def test_reject_non_video_and_private_hosts():
    assert is_media_url("https://finder.video.qq.com/sample.mp4")
    assert not is_media_url("https://evil.example/a.mp4")
    assert not is_media_url("http://finder.video.qq.com/sample.mp4")


def test_har_extract():
    har = {"log": {"entries": [
        {"request": {"url": "https://finder.video.qq.com/a.mp4?token=x"},
         "response": {"content": {"mimeType": "video/mp4"}, "headers": []}},
        {"request": {"url": "https://other.example/foo.mp4"},
         "response": {"content": {"mimeType": "video/mp4"}, "headers": []}},
    ]}}
    assert extract_media_urls(har) == ["https://finder.video.qq.com/a.mp4?token=x"]
