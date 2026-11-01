const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 const p=await b.newPage({viewport:{width:1400,height:1600}});
 const html=require('fs').readFileSync('ten_hag_carousel_plan.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset=utf8></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.addStyleTag({content:'.card.pending .rs{opacity:1!important}.card *{animation:none!important}.card{width:1080px!important;max-width:none!important;box-shadow:none!important}.slide{display:block!important}'});
 await p.evaluate(()=>document.fonts.ready);
 const fonts=await p.evaluate(()=>[...document.fonts].map(f=>f.family+':'+f.status));
 console.log(JSON.stringify([...new Set(fonts)]));
 const cards=await p.locator('.card').all();
 for(let i=0;i<cards.length;i++){await cards[i].screenshot({path:`final/Ten_Hag_Slide_${i+1}.png`});}
 await b.close();
})();
