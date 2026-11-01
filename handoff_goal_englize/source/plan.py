import json, re
SRC='/root/.claude/projects/-home-user-goal-englize-watcher/3795416f-4611-5512-bdea-dc096a1a5987/tool-results/artifact-488d4a6f-1791714197-35fe.html'
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

S=[];D=[];IMG=[]
T=9
# ---------- 1 cover
S.append(sec(1,T,'Text on top, photo in the lower 63%, forward arrow',card(
 '<div class="tz" style="right:7cqw;left:7cqw;top:5cqw;height:51cqw"><div class="rs c-h" style="--d:.2s;font-size:7.4cqw">تن هاغ يكسر <span class="hl">صمته</span> عن يونايتد<span style="display:block;font-size:4.6cqw;margin-top:1.5cqw">بعد سنتين من إقالته: <span class="hl">الوعود</span> لم تُحترم</span></div><div class="rs c-b" style="--d:.7s;margin-top:6.5cqw">مقابلة حصرية مع The Athletic</div><div class="rs c-b" style="--d:.9s;margin-top:1.5cqw">ماذا قال عن الإدارة وكين ورونالدو؟</div></div>'
 +ph('left:0;right:0;bottom:0;height:84cqw','fb bf','Photo: Ten Hag'),True),[
 ('Headline','تن هاغ يكسر صمته عن يونايتد','ar h'),
 ('Second line','بعد سنتين من إقالته: الوعود لم تُحترم','ar'),
 ('Body 1','مقابلة حصرية مع The Athletic','ar'),
 ('Body 2','ماذا قال عن الإدارة وكين ورونالدو؟','ar'),
 ('Check','The article says he kept silent for two years since the October 2024 sacking. «لم تُحترم» is my paraphrase of his quote «the promises, they didn\'t keep».','')]))
D.append("Headline: تن هاغ يكسر صمته عن يونايتد\nSecond line: بعد سنتين من إقالته: الوعود لم تُحترم\nBody 1: مقابلة حصرية مع The Athletic\nBody 2: ماذا قال عن الإدارة وكين ورونالدو؟")
IMG.append({"size":"1:1 square, generate at 1024x1024 or larger","comp":"Keep the top fifth open and bright, it fades into the white. Subject sits in the lower two thirds.","grab":{"what":"A real, licensed photo of Erik ten Hag on the touchline or at a press conference","search":"Erik ten Hag","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"The slide is about him personally, so a real photo is better than an AI one."},"fallback":True,
 "A":"Editorial photograph of a lone football manager seen from behind in a dark overcoat, standing at the edge of a floodlit pitch at dusk, empty stands curving above, wet grass catching the light. Keep the top fifth as soft pale sky. Square 1:1. True-to-life colour, bright high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of an empty technical area on a football touchline, a padded coaching bench and a folded tactics board under bright stadium lights, nobody present. Keep the top fifth soft and bright. Square 1:1. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 2 FA Cup
S.append(sec(2,T,'Photo on top (62%), headline and body below',card(
 ph('left:0;right:0;top:0;height:82cqw','ft','Photo: FA Cup night')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:82cqw;height:43cqw"><div class="rs c-h" style="--d:.2s;font-size:6.6cqw;text-align:center">فاز <span class="hl">٢-١</span> على سيتي في ويمبلي... فبقي في منصبه</div><div class="rs c-b" style="--d:.7s;margin-top:4cqw;text-align:center;font-size:3.8cqw">كانت المحادثات مع توخيل ودي زيربي قد خرجت إلى العلن. بعد النهائي تراجعت الإدارة، وبعد أسبوعين فُعّل بند تمديد عقده سنة.</div></div>'),[
 ('Headline','فاز ٢-١ على سيتي في ويمبلي... فبقي في منصبه','ar h'),
 ('Body','كانت المحادثات مع توخيل ودي زيربي قد خرجت إلى العلن. بعد النهائي تراجعت الإدارة، وبعد أسبوعين فُعّل بند تمديد عقده سنة.','ar'),
 ('Check','Spelling to confirm: «توخيل» (Tuchel), «دي زيربي» (De Zerbi). The article says the clause was triggered two weeks later, after talks during his holiday in Ibiza.','')]))
D.append("Headline: فاز ٢-١ على سيتي في ويمبلي... فبقي في منصبه\nBody: كانت المحادثات مع توخيل ودي زيربي قد خرجت إلى العلن. بعد النهائي تراجعت الإدارة، وبعد أسبوعين فُعّل بند تمديد عقده سنة.")
IMG.append({"size":"3:2 landscape works too, but square 1:1 at 1024x1024 is safest","comp":"Keep the bottom fifth calm and light. It fades into the white. Trophy or confetti in the upper two thirds.","grab":None,"fallback":False,
 "A":"Editorial photograph of a silver football cup with ribbons standing on a plinth on a pitch under bright stadium lights, red and white confetti drifting down, a vast stadium bowl blurred behind, no people. Keep the bottom fifth soft and bright. Square 1:1. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of red and white ticker tape scattered across empty stadium seats after a final, late golden light, shallow depth of field, no people. Keep the bottom fifth soft and bright. Square 1:1. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 3 promises
S.append(sec(3,T,'Photo on top (55%), headline and three promise columns below',card(
 ph('left:0;right:0;top:0;height:74cqw','ft','Photo: Ibiza, two empty chairs')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:70cqw;height:54cqw"><div class="rs c-h" style="--d:.2s;font-size:7cqw;text-align:center">في إيبيزا... <span class="hl">ثلاثة</span> وعود</div><div style="display:flex;margin-top:5cqw;align-items:stretch"><div class="rs c-h" style="--d:.6s;flex:1;text-align:center;font-size:6.2cqw">الولاء</div><div class="dv" style="position:static;width:.5cqw"></div><div class="rs c-h" style="--d:.8s;flex:1;text-align:center;font-size:6.2cqw">الدعم</div><div class="dv" style="position:static;width:.5cqw"></div><div class="rs c-h" style="--d:1s;flex:1;text-align:center;font-size:6.2cqw">التواصل</div></div><div class="rs c-b" style="--d:1.3s;margin-top:6cqw;text-align:center;font-size:4cqw">يقول تن هاغ: «لكن الوعود... لم يلتزموا بها»</div></div>'),[
 ('Headline','في إيبيزا... ثلاثة وعود','ar h'),
 ('Column 1','الولاء','ar h'),('Column 2','الدعم','ar h'),('Column 3','التواصل','ar h'),
 ('Quote','يقول تن هاغ: «لكن الوعود... لم يلتزموا بها»','ar'),
 ('Check','Source quote: «They promised me loyalty, they promised me backing, they promised communication... But the promises, they didn\'t keep.»','')]))
D.append("Headline: في إيبيزا... ثلاثة وعود\nColumn 1: الولاء\nColumn 2: الدعم\nColumn 3: التواصل\nQuote: يقول تن هاغ: «لكن الوعود... لم يلتزموا بها»")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. Table and chairs in the middle.","grab":None,"fallback":False,
 "A":"Editorial photograph of a Mediterranean hotel terrace at golden hour, a small round table with two empty cane chairs facing each other, two untouched glasses of water, white stone wall and pale sea beyond, no people. Keep the bottom fifth soft and bright. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "B":"Editorial photograph of an empty poolside lounger and a folded white towel at a Mediterranean holiday resort in soft morning light, calm water, no people. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 4 McTominay
S.append(sec(4,T,'Photo on the left (56%), number block and text on the right',card(
 ph('left:0;top:0;bottom:0;width:56cqw','fl bf','Photo: McTominay')
 +'<div class="tz" style="right:6cqw;width:38cqw;top:8cqw;bottom:14cqw"><div class="rs c-n" style="--d:.2s;font-size:16cqw;text-align:center">٣٠٫٥</div><div class="rs c-b" style="--d:.45s;font-size:5cqw;line-height:1.2;margin-top:1.2cqw;text-align:center">مليون يورو</div><div class="rs c-h" style="--d:.7s;font-size:6cqw;margin-top:6cqw;text-align:center">بيع ماكتومناي إلى نابولي</div><div class="rs c-b" style="--d:1s;margin-top:5cqw;text-align:center;font-size:3.8cqw">اتفقوا في إيبيزا على عدم بيعه، وكان قد سجّل <span class="hl">١٠</span> أهداف. ثم بيع.</div><div class="rs c-b" style="--d:1.3s;margin-top:4cqw;text-align:center;font-size:3.6cqw;color:var(--green)">«شعرت بالإحراج والخيبة»</div></div>'),[
 ('Big number','٣٠٫٥','ar h'),('Unit','مليون يورو','ar'),
 ('Headline','بيع ماكتومناي إلى نابولي','ar h'),
 ('Body','اتفقوا في إيبيزا على عدم بيعه، وكان قد سجّل ١٠ أهداف. ثم بيع.','ar'),
 ('Quote (green)','«شعرت بالإحراج والخيبة»','ar'),
 ('Check','Article: €30.5m (then £25.7m), sold to fund the Manuel Ugarte signing, 10 goals that season. Spelling to confirm: «ماكتومناي», «أوغارتي».','')]))
D.append("Big number: ٣٠٫٥\nUnit: مليون يورو\nHeadline: بيع ماكتومناي إلى نابولي\nBody: اتفقوا في إيبيزا على عدم بيعه، وكان قد سجّل ١٠ أهداف. ثم بيع.\nQuote: «شعرت بالإحراج والخيبة»")
IMG.append({"size":"2:3 portrait, generate at 1024x1536 or larger","comp":"Keep the right fifth open and bright. It fades into the white. Subject in the left four fifths.","grab":{"what":"A real, licensed photo of Scott McTominay in a Napoli shirt","search":"Scott McTominay Napoli","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"Napoli only appears in the headline, so a United-era photo also works. Check the licence either way."},"fallback":True,
 "A":"Editorial photograph of a plain navy training bib hanging alone on a metal peg in an empty football dressing room, a bench and a bright window beyond, no people. Keep the right fifth as soft pale wall. Portrait 2:3. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of a pair of football boots on a bench in a bright empty changing room, laces undone, a kit bag beside them, no people. Keep the right fifth soft and bright. Portrait 2:3. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 5 Kane
S.append(sec(5,T,'Photo on the right (48%), number block and text on the left',card(
 ph('right:0;top:0;bottom:0;width:48cqw','fr bf','Photo: Kane')
 +'<div class="tz" style="left:6cqw;width:44cqw;top:8cqw;bottom:14cqw"><div class="rs c-n" style="--d:.2s;font-size:17cqw;text-align:center">١١٠</div><div class="rs c-b" style="--d:.45s;font-size:5cqw;line-height:1.2;margin-top:1.2cqw;text-align:center">مليون يورو</div><div class="rs c-h" style="--d:.7s;font-size:6cqw;margin-top:6cqw;text-align:center">كين... الاسم الذي أراده</div><div class="rs c-b" style="--d:1s;margin-top:5cqw;text-align:center;font-size:3.8cqw">«أريد لاعبًا <span class="hl">واحدًا</span> فقط... وأنتم تعرفونه». قيل له لا، فانتقل كين إلى بايرن ميونخ.</div></div>'),[
 ('Big number','١١٠','ar h'),('Unit','مليون يورو','ar'),
 ('Headline','كين... الاسم الذي أراده','ar h'),
 ('Body','«أريد لاعبًا واحدًا فقط... وأنتم تعرفونه». قيل له لا، فانتقل كين إلى بايرن ميونخ.','ar'),
 ('Check','Article: summer 2023, Kane then 30, Bayern deal worth €110m. Ten Hag says he never spoke to Kane and did not see the financials. Spelling to confirm: «كين».','')]))
D.append("Big number: ١١٠\nUnit: مليون يورو\nHeadline: كين... الاسم الذي أراده\nBody: «أريد لاعبًا واحدًا فقط... وأنتم تعرفونه». قيل له لا، فانتقل كين إلى بايرن ميونخ.")
IMG.append({"size":"2:3 portrait, generate at 1024x1536 or larger","comp":"Keep the left fifth open and bright. It fades into the white. Subject in the right four fifths.","grab":{"what":"A real, licensed photo of Harry Kane in a Bayern Munich or England shirt","search":"Harry Kane","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"The slide names him, so a real photo is better than an AI one."},"fallback":True,
 "A":"Editorial photograph of a lone centre-forward seen from behind, plain red training top, standing alone in a vast empty stadium penalty area at dusk, goalposts in the background, long shadows. Keep the left fifth as soft pale sky. Portrait 2:3. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of a football resting on the penalty spot of an empty stadium pitch in bright light, goal net blurred behind, no people. Keep the left fifth soft and bright. Portrait 2:3. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 6 others
def lrow(n,t): return f'<div class="rs" style="display:flex;justify-content:space-between;gap:3cqw;border-top:.3cqw solid var(--line);padding:2.1cqw 0;align-items:baseline"><span class="c-h" style="font-size:4.8cqw;white-space:nowrap">{n}</span><span class="c-b" style="font-size:3.7cqw;text-align:left">{t}</span></div>'
S.append(sec(6,T,'Text and list on top, photo in the lower 52%',card(
 '<div class="tz" style="right:7cqw;left:7cqw;top:5cqw;height:60cqw;justify-content:flex-start"><div class="rs c-h" style="--d:.2s;font-size:6.8cqw;text-align:center;margin-bottom:4cqw">وأسماء أخرى <span class="hl">لم تكتمل</span></div>'
 +lrow('ديكلان رايس','وست هام لم يبع، وانتقل إلى أرسنال')+lrow('فرينكي دي يونغ','رفض الانضمام')+lrow('بريان بروبي','تأخروا عليه')+lrow('داني ويلبيك','لم يُقدَّم عرض رسمي')+'</div>'
 +ph('left:0;right:0;bottom:0;height:70cqw','fb bf','Photo: empty transfer-window desk')),[
 ('Headline','وأسماء أخرى لم تكتمل','ar h'),
 ('Row 1','ديكلان رايس: وست هام لم يبع، وانتقل إلى أرسنال','ar'),
 ('Row 2','فرينكي دي يونغ: رفض الانضمام','ar'),
 ('Row 3','بريان بروبي: تأخروا عليه','ar'),
 ('Row 4','داني ويلبيك: لم يُقدَّم عرض رسمي','ar'),
 ('Check','Article: Rice went to Arsenal for a package worth £105m. De Jong declined after weeks of talks. Brobbey: «we were late», he was already in a different process. Welbeck: the club never committed to a formal offer. Spelling to confirm: «بروبي», «ويلبيك».','')]))
D.append("Headline: وأسماء أخرى لم تكتمل\nRow 1: ديكلان رايس: وست هام لم يبع، وانتقل إلى أرسنال\nRow 2: فرينكي دي يونغ: رفض الانضمام\nRow 3: بريان بروبي: تأخروا عليه\nRow 4: داني ويلبيك: لم يُقدَّم عرض رسمي")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the top fifth open and bright. It fades into the white. Rail of shirts in the lower two thirds.","grab":None,"fallback":False,
 "A":"Editorial photograph of four plain unbranded football shirts in different colours hanging on a clothes rail in a bright empty room, a wooden desk with a closed laptop beside it, no people. Keep the top fifth as soft pale wall. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no crests, no watermarks, no people.",
 "B":"Editorial photograph of an empty long boardroom table with four closed folders laid out in a row under bright daylight from tall windows, no people. Keep the top fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 7 Ronaldo
def bl(t): return f'<div style="display:flex;gap:2.2cqw;align-items:baseline;margin-top:2cqw"><span class="hl" style="font-size:4cqw">•</span><span>{t}</span></div>'
S.append(sec(7,T,'Photo on top (58%), headline and three points below',card(
 ph('left:0;right:0;top:0;height:76cqw','ft','Photo: Ronaldo')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:70cqw;height:55cqw"><div class="rs c-h" style="--d:.2s;font-size:6.4cqw;text-align:center">رونالدو: «خذل الفريق <span class="hl">وخذلني</span>»</div><div class="rs c-b" style="--d:.7s;margin-top:3cqw;font-size:3.7cqw;text-align:right">'
 +bl('ينسحب من بعض الحصص التدريبية')+bl('لا يرفع نبض قلبه إلى المستوى المطلوب')+bl('أكمل لفّتين فقط من ثلاث بعد الخسارة ٤-٠ أمام برينتفورد')
 +'</div><div class="rs c-b" style="--d:1.2s;margin-top:3cqw;text-align:center;font-size:3.2cqw;color:var(--green)">ممثل رونالدو لم يردّ على The Athletic</div></div>'),[
 ('Headline','رونالدو: «خذل الفريق وخذلني»','ar h'),
 ('Point 1','ينسحب من بعض الحصص التدريبية','ar'),
 ('Point 2','لا يرفع نبض قلبه إلى المستوى المطلوب','ar'),
 ('Point 3','أكمل لفّتين فقط من ثلاث بعد الخسارة ٤-٠ أمام برينتفورد','ar'),
 ('Detail (green)','ممثل رونالدو لم يردّ على The Athletic','ar'),
 ('Check','These are Ten Hag\'s claims, not established facts, so the slide frames them as his words. Article: Brentford 4-0 was August 2022. The Athletic put the comments to Ronaldo\'s representative and had no reply at publication.','')]))
D.append("Headline: رونالدو: «خذل الفريق وخذلني»\nPoint 1: ينسحب من بعض الحصص التدريبية\nPoint 2: لا يرفع نبض قلبه إلى المستوى المطلوب\nPoint 3: أكمل لفّتين فقط من ثلاث بعد الخسارة ٤-٠ أمام برينتفورد\nDetail: ممثل رونالدو لم يردّ على The Athletic")
IMG.append({"size":"1:1 square, generate at 1024x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.","grab":{"what":"A real, licensed photo of Cristiano Ronaldo in a Manchester United shirt","search":"Cristiano Ronaldo Manchester United","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"The slide quotes about him, so a real photo is better. Avoid an image that looks celebratory."},"fallback":True,
 "A":"Editorial photograph of a lone footballer seen from behind jogging on a training pitch at first light, mist over the grass, cones in a line, empty stands beyond. Keep the bottom fifth as soft pale mist. Square 1:1. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of a row of orange training cones across a wet football pitch in early morning light, no people, shallow depth of field. Keep the bottom fifth soft and bright. Square 1:1. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 8 culture
S.append(sec(8,T,'Photo on top (50%), headline and body below',card(
 ph('left:0;right:0;top:0;height:68cqw','ft','Photo: dressing room')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:62cqw;height:63cqw"><div class="rs c-h" style="--d:.2s;font-size:6cqw;text-align:center">«الثقافة <span class="hl">السامة</span>» و«مجموعة مدريد»</div><div class="rs c-b" style="--d:.7s;margin-top:3.5cqw;text-align:center;font-size:3.6cqw">يقول تن هاغ إن الإدارة لم تدعمه في عقوبات على لاعبين مثل سانشو وراشفورد، وإن «مجموعة مدريد» (كاسيميرو، فاران، رونالدو) جلبت نفوذ اللاعبين.</div><div class="rs c-b" style="--d:1.2s;margin-top:3cqw;text-align:center;font-size:3.2cqw;color:var(--green)">يونايتد يرى أن السلوك تحسّن مع أموريم</div></div>'),[
 ('Headline','«الثقافة السامة» و«مجموعة مدريد»','ar h'),
 ('Body','يقول تن هاغ إن الإدارة لم تدعمه في عقوبات على لاعبين مثل سانشو وراشفورد، وإن «مجموعة مدريد» (كاسيميرو، فاران، رونالدو) جلبت نفوذ اللاعبين.','ar'),
 ('Detail (green)','يونايتد يرى أن السلوك تحسّن مع أموريم','ar'),
 ('Check','Article: «they are continuing the toxic culture... they give the power to the players». «Madrid connection» is his phrase for Casemiro, Varane and Ronaldo. The balancing line is the article\'s: United feel behaviours improved with Amorim. Spelling to confirm: «كاسيميرو», «فاران», «أموريم».','')]))
D.append("Headline: «الثقافة السامة» و«مجموعة مدريد»\nBody: يقول تن هاغ إن الإدارة لم تدعمه في عقوبات على لاعبين مثل سانشو وراشفورد، وإن «مجموعة مدريد» (كاسيميرو، فاران، رونالدو) جلبت نفوذ اللاعبين.\nDetail: يونايتد يرى أن السلوك تحسّن مع أموريم")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. Room in the upper two thirds.","grab":None,"fallback":False,
 "A":"Editorial photograph of a football dressing room with a row of empty wooden benches and plain shirts on hooks, a single player-sized gap in the row, bright light from a high window, no people. Keep the bottom fifth soft and bright. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no crests, no watermarks, no people.",
 "B":"Editorial photograph of a closed tunnel door with a metal handle in a stadium corridor, bright light spilling under it, no people. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 9 closer
S.append(sec(9,T,'Photo on top (53%), text and question below, four icons at the bottom',card(
 ph('left:0;right:0;top:0;height:71cqw','ft','Photo: Old Trafford')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:64cqw;height:47cqw"><div class="rs c-h" style="--d:.2s;font-size:5.8cqw;text-align:center">٢٨ أكتوبر ٢٠٢٤: المركز <span class="hl">١٤</span></div><div class="rs c-b" style="--d:.6s;margin-top:2.5cqw;text-align:center"><span style="font-size:3.5cqw;line-height:1.55;display:block">١١ نقطة من ٩ مباريات بعد الخسارة ٢-١ أمام وست هام.<br>وعن كاريك اليوم يقول: «إقالته ليست الحل... مئة بالمئة لا».</span></div><div class="rs c-h" style="--d:1s;font-size:6.2cqw;margin-top:3.5cqw;text-align:center;color:var(--red)">إحكيلي</div><div class="rs c-b" style="--d:1.2s;font-size:4.4cqw;margin-top:1cqw;text-align:center;color:var(--navy)">هل أخطأ يونايتد حين أقال تن هاغ؟</div></div>'
 +icons_svg,False),[
 ('Headline','٢٨ أكتوبر ٢٠٢٤: المركز ١٤','ar h'),
 ('Body','١١ نقطة من ٩ مباريات بعد الخسارة ٢-١ أمام وست هام. وعن كاريك اليوم يقول: «إقالته ليست الحل... مئة بالمئة لا».','ar'),
 ('Question line 1 (red)','إحكيلي','ar h'),
 ('Question line 2','هل أخطأ يونايتد حين أقال تن هاغ؟','ar'),
 ('Icons','Heart (red), comment (green), share (navy), save (navy), close together.',''),
 ('Check','Article: sacked 28 Oct 2024, the day after a 2-1 loss to West Ham, United 14th on 11 points from nine games. Carrick quote: «It is not the solution to dismiss him. 100 per cent not.» «Mئة بالمئة» is my wording of «100 per cent».','')]))
D.append("Headline: ٢٨ أكتوبر ٢٠٢٤: المركز ١٤\nBody: ١١ نقطة من ٩ مباريات بعد الخسارة ٢-١ أمام وست هام. وعن كاريك اليوم يقول: «إقالته ليست الحل... مئة بالمئة لا».\nQuestion line 1: إحكيلي\nQuestion line 2: هل أخطأ يونايتد حين أقال تن هاغ؟")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. Stadium in the upper two thirds.","grab":{"what":"A real photo of Old Trafford from outside in daylight","search":"Old Trafford stadium","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"The slide names the club's ground, so a real photo is better than an AI one."},"fallback":True,
 "A":"Editorial photograph of the exterior of a large English football stadium on a bright overcast afternoon, a wide stone forecourt in front, the stand roof and a floodlight pylon rising behind, a few distant fans walking toward the entrance, no readable signage. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, bright high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of a football stadium tunnel entrance seen from the pitch side at matchday, bright daylight at the end of the tunnel, empty seats above, no people, no signage. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})

S[8]=S[8].replace('«Mئة بالمئة»','«مئة بالمئة»')

LINK=lambda u,t:f'<li><a href="{u}" target="_blank" rel="noopener" style="color:var(--navy);font-weight:600">{t}</a></li>'
th='padding:6px 8px;border-bottom:1px solid var(--line)'
def tr(*c): return '<tr>'+''.join(f'<td style="padding:6px 8px;vertical-align:top">{x}</td>' for x in c)+'</tr>'
sources=f'''<div style="margin:0 0 34px;padding:18px 20px;border:1px solid var(--line);border-radius:10px;background:#FBFCFE"><h2 style="margin:0 0 6px;font-size:20px">Source: check every claim yourself</h2><p style="margin:0 0 12px;color:var(--mute)">Everything comes from one text: the Laurie Whitwell interview for The Athletic, 20 October 2026, as you pasted it. I read all of it. The pasted text stops in the middle of an answer near the end, and I did not check any figure against another outlet. Ten Hag's statements are his account, so the slides frame them as what he says.</p><div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;min-width:560px;font-size:14px"><tr style="text-align:left;color:var(--mute)"><th style="{th}">Slide</th><th style="{th}">Claim</th><th style="{th}">Article says</th><th style="{th}">Flag</th></tr>
{tr(2,'FA Cup 2-1 vs City; extra year triggered','Final win, then clause triggered two weeks later after talks in Ibiza','Dates not given beyond that')}
{tr(4,'McTominay sold for €30.5m','Left for Napoli, €30.5m (then £25.7m), to fund Ugarte; scored 10 that season','Ten Hag says he was against it')}
{tr(5,'Kane to Bayern, €110m','Ten Hag wanted only Kane in summer 2023; told no','He says he never spoke to Kane')}
{tr(6,'Rice £105m; Welbeck; Brobbey; De Jong','Rice to Arsenal in a £105m package; no formal Welbeck offer; Brobbey late; De Jong declined','Brobbey and Welbeck are Ten Hag\'s account')}
{tr(7,'Ronaldo claims','Skipped sessions, low heart rate, two of three laps after the 4-0 at Brentford','Ronaldo\'s representative had not replied')}
{tr(8,'Toxic culture, Madrid connection','Ten Hag says he was not backed on sanctions; blames the Madrid group','United say behaviour improved under Amorim')}
{tr(9,'14th, 11 points, sacked 28 Oct 2024','Sacked the day after 2-1 loss to West Ham','Carrick quote is from the same interview')}
</table></div><p style="margin:12px 0 0;color:var(--mute);font-size:13px">Left out on purpose: the article's figure of 14 Champions Leagues for Casemiro, Varane and Ronaldo (my own count of their Real Madrid wins gives 13, so check it before using it), Lisandro Martinez (Ten Hag declined to comment), Fred's man-management comment, and everything promised for part two (Mainoo, Garnacho, Sevilla, the data department).</p></div>'''

HEAD=f'''<meta name="claude:viewport-fit-sides" content="cover">
<title>Ten Hag Carousel Plan</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Figtree:wght@400;600;700&display=swap">
<style>
{font_and_css}
body{{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px;background:var(--white)}}
.row>div,.boxes>div,.pgrid>div,.slide>div{{min-width:0}}
.ph.fbs::after{{background:linear-gradient(to bottom,#fff 0,rgba(255,255,255,.85) 4%,rgba(255,255,255,.4) 11%,rgba(255,255,255,0) 24%)}}
</style>'''
BODY=f'''<div class="wrap"><h1>Ten Hag interview carousel: words, positions and images</h1><p class="lead">Nine slides on plain white, 3:4 (1080x1440), photo about 60% and text about 40%. Under each slide: Keep, Drop or Change, edit the text, position notes, and the image brief with Prompt A (main look) and Prompt B (a different take) for ChatGPT image generation. Copy everything at the end.</p><div class="rules"><span><i class="sw" style="background:var(--navy)"></i>Navy: headlines</span><span><i class="sw" style="background:var(--red)"></i>Red: the one key word or number</span><span><i class="sw" style="background:var(--green)"></i>Green: small details only</span><span>Generated images show generic scenes only, never a recognisable person.</span></div>
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
 var out=["TEN HAG INTERVIEW CAROUSEL FEEDBACK","Slides: "+D.length,""];
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
OUT='/tmp/claude-0/-home-user-goal-englize-watcher/3795416f-4611-5512-bdea-dc096a1a5987/scratchpad/ten_hag_carousel_plan.html'
open(OUT,'w',encoding='utf8').write(out)
print(len(out))
