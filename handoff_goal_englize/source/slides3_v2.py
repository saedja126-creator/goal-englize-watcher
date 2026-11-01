RED={1:'«النزيف»',2:'«٦»',3:'«٤٧» (والرقم الكبير)',4:'«١» و «١»',5:'«٢١» (والرقم الكبير)',6:'«١٧»',7:'«١٠» لا: أرقام الاحتمالات (٤١٫٧٪ و٣٣٫٨٪) و «إحكيلي»'}
RED[7]='أرقام الاحتمالات الثلاثة، و «إحكيلي»'
def src(*lines):
    return ('From the article',''.join(f'<span style="display:block;margin-bottom:6px">{l}</span>' for l in lines),'')
S=[];D=[];IMG=[]
T=7
def noimg(size,comp,A,B,grab=None,fallback=False):
    return {"size":size,"comp":comp,"grab":grab,"fallback":fallback,"A":A,"B":B}
def wm(what): return {"what":what[0],"search":what[1],"where":"Wikimedia Commons (commons.wikimedia.org). Filter the licence to CC BY, CC BY-SA or CC0 and note the credit.","note":what[2]}
# 1 cover
S.append(sec(1,T,'Centered text on top, photo in the lower 63%, forward arrow',card(
 '<div class="tz" style="right:7cqw;left:7cqw;top:6cqw;height:50cqw;text-align:center"><div class="rs c-h" style="--d:.2s;font-size:7.8cqw;text-align:center">كومو ضد يونايتد:<br>هل ينتهي <span class="hl">النزيف</span>؟</div><div class="rs c-b" id="sub1" style="--d:.5s;font-size:3.9cqw;margin-top:3cqw;text-align:center;white-space:nowrap">الأربعاء في دوري الأبطال... وكاريك تحت الضغط</div><div class="rs c-b" style="--d:.8s;margin-top:6.5cqw;text-align:center">٦ مباريات بلا فوز في كل البطولات</div><div class="rs c-b" style="--d:1s;margin-top:1.5cqw;text-align:center">فهل يكسرها أمام فريق فابريغاس؟</div></div>'
 +ph('left:0;right:0;bottom:0;height:84cqw','fb bf','Photo: Carrick'),True),[
 ('Headline (centered, two lines)','كومو ضد يونايتد: هل ينتهي النزيف؟','ar h'),
 ('Second line (one full line)','الأربعاء في دوري الأبطال... وكاريك تحت الضغط','ar'),
 ('Body 1','٦ مباريات بلا فوز في كل البطولات','ar'),
 ('Body 2','فهل يكسرها أمام فريق فابريغاس؟','ar'),
 ('Red mark','«النزيف»','ar'),
 src('«Manchester United will look to ease the pressure on Michael Carrick and put their recent struggles behind them when they resume their Champions League campaign against Como.»','«Carrick has now overseen a six-match winless run in all competitions (D3 L3).»','Article date: 20 Oct 2026, «Wednesday\'s Champions League clash at Stadio Giuseppe Sinigaglia».'),
 ('My wording','«النزيف» is my word for the winless run. «تحت الضغط» is the article\'s «ease the pressure on Michael Carrick». Spelling to confirm: «كومو», «فابريغاس».','')]))
D.append("Headline: كومو ضد يونايتد: هل ينتهي النزيف؟\nSecond line: الأربعاء في دوري الأبطال... وكاريك تحت الضغط\nBody 1: ٦ مباريات بلا فوز في كل البطولات\nBody 2: فهل يكسرها أمام فريق فابريغاس؟")
IMG.append(noimg("1:1 square, generate at 1024x1024 or larger","Keep the top fifth open and bright. It fades into the white. Subject sits in the lower two thirds.",
 "Editorial photograph of a lone football manager seen from behind in a dark overcoat, standing at the edge of a floodlit pitch at dusk, a small stadium and a mountain lake blurred beyond, wet grass catching the light. Keep the top fifth as soft pale sky. Square 1:1. True-to-life colour, bright high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "Editorial photograph of an empty technical area on a football touchline, a padded coaching bench and a folded tactics board under bright stadium lights, nobody present. Keep the top fifth soft and bright. Square 1:1. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Michael Carrick on the touchline","Michael Carrick","The slide is about him, so a real photo is better than an AI one.")),True))
# 2 winless run
S.append(sec(2,T,'Photo on top (50%), number, headline and text below',card(
 ph('left:0;right:0;top:0;height:66cqw','ft','Photo: six empty shirts')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:60cqw;height:65cqw"><div class="rs" style="--d:.2s;display:flex;justify-content:center;align-items:baseline;gap:3cqw"><span class="c-n" style="font-size:15cqw">٦</span><span class="c-b" style="font-size:5cqw">مباريات بلا فوز</span></div><div class="rs c-h" style="--d:.6s;font-size:6.4cqw;margin-top:3cqw;text-align:center">٣ تعادلات و٣ هزائم</div><div class="rs c-b" style="--d:1s;margin-top:3.5cqw;text-align:center;font-size:3.4cqw"><span style="display:block;white-space:nowrap">آخرها ١-١ أمام ليدز: مبيومو سجّل وكالفرت-لوين عادل.</span><span style="display:block;white-space:nowrap;margin-top:1cqw">وقبلها خسر ٠-٢ أمام أتلتيكو مدريد.</span></div><div class="rs c-b" style="--d:1.3s;margin-top:3cqw;text-align:center;font-size:3.4cqw;color:var(--green)">في كل البطولات تحت قيادة كاريك</div></div>'),[
 ('Big number','٦','ar h'),('Unit','مباريات بلا فوز','ar'),
 ('Headline','٣ تعادلات و٣ هزائم','ar h'),
 ('Body (one sentence per line)','آخرها ١-١ أمام ليدز: مبيومو سجّل وكالفرت-لوين عادل.<br>وقبلها خسر ٠-٢ أمام أتلتيكو مدريد.','ar'),
 ('Detail (green)','في كل البطولات تحت قيادة كاريك','ar'),
 ('Red mark','«٦» (الرقم الكبير)','ar'),
 src('«Carrick has now overseen a six-match winless run in all competitions (D3 L3).»','«Following Sunday\'s 1-1 draw with cross-Pennine rivals Leeds United, in which Dominic Calvert-Lewin cancelled out Bryan Mbeumo\'s first-half effort»','«beaten 2-0 by Atlético Madrid in Spain last week.»'),
 ('My wording','«تحت قيادة كاريك» is my Arabic for «overseen». The article does not say when the run began. Spelling to confirm: «كالفرت-لوين», «مبيومو».','')]))
D.append("Big number: ٦\nUnit: مباريات بلا فوز\nHeadline: ٣ تعادلات و٣ هزائم\nBody: آخرها ١-١ أمام ليدز: مبيومو سجّل وكالفرت-لوين عادل. وقبلها خسر ٠-٢ أمام أتلتيكو مدريد.\nDetail: في كل البطولات تحت قيادة كاريك")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Shirts in the upper four fifths.",
 "Editorial photograph of a football dressing room bench with six plain red shirts folded in a row, a bright window behind, nobody present. Keep the bottom fifth as soft pale floor. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no crests, no watermarks, no people.",
 "Editorial photograph of a wet football pitch under grey skies, a single ball on the centre spot, empty stands beyond, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."))
# 3 47 seconds
S.append(sec(3,T,'Photo on the left (56%), number block and text on the right',card(
 ph('left:0;top:0;bottom:0;width:56cqw','fl bf','Photo: Atletico match')
 +'<div class="tz" style="right:6cqw;width:38cqw;top:8cqw;bottom:14cqw"><div class="rs c-n" style="--d:.2s;font-size:19cqw;text-align:center">٤٧</div><div class="rs c-b" style="--d:.45s;font-size:5cqw;line-height:1.2;margin-top:1.2cqw;text-align:center">ثانية</div><div class="rs c-h" style="--d:.7s;font-size:6cqw;margin-top:6cqw;text-align:center">هدف أتلتيكو الأول</div><div class="rs c-b" style="--d:1s;margin-top:5cqw;text-align:center;font-size:3.8cqw">رابع هدف يستقبله يونايتد في الدقيقة الأولى بدوري الأبطال. ثم طُرد يورو في الدقيقة ٧٤، فيغيب عن كومو.</div><div class="rs c-b" style="--d:1.3s;margin-top:4cqw;text-align:center;font-size:3.5cqw;color:var(--green)">٤ فرص كبيرة... ولا هدف</div></div>'),[
 ('Big number','٤٧','ar h'),('Unit','ثانية','ar'),
 ('Headline','هدف أتلتيكو الأول','ar h'),
 ('Body','رابع هدف يستقبله يونايتد في الدقيقة الأولى بدوري الأبطال. ثم طُرد يورو في الدقيقة ٧٤، فيغيب عن كومو.','ar'),
 ('Detail (green)','٤ فرص كبيرة... ولا هدف','ar'),
 ('Red mark','«٤٧» (الرقم الكبير)','ar'),
 src('«Pablo Barrios struck after just 47 seconds as United conceded in the opening minute of a Champions League game for only the fourth time»','«Leny Yoro was sent off for a professional foul in the 74th minute – meaning he will miss Wednesday\'s trip to Italy»','«They created four big chances without scoring any, their most without scoring in a Champions League game since September 2012 against Galatasaray (also 0/4).»'),
 ('My wording','«في الدقيقة الأولى» is the article\'s «in the opening minute». The other three times are in the article too (Juventus 1997, Barcelona 1998, Basel 2002) if you want them on the slide. Spelling to confirm: «يورو» (Yoro), «باريوس».','')]))
D.append("Big number: ٤٧\nUnit: ثانية\nHeadline: هدف أتلتيكو الأول\nBody: رابع هدف يستقبله يونايتد في الدقيقة الأولى بدوري الأبطال. ثم طُرد يورو في الدقيقة ٧٤، فيغيب عن كومو.\nDetail: ٤ فرص كبيرة... ولا هدف")
IMG.append(noimg("2:3 portrait, generate at 1024x1536 or larger","Keep the right fifth open and bright. It fades into the white. Subject in the left four fifths.",
 "Editorial photograph of a goal net seen from behind the goal in a floodlit stadium at night, a single ball resting in the net, empty seats curving above, nobody present. Keep the right fifth as soft pale haze. Portrait 2:3. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of a stopwatch with a blurred dial lying on a white pitch line, shallow depth of field, floodlights glowing beyond, no readable digits, no people. Keep the right fifth soft and bright. Portrait 2:3. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo from the Atlético Madrid v Manchester United match or of Leny Yoro","Leny Yoro; Atlético Madrid Manchester United","The slide names Yoro and the game, so a real photo works better. Check the licence.")),True))
# 4 away record
def col(label,num,sub,d): return f'<div class="rs" style="--d:{d}s;flex:1;text-align:center"><div class="c-b" style="font-size:3.8cqw;line-height:1.3">{label}</div><div class="c-n" style="font-size:15cqw;margin-top:1cqw">{num}</div><div class="c-b" style="font-size:3.6cqw;line-height:1.3;margin-top:1cqw">{sub}</div></div>'
S.append(sec(4,T,'Photo on top (44%), headline and two stat columns below',card(
 ph('left:0;right:0;top:0;height:58cqw','ft','Photo: empty away end')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:54cqw;height:71cqw"><div class="rs c-h" style="--d:.2s;font-size:6cqw;text-align:center">خارج الديار... الأرقام ضد يونايتد</div><div style="display:flex;gap:3cqw;align-items:stretch;margin-top:4cqw">'
 +col('الفوز خارج الديار','١','من آخر ١٠ مباريات',.6)+'<div style="width:.5cqw;background:var(--line)"></div>'+col('الشباك النظيفة','١','من آخر ١٥ مباراة',.8)
 +'</div><div class="rs c-b" style="--d:1.2s;margin-top:4.5cqw;text-align:center;font-size:3.5cqw;color:var(--green)">في دوري الأبطال: خسر ٢١٪ من مبارياته تحت فيرغسون، و٣٨٪ بعده</div></div>'),[
 ('Headline','خارج الديار... الأرقام ضد يونايتد','ar h'),
 ('Column 1','الفوز خارج الديار: ١ من آخر ١٠ مباريات','ar'),
 ('Column 2','الشباك النظيفة: ١ من آخر ١٥ مباراة','ar'),
 ('Detail (green)','في دوري الأبطال: خسر ٢١٪ من مبارياته تحت فيرغسون، و٣٨٪ بعده','ar'),
 ('Red mark','الرقمان الكبيران «١» و «١»','ar'),
 src('«Manchester United have just one win from their last 10 Champions League away matches (D3 L6), and have only kept one clean sheet in their last 15 on the road.»','«Man Utd only lost 21% of their 190 matches in the competition under Alex Ferguson (W102 D49 L39). Since his retirement, though, they have been beaten in 38% of their 56 games (W24 D11 L21).»'),
 ('Check this','The article contradicts itself: the key stats say 10 away games (W1 D3 L6), but a later line says «a sixth defeat in 10 Champions League outings away from Old Trafford (W1 D2)», which adds up to 9. The slide uses the key-stats line (1 win from 10). Spelling to confirm: «فيرغسون».','')]))
D.append("Headline: خارج الديار... الأرقام ضد يونايتد\nColumn 1: الفوز خارج الديار: ١ من آخر ١٠ مباريات\nColumn 2: الشباك النظيفة: ١ من آخر ١٥ مباراة\nDetail: في دوري الأبطال: خسر ٢١٪ من مبارياته تحت فيرغسون، و٣٨٪ بعده")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Seats in the upper four fifths.",
 "Editorial photograph of an empty visitors' section in a football stadium, rows of plain red plastic seats behind a fence, bright overcast daylight, nobody present, no signage. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of a plain white team coach parked outside a floodlit stadium at dusk, no signage, nobody visible. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people."))
# 5 Como / Diao
S.append(sec(5,T,'Photo on the right (48%), number block and text on the left',card(
 ph('right:0;top:0;bottom:0;width:48cqw','fr bf','Photo: Diao')
 +'<div class="tz" style="left:6cqw;width:44cqw;top:8cqw;bottom:14cqw"><div class="rs c-n" style="--d:.2s;font-size:19cqw;text-align:center">٢١</div><div class="rs c-b" style="--d:.45s;font-size:5cqw;line-height:1.2;margin-top:1.2cqw;text-align:center">سنة</div><div class="rs c-h" style="--d:.7s;font-size:6cqw;margin-top:6cqw;text-align:center">ديو... سلاح كومو</div><div class="rs c-b" style="--d:1s;margin-top:5cqw;text-align:center;font-size:3.7cqw">سجّل في أول مباراتين له بدوري الأبطال، وهو أصغر لاعب أفريقي يفعلها.</div><div class="rs c-b" style="--d:1.3s;margin-top:4cqw;text-align:center;font-size:3.4cqw;color:var(--green)">وكومو بلا لاعب إيطالي في تشكيلته الأساسية</div></div>'),[
 ('Big number','٢١','ar h'),('Unit','سنة','ar'),
 ('Headline','ديو... سلاح كومو','ar h'),
 ('Body','سجّل في أول مباراتين له بدوري الأبطال، وهو أصغر لاعب أفريقي يفعلها.','ar'),
 ('Detail (green)','وكومو بلا لاعب إيطالي في تشكيلته الأساسية','ar'),
 ('Red mark','«٢١» (الرقم الكبير)','ar'),
 src('«After scoring in the 4-1 win over RB Leipzig and last week\'s 3-2 defeat at Feyenoord, the Senegal international became only the third player to find the net in an Italian club\'s opening two Champions League matches»','«At 21 years and 37 days old, Diao also became the youngest African player to find the target in both his first two appearances in the competition.»','«only the second team not to name a single player from their own nation in the starting XI for either of their first two matches in the competition, after Sheriff Tiraspol in 2021-22.»'),
 ('Check this','The green line is about Como\'s first two matches (no Italian in the starting XI). It does not say they will start without one on Wednesday. The predicted XI in the article has no Italian name, but it is a prediction. Spelling to confirm: «ديو» (Diao) is my guess.','')]))
D.append("Big number: ٢١\nUnit: سنة\nHeadline: ديو... سلاح كومو\nBody: سجّل في أول مباراتين له بدوري الأبطال، وهو أصغر لاعب أفريقي يفعلها.\nDetail: وكومو بلا لاعب إيطالي في تشكيلته الأساسية")
IMG.append(noimg("2:3 portrait, generate at 1024x1536 or larger","Keep the left fifth open and bright. It fades into the white. Subject in the right four fifths.",
 "Editorial photograph of a small football stadium on a lake shore at dusk, steep green hills behind, floodlights switched on, empty stands, a single ball on the grass, nobody present. Keep the left fifth as soft pale sky. Portrait 2:3. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of a pair of football boots on a wooden bench in a bright changing room, a window showing mountains beyond, no people. Keep the left fifth soft and bright. Portrait 2:3. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Assane Diao in a Como shirt","Assane Diao Como","The slide names him. Check the licence; a recent Como photo may not be on Commons yet.")),True))
# 6 Rashford
S.append(sec(6,T,'Photo on top (45%), number, headline and text below',card(
 ph('left:0;right:0;top:0;height:64cqw','ft','Photo: Rashford')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:58cqw;height:67cqw"><div class="rs" style="--d:.2s;display:flex;justify-content:center;align-items:baseline;gap:3cqw"><span class="c-n" style="font-size:15cqw">١٧</span><span class="c-b" style="font-size:5cqw">هدفًا في دوري الأبطال</span></div><div class="rs c-h" style="--d:.6s;font-size:6.2cqw;margin-top:3cqw;text-align:center">راشفورد يقترب من المباراة ٥٠</div><div class="rs c-b" style="--d:1s;margin-top:3.5cqw;text-align:center;font-size:3.6cqw"><span style="display:block;white-space:nowrap">٣٤ مع يونايتد، و٤ مع فيلا، و١١ مع برشلونة.</span><span style="display:block;margin-top:1.2cqw">لا يتفوق عليه من الإنجليز في أول ٥٠ مباراة <span class="hl">إلا كين وستيرلينغ وكول.</span></span></div><div class="rs c-b" style="--d:1.3s;margin-top:3cqw;text-align:center;font-size:3.4cqw;color:var(--green)">في التشكيلة المتوقعة لكاريك</div></div>'),[
 ('Big number','١٧','ar h'),('Unit','هدفًا في دوري الأبطال','ar'),
 ('Headline','راشفورد يقترب من المباراة ٥٠','ar h'),
 ('Body (one sentence per line)','٣٤ مع يونايتد، و٤ مع فيلا، و١١ مع برشلونة.<br>لا يتفوق عليه من الإنجليز في أول ٥٠ مباراة <span style="color:#C8202B">إلا كين وستيرلينغ وكول.</span>','ar'),
 ('Detail (green)','في التشكيلة المتوقعة لكاريك','ar'),
 ('Red mark','«١٧» (الرقم الكبير) و «إلا كين وستيرلينغ وكول.»','ar'),
 src('«Carrick will be looking for inspiration in Lombardy from the likes of Marcus Rashford, who could make his 50th Champions League appearance (34 for Man Utd, four for Aston Villa, 11 for Barcelona).»','«Harry Kane (34), Raheem Sterling (20) and Andrew Cole (18) are the only English players to better Rashford\'s tally of 17 goals in their first 50 games in the competition.»','Predicted lineup lists «Marcus Rashford» in United\'s XI.'),
 ('Check this','The article says he «could» make his 50th appearance, and the lineup is a prediction, so the slide says «يقترب» (nears) and «المتوقعة» (predicted). The 17 goals are his tally across those games. The numbers 34, 20, 18 in the article are the goals of Kane, Sterling and Cole, so I left them off. Spelling to confirm: «ستيرلينغ», «كول».','')]))
D.append("Big number: ١٧\nUnit: هدفًا في دوري الأبطال\nHeadline: راشفورد يقترب من المباراة ٥٠\nBody: ٣٤ مع يونايتد، و٤ مع فيلا، و١١ مع برشلونة. لا يتفوق عليه من الإنجليز في أول ٥٠ مباراة إلا كين وستيرلينغ وكول.\nDetail: في التشكيلة المتوقعة لكاريك")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. Subject in the upper four fifths.",
 "Editorial photograph of a lone footballer seen from behind walking out of a stadium tunnel toward bright daylight, empty stands ahead, long shadow on the grass. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no recognisable faces.",
 "Editorial photograph of a row of football boots on a bench in a bright empty dressing room, no people. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real, licensed photo of Marcus Rashford in a Manchester United shirt","Marcus Rashford","The slide names him. Pick a Champions League photo if you can; check the licence.")),True))
# 7 closer
def pc(who,num,color,d): return f'<div class="rs" style="--d:{d}s;flex:1;text-align:center"><div class="c-b" style="font-size:3.6cqw;line-height:1.3">{who}</div><div class="c-n" style="font-size:9.5cqw;color:{color};margin-top:1cqw">{num}</div></div>'
S.append(sec(7,T,'Photo on top (30%), three probability columns, question and four icons below',card(
 ph('left:0;right:0;top:0;height:40cqw','ft','Photo: Stadio Sinigaglia')
 +'<div class="tz" style="right:7cqw;left:7cqw;top:34cqw;height:78cqw"><div class="rs c-h" style="--d:.2s;font-size:5.6cqw;text-align:center">توقعات Opta للمباراة</div><div class="rs" style="--d:.6s;display:flex;gap:2cqw;align-items:stretch;margin-top:3.5cqw">'
 +pc('كومو','٤١٫٧٪','var(--navy)',.6)+'<div style="width:.5cqw;background:var(--line)"></div>'+pc('تعادل','٢٤٫٥٪','var(--mute)',.8)+'<div style="width:.5cqw;background:var(--line)"></div>'+pc('يونايتد','٣٣٫٨٪','var(--red)',1)
 +'</div><div class="rs c-b" style="--d:1.2s;margin-top:3cqw;text-align:center;font-size:3.3cqw;color:var(--green)">يونايتد لم يخسر في آخر ٦ مباريات خارج الديار أمام فرق إيطالية</div><div class="rs c-h" style="--d:1.4s;font-size:6cqw;margin-top:3cqw;text-align:center;color:var(--red)">إحكيلي</div><div class="rs c-b" style="--d:1.6s;font-size:4.7cqw;margin-top:2.6cqw;text-align:center;color:var(--red)">يونايتد بيكسر السلسلة ولا كومو بيكمّلها؟</div></div>'
 +icons_svg,False),[
 ('Headline','توقعات Opta للمباراة','ar h'),
 ('Column 1','كومو ٤١٫٧٪','ar'),('Column 2','تعادل ٢٤٫٥٪','ar'),('Column 3 (red)','يونايتد ٣٣٫٨٪','ar'),
 ('Detail (green)','يونايتد لم يخسر في آخر ٦ مباريات خارج الديار أمام فرق إيطالية','ar'),
 ('Question line 1 (red)','إحكيلي','ar h'),
 ('Question line 2 (red, bigger)','يونايتد بيكسر السلسلة ولا كومو بيكمّلها؟','ar'),
 ('Icons','Heart (red), comment (green), share (navy), save (navy), close together.',''),
 ('Red mark','«إحكيلي» ورقم يونايتد','ar'),
 src('«The Opta supercomputer marginally favours a Como victory, with the Serie A side given a 41.7% chance. Man Utd\'s hopes of ending their winless run are rated at 33.8%, with a draw at 24.5%.»','«The Red Devils are unbeaten in each of their last six Champions League away games against Italian sides (W3 D3).»','Also in the article: this is the first ever meeting of Como and Man Utd.'),
 ('My wording','«بيكسر السلسلة ولا بيكمّلها» is my question: the winless run for United, Como\'s run of results for the other side. The article\'s «Como\'s first two home games» claim is left out. Opta numbers are a pre-match model, not a result.','')]))
D.append("Headline: توقعات Opta للمباراة\nColumn 1: كومو ٤١٫٧٪\nColumn 2: تعادل ٢٤٫٥٪\nColumn 3: يونايتد ٣٣٫٨٪\nDetail: يونايتد لم يخسر في آخر ٦ مباريات خارج الديار أمام فرق إيطالية\nQuestion line 1: إحكيلي\nQuestion line 2: يونايتد بيكسر السلسلة ولا كومو بيكمّلها؟")
IMG.append(noimg("3:2 landscape, generate at 1536x1024 or larger","Keep the bottom fifth open and bright. It fades into the white. The photo band is short on this slide, so keep the roofline in the upper half.",
 "Editorial photograph of a small football stadium on a lake shore at dusk, steep green hills behind, floodlights switched on, empty stands, nobody present. Keep the bottom fifth as soft pale ground. Landscape 3:2. True-to-life colour, high-key exposure, Reuters or Getty editorial style. No text, no logos, no watermarks, no people.",
 "Editorial photograph of an empty football pitch under floodlights in light mist, two goals in the distance, nobody present. Keep the bottom fifth soft and bright. Landscape 3:2. Natural texture, high-key exposure, editorial style. No text, no logos, no watermarks, no people.",
 wm(("A real photo of Stadio Giuseppe Sinigaglia, Como, from outside in daylight","Stadio Giuseppe Sinigaglia","The slide names the stadium, so a real photo is better than an AI one.")),True))

th='padding:6px 8px;border-bottom:1px solid var(--line)'
def tr(*c): return '<tr>'+''.join(f'<td style="padding:6px 8px;vertical-align:top">{x}</td>' for x in c)+'</tr>'
sources=f'''<div style="margin:0 0 34px;padding:18px 20px;border:1px solid var(--line);border-radius:10px;background:#FBFCFE"><h2 style="margin:0 0 6px;font-size:20px">Source: check every claim yourself</h2><p style="margin:0 0 12px;color:var(--mute)">Everything comes from one text: the Opta Analyst «Como vs Man Utd Prediction: Champions League Preview» by Jonathan Davies, 20 October 2026, as you pasted it. I read all of it. It is a pre-match preview, so the lineups and percentages are predictions. Each slide's right-hand column has a "From the article" row with the exact English sentences it uses. I did not check any figure against another outlet.</p><div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;min-width:560px;font-size:14px"><tr style="text-align:left;color:var(--mute)"><th style="{th}">Slide</th><th style="{th}">Claim</th><th style="{th}">Article says</th><th style="{th}">Flag</th></tr>
{tr(2,'6-match winless run (D3 L3), 1-1 at Leeds, 0-2 at Atlético','Run is «in all competitions»','Start of the run is not stated')}
{tr(3,'47 seconds, Yoro sent off, 4 big chances','Barrios scored after 47 seconds; 4th time United conceded in the first minute; Yoro off in the 74th and misses Como','Atlético’s other goal (Lookman) is left out')}
{tr(4,'1 win in 10 away, 1 clean sheet in 15; 21% v 38%','W1 D3 L6 in last 10 away; Ferguson era 190 matches, 21% lost; since then 56 games, 38% lost','The article contradicts itself on «10 away games»: a later line gives W1 D2 L6, which is 9')}
{tr(5,'Diao scored in first two CL games; 21 years 37 days','Scored v Leipzig (4-1) and Feyenoord (3-2 defeat); youngest African to score in both first two','Name spelling in Arabic is my guess')}
{tr(6,'Rashford 17 goals, 50th appearance','«Could make his 50th»; 34 United, 4 Villa, 11 Barcelona; only Kane, Sterling, Cole have more in first 50','Appearance and lineup are predictions')}
{tr(7,'Opta 41.7 / 24.5 / 33.8; unbeaten in last 6 away v Italian sides','Como 41.7%, draw 24.5%, United 33.8%; W3 D3','Model output, not a result')}
</table></div><p style="margin:12px 0 0;color:var(--mute);font-size:13px">Left out on purpose: the Sabah 4-0 on Matchday 1, Como’s chance to be the first Italian side since Lazio (1999-2000) to win its first two home games, Chalobah’s fitness doubt, Carrick and Fàbregas meeting as players in the 2008-09 semi-final, the predicted lineups, and the Opta Power Rankings. The article also confirms the 1-1 draw at Leeds on Sunday, which is the last game in the Carrick numbers on the Ten Hag slide 7.</p></div>'''
