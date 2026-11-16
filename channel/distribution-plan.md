# The Lost Gyaan: distribution plan

Written 2026-11-16. Treat it as a starting plan to test: after 4 weeks, let each channel's own analytics overrule it (YouTube Studio → Audience → "When your viewers are on YouTube"; Instagram → Insights → Followers → Most active times).

## 1. One brand, two accounts per platform (decided 2026-11-16)

| Language | YouTube | Instagram |
|---|---|---|
| **Hindi (main)** | `@thelostgyaan` | `@thelostgyaan` |
| **English** | `@thelostgyaan.en` | `@thelostgyaan.en` |

- **Why split by language:** YouTube recommends Shorts by the language a viewer watches in, and on a mixed channel each language's viewers swipe away from the other's videos, which hurts retention for both. Separate accounts keep every feed in one language.
- **Why one name:** the logo, banner, end card and thumbnails stay the same; only the handle changes. If someone drops the ".en", they land on our Hindi account, which links straight back.
- **Cross-links:** each bio and YouTube description links the other ("Watch in English: @thelostgyaan.en" / "हिंदी में देखें: @thelostgyaan"), and so do the YouTube banner links.
- **Display names:** Hindi "The Lost Gyaan | हिंदी", English "The Lost Gyaan | English" (Instagram's name field allows 30 characters).
- **End card:** each language's video shows its own handle (`studio/src/lib/brand.ts`).
- **Hindi gets priority** (the biggest audience for Indian mythology); English widens the reach (urban India, the diaspora, world mythology and history later).

## 2. When to post (IST)

| | Main slot | Second slot | Why |
|---|---|---|---|
| **YouTube Hindi** | **7:00–8:30 PM** weekdays | **7:00–8:00 AM** for devotional stories | The evening scroll after work and college; mornings are puja and darshan time for devotional topics. |
| **YouTube English** | **7:30–8:30 AM** | 8:00–9:00 PM | 7:30 AM IST is about 9 PM in New York (the US diaspora's evening) and the morning commute in India. |
| **Instagram Hindi** | **7:00–9:00 PM** weekdays | Saturday **11 AM–1 PM** | The most common Reels peak across sources. |
| **Instagram English** | **12:00–1:00 PM** | 8:00–9:00 PM | The lunch-break scroll; English India audiences also peak in the evening. |

**Rules that matter more than the clock:**
1. **Festivals and tithis beat everything.** A mythology Short posted **1–2 days before** its festival rides the search spike. Keep a calendar (§5): Ekadashi for Khatu Shyam, Tuesday and Saturday for Hanuman, Monday and Shivaratri for Shiva, Janmashtami for Krishna.
2. **Shorts are tested over days.** The upload hour decides only the first few hundred views; the hook and the retention decide the rest. Don't delay a ready video for a perfect slot.
3. **Avoid India cricket matches** (and IPL nights): attention collapses.
4. **Schedule in advance** (YouTube Studio scheduling; Instagram's scheduler or Meta Business Suite) so posting is never the bottleneck.

## 3. How often

| Phase | Stories per week | Each story becomes | Posts per week |
|---|---|---|---|
| **Weeks 1–8** (now) | **3** (Mon, Wed, Fri) | 1 Hindi Short, 1 English Short, 1 Hindi Reel, 1 English Reel | 6 YouTube + 6 IG |
| **After the end-to-end SVG flow** | 4–5 | same | 8–10 YouTube + 4–10 IG |
| **Monthly, from about episode 6** | 1 long-form (16:9, 8–12 min, chapters) | 5–8 related Shorts stitched together, the same voice and art | +1 YouTube |

- **Consistency beats volume.** 3 a week every week for 8 weeks does more than 7 in week one and then a gap. The algorithm and the audience both learn the rhythm.
- **Keep a buffer:** have 4–6 finished episodes before launch, and keep at least 3 in reserve. Production time is the real limit (research → script → voice → render).
- **Series help retention:** group stories into named series ("Curses of the Mahabharata", "Lost Kings", later "Gods of Greece"). Each Short ends by teasing the next one, and the YouTube playlist is where binge-watching happens.
- **Long-form is where The Knowledge Stream's views come from** (its 9-minute Garuda video has 785k views). Once a series has 5–8 Shorts, stitch them into one 16:9 video.

## 4. Titles, descriptions and hashtags (the formula)

### YouTube Shorts
- **Title (≤ 60 characters, the main search signal):** the hook, not a label. Name the famous person or epic in the first 3–4 words. Pattern: *[famous name] + [surprising fact or question]*. "He Could End the Mahabharata War With 3 Arrows" beats "The Story of Barbarika".
- **Hindi titles in Devanagari** (most Hindi searches are typed or spoken in Devanagari); Roman Hinglish only as a test variant.
- **Description:**
  1. Line 1 restates the hook with the main keywords (it shows in search).
  2. Lines 2–3: who it's about, which telling we follow.
  3. The series line + "Follow for the next lost story".
  4. Sources (our trust advantage; viewers notice).
  5. 3–5 hashtags at the end. **The first three appear above the title**, so put the strongest three first.
- **Hashtag mix (3–5):** 1 big (#Mahabharata, #IndianMythology), 1–2 specific (#KhatuShyam, #Barbarika), 1 brand (#TheLostGyaan), then #Shorts. Hindi Shorts: Devanagari tags first (#महाभारत #खाटूश्याम), one Roman tag.
- **Pinned comment:** a question that invites a version debate ("Which telling did you grow up with?"). Comments count as engagement.
- **Add to the series playlist** at upload, and set "Related video" to the previous episode of the series.

### Instagram Reels
- **Caption (keywords matter more than hashtags now):** line 1 is the hook (the first ~125 characters show before "…more"). Then 1–2 lines with the names people search (Barbarika, Khatu Shyam, Mahabharata), then a CTA ("Follow @thelostgyaan for the stories history forgot").
- **Hashtags: at most 5** (Instagram's limit). 1 broad + 2–3 specific + #TheLostGyaan.
- **Location tag** when the story has a place: e.g. *Khatu Shyam Ji Temple, Sikar*. Devotees browse location pages.
- **Cover:** the episode thumbnail (`render/<ID>-thumb-hi.png`).
- **Alt text:** one sentence describing the scene, for search.
- **Share to Story** after posting, with a poll ("Had you heard this version?").

## 5. Calendar hooks (check exact dates each year in a panchang)
| Date (2026–27) | Occasion | Story ideas |
|---|---|---|
| **Fri 20 Nov 2026** | **Khatu Shyam Janmotsav / Dev Uthani Ekadashi** (Kartik Shukla Ekadashi; some Vaishnava calendars mark 21 Nov) | **X001 Barbarika: post Thu 19 Nov evening** |
| every Ekadashi | Khatu Shyam's day, Vishnu | Vishnu and Krishna stories |
| Tuesdays and Saturdays | Hanuman | Hanuman stories |
| Mahashivaratri, Mondays | Shiva | Shiva stories |
| Feb–Mar 2027 | Khatu Shyam Phalguna Mela (Phalguna Shukla Ekadashi) | repost X001, or a part 2 |

## 6. Launch checklist for X001 (going out early, on 16–17 Nov)
- [ ] Create `@thelostgyaan.en` on YouTube and Instagram (same emblem and banner), and cross-link the bios
- [ ] **Hindi, Mon 16 Nov:** YouTube Short 7:30 PM IST, Instagram Reel 8:00 PM IST (location Khatu Shyam Ji Temple)
- [ ] **English, Tue 17 Nov:** YouTube Short 7:30 AM IST, Instagram Reel 12:30 PM IST
- [ ] **Janmotsav, Fri 20 Nov:** reshare as an Instagram Story and a YouTube community post ("Jai Shri Shyam 🙏, Baba's Janmotsav today")
- [ ] Captions, titles and hashtags from `episodes/X001-barbarika-three-arrows/07-publish.md`; thumbnails `render/X001-thumb-{hi,en}.png`
- [ ] Pin the version-debate comment on each
- [ ] After 48 hours: note the views, average view duration and swipe-away rate in `08-review.md`

Sources: [Khatu Shyam birthday 2026 (Arun Pandit)](https://astroarunpandit.org/blogs/khatu-shyam-birthday-2026-date-tithi-puja-vidhi-story/) · [Dev Uthani Ekadashi 2026 (Arun Pandit)](https://astroarunpandit.org/blogs/dev-uthani-ekadashi-2026-date-puja-vidhi-vrat-katha-parana-time/) · [Khatu Shyam birthday (Bhakti Bharat)](https://www.bhaktibharat.com/en/festival/khatu-shyam-birthday) · [Best time to post YouTube Shorts in India (Fluxnote)](https://fluxnote.io/guides/best-time-to-post-youtube-shorts-india-2026) · [Best time to post on Instagram in India (WsCube Tech)](https://www.wscubetech.com/blog/instagram-post-time/) · [Best time to post (Buffer)](https://buffer.com/library/best-time-to-post-social-media/). The posting-time sources disagree (some favour afternoons or late nights), so the evening slots here are the common ground, to be checked against our own analytics.
