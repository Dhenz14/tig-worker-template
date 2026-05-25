# TIG Worker Template Contract Receipt - 2026-05-24

## Status
Complete.

## Scope
The standalone `tig-worker-template` repository now reflects its current public
posture, exposes canonical `hiveai.unified_capability.v1` registry contracts,
and keeps `auto-mine` BYOM instead of hardcoding a hosted model.

## Files Changed
- `README.md`
- `PUBLISH.md`
- `Makefile`
- `capabilities.yaml`
- `scripts/check_template_contract.py`

## Commands Run
- `python3 scripts/check_template_contract.py`
- `make check`
- `make auto-mine` without `MODEL` - expected fail-closed exit 2 before invoking `hiveai`.
- Hive-AI local parser smoke via `hiveai.scripts.aggregate_capabilities._parse_yaml_text` - parsed 7 LIVE entries.
- `git diff --check`

## Tests
The guard rejects stale one-time publish instructions, legacy capability fields,
missing canonical TIG surfaces, hardcoded model identifiers, and `auto-mine`
targets that do not fail closed when no model is configured.

## Evidence
Final commit evidence is captured in the operator report for this slice.

## Risks
The Hive-AI monorepo mirror should be updated whenever this standalone template
changes, so both miner entry points stay aligned.
