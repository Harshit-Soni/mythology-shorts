# Voice Direction: X001

**Voice:** ElevenLabs `5gaEGrWSk4v20HMfIhgC` (the channel narrator, PIPELINE.md Stage 5), same voice for EN and HI.
**Generate each language as ONE full take** (the beats as paragraphs), not beat by beat. A single take keeps the emotional arc flowing across the story; beat-by-beat clips reset the pitch each time and sound flat. The renderer aligns the take to the beats afterwards (`voice:import … auto`, or a Scribe transcript for exact word times).

**Settings (expressive storyteller, not newsreader):**
| Setting | Value | Why |
|---|---|---|
| Stability | **0.30–0.40** | Lower = more pitch movement and emotion (the draft was monotone) |
| Similarity | 0.75 | Keeps the narrator's identity |
| Style exaggeration | **0.35–0.50** | Adds dramatic colour; above ~0.6 it starts to wobble |
| Speaker boost | on | |
| Speed | **0.95** EN · **0.92** HI | Room for the pauses; check the total stays ≤ 60 s |

**The arc:** quiet mystery → wonder → playful tension (the test) → dread (the realisation) → hush (the sacrifice) → awe and warmth (the ending). The lowest, quietest moment is beat 11; the warmest is beat 14.

## Takes used (2026-11-08)
| Lang | Model / voice | Raw take | Fit | Final | Alignment |
|---|---|---|---|---|---|
| EN | eleven_v4 · 5gaEGrWSk4v20HMfIhgC, direction tags (no voice_settings on v4) | `audio/takes/en.eleven-v4.take.mp3` 60.7 s | `atempo 1.025` (pitch kept) | 59.6 s | `voice:import … auto`, all 14 beats within ~1 s of expected |
| HI | same | `audio/takes/hi.eleven-v4.take.mp3` 63.4 s | `atempo 1.06` (pitch kept) | 60.2 s | same |

Notes: eleven_v4 has no stability/style/speed settings; delivery comes from the inline tags (`[softly]`, `[whispers]`, `[pause]`, `[tenderly]`, `[warmly] [slowly]`…). Trimming pauses by hand broke the pause-based auto alignment; a small uniform tempo lift keeps pause proportions, so alignment holds. The free-tier queue was busy for ~6 attempts (no charge); the takes cost 1,092 (EN) + 993 (HI) credits.

### Beat 9 correction (2026-11-10)
The first takes said "the side he joined would start **losing**", which is backwards. New beat 9 lines were generated alone (eleven_v4, same voice, `[gravely]`; 110 + 106 credits) and spliced into the raw takes at the pauses on either side (EN 34.90→41.05 s, HI 35.64→42.39 s), loudness-matched (EN +1.5 dB, HI −1.9 dB). Files: `audio/takes/<lang>.beat9.v2.mp3`, `<lang>.eleven-v4.spliced.mp3`. Fit: EN `atempo 1.03` → video 60.0 s; HI `atempo 1.075` → video 60.9 s.

## Beat-by-beat delivery
Pauses: `…` ≈ 0.6–0.8 s, a paragraph break ≈ 0.5 s. **Bold** = stress the word. ↗ rising pitch, ↘ falling pitch.

| # | Line (EN) | Delivery |
|---|---|---|
| 1 | One warrior could have ended the Mahabharata war… with **three arrows**. | Low, intimate, slow. A real pause after "war…", then drop the voice on "three arrows" ↘, like a secret |
| 2 | In the Khatu telling, Bhima's grandson **Barbarika** won three unfailing arrows from the **goddess**. | Warm storyteller; lift ↗ on "Barbarika", reverent on "goddess" |
| 3 | And he vowed… to **always** fight for the **losing** side. | Proud, firm. Small pause after "vowed"; lean on "always" |
| 4 | Before the war, an old Brahmin stopped him under a peepal tree. | Lighter, a touch of mystery; slightly quicker, scene-setting |
| 5 | "Three arrows? **Pierce every leaf** of this tree." | Character voice: an old man, amused and teasing. Rising doubt on "Three arrows?" ↗ |
| 6 | Secretly… he hid **one leaf** underfoot. | Conspiratorial, almost a whisper. Pause after "Secretly…" |
| 7 | One arrow marked **every** leaf… then **circled his foot**. | Building wonder, pace picks up, then slow down on "circled his foot" |
| 8 | The Brahmin was **Krishna**… and he saw the **danger** in that vow. | The reveal: a beat before "Krishna", said with awe. Darker, lower on "danger" |
| 9 | Any side he joined would start **winning**… so he'd have to switch, until **both armies** were gone. | Grave, deliberate, slower. A long pause before "until no one was left" ↘ |
| 10 | So Krishna asked a gift: "**Your head.**" | Soft and heavy. Pause after "gift:"; "Your head" gentle, not cruel |
| 11 | He bowed. "It's yours. Just let me **watch the war**." | **The quietest moment.** Calm acceptance, no drama, almost tender. Pause after "He bowed." |
| 12 | From a hilltop, his head watched all **eighteen days**. | Awe, opening up; brighter, steady |
| 13 | Krishna blessed him: "You'll be worshipped by my name… **Shyam**." | Warm and blessing-like. A small pause before "Shyam", held slightly |
| 14 | Today he's **Khatu Shyam**: the support of those who **lose**. | Warmest line. Slow, a smile in the voice; let "those who lose" land and fade ↘ |

## हिंदी: delivery notes
Same arc and the same pauses. Hindi needs **clear consonants** and natural intonation, not a translated rhythm:
- **1:** "एक योद्धा… जो **तीन बाणों** से महाभारत ख़त्म कर सकते थे…": hushed, with a pause after "योद्धा…"
- **5:** "तीन बाण? इस पेड़ का **हर पत्ता** भेदो।": playful, an old man's voice
- **8:** "ब्राह्मण… स्वयं **कृष्ण** थे": a pause before "स्वयं कृष्ण", then reverence
- **10:** "अपना **शीश**।": soft, heavy
- **11:** "ले लीजिए… बस युद्ध देखने दीजिए।": the quietest, most tender line
- **14:** "आज वही हैं **खाटू श्याम**… **हारे का सहारा**।": warm devotion, a slight pause before "हारे का सहारा"
- Pronunciation: बर्बरीक (bar-ba-reek), शीश (sheesh), श्याम (shyaam), अचूक (a-chook), प्रण (pran)

## Take text
Paste exactly (paragraph = beat). Keep the words identical to `02-script.md` so alignment works; only the `…` pauses are added.

### EN
```
One warrior could have ended the Mahabharata war… with three arrows.

In the Khatu telling, Bhima's grandson Barbarika won three unfailing arrows from the goddess.

And he vowed… to always fight for the losing side.

Before the war, an old Brahmin stopped him under a peepal tree.

"Three arrows? Pierce every leaf of this tree."

Secretly… he hid one leaf underfoot.

One arrow marked every leaf… then circled his foot.

The Brahmin was Krishna… and he saw the danger in that vow.

Whichever side he joined would start losing. He'd switch sides… until no one was left.

So Krishna asked a gift: "Your head."

He bowed. "It's yours. Just let me watch the war."

From a hilltop, his head watched all eighteen days.

Krishna blessed him: "You'll be worshipped by my name… Shyam."

Today he's Khatu Shyam: the support of those who lose.
```

### HI
```
एक योद्धा… जो तीन बाणों से महाभारत ख़त्म कर सकते थे…

खाटू की कथा में, भीम के पोते बर्बरीक को देवी से तीन अचूक बाण मिले।

और उन्होंने प्रण लिया: हमेशा हारने वाले का साथ दूँगा।

युद्ध से पहले, पीपल के नीचे एक बूढ़े ब्राह्मण ने उन्हें रोका।

"तीन बाण? इस पेड़ का हर पत्ता भेदो।"

और चुपके से… एक पत्ता पैर तले दबा लिया।

बाण ने हर पत्ता भेदा… फिर पैर के चारों ओर घूमने लगा।

ब्राह्मण… स्वयं कृष्ण थे, और उन्हें उस प्रण में ख़तरा दिखा।

बर्बरीक जिस पक्ष में जाते, वही हारने लगता। पक्ष बदलते-बदलते… कोई न बचता।

तो कृष्ण ने दान माँगा: "अपना शीश।"

बर्बरीक ने सिर झुकाया: "ले लीजिए… बस युद्ध देखने दीजिए।"

पहाड़ी से उनके शीश ने, अठारह दिन का युद्ध देखा।

कृष्ण का वरदान: "कलियुग में तुम मेरे नाम, श्याम से पूजे जाओगे।"

आज वही हैं खाटू श्याम… हारे का सहारा।
```

## After the take
1. Check the length: **≤ 60 s** for each language. If it's over, use the ready cuts in `02-script.md`, not a faster speed (speed kills the feeling).
2. Import it: `npm run voice:import -- X001 en take-en.mp3 auto` (and `hi`). The import prints each beat's span; check none is badly off.
3. Re-render: `npm run render -- X001 en --final` and `hi`.
