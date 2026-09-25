import json
import re

from PIL import Image

from .providers import call_gemini


_FEEDBACK_RE = re.compile(r'\{[^{}]*"feedback"[^{}]*\}', re.DOTALL)


def build_reflection_prompt(instruction: str, original_code: str, schema_text: str, out_path: str) -> str:
    prompt = f"""
You are reviewing a chart image against this instruction: {instruction}

Original code that produced the chart:
{original_code}

DataFrame schema:
{schema_text}

Respond in exactly two parts, nothing else:
1. A single-line JSON object: {{"feedback": "critique"}}
2. The improved code, wrapped in:
<execute_python>
#valid python code here
</execute_python>

Requirements:
- Use matplotlin only, assume 'df' already exists, do not read any file.
- Save the figure to '{out_path}' with dpi=300, then call plot.close().
- Include every import statements the code needs
"""
    return prompt.strip()


def parse_feedback(raw: str) -> str:
    match = _FEEDBACK_RE.search(raw)
    if not match:
        return "no Feedback returned"
    try:
        return json.loads(match.group(0))["feedback"]
    except json.JSONDecodeError:
        return match.group(0)


def reflect_and_refine(model: str, chart_path: str, instruction: str, original_code: str, schema_text: str, out_path: str):
    prompt = build_reflection_prompt(instruction, original_code, schema_text, out_path)
    img = Image.open(chart_path)

    response = call_gemini(model, [prompt, img])

    raw = response.text
    return parse_feedback(raw), raw


