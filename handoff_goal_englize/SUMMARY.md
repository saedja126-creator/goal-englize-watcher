# Goal Englize carousels: full handoff (as of 1 Nov 2026)

Everything from the cloud chat: the rules you set, the design, the four carousel projects and their status, how to rebuild and export, and what is still open. Written to be read cold by Claude Code on your machine.

---

## 1. What this is

You run **Goal Englize** (Arabic football content, Instagram carousels, English Premier League "Big Six" focus). The working loop with Claude:

1. You paste an article or report (or a link, if the network allows it).
2. Claude extracts the key facts and checks every claim against the source.
3. Claude builds a **planner**: an HTML artifact with the slides in your design. Under each slide there are Keep / Drop / Change controls, an editable text box, position notes, image prompts, the exact source sentence and a "Check this" note.
4. You press Keep / Drop / Change on every slide and paste the notes back ("Copy all notes").
5. After you approve, Claude places your photos, exports **9 MP4 (with motion) plus 9 PNG** at 1080x1440, builds a **download page** you can open on your phone, and writes a short Arabic **caption**.

Copy source: sometimes Gemini writes the Arabic copy and Claude only verifies it (INEOS). Sometimes Claude writes it (Man Utd scenario).

---

## 2. Rules you set (do not break these)

| Rule | Detail |
|---|---|
| **Never invent facts** | Every figure and claim must trace to the source. If unsure, flag it. Never fill in from memory. |
| **Flag, don't hide** | Each slide shows: the exact source sentence, "what I changed" versus the draft, "Check this" flags. Own calculations, estimates and unopened pages are labelled. |
| **Fonts are fixed** | Headlines: **MBA** (embedded as base64, taken from your old artifact). Body: **Amiri Bold**. Never substitute a font (the Lalezar swap made you angry). |
| **Spelling** | **«إينيوس»** (your spelling), not «إنيوس». |
| **Colour per line** | Yellow `#FFD84D` for key words, red `#FF3B30` for the key warning. A colour **never crosses a line break**. Each body line is explicit. |
| **Slide 1 of a Gemini copy** | Do not touch the wording. Only punctuation and colours. |
| **Photos** | Your photos from the Drive folder go in. Face and subject must never sit under the text or be hidden. |
| **Language** | Arabic content: street-level Jordanian/Palestinian tone where asked, otherwise clear Arabic. Technical discussion in English. |
| **No lecturing, no filler** | Short answers. Tables for structured info. |
| **Multiple image prompts** | Ask first whether you want bulk format (one line per prompt, blank line between). |
| **Slide 1 must be a real hook** | Big yellow word + one contrast line + one image line. **No numbers, no lists of nouns.** |
| **A carousel is a story** | Every slide must pull into the next (bridge line at the end, connector at the start). Slides must not be readable alone and swappable. |
| **Swipe arrow** | The double chevron in the bottom corner on slides 1 to 8 (not the last). I wrongly left it off the winning-design cards (I assumed it was Instagram's own button). |
| **Density** | Winning design: **3 short lines per slide, at most 1 number.** |
| **Accuracy of estimates** | Label estimates «تقدير» on the slide. Never write «فوراً», «18 months» or «forced owners» where the report does not say so. |

---

## 3. The winning design (used by INEOS and Man Utd scenario)

- Card: 3:4, 1080x1440, black, direction RTL, `container-type:inline-size` so everything scales in `cqw`.
- Photo block: full-bleed, top, height `92cqw` for landscape photos. Tall full-card block (`133.34cqw`) for portrait photos that already have a black bottom. Optional vertical shift.
- Gradient over the photo: transparent to 40% of the card height, 0.7 black at 56%, solid black from 68%.
- Text block `.wtext`: left and right `7.5cqw`, `bottom:13cqw`, flex column, centred, gap `3.2cqw`.
- Headline `.wh`: MBA, `9.6cqw` (smaller on long ones, 7.4 to 8.6), yellow `#FFD84D`, line-height 1.2, subtle text shadow.
- Body `.wb`: Amiri 700, `4.9cqw` default (4.2 to 4.5 on dense slides), line-height 1.62, white. Each line is `.bl` (`display:block; white-space:nowrap`) so no line wraps. The overflow check (`fit8.js`) must report no `OVER`.
- Slide 1: `.wk` (`19cqw`, yellow) is the big word. `.w2` (`8.8cqw`, white) is the contrast line with one red word.
- Motion: `rise` (text, 0.8s, delays 0.2s+) and `zoombg` (photo `background-size` from `--bs0` to `--bs1`, about 7 to 8 s).

---

## 4. Projects and status

| Project | Slides | Planner | Finished | Status |
|---|---|---|---|---|
| Ten Hag interview | 6 to 7 | https://claude.ai/artifact/VUXXqGmNViuFhRReiQ5uxP | https://claude.ai/artifact/FEjwBvxWU7FU7yReN3gKUm | Done, caption written |
| Como v Man Utd | 7 | https://claude.ai/artifact/1NDV2w4gySZhETSELfs7vr | https://claude.ai/artifact/U5H96boHcxet3Rf1L33nqf | Done (video and PNG downloads built) |
| **INEOS** (winning design) | 9 | https://claude.ai/artifact/5UA7KEoE3NPNzc3behSepy | https://claude.ai/artifact/9PEM6d24EXtXc3M5NtSsx5 | **Done**: photos placed, 9 MP4 + 9 PNG, caption. Slides 1 and 8 were waiting for your Keep. |
| **Man Utd relegation scenario** | 9 | https://claude.ai/artifact/9ceH1gEoPd6LY9xd9tcKc3 (version 2) | not started | **In progress**, version 3 planned, see section 6 |

Your other artifacts (Chelsea reports, Command Center, Fact-Check Kit, ornament business maps and so on) belong to other chats and are not part of this handoff.

---

## 5. INEOS: final copy

Source: your INEOS research report (Arabic) plus Gemini's 9-slide copy, checked by Claude.

| # | Headline | Body lines |
|---|---|---|
| 1 | إينيوس (big, yellow) / وعود براقة وواقع مرير! (white, «مرير» red) | مشروع رياضي يعاني من عمى الألوان منذ اليوم الأول |
| 2 | إمبراطورية البتروكيماويات! | اشترت لوزان في ٢٠١٧، ثم نيس في ٢٠١٩، / وفي ٢٠٢٤ تولّت إدارة كرة القدم في يونايتد. / ٣ أندية... فهل نجح النموذج؟ |
| 3 | حتى الشعار لم يسلم! | بعد الاستحواذ بوقت قصير، عدّلت إينيوس / شعار لوزان ليحاكي هويتها البصرية، / واضطرت للتراجع تحت ضغط المشجعين الغاضبين. |
| 4 | هبوط... ثم هبوط! | هبط لوزان في موسم الاستحواذ ٢٠١٧-١٨، / ثم مرة ثانية في ٢٠٢٢. / واليوم هو الأخير بـ٦ نقاط من ١١ مباراة، / والمدرب إلسنر يصف الوضع بـ«حالة طوارئ». |
| 5 | «أفضل دون تدخلنا»! | أنهى نيس ٢٠٢٤-٢٥ رابعًا، وقال راتكليف: / «كانوا أفضل بكثير دون تدخلنا» / وبعد عودتهم: سادس عشر وملحق البقاء |
| 6 | ١١٦ يومًا فقط! | مدّد يونايتد عقد تين هاغ في يوليو ٢٠٢٤ / ثم أقاله في أكتوبر وهو في المركز ١٤ / وكلّف تغيير الطاقم ١٤٫٥ مليون جنيه |
| 7 | ٥ أشهر فقط! | عيّنت يونايتد دان أشوورث مديرًا رياضيًا / في يوليو ٢٠٢٤، ورحل بالتراضي في ٨ ديسمبر. / ثم أقالت أموريم بعد ١٤ شهرًا فقط. |
| 8 | الغداء المجاني... انتهى! | ألغت إينيوس الغداء المجاني لموظفي أولد ترافورد / بعد الاستغناء عن نحو ٢٥٠ موظفًا / ورفعت بعض التذاكر إلى ٦٦ جنيهًا / بلا خصم للأطفال والمتقاعدين. |
| 9 | إحكيلي: مين المسؤول؟ | ٣ أندية، ولاعبان فقط انتقلا بينها منذ ٢٠٢٣. / هل المشكلة في النموذج متعدد الأندية، / ولا في القرارات؟ / شاركنا رأيك بالتعليقات! |

Photos placed (your Drive folder `1Va2GmGM2rFo1NQH-9kCzA82NFpSD-pcX`, files `Slide1` to `Slide9`): 1 three men at a stadium, 2 refinery, 3 Lausanne badge, 4 three Lausanne players, 5 Ratcliffe at Nice (only 739 px wide, upscaled 2x, soft at full size), 6 Ten Hag, 7 Ashworth and Amorim (the third man on the left is cropped out), 8 Old Trafford, 9 three chairs.

**Unverified or flagged INEOS items** (decide before posting):
- «١١٦ يومًا» is Claude's own count (July to October), not a report figure.
- The £14.5m is not Ten Hag alone: the slide says «تغيير الطاقم».
- League tables and the £66 ticket come from pages Claude could not open.
- Slide 8 «ألغت / ورفعت إينيوس» is your attribution (the report says the club announced it).
- Slide 3 «تحت ضغط» is your wording; the report says fans objected and the change was reversed.
- The Amorim £11m figure was dropped (no matching page).

**Caption (INEOS)**

> إينيوس اشترت لوزان، بعدين نيس، وبعدين استلمت كرة القدم في يونايتد. ٣ أندية... وهاي النتيجة 👇
>
> لوزان هبط مرتين وهلأ بالمركز الأخير. نيس أنهى الموسم رابعًا، وبعد رجوعهم صار سادس عشر وخاض ملحق البقاء. وبين الأندية الثلاثة، لاعبان فقط انتقلوا منذ ٢٠٢٣.
>
> المشكلة بالنموذج متعدد الأندية، ولا بالقرارات؟ شاركنا رأيك بالتعليقات!
>
> #إينيوس #مانشستر_يونايتد #نيس #لوزان #البريميرليغ

Every figure in the caption is on the slides and from the report. Pattern for future captions: one hook line, two or three facts, one open question.

---

## 6. Man Utd relegation scenario (the current work)

**Source:** The Esk, "The Analysis Series: Manchester United, the financial & covenant consequences of a low finish or relegation in 2026/27", Paul Quinn, 1 November 2026. It is **conditional scenario analysis, not a forecast** (the report says so). Credit The Esk and Paul Quinn in the caption.

**Key facts verified against the pasted report**

| Fact | Value |
|---|---|
| Position (1 Nov 2026) | 16th/17th, 7 pts from 9 games (W1 D4 L4, GD -5); 20th in the Champions League league phase with 3 pts from 3; under 30 pts over 38 games at that rate |
| FY2026 | Revenue £677.6m, adjusted EBITDA £216.4m (record), net loss £43.0m, cash £67.2m, net debt about £621.7m |
| Bank covenant | Consolidated Adjusted EBITDA at least **£125m** per rolling 12 months, tested quarterly. Raised from **£65m** in the June 2026 refinancing. Profit on player sales excluded. Dispensation up to twice, never in consecutive years. |
| Scenario A (14th to 17th, no Europe, 2027/28) | Revenue about £605m, EBITDA about £135m, only about £10m above the floor |
| Scenario B (relegation, year 1) | Revenue about £392m, EBITDA about -£3m (about zero) |
| adidas | £90m a year minimum guarantee (£900m over 10 years). -£10m per season without the Champions League. Up to a 50% cut in any season outside the Premier League. Termination on one full season's notice after relegation. |
| Transfer payables | £375.0m, about £218m due within a year, up to £122.8m contingent, plus £191.7m of summer 2026 commitments |
| Liquidity | RCF £400m, £200m drawn at 21 Sep 2026, about £200m undrawn. Scenario B year 1 free cash flow about -£185m. |
| Wages | Champions League pay step-ups fall away automatically. United reported as not usually negotiating relegation clauses. Regulator: clubs relegated in 2024/25 lost about £70m revenue and cut wages about £29m. |
| Stadium | £2bn, 100,000 seats, privately financed. A delays financing. B unfinanceable on commercial terms until promotion. |
| Ownership | Glazers 67.9% of votes (48.9% economic). INEOS 28.94% with football operations control. No disclosed obligation on any shareholder to fund losses. Ratcliffe's $33/share floor ends February 2027. |
| One versus two seasons | One season survivable (promotion plus about £50-100m). Two or more needs about £150-400m of new equity or refinancing. |

**Inconsistency inside the report:** the summary says the undrawn credit is exhausted within "about 18 months", but its own cash table shows about £185m used in year 1. Use the table.

**Your review of the Gemini-style draft** (the 9-slide draft you pasted): contradictions found and rules applied.
- Slide 1 and 9 of that draft were leftovers from the INEOS carousel (wrong topic).
- Slide 6 «تضحية بالعمال» (staff cuts) is not in this report.
- «الغياب عن أوروبا يهدد البقاء» contradicts the report (Scenario A stays solvent).
- «شرط خفي»: the covenant is disclosed.
- Corrected: adidas £90m is per year, the 50% cut is for any season outside the Premier League, termination needs a season's notice; £375m is exact and only about £218m is due within a year; "الدرجة الأولى" should be the second tier; the stadium is delayed or unfinanceable (not "frozen"); owners are not "forced".
- **Open question to you:** you said a figure was shown as 265 but was only 65 million. I could not find 265 anywhere in the planner. The only "65" is the old covenant floor. **Tell me which slide.**

**Planner version 2 (published) copy**

| # | Headline | Idea |
|---|---|---|
| 1 | يونايتد · لو هبط... المشكلة أكبر! | Hook (**you rejected this slide: too many words, no real hook**) |
| 2 | بداية متعثرة | The table decides the income |
| 3 | خط البنوك | The bank profit floor of £125m |
| 4 | صفعة أديداس | £90m a year, 50% cut, season's notice |
| 5 | فواتير معلقة | £375m instalments, any division |
| 6 | رواتب عالقة | Income falls fast, wages slowly |
| 7 | حلم مهدد | The £2bn stadium |
| 8 | نزيف السيولة | About £185m burned in year 1 |
| 9 | سنة تُحتمل... وسنتان لا! | One season survivable, two not, history, comments question |

**Your feedback on version 2 and the plan agreed for version 3 (not built yet)**
- The slides inform but do not form a story: each could be read alone.
- Slide 1 is the weakest (lots of numbers, words and nouns that mean nothing).
- No arrow like your style.
- Agreed answers: Slide 1 = **big word + contrast + metaphor** (INEOS pattern). Link style = **both** (a bridge at the end of each slide and a connector at the start of the next). Arrow = **double chevron, bottom corner, slides 1 to 8**. Density = **3 short lines, at most 1 number**.
- **Story spine "السلسلة" (the domino chain):** 1 hook → 2 the table becomes money → 3 the bank line → 4 the sponsor → 5 the bills → 6 wages → 7 the stadium → 8 cash drain → 9 verdict and your comments question.
- Slide 1 options proposed (waiting for your pick, or your own wording):
  - **A (recommended):** big «يونايتد» / «لو سقط يونايتد... سقط معه كل شيء!» / «سيناريو مالي يرصد ما يتساقط بعد الهبوط: الراعي، والبنك، والملعب الجديد».
  - **C:** big «الهبوط» / «يبدأ بنتيجة... وينتهي عند البنك!» / «سيناريو مالي: كيف تتحول مباراة خاسرة إلى أزمة سيولة؟».
- Move the numbers that do not carry the story (£45m, £10m, £50-100m) to the planner notes, not the slide.

---

## 7. How to rebuild, edit and export

**Setup (once)**
```bash
pip install pillow pillow-heif
npm i -g playwright   # Chromium for rendering
# ffmpeg must be on PATH
```

**Planner builders** (run from `source/`; they read `../reference/old_planner_format.html` for the font and CSS)
```bash
cd source
python3 plan9.py     # Man Utd scenario -> manutd_scenario_plan.html (identical to the published v2)
python3 plan7.py     # INEOS            -> ineos_carousel_plan.html (needs ineos_jpg/1.jpg..9.jpg next to it)
```
Slide text lives in `slides9_content.py` (Man Utd) and the `LINES` dict near the top of `plan7.py` (INEOS). After editing `slides9_content.py`, paste it back into `plan9.py` between `def srce(` and `th='padding` (or edit `plan9.py` directly).

**Checks and stills**
```bash
node fit8.js          # reports OVER for any line that overflows; target: no OVER
node still_mu.js stills_mu 7       # 1080x1440 stills at t=7s
node still_ineos.js stills_a 7
```

**Export motion (9 slides, 24 fps, 7 s, parallel batches)**
```bash
node motion_ineos.js 24 7 1 4 7 &   node motion_ineos.js 24 7 2 5 8 &   node motion_ineos.js 24 7 3 6 9 &
for n in 1 2 3 4 5 6 7 8 9; do ffmpeg -y -framerate 24 -i ineos_frames/s$n/%04d.jpg \
 -vf "crop=1080:1440:0:0,tpad=stop_mode=clone:stop_duration=1,format=yuv420p" \
 -c:v libx264 -profile:v high -level 4.0 -crf 27 -preset slow -movflags +faststart out/v$n.mp4; done
```

**Download page** (`build_dl_ineos.py`): embeds each MP4 and a JPEG q93 still as base64 in `<script type="text/plain">` tags and converts the still to a real PNG in the browser at save time (the page limit is 16 MB, the INEOS page is 10.9 MB). Test it with `testdl_ineos.js` (stubs the `downloads` capability). Publish with `capabilities: {"downloads": true}`.

**Traps we already hit**
- The page's scroll observer (`IntersectionObserver`) resets the animation during capture. The capture scripts delete it with `addInitScript` and load the page through `file://` (not `setContent`).
- Relative `fetch` of the video files failed in the artifact viewer ("The file did not load"). Embed the data in the page instead.
- Headless Chromium cannot play H.264, so the stub test checks the saved blobs, not playback.
- Python f-strings with `\'` fail: use `’` in table text.
- Colour spans must not straddle lines (write each line explicitly).
- Playwright and `crop=1080:1440` fix the 1441 px screenshot rounding.
- `download_file_content` saves huge base64 JSON to tool-results. Decode with `python3 -I dec_ineos.py <outdir>`.

---

## 8. Folder map

```
handoff_goal_englize/
  SUMMARY.md                  this file
  artifacts/                  the exact published HTML (planners and download pages)
  exports/ineos|como|tenhag/  finished MP4 and PNG files
  source/                     all builders, content files, capture scripts, tests
  reference/old_planner_format.html   your original planner (font, CSS, icons, motion script)
  private_photos/             your photos (raw). Not for any public repo.
  .gitignore                  ignores photos, artifacts, exports and the reference file
```

**Git note:** only `SUMMARY.md`, `source/` and `.gitignore` are committed to the repo. `reference/old_planner_format.html` (it embeds photos), `artifacts/`, `exports/` and `private_photos/` are only in the zip. Keep the zip: the builders in `source/` need `reference/old_planner_format.html` at `../reference/`.

---

## 9. Open items and warnings

1. **Pick slide 1** for Man Utd (A, C or your own words) and say "go" on the chain order. Then I build version 3 with the story links and the arrow.
2. **Which slide shows "265"?** I could not find it.
3. **Photos for Man Utd:** send the Drive folder once you have pressed Keep on the slides. Suggested shots are in the planner (Old Trafford at night, dejected players, red line, kit, stadium, training ground, stadium plan, owners, lower-league ground).
4. **Arrow on the INEOS carousel:** the exported INEOS slides have no arrow. Add it if you want it consistent.
5. **Security:** the GitHub repo `saedja126-creator/goal-englize-watcher` is **public** and contains `goal_englize_watcher.session` (a Telegram session file). Treat it as compromised: terminate that session in Telegram (Settings, Devices) and remove the file from the repo and history. Nothing was changed on `main`.
6. **Do not push this folder to a public repo.** The planners and exports embed your photos. Use a private repo or keep it local (`.gitignore` already excludes the heavy folders).
7. **Network:** this cloud session could not reach `theesk.org` (host not on the allowlist). Paste article text or allow the domain.

---

## 10. Prompt to resume in Claude Code

> Read `handoff_goal_englize/SUMMARY.md` first. We are on the Man Utd relegation scenario carousel. Rebuild planner version 3: slide 1 option A, the "السلسلة" story chain with bridge lines and connectors, the double chevron arrow on slides 1 to 8, 3 short lines per slide and at most one number. Keep MBA and Amiri fonts, spelling «إينيوس», the verified facts in section 6, and the rules in section 2. Do not publish photos to any public repo. Run `fit8.js` before showing me anything.
