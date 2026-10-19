# AI HOUSE asset provenance

- Characters, apartment, dinosaur, props, animation and scripts: original work created for this repository. No stock clips, franchise characters or copied scripts.
- Music and effects: original procedural synthesis in studio/render.py. No sampled recordings, commercial music or third-party sound libraries.
- Speech: hexgrad/Kokoro-82M, Apache-2.0 model weights. Voices af_heart, am_michael and am_fenrir from that model repository; no user-supplied voice clones. Sources: https://huggingface.co/hexgrad/Kokoro-82M and https://github.com/hexgrad/kokoro. Model card checked 2026-10-18. Retain upstream notices if redistributing model files; this repository does not redistribute model weights.
- Typeface: DejaVu Sans Bold from fonts-dejavu-core. Bitstream Vera / DejaVu font license permits use in rendered media. Source: https://dejavu-fonts.github.io/License.html. The runner's installed package retains the font license.
- Software dependencies are installed from their upstream distributions, retaining their own licenses. No paid APIs, proprietary demo endpoints, scraped voice services or noncommercial-only checkpoints.

Commercially usable inputs do not guarantee YouTube monetization or clearance in every jurisdiction. Editorial review remains required. Do not use another person's voice or likeness without authorization.

## Week 1 replacement voice test (2026-10-19)
- Engine: Pocket TTS 3.3.0, https://github.com/kyutai-labs/pocket-tts (MIT software). Current model card https://huggingface.co/kyutai/pocket-tts lists CC BY 4.0; credit Kyutai, Manu Orsini, Simon Rouard, Gabriel De Marmiesse, Václav Volhejn, Neil Zeghidour and Alexandre Défossez. Model weights are downloaded, not redistributed here.
- Luna: `alba`, the casual character performance by Alba MacKenna, released for reuse under CC BY 4.0. Credit Alba MacKenna / Kyutai TTS voices; https://huggingface.co/kyutai/tts-voices/blob/main/alba-mackenna/casual.wav . Generated dialogue is synthetic and is not a recording of the performer.
- Max: `marius`, donated preset Selfie; Zig: `javert`, donated preset Butter. Kyutai's verified voice-donation collection is CC0. Source and permission statement: https://huggingface.co/kyutai/tts-voices . Only these provided, licensed presets are used; no arbitrary voice impersonation.
- Attribution license: https://creativecommons.org/licenses/by/4.0/ . The source voices are transformed into synthetic character dialogue. Keep this attribution with published videos. Noncommercial Expresso and EARS voices are explicitly excluded.
- Transcription: faster-whisper 1.2.1 / Whisper base.en for automated word checks and timing. Transcript agreement and signal checks are NOT human listening approval or a naturalness score.
- Standard ubuntu-24.04 public-repository runners only; no API credits, paid runners, subscriptions, or model caches. Account-wide artifact usage cannot be read through the current connector. Review artifacts expire after eight days.
