# Connect the XA XAUUSD EA project (for Claude + Cursor team)

The **XA gold EA** is separate from the ADALL course notebooks in this repo.  
Cursor Cloud Agents only see files that are **in the git repo** or **downloaded into the workspace**.

## Option A — GitHub (recommended for the team)

1. Create or use a repo that contains your EA tree, for example:
   - `XA_FRAMA_Band_Scalper.mq5`
   - `team/ACCESS_TEST.md`
   - `team/inbox/`
   - `.cursorignore`
2. In **Cursor → Cloud Agent → Environment**, add that repository (or run agents only on that repo).
3. Push your half-finished work; agents can then read/write on a branch.

## Option B — Google Drive shared folder

1. In Drive, open the **XA EA project folder** → Share → **Anyone with the link** (Viewer is enough for download).
2. Copy the folder ID from  
   `https://drive.google.com/drive/folders/<FOLDER_ID>`
3. On your machine or in a one-off Colab cell:

```bash
pip install gdown
export GOOGLE_DRIVE_XA_EA_FOLDER_ID="<FOLDER_ID>"
python scripts/sync_xa_ea_from_drive.py
```

4. Commit the synced tree to GitHub (without secrets — keep `.env` and `*.session` out of git).

## Option C — Colab + Drive mount (manual)

If the project lives in `My Drive/XA`:

```python
from google.colab import drive
drive.mount('/content/drive')
# Copy the folder into Drive or zip and upload to GitHub
```

## Working with Claude AI

- Use **`ANTHROPIC_API_KEY`** in Colab Secrets or locally; team prompts can reference `adall_llm.py`-style helpers in the EA repo once connected.
- Do **not** commit API keys, Telegram bot tokens, or `.session` files. Use `.cursorignore` in the EA repo.

## Current agent limitation

This run was started on **`theezen/ADALL_github`**, which does **not** contain the EA sources.  
Status report: [`team/inbox/cursor_status.md`](../team/inbox/cursor_status.md).
