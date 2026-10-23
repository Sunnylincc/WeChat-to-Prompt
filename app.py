"""Local-only web UI for authorized video-to-prompt conversion."""

import os
import tempfile
import time
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from google import genai

from src.prompting import SUPPORTED_STYLES, build_instruction
from src.resolver import MAX_BYTES, UnsupportedLinkError, resolve_public_video

load_dotenv()


def generate_prompt(link: str, upload: str | None, style: str) -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return "Set GEMINI_API_KEY in your local .env file."
    if not upload and not (link or "").strip():
        return "Paste a supported public video URL or upload an authorized video."
    client = None
    uploaded_resource = None
    try:
        with tempfile.TemporaryDirectory(prefix="wechat_to_prompt_") as tmp:
            video = Path(upload) if upload else resolve_public_video(link.strip(), tmp)
            if not video.is_file() or video.stat().st_size > MAX_BYTES:
                return "Video is missing or exceeds 200 MB."
            client = genai.Client(api_key=key)
            uploaded_resource = client.files.upload(file=str(video))
            for _ in range(60):
                uploaded_resource = client.files.get(name=uploaded_resource.name)
                state = str(uploaded_resource.state).upper()
                if "ACTIVE" in state:
                    break
                if "FAILED" in state:
                    return "Gemini could not process the uploaded video."
                time.sleep(2)
            else:
                return "Video processing timed out. Try a shorter video."
            result = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
                contents=[uploaded_resource, build_instruction(style)],
            )
            return result.text or "Gemini returned an empty result."
    except (UnsupportedLinkError, ValueError) as exc:
        return str(exc)
    except Exception as exc:
        # Avoid exposing credentials, response bodies or local file paths in the UI.
        return f"Video processing error ({type(exc).__name__}). Check local configuration."
    finally:
        if uploaded_resource is not None and client is not None:
            try:
                client.files.delete(name=uploaded_resource.name)
            except Exception:
                pass


with gr.Blocks(title="WeChat to Prompt") as app:
    gr.Markdown("# WeChat to Prompt\nTurn authorized videos into AI generation prompts locally.")
    gr.Markdown("**WeChat Channels sharing URLs are not supported yet.** Use a permitted local video upload to test Gemini analysis.")
    url = gr.Textbox(label="Public video URL", placeholder="https://...")
    video = gr.File(label="Or upload video", file_types=[".mp4", ".mov", ".webm", ".mkv"], type="filepath")
    style = gr.Radio(choices=list(SUPPORTED_STYLES), value="Sora", label="Prompt format")
    output = gr.Textbox(label="Generated prompt", lines=16, show_copy_button=True)
    gr.Button("Generate Prompt", variant="primary").click(generate_prompt, inputs=[url, video, style], outputs=output)

if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", share=False)
