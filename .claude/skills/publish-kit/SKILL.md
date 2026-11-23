---
name: publish-kit
description: Stage 7 of the pipeline. Write titles, descriptions, hashtags and pinned comments for YouTube Shorts (English and Hindi) and the Hindi Instagram Reel.
argument-hint: <episode-id>
---

Prepare the publish kit for episode $ARGUMENTS.

1. Read the episode's `02-script.md`, `01-research.md`, the series' `series.md` and `LEARNINGS.md`.
2. Fill in `07-publish.md`:
   - **Platforms:** YouTube Shorts in English (`@thelostgyaan_en`) and Hindi (`@thelostgyaan`); Instagram in **Hindi only** (`@thelostgyaan`). Don't write an English Instagram section, and don't cross-link the two languages in descriptions or captions (no "Watch in English" / "हिंदी में देखें" lines).
   - **Titles:** under 60 characters, built on the curiosity of the hook, and true. No clickbait the video doesn't pay off. All Hindi posting copy (titles, descriptions, captions, hashtags, pinned comments) is in **Roman script (Hinglish)**; the video itself stays in Devanagari.
   - **Descriptions:** a 2-line hook, a 1-line series note, then **Sources** (from the research table) and the series hashtag.
   - **Hashtags:** 3–5 per post (e.g. #Mahabharata #IndianMythology plus a series tag). Keep them consistent across the series. The brand tag is `#TheLostGyaaann` on the Hindi Instagram Reel and `#TheLostGyaan` on YouTube.
   - **Pinned comment:** a question that invites viewers to share their own version or opinion.
   - **Instagram (Hindi):** caption, cover (`render/<ID>-thumb-hi.png` or a timestamp), alt text, audio name and a Story poll.
3. Update Stage in `episodes/INDEX.md` to `7 Ready to publish`.
4. Remind the user to paste the live links into `INDEX.md` after uploading and to fill in `08-review.md` 7 days later.
