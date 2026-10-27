# Verified tests — 2026-10-28 IST

- 7 original tests passed before modifications.
- 23 local unit/API tests passed after modifications, covering speech pacing/alignment, auth rejection, permission checks, validated render/weekly dispatch, calendar persistence using SHA, direct media responses, backup extraction and bounded retries. GitHub calls are mocked in API tests.
- JavaScript syntax and Python compile checks passed.
- Local opening-frame render executed and inspected; existing art preserved.
- GitHub Studio Tests 40590619415 passed all 23 tests and Chromium checks at 390x844 and 1280x800. Real unauthenticated API denial tested; signed-in UI uses fixtures. Mobile screenshot downloaded and inspected.
- First fresh production run 40590203646: render/verification PASS, release FAIL HTTP 403.
- Repaired production run 40590619343: SUCCESS, including rendering, verification, artifact backup and draft release with MP4 plus metadata and QA files.
- Fresh MP4 downloaded via backup artifact 12773218342; ffprobe confirmed H.264 1080x1920 30fps, AAC stereo 48000Hz, 19.013s, 1729898 bytes. Local full-decode exit status unavailable because environment disconnected. Workflow full-decode gate passed.
- Naturalness listening, real Android installation, deployed health and authenticated dashboard end-to-end interactions NOT verified. No social publishing test performed.
