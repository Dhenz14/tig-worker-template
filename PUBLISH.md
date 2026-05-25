# Publishing and Sync Policy

`Dhenz14/tig-worker-template` is already the public standalone repository for
the TIG worker starter. Treat this repo as the source of truth for outside
miners. The Hive-AI monorepo may keep a mirrored `templates/tig-worker/` copy
for local development, but public-facing template changes should land here
first or be mirrored here immediately in the same release slice.

## Release Update

Use a fresh clone or clean worktree, run the template checks, and push to
`main` only after the contract is green:

```bash
git clone https://github.com/Dhenz14/tig-worker-template.git
cd tig-worker-template
python3 scripts/check_template_contract.py
git status --short
```

If a Hive-AI monorepo change updates `templates/tig-worker/`, mirror that exact
change back into this repo from a reviewed checkout:

```bash
rsync -a --delete \
  --exclude='.git/' \
  --exclude='__pycache__' \
  --exclude='runs/' \
  --exclude='keypair.json' \
  /path/to/Hive-AI/templates/tig-worker/ ./
python3 scripts/check_template_contract.py
git diff --check
git add -A
git commit -m "sync: update TIG worker template from Hive-AI@<sha>"
git push origin main
```

## Local Secrets

Never commit `keypair.json`, run outputs, local provider tokens, or model
credentials. The `auto-mine` path is BYOM; pass the model identifier through
`MODEL=<provider:model>` or `HIVEAI_TIG_MODEL`, and keep provider credentials in
your local environment.
