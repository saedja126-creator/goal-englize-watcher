const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 const p=await b.newPage({viewport:{width:1100,height:1400}});
 const msgs=[];p.on('console',m=>{if(m.type()==='error')msgs.push(m.text())});p.on('pageerror',e=>msgs.push('PAGEERR '+e.message));
 const html=require('fs').readFileSync('como_man_utd_carousel_plan.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset=utf8></head><body>'+html+'</body></html>',{waitUntil:'domcontentloaded'});
 await p.addStyleTag({content:'.card.pending .rs{opacity:1!important}.card .rs{animation:none!important}'});
 await p.waitForTimeout(800);
 const cards=await p.locator('.card').all();
 for(let i=0;i<cards.length;i++){await cards[i].screenshot({path:`c${i+1}.png`});}
 const over=await p.evaluate(()=>[...document.querySelectorAll('.tz')].map((t,i)=>[i+1,t.scrollHeight,t.clientHeight]));
 console.log(JSON.stringify(over),msgs.slice(0,5));
 await p.screenshot({path:'page.png',fullPage:false});
 await b.close();
})();
