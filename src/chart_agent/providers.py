import os

from google import genai
from google.genai import errors
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


def get_gemini_client() -> genai.Client:
    # reads the key from the .env
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not set")

    return genai.Client(api_key=api_key)


@retry(
    retry=retry_if_exception_type(errors.ServerError),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    stop=stop_after_attempt(4),
    reraise=True,
)
def call_gemini(model: str, contents):
    """Call Gemini's generate_content, retrying on transient server errors (e.g. 503)."""
    client = get_gemini_client()
    return client.models.generate_content(model=model, contents=contents)


def generate_text(model: str, prompt: str) -> str:
    return call_gemini(model, prompt).text
