# AI HOUSE — You Decide

Original 2D interactive roommate comedy with Luna, Max, Zig and one expensive dinosaur.

## What works
- 1080×1920 / 30 fps animated review MP4s, native-resolution character art, expression changes, gestures, blinks and story actions.
- Three Kokoro voices with per-character delivery rates, word-timed captions, approximate phoneme mouth shapes, and silence-aware mouths.
- Original stereo score and effects, dialogue ducking, loudness mastering, SRT and shot previews.
- Technical gates: dimensions, frame rate, codecs, stereo, duration, complete speech, audio clipping, animation changes and full decode.
- Pilot renders on renderer changes. Weekly Studio renders all seven drafts plus connective scenes on production-workflow changes or manual dispatch.
- Daily schedule: 12:47 PM Asia/Kolkata. First prepared week: 19–25 October 2026. Sunday compiles all seven verified daily artifacts into a re-edited story with eight new connective scenes and only one final CTA.

## Publishing is disabled
No YouTube token is read and no upload/publish operation exists. Technical PASS is not creative approval. The owner must approve the actual MP4 before any publishing integration is added.

## Audience choices and continuity
Week one is an editorial draft. No votes have been collected or counted. The six follow-up scripts explore the dinosaur's trial week without claiming a winning poll result. Before preparing the next pack, record real viewer decisions with source video/comment IDs and a cutoff; never invent a result. The current schedule stops producing after 25 October rather than recycling the same seven episodes. A new pack and its editorial review are required for future weeks.

## Zero-budget boundary
Uses standard Ubuntu runners on this public repository and free local inference; no paid services, larger runners or paid TTS. Individual artifacts are capped at 20 MB, compilation at 80 MB; retention is eight days (pilot two days). Actual account-wide storage and GitHub service policies still govern billing. Do not enable paid spending or change to a paid runner. No model cache is retained in Actions.

## Commands
- `python studio/render.py --episode 001` then `python studio/verify.py output/001`
- `python studio/render.py --episode 001 --preview` for still layout review
- `python production/schedule_pack.py --batch` for first-week render matrix
- `python production/collect.py` with the job-scoped GitHub token to fetch this pack's verified source artifacts
- `python production/compile_week.py` to re-edit the weekly MP4

See LICENSES.md for provenance. Video exports and model caches are excluded from Git.
