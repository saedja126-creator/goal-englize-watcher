const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 const p=await b.newPage({viewport:{width:1200,height:1500}});
 await p.goto('file:///home/user/goal-englize-watcher/carousel_tenhag_interview.html',{waitUntil:'domcontentloaded'});
 for(let i=1;i<=6;i++){
  await p.evaluate(i=>{document.querySelectorAll('.slide').forEach(s=>s.classList.remove('active'));document.getElementById('s'+i).classList.add('active');},i);
  await p.locator('#s'+i).screenshot({path:`s${i}.png`});
 }
 await b.close();
})();
