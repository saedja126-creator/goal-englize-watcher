RED={1:'«فعلًا»، والأرقام الثلاثة',2:'الأرقام الثلاثة وسطرا التفصيل',3:'«١٤٫٥» و «٢٥٠» وسطر التوفير',4:'«ولم يفوا» (سطر الاقتباس)',5:'«كانوا أفضل بكثير دون تدخلنا»',6:'«١٦»، «ملحق...» والسطر الأخير',7:'«٢» والسطر الأخير',8:'«٤٠» والسطر الأخير',9:'«إحكيلي» والسؤال، وسطر موريس'}
def src(ref,*lines):
    q=''.join(f'<span dir="rtl" style="display:block;margin-bottom:6px;text-align:right">{l}</span>' for l in lines)
    return ('From the report',q+f'<span style="display:block;color:#667085;font-size:13px">{ref}</span>','')
def noimg(size,comp,A,B,grab=None,fallback=False):
    return {"size":size,"comp":comp,"grab":grab,"fallback":fallback,"A":A,"B":B}
def wm(what): return {"what":what[0],"search":what[1],"where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":what[2]}
S=[];D=[];IMG=[]
T=9
DIV='<div style="width:.5cqw;background:var(--line)"></div>'
def col(label,num,color,sub,d,fs=12): return f'<div class="rs" style="--d:{d}s;flex:1;text-align:center"><div class="c-b" style="font-size:3.6cqw;line-height:1.3">{label}</div><div class="c-n" style="font-size:{fs}cqw;color:{color};margin-top:1cqw">{num}</div><div class="c-b" style="font-size:3.3cqw;line-height:1.3;margin-top:1cqw;color:var(--red)">{sub}</div></div>'
def nr(num,unit,d=.2): return f'<div class="rs" style="--d:{d}s;display:flex;justify-content:center;align-items:baseline;gap:3cqw"><span class="c-n" style="font-size:15cqw">{num}</span><span class="c-b" style="font-size:5cqw">{unit}</span></div>'
def sent(t,extra=''): return f'<span style="display:block;white-space:nowrap;margin-top:1cqw;{extra}">{t}</span>'
def tline(html,d,mt=2.6): return f'<div class="rs c-b" style="--d:{d}s;font-size:4cqw;margin-top:{mt}cqw;text-align:center;white-space:nowrap">{html}</div>'
R=lambda t:f'<span class="hl" style="font-weight:900">{t}</span>'
# ---------- 1 cover with a hook
S.append(sec(1,T,'Centered hook on top, photo in the lower 57%, forward arrow',card(
 '<div class="tz" style="right:6cqw;left:6cqw;top:5cqw;height:58cqw;text-align:center"><div class="rs c-h" style="--d:.2s;font-size:8.6cqw;text-align:center">كم هو سيئ سجل<br>إينيوس '+R('فعلًا')+'؟</div>'
 +tline(R('١١٦ يومًا')+' بين تمديد تين هاغ وإقالته',.5,4)
 +tline('نيس: من المركز '+R('٤')+' إلى '+R('١٦')+' في موسم واحد',.7)
 +tline('لوزان: '+R('هبوطان')+' في أقل من ٥ سنوات',.9)
 +'<div class="rs c-b" style="--d:1.2s;font-size:3.9cqw;margin-top:4cqw;text-align:center;color:var(--navy);font-weight:700">٨ وقائع من الملف الكامل... اسحب</div></div>'
 +ph('left:0;right:0;bottom:0;height:66cqw','fbs bf','Photo: Ratcliffe'),True),[
 ('Headline (centered, two lines)','كم هو سيئ سجل إينيوس فعلًا؟','ar h'),
 ('Teaser 1','١١٦ يومًا بين تمديد تين هاغ وإقالته','ar'),
 ('Teaser 2','نيس: من المركز ٤ إلى ١٦ في موسم واحد','ar'),
 ('Teaser 3','لوزان: هبوطان في أقل من ٥ سنوات','ar'),
 ('Call to swipe (blue)','٨ وقائع من الملف الكامل... اسحب','ar'),
 ('Red mark','«فعلًا» والأرقام الثلاثة','ar'),
 ('Other hooks','If you want a different hook: «٣ أندية... قرارات متقلبة: مشروع أم فوضى؟» or «١١٦ يومًا فقط... وبعدها أقالوه». Tell me which and I will swap it.','') ,
 src('Facts on slides 2, 6 and 7','Each teaser is a fact from a later slide: 116 days (slide 2), Nice 4th to 16th (slide 6), Lausanne relegated in 2018 and 2022 (slide 7).'),
 ('Check this','«كم هو سيئ» frames a critical file. The report itself says it is not a balanced review of everything INEOS has done. The caption should say «ملف نقدي» so it is clear.','')]))
D.append("Headline: كم هو سيئ سجل إينيوس فعلًا؟\nTeaser 1: ١١٦ يومًا بين تمديد تين هاغ وإقالته\nTeaser 2: نيس: من المركز ٤ إلى ١٦ في موسم واحد\nTeaser 3: لوزان: هبوطان في أقل من ٥ سنوات\nCall to swipe: ٨ وقائع من الملف الكامل... اسحب")
IMG.append(noimg("1:1 square, generate at 1024x1024 or larger","Keep the top fifth open and bright. It fades into the white. Subject sits in the lower two thirds.",
 "Editorial photograph of three empty football stadium stands side by side in different weather, one under snow-capped mountains, one by a sea coast, one under grey northern English sky, as a clean triptych, nobody present. Keep the top fifth as soft pale sky. Square 1:1. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of an empty boardroom table with three closed folders in a row and a floor-to-ceiling window onto a grey city, nobody present. Keep the top fifth soft and bright. Square 1:1. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Sir Jim Ratcliffe","Jim Ratcliffe","The hook is about his group, so a real photo is better. Check the licence.")),True))
# ---------- 2 three timelines
def tcol(who,num,sub,d): return f'<div class="rs" style="--d:{d}s;flex:1;text-align:center"><div class="c-h" style="font-size:4.4cqw;line-height:1.3">{who}</div><div class="c-n" style="font-size:12cqw;margin-top:.8cqw">{num}</div><div class="c-b" style="font-size:3.2cqw;line-height:1.35;margin-top:.8cqw">{sub}</div></div>'
S.append(sec(2,T,'Photo on top (33%), headline, three stat columns and two detail lines below',card(
 ph('left:0;right:0;top:0;height:46cqw','ft','Photo: United managers')
 +'<div class="tz" style="right:6cqw;left:6cqw;top:41cqw;height:84cqw"><div class="rs c-h" style="--d:.2s;font-size:5.8cqw;text-align:center">٣ قرارات كبرى... بلا استقرار</div><div style="display:flex;gap:2.5cqw;align-items:stretch;margin-top:4cqw">'
 +tcol('تين هاغ','١١٦','يومًا من التمديد<br>إلى الإقالة',.6)+DIV+tcol('أشوورث','٥','أشهر مديرًا<br>رياضيًا',.8)+DIV+tcol('أموريم','١٤','شهرًا حتى<br>الإقالة',1)
 +'</div><div class="rs c-b" style="--d:1.3s;margin-top:5cqw;text-align:center;font-size:3.4cqw;color:var(--red)">'+sent('المركز ١٥ في ٢٠٢٤-٢٥: الأدنى منذ ١٩٧٤')+sent('وخسر نهائي الدوري الأوروبي')+'</div></div>'),[
 ('Headline','٣ قرارات كبرى... بلا استقرار','ar h'),
 ('Column 1','تين هاغ: ١١٦ يومًا من التمديد إلى الإقالة','ar'),
 ('Column 2','أشوورث: ٥ أشهر مديرًا رياضيًا','ar'),
 ('Column 3','أموريم: ١٤ شهرًا حتى الإقالة','ar'),
 ('Detail (red, two lines)','المركز ١٥ في ٢٠٢٤-٢٥: الأدنى منذ ١٩٧٤<br>وخسر نهائي الدوري الأوروبي','ar'),
 ('Red mark','الأرقام الثلاثة وسطرا التفصيل','ar'),
 src('Report section 1, points 1, 3, 4 and 5 · refs [5][6][9][10] Reuters','«في 4 يوليو 2024، أعلن يونايتد تمديد عقد إريك تين هاغ ... وفي 28 أكتوبر من العام نفسه، أقالته الإدارة والفريق في المركز الرابع عشر.» «وفي 8 ديسمبر، أعلن النادي رحيله بالتراضي، بعد خمسة أشهر فقط.» «ثم أقاله في 5 يناير 2026 بعد نحو 14 شهرًا.»','«أنهى يونايتد موسم 2024–25 في المركز الخامس عشر؛ أدنى مركز له منذ موسم الهبوط عام 1974، بحسب رويترز. كما خسر نهائي الدوري الأوروبي».'),
 ('Check this','116 is my own count of 4 July to 28 October. The report says the Ten Hag decision was INEOS\'s own (it kept him, then sacked him). The Amorim fee (about £11m) is left off because I could not tie it to a page. Spelling to confirm: «أشوورث», «أموريم».','')]))
D.append("Headline: ٣ قرارات كبرى... بلا استقرار\nColumn 1: تين هاغ: ١١٦ يومًا من التمديد إلى الإقالة\nColumn 2: أشوورث: ٥ أشهر مديرًا رياضيًا\nColumn 3: أموريم: ١٤ شهرًا حتى الإقالة\nDetail line 1: المركز ١٥ في ٢٠٢٤-٢٥: الأدنى منذ ١٩٧٤\nDetail line 2: وخسر نهائي الدوري الأوروبي")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Three subjects across the upper four fifths.",
 "Editorial photograph of three plain empty dark leather office chairs in a row behind a long desk in a bright boardroom, each with a closed folder in front of it, nobody present. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of three different football manager's coats hanging on pegs in an empty dressing room, bright light from a window, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("Real, licensed photos of Ten Hag, Dan Ashworth and Ruben Amorim, one per column","Erik ten Hag; Dan Ashworth; Ruben Amorim","You already have Ten Hag photos in your Drive folder from the earlier carousel. Check the licence for the others.")),True))
# ---------- 3 cost vs cuts
S.append(sec(3,T,'Photo on top (35%), headline, two stat columns and two detail lines below',card(
 ph('left:0;right:0;top:0;height:50cqw','ft','Photo: Old Trafford')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:45cqw;height:80cqw"><div class="rs c-h" style="--d:.2s;font-size:6cqw;text-align:center">فاتورة التغيير... وفاتورة التقشف</div><div style="display:flex;gap:3cqw;align-items:stretch;margin-top:4cqw">'
 +col('تكاليف رحيل تين هاغ<br>وطاقم رياضي','١٤٫٥','var(--red)','مليون جنيه',.6,13)+DIV+col('وظيفة ألغيت في ٢٠٢٤','٢٥٠','var(--red)','تقريبًا، و١٥٠-٢٠٠ مقترحة',.8,13)
 +'</div><div class="rs c-b" style="--d:1.2s;margin-top:5cqw;text-align:center;font-size:3.4cqw"><span style="display:block;white-space:nowrap;color:var(--navy)">ثم وقف الغداء المجاني لموظفي أولد ترافورد</span><span style="display:block;white-space:nowrap;margin-top:1.4cqw;color:var(--red)">توفير متوقع: أكثر من مليون جنيه سنويًا</span></div></div>'),[
 ('Headline','فاتورة التغيير... وفاتورة التقشف','ar h'),
 ('Column 1','تكاليف رحيل تين هاغ وطاقم رياضي: ١٤٫٥ مليون جنيه','ar'),
 ('Column 2','وظيفة ألغيت في ٢٠٢٤: ٢٥٠ تقريبًا، و١٥٠-٢٠٠ مقترحة','ar'),
 ('Detail line 1 (blue)','ثم وقف الغداء المجاني لموظفي أولد ترافورد','ar'),
 ('Detail line 2 (red)','توفير متوقع: أكثر من مليون جنيه سنويًا','ar'),
 ('Red mark','«١٤٫٥» و «٢٥٠» وسطر التوفير','ar'),
 src('Report section 1 point 2 and section 2 points 7 and 8 · refs [7][8][3] RFI, Flashscore, BBC','«أظهرت الحسابات المالية المنشورة في فبراير 2025 تكاليف استثنائية قدرها 14.5 مليون جنيه مرتبطة برحيل تين هاغ وأعضاء آخرين من الطاقم الرياضي.»','«شهد عام 2024 الاستغناء عن نحو 250 موظفًا. وفي فبراير 2025، أعلن النادي أن ما بين 150 و200 وظيفة إضافية قد تُلغى.»','«أعلن النادي وقف تقديم وجبات الغداء المجانية لموظفي أولد ترافورد، بتوفير متوقع يزيد على مليون جنيه سنويًا.»'),
 ('Check this','The report says the two figures should not be added or called «Ten Hag\'s compensation», and that the 150-200 jobs were «may be cut», so the slide says «مقترحة». Putting them side by side is the report\'s own point, not a claim that one caused the other. The report also notes the club\'s losses ran for five years before INEOS.','')]))
D.append("Headline: فاتورة التغيير... وفاتورة التقشف\nColumn 1: تكاليف رحيل تين هاغ وطاقم رياضي: ١٤٫٥ مليون جنيه\nColumn 2: وظيفة ألغيت في ٢٠٢٤: ٢٥٠ تقريبًا، و١٥٠-٢٠٠ مقترحة\nDetail line 1: ثم وقف الغداء المجاني لموظفي أولد ترافورد\nDetail line 2: توفير متوقع: أكثر من مليون جنيه سنويًا")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.",
 "Editorial photograph of an open-plan office with rows of empty desks and switched-off monitors, bright daylight through large windows, nobody present. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of an empty staff canteen with clean tables and chairs in bright daylight, a closed serving counter, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real photo of Old Trafford from outside in daylight","Old Trafford stadium","The slide is about the club, so a real stadium photo works. Check the licence.")),True))
# ---------- 4 Ten Hag promises
S.append(sec(4,T,'Photo on top (50%), headline and three promise columns below',card(
 ph('left:0;right:0;top:0;height:66cqw','ft','Photo: Ten Hag')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:60cqw;height:65cqw"><div class="rs c-h" style="--d:.2s;font-size:6.4cqw;text-align:center">تين هاغ: «وعدوني بثلاثة أشياء»</div><div style="display:flex;margin-top:5cqw;align-items:stretch"><div class="rs c-h" style="--d:.6s;flex:1;text-align:center;font-size:6cqw">الولاء</div>'+DIV+'<div class="rs c-h" style="--d:.8s;flex:1;text-align:center;font-size:6cqw">الدعم</div>'+DIV+'<div class="rs c-h" style="--d:1s;flex:1;text-align:center;font-size:6cqw">التواصل</div></div><div class="rs c-b" style="--d:1.3s;margin-top:5cqw;text-align:center;font-size:4cqw;color:var(--red)">«لكن الوعود... لم يلتزموا بها»</div><div class="rs c-b" style="--d:1.6s;margin-top:3cqw;text-align:center;font-size:3.3cqw;color:var(--navy)">من مقابلته مع The Athletic، ٢٠ أكتوبر ٢٠٢٦</div></div>'),[
 ('Headline','تين هاغ: «وعدوني بثلاثة أشياء»','ar h'),
 ('Column 1','الولاء','ar h'),('Column 2','الدعم','ar h'),('Column 3','التواصل','ar h'),
 ('Quote (red)','«لكن الوعود... لم يلتزموا بها»','ar'),
 ('Line (blue)','من مقابلته مع The Athletic، ٢٠ أكتوبر ٢٠٢٦','ar'),
 ('Red mark','سطر «لكن الوعود... لم يلتزموا بها»','ar'),
 src('Report section 2, point 13 · ref [16] The Athletic','«في مقابلة مع The Athletic نُشرت في 20 أكتوبر 2026، قال تين هاغ إن الإدارة وعدته بالولاء والدعم والتواصل، لكنها لم تفِ بهذه الوعود.»','From the Ten Hag article you shared earlier: «They promised me loyalty, they promised me backing, they promised communication... But the promises, they didn\'t keep.»'),
 ('Check this','This is a former manager\'s account, not a ruling. The report says so itself. The slide keeps it as his words and attributes it.','')]))
D.append("Headline: تين هاغ: «وعدوني بثلاثة أشياء»\nColumn 1: الولاء\nColumn 2: الدعم\nColumn 3: التواصل\nQuote: «لكن الوعود... لم يلتزموا بها»\nLine: من مقابلته مع The Athletic، ٢٠ أكتوبر ٢٠٢٦")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.",
 "Editorial photograph of a Mediterranean hotel terrace at golden hour, a small round table with two empty cane chairs facing each other, two untouched glasses of water, white stone wall and pale sea beyond, no people. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of a handshake-less empty meeting table with two pens and two closed notebooks facing each other, soft window light, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Erik ten Hag","Erik ten Hag","You already have Ten Hag photos in your Drive folder from the earlier carousel.")),True))
# ---------- 5 Nice quote
S.append(sec(5,T,'Photo on top (42%), headline, one line and a big quote below',card(
 ph('left:0;right:0;top:0;height:56cqw','ft','Photo: Nice stadium')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:50cqw;height:75cqw"><div class="rs c-h" style="--d:.2s;font-size:6.6cqw;text-align:center">راتكليف عن نيس</div><div class="rs c-b" style="--d:.6s;margin-top:4cqw;text-align:center;font-size:3.8cqw;color:var(--navy)">قال إنه لا يستمتع كثيرًا بمشاهدته</div><div class="rs c-h" style="--d:1s;font-size:8.2cqw;margin-top:7cqw;text-align:center;color:var(--red);line-height:1.35">«كانوا أفضل بكثير<br>دون تدخلنا»</div><div class="rs c-b" style="--d:1.5s;margin-top:6cqw;text-align:center;font-size:3.4cqw">قالها عن موسم ٢٠٢٤-٢٥: نيس رابع وفي دوري الأبطال</div></div>'),[
 ('Headline','راتكليف عن نيس','ar h'),
 ('Line (blue)','قال إنه لا يستمتع كثيرًا بمشاهدته','ar'),
 ('Big quote (red)','«كانوا أفضل بكثير دون تدخلنا»','ar h'),
 ('Detail','قالها عن موسم ٢٠٢٤-٢٥: نيس رابع وفي دوري الأبطال','ar'),
 ('Red mark','سطر الاقتباس الكبير','ar'),
 src('Report section 3, points 15 and 16 · ref [12] The Athletic','«قال راتكليف في مقابلة مع The Times، نقلتها The Athletic، إنه لا يستمتع كثيرًا بالذهاب لمشاهدة نيس؛ فهناك لاعبون جيدون، لكن مستوى كرة القدم ليس مرتفعًا بما يكفي لإثارته.»','«اضطرت إينيوس إلى الابتعاد مؤقتًا عن إدارة نيس خلال موسم 2024–25 ... أنهى نيس ذلك الموسم رابعًا، وتأهل إلى دوري الأبطال.» راتكليف: «لقد كانوا أفضل بكثير دون تدخلنا! ربما هناك درس في ذلك أيضًا».'),
 ('Check this','The first line is the report\'s paraphrase, not a word-for-word quote, so it is not in quotation marks. The big quote is word for word. The report warns it proves INEOS said it, not that its absence caused the rise.','')]))
D.append("Headline: راتكليف عن نيس\nLine: قال إنه لا يستمتع كثيرًا بمشاهدته\nBig quote: «كانوا أفضل بكثير دون تدخلنا»\nDetail: قالها عن موسم ٢٠٢٤-٢٥: نيس رابع وفي دوري الأبطال")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Stadium in the upper four fifths.",
 "Editorial photograph of a Mediterranean football stadium by the coast at dusk, empty pitch under floodlights, palm trees beyond the stands, nobody present. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of an empty VIP box balcony overlooking a football pitch at night, two empty leather seats, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Jim Ratcliffe, or the Allianz Riviera stadium in Nice","Jim Ratcliffe; Allianz Riviera","The quote is his, so a real photo of him works well. Check the licence.")),True))
# ---------- 6 Nice collapse
S.append(sec(6,T,'Photo on top (40%), headline, two stat columns and two detail lines below',card(
 ph('left:0;right:0;top:0;height:52cqw','ft','Photo: Nice fans')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:48cqw;height:77cqw"><div class="rs c-h" style="--d:.2s;font-size:5.8cqw;text-align:center">نيس: من الرابع إلى السادس عشر</div><div style="display:flex;gap:3cqw;align-items:stretch;margin-top:4cqw">'
 +col('٢٠٢٤-٢٥','٤','var(--navy)','المركز الرابع',.6,14)+DIV+col('٢٠٢٥-٢٦','١٦','var(--red)','ملحق البقاء أمام سانت إتيان',.8,14)
 +'</div><div class="rs c-b" style="--d:1.2s;margin-top:4.5cqw;text-align:center;font-size:3.2cqw"><span style="display:block;white-space:nowrap;color:var(--navy)">٠-٠ أمام ميتز الهابط، ثم اقتحام جماهيري للملعب</span><span style="display:block;white-space:nowrap;margin-top:1.4cqw;color:var(--red)">المدرب: ٣ أيام بلا اتصال من مسؤول إينيوس بعد الأزمة</span></div></div>'),[
 ('Headline','نيس: من الرابع إلى السادس عشر','ar h'),
 ('Column 1','٢٠٢٤-٢٥: المركز الرابع (٤)','ar'),
 ('Column 2 (red)','٢٠٢٥-٢٦: ملحق البقاء أمام سانت إتيان (١٦)','ar'),
 ('Detail line 1 (blue)','٠-٠ أمام ميتز الهابط، ثم اقتحام جماهيري للملعب','ar'),
 ('Detail line 2 (red)','المدرب: ٣ أيام بلا اتصال من مسؤول إينيوس بعد الأزمة','ar'),
 ('Red mark','«١٦»، «ملحق البقاء...» والسطر الأخير','ar'),
 src('Report section 3, points 17, 18 and 21 · refs [12][20] The Athletic, FotMob','«أنهى نيس موسم 2025–26 في المركز السادس عشر، واضطر إلى خوض ملحق البقاء أمام سانت إتيان.» «تعادل 0–0، وفشل في ضمان البقاء المباشر، ثم اقتحمت جماهير أرض الملعب بعد النهاية.»','«قال فرانك إيز إنه اقترب من الرحيل بعد أزمة مركز التدريب، وإن جان كلود بلان، المسؤول التنفيذي عن القطاع الرياضي في إينيوس، لم يتواصل معه لمدة ثلاثة أيام، ثم فعل ذلك برسالة نصية.»'),
 ('Check this','The pitch invasion and the attack on players at the training centre were by fans, and the report says not to blame INEOS for them. The slide only states that the invasion happened. The «three days» line is the coach\'s own claim, reported by The Athletic. Spelling to confirm: «ميتز», «سانت إتيان».','')]))
D.append("Headline: نيس: من الرابع إلى السادس عشر\nColumn 1: ٢٠٢٤-٢٥: المركز الرابع (٤)\nColumn 2: ٢٠٢٥-٢٦: ملحق البقاء أمام سانت إتيان (١٦)\nDetail line 1: ٠-٠ أمام ميتز الهابط، ثم اقتحام جماهيري للملعب\nDetail line 2: المدرب: ٣ أيام بلا اتصال من مسؤول إينيوس بعد الأزمة")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.",
 "Editorial photograph of red and black football scarves and a plain flag scattered on the grass of an empty stadium pitch at dusk, nobody present. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of a closed training-ground gate with a team bus parked behind it in grey daylight, no signage, nobody visible. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Nice fans or the Allianz Riviera","Allianz Riviera","Avoid anything that shows identifiable fans in the attack. Check the licence.")),True))
# ---------- 7 Lausanne relegations
S.append(sec(7,T,'Photo on the right (48%), number block and text on the left',card(
 ph('right:0;top:0;bottom:0;width:48cqw','fr bf','Photo: Lausanne')
 +'<div class="tz" style="left:6cqw;width:44cqw;top:8cqw;bottom:14cqw"><div class="rs c-n" style="--d:.2s;font-size:19cqw;text-align:center">٢</div><div class="rs c-b" style="--d:.45s;font-size:5cqw;line-height:1.2;margin-top:1.2cqw;text-align:center">هبوطان</div><div class="rs c-h" style="--d:.7s;font-size:5.6cqw;margin-top:2.6cqw;text-align:center">لوزان بعد إينيوس</div><div class="rs c-b" style="--d:1s;margin-top:4cqw;text-align:center;font-size:3.5cqw"><span style="display:block">هبط في موسم الاستحواذ ٢٠١٧-١٨.</span><span style="display:block;margin-top:2cqw">وهبط مرة ثانية في ٢٠٢٢.</span></div><div class="rs c-b" style="--d:1.3s;margin-top:4cqw;text-align:center;font-size:3.4cqw;color:var(--red)">واليوم: الأخير بـ٦ نقاط من ١١ مباراة</div></div>'),[
 ('Big number','٢','ar h'),('Unit','هبوطان','ar'),
 ('Headline','لوزان بعد إينيوس','ar h'),
 ('Body (one sentence per line)','هبط في موسم الاستحواذ ٢٠١٧-١٨.<br>وهبط مرة ثانية في ٢٠٢٢.','ar'),
 ('Detail (red)','واليوم: الأخير بـ٦ نقاط من ١١ مباراة','ar'),
 ('Red mark','«٢» والسطر الأخير','ar'),
 src('Report section 4, points 24, 25 and 28 · refs [1][23][25][26] club site, FBref, Sofascore, YSScores','«اشترت إينيوس لوزان في نوفمبر 2017، وانتهى موسم 2017–18 بهبوطه إلى الدرجة الثانية.» «بعد العودة إلى الدرجة الأولى، هبط لوزان مجددًا في موسم 2021–22.»','«وبعد خسارة سيون يوم 25 أكتوبر، بقي أخيرًا برصيد ست نقاط من 11 مباراة.»'),
 ('Check this','The report notes Lausanne was 5th, not last, when INEOS bought it, so the slide does not say INEOS relegated a leading side. The league table comes from score sites I could not open. «موسم الاستحواذ ٢٠١٧-١٨» is the season INEOS bought the club (November 2017).','')]))
D.append("Big number: ٢\nUnit: هبوطان\nHeadline: لوزان بعد إينيوس\nBody: هبط في موسم الاستحواذ ٢٠١٧-١٨.\nوهبط مرة ثانية في ٢٠٢٢.\nDetail: واليوم: الأخير بـ٦ نقاط من ١١ مباراة")
IMG.append(noimg("2:3 portrait, generate at 1024x1536 or larger","Keep the left fifth open and bright. It fades into the white. Subject in the right four fifths.",
 "Editorial photograph of a small football stadium beside a large Alpine lake in grey light, empty terraces and an empty pitch, snow-capped mountains faintly behind, nobody present. Keep the left fifth as soft pale haze. Portrait 2:3. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of a blank league table board on a wall in a bright corridor, empty slots, nobody present, no readable text. Keep the left fifth soft and bright. Portrait 2:3. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of the Lausanne stadium (Stade de la Pontaise) from outside","Stade de la Pontaise","The slide names the club, so a real stadium photo works. Check the licence.")),True))
# ---------- 8 Lausanne identity
S.append(sec(8,T,'Photo on top (42%), number, headline, two sentences and a quote below',card(
 ph('left:0;right:0;top:0;height:54cqw','ft','Photo: Lausanne badge')
 +'<div class="tz" style="right:6cqw;left:6cqw;top:49cqw;height:76cqw">'+nr('٤٠','صفقة في ١٨ شهرًا')+'<div class="rs c-h" style="--d:.6s;font-size:5.8cqw;margin-top:3cqw;text-align:center">«انتقالات بالمروحية»</div><div class="rs c-b" style="--d:1s;margin-top:3cqw;text-align:center;font-size:3.4cqw">'+sent('وصف وكلاء المرحلة هكذا، بحسب مراجعة 90min.')+sent('وعُدّل الشعار ليحاكي هوية إينيوس، ثم تراجعوا.')+'</div><div class="rs c-b" style="--d:1.3s;margin-top:3.5cqw;text-align:center;font-size:3.4cqw;color:var(--red)">'+sent('نائب الرئيس السابق: «فقدان هوية')+sent('كان مكلفًا جدًا»')+'</div></div>'),[
 ('Big number','٤٠','ar h'),('Unit','صفقة في ١٨ شهرًا','ar'),
 ('Headline','«انتقالات بالمروحية»','ar h'),
 ('Body (one sentence per line)','وصف وكلاء المرحلة هكذا، بحسب مراجعة 90min.<br>وعُدّل الشعار ليحاكي هوية إينيوس، ثم تراجعوا.','ar'),
 ('Detail (red)','نائب الرئيس السابق: «فقدان هوية كان مكلفًا جدًا»','ar'),
 ('Red mark','«٤٠» والسطرين الأخيرين','ar'),
 src('Report section 4, points 23, 26 and 27 · refs [12][21][22][24] The Athletic, 24 heures, RTS, 90min','«وصفت مراجعة 90min المرحلة بأنها شهدت نحو 40 صفقة خلال 18 شهرًا، ونقلت وصف بعض الوكلاء لها بأنها «انتقالات بالمروحية».»','«عُدّل شعار لوزان بحيث يحاكي حرف «o» في اسم النادي الهوية البصرية لإينيوس. أثار ذلك اعتراض الجماهير، قبل التراجع عن التغيير.»','شتيفان نيلين، نائب رئيس لوزان السابق: «قلبت إينيوس كل شيء رأسًا على عقب ... ما أدى إلى فقدان هوية كان مكلفًا جدًا».'),
 ('Check this','The report says the 40 figure is from a press review, not club accounts, so the slide attributes it to 90min. The Nellen line is his own assessment, shown as a quote. The slide shortens his words to the last phrase.','')]))
D.append("Big number: ٤٠\nUnit: صفقة في ١٨ شهرًا\nHeadline: «انتقالات بالمروحية»\nBody: وصف وكلاء المرحلة هكذا، بحسب مراجعة 90min.\nوعُدّل الشعار ليحاكي هوية إينيوس، ثم تراجعوا.\nDetail: نائب الرئيس السابق: «فقدان هوية كان مكلفًا جدًا»")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.",
 "Editorial photograph of a helicopter landing pad painted on the roof of a plain building under grey Alpine sky, a lake in the distance, nobody present, no markings. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of a football club badge outline sketched in chalk on a plain concrete wall, half smudged, nobody present, no readable marks. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real photo of the Lausanne-Sport badge or stadium","Lausanne-Sport","The slide is about the badge, so a real image of the club works. Check the licence; a badge may be trademarked.")),True))
# ---------- 9 closer
S.append(sec(9,T,'Photo on top (30%), headline, two lines, question and four icons below',card(
 ph('left:0;right:0;top:0;height:40cqw','ft','Photo: three crests')
 +'<div class="tz" style="right:6cqw;left:6cqw;top:34cqw;height:78cqw"><div class="rs c-h" style="--d:.2s;font-size:5.6cqw;text-align:center">٣ أندية... ولاعبان فقط انتقلا بينها</div><div class="rs c-b" style="--d:.6s;margin-top:4cqw;text-align:center;font-size:3.5cqw">'+sent('منذ ٢٠٢٣: فريدريكسون وكوني، من يونايتد إلى لوزان.')+sent('مدير نيس الرياضي السابق: أولوية يونايتد كانت البيع.','color:var(--red)')+'</div><div class="rs c-h" style="--d:1.2s;font-size:6cqw;margin-top:5cqw;text-align:center;color:var(--red)">إحكيلي</div><div class="rs c-b" style="--d:1.5s;font-size:4.7cqw;margin-top:2.6cqw;text-align:center;color:var(--red)">شو أكبر غلطة عملتها إينيوس؟</div></div>'
 +icons_svg,False),[
 ('Headline','٣ أندية... ولاعبان فقط انتقلا بينها','ar h'),
 ('Body (one sentence per line, second red)','منذ ٢٠٢٣: فريدريكسون وكوني، من يونايتد إلى لوزان.<br>مدير نيس الرياضي السابق: أولوية يونايتد كانت البيع.','ar'),
 ('Question line 1 (red)','إحكيلي','ar h'),
 ('Question line 2 (red, bigger)','شو أكبر غلطة عملتها إينيوس؟','ar'),
 ('Icons','Heart (red), comment (green), share (navy), save (navy), close together.',''),
 ('Red mark','سطر موريس، «إحكيلي» والسؤال','ar'),
 src('Report section 5, point 30 · ref [12] The Athletic','«انتقل لاعبان فقط بين الأندية الثلاثة منذ 2023: تايلر فريدريكسون وسيكو كوني، من يونايتد إلى لوزان، أحدهما انتقالًا والآخر إعارة.» «وقال فلوريان موريس، المدير الرياضي السابق لنيس، إنه ناقش حلولًا مع يونايتد، من بينها شراء لاعب ثم إعارته لنيس، لكن أولوية النادي الإنجليزي كانت البيع.»'),
 ('Check this','The second line is Maurice\'s account as reported by The Athletic, so it is attributed. The report says the slide should not claim the multi-club model was a mistake on this evidence alone. Spelling to confirm: «فريدريكسون» (Fredricson), «كوني», «موريس».','')]))
D.append("Headline: ٣ أندية... ولاعبان فقط انتقلا بينها\nBody: منذ ٢٠٢٣: فريدريكسون وكوني، من يونايتد إلى لوزان.\nمدير نيس الرياضي السابق: أولوية يونايتد كانت البيع.\nQuestion line 1: إحكيلي\nQuestion line 2: شو أكبر غلطة عملتها إينيوس؟")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.",
 "Editorial photograph of three plain empty wooden chairs in a row on a bright stadium pitch, each facing a different empty stand, no people, no signage. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of three plain cardboard boxes in a row on a bright changing-room floor, one with an open flap, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("Three real stadium photos for the band (Old Trafford, Allianz Riviera, Stade de la Pontaise)","Old Trafford; Allianz Riviera; Stade de la Pontaise","Pick one wide shot per club and place them side by side.")),True))

th='padding:6px 8px;border-bottom:1px solid var(--line)'
def tr(*c): return '<tr>'+''.join(f'<td style="padding:6px 8px;vertical-align:top">{x}</td>' for x in c)+'</tr>'
sources=f'''<div style="margin:0 0 34px;padding:18px 20px;border:1px solid var(--line);border-radius:10px;background:#FBFCFE"><h2 style="margin:0 0 6px;font-size:20px">Source: check every claim yourself</h2><p style="margin:0 0 12px;color:var(--mute)">Everything comes from the research report you pasted, a critical file on INEOS at United, Nice and Lausanne up to 26 October 2026. This version picks the strongest facts from all five sections, not the first ones: 3 slides on United, 2 on Nice, 2 on Lausanne and 1 on the group. Each slide's right-hand column quotes the report's own sentence and the source numbers it cites. I could not open the cited pages, so I checked only what I could: the 116-day count is my own sum, and the Ten Hag dates and promises match the Ten Hag article you shared earlier. The report warns that not every crisis is INEOS's doing, so the slides state facts and leave out accusations.</p><div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;min-width:560px;font-size:14px"><tr style="text-align:left;color:var(--mute)"><th style="{th}">Slide</th><th style="{th}">Club</th><th style="{th}">Claim</th><th style="{th}">Flag</th></tr>
{tr(2,'United','116 days, 5 months, 14 months, 15th lowest since 1974','116 is my sum; Amorim fee left out (no matching page)')}
{tr(3,'United','£14.5m exceptional costs vs 250 jobs cut, free lunches ended','Do not add the figures; 150-200 jobs only proposed')}
{tr(4,'United','Ten Hag: promised loyalty, backing, communication','His account, not a ruling')}
{tr(5,'Nice','Ratcliffe: «much better without our interference»','Says it, does not prove the cause')}
{tr(6,'Nice','4th to 16th, Metz 0-0, three days without contact','Fan acts are not INEOS’s; coach claim is reported')}
{tr(7,'Lausanne','Relegated 2018 and 2022, bottom with 6 from 11','Was 5th at takeover; table not opened')}
{tr(8,'Lausanne','40 transfers in 18 months, badge change, Nellen quote','40 is a press review figure, attributed to 90min')}
{tr(9,'Group','2 transfers since 2023; Maurice on United’s priority','Maurice’s account, reported')}
</table></div><p style="margin:12px 0 0;color:var(--mute);font-size:13px">Left out on purpose, in favour of the stronger Nice and Lausanne facts: Ratcliffe’s immigration remarks and apology (a reputation row, and the FA took no action), the £66 ticket price, season-ticket moves for hospitality, the women’s team move and Ratcliffe’s comments, United’s league position after the Bournemouth loss (table page not opened), the Lazard search for a Nice buyer at about €250m, and the multi-club ownership rules. The report’s own «do not use» list is respected: no «fired 18 coaches», no cut to the disabled supporters’ budget, no «INEOS relegated Nice», and no blaming INEOS for the fan attack.</p></div>'''
