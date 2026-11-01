P="#8B5CF6"; A="#EC4899"; BG="#000000"
TOT=6
def prog(i):
    return '<div class="progress">'+''.join(
        f'<span class="{"p-done" if k<i else "p-active" if k==i else "p-next"}"></span>' for k in range(1,TOT+1))+'</div>'
def slide(i, body):
    return f'<div class="slide{" active" if i==1 else ""}" id="s{i}">{prog(i)}<div class="slide-num">{i} / {TOT}</div><div class="content">{body}</div></div>'
def items(lst, fs=36):
    return ''.join(f'<div class="list-item"><div class="num-circle">{n}</div><div class="item-text" style="font-size:{fs}px">{t}</div></div>' for n,t in enumerate(lst,1))

s=[]
s.append(slide(1,'''
<div class="sub-text" style="font-size:34px;letter-spacing:2px;margin-bottom:30px">🔴 حصري من The Athletic</div>
<div class="grad" style="font-size:112px">تن هاغ يفتح الصندوق الأسود</div>
<div class="main-text" style="font-size:54px;margin-top:40px">"وعدوني بالولاء والدعم…<br>بس ما وفّوا بشي"</div>
<div class="cta-btn">اسحب وشوف القصة ←</div>
<div class="arrow-btn">›</div>'''))
s.append(slide(2,'''
<div style="font-size:200px;line-height:1">⚖️</div>
<div class="main-text" style="font-size:62px;margin-top:30px">فاز بكأس إنجلترا على سيتي…<br><span class="grad" style="font-size:62px">وبعدها بخمسة شهور انقال؟</span></div>
<div class="sub-text" style="font-size:44px;margin-top:44px">٢٨ أكتوبر ٢٠٢٤ — يونايتد بالمركز ١٤<br>١١ نقطة من ٩ مباريات، يوم الإقالة</div>
<div class="sub-text" style="font-size:40px;margin-top:30px">تن هاغ: "الداتا كانت تقول إحنا منيحين"</div>'''))
s.append(slide(3,'''
<div class="grad" style="font-size:78px;margin-bottom:70px">الوعود اللي انكسرت</div>'''+items([
 'اتفاق في إيبيزا بعد النهائي: ولاء + دعم + تواصل',
 'شرط واضح: <span class="grad" style="font-size:36px">ما حدا يبيع ماكتومناي</span>',
 'انباع لنابولي بـ ٣٠.٥ مليون يورو لتمويل أوغارتي',
 'تن هاغ: "انحرجت كثير… وانخيبت"'],44)))
s.append(slide(4,'''
<div class="grad" style="font-size:72px;margin-bottom:44px">الأسماء اللي ما وصلت</div>'''+items([
 '<b>هاري كين</b> — "بدي لاعب واحد بس… وإنتو بتعرفوه". انرفض، ورح لبايرن بـ ١١٠م يورو',
 '<b>ديكلان رايس</b> — وست هام ما باع، وراح لأرسنال بـ ١٠٥م جنيه',
 '<b>فرينكي دي يونغ</b> — رفض يجي رغم أسابيع مفاوضات',
 '<b>بروبي وويلبيك</b> — بروبي: اتأخروا عليه. ويلبيك: ما انقدّم عرض رسمي'],37)))
s.append(slide(5,'''
<div style="font-size:170px;line-height:1">🐐🔥</div>
<div class="grad" style="font-size:76px;margin-top:20px">رونالدو و"الثقافة السامة"</div>
<div class="main-text" style="font-size:46px;margin-top:40px">"خذل الفريق وخذلني"</div>
<div class="sub-text" style="font-size:36px;margin-top:36px;line-height:1.8">• كمّل لفّتين بس من ٣ بعد خسارة برينتفورد ٤-٠<br>• "كان يقول للاعيبة: وفّروا طاقتكم بالتمرين"<br>• تن هاغ يشوف "مجموعة مدريد" (كاسيميرو، فاران، رونالدو) جابت نفوذ اللاعبين</div>'''))
s.append(slide(6,'''
<div style="font-size:150px;line-height:1">🗳️</div>
<div class="main-text" style="font-size:60px;margin-top:20px">وكاريك؟ تن هاغ بحكي:<br><span class="grad" style="font-size:60px">"إقالته مش الحل أبداً"</span></div>
<div class="main-text" style="font-size:52px;margin-top:50px">مين الغلطان بقصة تن هاغ؟</div>
<div class="sub-text" style="font-size:40px;margin-top:30px;line-height:1.9">١ — الإدارة 🏢 &nbsp; ٢ — تن هاغ 🇳🇱 &nbsp; ٣ — اللاعبين 😤</div>
<div class="cta-btn" style="font-size:34px">احفظ 🔖 وشارك مع صاحبك المانيوتدي</div>
<div class="sub-text" style="font-size:38px;margin-top:40px;font-weight:700"><span style="direction:ltr;unicode-bidi:isolate">@GoalEnglize</span></div>'''))

css=f'''*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#141414;font-family:'Cairo',Tahoma,Arial,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;gap:24px;padding:24px 0;}}
.slide{{width:1080px;height:1350px;background:{BG};border-radius:32px;display:none;flex-direction:column;overflow:hidden;}}
.slide.active{{display:flex;}}
.progress{{display:flex;gap:8px;padding:40px 60px 0;direction:ltr;}}
.progress span{{height:8px;border-radius:4px;flex:1;}}
.p-done{{background:#4b4b57;}}
.p-active{{background:linear-gradient(90deg,{P},{A});}}
.p-next{{background:#1d1d24;}}
.slide-num{{color:#8a8a99;font-size:32px;font-weight:700;padding:10px 60px 0;text-align:left;direction:ltr;}}
.content{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 80px 60px;text-align:center;}}
.grad{{background:linear-gradient(90deg,{P},{A});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:900;padding-bottom:12px;display:inline-block;line-height:1.3;}}
.main-text{{color:#fff;font-weight:700;line-height:1.4;}}
.sub-text{{color:#b4b4c2;line-height:1.6;}}
.cta-btn{{background:{P}33;border:4px solid {P};border-radius:60px;padding:24px 70px;color:#fff;font-size:36px;font-weight:700;margin-top:40px;display:inline-block;}}
.arrow-btn{{width:90px;height:90px;background:{P};border-radius:50%;display:flex;align-items:center;justify-content:center;margin:24px auto 0;font-size:40px;color:#fff;font-weight:900;direction:ltr;}}
.list-item{{display:flex;flex-direction:row;align-items:center;gap:30px;width:100%;margin-bottom:40px;}}
.num-circle{{width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,{P},{A});display:flex;align-items:center;justify-content:center;color:#fff;font-size:36px;font-weight:900;flex-shrink:0;}}
.item-text{{color:#fff;font-weight:700;text-align:right;flex:1;line-height:1.5;}}
.nav{{display:flex;gap:20px;align-items:center;flex-wrap:wrap;justify-content:center;}}
.nav-btn{{background:#333;border:none;color:#fff;font-size:32px;width:72px;height:72px;border-radius:50%;cursor:pointer;}}
.nav-info{{color:#888;font-size:24px;}}
.dl-btn{{background:linear-gradient(90deg,{P},{A});border:none;border-radius:20px;padding:16px 40px;color:#fff;font-size:24px;font-weight:700;cursor:pointer;font-family:inherit;}}
.dl-all-btn{{background:#1a1a1a;border:2px solid {P};border-radius:20px;padding:16px 40px;color:#fff;font-size:24px;font-weight:700;cursor:pointer;font-family:inherit;}}'''

js='''let c=1,tot=6;
function go(d){document.getElementById('s'+c).classList.remove('active');c=Math.max(1,Math.min(tot,c+d));document.getElementById('s'+c).classList.add('active');document.getElementById('info').textContent=c+' / '+tot;}
function dlCurrent(){var el=document.getElementById('s'+c);htmlToImage.toPng(el,{width:1080,height:1350,pixelRatio:1}).then(function(url){var a=document.createElement('a');a.download='slide_'+c+'.png';a.href=url;a.click();});}
async function dlAll(){var orig=c;for(var i=1;i<=tot;i++){var el=document.getElementById('s'+i);el.style.display='flex';await new Promise(r=>setTimeout(r,300));var url=await htmlToImage.toPng(el,{width:1080,height:1350,pixelRatio:1});if(i!==orig)el.style.display='none';var a=document.createElement('a');a.download='slide_'+i+'.png';a.href=url;a.click();await new Promise(r=>setTimeout(r,500));}document.getElementById('s'+orig).style.display='flex';document.getElementById('info').textContent=orig+' / '+tot;}'''

html=f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>Carousel - Ten Hag Interview</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html-to-image/1.11.11/html-to-image.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
{chr(10).join(s)}
<div class="nav">
  <button class="nav-btn" onclick="go(-1)">‹</button>
  <span class="nav-info" id="info">1 / 6</span>
  <button class="nav-btn" onclick="go(1)">›</button>
  <button class="dl-btn" onclick="dlCurrent()">📥 حمّل الشريحة PNG</button>
  <button class="dl-all-btn" onclick="dlAll()">⬇️ حمّل الكل</button>
</div>
<script>
{js}
</script>
</body>
</html>'''
open('/home/user/goal-englize-watcher/carousel_tenhag_interview.html','w').write(html)
