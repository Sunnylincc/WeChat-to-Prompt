# WeChat-to-Prompt

Local research MVP: turn authorized short videos into structured AI video-generation prompts for Sora, Runway, Kling, or a generic model.

**Status (Oct 2026):** Local file upload, Gemini API integration, prompt templates, and experimental yt-dlp public URL extraction are implemented. **Experimental WeChat Channels share-link extraction is implemented behind an opt-in consent checkbox, but the provided real link has not been verified end-to-end.** A real accessible link is needed to investigate a permitted approach. GitHub hosts the source code; it does not run this app.

## Quick start

Python 3.10+ required:

```bash
git clone https://github.com/Sunnylincc/WeChat-to-Prompt.git
cd WeChat-to-Prompt
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Copy .env.example to .env; edit .env and enter your own Gemini API key
python app.py
```

Visit http://127.0.0.1:7860. Upload an MP4/MOV/WebM/MKV file you have permission to analyze. Requires your own GEMINI_API_KEY, with potential API usage costs.

## Tests
```bash
python -m pytest -q
```

Unit tests cover prompts and link validation; they do **not** establish live Gemini connectivity or working WeChat extraction.

## Next steps
1. Validate authorized video upload -> Gemini -> prompt with a real API key.
2. Test the provided sample https://weixin.qq.com/sph/ABAYvs0amf locally with an explicit opt-in. The parser currently uses an unaffiliated third-party endpoint and sends the pasted link to that service. Do not use private links or login credentials.
3. Validate the experimental resolver across more accessible links and replace or disable it if terms, reliability or security are unsuitable. The code does not bypass access controls.
4. Integrate with ClipToPrompt only after end-to-end validation.

## Privacy and constraints
No real API keys, tokens, cookies, session details, sample private video files, or identifying user data belong in this public repository. The local .env is gitignored. Videos analyzed by Gemini are uploaded to Google's API. We do not bypass authentication, DRM, or access controls. Non-commercial or open-source status does not automatically waive platform terms or third-party licenses. This prototype is not hardened for public hosting.


## WeChat link privacy
The optional checkbox is off by default. When enabled, the URL is shared with `sph.litao.workers.dev` and the returned media is downloaded locally before being submitted to Gemini. This third-party service is not affiliated with Tencent or this project. Its API may change without notice. No WeChat login credentials are needed or accepted.

## October 2026 resolver status
Independent reports indicate the formerly anonymous `sph.litao.workers.dev` parser now requires authentication and cannot be assumed operational (HTTP 401). We do not use it as an automatic default. For WeChat links, configure an HTTPS resolver you have authorization to use using `WECHAT_RESOLVER_ENDPOINT` and optionally `WECHAT_RESOLVER_TOKEN` in your local `.env`. The UI opt-in control is still required. If unavailable, upload a video you own or have permission to analyze. **The supplied sample link `https://weixin.qq.com/sph/ABAYvs0amf` remains unverified as a playable video.** The separate ClipToPrompt product is unchanged until an authorized parser is validated.

## Self-developed, no-resolver capture experiment

We are no longer pursuing Xiaobao or publicly exposed third-party WeChat parsing APIs. The project now includes our own first-party **browser-assisted network observation** in `tools/capture_wechat.py` and a HAR metadata extractor in `src/media_capture.py`.

```bash
pip install playwright
python -m playwright install chromium
python tools/capture_wechat.py https://weixin.qq.com/sph/ABAYvs0amf
```

This opens an interactive Chromium browser. If the video plays through a normal authorized browser session, it detects media network responses without exporting browser cookies or auth headers. It intentionally prints the media host/path only because temporary query tokens can be sensitive.

**Known limitation:** WeChat's share page may only play inside WeChat or an authenticated environment. When that happens the browser will not see video packets; that is not a bug in Gemini, and the script will report no observed media. It does not impersonate WeChat, copy login sessions, or bypass access controls. The provided sample URL has **not** been verified as playable in the execution environment. This is a diagnostic foundation, not a claim of automatic URL-to-prompt support.

Privacy: HAR files can contain cookies and tokens; do not upload/commit HAR files. The HAR extractor reads locally. This code does not require or retrieve the user's WeChat account credentials.
