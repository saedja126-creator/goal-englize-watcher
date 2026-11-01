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
S=[];D=[];IMG=[]
T=9
def add(n,title,head,body,label,rows_,dtext,img):
    S.append(sec(n,T,title,wcard(head,body,label),rows_)); D.append(dtext); IMG.append(img)
CH='Gemini original'
# 1 (wording kept exactly; only punctuation and colours)
add(1,'Full-bleed photo, yellow headline, white line below (wording unchanged)',
 Y('إنيوس:')+' وعود براقة وواقع '+Rd('مرير')+'!',
 'مشروع رياضي يعاني من '+Rd('عمى الألوان')+' منذ اليوم الأول',
 'Photo: Ratcliffe',
 [('Headline (yellow, red word)','إنيوس: وعود براقة وواقع مرير!','ar h'),
  ('Body (white, red phrase)','مشروع رياضي يعاني من عمى الألوان منذ اليوم الأول','ar'),
  (CH,'إنيوس · وعود براقة وواقع مرير! · مشروع رياضي يعاني من عمى الألوان منذ اليوم الأول','ar'),
  ('What I changed','Nothing in the words. I only added a colon after «إنيوس:» and coloured two spots (yellow «إنيوس:», red «مرير» and «عمى الألوان»). The spelling «إنيوس» is yours, and I use it on every slide.',''),
  ('Check this','This is a hook, not a fact. «عمى الألوان» is a figure of speech, so it is not backed by a source and the later slides carry the facts.','')],
 "Headline: إنيوس: وعود براقة وواقع مرير!\nBody: مشروع رياضي يعاني من عمى الألوان منذ اليوم الأول",
 noimg(SZ,COMP,
  "Editorial photograph of a lone older businessman in a dark overcoat seen from behind, standing at the edge of an empty football stadium pitch at dusk, floodlights glowing, stands curving above, no readable signage. The subject fills the top two thirds, the bottom third falls into deep shadow. Portrait 3:4. True-to-life colour, cinematic contrast, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
  "Editorial photograph of three empty football stadium stands side by side, one under snow-capped mountains, one by a sea coast, one under a grey English sky, as a triptych, nobody present. The images fill the top two thirds, the bottom third fades to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  wm(("A real, licensed photo of Sir Jim Ratcliffe","Jim Ratcliffe","The hook is about his group, so a real photo is better. Check the licence.")),True))
# 2
add(2,'Full-bleed photo, yellow headline, four-line body',
 'إمبراطورية البتروكيماويات!',
 'اشترت '+Y('لوزان')+' في ٢٠١٧، ثم '+Y('نيس')+' في ٢٠١٩، وفي ٢٠٢٤ تولّت إدارة كرة القدم في '+Y('مانشستر يونايتد')+'. ٣ أندية... '+Rd('فهل نجح النموذج؟'),
 'Photo: three clubs',
 [('Headline (yellow)','إمبراطورية البتروكيماويات!','ar h'),
  ('Body (names yellow, question red)','اشترت لوزان في ٢٠١٧، ثم نيس في ٢٠١٩، وفي ٢٠٢٤ تولّت إدارة كرة القدم في مانشستر يونايتد. ٣ أندية... فهل نجح النموذج؟','ar'),
  (CH,'حين تتحول إعادة الهيكلة الصناعية إلى عملية انتحارية بطيئة تدمر الأندية، حيث استحوذت إنيوس تدريجياً على لوزان، نيس، وأخيراً مانشستر يونايتد لفرض نموذجها الفاشل.','ar'),
  ('What I changed','Dropped «عملية انتحارية بطيئة تدمر الأندية» and «نموذجها الفاشل». The report does not say that, and it is the opinion the other slides have to prove. The years and the order are the report\'s. The ending is now a question.',''),
  src('Report intro and section 1 · refs [1][2][3][4]','«الفترة المشمولة: منذ استحواذ إينيوس على لوزان في 2017، ونيس في 2019، وتوليها إدارة كرة القدم في مانشستر يونايتد في فبراير 2024.» «حصتها فيه أقلية وليست ملكية كاملة.»'),
  ('Check this','«إمبراطورية البتروكيماويات» comes from your Gemini line. The Ten Hag article calls INEOS «their petrochemicals firm», so the word is right. At United INEOS has a minority stake and runs football operations, so the slide says «تولّت إدارة كرة القدم», not «اشترت».','')],
 "Headline: إمبراطورية البتروكيماويات!\nBody: اشترت لوزان في ٢٠١٧، ثم نيس في ٢٠١٩، وفي ٢٠٢٤ تولّت إدارة كرة القدم في مانشستر يونايتد. ٣ أندية... فهل نجح النموذج؟",
 noimg(SZ,COMP,
  "Editorial photograph of a huge industrial chemical plant at blue hour, towers, pipes and glowing lights reflected in still water, a tiny football pitch with floodlights visible in the far distance, no people, no readable signage. The plant fills the top two thirds, the bottom third falls to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  "Editorial photograph of three football club scarves hanging side by side on a metal fence in front of a grey industrial skyline, no readable text or crests, nobody present. Subject in the top two thirds, the bottom third fades to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  wm(("A real photo of an INEOS plant, or three stadium photos side by side (Old Trafford, Allianz Riviera, Pontaise)","INEOS Grangemouth; Old Trafford; Allianz Riviera; Stade de la Pontaise","Pick one wide shot. Check the licence.")),True))
# 3
add(3,'Full-bleed photo, yellow headline, three-line body',
 'حتى الشعار لم يسلم!',
 'بعد الاستحواذ بوقت قصير، عدّلت إنيوس '+Y('شعار لوزان')+' ليحاكي هويتها البصرية. '+Rd('غضب المشجعون')+'... فتراجعت عن التغيير.',
 'Photo: Lausanne badge',
 [('Headline (yellow)','حتى الشعار لم يسلم!','ar h'),
  ('Body (club yellow, fans red)','بعد الاستحواذ بوقت قصير، عدّلت إنيوس شعار لوزان ليحاكي هويتها البصرية. غضب المشجعون... فتراجعت عن التغيير.','ar'),
  (CH,'طمس الهوية · ثورة في لوزان بعد الاستحواذ بفترة قصيرة، حيث حاولت إنيوس فرض هويتها البصرية على شعار النادي العريق واضطرت للتراجع تحت ضغط المشجعين الغاضبين.','ar'),
  ('What I changed','Headline: «طمس الهوية» (erasing identity) is a conclusion, so the headline now states what happened. «ثورة» is dropped because the report says fans objected, not rebelled. The facts are unchanged.',''),
  src('Report section 4, point 23 · refs [12][21][22] The Athletic, 24 heures, RTS','«بعد الاستحواذ بفترة قصيرة، عُدّل شعار لوزان بحيث يحاكي حرف «o» في اسم النادي الهوية البصرية لإينيوس. أثار ذلك اعتراض الجماهير، قبل التراجع عن التغيير.»'),
  ('Check this','The report says the «o» in the club name was made to echo INEOS\'s look. «العريق» (historic) is dropped. It is not in the source.','')],
 "Headline: حتى الشعار لم يسلم!\nBody: بعد الاستحواذ بوقت قصير، عدّلت إنيوس شعار لوزان ليحاكي هويتها البصرية. غضب المشجعون... فتراجعت عن التغيير.",
 noimg(SZ,COMP,
  "Editorial photograph of a football club badge outline sketched in chalk on a plain concrete wall, half smudged by a hand-wipe, bright side light, nobody present, no readable marks. The wall fills the top two thirds, the bottom third falls to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  "Editorial photograph of an empty football stand with rows of seats in club colours under grey Alpine light, a large banner folded and left on the seats, no readable text, nobody present. Subject in the top two thirds, bottom third fades to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  wm(("A real photo of the Lausanne-Sport old and new badge, or the stadium","Lausanne-Sport badge; Stade de la Pontaise","A badge may be trademarked. A stadium photo is safer. Check the licence.")),True))
# 4
add(4,'Full-bleed photo, yellow headline, four-line body',
 'هبوط... ثم هبوط!',
 'هبط '+Y('لوزان')+' في موسم الاستحواذ ٢٠١٧-١٨، ثم '+Rd('مرة ثانية')+' في ٢٠٢٢. واليوم هو '+Y('الأخير')+' بـ٦ نقاط من ١١ مباراة، والمدرب إلسنر يصف الوضع بـ'+Rd('«حالة طوارئ»')+'.',
 'Photo: Lausanne',
 [('Headline (yellow)','هبوط... ثم هبوط!','ar h'),
  ('Body (club and «last» yellow, red phrases)','هبط لوزان في موسم الاستحواذ ٢٠١٧-١٨، ثم مرة ثانية في ٢٠٢٢. واليوم هو الأخير بـ٦ نقاط من ١١ مباراة، والمدرب إلسنر يصف الوضع بـ«حالة طوارئ».','ar'),
  (CH,'هبوط متكرر · حالة طوارئ مستمرة بعد أن تكرر كابوس الهبوط للدرجة الثانية خلال سنوات قصيرة، وصولاً لوصف المدرب لوكا إلسنر وضع الفريق بأنه كارثي.','ar'),
  ('What I changed','«كارثي» is replaced by the coach\'s real words, «حالة طوارئ». I added the two seasons and the 6-from-11 record, so the slide says exactly how many relegations and when.',''),
  src('Report section 4, points 24, 25 and 28 · refs [1][23][25][26][12]','«اشترت إينيوس لوزان في نوفمبر 2017، وانتهى موسم 2017–18 بهبوطه إلى الدرجة الثانية.» «هبط لوزان مجددًا في موسم 2021–22.» «وبعد خسارة سيون يوم 25 أكتوبر، بقي أخيرًا برصيد ست نقاط من 11 مباراة.»','«ووصف المدرب لوكا إلسنر وضع النادي بأنه «حالة طوارئ» مستمرة منذ أسابيع.»'),
  ('Check this','The report says Lausanne was 5th when INEOS bought it, so the slide does not say it «was relegated while leading». The league table comes from score sites I could not open. Spelling to confirm: «إلسنر».','')],
 "Headline: هبوط... ثم هبوط!\nBody: هبط لوزان في موسم الاستحواذ ٢٠١٧-١٨، ثم مرة ثانية في ٢٠٢٢. واليوم هو الأخير بـ٦ نقاط من ١١ مباراة، والمدرب إلسنر يصف الوضع بـ«حالة طوارئ».",
 noimg(SZ,COMP,
  "Editorial photograph of a small football stadium beside a large Alpine lake in grey light, empty terraces and an empty pitch, snow-capped mountains faintly behind, nobody present. The scene fills the top two thirds, the bottom third falls to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  "Editorial photograph of a footballer seen from behind sitting alone on a team bench with his head down, a towel over his shoulders, empty stadium lights glowing, no readable numbers. Subject in the top two thirds, bottom third fades to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no recognisable faces.",
  wm(("A real photo of Lausanne players after a defeat, or the stadium","Lausanne-Sport; Stade de la Pontaise","Check the licence.")),True))
# 5
add(5,'Full-bleed photo, yellow headline, four-line body',
 '«أفضل دون تدخلنا»!',
 'قال راتكليف عن نيس: '+Y('«كانوا أفضل بكثير دون تدخلنا»')+'. وأنهى نيس ٢٠٢٤-٢٥ '+Y('رابعًا')+'، وفي الموسم التالي بعد عودتهم أنهاه '+Rd('سادس عشر')+' وخاض '+Rd('ملحق البقاء')+'.',
 'Photo: Nice',
 [('Headline (yellow)','«أفضل دون تدخلنا»!','ar h'),
  ('Body (quote and 4th yellow, 16th and playoff red)','قال راتكليف عن نيس: «كانوا أفضل بكثير دون تدخلنا». وأنهى نيس ٢٠٢٤-٢٥ رابعًا، وفي الموسم التالي بعد عودتهم أنهاه سادس عشر وخاض ملحق البقاء.','ar'),
  (CH,'أزمات نيس · فريق بلا بوصلة بعد اعتراف راتكليف بأنهم عطلوا منظومة عمل نجحت في التأهل لدوري الأبطال، ليقودوا الفريق نحو المركز السادس عشر بعد عودتهم للإدارة.','ar'),
  ('What I changed','«بلا بوصلة» and «ليقودوا الفريق نحو المركز السادس عشر» say INEOS caused the fall. The report says the order of events does not prove that. The slide now gives Ratcliffe\'s exact quote and the two seasons, and lets readers connect them.',''),
  src('Report section 3, points 16 and 17 · ref [12] The Athletic','«اضطرت إينيوس إلى الابتعاد مؤقتًا عن إدارة نيس خلال موسم 2024–25 ... أنهى نيس ذلك الموسم رابعًا، وتأهل إلى دوري الأبطال.» «لقد كانوا أفضل بكثير دون تدخلنا! ربما هناك درس في ذلك أيضًا». «عادت إينيوس إلى زمام الأمور في 2025، ثم أنهى نيس موسم 2025–26 في المركز السادس عشر، واضطر إلى خوض ملحق البقاء أمام سانت إتيان.»'),
  ('Check this','The quote is word for word. «بعد عودتهم» is the report\'s «عادت إينيوس إلى زمام الأمور». The report itself says there were other factors (coach, players, rivals).','')],
 "Headline: «أفضل دون تدخلنا»!\nBody: قال راتكليف عن نيس: «كانوا أفضل بكثير دون تدخلنا». وأنهى نيس ٢٠٢٤-٢٥ رابعًا، وفي الموسم التالي بعد عودتهم أنهاه سادس عشر وخاض ملحق البقاء.",
 noimg(SZ,COMP,
  "Editorial photograph of a Mediterranean football stadium by the coast at dusk, empty pitch under floodlights, palm trees beyond the stands, nobody present. The stadium fills the top two thirds, the bottom third falls to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  "Editorial photograph of a lone older man in a dark coat watching a football match from an empty VIP box balcony at night, seen from behind, no readable signage. Subject in the top two thirds, bottom third fades to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no recognisable faces.",
  wm(("A real, licensed photo of Jim Ratcliffe, or the Allianz Riviera stadium in Nice","Jim Ratcliffe; Allianz Riviera","The quote is his, so a real photo of him works well. Check the licence.")),True))
# 6
add(6,'Full-bleed photo, yellow headline, four-line body',
 '١١٦ يومًا فقط!',
 'مدّدت يونايتد عقد '+Y('تين هاغ')+' في يوليو ٢٠٢٤، ثم أقالته في أكتوبر وهو في '+Rd('المركز ١٤')+'. وكلّف التغيير '+Y('١٤٫٥ مليون جنيه')+' بين تكاليف رحيله ورحيل أفراد من الطاقم الرياضي.',
 'Photo: Ten Hag',
 [('Headline (yellow)','١١٦ يومًا فقط!','ar h'),
  ('Body (name and amount yellow, 14th red)','مدّدت يونايتد عقد تين هاغ في يوليو ٢٠٢٤، ثم أقالته في أكتوبر وهو في المركز ١٤. وكلّف التغيير ١٤٫٥ مليون جنيه بين تكاليف رحيله ورحيل أفراد من الطاقم الرياضي.','ar'),
  (CH,'قرارات عبثية · مددوا عقد تين هاغ في صيف 2024 ثم أقالوه بعد 116 يوماً فقط، ليتحمل نادي مانشستر يونايتد ملايين الاستغناء فوق كاهله بسبب التخبط.','ar'),
  ('What I changed','«عبثية» and «بسبب التخبط» are opinion, so they are out. The number 116 is now the hook. I give the real cost: £14.5m, with the report\'s warning that it covers Ten Hag and other sports staff, so the slide does not call it «Ten Hag\'s compensation».',''),
  src('Report section 1, points 1 and 2 · refs [5][6][7][8] Reuters, RFI, Flashscore','«في 4 يوليو 2024، أعلن يونايتد تمديد عقد إريك تين هاغ ... وفي 28 أكتوبر من العام نفسه، أقالته الإدارة والفريق في المركز الرابع عشر.» «تكاليف استثنائية قدرها 14.5 مليون جنيه مرتبطة برحيل تين هاغ وأعضاء آخرين من الطاقم الرياضي.»'),
  ('Check this','116 is my own count of 4 July to 28 October (27 + 31 + 30 + 28). The Ten Hag article you shared earlier also gives 14th place and 28 October. The £14.5m is a figure from the club\'s accounts as reported by two second-hand sites.','')],
 "Headline: ١١٦ يومًا فقط!\nBody: مدّدت يونايتد عقد تين هاغ في يوليو ٢٠٢٤، ثم أقالته في أكتوبر وهو في المركز ١٤. وكلّف التغيير ١٤٫٥ مليون جنيه بين تكاليف رحيله ورحيل أفراد من الطاقم الرياضي.",
 noimg(SZ,COMP,
  "Editorial photograph of a torn-off calendar page lying on a wooden desk beside a signed contract folder, dramatic side light, no readable dates or text, nobody present. The desk fills the top two thirds, the bottom third falls to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  "Editorial photograph of an empty football manager's office chair behind a desk with a closed laptop, deep shadows, nobody present. Subject in the top two thirds, bottom third fades to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  wm(("A real, licensed photo of Erik ten Hag (you already have Ten Hag photos in your Drive folder)","Erik ten Hag","Pick a serious expression.")),True))
# 7
add(7,'Full-bleed photo, yellow headline, four-line body',
 '٥ أشهر فقط!',
 'عيّنت يونايتد '+Y('دان أشوورث')+' مديرًا رياضيًا في يوليو ٢٠٢٤، وأعلنت رحيله بالتراضي في ٨ ديسمبر. ثم أقالت '+Y('أموريم')+' بعد '+Rd('١٤ شهرًا')+' فقط.',
 'Photo: Ashworth',
 [('Headline (yellow)','٥ أشهر فقط!','ar h'),
  ('Body (names yellow, 14 months red)','عيّنت يونايتد دان أشوورث مديرًا رياضيًا في يوليو ٢٠٢٤، وأعلنت رحيله بالتراضي في ٨ ديسمبر. ثم أقالت أموريم بعد ١٤ شهرًا فقط.','ar'),
  (CH,'صفقات فاشلة · رحيل دان أشوورث بعد 5 أشهر فقط من تعيينه كمدير رياضي، ليثبت أن التخطيط طويل الأمد والتبريرات الاستراتيجية كانت حبراً على ورق.','ar'),
  ('What I changed','«صفقات فاشلة» is wrong: Ashworth\'s exit is not a signing. «حبراً على ورق» is opinion. I added Amorim\'s 14 months, a second short-term decision from the same report, so «long-term planning» is shown by dates, not by adjectives.',''),
  src('Report section 1, points 3 and 4 · refs [9][10] Reuters','«بدأ دان أشوورث عمله مديرًا رياضيًا في يوليو 2024 ... وفي 8 ديسمبر، أعلن النادي رحيله بالتراضي، بعد خمسة أشهر فقط.» «أقاله في 5 يناير 2026 بعد نحو 14 شهرًا.»'),
  ('Check this','The report says who decided Ashworth\'s exit is only reported, so the slide does not say. Spelling to confirm: «أشوورث», «أموريم».','')],
 "Headline: ٥ أشهر فقط!\nBody: عيّنت يونايتد دان أشوورث مديرًا رياضيًا في يوليو ٢٠٢٤، وأعلنت رحيله بالتراضي في ٨ ديسمبر. ثم أقالت أموريم بعد ١٤ شهرًا فقط.",
 noimg(SZ,COMP,
  "Editorial photograph of an empty executive desk chair in a modern glass-walled office, a single name-plate frame face down on the desk, dramatic side light, nobody present. The room fills the top two thirds, the bottom third falls to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  "Editorial photograph of a lone manager in a dark coat seen from behind walking down a stadium tunnel toward bright daylight, long shadow. Subject in the top two thirds, bottom third fades to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no recognisable faces.",
  wm(("Real, licensed photos of Dan Ashworth and Ruben Amorim","Dan Ashworth; Ruben Amorim","Split the photo in two if you want both. Check the licence.")),True))
# 8
add(8,'Full-bleed photo, yellow headline, five-line body',
 'الغداء المجاني... انتهى!',
 'ألغى يونايتد '+Y('الغداء المجاني')+' لموظفي أولد ترافورد (توفير يفوق مليون جنيه سنويًا)، بعد الاستغناء عن نحو '+Rd('٢٥٠ موظفًا')+'. ورفع بعض التذاكر إلى '+Y('٦٦ جنيهًا')+' بلا خصم للأطفال والمتقاعدين.',
 'Photo: Old Trafford',
 [('Headline (yellow)','الغداء المجاني... انتهى!','ar h'),
  ('Body (lunch and £66 yellow, 250 staff red)','ألغى يونايتد الغداء المجاني لموظفي أولد ترافورد (توفير يفوق مليون جنيه سنويًا)، بعد الاستغناء عن نحو ٢٥٠ موظفًا. ورفع بعض التذاكر إلى ٦٦ جنيهًا بلا خصم للأطفال والمتقاعدين.','ar'),
  (CH,'تقشف مقزز · إلغاء وجبات الغداء المجانية لعمال أولد ترافورد ورفع أسعار التذاكر على المخلصين، في وقت تسببت قرارات الإدارة العشوائية بنزيف مالي غير مسبوق.','ar'),
  ('What I changed','«مقزز», «العشوائية» and «نزيف مالي غير مسبوق» are out. The report says the club\'s losses ran for five years before INEOS, so «غير مسبوق» is not supported. The three real facts stay: lunches, jobs, the £66 ticket.',''),
  src('Report section 2, points 7 to 9 · ref [3] BBC','«أعلن النادي وقف تقديم وجبات الغداء المجانية لموظفي أولد ترافورد، بتوفير متوقع يزيد على مليون جنيه سنويًا.» «شهد عام 2024 الاستغناء عن نحو 250 موظفًا.» «رفعت الإدارة أسعار تذاكر المباريات المشمولة بالتغيير إلى 66 جنيهًا، دون أسعار مخفضة للأطفال أو المتقاعدين.»'),
  ('Check this','The report warns not to say every ticket or season ticket is now £66. The slide says «بعض التذاكر». «الاستغناء» happened in 2024 and the lunch decision in February 2025, so the order in the sentence is right.','')],
 "Headline: الغداء المجاني... انتهى!\nBody: ألغى يونايتد الغداء المجاني لموظفي أولد ترافورد (توفير يفوق مليون جنيه سنويًا)، بعد الاستغناء عن نحو ٢٥٠ موظفًا. ورفع بعض التذاكر إلى ٦٦ جنيهًا بلا خصم للأطفال والمتقاعدين.",
 noimg(SZ,COMP,
  "Editorial photograph of an empty staff canteen with clean tables and chairs, a closed serving counter and a single plain tray left on a table, cold daylight, nobody present. The room fills the top two thirds, the bottom third falls to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  "Editorial photograph of the exterior of a large English football stadium on a grey afternoon, a long queue of tiny distant people at the turnstiles, no readable signage. Subject in the top two thirds, bottom third fades to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no recognisable faces.",
  wm(("A real photo of Old Trafford from outside in daylight","Old Trafford stadium","The slide is about the club, so a real stadium photo works. Check the licence.")),True))
# 9
add(9,'Full-bleed photo, yellow headline, four-line body',
 'إحكيلي: مين المسؤول؟',
 Y('٣ أندية')+'، ولاعبان فقط انتقلا بينها منذ ٢٠٢٣. هل المشكلة في '+Y('النموذج متعدد الأندية')+'، ولا في '+Rd('القرارات')+'؟ شاركنا رأيك بالتعليقات!',
 'Photo: three clubs',
 [('Headline (yellow)','إحكيلي: مين المسؤول؟','ar h'),
  ('Body (3 clubs and model yellow, decisions red)','٣ أندية، ولاعبان فقط انتقلا بينها منذ ٢٠٢٣. هل المشكلة في النموذج متعدد الأندية، ولا في القرارات؟ شاركنا رأيك بالتعليقات!','ar'),
  (CH,'ضياع شامل · من المسؤول عن هذا الفشل؟ هل تشوف إن نموذج إينيوس متعدد الأندية مدمر بطبعه، ولا الإدارة هي اللي مش فاهمة كرة القدم؟ شاركنا رأيك بالتعليقات!','ar'),
  ('What I changed','Both options in Gemini\'s question were loaded: «مدمر بطبعه» and «مش فاهمة كرة القدم». The report says neither can be proven from these facts, and says the critique does not need to say INEOS «does not understand football». So the question now offers the model or the decisions, backed by a fact: only 2 players moved.',''),
  src('Report section 5, points 29 and 30 · ref [12] The Athletic','«انتقل لاعبان فقط بين الأندية الثلاثة منذ 2023: تايلر فريدريكسون وسيكو كوني، من يونايتد إلى لوزان.»'),
  ('Check this','The dialect line «إحكيلي: مين المسؤول؟» matches your brand voice. The closing question stays open, so people answer in the comments.','')],
 "Headline: إحكيلي: مين المسؤول؟\nBody: ٣ أندية، ولاعبان فقط انتقلا بينها منذ ٢٠٢٣. هل المشكلة في النموذج متعدد الأندية، ولا في القرارات؟ شاركنا رأيك بالتعليقات!",
 noimg(SZ,COMP,
  "Editorial photograph of three plain empty wooden chairs in a row on a stadium pitch at dusk, each facing a different empty stand, no people, no signage. The scene fills the top two thirds, the bottom third falls to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  "Editorial photograph of three plain cardboard boxes in a row on a dark changing-room floor under a single hard light, one with an open flap, nobody present. Subject in the top two thirds, bottom third fades to black. Portrait 3:4. Cinematic contrast, editorial style. No text, no logos, no watermarks, no people.",
  wm(("Three real stadium photos for a collage (Old Trafford, Allianz Riviera, Stade de la Pontaise)","Old Trafford; Allianz Riviera; Stade de la Pontaise","Pick one wide shot per club and stack them. Check the licence.")),True))

th='padding:6px 8px;border-bottom:1px solid var(--line)'
def tr(*c): return '<tr>'+''.join(f'<td style="padding:6px 8px;vertical-align:top">{x}</td>' for x in c)+'</tr>'
sources=f'''<div style="margin:0 0 34px;padding:18px 20px;border:1px solid var(--line);border-radius:10px;background:#FBFCFE"><h2 style="margin:0 0 6px;font-size:20px">Source: Gemini's copy checked against the report</h2><p style="margin:0 0 12px;color:var(--mute)">Design: your winning carousel (full-bleed photo, yellow headline, white text, yellow and red highlights). The 2/7 counter and the little arrow in your screenshots are Instagram's own buttons, so they are not on the slides. Copy: Gemini's breakdown, shortened and checked against the research report you pasted. Slide 1 keeps Gemini's wording exactly. On slides 2 to 9, each line that went beyond the report is replaced by the report's own fact, and each slide's right-hand column shows Gemini's original next to what I changed and why. I could not open the pages the report cites, so I checked only what I could: the 116-day count is my own sum, and the Ten Hag dates match the Ten Hag article you shared earlier. The spelling «إنيوس» is yours, used on every slide.</p><div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;min-width:560px;font-size:14px"><tr style="text-align:left;color:var(--mute)"><th style="{th}">Slide</th><th style="{th}">Removed from Gemini</th><th style="{th}">Replaced by</th></tr>
{tr(2,'«عملية انتحارية بطيئة»، «نموذجها الفاشل»','The years and the order in the report, then a question')}
{tr(3,'«طمس الهوية»، «ثورة»، «العريق»','What happened to the badge, and the fans’ objection')}
{tr(4,'«كارثي»','The coach’s real words, «حالة طوارئ», and the 2 relegations')}
{tr(5,'«بلا بوصلة»، «ليقودوا الفريق نحو...»','Ratcliffe’s exact quote, and the two seasons')}
{tr(6,'«عبثية»، «بسبب التخبط»','116 days, and the £14.5m with its caveat')}
{tr(7,'«صفقات فاشلة»، «حبراً على ورق»','Ashworth 5 months, and Amorim 14 months')}
{tr(8,'«مقزز»، «العشوائية»، «نزيف مالي غير مسبوق»','Lunches, 250 jobs, the £66 ticket')}
{tr(9,'«مدمر بطبعه»، «مش فاهمة كرة القدم»','A fact (2 transfers) and an open question')}
</table></div></div>'''
