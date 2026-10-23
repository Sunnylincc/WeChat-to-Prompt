from src.prompting import SUPPORTED_STYLES, build_instruction
from src.resolver import is_wechat_share_link, resolve_public_video, UnsupportedLinkError

import pytest


@pytest.mark.parametrize("style", SUPPORTED_STYLES)
def test_style_in_prompt(style):
    prompt = build_instruction(style)
    assert style.upper() in prompt
    assert "FIRST-SECOND HOOK" in prompt


def test_reject_unknown_style():
    with pytest.raises(ValueError):
        build_instruction("Unknown")


def test_recognize_wechat_hosts():
    assert is_wechat_share_link("https://weixin.qq.com/sph/abc")
    assert is_wechat_share_link("https://channels.weixin.qq.com/foo")
    assert not is_wechat_share_link("https://notweixin.qq.com/sph/abc")


def test_wechat_link_reports_not_yet_supported(tmp_path):
    with pytest.raises(UnsupportedLinkError):
        resolve_public_video("https://weixin.qq.com/sph/test", str(tmp_path))
