# ---- 7-slide version; relies on helpers from the head of plan.py
RED={1:'«صمته» و «الوعود»',2:'«ثلاثة»',3:'«١٠» (والرقم الكبير)',4:'«ولم تأتِ»',5:'«وخذلني»',6:'«السامة»',7:'«١٤» و «إحكيلي»'}
def src(*lines):
    return ('From the article',''.join(f'<span style="display:block;margin-bottom:6px">{l}</span>' for l in lines),'')
S=[];D=[];IMG=[]
T=7
# ---------- 1 cover
S.append(sec(1,T,'Text on top, photo in the lower 63%, forward arrow',card(
 '<div class="tz" style="right:7cqw;left:7cqw;top:5cqw;height:51cqw"><div class="rs c-h" style="--d:.2s;font-size:7.4cqw">تن هاغ يكسر <span class="hl">صمته</span> عن يونايتد<span style="display:block;font-size:4.6cqw;margin-top:1.5cqw">بعد سنتين من إقالته: <span class="hl">الوعود</span> لم تُحترم</span></div><div class="rs c-b" style="--d:.7s;margin-top:6.5cqw">مقابلة حصرية مع The Athletic</div><div class="rs c-b" style="--d:.9s;margin-top:1.5cqw">ماذا قال عن الإدارة وكين ورونالدو؟</div></div>'
 +ph('left:0;right:0;bottom:0;height:84cqw','fb bf','Photo: Ten Hag'),True),[
 ('Headline','تن هاغ يكسر صمته عن يونايتد','ar h'),
 ('Second line','بعد سنتين من إقالته: الوعود لم تُحترم','ar'),
 ('Body 1','مقابلة حصرية مع The Athletic','ar'),
 ('Body 2','ماذا قال عن الإدارة وكين ورونالدو؟','ar'),
 src('«Erik ten Hag has kept his counsel on Manchester United for two years since his sacking in October 2024»','«But the promises, they didn\'t keep.»'),
 ('My wording','«لم تُحترم» is my Arabic for «they didn\'t keep» the promises. The last line is my teaser, not a quote.','')]))
D.append("Headline: تن هاغ يكسر صمته عن يونايتد\nSecond line: بعد سنتين من إقالته: الوعود لم تُحترم\nBody 1: مقابلة حصرية مع The Athletic\nBody 2: ماذا قال عن الإدارة وكين ورونالدو؟")
IMG.append({"size":"1:1 square, generate at 1024x1024 or larger","comp":"Keep the top fifth open and bright. It fades into the white. Subject sits in the lower two thirds.","grab":{"what":"A real, licensed photo of Erik ten Hag on the touchline or at a press conference","search":"Erik ten Hag","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"The slide is about him personally, so a real photo is better than an AI one."},"fallback":True,
 "A":"Editorial photograph of a lone football manager seen from behind in a dark overcoat, standing at the edge of a floodlit pitch at dusk, empty stands curving above, wet grass catching the light. Keep the top fifth as soft pale sky. Square 1:1. True-to-life colour, bright high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of an empty technical area on a football touchline, a padded coaching bench and a folded tactics board under bright stadium lights, nobody present. Keep the top fifth soft and bright. Square 1:1. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 2 promises (FA Cup + Ibiza + three promises)
S.append(sec(2,T,'Photo on top (53%), headline, short body and three promise columns below',card(
 ph('left:0;right:0;top:0;height:70cqw','ft','Photo: two empty chairs')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:64cqw;height:60cqw"><div class="rs c-h" style="--d:.2s;font-size:6.8cqw;text-align:center">بعد الكأس: <span class="hl">ثلاثة</span> وعود</div><div class="rs c-b" style="--d:.6s;margin-top:3cqw;text-align:center;font-size:3.5cqw">فاز على سيتي ٢-١ في نهائي كأس الاتحاد، وبعد أسبوعين فُعّل بند تمديد عقده سنة، بعد محادثات في إيبيزا.</div><div style="display:flex;margin-top:4cqw;align-items:stretch"><div class="rs c-h" style="--d:.9s;flex:1;text-align:center;font-size:6cqw">الولاء</div><div class="dv" style="position:static;width:.5cqw"></div><div class="rs c-h" style="--d:1.1s;flex:1;text-align:center;font-size:6cqw">الدعم</div><div class="dv" style="position:static;width:.5cqw"></div><div class="rs c-h" style="--d:1.3s;flex:1;text-align:center;font-size:6cqw">التواصل</div></div><div class="rs c-b" style="--d:1.6s;margin-top:4cqw;text-align:center;font-size:3.9cqw">يقول تن هاغ: «لكن الوعود... لم يلتزموا بها»</div></div>'),[
 ('Headline','بعد الكأس: ثلاثة وعود','ar h'),
 ('Body','فاز على سيتي ٢-١ في نهائي كأس الاتحاد، وبعد أسبوعين فُعّل بند تمديد عقده سنة، بعد محادثات في إيبيزا.','ar'),
 ('Column 1','الولاء','ar h'),('Column 2','الدعم','ar h'),('Column 3','التواصل','ar h'),
 ('Quote','يقول تن هاغ: «لكن الوعود... لم يلتزموا بها»','ar'),
 src('«a 2-1 victory against Pep Guardiola\'s champions prompted a U-turn from the club\'s hierarchy»','«Two weeks later, the clause in his contract for an additional year was triggered after crunch talks during his holiday in Ibiza.»','«They promised me loyalty, they promised me backing, they promised communication, that we get aligned. ... But the promises, they didn\'t keep.»'),
 ('My wording','The three words are the three promises in the quote. «بعد أسبوعين» comes from «Two weeks later» (after the final). The photo is a generic metaphor, not a place.','')]))
D.append("Headline: بعد الكأس: ثلاثة وعود\nBody: فاز على سيتي ٢-١ في نهائي كأس الاتحاد، وبعد أسبوعين فُعّل بند تمديد عقده سنة، بعد محادثات في إيبيزا.\nColumn 1: الولاء\nColumn 2: الدعم\nColumn 3: التواصل\nQuote: يقول تن هاغ: «لكن الوعود... لم يلتزموا بها»")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. Table and chairs in the middle.","grab":None,"fallback":False,
 "A":"Editorial photograph of a Mediterranean hotel terrace at golden hour, a small round table with two empty cane chairs facing each other, two untouched glasses of water, white stone wall and pale sea beyond, no people. Keep the bottom fifth soft and bright. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "B":"Editorial photograph of a trophy cup on a plain wooden table beside a closed contract folder and a pen, soft window light, no people. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 3 McTominay
S.append(sec(3,T,'Photo on the left (56%), number block and text on the right',card(
 ph('left:0;top:0;bottom:0;width:56cqw','fl bf','Photo: McTominay')
 +'<div class="tz" style="right:6cqw;width:38cqw;top:8cqw;bottom:14cqw"><div class="rs c-n" style="--d:.2s;font-size:16cqw;text-align:center">٣٠٫٥</div><div class="rs c-b" style="--d:.45s;font-size:5cqw;line-height:1.2;margin-top:1.2cqw;text-align:center">مليون يورو</div><div class="rs c-h" style="--d:.7s;font-size:6cqw;margin-top:6cqw;text-align:center">بيع ماكتومناي إلى نابولي</div><div class="rs c-b" style="--d:1s;margin-top:5cqw;text-align:center;font-size:3.8cqw">اتفقوا في إيبيزا على عدم بيعه، وكان قد سجّل <span class="hl">١٠</span> أهداف. ثم بيع.</div><div class="rs c-b" style="--d:1.3s;margin-top:4cqw;text-align:center;font-size:3.6cqw;color:var(--green)">«شعرت بالإحراج والخيبة»</div></div>'),[
 ('Big number','٣٠٫٥','ar h'),('Unit','مليون يورو','ar'),
 ('Headline','بيع ماكتومناي إلى نابولي','ar h'),
 ('Body','اتفقوا في إيبيزا على عدم بيعه، وكان قد سجّل ١٠ أهداف. ثم بيع.','ar'),
 ('Quote (green)','«شعرت بالإحراج والخيبة»','ar'),
 src('«In Ibiza, we agreed. I said, \'No selling Scott McTominay\'.»','«Scott McTominay, who had scored 10 goals that campaign ... ended up leaving United for Napoli later that summer for €30.5million (then £25.7m; $33.7m) as the club raised funds to buy Manuel Ugarte.»','«I got, of course, very embarrassed and disappointed.»'),
 ('My wording','«ثم بيع» is a short form of the sale to Napoli. The article\'s own phrasing is that United sold him to raise funds for Ugarte. Spelling to confirm: «ماكتومناي», «أوغارتي».','')]))
D.append("Big number: ٣٠٫٥\nUnit: مليون يورو\nHeadline: بيع ماكتومناي إلى نابولي\nBody: اتفقوا في إيبيزا على عدم بيعه، وكان قد سجّل ١٠ أهداف. ثم بيع.\nQuote: «شعرت بالإحراج والخيبة»")
IMG.append({"size":"2:3 portrait, generate at 1024x1536 or larger","comp":"Keep the right fifth open and bright. It fades into the white. Subject in the left four fifths.","grab":{"what":"A real, licensed photo of Scott McTominay in a Napoli shirt","search":"Scott McTominay Napoli","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"Napoli only appears in the headline, so a United-era photo also works. Check the licence either way."},"fallback":True,
 "A":"Editorial photograph of a plain navy training bib hanging alone on a metal peg in an empty football dressing room, a bench and a bright window beyond, no people. Keep the right fifth as soft pale wall. Portrait 2:3. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of a pair of football boots on a bench in a bright empty changing room, laces undone, a kit bag beside them, no people. Keep the right fifth soft and bright. Portrait 2:3. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 4 names that did not come
def lrow(n,t): return f'<div class="rs" style="display:flex;justify-content:space-between;gap:3cqw;border-top:.3cqw solid var(--line);padding:1.4cqw 0;align-items:baseline"><span class="c-h" style="font-size:4.8cqw;white-space:nowrap">{n}</span><span class="c-b" style="font-size:3.6cqw;text-align:left">{t}</span></div>'
S.append(sec(4,T,'Text and list on top, photo in the lower 52%',card(
 '<div class="tz" style="right:7cqw;left:7cqw;top:5cqw;height:63cqw;justify-content:flex-start"><div class="rs c-h" style="--d:.2s;font-size:6.8cqw;text-align:center;margin-bottom:3cqw">أسماء طلبها... <span class="hl">ولم تأتِ</span></div>'
 +lrow('هاري كين','قيل له لا، فذهب إلى بايرن')+lrow('ديكلان رايس','وست هام لم يبع، فذهب إلى أرسنال')+lrow('فرينكي دي يونغ','رفض الانضمام')+lrow('داني ويلبيك','لم يُقدَّم له عرض رسمي')
 +'<div class="rs c-b" style="--d:1.4s;margin-top:3cqw;text-align:center;font-size:3.5cqw;color:var(--green)">عن كين: «أريد لاعبًا واحدًا فقط... وأنتم تعرفونه»</div></div>'
 +ph('left:0;right:0;bottom:0;height:66cqw','fb bf','Photo: empty transfer-window desk')),[
 ('Headline','أسماء طلبها... ولم تأتِ','ar h'),
 ('Row 1','هاري كين: قيل له لا، فذهب إلى بايرن','ar'),
 ('Row 2','ديكلان رايس: وست هام لم يبع، فذهب إلى أرسنال','ar'),
 ('Row 3','فرينكي دي يونغ: رفض الانضمام','ar'),
 ('Row 4','داني ويلبيك: لم يُقدَّم له عرض رسمي','ar'),
 ('Quote (green)','عن كين: «أريد لاعبًا واحدًا فقط... وأنتم تعرفونه»','ar'),
 src('Kane: «I said to them, \'I want only one player — and you know who\'.» ... «Ten Hag was told no.» ... «Instead, Kane moved from Tottenham Hotspur to Bayern Munich in a €110m deal.»','Rice: «The issue was that West Ham didn\'t want to let him go.» ... «Rice, then 24, ended up moving to Arsenal in the summer of 2023 for a package worth £105m.»','De Jong: «Barcelona\'s Frenkie de Jong was his first choice for midfield. United were in negotiations for several weeks, but the player declined to join.»','Welbeck: «the club never committed to a formal offer for Welbeck at that time.»'),
 ('My wording','The €110m (Kane) and £105m (Rice) figures are left off the card on purpose, to keep it short. Say if you want them in. Brobbey was cut from this version. Spelling to confirm: «ويلبيك», «دي يونغ».','')]))
D.append("Headline: أسماء طلبها... ولم تأتِ\nRow 1: هاري كين: قيل له لا، فذهب إلى بايرن\nRow 2: ديكلان رايس: وست هام لم يبع، فذهب إلى أرسنال\nRow 3: فرينكي دي يونغ: رفض الانضمام\nRow 4: داني ويلبيك: لم يُقدَّم له عرض رسمي\nQuote: عن كين: «أريد لاعبًا واحدًا فقط... وأنتم تعرفونه»")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the top fifth open and bright. It fades into the white. Rail of shirts in the lower two thirds.","grab":None,"fallback":False,
 "A":"Editorial photograph of four plain unbranded football shirts in different colours hanging on a clothes rail in a bright empty room, a wooden desk with a closed laptop beside it, no people. Keep the top fifth as soft pale wall. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no crests, no watermarks, no people.",
 "B":"Editorial photograph of an empty long boardroom table with four closed folders laid out in a row under bright daylight from tall windows, no people. Keep the top fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 5 Ronaldo
def bl(t): return f'<div style="display:flex;gap:2.2cqw;align-items:baseline;margin-top:2cqw"><span class="hl" style="font-size:4cqw">•</span><span>{t}</span></div>'
S.append(sec(5,T,'Photo on top (58%), headline and three points below',card(
 ph('left:0;right:0;top:0;height:76cqw','ft','Photo: Ronaldo')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:70cqw;height:55cqw"><div class="rs c-h" style="--d:.2s;font-size:6.4cqw;text-align:center">رونالدو: «خذل الفريق <span class="hl">وخذلني</span>»</div><div class="rs c-b" style="--d:.7s;margin-top:3cqw;font-size:3.7cqw;text-align:right">'
 +bl('ينسحب من بعض الحصص التدريبية')+bl('لا يرفع نبض قلبه إلى المستوى المطلوب')+bl('أكمل لفّتين فقط من ثلاث بعد الخسارة ٤-٠ أمام برينتفورد')
 +'</div><div class="rs c-b" style="--d:1.2s;margin-top:3cqw;text-align:center;font-size:3.2cqw;color:var(--green)">ممثل رونالدو لم يردّ على The Athletic</div></div>'),[
 ('Headline','رونالدو: «خذل الفريق وخذلني»','ar h'),
 ('Point 1','ينسحب من بعض الحصص التدريبية','ar'),
 ('Point 2','لا يرفع نبض قلبه إلى المستوى المطلوب','ar'),
 ('Point 3','أكمل لفّتين فقط من ثلاث بعد الخسارة ٤-٠ أمام برينتفورد','ar'),
 ('Detail (green)','ممثل رونالدو لم يردّ على The Athletic','ar'),
 src('«He let the team down, and he let me down, because we planned with him»','«According to Ten Hag, Ronaldo pulled out of training sessions, did not get his heart rate raised to the required level when he did train, and only completed two of the three scheduled laps of the infamous run Ten Hag made his players do after they lost 4-0 at Brentford in August 2022.»','«The Athletic put Ten Hag\'s comments to Ronaldo\'s representative but had not received a reply at the time of publication.»'),
 ('My wording','These are Ten Hag\'s claims, so the slide keeps them as his words. «بعض الحصص» is my wording of «pulled out of training sessions».','')]))
D.append("Headline: رونالدو: «خذل الفريق وخذلني»\nPoint 1: ينسحب من بعض الحصص التدريبية\nPoint 2: لا يرفع نبض قلبه إلى المستوى المطلوب\nPoint 3: أكمل لفّتين فقط من ثلاث بعد الخسارة ٤-٠ أمام برينتفورد\nDetail: ممثل رونالدو لم يردّ على The Athletic")
IMG.append({"size":"1:1 square, generate at 1024x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.","grab":{"what":"A real, licensed photo of Cristiano Ronaldo in a Manchester United shirt","search":"Cristiano Ronaldo Manchester United","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"The slide quotes about him, so a real photo is better. Avoid an image that looks celebratory."},"fallback":True,
 "A":"Editorial photograph of a lone footballer seen from behind jogging on a training pitch at first light, mist over the grass, cones in a line, empty stands beyond. Keep the bottom fifth as soft pale mist. Square 1:1. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of a row of orange training cones across a wet football pitch in early morning light, no people, shallow depth of field. Keep the bottom fifth soft and bright. Square 1:1. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 6 culture
S.append(sec(6,T,'Photo on top (50%), headline and body below',card(
 ph('left:0;right:0;top:0;height:68cqw','ft','Photo: dressing room')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:62cqw;height:63cqw"><div class="rs c-h" style="--d:.2s;font-size:6cqw;text-align:center">«الثقافة <span class="hl">السامة</span>» و«مجموعة مدريد»</div><div class="rs c-b" style="--d:.7s;margin-top:3.5cqw;text-align:center;font-size:3.6cqw">يقول تن هاغ إن الإدارة لم تدعمه في عقوبات على لاعبين مثل سانشو وراشفورد، وإن «مجموعة مدريد» (كاسيميرو، فاران، رونالدو) جلبت نفوذ اللاعبين.</div><div class="rs c-b" style="--d:1.2s;margin-top:3cqw;text-align:center;font-size:3.2cqw;color:var(--green)">يونايتد يرى أن السلوك تحسّن مع أموريم</div></div>'),[
 ('Headline','«الثقافة السامة» و«مجموعة مدريد»','ar h'),
 ('Body','يقول تن هاغ إن الإدارة لم تدعمه في عقوبات على لاعبين مثل سانشو وراشفورد، وإن «مجموعة مدريد» (كاسيميرو، فاران، رونالدو) جلبت نفوذ اللاعبين.','ar'),
 ('Detail (green)','يونايتد يرى أن السلوك تحسّن مع أموريم','ar'),
 src('«Ten Hag ... felt he was not supported in sanctions on several matters of player discipline, including with Jadon Sancho, Rashford and others.»','«And so, they are continuing the toxic culture; they fuel it, they give the power to the players»','«I think that\'s what the Madrid connection brought in, that players are powerful and they want to decide.» ... «By the \'Madrid connection\', Ten Hag means Casemiro, Varane, and Ronaldo»','«United feel behaviours in the squad did improve, with Amorim supported by the hierarchy in moving players on.»'),
 ('My wording','«جلبت نفوذ اللاعبين» is my Arabic for «players are powerful and they want to decide». Spelling to confirm: «كاسيميرو», «فاران», «أموريم».','')]))
D.append("Headline: «الثقافة السامة» و«مجموعة مدريد»\nBody: يقول تن هاغ إن الإدارة لم تدعمه في عقوبات على لاعبين مثل سانشو وراشفورد، وإن «مجموعة مدريد» (كاسيميرو، فاران، رونالدو) جلبت نفوذ اللاعبين.\nDetail: يونايتد يرى أن السلوك تحسّن مع أموريم")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. Room in the upper two thirds.","grab":None,"fallback":False,
 "A":"Editorial photograph of a football dressing room with a row of empty wooden benches and plain shirts on hooks, a single player-sized gap in the row, bright light from a high window, no people. Keep the bottom fifth soft and bright. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no crests, no watermarks, no people.",
 "B":"Editorial photograph of a closed tunnel door with a metal handle in a stadium corridor, bright light spilling under it, no people. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 7 closer
S.append(sec(7,T,'Photo on top (53%), text and question below, four icons at the bottom',card(
 ph('left:0;right:0;top:0;height:71cqw','ft','Photo: Old Trafford')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:64cqw;height:47cqw"><div class="rs c-h" style="--d:.2s;font-size:5.8cqw;text-align:center">٢٨ أكتوبر ٢٠٢٤: المركز <span class="hl">١٤</span></div><div class="rs c-b" style="--d:.6s;margin-top:2.5cqw;text-align:center"><span style="font-size:3.5cqw;line-height:1.55;display:block">١١ نقطة من ٩ مباريات بعد الخسارة ٢-١ أمام وست هام.<br>وعن كاريك اليوم يقول: «إقالته ليست الحل... مئة بالمئة لا».</span></div><div class="rs c-h" style="--d:1s;font-size:6.2cqw;margin-top:3.5cqw;text-align:center;color:var(--red)">إحكيلي</div><div class="rs c-b" style="--d:1.2s;font-size:4.4cqw;margin-top:1cqw;text-align:center;color:var(--navy)">هل أخطأ يونايتد حين أقال تن هاغ؟</div></div>'
 +icons_svg,False),[
 ('Headline','٢٨ أكتوبر ٢٠٢٤: المركز ١٤','ar h'),
 ('Body','١١ نقطة من ٩ مباريات بعد الخسارة ٢-١ أمام وست هام. وعن كاريك اليوم يقول: «إقالته ليست الحل... مئة بالمئة لا».','ar'),
 ('Question line 1 (red)','إحكيلي','ar h'),
 ('Question line 2','هل أخطأ يونايتد حين أقال تن هاغ؟','ar'),
 ('Icons','Heart (red), comment (green), share (navy), save (navy), close together.',''),
 src('«United were 14th in the Premier League on 11 points from nine games when Ten Hag was dismissed on October 28, 2024, the day after his side lost 2-1 to West Ham United.»','«It is not the solution to dismiss him. 100 per cent not,» he says.'),
 ('My wording','«مئة بالمئة» is my Arabic for «100 per cent». «إحكيلي» and the question are my engagement line, not a quote. The article calls Carrick «the man currently in the hot seat».','')]))
D.append("Headline: ٢٨ أكتوبر ٢٠٢٤: المركز ١٤\nBody: ١١ نقطة من ٩ مباريات بعد الخسارة ٢-١ أمام وست هام. وعن كاريك اليوم يقول: «إقالته ليست الحل... مئة بالمئة لا».\nQuestion line 1: إحكيلي\nQuestion line 2: هل أخطأ يونايتد حين أقال تن هاغ؟")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. Stadium in the upper two thirds.","grab":{"what":"A real photo of Old Trafford from outside in daylight","search":"Old Trafford stadium","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"The slide names the club's ground, so a real photo is better than an AI one."},"fallback":True,
 "A":"Editorial photograph of the exterior of a large English football stadium on a bright overcast afternoon, a wide stone forecourt in front, the stand roof and a floodlight pylon rising behind, a few distant fans walking toward the entrance, no readable signage. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of a football stadium tunnel entrance seen from the pitch side at matchday, bright daylight at the end of the tunnel, empty seats above, no people, no signage. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})

th='padding:6px 8px;border-bottom:1px solid var(--line)'
def tr(*c): return '<tr>'+''.join(f'<td style="padding:6px 8px;vertical-align:top">{x}</td>' for x in c)+'</tr>'
sources=f'''<div style="margin:0 0 34px;padding:18px 20px;border:1px solid var(--line);border-radius:10px;background:#FBFCFE"><h2 style="margin:0 0 6px;font-size:20px">Source: check every claim yourself</h2><p style="margin:0 0 12px;color:var(--mute)">Everything comes from one text: the Laurie Whitwell interview for The Athletic, 20 October 2026, as you pasted it. Each slide's right-hand column has a "From the article" row with the exact English sentences it is built on, and a "My wording" row for anything I put into Arabic myself. The pasted text stops in the middle of an answer near the end. I did not check any figure against another outlet. Ten Hag's statements are his account, so the slides frame them as what he says.</p><div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;min-width:560px;font-size:14px"><tr style="text-align:left;color:var(--mute)"><th style="{th}">Slide</th><th style="{th}">Claim</th><th style="{th}">Article says</th><th style="{th}">Flag</th></tr>
{tr(2,'FA Cup 2-1 vs City; extra year; Ibiza; three promises','Win prompted a U-turn; clause triggered two weeks later after talks during his holiday in Ibiza; loyalty, backing, communication','Ten Hag’s account of the promises')}
{tr(3,'McTominay €30.5m to Napoli','No selling agreed in Ibiza; 10 goals that season; sold to fund Ugarte','Ten Hag’s account')}
{tr(4,'Kane, Rice, De Jong, Welbeck','Kane told no, then Bayern (€110m); Rice to Arsenal (£105m) after West Ham refused; De Jong declined; no formal Welbeck offer','Welbeck: Darren Fletcher was in contact, per Ten Hag')}
{tr(5,'Ronaldo claims','Skipped sessions, low heart rate, two of three laps after the 4-0 at Brentford (Aug 2022)','Ronaldo’s representative had not replied')}
{tr(6,'Toxic culture, Madrid connection','Not backed on sanctions (Sancho, Rashford, others); blames the Madrid group','United say behaviour improved under Amorim')}
{tr(7,'14th, 11 points, sacked 28 Oct 2024; Carrick','Sacked the day after the 2-1 West Ham loss; Carrick: «not the solution to dismiss him»','Carrick quote is from the same interview')}
</table></div><p style="margin:12px 0 0;color:var(--mute);font-size:13px">Left out on purpose: Brian Brobbey (cut to save space), the article's figure of 14 Champions Leagues for Casemiro, Varane and Ronaldo (my own count of their Real Madrid wins gives 13, so check it before using it), Lisandro Martinez (Ten Hag declined to comment), Fred's man-management comment, and everything promised for part two (Mainoo, Garnacho, Sevilla, the data department).</p></div>'''
