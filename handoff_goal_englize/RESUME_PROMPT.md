# Paste this into Claude Code

Before pasting: unzip `handoff_goal_englize.zip` and open that folder in Claude Code, so it can see the files.

---

You are continuing a project from a cloud chat with Claude. All context is in this folder. Read these first, in order:
1. SUMMARY.md (rules, design spec, project status, commands, open items)
2. sources/the_esk_man_utd_relegation_scenario.md (the ONLY source for the current carousel; every fact must trace to it)
3. source/plan9.py and source/slides9_content.py (the builder and slide content of planner version 2)
4. artifacts/manutd_scenario_plan.html (what I currently see, version 2)

WHO I AM: I run "Goal Englize", Arabic football content (Instagram carousels, Premier League Big Six focus). Be precise and concise. No filler, no lecturing, no unsolicited advice. Arabic content is for a Jordanian/Palestinian audience; discussion with me is in English.

THE TASK: Rebuild the Man Utd relegation-scenario carousel as planner VERSION 3, as an HTML page I can open and use to press Keep / Drop / Change on each slide. Same format as version 2: dark "winning design" cards (3:4, MBA headlines, Amiri body, yellow #FFD84D and red #FF3B30 highlights), and under each slide: Keep/Drop/Change, editable text, position notes, image prompts A and B, "From the report" (exact source sentence), "From your draft", "Behind the number", "Check this", plus a "Copy all notes" button.
If you have the Artifact tool, publish it as a new artifact. Otherwise write source/manutd_scenario_plan_v3.html and open it in the browser.

WHAT CHANGED IN V3 (my feedback on v2, already agreed):
- v2 reads as 9 separate facts. v3 must be ONE STORY, "السلسلة" (a domino chain): every slide ends with a bridge line that raises a question, and the next slide opens with a connector (ثم، والأسوأ، لكن، وهنا...) and answers it. No two slides can be swapped without breaking the story.
  Spine: 1 hook → 2 the table becomes money → 3 the bank line (£125m covenant) → 4 the sponsor (adidas) → 5 the bills (£375m instalments) → 6 wages → 7 the stadium → 8 the cash drain and who covers it → 9 verdict (one season survivable, two not) + my comments question.
- SLIDE 1 is the worst slide and must copy my INEOS winning slide 1: one BIG yellow word, one white contrast line with one red word, one short image line. NO numbers, NO lists of nouns, about a dozen words. Ask me to pick before building:
  A (recommended): big «يونايتد» / «لو سقط يونايتد... سقط معه كل شيء!» / «سيناريو مالي يرصد ما يتساقط بعد الهبوط: الراعي، والبنك، والملعب الجديد».
  C: big «الهبوط» / «يبدأ بنتيجة... وينتهي عند البنك!» / «سيناريو مالي: كيف تتحول مباراة خاسرة إلى أزمة سيولة؟».
  Or my own wording.
- ARROW: the double chevron in the bottom corner (the ARROW svg in source/plan.py card()), on slides 1 to 8 only, in the planner and in any export. The winning-design cards (.card.w) currently have none: add it.
- DENSITY: 3 short lines per slide, at most 1 number per slide. Move numbers that do not carry the story (£45m, £10m, £50-100m) into the planner notes.

RULES (non-negotiable):
- Never invent or "round up" a fact. Everything traces to the Esk article. Label estimates «تقدير» on the slide. Flag anything I should check.
- The article is conditional scenario analysis, NOT a forecast. Every slide must stay conditional ("لو", "سيناريو"). Credit The Esk and Paul Quinn in the caption.
- Corrections already agreed (do not regress): adidas £90m is PER YEAR; the 50% cut applies to any season outside the Premier League; ending the deal needs one full season's notice. Transfer payables are exactly £375.0m, only about £218m due within a year. The Championship is the second tier (say الدرجة الثانية). Stadium: delayed in scenario A, unfinanceable on commercial terms until promotion in scenario B (not "frozen"). No shareholder is obliged to fund losses (do not say owners are "forced"). Use the report's cash table (about £185m in year 1), not its "18 months" wording. Do not mention staff cuts (not in this report). Do not use "winless in nine" (it clashes with W1 in nine).
- Fonts are fixed: MBA for headlines, Amiri Bold for body. Never substitute. Spelling is «إينيوس» (not «إنيوس»).
- Colour never crosses a line break: write each body line explicitly.
- Photos are mine and private: never push photos, exports, artifacts or the reference file to a public git repo.

HOW TO BUILD AND CHECK:
- cd source; python3 plan9.py reproduces v2 exactly (needs ../reference/old_planner_format.html; if it is missing, ask me for the zip).
- Put the v3 slide text in slides9_content.py (copy it to slides10_content.py), rebuild with a copy of plan9.py, then run node fit8.js (adapted to the new file name): it must report NO "OVER" lines.
- Render stills with a copy of still_mu.js and LOOK at them (every line fits, arrow visible, chain reads in order) before showing me.
- Show me the 9 headlines plus the bridge/connector of each slide in a table first, then build.

OPEN QUESTIONS FOR ME: (1) slide 1 choice A, C or mine; (2) I once saw a figure shown as 265 that should have been 65 million: I could not find it; if you spot any wrong figure, tell me. After I press Keep/Drop/Change and send the notes, the next steps are: place my photos (I will give a Drive folder), export 9 MP4 + 9 PNG at 1080x1440, build the download page, and write a short Arabic caption.
