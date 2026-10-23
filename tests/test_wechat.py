import pytest
from src.wechat import validate_share_url, resolve_and_download


def test_valid_sample_url():
    assert validate_share_url("https://weixin.qq.com/sph/ABAYvs0amf").endswith("ABAYvs0amf")


@pytest.mark.parametrize("url", [
    "http://weixin.qq.com/sph/abc",
    "https://notweixin.qq.com/sph/abc",
    "https://weixin.qq.com/",
    "file:///etc/passwd",
])
def test_invalid_links(url):
    with pytest.raises(ValueError):
        validate_share_url(url)


def test_no_third_party_call_without_consent(tmp_path):
    with pytest.raises(ValueError, match="consent"):
        resolve_and_download("https://weixin.qq.com/sph/ABAYvs0amf", str(tmp_path))
