# S01E01: The Sage Who Put Dharma on Trial

- **Series:** S01 Shraap: Curses That Shaped the Mahabharata (pilot)
- **Idea (one line):** Sage Mandavya is impaled on a stake for a theft he didn't commit. He survives, demands to know why from Dharma (god of justice), learns it was for hurting an insect as a child, and curses Dharma to be born on Earth as a human. Dharma becomes Vidura. (Note: the epic says Dharma, not Yama; see 01-research.md.)
- **Why it will work:** The reversal: a mortal puts the God of Justice on trial and wins. It raises a question of justice (is punishment fair for something done as a child?), and the payoff turns a famous Mahabharata figure (Vidura) into a god in disguise. Only 2 main characters, so it's cheap to make for a pilot.
- **Created:** 2026-11-07

## Status
- [x] 1 Research (verified by me)
- [x] 2 Script (read aloud, EN + HI)
- [x] 3 Storyboard
- [x] 4 Assets
- [x] 5 Voice
- [~] 6 Render (rendered; phone GATE pending)
- [ ] 7 Published (links in INDEX.md)
- [ ] 8 Reviewed (7 days after upload)

## Open items (as of 2026-11-07)
- [ ] **Hindi length:** 73.3 s (target ≤ 60). Decide: tighten the Hindi script (beats 1, 5, 13, 14; cuts listed in 02-script.md) and regenerate (~900 credits), speed up ~15%, or keep it.
- [x] **Detailed cast** (2026-11-08): all 8 characters redrawn as detailed rigs, reviewed (04-asset-review.md), filed and re-rendered in EN + HI.
- [x] **Vultures redo** (2026-11-08): v3 approved and filed, finals re-rendered.
- [ ] **Sound:** studio mixing built and the plan is in `03-scenes.json`; the ElevenLabs music + 12 SFX still need generating (node IDs under Production facts).
- [ ] **GATE 6:** watch `render/S01E01-en.mp4` and `render/S01E01-hi.mp4` on a phone, sound on and off.
- [ ] **Stage 7:** `/publish-kit S01E01`.
- Optional: exact word timings via a Scribe transcript (`/voice` step 3) if any cue feels early or late.

## Production facts
- ElevenLabs flow: `mXxKe7kyijEYkNRdeVEX` (EN take on node `I8bjDMpCAxJDUqf65wOi`, HI on `rZi70Sd82Y7mVNDNu33K`). Voice `5gaEGrWSk4v20HMfIhgC`, model `eleven_v4`. Spend so far: 1,679 credits.
- **Sound pass (set up 2026-11-08, not generated yet):** plan in `03-scenes.json` (`sound` + per-scene `sfx`/`music`), mixed by `studio/src/components/Sound.tsx`. Files go to `assets/music/<id>.mp3` and `assets/sfx/<id>.mp3`. Nodes on flow `mXxKe7kyijEYkNRdeVEX` (params set; run them one at a time): music `mythic-drone` `eIZrmbwcLr6OwERKALWG` (75 s, instrumental, ~900 cr); sfx (~50 cr each): drum-hit `zQwAj7j0yLGU3iPUgKyd`, stamp-thud `AZfENb9IzVOKlyEzFk9h`, gong-soft `Sbn53f70tw5rs8O81Bj3`, coins-spill `Y95AEpFOHs4MXs4756Is`, drum-boom-deep `Me0GiuQJbg5HZB24lQix`, wind-desolate `pMPrk9OkPAnGNBImBcMy`, heartbeat `nIqsy00VFiRshqMl0jxQ`, scale-clank-boom `AOMoDnhkG2cj2lXpEJak`, thunder-crack `PNKiYNL8MVLu6XApaikI`, glass-crack `OXvfRHs1DVsFg26LGX7Y`, shimmer-descend `XSVtDmyBg6PBpx9Z232Q`, bowstring-creak `C37Hgdh8gZvDgRjP2zS7`. Approved spend: ~1,500 credits. **Done:** bowstring-creak (20 cr, filed to `assets/sfx/`). The other 12 hit the busy free queue (not charged); run them in one call, failed nodes cost nothing.
- Takes are kept in `audio/<lang>.take.mp3`; aligned audio and timestamps in `audio/<lang>.mp3` / `.timestamps.json`.
