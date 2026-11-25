# Voice Direction: S01E06 v2

**v2 script (2026-11-25).** v1 takes and prompts: `review/audio-v1/`, `review/05-voice-direction-v1.md`.

**Voice:** ElevenLabs `5gaEGrWSk4v20HMfIhgC`, model `eleven_v4` (PIPELINE.md Stage 5), the same narrator for EN and HI. One full take per language, with the beats as paragraphs. The delivery comes from the inline tags.
**ElevenLabs flow:** `NvM1H2Qyly5DBYGmdnbi` (the series flow).
**Word times:** always a Scribe transcript, never `auto` (LEARNINGS → Voice).

**The arc:** a strange fact → a humble man → wonder at a power → menace → a calm trap → pride → the curse → begging, and mercy → ages later, a fight → a weary voice asking → a quiet answer → remorse → release → a tease.

## Prompts (paste as-is; the tags are not spoken)
### EN
```
[intrigued] The gods once made a human their king. He became a snake.

[matter-of-fact] Their king, Indra, had vanished, so they chose Nahusha. [humble] "I'm too weak," he said.

[with wonder] So they gave him a power: one look, and he took anyone's strength.

[ominous] Then power changed him. He demanded Indra's queen, Shachi.

[calmly, cunning] She set a trap for his pride: "Come to me carried by sages. No god ever has."

[proud, building] He did. And when the sages rebuked him, he set his foot on Agastya's head.

[intense] Agastya cursed him: [angry] "Fall from heaven. Become a snake!"

[desperate] Falling, Nahusha begged for mercy. Agastya said: [gently] "Whoever answers your questions will free you."

[tense] Ages later, that snake seized mighty Bhima, and took his strength.

[urgent] Yudhishthira found his brother. [deep, weary] "I am Nahusha, your ancestor," said the snake. [deep, slowly] "Answer me, and he lives: who is a Brahmin?"

[calmly] Yudhishthira said: [sincerely] "One with truth, forgiveness and compassion. It's conduct that makes one, not birth alone."

[gravely] Nahusha had lost heaven by his own conduct. [remorseful, slowly] "Power deludes even the wise," he said.

[relieved, warmly] He let Bhima go, and the curse broke. The man who'd said "I'm too weak" rose to heaven again.

[intrigued] Next: a dead snake, and a king with seven days to live.
```

### HI
```
[intrigued] देवताओं ने एक मनुष्य को राजा बनाया। वो साँप बन गया।

[matter-of-fact] देवराज इन्द्र ग़ायब थे, तो राजा नहुष चुने गए। वो बोले: [humble] "मैं दुर्बल हूँ।"

[with wonder] तो देवताओं ने शक्ति दी: जिसे देखें, उसका बल हर लें।

[ominous] पर शक्ति ने उन्हें बदल दिया। वो इन्द्र की रानी शची को माँग बैठे।

[calmly, cunning] शची ने उनके घमंड के लिए जाल बिछाया: "ऋषियों से पालकी उठवाकर आइए। ऐसे कोई देवता नहीं आया।"

[proud, building] नहुष ने यही किया। ऋषियों ने टोका, तो अगस्त्य ऋषि के सिर पर पैर रख दिया।

[intense] अगस्त्य ने शाप दिया: [angry] "स्वर्ग से गिर! साँप बन जा!"

[desperate] गिरते हुए नहुष ने क्षमा माँगी। अगस्त्य बोले: [gently] "जो तुम्हारे प्रश्नों का उत्तर देगा, वही तुम्हें मुक्त करेगा।"

[tense] बहुत समय बाद, उसी साँप ने महाबली भीम को जकड़कर उनका बल हर लिया।

[urgent] युधिष्ठिर भाई को ढूँढते आए। साँप बोला: [deep, weary] "मैं नहुष हूँ, तुम्हारा पूर्वज। [deep, slowly] उत्तर दो, तो ये बचेगा: ब्राह्मण कौन है?"

[calmly] युधिष्ठिर बोले: [sincerely] "जिसमें सत्य, क्षमा और दया हो। ब्राह्मण आचरण से होता है, केवल जन्म से नहीं।"

[gravely] नहुष ने स्वर्ग अपने ही आचरण से खोया था। वो बोले: [remorseful, slowly] "वैभव ज्ञानी को भी भटका देता है।"

[relieved, warmly] भीम छूट गए, और शाप टूट गया। जो कभी बोले थे "मैं दुर्बल हूँ," वो फिर स्वर्ग लौट गए।

[intrigued] अगली बार: एक मरा साँप, और एक राजा के आख़िरी सात दिन।
```

## Takes
| Lang | Status |
|---|---|
| EN | 2026-11-25: node `JAsmY73dHnqyIiLs10ul`, generation `a17XMOHwO4xm74V3X6GZ`, 1,385 credits. Raw 80.8 s; Scribe node `V2tNLI4bsj35PS7ApHsB`, 197/197 words, 0 interpolated; speech ends at 82.4 s incl. the sting. Sync 0 off, no missed cues. **Checked independently** with an offline Whisper (small.en): 197/197 words the same, no tags spoken. **In use.** |
| HI | 2026-11-25: node `fJgUeaBgsMpAow8frmeP`, generation `MR9QgI0KuwrX7XgplABz`, 1,328 credits. Raw 88.0 s; Scribe node `rljzm1TrnxtGULFwNC4s`, 212/212 words, 0 interpolated; speech ends at 89.4 s. Sync 0 off, no missed cues; word starts sit within 0.3 s of the real pauses. **Pronunciation not checked by machine: needs a listen** (नहुष, शची, अगस्त्य, युधिष्ठिर, घमंड, ढूँढते). **In use.** |

**Note on Scribe:** its transcript repeats the prompt, so a full match proves the timing only, never the pronunciation (see E05's note).
