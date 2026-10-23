"""Prompt templates for authorized video analysis."""

SUPPORTED_STYLES = ("Sora", "Runway", "Kling", "Generic")


def build_instruction(style: str) -> str:
    if style not in SUPPORTED_STYLES:
        raise ValueError(f"Unknown target format: {style}")
    return f"""Analyze the attached video and write a production-ready {style} text-to-video prompt in English.
Identify its first-second hook, subjects, environment, action sequence, camera movement,
lighting, composition, temporal pacing, audio cues, and the ending. Recreate the visual
principles and motion, without copying visible text, logos, watermarks, or identifiable
people. Avoid making unsupported claims. Where visual information is unclear, mark it
as uncertain rather than guessing.

Return exactly these sections:
1. VISUAL BREAKDOWN (brief factual description)
2. FIRST-SECOND HOOK
3. {style.upper()} VIDEO GENERATION PROMPT (one coherent paste-ready prompt)
4. NEGATIVE PROMPT (if useful)
5. OPTIONAL CREATIVE VARIATION (an original alternative, not a direct copy)
Do not claim the resulting generation is guaranteed to match the source.
"""
