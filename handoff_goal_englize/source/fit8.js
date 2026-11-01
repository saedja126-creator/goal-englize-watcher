const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 const p=await b.newPage({viewport:{width:1100,height:1400}});
 const html=require('fs').readFileSync('manutd_scenario_plan.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset=utf8></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.addStyleTag({content:'.card.pending .rs{opacity:1!important}.card .rs{animation:none!important}'});
 await p.evaluate(()=>document.fonts.ready);
 const r=await p.evaluate(()=>{const out=[];document.querySelectorAll('.card.w').forEach((c,i)=>{const w=c.querySelector('.wtext');c.querySelectorAll('.bl').forEach(l=>{if(l.scrollWidth>l.clientWidth+1)out.push(['OVER',i+1,l.textContent.slice(0,18),l.scrollWidth,l.clientWidth])});const t=w.getBoundingClientRect(),cr=c.getBoundingClientRect();out.push([i+1,'text top %',Math.round((t.top-cr.top)/cr.height*100),'bottom %',Math.round((cr.bottom-t.bottom)/cr.height*100)])});return out});
 console.log(JSON.stringify(r));
 const cards=await p.locator('.card').all();
 for(let i=0;i<cards.length;i++){await cards[i].screenshot({path:`m${i+1}.png`});}
 await b.close();
})();
