import json, re
SRC='../reference/old_planner_format.html'
lines=open(SRC,encoding='utf8').read().split('\n')
font_and_css='\n'.join(lines[4:126])          # lines 5..126 : @font-face + all css (1-indexed)
icons_svg=re.search(r'<div class="icons".*?</div>',lines[138],re.S).group(0)   # slide 9 icon row from the old plan

def ph(style,cls,label): return f'<div class="ph {cls}" style="{style}"><span>{label}</span></div>'
ARROW='<svg class="arrow" viewBox="0 0 24 12"><path d="M1 1l9 5-9 5zM12 1l9 5-9 5z" fill="currentColor"/></svg>'
MARK='<div class="mark">جول إنجليزي</div>'
def card(inner,arrow=True): return f'<div class="card" data-motion="1">{inner}{ARROW if arrow else ""}{MARK}</div>'
def rows(items):
    out=''
    for lab,txt,cls in items:
        c=f' class="{cls}"' if cls else ''
        out+=f'<div class="row"><b>{lab}</b><div{c}>{txt}</div></div>'
    motion='<div class="row"><b>Motion</b><div>The text rises in order, top to bottom. The photo zooms in slowly. About 6 seconds. <button type="button" class="replay">Replay motion</button></div></div>'
    return out+motion
RED={1:'«صمته» و «الوعود»',2:'«٢-١»',3:'«ثلاثة»',4:'«١٠» (والرقم الكبير)',5:'«واحدًا» (والرقم الكبير)',6:'«لم تكتمل»',7:'«وخذلني»',8:'«السامة»',9:'«١٤» و «إحكيلي»'}
def sec(n,total,title,card_html,items):
    idx=next((i for i,x in enumerate(items) if x[0]=='Check'),len(items))
    items=items[:idx]+[('Red mark',RED[n],'ar')]+items[idx:]
    return f'<section class="slide">{card_html}<div><p class="k">Slide {n} of {total}</p><h2>{title}</h2>{rows(items)}</div></section>'

RED={}
def sec(n,total,title,card_html,items):
    return f'<section class="slide">{card_html}<div><p class="k">Slide {n} of {total}</p><h2>{title}</h2>{rows(items)}</div></section>'
def Y(t): return f'<b class="y">{t}</b>'
def Rd(t): return f'<b class="r">{t}</b>'
def wcard(head,body,label,d0=.2):
    return (f'<div class="card w" data-motion="1">{ph("left:0;right:0;top:0;height:92cqw","wph",label)}<div class="wgrad"></div>'
            f'<div class="wtext"><div class="rs wh" style="--d:{d0}s">{head}</div><div class="rs wb" style="--d:{d0+.5}s">{body}</div></div></div>')
def src(ref,*lines):
    q=''.join(f'<span dir="rtl" style="display:block;margin-bottom:6px;text-align:right">{l}</span>' for l in lines)
    return ('From the report',q+f'<span style="display:block;color:#667085;font-size:13px">{ref}</span>','')
def noimg(size,comp,A,B,grab=None,fallback=False):
    return {"size":size,"comp":comp,"grab":grab,"fallback":fallback,"A":A,"B":B}
def wm(what): return {"what":what[0],"search":what[1],"where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":what[2]}
SZ="3:4 portrait, generate at 1080x1440 or larger"
COMP="The subject fills the top two thirds. Keep the bottom third dark and empty, because the text sits there on a black gradient."
RED={}
def sec(n,total,title,card_html,items):
    return f'<section class="slide">{card_html}<div><p class="k">Slide {n} of {total}</p><h2>{title}</h2>{rows(items)}</div></section>'
def Y(t): return f'<b class="y">{t}</b>'
def Rd(t): return f'<b class="r">{t}</b>'
def wcard(head,body,label,d0=.2):
    return (f'<div class="card w" data-motion="1">{ph("left:0;right:0;top:0;height:92cqw","wph",label)}<div class="wgrad"></div>'
            f'<div class="wtext"><div class="rs wh" style="--d:{d0}s">{head}</div><div class="rs wb" style="--d:{d0+.5}s">{body}</div></div></div>')
def src(ref,*lines):
    q=''.join(f'<span dir="rtl" style="display:block;margin-bottom:6px;text-align:right">{l}</span>' for l in lines)
    return ('From the report',q+f'<span style="display:block;color:#667085;font-size:13px">{ref}</span>','')
def noimg(size,comp,A,B,grab=None,fallback=False):
    return {"size":size,"comp":comp,"grab":grab,"fallback":fallback,"A":A,"B":B}
def wm(what): return {"what":what[0],"search":what[1],"where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":what[2]}
SZ="3:4 portrait, generate at 1080x1440 or larger"
COMP="The subject fills the top two thirds. Keep the bottom third dark and empty, because the text sits there on a black gradient."
RED={}
def sec(n,total,title,card_html,items):
    return f'<section class="slide">{card_html}<div><p class="k">Slide {n} of {total}</p><h2>{title}</h2>{rows(items)}</div></section>'
def Y(t): return f'<b class="y">{t}</b>'
def Rd(t): return f'<b class="r">{t}</b>'
def wcard(head,body,label,d0=.2,hs=None,bs=None):
    hst=f' style="--d:{d0}s;font-size:{hs}cqw"' if hs else f' style="--d:{d0}s"'
    bst=f' style="--d:{d0+.5}s;font-size:{bs}cqw"' if bs else f' style="--d:{d0+.5}s"'
    return (f'<div class="card w" data-motion="1">{ph("left:0;right:0;top:0;height:92cqw","wph",label)}<div class="wgrad"></div>'
            f'<div class="wtext"><div class="rs wh"{hst}>{head}</div><div class="rs wb"{bst}>{body}</div></div></div>')
import re as _re
def _plain(h): return _re.sub(r'<[^>]+>','',h)
def src(ref,*lines):
    q=''.join(f'<span dir="rtl" style="display:block;margin-bottom:6px;text-align:right">{l}</span>' for l in lines)
    return ('From the report',q+f'<span style="display:block;color:#667085;font-size:13px">{ref}</span>','')
def noimg(size,comp,A,B,grab=None,fallback=False):
    return {"size":size,"comp":comp,"grab":grab,"fallback":fallback,"A":A,"B":B}
def wm(what): return {"what":what[0],"search":what[1],"where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":what[2]}
SZ="3:4 portrait, generate at 1080x1440 or larger"
COMP="The subject fills the top two thirds. Keep the bottom third dark and empty, because the text sits there on a black gradient."
import base64 as _b64
def _jpg(n): return _b64.b64encode(open(f'ineos_jpg/{n}.jpg','rb').read()).decode()
# label: (photo no, bg-size start, bg-size end, bg-position, tall=full-card block)
PICS={}
_ph0=ph
def ph(style,cls,label):
    p=PICS.get(label)
    if not p: return _ph0(style,cls,label)
    n,b0,b1,pos,tall=p
    if tall: style=style.replace('height:92cqw','height:133.34cqw')
    if tall not in (True,False): style=style.replace('top:0','top:%scqw'%tall)
    return (f'<div class="ph has {cls}" style="{style}"><i class="pi" style="background-image:url(data:image/jpeg;base64,{_jpg(n)});'
            f'background-position:{pos};--bs0:{b0};--bs1:{b1}"></i></div>')
S=[];D=[];IMG=[]
T=9
def add(n,title,head,body,label,rows_,dtext,img):
    L=LINES.get(n,{})
    if 'head' in L: head=L['head']
    if 'lines' in L: body=''.join(f'<span class="bl">{l}</span>' for l in L['lines'])
    plain_lines=[_plain(l) for l in L.get('lines',[])]
    new_rows=[]
    for lab,txt,cls in rows_:
        if lab.startswith('Body') and plain_lines:
            new_rows.append(('Body (one line each, no colour crosses a line)','<br>'.join(plain_lines),'ar'))
        elif lab.startswith('Headline') and 'headrow' in L:
            new_rows.append(L['headrow'])
        else:
            new_rows.append((lab,txt,cls))
    if plain_lines:
        dtext=dtext[:dtext.index('\nBody:')]+'\nBody: '+'\n'.join(plain_lines)
    if 'headrow' in L:
        dtext=L['dtext']+"\nBody: "+'\n'.join(plain_lines)
    S.append(sec(n,T,title,wcard(head,body,label,hs=L.get('hs'),bs=L.get('bs')),new_rows)); D.append(dtext)
    if label in PICS: img=dict(img,have=f'Slide {PICS[label][0]} from your Drive folder, placed in the card')
    IMG.append(img)
# ---- Man Utd scenario carousel: content (exec'd inside plan8.py after helpers) ----
# ---- Man Utd scenario carousel: content (exec'd inside plan8.py after helpers) ----
# ---- Man Utd scenario carousel: content (exec'd inside plan8.py after helpers) ----
# ---- Man Utd scenario carousel v2 (plain-language, fewer numbers) ----
# ---- Man Utd scenario carousel v2 (plain-language, fewer numbers) ----
# ---- Man Utd scenario carousel v2 (plain-language, fewer numbers) ----
def srce(ref,*lines):
    q=''.join(f'<span dir="ltr" style="display:block;margin-bottom:6px;text-align:left">{l}</span>' for l in lines)
    return ('From the report',q+f'<span style="display:block;color:#667085;font-size:13px">{ref}</span>','')
def beh(t): return ('Behind the number',t,'')
def chk(t): return ('Check this',t,'')
def drf(t): return ('From your draft',t,'')
SZ="3:4 portrait, generate at 1080x1440 or larger"
COMP="The subject fills the top two thirds. Keep the bottom third dark and empty, because the text sits there on a black gradient."
def A_(s): return s+" Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no recognisable faces."
LINES={
1:{'head':'<span class="wk">يونايتد</span><span class="w2">لو هبط... المشكلة '+Rd('أكبر')+'!</span>',
   'headrow':('Line 1 yellow, line 2 white with a red word','يونايتد<br>لو هبط... المشكلة أكبر!','ar h'),
   'dtext':"Line 1: يونايتد\nLine 2: لو هبط... المشكلة أكبر!",
   'lines':['تقرير مالي يحلّل سيناريو الهبوط في ٢٠٢٦/٢٧،','ويشرح ما وراء الأرقام: '+Y('الديون والعقود')+' والرعاة']},
2:{'bs':4.5,'lines':['بعد ٩ مباريات: '+Y('٧ نقاط فقط')+'، والمركز ١٦ أو ١٧،',Rd('وبهذا المعدل: أقل من ٣٠ نقطة في الموسم.'),'والجدول هنا لا يعني الكبرياء فقط، بل '+Y('المال')+':','كل مركز أقل ودوري أبطال غائب يعنيان دخلًا أقل.']},
3:{'bs':4.5,'lines':['اقترض النادي بشرط أن يحقق '+Y('أرباحًا تشغيلية'),'لا تقل عن '+Y('١٢٥ مليونًا')+' في السنة،','وموسم سيئ بلا أوروبا يتركه فوق الخط بـ'+Y('١٠ ملايين')+' فقط،',Rd('أما الهبوط فيدفعها إلى ما يقارب الصفر.')]},
4:{'bs':4.4,'lines':['عقد أديداس يمنح النادي حدًا أدنى '+Y('٩٠ مليونًا في السنة')+'،','لكن لها حق '+Y('خفض الدفعة ٥٠٪')+' خارج الدوري الممتاز،',Rd('وإنهاء العقد بإشعار مدته موسم كامل بعد الهبوط،'),'ومعها بند خصم عشرة ملايين لموسم بلا دوري أبطال.']},
5:{'bs':4.5,'lines':['اشترى النادي لاعبين بالتقسيط، وعليه '+Y('نحو ٣٧٥ مليونًا'),'منها '+Y('نحو ٢١٨ مليونًا')+' خلال سنة واحدة،','وتبقى الأقساط واجبة في أي دوري يلعب فيه،',Rd('بينما يقلّ دخل المباريات والبث بعد الهبوط.')]},
6:{'bs':4.3,'lines':['الإيرادات تنهار بعد الهبوط، لكن الرواتب لا:','هابطو ٢٤/٢٥ خسروا '+Y('٧٠ مليونًا')+' وخفّضوا '+Y('٢٩')+' فقط،',Rd('ويونايتد، بحسب تقارير، لا يضع بنود هبوط في العقود،'),'فتنخفض الرواتب ببيع اللاعبين وفقدان زيادات الأبطال.']},
7:{'bs':4.3,'lines':['يخطط النادي لملعب جديد بنحو '+Y('ملياري جنيه')+' وبتمويل خاص،','ومع الهبوط يتعذّر تمويله '+Y('تجاريًا')+' حتى الصعود،','فالمقرضون لن يموّلوا التسمية والمقاعد المميزة',Rd('على دخل الدرجة الثانية، وحتى الموسم السيئ يؤخّره.')]},
8:{'bs':4.3,'lines':['أول موسم بعد الهبوط يستهلك '+Y('نحو ١٨٥ مليونًا')+' نقدًا (تقدير)،','أي تقريبًا كل '+Y('الائتمان المتبقي: ٢٠٠ مليون')+'،',Rd('ولا التزام معلنًا على أي مساهم بتغطية الخسائر،'),'ويرى كاتب التقرير أن '+Y('البيع الاضطراري')+' الأرجح بعد الهبوط.']},
9:{'hs':8.2,'bs':4.3,'lines':['سنة واحدة خارج الدوري الممتاز '+Y('تُحتمل')+' لو صعد فورًا،',Rd('لكن سنتين متتاليتين تخرقان شرط البنوك إلا بتساهلهم،'),'والتاريخ منقسم: عاد يونايتد ١٩٧٥، ودخل '+Y('ليدز')+' دوامة.','سيناريو افتراضي لا توقّع... '+Y('شاركنا رأيك بالتعليقات!')]},
}
def mk(n,title,head,label,rows_,dtext,img): add(n,title,head,'',label,rows_,dtext,img)
# 1
mk(1,'Hook: the question, then the promise to explain',"",'Photo: Old Trafford night',
 [('Headline (yellow, red word)','يونايتد · لو هبط... المشكلة أكبر!','ar h'),
  ('Body','تقرير مالي يحلّل سيناريو الهبوط في ٢٠٢٦/٢٧، ويشرح ما وراء الأرقام: الديون والعقود والرعاة','ar'),
  beh("The report's point in one sentence: relegation would be a financing problem, not only a drop in income. The hook says «لو» (if), so nobody reads it as a prediction."),
  drf("Your draft's slide 1 was the INEOS slide («إنيوس»), copied over from the last carousel, so I dropped it and wrote a hook for this report."),
  srce('Summary, first paragraph',"“Relegation at the end of 2026/27 would be a solvency and financing event for Manchester United, not merely a revenue shock.”","“This is conditional scenario analysis for public discussion, not a forecast that Manchester United will be relegated, and not investment advice.”"),
  chk("The report says outright that this is not a forecast, so the hook is conditional. Please credit The Esk and Paul Quinn in the caption.")],
 "Line 1: يونايتد\nLine 2: لو هبط... المشكلة أكبر!\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a huge empty football stadium at night under floodlights, rows of empty red seats curving away, mist on the pitch."+" The stand fills the top two thirds, the bottom third falls to deep shadow."),
  A_("Editorial photograph of a football stadium exterior at dusk with a single glowing sign above a locked gate, cold blue light, nobody present."),
  wm(("A real photo of Old Trafford at night","Old Trafford floodlights; Old Trafford at night","You already placed a real Old Trafford photo on INEOS slide 8. A different angle keeps the two carousels apart. Check the licence.")),True))
# 2
mk(2,'Where they are now, and why the table means money',"بداية متعثرة",'Photo: dejected players',
 [('Headline (yellow)','بداية متعثرة','ar h'),
  ('Body','بعد ٩ مباريات: ٧ نقاط فقط، والمركز ١٦ أو ١٧، وبهذا المعدل: أقل من ٣٠ نقطة في الموسم. والجدول هنا لا يعني الكبرياء فقط، بل المال: كل مركز أقل ودوري أبطال غائب يعنيان دخلًا أقل.','ar'),
  beh("A place in the table is not only pride. The report values each league place at about £3.5m of prize money (its assumption), and missing European football removes income and also the pay rises the club had planned around."),
  drf("Kept your idea that results turn into money, but only as «دخل أقل» and without saying survival is at risk. Missing Europe alone is «painful but manageable» in the report."),
  srce('Key findings, «Position at 1 November 2026»; section 1.2',"“United are 16th–17th in the Premier League after nine games with 7 points… Over 38 games, that rate would produce fewer than 30 points.”","“I estimate the 2026/27 merit payment at about £45m lower at 16th than at 3rd (assuming £3.5m per place).”","“A 14th–17th place finish without European football is painful but manageable.”"),
  chk("The report says sources differ on 16th or 17th, so the slide says «١٦ أو ١٧». I left out «winless in nine across all competitions»: it sits oddly next to W1 in nine league games. The per-place value is the author's assumption, so the slide gives no figure for it.")],
 "Headline: بداية متعثرة\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of two footballers in red kit seen from behind walking off an empty pitch after a match, heads down, stadium lights glowing, no readable numbers or names. The scene fills the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of a stadium scoreboard glowing in the dark above empty stands, the numbers blurred and unreadable, cold light."),
  wm(("A real photo of United players after a defeat or a draw","Manchester United players dejected Old Trafford","Choose a wide shot where faces are small. Check the licence.")),True))
# 3
mk(3,'The bank line',"خط البنوك",'Photo: red line',
 [('Headline (yellow)','خط البنوك','ar h'),
  ('Body','اقترض النادي بشرط أن يحقق أرباحًا تشغيلية لا تقل عن ١٢٥ مليونًا في السنة، وموسم سيئ بلا أوروبا يتركه فوق الخط بـ١٠ ملايين فقط، أما الهبوط فيدفعها إلى ما يقارب الصفر.','ar'),
  beh("The banks that lent United money set one test: the club must keep earning at least £125m a year from running the club, checked every quarter. In a bad finish the club clears the line by only £10m. After relegation it is nowhere near. Selling players cannot cure it, because profit on sales does not count."),
  drf("Your «شرط خفي» becomes «خط البنوك»: the covenant is public (it is in the 20-F), not hidden. Your «prevents borrowing» is softened: a breach lets lenders decline further credit, and the first bad season uses the one-year dispensation."),
  srce('Key findings; section 1.3; section 2.2',"“…all require Consolidated Adjusted EBITDA of at least £125m per rolling 12 months, tested quarterly. The floor was raised from £65m in the June 2026 refinancing.”","“A 14th–17th place finish without European football… EBITDA falls to about £135m in FY2028, only about £10m above the covenant floor.”","“Scenario B (relegation): … EBITDA to about zero.”"),
  chk("«أرباح تشغيلية» is my plain label for adjusted EBITDA (earnings from running the club, before interest and amortisation). It is not the club's net result: the club reported a net loss of £43.0m for FY2026. The £135m and the «ما يقارب الصفر» (−£3m) are the report's estimates for 2027/28.")],
 "Headline: خط البنوك\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a single bright red line painted across the grass of an empty football pitch at dusk, seen from a high angle, floodlights behind. The pitch fills the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of a red velvet rope barrier across an empty stadium tunnel entrance, dim light, nobody present."),
  wm(("A real photo of Old Trafford's pitch or tunnel","Old Trafford pitch aerial; Old Trafford tunnel","Any wide pitch shot works. The red line can be added in the design. Check the licence.")),True))
# 4
mk(4,'The adidas deal',"صفعة أديداس",'Photo: kit',
 [('Headline (yellow)','صفعة أديداس','ar h'),
  ('Body','عقد أديداس يمنح النادي حدًا أدنى ٩٠ مليونًا في السنة، لكن لها حق خفض الدفعة ٥٠٪ في أي موسم خارج الدوري الممتاز، وإنهاء العقد بإشعار مدته موسم كامل بعد الهبوط، ومعها بند خصم عشرة ملايين لموسم بلا دوري أبطال.','ar'),
  beh("A kit deal sounds safe, but it carries conditions tied to the club's level. Outside the Premier League, adidas can pay half. After relegation it can also give a full season's notice to end the deal. The effect is that relegation hits the club's income in two places at once: the league and the sponsor."),
  drf("Kept your «صفعة أديداس». Corrected: the £90m is per year (£900m over 10 years), the 50% cut applies to any season outside the Premier League (not «immediately»), and ending the deal needs a full season's notice (not «cancelled after one season»)."),
  srce('Section 3 (commercial contracts)',"adidas: “£90m minimum guarantee (£900m over 10 years) – verified; −£10m per season without the Champions League; −50% in any year outside the Premier League; termination on one full season’s notice if relegated.”","Scenario B: “adidas at 50%” (£40m in a year outside the Premier League)."),
  chk("The report says adidas «may» cut or terminate: they are rights, and the model assumes the cut is used. I wrote the rights as rights. «بحد أدنى» matches the report's «minimum guarantee».")],
 "Headline: صفعة أديداس\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a neatly folded red football shirt and a pair of boots on a dressing-room bench, side light, no logos, no readable text. The bench fills the top two thirds, the bottom third falls to black."),
  A_("Editorial photograph of a stack of unsigned contract pages with a pen resting across them on a dark table beside a window with a stadium at dusk, no readable text."),
  wm(("A real photo of United players in training or a wide shot of the kit","Manchester United training kit; Old Trafford players","Avoid close-ups of logos. Check the licence.")),True))
# 5
mk(5,'The bill that does not change division',"فواتير معلقة",'Photo: stadium bill',
 [('Headline (yellow)','فواتير معلقة','ar h'),
  ('Body','اشترى النادي لاعبين بالتقسيط، وعليه نحو ٣٧٥ مليونًا، منها نحو ٢١٨ مليونًا خلال سنة واحدة، وتبقى الأقساط واجبة في أي دوري يلعب فيه، بينما يقلّ دخل المباريات والبث بعد الهبوط.','ar'),
  beh("Clubs pay for players in instalments over several years, and those payments are already signed. They do not shrink when the club drops a division, so the money going out stays the same just as the money coming in falls."),
  drf("Kept your «فواتير معلقة». Corrected: exactly £375.0m (not «more than»), only about £218m of it is due within a year (not «immediately»), and income from tickets and TV falls (not «lost»). I wrote «الدرجة الثانية» elsewhere, because the Championship is the second tier."),
  srce('Key findings, «Liquidity»; section 2.4',"“Transfer payables were £375.0m, about £218m of it due within a year, plus up to £122.8m of contingent fees.”","“…transfer instalments that remain payable whatever division the club is in.”"),
  chk("£375.0m and about £218m are from the audited accounts at 30 June 2026. The slide says «تقسيط», the report's word is «instalments».")],
 "Headline: فواتير معلقة\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a long stadium corridor with a clock on the wall and a stack of unopened envelopes on a desk in the foreground, dim cold light, nobody present, no readable text."),
  A_("Editorial photograph of a heavy ledger book closed on a desk beside a calculator in an empty office overlooking a floodlit stadium at night, no readable text."),
  wm(("A real photo of Old Trafford's exterior or offices","Old Trafford exterior; Old Trafford megastore","Any exterior shot. Check the licence.")),True))
# 6
mk(6,'Income falls fast, wages do not',"رواتب عالقة",'Photo: training ground',
 [('Headline (yellow)','رواتب عالقة','ar h'),
  ('Body','الإيرادات تنهار بسرعة بعد الهبوط، لكن الرواتب لا: الهابطون في ٢٠٢٤/٢٥ خسروا ٧٠ مليونًا وخفّضوا الرواتب ٢٩ فقط، ويونايتد، بحسب تقارير، لا يضع بنود هبوط في العقود، فتنخفض الرواتب ببيع اللاعبين وفقدان زيادات الأبطال.','ar'),
  beh("Players signed on current wages. If a contract has no clause that cuts pay after relegation, the club keeps paying the same salary on much smaller income. That is the human side of the money problem: the cost does not fall as fast as the income."),
  drf("Replaces your «تضحية بالعمال». Dropped: staff austerity is not in this report (that came from the INEOS report). Fixed: absent relegation clauses means no protection, not a guarantee of it."),
  srce('Section 4 (IFR); Key findings, «Player contracts give little protection»',"“…clubs relegated in 2024/25 lost about £70m of revenue on average while cutting wages by only about £29m.”","“…most first-team contracts include pay step-ups tied to the Champions League league stage… United have been reported as not usually negotiating relegation clauses. Wages would therefore fall only through the loss of Champions League step-ups and through player sales.”"),
  chk("£70m and £29m are averages for all clubs relegated in 2024/25 (the regulator's finding), not United's own numbers. The slide says «الهابطون». «بحسب تقارير» is the report's own «reported»: it is not confirmed by a United document.")],
 "Headline: رواتب عالقة\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a row of football boots and a bib on a bench in an empty dressing room, a single hard light, nobody present, no readable names."),
  A_("Editorial photograph of an empty training pitch at dawn with a line of cones and a single bag of footballs, mist, nobody present."),
  wm(("A real photo of United's training ground or players in training","Manchester United Carrington training","Pick a wide shot. Check the licence.")),True))
# 7
mk(7,'The stadium plan',"حلم مهدد",'Photo: stadium plan',
 [('Headline (yellow)','حلم مهدد','ar h'),
  ('Body','يخطط النادي لملعب جديد بنحو ملياري جنيه وبتمويل خاص، ومع الهبوط يصبح تمويله غير ممكن بشروط تجارية حتى الصعود، فالمقرضون لن يموّلوا حقوق التسمية والمقاعد المميزة على دخل الدرجة الثانية، وحتى موسم سيئ بلا هبوط يؤخّر التمويل.','ar'),
  beh("A stadium this size is paid for with future income: naming rights, premium seats and borrowing. If the club is in the second tier, lenders will not count on that income, so they will not fund it until the club is back up."),
  drf("Kept your «حلم مهدد». Corrected: not «frozen completely». In the bad-finish case the financing is delayed, and after relegation it is unfinanceable on commercial terms until promotion. The report names lenders, not «investors»."),
  srce('Section 5, «Stadium»',"“The plan is a £2bn, 100,000-seat stadium, to be privately financed… Scenario A delays the financing. Scenario B makes it unfinanceable on commercial terms until promotion: lenders will not underwrite naming rights, premium seating or debt capacity on Championship cash flows.”"),
  chk("The line is conditional («مع الهبوط»), as the report is. The slide does not give the completion year (2035) or the land cost, to keep the number count down.")],
 "Headline: حلم مهدد\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of an architectural model of a huge football stadium on a table under a single spotlight in a dark room, nobody present, no readable text."),
  A_("Editorial photograph of an empty construction site at dusk with a crane and a stadium outline in the distance, no people, no readable signage."),
  wm(("A real photo of Old Trafford from above, or of the land beside it","Old Trafford aerial view","Check the licence.")),True))
# 8
mk(8,'The cash drain and who covers it',"نزيف السيولة",'Photo: owners',
 [('Headline (yellow)','نزيف السيولة','ar h'),
  ('Body','أول موسم بعد الهبوط يستهلك نحو ١٨٥ مليونًا نقدًا (تقدير)، أي تقريبًا كل الائتمان المتبقي: ٢٠٠ مليون، ولا التزام معلنًا على أي مساهم بتغطية الخسائر، ويرى كاتب التقرير أن البيع الاضطراري الأرجح بعد الهبوط.','ar'),
  beh("Besides the bank line, the club has a credit facility it can draw on: about £200m is still undrawn out of £400m. The first season after relegation would use almost all of it. And nobody is obliged to put new money in, so it is not automatic that the owners will."),
  drf("Kept your «نزيف السيولة». Corrected: the report's own table gives about £185m in year 1, not «18 months» (its summary says 18 months, so the report is inconsistent). «Owners forced» is dropped: the report says there is no disclosed obligation to fund losses. A forced sale is only the author's view of the likeliest route."),
  srce('Section 2.4; section 5; Key findings',"“Scenario B, year 1 absorbs about £185m, almost the whole undrawn RCF…”","“RCF drawings were £110m at year end and £200m by 21 September 2026, out of a £400m facility, leaving about £200m of headroom.”","“There is no disclosed obligation on any shareholder to fund losses… a distressed sale after relegation is the most likely route to fresh capital.”"),
  chk("£185m is an estimate and the slide says so. The last line is the author's judgement and the slide attributes it to «كاتب التقرير». The photo you already have of Ratcliffe with two other men would suit this slide, but I can't tell who the other two are, so check before using it.")],
 "Headline: نزيف السيولة\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of an hourglass almost empty of sand on a table in an empty stadium executive box at dusk, nobody present."),
  A_("Editorial photograph of a fuel gauge needle at empty on a dark dashboard with a stadium glowing in the distance through the windscreen, no readable text."),
  wm(("A real photo of the owners or Old Trafford from the boardroom side","Jim Ratcliffe Old Trafford; Glazer family Old Trafford","You already have a Ratcliffe photo from INEOS slides 1 and 5. Check the licence on any new one.")),True))
# 9
mk(9,'One season survivable, two not, plus history and the question',"سنة تُحتمل... وسنتان لا!",'Photo: lower-league ground',
 [('Headline (yellow)','سنة تُحتمل... وسنتان لا!','ar h'),
  ('Body','سنة واحدة خارج الدوري الممتاز تُحتمل لو صعد فورًا، لكن سنتين متتاليتين تخرقان شرط البنوك إلا بتساهلهم، والتاريخ منقسم: عاد يونايتد ١٩٧٥، ودخل ليدز دوامة. سيناريو افتراضي لا توقّع... شاركنا رأيك بالتعليقات!','ar'),
  beh("The bank test can be missed in one year but not two years running. One bad season can be forgiven if the club bounces straight back, and the report says that is what clubs with sound finances and committed owners usually do. Clubs already carrying debt tend to spiral."),
  drf("Replaces your «ضياع شامل». Dropped: «الهاوية», «who is responsible», «the model collapsed» and the blame tone. The report is conditional, has no probability for relegation, and says the club is solvent today."),
  srce('Summary; section 2.4; Historic comparables',"“One season outside the Premier League is survivable. Two or more is not survivable without fresh equity.”","“Scenario B-ii: FY2029 EBITDA of about £16m against a £125m floor, with no dispensation available in consecutive years, is a covenant breach unless lenders waive it.”","“The pattern is consistent: clubs with intact balance sheets and committed owners bounce back. Clubs relegated while carrying debt and contracted costs, Leeds, Schalke, spiral.” Manchester United relegated 1974, promoted at the first attempt in 1975."),
  chk("The comparables are the author's list: I kept United (1975) and Leeds. «إلا بتساهلهم» is the report's «unless lenders waive it». I did not add a probability of relegation: the report assigns none.")],
 "Headline: سنة تُحتمل... وسنتان لا!\nBody: x",
 noimg(SZ,COMP,
  A_("Editorial photograph of a half-empty lower-league football ground on a grey afternoon, a few supporters in a small stand, wet pitch, floodlights off, no readable signage."),
  A_("Editorial photograph in black and white of an old football stadium terrace with wooden stands and a lone fence, grain, soft light, nobody present."),
  wm(("A real photo of a Championship ground or a muddy pitch","Championship football ground; Elland Road; Turf Moor","Wikimedia has several lower-league ground photos. Check the licence.")),True))

th='padding:6px 8px;border-bottom:1px solid var(--line)'
def tr(*c): return '<tr>'+''.join(f'<td style="padding:6px 8px;vertical-align:top">{x}</td>' for x in c)+'</tr>'
sources=f'''<div style="margin:0 0 34px;padding:18px 20px;border:1px solid var(--line);border-radius:10px;background:#FBFCFE"><h2 style="margin:0 0 6px;font-size:20px">Source: The Esk, «The Analysis Series», by Paul Quinn, 1 November 2026</h2><p style="margin:0 0 12px;color:var(--mute)">Design: your winning carousel (full-bleed photo, yellow headline, white text, yellow and red highlights). Copy: version 2, rebuilt after your review of the Gemini-style 9-slide draft. Fewer numbers (at most two per slide), short two-word headlines, and each slide explains what is behind the figure. Every slide has a «From your draft» row that says what I took, fixed or dropped, so you can decide. Each right-hand column shows the report's exact sentence and what to check. The report is a scenario, not a forecast, and the slides say so. Estimates are labelled «تقدير».</p><div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;min-width:560px;font-size:14px"><tr style="text-align:left;color:var(--mute)"><th style="{th}">Report term</th><th style="{th}">Plain Arabic on the slide</th><th style="{th}">What it means</th></tr>
{tr('Adjusted EBITDA','الأرباح التشغيلية','Earnings from running the club, before interest and amortisation')}
{tr('Covenant','شرط البنوك','The lenders’ test: at least £125m a year or they can stop lending')}
{tr('Parachute payments','تعويضات الهبوط','Money paid to relegated clubs for a few years')}
{tr('Champions League step-ups','زيادات الأبطال','Pay rises in player contracts triggered by Champions League football')}
{tr('Transfer payables','أقساط انتقالات','Instalments still owed on players already bought')}
{tr('Dispensation','إعفاء','The two years the covenant can be missed, never in a row')}
</table></div></div>'''


HEAD=f'''<meta name="claude:viewport-fit-sides" content="cover">
<title>Man Utd Scenario Plan</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Figtree:wght@400;600;700&display=swap">
<style>
{font_and_css}
body{{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px;background:var(--white)}}
.row>div,.boxes>div,.pgrid>div,.slide>div{{min-width:0}}
.card.w{{background:#000;box-shadow:none;container-type:inline-size}}
.card.w .wph{{background:repeating-linear-gradient(135deg,#2c3037 0 2.2cqw,#24272d 2.2cqw 4.4cqw);color:#9aa3b0}}
.card.w .wph span{{background:rgba(0,0,0,.55);color:#cdd3dc}}
.card.w .wgrad{{left:0;right:0;top:0;bottom:0;background:linear-gradient(to bottom,rgba(0,0,0,0) 0,rgba(0,0,0,0) 40%,rgba(0,0,0,.7) 56%,#000 68%,#000 100%)}}
.card.w .wtext{{left:7.5cqw;right:7.5cqw;bottom:13cqw;display:flex;flex-direction:column;gap:3.2cqw;text-align:center}}
.card.w .wh{{font-family:"MBA","Amiri",serif;font-size:9.6cqw;line-height:1.2;color:#FFD84D;text-shadow:0 .5cqw 1.4cqw rgba(0,0,0,.6);text-wrap:balance}}
.card.w .wb{{font-family:"Amiri",serif;font-weight:700;font-size:4.9cqw;line-height:1.62;color:#fff;text-wrap:pretty}}
.card.w .bl{{display:block;white-space:nowrap}}
.card.w .wk{{display:block;font-size:19cqw;line-height:1.05;text-shadow:0 .5cqw 1.4cqw rgba(0,0,0,.6)}}
.card.w .w2{{display:block;font-size:8.8cqw;line-height:1.2;margin-top:1.4cqw;color:#fff}}
.card.w .wph.has{{background:#000}}
.card.mo.w .ph.has{{animation:none}}
.card.w .y{{color:#FFD84D;font-weight:700}}
.card.w .r{{color:#FF3B30;font-weight:700}}
.ph.fbs::after{{background:linear-gradient(to bottom,#fff 0,rgba(255,255,255,.85) 4%,rgba(255,255,255,.4) 11%,rgba(255,255,255,0) 24%)}}
</style>'''
BODY=f'''<div class="wrap"><h1>Man Utd relegation scenario, version 2: words, positions and images</h1><p class="lead">Nine slides on plain white, 3:4 (1080x1440), photo about 60% and text about 40%. Under each slide: Keep, Drop or Change, edit the text, position notes, and the image brief with Prompt A (main look) and Prompt B (a different take) for ChatGPT image generation. Copy everything at the end.</p><div class="rules"><span><i class="sw" style="background:var(--navy)"></i>Navy: headlines</span><span><i class="sw" style="background:var(--red)"></i>Red: the one key word or number</span><span><i class="sw" style="background:var(--green)"></i>Green: small details only</span><span>Generated images show generic scenes only, never a recognisable person.</span></div>
{sources}
{chr(10).join(S)}
<div class="finish">
 <h2>Finish and send</h2>
 <p class="tally" id="tally">Nothing decided yet.</p>
 <button class="copybtn" id="copyAll" type="button">Copy all notes</button><span class="copymsg" id="copymsg" role="status"></span>
 <textarea class="out" id="out" readonly hidden aria-label="All notes as text"></textarea>
 <p class="note">Nothing is saved while you type. Press the button when you are done, then paste it to me in chat. Do not close this page before you copy.</p>
</div></div>'''
JS1='''<script>
(function(){
var D=%s;
var IMG=%s;
var LBL={keep:"KEEP",drop:"DROP",change:"CHANGE"};
var state=D.map(function(){return {v:"",t:null,p:"",a:null,b:null,n:""}});
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
var secs=document.querySelectorAll("section.slide");
secs.forEach(function(sec,i){
 var im=IMG[i];
 var panel=document.createElement("div");panel.className="fb-panel";
 var grab="";
 if(im.grab){grab='<div class="grab"><b>Image you grab yourself:</b> '+esc(im.grab.what)+'<br><b>Search:</b> '+esc(im.grab.search)+'<br><b>Where:</b> '+esc(im.grab.where)+'<br>'+esc(im.grab.note)+'</div>';}
 var prompts='<p class="imeta">'+(im.fallback?'Fallback only, if you cannot find the real photo. It is a generic image, not the real thing.':'Generate with ChatGPT image generation.')+'</p>'+
  '<div class="pgrid"><div><label for="a'+i+'">Prompt A: main look <button type="button" class="cp" data-for="a'+i+'">Copy</button></label><textarea id="a'+i+'"></textarea></div>'+
  '<div><label for="b'+i+'">Prompt B: a different take <button type="button" class="cp" data-for="b'+i+'">Copy</button></label><textarea id="b'+i+'"></textarea></div></div>';
 panel.innerHTML='<div class="fb-head"><strong>Slide '+(i+1)+': your decision</strong><div class="tabs" role="group" aria-label="Decision for slide '+(i+1)+'">'+
 '<button type="button" class="tab" data-v="keep" aria-pressed="false">Keep</button>'+
 '<button type="button" class="tab" data-v="drop" aria-pressed="false">Drop</button>'+
 '<button type="button" class="tab" data-v="change" aria-pressed="false">Change</button></div></div>'+
 '<div class="boxes"><div><label for="t'+i+'">1. The text (edit it here)</label><textarea id="t'+i+'" dir="auto"></textarea></div>'+
 '<div><label for="p'+i+'">2. Position or layout notes</label><textarea id="p'+i+'" class="pos" placeholder="For example: move the number lower, make the headline bigger, photo on the right"></textarea></div></div>'+
 '<div class="imgbox"><h3>Image for this slide</h3>'+(im.have?'<p class="imeta"><b>Image you have:</b> '+esc(im.have)+'</p>':'')+'<p class="imeta"><b>Size:</b> '+esc(im.size)+'. <b>Composition:</b> '+esc(im.comp)+'</p>'+grab+prompts+
 '<textarea id="n'+i+'" class="inote" placeholder="Image notes or a change request, for example: use a different scene, or I will use my own photo"></textarea></div>';
 sec.insertAdjacentElement("afterend",panel);
 var ta=panel.querySelector("#t"+i),pa=panel.querySelector("#p"+i),na=panel.querySelector("#n"+i);
 ta.value=D[i];
 ta.addEventListener("input",function(){state[i].t=ta.value;tally()});
 pa.addEventListener("input",function(){state[i].p=pa.value;tally()});
 na.addEventListener("input",function(){state[i].n=na.value;tally()});
 var aa=panel.querySelector("#a"+i),bb=panel.querySelector("#b"+i);
 aa.value=im.A;bb.value=im.B;
 aa.addEventListener("input",function(){state[i].a=aa.value});
 bb.addEventListener("input",function(){state[i].b=bb.value});
 panel.querySelectorAll(".cp").forEach(function(btn){btn.addEventListener("click",function(){
  var el=panel.querySelector("#"+btn.getAttribute("data-for"));
  var done=function(){var o=btn.textContent;btn.textContent="Copied";setTimeout(function(){btn.textContent=o},1400)};
  var fb=function(){el.focus();el.select();btn.textContent="Select and copy";};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(el.value).then(done,fb)}else{fb()}
 })});
 panel.querySelectorAll(".tab").forEach(function(b){b.addEventListener("click",function(){
  var v=b.getAttribute("data-v");state[i].v=(state[i].v===v)?"":v;
  panel.querySelectorAll(".tab").forEach(function(x){x.setAttribute("aria-pressed",String(x.getAttribute("data-v")===state[i].v))});
  panel.classList.toggle("dropped",state[i].v==="drop");tally();});});
});
function tally(){
 var c={keep:0,drop:0,change:0},n=0;state.forEach(function(s){if(s.v){c[s.v]++;n++}});
 document.getElementById("tally").textContent=n?("Decided "+n+" of "+D.length+": "+c.keep+" keep, "+c.drop+" drop, "+c.change+" change."):"Nothing decided yet.";
}
function build(){
 var out=["MAN UTD SCENARIO CAROUSEL FEEDBACK","Slides: "+D.length,""];
 state.forEach(function(s,i){
  var txt=(s.t===null)?D[i]:s.t, changed=(txt!==D[i]), im=IMG[i];
  out.push("=== SLIDE "+(i+1)+" ===");
  out.push("Decision: "+(s.v?LBL[s.v]:"NOT DECIDED"));
  out.push("Text edited: "+(changed?"YES":"no"));
  out.push("TEXT:");out.push(txt);
  out.push("POSITION NOTES: "+(s.p.trim()||"(none)"));
  out.push("IMAGE SIZE: "+im.size);
  if(im.grab){out.push("IMAGE TO GRAB: "+im.grab.what+" (search: "+im.grab.search+")")}
  var a=(s.a===null)?im.A:s.a,b=(s.b===null)?im.B:s.b;
  out.push("PROMPT A edited: "+((a!==im.A)?"YES":"no"));
  if(a!==im.A){out.push("PROMPT A: "+a)}
  out.push("PROMPT B edited: "+((b!==im.B)?"YES":"no"));
  if(b!==im.B){out.push("PROMPT B: "+b)}
  out.push("IMAGE NOTES: "+(s.n.trim()||"(none)"));
  out.push("");
 });
 return out.join("\\n");
}
var btn=document.getElementById("copyAll"),msg=document.getElementById("copymsg"),box=document.getElementById("out");
btn.addEventListener("click",function(){
 var t=build();box.value=t;box.hidden=false;
 function fallback(){box.focus();box.select();msg.style.color="#7A5200";msg.textContent="Select the text below and copy it."}
 if(navigator.clipboard&&navigator.clipboard.writeText){
  navigator.clipboard.writeText(t).then(function(){msg.style.color="";msg.textContent="Copied. Paste it to me in chat."},fallback);
 }else{fallback()}
});
})();
</script>''' % (json.dumps(D,ensure_ascii=False), json.dumps(IMG,ensure_ascii=False))
JS2='\n'.join(lines[245:265])   # motion script from old plan (<script> ... </script>)
out=HEAD+'\n'+BODY+'\n'+JS1+'\n'+JS2+'\n'
OUT='manutd_scenario_plan.html'
open(OUT,'w',encoding='utf8').write(out)
print(len(out))
