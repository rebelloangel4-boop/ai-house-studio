# Exact continuation — AI HOUSE 2.0

1. Read PRODUCTION_MANIFEST.json and inspect output/201 for actual final media and qa.json. Do not rerender valid checkpoints unnecessarily.
2. Environment used: /tmp/aihouse-venv, CPU torch 2.6.0, production/voice-requirements.txt plus socksio for the current proxy. Recreate if missing. Set HF_HUB_DISABLE_XET=1 where needed.
3. Run `python production/v2/run.py --episode 201`. This renders the complete first episode, then runs baseline and extended technical checks. Each scene/voice has a cache; retries are bounded.
4. Inspect the actual rendered scenes and ending. Audio-capable review must assess voice naturalness, pacing, lip sync, and mix quality; this session cannot consume audio input. Never mark that review PASS based on ASR.
5. After Episode 1 technical verification, continue sources 202–210 independently. Preserve output and inspect every episode. Revise overlong dialogue instead of truncating it.
6. Generate thumbnails/upload metadata with license attribution. Retain individual MP4s on GitHub releases or approved storage; do not supply ZIP-only delivery. Only verified final outputs get final approval; QA-pending candidates must be clearly labeled.
7. Run `python production/v2/checkpoint.py` after each milestone and update these documents with actual results. No future background execution is promised without a live job.

Do not overwrite episodes 001–034, change established voices, enable paid runners/services, send files to Drive, or publish to YouTube.
