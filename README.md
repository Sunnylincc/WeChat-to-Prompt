# WeChat-to-Prompt

Local research MVP: turn authorized short videos into structured AI video-generation prompts for Sora, Runway, Kling, or a generic model.

**Status (Oct 2026):** Local file upload, Gemini API integration, prompt templates, and experimental yt-dlp public URL extraction are implemented. **WeChat Channels share-link extraction is not implemented or tested yet.** A real accessible link is needed to investigate a permitted approach. GitHub hosts the source code; it does not run this app.

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
2. Inspect a WeChat Channels sharing URL to see whether an authorized, technically reliable video access method exists.
3. Implement a standalone WeChat adapter only if permissible; otherwise retain user-supplied video upload.
4. Integrate with ClipToPrompt only after end-to-end validation.

## Privacy and constraints
No real API keys, tokens, cookies, session details, sample private video files, or identifying user data belong in this public repository. The local .env is gitignored. Videos analyzed by Gemini are uploaded to Google's API. We do not bypass authentication, DRM, or access controls. Non-commercial or open-source status does not automatically waive platform terms or third-party licenses. This prototype is not hardened for public hosting.
