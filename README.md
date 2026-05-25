# tig-worker — drop-in starter for the Hive-AI TIG protocol

You're a miner. Your job is to write a Python function that beats the
champion on a Hive-AI RAG challenge.

## Quick start (6 commands)

```bash
# 1. Pick a challenge.
hiveai tig list

# 2. Drop the spec + manifest + skeleton into a working dir.
hiveai tig fetch chunking --dest ./my-tig-run

# 3. Edit my_solution.py. The manifest.json tells you the function signature.
$EDITOR ./my-tig-run/my_solution.py

# 4. Score it locally with structured feedback.
hiveai tig rehearse ./my-tig-run/my_solution.py --challenge chunking

# 5. Create (or reuse) your miner identity.
hiveai tig keygen --save ./my-tig-run/keypair.json

# 6. Submit when score >= threshold.
hiveai tig submit ./my-tig-run/my_solution.py \
  --challenge chunking \
  --host https://hiveai.example \
  --key ./my-tig-run/keypair.json
```

## Or let an LLM mine for you

```bash
MODEL=<provider:model> \
hiveai tig auto-mine \
  --challenge chunking \
  --model "$MODEL" \
  --rounds 3 \
  --budget-usd 2.00 \
  --submit
```

The `auto-mine` loop reads the manifest, prompts the model with the
function signature + return shape + last round's feedback, scores the
candidate locally, and iterates. Set `--submit` to push the best one.
The template is BYOM: choose the provider/model string in your local
environment instead of relying on a baked-in hosted model.

## Rules of engagement

- Your candidate file must be ≤ 256 KB.
- It must be a single Python file with the exact function name from the
  manifest (e.g. `chunk_documents`, `refine_embeddings`, ...).
- It runs in a subprocess sandbox with a memory + CPU + wallclock cap.
  No network, no shell, no `os`/`subprocess`/`socket`/`urllib`/`ctypes`.
- It must not use `eval`, `exec`, `compile`, or `__import__`.
- It must not reach for dunders like `__class__.__bases__.__subclasses__`.

If your candidate hits the AST denylist, the rehearse step will tell you
exactly what was blocked and on which line.

## Files in this template

- `manifest.json`        — machine-readable challenge contract
                           (will be filled in by `hiveai tig fetch`)
- `spec.md`              — human-readable challenge spec
- `my_solution.py`       — the file you edit
- `keypair.json`         — your ed25519 identity (after `hiveai tig keygen --save keypair.json`)

## Reward signal

When your candidate is promoted to the frontier, every retrieval that
hits one of your chunks/embeddings/index-deltas counts toward your
champion's reuse counter. The leaderboard surfaces:

- **Submission rank** at this difficulty bucket
- **Times reused** in the live RAG hot path over the last 7 days
- **Retrieval lift** vs the previous champion

That's the reward. No token. Your code is in the brain — that *is* the
payoff.
