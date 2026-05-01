# Publishing this template as a standalone repo

This directory is the source of truth for the `tig-worker-template`
public repository. It currently lives inside the Hive-AI monorepo so the
files stay in sync with the protocol; promote it to its own repo when
the protocol opens to outside miners.

## One-time publish

```bash
# 1. Sync to a fresh clone outside the monorepo.
TARGET=$HOME/projects/tig-worker-template
mkdir -p "$TARGET"
rsync -a --exclude='__pycache__' --exclude='runs/' --exclude='keypair.json' \
    templates/tig-worker/ "$TARGET/"

# 2. Initialize git in the target.
cd "$TARGET"
git init -b main
git add .
git commit -m "feat: initial commit — TIG worker template (mirrored from Hive-AI)"

# 3. Create the GitHub repo + push.
gh repo create Dhenz14/tig-worker-template --public --source=. --push
```

## Keeping in sync after publish

Every time `templates/tig-worker/` changes in this repo, mirror the
update:

```bash
cd $HOME/projects/tig-worker-template
rsync -a --delete \
    --exclude='__pycache__' --exclude='runs/' --exclude='keypair.json' \
    --exclude='.git/' \
    /path/to/Hive-AI/templates/tig-worker/ ./
git add -A
git commit -m "sync: update from Hive-AI@<sha>"
git push
```

A scheduled GitHub Action on the source repo can do this automatically
once the standalone repo exists.
