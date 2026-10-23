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
