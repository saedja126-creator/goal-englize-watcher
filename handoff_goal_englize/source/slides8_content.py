# ---- Man Utd scenario carousel: content (exec'd inside plan8.py after helpers) ----
def srce(ref,*lines):
    q=''.join(f'<span dir="ltr" style="display:block;margin-bottom:6px;text-align:left">{l}</span>' for l in lines)
    return ('From the report',q+f'<span style="display:block;color:#667085;font-size:13px">{ref}</span>','')
def beh(t): return ('Behind the number',t,'')
def chk(t): return ('Check this',t,'')
SZ="3:4 portrait, generate at 1080x1440 or larger"
COMP="The subject fills the top two thirds. Keep the bottom third dark and empty, because the text sits there on a black gradient."
def A_(s): return s+" Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no recognisable faces."
LINES={
1:{'head':'<span class="wk">يونايتد</span><span class="w2">لو هبط... المشكلة '+Rd('أكبر')+'!</span>',
   'headrow':('Line 1 yellow, line 2 white with a red word','يونايتد<br>لو هبط... المشكلة أكبر!','ar h'),
   'dtext':"Line 1: يونايتد\nLine 2: لو هبط... المشكلة أكبر!",
   'lines':['تقرير مالي يحلّل سيناريو الهبوط في ٢٠٢٦/٢٧،','ويشرح ما وراء الأرقام: '+Y('الديون والعقود')+' والرعاة']},
2:{'hs':8.6,'bs':4.4,'lines':['بعد ٩ مباريات: '+Y('٧ نقاط فقط')+'، والمركز ١٦ أو ١٧،','وفي دوري الأبطال: المركز ٢٠ بـ٣ نقاط من ٣ مباريات.',Rd('وبهذا المعدل: أقل من ٣٠ نقطة في الموسم!'),'ومكافأة المركز ١٦ أقل '+Y('بنحو ٤٥ مليونًا')+' من الثالث (تقدير)']},
3:{'hs':8.2,'bs':4.5,'lines':['تشترط البنوك أرباحًا تشغيلية لا تقل عن '+Y('١٢٥ مليونًا'),'كانت ٢١٦ مليونًا في ٢٠٢٥/٢٦، وهو رقم قياسي،','وتنزل إلى '+Y('١٣٥')+' لو أنهى بين ١٤ و١٧ بلا أوروبا،',Rd('وبعد الهبوط: قرابة الصفر!')]},
4:{'bs':4.5,'lines':['بثّ الدوري يتحول إلى '+Y('تعويضات هبوط')+' أقل بكثير،','وأديداس تملك حق '+Y('خفض دفعتها ٥٠٪')+'،','وإيرادات المباريات تنخفض '+Y('نحو الثلث')+'،',Rd('فتنزل الإيرادات من ٦٧٨ إلى نحو ٣٩٢ مليونًا (تقدير)')]},
5:{'hs':7.4,'bs':4.3,'lines':['الهابطون في ٢٠٢٤/٢٥ خسروا '+Y('نحو ٧٠ مليونًا')+' إيرادات،','وخفّضت الرواتب '+Y('نحو ٢٩ مليونًا')+' فقط، بحسب الهيئة المستقلة،',Rd('ويونايتد، بحسب تقارير، لا يضع بنود هبوط في العقود،'),'فتنخفض الرواتب ببيع اللاعبين وفقدان زيادات الأبطال.']},
6:{'hs':8.2,'bs':4.5,'lines':['على النادي '+Y('نحو ٣٧٥ مليونًا')+' أقساط انتقالات،','منها '+Y('نحو ٢١٨ مليونًا')+' تُدفع خلال سنة،','وتبقى واجبة الدفع في أي دوري يلعب فيه،',Rd('ويستهلك أول موسم بعد الهبوط نحو ١٨٥ مليونًا من السيولة')]},
7:{'hs':8.2,'bs':4.3,'lines':['موسم هبوط واحد وصعود فوري يحتاجان '+Y('٥٠–١٠٠ مليون')+'،','وسنتان فأكثر تحتاجان '+Y('١٥٠–٤٠٠ مليون')+' تمويلًا جديدًا،',Rd('لأن إعفاء شرط الـ١٢٥ مليونًا لا يُمنح سنتين متتاليتين،'),'وبيع اللاعبين لا ينقذه: أرباح بيعهم '+Y('لا تُحتسب')+' فيه.']},
8:{'bs':4.2,'lines':['لا التزام معلنًا على أي مساهم بتمويل خسائر النادي،','وغليزر تملك '+Y('٦٧٫٩٪ من الأصوات')+'، وإينيوس '+Y('٢٨٫٩٤٪')+'،',Rd('وسعر الـ٣٣ دولارًا الأدنى لراتكليف ينتهي في فبراير ٢٠٢٧،'),'وبعد الهبوط يرى كاتب التقرير أن '+Y('البيع الاضطراري')+' الأرجح.']},
9:{'bs':4.5,'lines':['الأندية ذات '+Y('الميزانية السليمة')+' والملاك الملتزمين تعود سريعًا،','ويونايتد نفسه هبط ١٩٧٤ وصعد ١٩٧٥ من أول محاولة،',Rd('أما المثقلة بالديون كليدز وشالكه فدخلت دوامة.'),'سيناريو افتراضي لا توقّع... '+Y('شاركنا رأيك بالتعليقات!')]},
}
CH=None
def mk(n,title,head,label,rows_,dtext,img): add(n,title,head,'',label,rows_,dtext,img)

# 1
mk(1,'Hook: the question, then the promise to explain',"",'Photo: Old Trafford night',
 [('Headline (yellow, red word)','يونايتد · لو هبط... المشكلة أكبر!','ar h'),
  ('Body','تقرير مالي يحلّل سيناريو الهبوط في ٢٠٢٦/٢٧، ويشرح ما وراء الأرقام: الديون والعقود والرعاة','ar'),
  beh("The report's point in one sentence: relegation would be a financing and solvency problem, not only a drop in income. The hook says «لو» (if) so nobody reads it as a prediction."),
  srce('Summary, first paragraph',"“Relegation at the end of 2026/27 would be a solvency and financing event for Manchester United, not merely a revenue shock.”","“This is conditional scenario analysis for public discussion, not a forecast that Manchester United will be relegated, and not investment advice.”"),
  chk("The report says outright that this is not a forecast. So the hook is conditional («لو هبط») and the body says «سيناريو». I suggest crediting The Esk and Paul Quinn in the caption. «المشكلة أكبر» is my plain-language version of «not merely a revenue shock».")],
 "Line 1: يونايتد\nLine 2: لو هبط... المشكلة أكبر!\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a huge empty football stadium at night under floodlights, rows of empty red seats curving away, a lone figure far in the stands, mist on the pitch. The stand fills the top two thirds, the bottom third falls to deep shadow."),
  A_("Editorial photograph of a football stadium exterior at dusk with a single glowing sign above a locked gate, cold blue light, nobody present. The building fills the top two thirds, the bottom third fades to black."),
  wm(("A real photo of Old Trafford at night","Old Trafford floodlights; Old Trafford at night","You already placed a real Old Trafford photo on INEOS slide 8. A different angle keeps the two carousels apart. Check the licence.")),True))
# 2
mk(2,'Where they are now, and why the table means money',"بداية متعثرة!",'Photo: dejected players',
 [('Headline (yellow)','بداية متعثرة!','ar h'),
  ('Body','بعد ٩ مباريات: ٧ نقاط فقط، والمركز ١٦ أو ١٧، وفي دوري الأبطال: المركز ٢٠ بـ٣ نقاط من ٣ مباريات. وبهذا المعدل: أقل من ٣٠ نقطة في الموسم! ومكافأة المركز ١٦ أقل بنحو ٤٥ مليونًا من الثالث (تقدير)','ar'),
  beh("A place in the table is not only pride. Each place is worth about £3.5m in league prize money (the report's estimate), and finishing outside the European places also removes the Champions League income and pay arrangements the club planned around."),
  srce('Key findings, «Position at 1 November 2026»; section 1.2',"“United are 16th–17th in the Premier League after nine games with 7 points (W1 D4 L4, goal difference −5), and winless in nine across all competitions. They are 20th in the Champions League league phase with 3 points from 3 games. Over 38 games, that rate would produce fewer than 30 points.”","“I estimate the 2026/27 merit payment at about £45m lower at 16th than at 3rd (assuming £3.5m per place).”"),
  chk("The report itself says sources differ on 16th or 17th, so the slide says «١٦ أو ١٧». I left out «winless in nine across all competitions»: it sits oddly next to W1 in nine league games, so I would need to confirm which nine games it counts. The £45m is the author's estimate, so the slide says «تقدير». It is about the 2026/27 league payment only.")],
 "Headline: بداية متعثرة!\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of two footballers in red kit seen from behind walking off an empty pitch after a match, heads down, stadium lights glowing, no readable numbers or names. The scene fills the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of a stadium scoreboard glowing in the dark above empty stands, the numbers blurred and unreadable, cold light. The scoreboard fills the top two thirds, the bottom third fades to black."),
  wm(("A real photo of United players after a defeat or a draw","Manchester United players dejected Old Trafford","Choose a wide shot where faces are small. Check the licence.")),True))
# 3
mk(3,'The red line: the lenders\' floor',"الخط الأحمر: ١٢٥ مليونًا!",'Photo: red line',
 [('Headline (yellow)','الخط الأحمر: ١٢٥ مليونًا!','ar h'),
  ('Body','تشترط البنوك أرباحًا تشغيلية لا تقل عن ١٢٥ مليونًا. كانت ٢١٦ مليونًا في ٢٠٢٥/٢٦، وهو رقم قياسي، وتنزل إلى ١٣٥ لو أنهى بين ١٤ و١٧ بلا أوروبا، وبعد الهبوط: قرابة الصفر!','ar'),
  beh("The banks that lent United money set one test: the club must keep earning at least £125m a year from its operations, checked every quarter. Fall below it and the lenders can stop lending. In the bad-finish case the club clears the line by only £10m; after relegation it is nowhere near."),
  srce('Key findings; section 1.3; section 2.2',"“The revolving credit facility (RCF), the secured term loan and the 5.36% notes due 2031 all require Consolidated Adjusted EBITDA of at least £125m per rolling 12 months, tested quarterly. The floor was raised from £65m in the June 2026 refinancing.”","“Scenario A… EBITDA to about £135m in FY2028… almost no room under the £125m covenant floor.” “Scenario B… EBITDA to about zero.”","Table 2.2: Adjusted EBITDA FY2026 216.4 · A (15th, no Europe) 135 · B (Championship, year 1) (3)."),
  chk("«الأرباح التشغيلية» is my plain-language label for «adjusted EBITDA» (earnings from running the club, before interest and amortisation). The report's own headroom row treats the covenant figure and the reported figure as the same, so the slide does too. £135m and «قرابة الصفر» (−£3m) are the report's estimates for 2027/28. The table uses 15th, the text says 14th to 17th, and the slide follows the text.")],
 "Headline: الخط الأحمر: ١٢٥ مليونًا!\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a single bright red line painted across the grass of an empty football pitch at dusk, seen from a high angle, floodlights behind. The pitch fills the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of a red velvet rope barrier across an empty stadium tunnel entrance, dim light, nobody present. The tunnel fills the top two thirds, the bottom third fades to black."),
  wm(("A real photo of Old Trafford's pitch or tunnel","Old Trafford pitch aerial; Old Trafford tunnel","Any wide pitch shot works. The red line idea can be added in the design. Check the licence.")),True))
# 4
mk(4,'What disappears with relegation',"ماذا يضيع بالهبوط؟",'Photo: empty stand',
 [('Headline (yellow)','ماذا يضيع بالهبوط؟','ar h'),
  ('Body','بثّ الدوري يتحول إلى تعويضات هبوط أقل بكثير، وأديداس تملك حق خفض دفعتها ٥٠٪، وإيرادات المباريات تنخفض نحو الثلث، فتنزل الإيرادات من ٦٧٨ إلى نحو ٣٩٢ مليونًا (تقدير)','ar'),
  beh("Three income streams are tied to the Premier League itself: the TV money, the kit deal and the crowd. Relegation does not remove them one by one, it removes the top level they sit on. The «parachute» is money paid to relegated clubs for a few years, and it is far smaller than normal league income (about £50m in the first year against about £195m)."),
  srce('Headline conclusions, Scenario B; table 2.2',"“Scenario B (relegation): revenue falls to circa £390m in 2027/28 and EBITDA to about zero. The drivers are the switch from Premier League distributions to parachute payments; adidas’ contractual right to cut its payment by 50% for any season outside the Premier League, and to terminate on one full season’s notice after relegation; matchday revenue down by about a third…”","Table 2.2: Total revenue FY2026 677.6 · B 392. Premier League central / parachute c.195 → 50."),
  chk("£678m is the real figure for the year to June 2026. £392m is the report's estimate for 2027/28 (the first season after relegation), so the slide says «تقدير». They are two seasons apart. The report says adidas «may» cut by 50%: it is a right, and the model assumes it is used. Matchday falls from £153.5m to £105m, which is about a third.")],
 "Headline: ماذا يضيع بالهبوط؟\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of rows of empty red stadium seats with a few seats folded up, side light, dust in the air, nobody present. The seats fill the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of an empty stadium turnstile and closed ticket window at night, shutters down, cold light, no readable text. The scene fills the top two thirds, the bottom third fades to black."),
  wm(("A real photo of empty seats at Old Trafford","Old Trafford empty seats","A close shot of seats avoids showing anyone. Check the licence.")),True))
# 5
mk(5,'The behind-the-numbers slide: costs do not fall as fast',"الإيرادات تسقط... والرواتب لا!",'Photo: training ground',
 [('Headline (yellow)','الإيرادات تسقط... والرواتب لا!','ar h'),
  ('Body','الهابطون في ٢٠٢٤/٢٥ خسروا نحو ٧٠ مليونًا إيرادات، وخفّضت الرواتب نحو ٢٩ مليونًا فقط، بحسب الهيئة المستقلة. ويونايتد، بحسب تقارير، لا يضع بنود هبوط في العقود، فتنخفض الرواتب ببيع اللاعبين وفقدان زيادات الأبطال.','ar'),
  beh("This is the human side of the money problem. Players signed on current wages. If a contract has no clause that cuts the pay after relegation, the club keeps paying the same salary on much smaller income. That is why income can fall quickly while the wage bill falls slowly."),
  srce('Section 4 (IFR); Key findings, «Player contracts give little protection»',"“…clubs relegated in 2024/25 lost about £70m of revenue on average while cutting wages by only about £29m.”","“The 20-F confirms that most first-team contracts include pay step-ups tied to the Champions League league stage… However, United have been reported as not usually negotiating relegation clauses. Wages would therefore fall only through the loss of Champions League step-ups and through player sales.”"),
  chk("The £70m and £29m are averages for clubs relegated in 2024/25 (the regulator's finding), not United's own numbers. The slide says so. «بحسب تقارير» on the relegation clauses is the report's own «reported»: it is not confirmed by a United document. «زيادات الأبطال» = the pay step-ups tied to the Champions League that fall away automatically.")],
 "Headline: الإيرادات تسقط... والرواتب لا!\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a row of football boots and a bib on a bench in an empty dressing room, a single hard light, nobody present, no readable names. The room fills the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of an empty training pitch at dawn with a line of cones and a single bag of footballs, mist, nobody present. The pitch fills the top two thirds, the bottom third fades to black."),
  wm(("A real photo of United's training ground or players in training","Manchester United Carrington training","Pick a wide shot. Check the licence.")),True))
# 6
mk(6,'The bill that does not change division',"القسط لا يعرف الدرجة!",'Photo: stadium bill',
 [('Headline (yellow)','القسط لا يعرف الدرجة!','ar h'),
  ('Body','على النادي نحو ٣٧٥ مليونًا أقساط انتقالات، منها نحو ٢١٨ مليونًا تُدفع خلال سنة، وتبقى واجبة الدفع في أي دوري يلعب فيه، ويستهلك أول موسم بعد الهبوط نحو ١٨٥ مليونًا من السيولة','ar'),
  beh("When a club buys a player it pays in instalments over several years. Those instalments are already signed. They do not shrink if the club drops a division, so the money going out stays the same just as the money coming in falls. The result in the first season after relegation is a heavy cash drain."),
  srce('Key findings, «Liquidity»; section 2.4',"“Transfer payables were £375.0m, about £218m of it due within a year, plus up to £122.8m of contingent fees. Summer 2026 signings added a further £191.7m of commitments.”","“Scenario B, year 1 absorbs about £185m, almost the whole undrawn RCF, because transfer instalments from earlier deals remain payable, season ticket and sponsor prepayments shrink, and EBITDA disappears.”"),
  chk("£375m and £218m are from the audited accounts (30 June 2026). £185m is the report's estimate of free cash flow for the first season after relegation, so the slide shows it as a drain on liquidity, not a fact already happened. I did not use the £191.7m of summer 2026 commitments on the slide: it is a separate number and would make the line too long.")],
 "Headline: القسط لا يعرف الدرجة!\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a long stadium corridor with a clock on the wall and a stack of unopened envelopes on a desk in the foreground, dim cold light, nobody present, no readable text. The corridor fills the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of a heavy ledger book closed on a desk beside a calculator in an empty office overlooking a floodlit stadium at night, no readable text. The window view fills the top two thirds, the bottom third fades to black."),
  wm(("A real photo of Old Trafford's exterior or offices","Old Trafford exterior; Old Trafford megastore","Any exterior shot. Check the licence.")),True))
# 7
mk(7,'One season survivable, two not',"سنة تُحتمل... وسنتان لا!",'Photo: Championship pitch',
 [('Headline (yellow)','سنة تُحتمل... وسنتان لا!','ar h'),
  ('Body','موسم هبوط واحد وصعود فوري يحتاجان ٥٠–١٠٠ مليون، وسنتان فأكثر تحتاجان ١٥٠–٤٠٠ مليون تمويلًا جديدًا، لأن إعفاء شرط الـ١٢٥ مليونًا لا يُمنح سنتين متتاليتين، وبيع اللاعبين لا ينقذه: أرباح بيعهم لا تُحتسب فيه.','ar'),
  beh("The lenders allow the club to miss the £125m test twice in the life of the notes, but never in two years running. One bad season can be forgiven. A second in a row is a breach, and then the banks could refuse new money. Selling players cannot fix it, because profit on player sales does not count in the test."),
  srce('Summary; Key findings; section 1.3; section 2.4',"“One season outside the Premier League is survivable. Two or more is not survivable without fresh equity.”","“The price of survival: immediate promotion plus about £50–100m of bridging capital is survivable. Two or more seasons down requires an estimated £150–400m of equity or refinancing…”","“The dispensation for missing the Champions League can be used only twice over the life of the notes, and never in consecutive financial years.” “Profit on player sales is excluded, so selling players cannot cure a breach.”"),
  chk("The £50–100m and £150–400m are the report's estimates. «لا يُمنح سنتين متتاليتين» is exact: the dispensation is for missing the Champions League league stage, and it cannot be used in consecutive years. In the model the second Championship year has EBITDA of about £16m against £125m, which is a breach unless lenders waive it. The «banks could refuse new money» point is from the 20-F as quoted in the report: «lenders could decline to extend further credit».")],
 "Headline: سنة تُحتمل... وسنتان لا!\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a half-empty lower-league football ground on a grey afternoon, a few supporters in a small stand, wet pitch, floodlights off, no readable signage. The ground fills the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of a calendar on a locker-room wall with two seasons crossed out in red marker, no readable dates or names. The wall fills the top two thirds, the bottom third fades to black."),
  wm(("A real photo of a Championship ground or a muddy pitch","Championship football ground; Elland Road; Turf Moor","Wikimedia has several lower-league ground photos. Check the licence.")),True))
# 8
mk(8,'Who pays: ownership and the missing safety net',"من يدفع الفاتورة؟",'Photo: Ratcliffe and Glazers',
 [('Headline (yellow)','من يدفع الفاتورة؟','ar h'),
  ('Body','لا التزام معلنًا على أي مساهم بتمويل خسائر النادي، وغليزر تملك ٦٧٫٩٪ من الأصوات، وإينيوس ٢٨٫٩٤٪، وسعر الـ٣٣ دولارًا الأدنى لراتكليف ينتهي في فبراير ٢٠٢٧، وبعد الهبوط يرى كاتب التقرير أن البيع الاضطراري الأرجح.','ar'),
  beh("If the club needs fresh money, nobody is obliged to supply it. The Glazer family controls the votes, INEOS runs football matters, and the two do not have a shared rule for who covers losses. The report's author argues that a forced sale would be the likeliest way to raise cash after relegation. This is his judgement, not a fact."),
  srce('Section 1.4; section 5',"“The Glazer family hold about 48.9% of the economic interest and 67.9% of the votes… INEOS Services Limited holds 28.94%, has operational control of football matters… Ratcliffe’s entitlement to a $33 per share minimum price in a Glazer-led sale lasts only until February 2027.”","“There is no disclosed obligation on any shareholder to fund losses… With the $33 price floor gone after February 2027, a distressed sale after relegation is the most likely route to fresh capital.”"),
  chk("The last line is the author's own judgement and the slide attributes it to «كاتب التقرير». The $33 floor is described as Ratcliffe's entitlement in the report, so the slide names him. Ownership percentages are from the 20-F. The change-of-control terms in the debt are second-hand in the report, so I did not use them. The photo you already have of Ratcliffe with two other men would suit this slide, but I cannot tell who the other two are, so check before using it.")],
 "Headline: من يدفع الفاتورة؟\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of three plain empty leather chairs around a long boardroom table with a stadium visible through the window at dusk, nobody present. The room fills the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of a single key and a folded document on a dark table beside a glowing window, stadium lights blurred outside, no readable text. The table fills the top two thirds, the bottom third fades to black."),
  wm(("A real photo of the owners or Old Trafford from the boardroom side","Jim Ratcliffe Old Trafford; Glazer family Old Trafford","You already have a Ratcliffe photo from INEOS slide 1 and slide 5. Check the licence on any new one.")),True))
# 9
mk(9,'History and the open question',"التاريخ يقول...",'Photo: old black and white stadium',
 [('Headline (yellow)','التاريخ يقول...','ar h'),
  ('Body','الأندية ذات الميزانية السليمة والملاك الملتزمين تعود سريعًا، ويونايتد نفسه هبط ١٩٧٤ وصعد ١٩٧٥ من أول محاولة، أما المثقلة بالديون كليدز وشالكه فدخلت دوامة. سيناريو افتراضي لا توقّع... شاركنا رأيك بالتعليقات!','ar'),
  beh("The report's pattern: the same relegation ends very differently depending on the balance sheet and the owners behind the club. A club without debt and with committed owners usually returns. A club carrying debt and contracted costs can spiral. The closing line repeats that this is a scenario, not a forecast."),
  srce('Historic comparables',"“The pattern is consistent: clubs with intact balance sheets and committed owners bounce back. Clubs relegated while carrying debt and contracted costs, Leeds, Schalke, spiral.”","Table: Manchester United relegated 1974, promoted at the first attempt in 1975 · Juventus 2006, promoted at the first attempt · Leeds 2004, administration in 2007, fell to League One · Schalke relegated 2021, promoted 2022, relegated again 2023."),
  chk("The comparables are the author's list; I kept the three that tell the story (United, Leeds, Schalke). The slide uses the report's words for «spiral». «لا توقّع» repeats the report's own warning. If you want a stronger closing question, change the last line. The report assigns no probability to relegation, so I did not add one.")],
 "Headline: التاريخ يقول...\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph in black and white of an old football stadium terrace with wooden stands and a lone fence, grain, soft light, nobody present. The terrace fills the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of an old tattered pennant hanging on a rusty stadium fence in the wind, shallow depth, muted tones, no readable text. The fence fills the top two thirds, the bottom third fades to black."),
  wm(("An archive-style photo of old Old Trafford, or the 1970s stands","Old Trafford 1970s; Old Trafford history","Look for public-domain or CC archive images. Check the licence.")),True))
