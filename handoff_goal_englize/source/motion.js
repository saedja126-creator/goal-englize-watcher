// usage: node motion.js <slideNo> <fps> <seconds>
const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
 const n=+process.argv[2], fps=+process.argv[3]||24, secs=+process.argv[4]||7;
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 const p=await b.newPage({viewport:{width:1200,height:1600}});
 const html=fs.readFileSync('como_man_utd_carousel_plan.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset=utf8></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.addStyleTag({content:'.card{width:1080px!important;max-width:none!important;box-shadow:none!important}.slide{display:block!important}.card.mo .pi{animation-duration:'+secs+'s!important}.card.mo .ph.has{animation:none!important}'});
 await p.evaluate(()=>document.fonts.ready);
 const card=p.locator('.card').nth(n-1);
 await card.scrollIntoViewIfNeeded();
 const dir=`frames/s${n}`; fs.rmSync(dir,{recursive:true,force:true}); fs.mkdirSync(dir,{recursive:true});
 await card.evaluate(c=>{c.classList.remove('pending');c.classList.add('mo');});
 const total=Math.round(fps*secs);
 for(let f=0;f<=total;f++){
  const t=Math.min(f/fps,secs);
  await card.evaluate((c,t)=>{c.getAnimations({subtree:true}).forEach(a=>{a.pause();a.currentTime=t*1000;});},t);
  await card.screenshot({path:`${dir}/${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});
  if(f===total){await card.screenshot({path:`final_como/Como_Slide_${n}.png`});}
 }
 await b.close();
 console.log('done',n,total+1);
})();
