# AI HOUSE 2.0 test report

- Repository recovery: real main cloned at ad49ab3872164036e39680158b207b0cb02874dc.
- Existing regression suite: 23/23 unit/API tests passed locally.
- Python compile checks: passed for studio and production/v2.
- Episode 1 voice generation: 9/9 lines passed existing automated speech transcript validation; two Max lines needed retries. This is content validation, not listening approval.
- Episode 1 still preview: all nine shot layouts inspected. Dinosaur moved up to reduce subtitle occlusion.
- Full Episode 1 render and technical video/audio checks: pending at checkpoint.
- Episodes 2–10: scripts and graphics implemented; final MP4 QA not run.
- Audio listening review: NOT PERFORMED. Tool explicitly returned “audio content omitted because you do not support audio input.”
- Cinematic quality, expressive naturalness and accurate phoneme-level lip sync are not certified. Existing mouth animation is approximate, using speech amplitude and word timing.

Extended verifier measures decoded output loudness/true peak, scans black/frozen frames, verifies every scene and subtitle text, full decode, video/audio streams, and presence of effect cue manifests. Technical passing alone never sets Complete=true.
