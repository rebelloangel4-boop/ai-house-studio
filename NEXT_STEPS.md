# Exact continuation

1. Read CONTINUATION_STATE.json and fetch current main. Implementation already committed at ad7decd02c62c44949c83991b6daf5a6d46710e4. Do not rebuild the renderer.
2. Successful baselines: Studio Tests 40590619415 and Studio Production 40590619343. Inspect newer runs only if needed. Existing 001 output is technically verified and retained; do not rerender just to repeat these checks.
3. Obtain explicit Render workspace selection. Available: My Workspace, tea-dbars849v7es739ncpcg. Connector returned no selected workspace and explicitly said to ask the user; do not silently pick it.
4. After confirmation and current Render documentation checks, create a free Python web service: name ai-house-studio, region singapore, repo https://github.com/rebelloangel4-boop/ai-house-studio, branch main, buildCommand "python -m compileall -q production/studio_server.py", startCommand "python production/studio_server.py". No database or paid resources required. Server is stateless.
5. Wait for deployment live, verify HTTPS /healthz and public login shell, unauthorized /api/catalog rejection, manifest and mobile UI. Do not claim live until checked.
6. User enters a fine-grained GitHub token privately in dashboard (only this repository; Actions read/write, Contents read/write). Never request it in chat. Test real authenticated dispatch, persisted calendar, release and backup MP4 previews/downloads, playback and logout. These were previously tested with mocks/fixtures only.
7. Audition the fresh video; technical gates are not proof of naturalness. Preserve creative review pending until performed.
8. Complete genuine AI script generation and creative revisions; current season generator uses authored beats. Add automatic weekly compilation scheduling and authorized publishing only for an explicitly chosen account/destination.
9. Enable the 30-day calendar on appropriate dates after live pipeline acceptance. Currently disabled; no new recurring series or automatic ChatGPT development continuation promised.

Checks: python -m unittest discover -s tests -v; node --check web/app.js; node --check web/sw.js; python tests/browser_smoke.py (requires Playwright Chromium).

Resume: "Resume rebelloangel4-boop/ai-house-studio from CONTINUATION_STATE.json, verify current Actions results, and continue unfinished acceptance criteria without rebuilding the working renderer."
