# ---- 7-slide version; relies on helpers from the head of plan.py
import json as _j
PICS_B64={int(k):v for k,v in _j.load(open('pics.json')).items()}
# label -> (image number, background-size start, end, background-position)
PICS={'Photo: Ten Hag':(1,'auto 100%','auto 107%','40% 50%'),
 'Photo: two empty chairs':(2,'100% auto','107% auto','50% 32%'),
 'Photo: McTominay':(3,'100% auto','107% auto','50% 40%'),
 'Photo: four empty positions for the player cut-outs':(4,'100% auto','107% auto','50% 25%'),
 'Photo: Ronaldo':(5,'100% auto','107% auto','50% 6%'),
 'Photo: dressing room':(6,'100% auto','107% auto','50% 12%'),
 'Photo: Old Trafford':(7,'100% auto','107% auto','50% 40%')}
_ph0=ph
def ph(style,cls,label):
    p=PICS.get(label)
    if not p: return _ph0(style,cls,label)
    n,b0,b1,pos=p
    return f'<div class="ph has {cls}" style="{style}"><i class="pi" style="background-image:url(data:image/jpeg;base64,{PICS_B64[n]});background-position:{pos};--bs0:{b0};--bs1:{b1}"></i></div>'
RED={1:'«صمته» و «الوعود»',2:'«ثلاثة» وسطر الاقتباس كله',3:'«سجّل ١٠ أهداف. ثم بيع.» والرقم الكبير',4:'«ولم تأتِ»',5:'«وخذلني»',6:'«السامة»',7:'«٧» (كاريك) و «إحكيلي» و «بالك رح ينطرد؟»'}
def src(*lines):
    return ('From the article',''.join(f'<span style="display:block;margin-bottom:6px">{l}</span>' for l in lines),'')
S=[];D=[];IMG=[]
T=7
# ---------- 1 cover
S.append(sec(1,T,'Text on top, photo in the lower 63%, forward arrow',card(
 '<div class="tz" style="right:7cqw;left:7cqw;top:5cqw;height:51cqw"><div class="rs c-h" style="--d:.2s;font-size:7.4cqw">تن هاغ يكسر <span class="hl">صمته</span> عن يونايتد<span style="display:block;font-size:4.6cqw;margin-top:1.5cqw">بعد سنتين من إقالته: <span class="hl">الوعود</span> لم تُحترم</span></div><div class="rs c-b" style="--d:.7s;margin-top:6.5cqw">مقابلة حصرية مع The Athletic</div><div class="rs c-b" style="--d:.9s;margin-top:1.5cqw">ماذا قال عن الإدارة وكين ورونالدو؟</div></div>'
 +ph('left:0;right:0;bottom:0;height:84cqw','fbs bf','Photo: Ten Hag'),True),[
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
 +'<div class="tz" style="right:7cqw;left:7cqw;top:64cqw;height:60cqw"><div class="rs c-h" style="--d:.2s;font-size:6.8cqw;text-align:center">بعد الكأس: <span class="hl">ثلاثة</span> وعود</div><div class="rs c-b" style="--d:.6s;margin-top:3cqw;text-align:center;font-size:3.5cqw">فاز على سيتي ٢-١ في نهائي كأس الاتحاد، وبعد أسبوعين فُعّل بند تمديد عقده سنة، بعد محادثات في إيبيزا.</div><div style="display:flex;margin-top:4cqw;align-items:stretch"><div class="rs c-h" style="--d:.9s;flex:1;text-align:center;font-size:6cqw">الولاء</div><div class="dv" style="position:static;width:.5cqw"></div><div class="rs c-h" style="--d:1.1s;flex:1;text-align:center;font-size:6cqw">الدعم</div><div class="dv" style="position:static;width:.5cqw"></div><div class="rs c-h" style="--d:1.3s;flex:1;text-align:center;font-size:6cqw">التواصل</div></div><div class="rs c-b" style="--d:1.6s;margin-top:4cqw;text-align:center;font-size:3.9cqw;color:var(--red)">يقول تن هاغ: «لكن الوعود... لم يلتزموا بها»</div></div>'),[
 ('Headline','بعد الكأس: ثلاثة وعود','ar h'),
 ('Body','فاز على سيتي ٢-١ في نهائي كأس الاتحاد، وبعد أسبوعين فُعّل بند تمديد عقده سنة، بعد محادثات في إيبيزا.','ar'),
 ('Column 1','الولاء','ar h'),('Column 2','الدعم','ar h'),('Column 3','التواصل','ar h'),
 ('Quote (red)','يقول تن هاغ: «لكن الوعود... لم يلتزموا بها»','ar'),
 src('«a 2-1 victory against Pep Guardiola\'s champions prompted a U-turn from the club\'s hierarchy»','«Two weeks later, the clause in his contract for an additional year was triggered after crunch talks during his holiday in Ibiza.»','«They promised me loyalty, they promised me backing, they promised communication, that we get aligned. ... But the promises, they didn\'t keep.»'),
 ('My wording','The three words are the three promises in the quote. «بعد أسبوعين» comes from «Two weeks later» (after the final). The photo is a generic metaphor, not a place.','')]))
D.append("Headline: بعد الكأس: ثلاثة وعود\nBody: فاز على سيتي ٢-١ في نهائي كأس الاتحاد، وبعد أسبوعين فُعّل بند تمديد عقده سنة، بعد محادثات في إيبيزا.\nColumn 1: الولاء\nColumn 2: الدعم\nColumn 3: التواصل\nQuote: يقول تن هاغ: «لكن الوعود... لم يلتزموا بها»")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. Table and chairs in the middle.","grab":None,"fallback":False,
 "A":"Editorial photograph of a Mediterranean hotel terrace at golden hour, a small round table with two empty cane chairs facing each other, two untouched glasses of water, white stone wall and pale sea beyond, no people. Keep the bottom fifth soft and bright. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "B":"Editorial photograph of a trophy cup on a plain wooden table beside a closed contract folder and a pen, soft window light, no people. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 3 McTominay
S.append(sec(3,T,'Photo on top (50%), number, headline and text below',card(
 ph('left:0;right:0;top:0;height:66cqw','ft','Photo: McTominay')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:60cqw;height:65cqw"><div class="rs" style="--d:.2s;display:flex;justify-content:center;align-items:baseline;gap:3cqw"><span class="c-n" style="font-size:15cqw">٣٠٫٥</span><span class="c-b" style="font-size:5cqw">مليون يورو</span></div><div class="rs c-h" style="--d:.6s;font-size:6.4cqw;margin-top:3cqw;text-align:center">بيع ماكتومني إلى نابولي</div><div class="rs c-b" style="--d:1s;margin-top:3.5cqw;text-align:center;font-size:4cqw">اتفق مع الإدارة على عدم بيع ماكتومني. <span class="hl">سجّل ١٠ أهداف. ثم بيع.</span></div><div class="rs c-b" style="--d:1.3s;margin-top:3cqw;text-align:center;font-size:3.6cqw;color:var(--green)">«شعرت بالإحراج والخيبة»</div></div>'),[
 ('Big number','٣٠٫٥','ar h'),('Unit','مليون يورو','ar'),
 ('Headline','بيع ماكتومني إلى نابولي','ar h'),
 ('Body','اتفق مع الإدارة على عدم بيع ماكتومني. سجّل ١٠ أهداف. ثم بيع.','ar'),
 ('Quote (green)','«شعرت بالإحراج والخيبة»','ar'),
 src('«In Ibiza, we agreed. I said, \'No selling Scott McTominay\'.»','«Scott McTominay, who had scored 10 goals that campaign ... ended up leaving United for Napoli later that summer for €30.5million (then £25.7m; $33.7m) as the club raised funds to buy Manuel Ugarte.»','«I got, of course, very embarrassed and disappointed.»'),
 ('Your wording','The body sentence is yours: «اتفق مع الإدارة على عدم بيع ماكتومني». Ibiza is removed from the slide. I kept it in the quote above because that is what the article says. I used your spelling «ماكتومني» in the headline too.','')]))
D.append("Big number: ٣٠٫٥\nUnit: مليون يورو\nHeadline: بيع ماكتومني إلى نابولي\nBody: اتفق مع الإدارة على عدم بيع ماكتومني. سجّل ١٠ أهداف. ثم بيع.\nQuote: «شعرت بالإحراج والخيبة»")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.","grab":{"what":"A real, licensed photo of Scott McTominay in a Napoli shirt","search":"Scott McTominay Napoli","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"Napoli only appears in the headline, so a United-era photo also works. Check the licence either way."},"fallback":True,
 "A":"Editorial photograph of a plain navy training bib hanging alone on a metal peg in an empty football dressing room, a bench and a bright window beyond, no people. Keep the bottom fifth as soft pale floor. Landscape 3:2. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of a pair of football boots on a bench in a bright empty changing room, laces undone, a kit bag beside them, no people. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
# ---------- 4 names that did not come
def lrow(n,t): return f'<div class="rs" style="display:flex;justify-content:space-between;gap:3cqw;border-top:.3cqw solid var(--line);padding:1.4cqw 0;align-items:baseline"><span class="c-h" style="font-size:4.8cqw;white-space:nowrap">{n}</span><span class="c-b" style="font-size:3.6cqw;text-align:left">{t}</span></div>'
S.append(sec(4,T,'Photo on top (51%), headline and list below',card(
 '<div class="tz" style="right:7cqw;left:7cqw;top:63cqw;height:62cqw;justify-content:flex-start"><div class="rs c-h" style="--d:.2s;font-size:6.4cqw;text-align:center;margin-bottom:2cqw">أسماء طلبها... <span class="hl">ولم تأتِ</span></div>'
 +lrow('هاري كين','قيل له لا، فذهب إلى بايرن')+lrow('ديكلان رايس','وست هام لم يبع، فذهب إلى أرسنال')+lrow('فرينكي دي يونغ','رفض الانضمام')+lrow('داني ويلبيك','لم يُقدَّم له عرض رسمي')
 +'<div class="rs c-b" style="--d:1.4s;margin-top:3cqw;text-align:center;font-size:3.5cqw;color:var(--green)">عن كين: «أريد لاعبًا واحدًا فقط... وأنتم تعرفونه»</div></div>'
 +ph('left:0;right:0;top:0;height:68cqw','ft','Photo: four empty positions for the player cut-outs')),[
 ('Headline','أسماء طلبها... ولم تأتِ','ar h'),
 ('Row 1','هاري كين: قيل له لا، فذهب إلى بايرن','ar'),
 ('Row 2','ديكلان رايس: وست هام لم يبع، فذهب إلى أرسنال','ar'),
 ('Row 3','فرينكي دي يونغ: رفض الانضمام','ar'),
 ('Row 4','داني ويلبيك: لم يُقدَّم له عرض رسمي','ar'),
 ('Quote (green)','عن كين: «أريد لاعبًا واحدًا فقط... وأنتم تعرفونه»','ar'),
 src('Kane: «I said to them, \'I want only one player — and you know who\'.» ... «Ten Hag was told no.» ... «Instead, Kane moved from Tottenham Hotspur to Bayern Munich in a €110m deal.»','Rice: «The issue was that West Ham didn\'t want to let him go.» ... «Rice, then 24, ended up moving to Arsenal in the summer of 2023 for a package worth £105m.»','De Jong: «Barcelona\'s Frenkie de Jong was his first choice for midfield. United were in negotiations for several weeks, but the player declined to join.»','Welbeck: «the club never committed to a formal offer for Welbeck at that time.»'),
 ('My wording','The €110m (Kane) and £105m (Rice) figures are left off the card on purpose, to keep it short. Say if you want them in. Brobbey is removed. Spelling to confirm: «ويلبيك», «دي يونغ».','')]))
D.append("Headline: أسماء طلبها... ولم تأتِ\nRow 1: هاري كين: قيل له لا، فذهب إلى بايرن\nRow 2: ديكلان رايس: وست هام لم يبع، فذهب إلى أرسنال\nRow 3: فرينكي دي يونغ: رفض الانضمام\nRow 4: داني ويلبيك: لم يُقدَّم له عرض رسمي\nQuote: عن كين: «أريد لاعبًا واحدًا فقط... وأنتم تعرفونه»")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the top fifth open and bright. It fades into the white. Four equal, empty standing positions in one straight row across the lower two thirds, about a fifth of the width each, evenly spaced, with clear floor and soft contact shadows.","grab":{"what":"Four real, licensed photos, one per player, each a clean full-body or waist-up pose: Kane, Rice, De Jong, Welbeck. Cut out the backgrounds and place one on each position","search":"Harry Kane; Declan Rice; Frenkie de Jong; Danny Welbeck","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"The prompts below make an empty backdrop on purpose, because generated images show no recognisable people. Both backdrops light from the front-left, so pick photos lit the same way. For three players, use three of the four positions and leave one empty."},"fallback":False,
 "A":"Editorial photograph of a wide empty football pitch at dusk, low camera on the halfway line facing across the pitch, four evenly spaced empty standing positions in a straight row in the lower two thirds of the frame, each marked only by a faint worn patch of grass about a fifth of the frame width apart, clear open space above each, stadium floodlights glowing softly behind, nobody present. Soft even light from the front-left. Keep the top fifth as soft pale sky. Landscape 3:2. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no lines, no logos, no watermarks, no people.",
 "B":"Editorial studio backdrop, seamless pale grey wall and floor, four evenly spaced soft oval floor shadows in a straight row across the lower two thirds marking where four figures will stand, each a fifth of the frame width apart, faint out-of-focus stadium lights far behind, nobody present. Soft even light from the front-left. Keep the top fifth bright and plain. Landscape 3:2. Clean, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})
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
def col(who,num,color,label,pos,d): return f'<div class="rs" style="--d:{d}s;flex:1;text-align:center"><div class="c-b" style="font-size:3.6cqw;line-height:1.3">{who}</div><div class="c-n" style="font-size:11cqw;color:{color};margin-top:.5cqw">{num}</div><div class="c-b" style="font-size:3.4cqw;line-height:1.3;margin-top:1cqw">{label}</div><div class="c-b" style="font-size:3.4cqw;line-height:1.3;color:var(--mute)">{pos}</div></div>'
S.append(sec(7,T,'Photo on top (30%), two stat columns, question and four icons below',card(
 ph('left:0;right:0;top:0;height:40cqw','ft','Photo: Old Trafford')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:33cqw;height:79cqw"><div class="rs c-h" style="--d:.2s;font-size:5.4cqw;text-align:center">تن هاغ يوم إقالته... وكاريك اليوم</div><div class="rs" style="--d:.6s;display:flex;gap:3cqw;align-items:stretch;margin-top:3.5cqw">'
 +col('تن هاغ · ٢٨ أكتوبر ٢٠٢٤','١١','var(--navy)','نقطة من ٩ مباريات','المركز ١٤',.6)
 +'<div style="width:.5cqw;background:var(--line)"></div>'
 +col('كاريك · اليوم','٧','var(--red)','نقاط من ٧ مباريات','المركز ١٣',.8)
 +'</div><div class="rs c-b" style="--d:1.1s;margin-top:2.5cqw;text-align:center;font-size:3.2cqw;color:var(--green)">تن هاغ عن كاريك: «إقالته ليست الحل»</div><div class="rs c-h" style="--d:1.3s;font-size:6cqw;margin-top:3cqw;text-align:center;color:var(--red)">إحكيلي</div><div class="rs c-b" style="--d:1.5s;font-size:3.7cqw;margin-top:1cqw;text-align:center;color:var(--navy)">لو كاريك لعب ٩ مباريات بنفس نقاط تن هاغ أو أقل...</div><div class="rs c-h" style="--d:1.7s;font-size:5cqw;margin-top:1cqw;text-align:center;color:var(--red)">بالك رح ينطرد؟</div></div>'
 +icons_svg,False),[
 ('Headline','تن هاغ يوم إقالته... وكاريك اليوم','ar h'),
 ('Left column','تن هاغ · ٢٨ أكتوبر ٢٠٢٤: ١١ نقطة من ٩ مباريات، المركز ١٤','ar'),
 ('Right column (red)','كاريك · اليوم: ٧ نقاط من ٧ مباريات، المركز ١٣','ar'),
 ('Detail (green)','تن هاغ عن كاريك: «إقالته ليست الحل»','ar'),
 ('Question line 1 (red)','إحكيلي','ar h'),
 ('Question line 2','لو كاريك لعب ٩ مباريات بنفس نقاط تن هاغ أو أقل...','ar'),
 ('Question line 3 (red)','بالك رح ينطرد؟','ar h'),
 ('Other question','Tighter version if you want it: «لو كاريك وصل ٩ مباريات بنفس نقاط تن هاغ... كانوا طردوه؟»','ar'),
 ('Icons','Heart (red), comment (green), share (navy), save (navy), close together.',''),
 src('Ten Hag: «United were 14th in the Premier League on 11 points from nine games when Ten Hag was dismissed on October 28, 2024, the day after his side lost 2-1 to West Ham United.»','Carrick: «It is not the solution to dismiss him. 100 per cent not,» he says.'),
 ('Not in the article','Carrick\'s numbers are not in the article. They come from web search results, and I could not open the match-report pages to confirm them. After the Spurs 1-1: 6 points from 6, worst start in 40 years (your own earlier plan used NBC and Read Man Utd for that). Then a 1-1 draw at Leeds: 13th after seven games, one win from seven (Sky Sports, from a search snippet). The 7 is my sum, 6 + 1. The two sets of numbers are not the same number of games, 9 against 7, so check the live table before you post.',''),
 ('My wording','Your question, with «أو أقل» added because I was not sure if you meant the same points or fewer. Carrick is on 1.00 points a game and Ten Hag was on 1.22 (my arithmetic). The slide does not say that.','')]))
D.append("Headline: تن هاغ يوم إقالته... وكاريك اليوم\nLeft column: تن هاغ · ٢٨ أكتوبر ٢٠٢٤: ١١ نقطة من ٩ مباريات، المركز ١٤\nRight column: كاريك · اليوم: ٧ نقاط من ٧ مباريات، المركز ١٣\nDetail: تن هاغ عن كاريك: «إقالته ليست الحل»\nQuestion line 1: إحكيلي\nQuestion line 2: لو كاريك لعب ٩ مباريات بنفس نقاط تن هاغ أو أقل...\nQuestion line 3: بالك رح ينطرد؟")
IMG.append({"size":"3:2 landscape, generate at 1536x1024 or larger","comp":"Keep the bottom fifth open and bright. It fades into the white. The photo band is shorter on this slide, so keep the stadium roofline in the upper half.","grab":{"what":"A real photo of Old Trafford from outside in daylight","search":"Old Trafford stadium","where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":"The slide names the club's ground, so a real photo is better than an AI one."},"fallback":True,
 "A":"Editorial photograph of the exterior of a large English football stadium on a bright overcast afternoon, a wide stone forecourt in front, the stand roof and a floodlight pylon rising behind, a few distant fans walking toward the entrance, no readable signage. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "B":"Editorial photograph of a football stadium tunnel entrance seen from the pitch side at matchday, bright daylight at the end of the tunnel, empty seats above, no people, no signage. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."})

_H=_j.load(open('have.json',encoding='utf8'))
for _i,_im in enumerate(IMG): _im['have']=_H[str(_i+1)]

th='padding:6px 8px;border-bottom:1px solid var(--line)'
def tr(*c): return '<tr>'+''.join(f'<td style="padding:6px 8px;vertical-align:top">{x}</td>' for x in c)+'</tr>'
sources=f'''<div style="margin:0 0 34px;padding:18px 20px;border:1px solid var(--line);border-radius:10px;background:#FBFCFE"><h2 style="margin:0 0 6px;font-size:20px">Source: check every claim yourself</h2><p style="margin:0 0 12px;color:var(--mute)">Everything comes from one text: the Laurie Whitwell interview for The Athletic, 20 October 2026, as you pasted it. Each slide's right-hand column has a "From the article" row with the exact English sentences it is built on, and a "My wording" row for anything I put into Arabic myself. The pasted text stops in the middle of an answer near the end. I did not check any figure against another outlet. Ten Hag's statements are his account, so the slides frame them as what he says.</p><div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;min-width:560px;font-size:14px"><tr style="text-align:left;color:var(--mute)"><th style="{th}">Slide</th><th style="{th}">Claim</th><th style="{th}">Article says</th><th style="{th}">Flag</th></tr>
{tr(2,'FA Cup 2-1 vs City; extra year; Ibiza; three promises','Win prompted a U-turn; clause triggered two weeks later after talks during his holiday in Ibiza; loyalty, backing, communication','Ten Hag’s account of the promises')}
{tr(3,'McTominay €30.5m to Napoli','No selling agreed in Ibiza; 10 goals that season; sold to fund Ugarte','Ten Hag’s account')}
{tr(4,'Kane, Rice, De Jong, Welbeck','Kane told no, then Bayern (€110m); Rice to Arsenal (£105m) after West Ham refused; De Jong declined; no formal Welbeck offer','Welbeck: Darren Fletcher was in contact, per Ten Hag')}
{tr(5,'Ronaldo claims','Skipped sessions, low heart rate, two of three laps after the 4-0 at Brentford (Aug 2022)','Ronaldo’s representative had not replied')}
{tr(6,'Toxic culture, Madrid connection','Not backed on sanctions (Sancho, Rashford, others); blames the Madrid group','United say behaviour improved under Amorim')}
{tr(7,'Ten Hag 14th, 11 points from 9, sacked 28 Oct 2024; Carrick quote','Sacked the day after the 2-1 West Ham loss; Carrick: «not the solution to dismiss him»','Carrick quote is from the same interview')}
{tr(7,'Carrick today: 7 points from 7, 13th','Not in the article','From web search results only (Sky Sports snippet; the 7 is my sum). Confirm on the live table')}
</table></div><p style="margin:12px 0 0;color:var(--mute);font-size:13px">Left out on purpose: Brian Brobbey (cut to save space), the article's figure of 14 Champions Leagues for Casemiro, Varane and Ronaldo (my own count of their Real Madrid wins gives 13, so check it before using it), Lisandro Martinez (Ten Hag declined to comment), Fred's man-management comment, and everything promised for part two (Mainoo, Garnacho, Sevilla, the data department).</p></div>'''
