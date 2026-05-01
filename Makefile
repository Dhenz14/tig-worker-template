# tig-worker quick targets
#
# Override the challenge with: make CHALLENGE=embedding rehearse

CHALLENGE ?= chunking
HOST ?= http://127.0.0.1:5000

.PHONY: help fetch rehearse submit auto-mine keygen leaderboard

help:
	@echo "tig-worker targets (CHALLENGE=$(CHALLENGE)):"
	@echo "  make fetch          — drop spec/manifest/skeleton for $(CHALLENGE)"
	@echo "  make rehearse       — score my_solution.py locally"
	@echo "  make submit         — sign + send my_solution.py to $(HOST)"
	@echo "  make auto-mine      — let an LLM iterate on a candidate"
	@echo "  make keygen         — generate ed25519 keypair into keypair.json"
	@echo "  make leaderboard    — show frontier for $(CHALLENGE)"

fetch:
	hiveai tig fetch $(CHALLENGE) --dest .

rehearse:
	hiveai tig rehearse my_solution.py --challenge $(CHALLENGE)

submit:
	hiveai tig submit my_solution.py --challenge $(CHALLENGE) --host $(HOST) --key keypair.json

auto-mine:
	hiveai tig auto-mine --challenge $(CHALLENGE) --model claude:opus-4-7 --rounds 3 --dest .

keygen:
	hiveai tig keygen --save keypair.json

leaderboard:
	hiveai tig leaderboard $(CHALLENGE)
