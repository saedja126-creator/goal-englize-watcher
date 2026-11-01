const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 const p=await b.newPage({viewport:{width:1100,height:1400}});
 const html=require('fs').readFileSync('como_man_utd_carousel_plan.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset=utf8></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.addStyleTag({content:'.card.pending .rs{opacity:1!important}.card .rs{animation:none!important}'});
 await p.evaluate(()=>document.fonts.ready);
 const r=await p.evaluate(()=>{const out=[];document.querySelectorAll('.tz').forEach((t,i)=>{t.querySelectorAll('[style*="nowrap"]').forEach(e=>{out.push([i+1,e.textContent.slice(0,22),Math.round(e.scrollWidth),Math.round(t.clientWidth)])});out.push(['tz',i+1,t.scrollHeight,t.clientHeight])});return out});
 console.log(JSON.stringify(r));
 const cards=await p.locator('.card').all();
 for(let i=0;i<cards.length;i++){await cards[i].screenshot({path:`c${i+1}.png`});}
 await b.close();
})();
