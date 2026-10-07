#!/usr/bin/env python3
"""Patch ADALL notebooks to support Claude alongside OpenAI."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SETUP_OLD = """# Default method: copy the prompt into the chatbot manually.
RUN_API_CELLS = False
OPENAI_MODEL = 'gpt-5.4-nano'
client = None

# Only use this section if your tutor has asked you to call the API from Colab.
# You must first save OPENAI_API_KEY in Colab Secrets.

if RUN_API_CELLS == True:
    from google.colab import userdata
    from openai import OpenAI

    api_key = userdata.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    print('OpenAI client is ready.')
else:
    print('Manual chatbot mode. Copy the prompts when they appear.')

# This cell prepares the notebook to use the OpenAI API, if needed.
# RUN_API_CELLS controls whether the notebook uses the API or manual chatbot mode.
# If RUN_API_CELLS is True, the notebook will try to connect to OpenAI using an API key.
# If RUN_API_CELLS is False, students can copy the prompt and paste it into ChatGPT manually.
# OPENAI_MODEL stores the model name that will be used later when sending prompts.
# client starts as None first, then becomes an OpenAI client after the API key is loaded.
# userdata.get('OPENAI_API_KEY') reads the API key saved in Colab Secrets.
# OpenAI(api_key=api_key) creates the connection object used to call the API."""

SETUP_NEW = """# Default method: copy the prompt into the chatbot manually.
RUN_API_CELLS = False
# LLM_PROVIDER: 'claude' (Anthropic) or 'openai'
LLM_PROVIDER = 'claude'
OPENAI_MODEL = 'gpt-5.4-nano'
CLAUDE_MODEL = 'claude-sonnet-4-5-20250929'
client = None
LLM_MODEL = None

# Only use this section if your tutor has asked you to call the API from Colab.
# Save ANTHROPIC_API_KEY (Claude) or OPENAI_API_KEY in Colab Secrets.

if RUN_API_CELLS == True:
    import urllib.request
    urllib.request.urlretrieve(
        'https://raw.githubusercontent.com/theezen/ADALL_github/main/adall_llm.py',
        'adall_llm.py',
    )
    from adall_llm import get_llm_client, load_colab_api_key

    api_key = load_colab_api_key(LLM_PROVIDER)
    client = get_llm_client(LLM_PROVIDER, api_key)
    LLM_MODEL = CLAUDE_MODEL if LLM_PROVIDER == 'claude' else OPENAI_MODEL
    print(f'{LLM_PROVIDER} client is ready. Model: {LLM_MODEL}')
else:
    print('Manual chatbot mode. Copy the prompts when they appear.')

# RUN_API_CELLS: API from Colab vs manual paste into Claude.ai or ChatGPT.
# LLM_PROVIDER selects Anthropic (Claude agents) or OpenAI."""

RESPONSE_BLOCK_OLD = """if client is not None:
    response = client.responses.create(
        model=OPENAI_MODEL,
        input="""

RESPONSE_BLOCK_NEW = """if client is not None:
    from adall_llm import llm_respond
    llm_output = llm_respond(client, LLM_PROVIDER, LLM_MODEL, """

# Week 5 step 3 setup (RUN_API_CELLS = True by default)
W5_SETUP_OLD = """RUN_API_CELLS = True
OPENAI_MODEL = 'gpt-5.4-nano'
client = None

if RUN_API_CELLS == True:
    from google.colab import userdata
    from openai import OpenAI

    api_key = userdata.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    print('OpenAI client is ready.')
else:
    print('Manual chatbot mode. Copy the prompt above into your chatbot.')"""

W5_SETUP_NEW = """RUN_API_CELLS = True
LLM_PROVIDER = 'claude'
OPENAI_MODEL = 'gpt-5.4-nano'
CLAUDE_MODEL = 'claude-sonnet-4-5-20250929'
client = None
LLM_MODEL = None

if RUN_API_CELLS == True:
    import urllib.request
    urllib.request.urlretrieve(
        'https://raw.githubusercontent.com/theezen/ADALL_github/main/adall_llm.py',
        'adall_llm.py',
    )
    from adall_llm import get_llm_client, load_colab_api_key

    api_key = load_colab_api_key(LLM_PROVIDER)
    client = get_llm_client(LLM_PROVIDER, api_key)
    LLM_MODEL = CLAUDE_MODEL if LLM_PROVIDER == 'claude' else OPENAI_MODEL
    print(f'{LLM_PROVIDER} client is ready. Model: {LLM_MODEL}')
else:
    print('Manual chatbot mode. Copy the prompt above into your chatbot.')"""


def patch_source(source: str) -> tuple[str, bool]:
    changed = False
    if SETUP_OLD in source:
        source = source.replace(SETUP_OLD, SETUP_NEW)
        changed = True
    if W5_SETUP_OLD in source:
        source = source.replace(W5_SETUP_OLD, W5_SETUP_NEW)
        changed = True

    # Week 4 style setup (slightly different else branch)
    w4_old = W5_SETUP_OLD.replace(
        "print('Manual chatbot mode. Copy the prompt above into your chatbot.')",
        "print('Manual chatbot mode.')",
    )
    if w4_old in source:
        source = source.replace(
            w4_old,
            W5_SETUP_NEW.replace(
                "print('Manual chatbot mode. Copy the prompt above into your chatbot.')",
                "print('Manual chatbot mode.')",
            ),
        )
        changed = True

    pattern = re.compile(
        r"if client is not None:\n"
        r"    response = client\.responses\.create\(\n"
        r"        model=OPENAI_MODEL,\n"
        r"        input=([^\)]+)\n"
        r"    \)\n"
        r"    print\('\\nLLM response:'\)\n"
        r"    print\(response\.output_text\)",
        re.MULTILINE,
    )

    def repl(m: re.Match) -> str:
        var = m.group(1).strip()
        return (
            f"if client is not None:\n"
            f"    from adall_llm import llm_respond\n"
            f"    print('\\nLLM response:')\n"
            f"    print(llm_respond(client, LLM_PROVIDER, LLM_MODEL, {var}))"
        )

    new_source, n = pattern.subn(repl, source)
    if n:
        source = new_source
        changed = True

    # response2 blocks (Week 4)
    pattern2 = re.compile(
        r"    response2 = client\.responses\.create\(\n"
        r"        model=OPENAI_MODEL,\n"
        r"        input=([^\)]+)\n"
        r"    \)\n"
        r"    print\('\\nLLM response:'\)\n"
        r"    print\(response2\.output_text\)",
        re.MULTILINE,
    )

    def repl2(m: re.Match) -> str:
        var = m.group(1).strip()
        return (
            f"    from adall_llm import llm_respond\n"
            f"    print('\\nLLM response:')\n"
            f"    print(llm_respond(client, LLM_PROVIDER, LLM_MODEL, {var}))"
        )

    new_source, n2 = pattern2.subn(repl2, source)
    if n2:
        source = new_source
        changed = True

    # Standalone response = client.responses.create (practice cells)
    pattern3 = re.compile(
        r"response = client\.responses\.create\(\n"
        r"    model=OPENAI_MODEL,\n"
        r"    input=([^\)]+)\n"
        r"\)\n\n"
        r"print\(response\.output_text\)",
        re.MULTILINE,
    )

    def repl3(m: re.Match) -> str:
        var = m.group(1).strip()
        return (
            f"from adall_llm import llm_respond\n"
            f"print(llm_respond(client, LLM_PROVIDER, LLM_MODEL, {var}))"
        )

    new_source, n3 = pattern3.subn(repl3, source)
    if n3:
        source = new_source
        changed = True

    # Markdown: OpenAI API -> LLM API
    if "### Optional: use the OpenAI API" in source:
        source = source.replace(
            "### Optional: use the OpenAI API",
            "### Optional: use the Claude or OpenAI API",
        )
        changed = True
    if "###<font color='blue'>Lets try with OpenAI </font>" in source:
        source = source.replace(
            "###<font color='blue'>Lets try with OpenAI </font>",
            "###<font color='blue'>Lets try with Claude or OpenAI </font>",
        )
        changed = True

    return source, changed


def patch_notebook(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    any_changed = False
    for cell in data.get("cells", []):
        if cell.get("cell_type") != "code":
            src = "".join(cell.get("source", []))
            new_src, changed = patch_source(src)
            if changed:
                cell["source"] = [new_src] if not new_src.endswith("\n") else [new_src]
                # preserve list-of-lines format
                if isinstance(cell.get("source"), list) and len(cell["source"]) > 1:
                    cell["source"] = [line + "\n" for line in new_src.splitlines(keepends=True)]
                    if cell["source"] and not cell["source"][-1].endswith("\n"):
                        cell["source"][-1] += "\n"
                any_changed = True
            continue

        lines = cell.get("source", [])
        if isinstance(lines, list):
            src = "".join(lines)
        else:
            src = lines
        new_src, changed = patch_source(src)
        if changed:
            cell["source"] = [line + "\n" for line in new_src.splitlines(keepends=True)]
            if cell["source"] and cell["source"][-1] == "\n":
                pass
            elif cell["source"] and not cell["source"][-1].endswith("\n"):
                cell["source"][-1] += "\n"
            any_changed = True

    if any_changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return any_changed


def main() -> None:
    for path in sorted(ROOT.glob("*.ipynb")):
        if patch_notebook(path):
            print(f"Patched {path.name}")
        else:
            print(f"No changes {path.name}")


if __name__ == "__main__":
    main()
