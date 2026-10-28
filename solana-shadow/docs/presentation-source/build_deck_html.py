"""Assemble the published slides into one standalone HTML file (arrow keys to move; print to save as PDF)."""
import json
import sys
from pathlib import Path

src = Path(sys.argv[1])  # folder holding project/deck.json and project/slides/*.html
out = Path(sys.argv[2])
deck = json.loads((src / "project" / "deck.json").read_text(encoding="utf-8"))
slides = []
for sid in deck["order"]:
    html = (src / "project" / "slides" / f"{sid}.html").read_text(encoding="utf-8").strip()
    html = html.replace("<section ", '<section class="slide" ', 1)
    slides.append(f'<div class="slide-wrap" id="s-{sid}">{html}</div>')

title = deck.get("title", "Presentation")
page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Public+Sans:wght@400;600;700&display=swap">
<style>
html,body{{margin:0;height:100%;background:#0b0f17;overflow:hidden;font-family:'Public Sans',Arial,sans-serif}}
:root{{--s:1}}
.slide-wrap{{position:absolute;width:1920px;height:1080px;transform:scale(var(--s));transform-origin:top left;
  left:calc((100vw - 1920px * var(--s)) / 2);top:calc((100vh - 1080px * var(--s)) / 2);display:none}}
.slide{{width:1920px;height:1080px;box-sizing:border-box;position:relative;overflow:hidden}}
.slide *{{margin:0;box-sizing:border-box}}
.slide ul,.slide ol{{padding-left:1.1em}}.slide li{{margin-bottom:.35em}}
.slide table{{border-collapse:collapse;width:100%;table-layout:fixed}}
.slide th,.slide td{{padding:.35em .6em;text-align:left;vertical-align:top}}
.slide aside{{display:none}}
x-shape{{display:block}}
x-shape[kind="arrow-right"]{{clip-path:polygon(0 28%,60% 28%,60% 0,100% 50%,60% 100%,60% 72%,0 72%)}}
.ui{{position:fixed;left:0;right:0;bottom:8px;text-align:center;color:#8a95a7;font-size:14px;z-index:5;pointer-events:none}}
@media print{{
  @page{{size:1920px 1080px;margin:0}}
  html,body{{overflow:visible;height:auto;background:none}}
  .slide-wrap{{display:block !important;position:relative !important;left:0 !important;top:0 !important;transform:none !important;page-break-after:always;break-after:page}}
  .ui{{display:none}}
}}
</style></head><body>
{chr(10).join(slides)}
<div class="ui"><span id="n"></span> &nbsp;·&nbsp; ← → to move &nbsp;·&nbsp; Print (Ctrl+P) and choose Save as PDF to keep a copy</div>
<script>
const w=[...document.querySelectorAll('.slide-wrap')];let i=0;
function fit(){{document.documentElement.style.setProperty('--s',Math.min(innerWidth/1920,innerHeight/1080))}}
function show(k){{i=Math.max(0,Math.min(w.length-1,k));w.forEach((e,j)=>e.style.display=j===i?'block':'none');
  document.getElementById('n').textContent=(i+1)+' / '+w.length;history.replaceState(null,'','#'+(i+1))}}
addEventListener('resize',fit);addEventListener('hashchange',()=>show((parseInt(location.hash.slice(1))||1)-1));
addEventListener('keydown',e=>{{if(['ArrowRight','PageDown',' '].includes(e.key))show(i+1);if(['ArrowLeft','PageUp'].includes(e.key))show(i-1);
  if(e.key==='Home')show(0);if(e.key==='End')show(w.length-1)}});
addEventListener('click',e=>show(e.clientX>innerWidth/2?i+1:i-1));
fit();show((parseInt(location.hash.slice(1))||1)-1);
</script></body></html>"""
out.write_text(page, encoding="utf-8")
print(f"{len(slides)} slides -> {out} ({out.stat().st_size} bytes)")
