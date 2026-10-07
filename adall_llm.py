"""Shared LLM helpers for ADALL notebooks (OpenAI and Claude / Anthropic)."""

from __future__ import annotations

from typing import Any, Literal

LLMProvider = Literal["openai", "claude"]

DEFAULT_OPENAI_MODEL = "gpt-5.4-nano"
DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-5-20250929"


def default_model(provider: LLMProvider) -> str:
    if provider == "claude":
        return DEFAULT_CLAUDE_MODEL
    return DEFAULT_OPENAI_MODEL


def get_llm_client(provider: LLMProvider, api_key: str) -> Any:
    """Return an OpenAI or Anthropic client for the given provider."""
    if provider == "claude":
        from anthropic import Anthropic

        return Anthropic(api_key=api_key)

    from openai import OpenAI

    return OpenAI(api_key=api_key)


def llm_respond(client: Any, provider: LLMProvider, model: str, prompt: str) -> str:
    """Send a single user prompt and return the model's text response."""
    if client is None:
        raise ValueError("LLM client is not connected. Set RUN_API_CELLS = True and add your API key.")

    if provider == "claude":
        message = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        parts = []
        for block in message.content:
            if getattr(block, "type", None) == "text":
                parts.append(block.text)
        return "".join(parts)

    response = client.responses.create(model=model, input=prompt)
    return response.output_text


def load_colab_api_key(provider: LLMProvider) -> str:
    """Read the API key from Google Colab Secrets."""
    from google.colab import userdata

    secret_name = "ANTHROPIC_API_KEY" if provider == "claude" else "OPENAI_API_KEY"
    return userdata.get(secret_name)
