# XA gold EA — Cursor build agent read-only status

**Role:** Build agent (read-only round)  
**Team lead:** Claude  
**Workspace repo:** `theezen/ADALL_github`  
**Date:** 2026-10-07 (UTC)

**Rules observed:** No code changes. Did not open `.env`, `*.session`, or key files. No EA source contents read (EA tree absent).

---

## 1. `team/ACCESS_TEST.md` marker

**UNVERIFIED** — `team/ACCESS_TEST.md` **not found** in this workspace. Marker cannot be quoted.

---

## 2. All `.mq5` / `.mqh` files (name and size in bytes)

**UNVERIFIED** — no `.mq5` or `.mqh` files under the workspace root (EA project folder not present).

| File | Size (bytes) |
|------|-------------:|
| *(none found)* | — |

---

## 3. `XA_FRAMA_Band_Scalper.mq5`

**UNVERIFIED** — file **not found**.

| Check | Result |
|--------|--------|
| Header version line | **UNVERIFIED** |
| Contains `RequireM5` | **UNVERIFIED** |
| Contains `StatusEveryBars` | **UNVERIFIED** |
| Size (bytes) | **UNVERIFIED** |
| Placeholder vs real EA | **UNVERIFIED** |

---

## 4. Scan for API keys, bot tokens, session files

**EA project folder:** **UNVERIFIED** — scan not run (no EA tree).

**This workspace (course/helper repo only, not the EA):**

| Item | Result |
|------|--------|
| `.env` / `.env.*` files | None found (by filename) |
| `*.session` files | None found (by filename) |

No EA-related secret-bearing filenames detected. A full content scan for the XA EA codebase is **UNVERIFIED** until the project is synced.

---

## 5. `.cursorignore`

**UNVERIFIED for EA project** — no `.cursorignore` at workspace root.

Patterns: **N/A** (file missing).

---

## Summary

The **XA XAUUSD EA** sources (`ACCESS_TEST`, `XA_FRAMA_Band_Scalper.mq5`, includes) are **not in this agent workspace**. Connect via GitHub repo or shared Google Drive folder (see `docs/CONNECT_XA_EA_PROJECT.md`), then re-run this checklist.

**STOP** — awaiting next instruction.
