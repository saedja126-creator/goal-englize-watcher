RED={1:'«الأرقام» و «أهم ٨ وقائع...»',2:'«١١٦» والسطر الأخير',3:'«١٤٫٥» والسطر الأخير',4:'«٥» والسطر الأخير',5:'«١٤» والسطرين الأخيرين',6:'«٢٥٠» و «١٥٠-٢٠٠»، وسطر التوفير',7:'«١٦»، «ملحق...»، وسطر راتكليف',8:'«٦» والسطر الأخير',9:'«إحكيلي» والسؤال'}
def src(ref,*lines):
    q=''.join(f'<span dir="rtl" style="display:block;margin-bottom:6px;text-align:right">{l}</span>' for l in lines)
    return ('From the report',q+f'<span style="display:block;color:#667085;font-size:13px">{ref}</span>','')
def noimg(size,comp,A,B,grab=None,fallback=False):
    return {"size":size,"comp":comp,"grab":grab,"fallback":fallback,"A":A,"B":B}
def wm(what): return {"what":what[0],"search":what[1],"where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":what[2]}
S=[];D=[];IMG=[]
T=9
def col(label,num,color,sub,d,fs=12): return f'<div class="rs" style="--d:{d}s;flex:1;text-align:center"><div class="c-b" style="font-size:3.6cqw;line-height:1.3">{label}</div><div class="c-n" style="font-size:{fs}cqw;color:{color};margin-top:1cqw">{num}</div><div class="c-b" style="font-size:3.4cqw;line-height:1.3;margin-top:1cqw;color:var(--red)">{sub}</div></div>'
DIV='<div style="width:.5cqw;background:var(--line)"></div>'
def nr(num,unit,d=.2): return f'<div class="rs" style="--d:{d}s;display:flex;justify-content:center;align-items:baseline;gap:3cqw"><span class="c-n" style="font-size:15cqw">{num}</span><span class="c-b" style="font-size:5cqw">{unit}</span></div>'
def sent(t,d,extra=''): return f'<span style="display:block;white-space:nowrap;margin-top:1cqw;{extra}">{t}</span>'
# ---------- 1 cover
S.append(sec(1,T,'Centered text on top, photo in the lower 63%, forward arrow',card(
 '<div class="tz" style="right:7cqw;left:7cqw;top:6cqw;height:50cqw;text-align:center"><div class="rs c-h" style="--d:.2s;font-size:7.8cqw;text-align:center">٣ أندية في يد إينيوس:<br>ماذا تقول <span class="hl">الأرقام</span>؟</div><div class="rs c-b" style="--d:.5s;font-size:3.9cqw;margin-top:4.8cqw;text-align:center;white-space:nowrap">لوزان ٢٠١٧ · نيس ٢٠١٩ · يونايتد ٢٠٢٤</div><div class="rs c-b" style="--d:.8s;margin-top:6cqw;text-align:center;color:var(--red)">أهم ٨ وقائع حتى ٢٦ أكتوبر ٢٠٢٦</div><div class="rs c-b" style="--d:1s;margin-top:1.5cqw;text-align:center;color:var(--navy)">اسحب لترى التفاصيل</div></div>'
 +ph('left:0;right:0;bottom:0;height:84cqw','fbs bf','Photo: Ratcliffe'),True),[
 ('Headline (centered, two lines)','٣ أندية في يد إينيوس: ماذا تقول الأرقام؟','ar h'),
 ('Second line (one line)','لوزان ٢٠١٧ · نيس ٢٠١٩ · يونايتد ٢٠٢٤','ar'),
 ('Body 1 (red)','أهم ٨ وقائع حتى ٢٦ أكتوبر ٢٠٢٦','ar'),
 ('Body 2 (blue)','اسحب لترى التفاصيل','ar'),
 ('Red mark','«الأرقام» وسطر «أهم ٨ وقائع»','ar'),
 src('The report, intro and section 1','«الفترة المشمولة: منذ استحواذ إينيوس على لوزان في 2017، ونيس في 2019، وتوليها إدارة كرة القدم في مانشستر يونايتد في فبراير 2024، حتى 26 أكتوبر 2026.»'),
 ('Check this','The report says INEOS has a minority stake in United and runs football operations. The cover says «في يد إينيوس» (in INEOS\'s hands), which fits Lausanne and Nice (owned) and is looser for United. Say if you want «تحت إدارة إينيوس» instead.','')]))
D.append("Headline: ٣ أندية في يد إينيوس: ماذا تقول الأرقام؟\nSecond line: لوزان ٢٠١٧ · نيس ٢٠١٩ · يونايتد ٢٠٢٤\nBody 1: أهم ٨ وقائع حتى ٢٦ أكتوبر ٢٠٢٦\nBody 2: اسحب لترى التفاصيل")
IMG.append(noimg("1:1 square, generate at 1024x1024 or larger","Keep the top fifth open and bright. It fades into the white. Subject sits in the lower two thirds.",
 "Editorial photograph of three empty football stadium stands side by side in different weather, one under snow-capped mountains, one by a sea coast, one under grey northern English sky, stitched as a clean triptych, nobody present. Keep the top fifth as soft pale sky. Square 1:1. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of an empty boardroom table with three closed folders in a row and a floor-to-ceiling window onto a grey city, nobody present. Keep the top fifth soft and bright. Square 1:1. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Sir Jim Ratcliffe","Jim Ratcliffe","The slide is about his group, so a real photo is better. Check the licence.")),True))
# ---------- 2 Ten Hag 116 days
S.append(sec(2,T,'Photo on top (50%), number, headline and two sentences below',card(
 ph('left:0;right:0;top:0;height:66cqw','ft','Photo: Ten Hag')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:60cqw;height:65cqw">'+nr('١١٦','يومًا')+'<div class="rs c-h" style="--d:.6s;font-size:6.4cqw;margin-top:3cqw;text-align:center">من التمديد إلى الإقالة</div><div class="rs c-b" style="--d:1s;margin-top:3.5cqw;text-align:center;font-size:3.4cqw">'+sent('مدّد يونايتد عقد تين هاغ حتى ٢٠٢٦ في ٤ يوليو ٢٠٢٤.',1)+sent('وأقاله في ٢٨ أكتوبر والفريق في المركز ١٤.',1)+'</div><div class="rs c-b" style="--d:1.3s;margin-top:3cqw;text-align:center;font-size:3.4cqw;color:var(--red)">ودون أي انتصار أوروبي في ذلك الموسم</div></div>'),[
 ('Big number','١١٦','ar h'),('Unit','يومًا','ar'),
 ('Headline','من التمديد إلى الإقالة','ar h'),
 ('Body (one sentence per line)','مدّد يونايتد عقد تين هاغ حتى ٢٠٢٦ في ٤ يوليو ٢٠٢٤.<br>وأقاله في ٢٨ أكتوبر والفريق في المركز ١٤.','ar'),
 ('Detail (red)','ودون أي انتصار أوروبي في ذلك الموسم','ar'),
 ('Red mark','«١١٦» والسطر الأخير','ar'),
 src('Report section 1, point 1 · refs [5][6] Reuters','«في 4 يوليو 2024، أعلن يونايتد تمديد عقد إريك تين هاغ حتى يونيو 2026 ... وفي 28 أكتوبر من العام نفسه، أقالته الإدارة والفريق في المركز الرابع عشر، ودون انتصار أوروبي في ذلك الموسم.»','«خلال نحو 116 يومًا.»'),
 ('Check this','I counted 4 July to 28 October myself: 27 + 31 + 30 + 28 = 116 days, so it matches. The Ten Hag article you shared earlier also says 14th, 11 points, sacked 28 Oct 2024.','')]))
D.append("Big number: ١١٦\nUnit: يومًا\nHeadline: من التمديد إلى الإقالة\nBody: مدّد يونايتد عقد تين هاغ حتى ٢٠٢٦ في ٤ يوليو ٢٠٢٤.\nوأقاله في ٢٨ أكتوبر والفريق في المركز ١٤.\nDetail: ودون أي انتصار أوروبي في ذلك الموسم")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.",
 "Editorial photograph of a calendar page torn off and lying on a wooden desk beside a signed contract folder, soft window light, no readable dates or text, nobody present. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of an empty football manager's office chair behind a desk with a closed laptop, bright daylight, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Erik ten Hag in a Manchester United setting","Erik ten Hag","You already have Ten Hag photos in your Drive folder from the earlier carousel.")),True))
# ---------- 3 £14.5m
S.append(sec(3,T,'Photo on the left (56%), number block and text on the right',card(
 ph('left:0;top:0;bottom:0;width:56cqw','fl bf','Photo: Old Trafford')
 +'<div class="tz" style="right:6cqw;width:38cqw;top:8cqw;bottom:14cqw"><div class="rs c-n" style="--d:.2s;font-size:16cqw;text-align:center">١٤٫٥</div><div class="rs c-b" style="--d:.45s;font-size:5cqw;line-height:1.2;margin-top:1.2cqw;text-align:center">مليون جنيه</div><div class="rs c-h" style="--d:.7s;font-size:6cqw;margin-top:2.6cqw;text-align:center">تكلفة التغيير</div><div class="rs c-b" style="--d:1s;margin-top:4cqw;text-align:center;font-size:3.7cqw">تكاليف استثنائية مرتبطة برحيل تين هاغ وأفراد من الطاقم الرياضي.</div><div class="rs c-b" style="--d:1.3s;margin-top:4cqw;text-align:center;font-size:3.4cqw;color:var(--red)">حسابات فبراير ٢٠٢٥... وليست تعويض تين هاغ وحده</div></div>'),[
 ('Big number','١٤٫٥','ar h'),('Unit','مليون جنيه','ar'),
 ('Headline','تكلفة التغيير','ar h'),
 ('Body','تكاليف استثنائية مرتبطة برحيل تين هاغ وأفراد من الطاقم الرياضي.','ar'),
 ('Detail (red)','حسابات فبراير ٢٠٢٥... وليست تعويض تين هاغ وحده','ar'),
 ('Red mark','«١٤٫٥» والسطر الأخير','ar'),
 src('Report section 1, point 2 · refs [7][8] RFI, Flashscore','«أظهرت الحسابات المالية المنشورة في فبراير 2025 تكاليف استثنائية قدرها 14.5 مليون جنيه مرتبطة برحيل تين هاغ وأعضاء آخرين من الطاقم الرياضي. وكان النادي قد كشف سابقًا أن تكلفة خروج تين هاغ وطاقمه بلغت 10.4 مليون جنيه.»'),
 ('Check this','The report warns not to call the whole £14.5m «Ten Hag\'s compensation» and not to add it to the £10.4m, because they may overlap. The slide follows that. The two sources it cites are a wire rewrite and a sports site, not the accounts themselves.','')]))
D.append("Big number: ١٤٫٥\nUnit: مليون جنيه\nHeadline: تكلفة التغيير\nBody: تكاليف استثنائية مرتبطة برحيل تين هاغ وأفراد من الطاقم الرياضي.\nDetail: حسابات فبراير ٢٠٢٥... وليست تعويض تين هاغ وحده")
IMG.append(noimg("2:3 portrait, generate at 1024x1536 or larger","Keep the right fifth open and bright. It fades into the white. Subject in the left four fifths.",
 "Editorial photograph of a pile of unmarked sealed cash envelopes on a polished boardroom table beside a closed ledger, soft daylight, nobody present, no readable text. Keep the right fifth as soft pale haze. Portrait 2:3. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of a calculator and a sheet of blank columned accounting paper on a clean desk, shallow depth of field, nobody present. Keep the right fifth soft and bright. Portrait 2:3. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real photo of Old Trafford from outside in daylight","Old Trafford stadium","The slide is about the club, so a real stadium photo works. Check the licence.")),True))
# ---------- 4 Ashworth
S.append(sec(4,T,'Photo on the right (48%), number block and text on the left',card(
 ph('right:0;top:0;bottom:0;width:48cqw','fr bf','Photo: Ashworth')
 +'<div class="tz" style="left:6cqw;width:44cqw;top:8cqw;bottom:14cqw"><div class="rs c-n" style="--d:.2s;font-size:19cqw;text-align:center">٥</div><div class="rs c-b" style="--d:.45s;font-size:5cqw;line-height:1.2;margin-top:1.2cqw;text-align:center">أشهر</div><div class="rs c-h" style="--d:.7s;font-size:6cqw;margin-top:2.6cqw;text-align:center">دان أشوورث يرحل</div><div class="rs c-b" style="--d:1s;margin-top:4cqw;text-align:center;font-size:3.6cqw"><span style="display:block">بدأ في يوليو ٢٠٢٤ بعد مفاوضات طويلة مع نيوكاسل.</span><span style="display:block;margin-top:2cqw">وأعلن النادي رحيله في ٨ ديسمبر.</span></div><div class="rs c-b" style="--d:1.3s;margin-top:4cqw;text-align:center;font-size:3.4cqw;color:var(--red)">رحيل «بالتراضي» بحسب النادي</div></div>'),[
 ('Big number','٥','ar h'),('Unit','أشهر','ar'),
 ('Headline','دان أشوورث يرحل','ar h'),
 ('Body (one sentence per line)','بدأ في يوليو ٢٠٢٤ بعد مفاوضات طويلة مع نيوكاسل.<br>وأعلن النادي رحيله في ٨ ديسمبر.','ar'),
 ('Detail (red)','رحيل «بالتراضي» بحسب النادي','ar'),
 ('Red mark','«٥» والسطر الأخير','ar'),
 src('Report section 1, point 3 · ref [9] Reuters','«بدأ دان أشوورث عمله مديرًا رياضيًا في يوليو 2024 بعد مفاوضات طويلة مع نيوكاسل. وفي 8 ديسمبر، أعلن النادي رحيله بالتراضي، بعد خمسة أشهر فقط.»'),
 ('Check this','The report says who decided his exit comes only from press reports, so the slide leaves it out. Spelling to confirm: «أشوورث».','')]))
D.append("Big number: ٥\nUnit: أشهر\nHeadline: دان أشوورث يرحل\nBody: بدأ في يوليو ٢٠٢٤ بعد مفاوضات طويلة مع نيوكاسل.\nوأعلن النادي رحيله في ٨ ديسمبر.\nDetail: رحيل «بالتراضي» بحسب النادي")
IMG.append(noimg("2:3 portrait, generate at 1024x1536 or larger","Keep the left fifth open and bright. It fades into the white. Subject in the right four fifths.",
 "Editorial photograph of an empty executive desk chair in a modern glass-walled office, a single name-plate frame face down on the desk, bright daylight, nobody present. Keep the left fifth as soft pale haze. Portrait 2:3. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of an open office door at the end of a bright corridor, a cardboard box on the floor, nobody present. Keep the left fifth soft and bright. Portrait 2:3. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Dan Ashworth","Dan Ashworth","The slide names him. Check the licence.")),True))
# ---------- 5 Amorim
S.append(sec(5,T,'Photo on top (44%), number, headline, two sentences and two detail lines below',card(
 ph('left:0;right:0;top:0;height:58cqw','ft','Photo: Amorim')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:54cqw;height:71cqw">'+nr('١٤','شهرًا')+'<div class="rs c-h" style="--d:.6s;font-size:5.6cqw;margin-top:3cqw;text-align:center;white-space:nowrap">أموريم: من الاستقدام إلى الإقالة</div><div class="rs c-b" style="--d:1s;margin-top:3cqw;text-align:center;font-size:3.4cqw">'+sent('دفع يونايتد نحو ١١ مليون جنيه لسبورتينغ لاستقدامه.',1)+sent('وأقاله في ٥ يناير ٢٠٢٦ بعد نحو ١٤ شهرًا.',1)+'</div><div class="rs c-b" style="--d:1.3s;margin-top:3cqw;text-align:center;font-size:3.4cqw;color:var(--red)">'+sent('المركز ١٥ في ٢٠٢٤-٢٥: الأدنى منذ ١٩٧٤',1)+sent('وخسر نهائي الدوري الأوروبي',1)+'</div></div>'),[
 ('Big number','١٤','ar h'),('Unit','شهرًا','ar'),
 ('Headline','أموريم: من الاستقدام إلى الإقالة','ar h'),
 ('Body (one sentence per line)','دفع يونايتد نحو ١١ مليون جنيه لسبورتينغ لاستقدامه.<br>وأقاله في ٥ يناير ٢٠٢٦ بعد نحو ١٤ شهرًا.','ar'),
 ('Detail (red, two lines)','المركز ١٥ في ٢٠٢٤-٢٥: الأدنى منذ ١٩٧٤<br>وخسر نهائي الدوري الأوروبي','ar'),
 ('Red mark','«١٤» والسطرين الأخيرين','ar'),
 src('Report section 1, points 4 and 5 · refs [3][10] BBC, Reuters','«دفع يونايتد نحو 11 مليون جنيه لسبورتينغ من أجل استقدام روبن أموريم في نوفمبر 2024، وفق BBC. ثم أقاله في 5 يناير 2026 بعد نحو 14 شهرًا.»','«أنهى يونايتد موسم 2024–25 في المركز الخامس عشر؛ أدنى مركز له منذ موسم الهبوط عام 1974، بحسب رويترز. كما خسر نهائي الدوري الأوروبي».'),
 ('Check this','The £11m figure is credited to BBC in the report, but the link it gives for it, [3], is the BBC redundancies article, so I could not tie the number to a page. Please confirm it. The report also corrects its own earlier line: the lowest finish since 1974 (not since 1989-90). Spelling to confirm: «أموريم», «سبورتينغ».','')]))
D.append("Big number: ١٤\nUnit: شهرًا\nHeadline: أموريم: من الاستقدام إلى الإقالة\nBody: دفع يونايتد نحو ١١ مليون جنيه لسبورتينغ لاستقدامه.\nوأقاله في ٥ يناير ٢٠٢٦ بعد نحو ١٤ شهرًا.\nDetail: المركز ١٥ في ٢٠٢٤-٢٥: الأدنى منذ ١٩٧٤\nوخسر نهائي الدوري الأوروبي")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.",
 "Editorial photograph of a lone manager seen from behind in a dark coat walking down a stadium tunnel toward bright daylight, empty seats beyond, long shadow. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "Editorial photograph of a silver football trophy cup on a plinth with a plain scarf draped beside it, bright stadium lights, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Ruben Amorim","Ruben Amorim","The slide names him. Check the licence.")),True))
# ---------- 6 austerity
S.append(sec(6,T,'Photo on top (42%), headline, two stat columns and two detail lines below',card(
 ph('left:0;right:0;top:0;height:56cqw','ft','Photo: empty office')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:52cqw;height:73cqw"><div class="rs c-h" style="--d:.2s;font-size:6.4cqw;text-align:center">التقشف داخل النادي</div><div style="display:flex;gap:3cqw;align-items:stretch;margin-top:4cqw">'
 +col('وظيفة ألغيت في ٢٠٢٤','٢٥٠','var(--navy)','تقريبًا',.6,12)+DIV+col('وظائف إضافية مقترحة','١٥٠-٢٠٠','var(--red)','فبراير ٢٠٢٥',.8,10)
 +'</div><div class="rs c-b" style="--d:1.2s;margin-top:4.5cqw;text-align:center;font-size:3.4cqw"><span style="display:block;white-space:nowrap;color:var(--navy)">ثم وقف الغداء المجاني لموظفي أولد ترافورد</span><span style="display:block;white-space:nowrap;margin-top:1.4cqw;color:var(--red)">توفير متوقع: أكثر من مليون جنيه سنويًا</span></div></div>'),[
 ('Headline','التقشف داخل النادي','ar h'),
 ('Column 1','وظيفة ألغيت في ٢٠٢٤: ٢٥٠ تقريبًا','ar'),
 ('Column 2','وظائف إضافية مقترحة: ١٥٠-٢٠٠ (فبراير ٢٠٢٥)','ar'),
 ('Detail line 1 (blue)','ثم وقف الغداء المجاني لموظفي أولد ترافورد','ar'),
 ('Detail line 2 (red)','توفير متوقع: أكثر من مليون جنيه سنويًا','ar'),
 ('Red mark','«١٥٠-٢٠٠» وسطر التوفير','ar'),
 src('Report section 2, points 7 and 8 · ref [3] BBC','«شهد عام 2024 الاستغناء عن نحو 250 موظفًا. وفي فبراير 2025، أعلن النادي أن ما بين 150 و200 وظيفة إضافية قد تُلغى، بعد التشاور مع الموظفين.»','«أعلن النادي وقف تقديم وجبات الغداء المجانية لموظفي أولد ترافورد، بتوفير متوقع يزيد على مليون جنيه سنويًا.»'),
 ('Check this','The 150-200 cuts were «may be cut» after consultation, not completed. The slide says «مقترحة» (proposed). The report also says these cuts come from losses built up over five years, before INEOS arrived, so the slide does not blame INEOS for the savings plan itself.','')]))
D.append("Headline: التقشف داخل النادي\nColumn 1: وظيفة ألغيت في ٢٠٢٤: ٢٥٠ تقريبًا\nColumn 2: وظائف إضافية مقترحة: ١٥٠-٢٠٠ (فبراير ٢٠٢٥)\nDetail line 1: ثم وقف الغداء المجاني لموظفي أولد ترافورد\nDetail line 2: توفير متوقع: أكثر من مليون جنيه سنويًا")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Office in the upper four fifths.",
 "Editorial photograph of an open-plan office floor with rows of empty desks and switched-off monitors, bright daylight through large windows, nobody present. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of an empty staff canteen with clean tables and chairs in bright daylight, a closed serving counter, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."))
# ---------- 7 Nice
S.append(sec(7,T,'Photo on top (42%), headline, two stat columns and two detail lines below',card(
 ph('left:0;right:0;top:0;height:54cqw','ft','Photo: Nice')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:50cqw;height:75cqw"><div class="rs c-h" style="--d:.2s;font-size:5.8cqw;text-align:center">نيس: من الرابع إلى السادس عشر</div><div style="display:flex;gap:3cqw;align-items:stretch;margin-top:4cqw">'
 +col('٢٠٢٤-٢٥','٤','var(--navy)','المركز الرابع',.6,14)+DIV+col('٢٠٢٥-٢٦','١٦','var(--red)','ملحق البقاء أمام سانت إتيان',.8,14)
 +'</div><div class="rs c-b" style="--d:1.2s;margin-top:4cqw;text-align:center;font-size:3.3cqw"><span style="display:block;white-space:nowrap;color:var(--navy)">٠-٠ أمام ميتز الهابط، ثم اقتحام جماهيري للملعب</span><span style="display:block;white-space:nowrap;margin-top:1.4cqw;color:var(--red)">راتكليف: «كانوا أفضل بكثير دون تدخلنا»</span></div></div>'),[
 ('Headline','نيس: من الرابع إلى السادس عشر','ar h'),
 ('Column 1','٢٠٢٤-٢٥: المركز الرابع (٤)','ar'),
 ('Column 2 (red)','٢٠٢٥-٢٦: ملحق البقاء أمام سانت إتيان (١٦)','ar'),
 ('Detail line 1 (blue)','٠-٠ أمام ميتز الهابط، ثم اقتحام جماهيري للملعب','ar'),
 ('Detail line 2 (red)','راتكليف: «كانوا أفضل بكثير دون تدخلنا»','ar'),
 ('Red mark','«١٦» و «ملحق البقاء...» وسطر راتكليف','ar'),
 src('Report section 3, points 16 to 19 · refs [12][20] The Athletic, FotMob','«أنهى نيس ذلك الموسم رابعًا، وتأهل إلى دوري الأبطال.» ... «أنهى نيس موسم 2025–26 في المركز السادس عشر، واضطر إلى خوض ملحق البقاء أمام سانت إتيان.»','«في الجولة الأخيرة ... تعادل 0–0، وفشل في ضمان البقاء المباشر، ثم اقتحمت جماهير أرض الملعب بعد النهاية.»','راتكليف: «لقد كانوا أفضل بكثير دون تدخلنا! ربما هناك درس في ذلك أيضًا».'),
 ('Check this','The report itself says the quote proves INEOS said it, not that its absence caused the rise: coach, players and rivals also changed. The pitch invasion was by fans, so the slide only states that it happened. The quote is about the 2024-25 season, when INEOS stepped back for European rules.','')]))
D.append("Headline: نيس: من الرابع إلى السادس عشر\nColumn 1: ٢٠٢٤-٢٥: المركز الرابع (٤)\nColumn 2: ٢٠٢٥-٢٦: ملحق البقاء أمام سانت إتيان (١٦)\nDetail line 1: ٠-٠ أمام ميتز الهابط، ثم اقتحام جماهيري للملعب\nDetail line 2: راتكليف: «كانوا أفضل بكثير دون تدخلنا»")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Stadium in the upper four fifths.",
 "Editorial photograph of a Mediterranean football stadium by the coast at dusk, empty pitch under floodlights, palm trees beyond the stands, nobody present. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of a pitch invasion aftermath: scattered plain red and black scarves on the grass of an empty stadium at dusk, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of the Nice stadium (Allianz Riviera) from outside","Allianz Riviera","The slide names the club, so a real stadium photo works. Check the licence.")),True))
# ---------- 8 Lausanne
S.append(sec(8,T,'Photo on the right (48%), number block and text on the left',card(
 ph('right:0;top:0;bottom:0;width:48cqw','fr bf','Photo: Lausanne')
 +'<div class="tz" style="left:6cqw;width:44cqw;top:8cqw;bottom:14cqw"><div class="rs c-n" style="--d:.2s;font-size:19cqw;text-align:center">٦</div><div class="rs c-b" style="--d:.45s;font-size:4.4cqw;line-height:1.2;margin-top:1.2cqw;text-align:center">نقاط من ١١ مباراة</div><div class="rs c-h" style="--d:.7s;font-size:6cqw;margin-top:2.6cqw;text-align:center">لوزان في القاع</div><div class="rs c-b" style="--d:1s;margin-top:4cqw;text-align:center;font-size:3.6cqw"><span style="display:block">هبط في موسم الاستحواذ ٢٠١٧-١٨.</span><span style="display:block;margin-top:2cqw">وهبط مرة ثانية في ٢٠٢٢.</span></div><div class="rs c-b" style="--d:1.3s;margin-top:4cqw;text-align:center;font-size:3.4cqw;color:var(--red)">اليوم: الأخير بعد الخسارة أمام سيون في ٢٥ أكتوبر</div></div>'),[
 ('Big number','٦','ar h'),('Unit','نقاط من ١١ مباراة','ar'),
 ('Headline','لوزان في القاع','ar h'),
 ('Body (one sentence per line)','هبط في موسم الاستحواذ ٢٠١٧-١٨.<br>وهبط مرة ثانية في ٢٠٢٢.','ar'),
 ('Detail (red)','اليوم: الأخير بعد الخسارة أمام سيون في ٢٥ أكتوبر','ar'),
 ('Red mark','«٦» والسطر الأخير','ar'),
 src('Report section 4, points 24, 25 and 28 · refs [1][23][25][26] club site, FBref, Sofascore, YSScores','«اشترت إينيوس لوزان في نوفمبر 2017، وانتهى موسم 2017–18 بهبوطه إلى الدرجة الثانية.»','«بعد العودة إلى الدرجة الأولى، هبط لوزان مجددًا في موسم 2021–22.»','«وبعد خسارة سيون يوم 25 أكتوبر، بقي أخيرًا برصيد ست نقاط من 11 مباراة.»'),
 ('Check this','The report says Lausanne was 5th, not last, when INEOS bought it, so the slide does not say INEOS «relegated a leading side». The league positions come from score sites I could not open.','')]))
D.append("Big number: ٦\nUnit: نقاط من ١١ مباراة\nHeadline: لوزان في القاع\nBody: هبط في موسم الاستحواذ ٢٠١٧-١٨.\nوهبط مرة ثانية في ٢٠٢٢.\nDetail: اليوم: الأخير بعد الخسارة أمام سيون في ٢٥ أكتوبر")
IMG.append(noimg("2:3 portrait, generate at 1024x1536 or larger","Keep the left fifth open and bright. It fades into the white. Subject in the right four fifths.",
 "Editorial photograph of a small football stadium beside a large Alpine lake in grey light, empty terraces and an empty pitch, snow-capped mountains faintly behind, nobody present. Keep the left fifth as soft pale haze. Portrait 2:3. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of an empty league table board with blank white slots on a wall in a bright corridor, nobody present, no readable text. Keep the left fifth soft and bright. Portrait 2:3. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of the Lausanne stadium (Stade de la Pontaise) from outside","Stade de la Pontaise","The slide names the club, so a real stadium photo works. Check the licence.")),True))
# ---------- 9 closer
S.append(sec(9,T,'Photo on top (30%), headline, two lines, question and four icons below',card(
 ph('left:0;right:0;top:0;height:40cqw','ft','Photo: three crests')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:34cqw;height:78cqw"><div class="rs c-h" style="--d:.2s;font-size:5.6cqw;text-align:center">٣ أندية... ولاعبان فقط انتقلا بينها</div><div class="rs c-b" style="--d:.6s;margin-top:4cqw;text-align:center;font-size:3.6cqw">'+sent('منذ ٢٠٢٣: فريدريكسون وكوني، من يونايتد إلى لوزان.',1)+sent('ويونايتد اليوم ١٦ بعد الخسارة ٠-٣ أمام بورنموث.',1,'color:var(--red)')+'</div><div class="rs c-h" style="--d:1.2s;font-size:6cqw;margin-top:5cqw;text-align:center;color:var(--red)">إحكيلي</div><div class="rs c-b" style="--d:1.5s;font-size:4.7cqw;margin-top:2.6cqw;text-align:center;color:var(--red)">شو أكبر غلطة عملتها إينيوس؟</div></div>'
 +icons_svg,False),[
 ('Headline','٣ أندية... ولاعبان فقط انتقلا بينها','ar h'),
 ('Body (one sentence per line, second red)','منذ ٢٠٢٣: فريدريكسون وكوني، من يونايتد إلى لوزان.<br>ويونايتد اليوم ١٦ بعد الخسارة ٠-٣ أمام بورنموث.','ar'),
 ('Question line 1 (red)','إحكيلي','ar h'),
 ('Question line 2 (red, bigger)','شو أكبر غلطة عملتها إينيوس؟','ar'),
 ('Icons','Heart (red), comment (green), share (navy), save (navy), close together.',''),
 ('Red mark','سطر «ويونايتد اليوم ١٦...»، «إحكيلي» والسؤال','ar'),
 src('Report section 5, point 30 and section 1, point 6 · refs [12][13][14] The Athletic, BBC table, ESPN','«انتقل لاعبان فقط بين الأندية الثلاثة منذ 2023: تايلر فريدريكسون وسيكو كوني، من يونايتد إلى لوزان، أحدهما انتقالًا والآخر إعارة.»','«وبحلول 26 أكتوبر 2026، كان في المركز السادس عشر، بعد خسارة 0–3 أمام بورنموث في أولد ترافورد.»'),
 ('Check this','The United league position and the 0-3 result come from table and results pages that I could not open. Please check them before posting. Earlier in this chat, search results had United 13th after seven games around 18 October, so 16th a week later is possible but unconfirmed. Spelling to confirm: «فريدريكسون» (Fredricson), «كوني».','')]))
D.append("Headline: ٣ أندية... ولاعبان فقط انتقلا بينها\nBody: منذ ٢٠٢٣: فريدريكسون وكوني، من يونايتد إلى لوزان.\nويونايتد اليوم ١٦ بعد الخسارة ٠-٣ أمام بورنموث.\nQuestion line 1: إحكيلي\nQuestion line 2: شو أكبر غلطة عملتها إينيوس؟")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.",
 "Editorial photograph of three plain empty wooden chairs in a row on a bright stadium pitch, each facing a different empty stand, no people, no signage. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of three plain cardboard boxes in a row on a bright changing-room floor, one with an open flap, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("Three real club-crest or stadium photos for the band (United, Nice, Lausanne)","Old Trafford; Allianz Riviera; Stade de la Pontaise","Pick one wide shot per club and place them side by side.")),True))

th='padding:6px 8px;border-bottom:1px solid var(--line)'
def tr(*c): return '<tr>'+''.join(f'<td style="padding:6px 8px;vertical-align:top">{x}</td>' for x in c)+'</tr>'
sources=f'''<div style="margin:0 0 34px;padding:18px 20px;border:1px solid var(--line);border-radius:10px;background:#FBFCFE"><h2 style="margin:0 0 6px;font-size:20px">Source: check every claim yourself</h2><p style="margin:0 0 12px;color:var(--mute)">Everything comes from the research report you pasted, which is written as a critical file on INEOS at United, Nice and Lausanne, up to 26 October 2026. The report cites Reuters, BBC, The Athletic and others, but I could not open those pages from here, so I checked only what I could: the 116-day count is my own sum, and the Ten Hag dates match the Ten Hag article you shared earlier. Each slide's right-hand column quotes the report's own sentence and the source numbers it cites. The report itself warns that not every crisis is INEOS's doing, so the slides state facts and leave out the accusations.</p><div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;min-width:560px;font-size:14px"><tr style="text-align:left;color:var(--mute)"><th style="{th}">Slide</th><th style="{th}">Claim</th><th style="{th}">Report cites</th><th style="{th}">Flag</th></tr>
{tr(2,'Extended 4 Jul 2024, sacked 28 Oct, 14th, 116 days','Reuters','Day count is my sum; dates match the Ten Hag article')}
{tr(3,'£14.5m exceptional costs','Feb 2025 accounts, via RFI and Flashscore','Not Ten Hag alone; do not add to £10.4m')}
{tr(4,'Ashworth five months','Reuters','Who decided his exit is only reported')}
{tr(5,'Amorim £11m, sacked 5 Jan 2026, 15th, EL final','BBC, Reuters','£11m has no matching page in the report’s links')}
{tr(6,'250 jobs, 150-200 more, free lunches','BBC','150-200 were proposed, not done')}
{tr(7,'Nice 4th to 16th, Metz 0-0, Ratcliffe quote','The Athletic, FotMob','Quote does not prove cause')}
{tr(8,'Lausanne relegated 2018 and 2022, bottom now','Club site, FBref, score sites','Was 5th at takeover')}
{tr(9,'2 transfers; United 16th after 0-3','The Athletic, BBC table, ESPN','Table not opened; confirm')}
</table></div><p style="margin:12px 0 0;color:var(--mute);font-size:13px">Left out on purpose, to stay within 9 slides and the strongest facts: Ratcliffe’s immigration remarks and apology (a reputation issue, not a football one, and the FA took no action), ticket prices at £66, season-ticket moves for hospitality, the women’s team move and Ratcliffe’s comments, the Lausanne badge change, Lausanne’s 40 transfers in 18 months, Nice’s sale search through Lazard at about €250m, Ten Hag’s «broken promises» interview, and the multi-club ownership rules. The report’s own «do not use» list is respected: no «fired 18 coaches», no cut to the disabled supporters’ budget, no «INEOS relegated Nice», and no blaming INEOS for the fan attack.</p></div>'''
