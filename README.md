# ADALL_github

Educational notebooks for Applied Data Analytics (ADALL).

## Connect to Claude AI agents from Colab

The course notebooks can call **Claude** (Anthropic) or **OpenAI** from Google Colab using the shared helper [`adall_llm.py`](adall_llm.py).

### 1. Add your API key in Colab Secrets

| Provider | Colab secret name |
|----------|-------------------|
| Claude (default) | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |

Get a Claude key from the [Anthropic Console](https://console.anthropic.com/).

### 2. Enable API cells in the notebook

In the setup cell:

```python
RUN_API_CELLS = True
LLM_PROVIDER = 'claude'   # or 'openai'
```

Run the setup cell before any cell that prints an LLM response.

### 3. Manual mode (no API)

Set `RUN_API_CELLS = False`, copy the printed prompt, and paste it into [Claude](https://claude.ai/) or ChatGPT.

### Local / Cursor testing

```bash
pip install -r requirements-llm.txt
export ANTHROPIC_API_KEY=your_key_here
python -c "from adall_llm import get_llm_client, llm_respond; c=get_llm_client('claude', __import__('os').environ['ANTHROPIC_API_KEY']); print(llm_respond(c,'claude','claude-sonnet-4-5-20250929','Say hello in one sentence.'))"
```
