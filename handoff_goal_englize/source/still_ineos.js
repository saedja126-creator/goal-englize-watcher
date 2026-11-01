// usage: node still_ineos.js <outdir> <t_seconds>
const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
 const out=process.argv[2], t=+process.argv[3]||7;
 fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 const p=await b.newPage({viewport:{width:1200,height:1600}});
 const html=fs.readFileSync('ineos_carousel_plan.html','utf8');
 await p.addInitScript(()=>{delete window.IntersectionObserver;});
 fs.writeFileSync('_ineos_page.html','<!doctype html><html><head><meta charset=utf8></head><body>'+html+'</body></html>');
 await p.goto('file://'+process.cwd()+'/_ineos_page.html',{waitUntil:'networkidle'});
 await p.addStyleTag({content:'.card{width:1080px!important;max-width:none!important;box-shadow:none!important}.slide{display:block!important}.card.mo .pi{animation-duration:7s!important}'});
 await p.evaluate(()=>document.fonts.ready);
 const cards=await p.locator('.card').all();
 for(let i=0;i<cards.length;i++){
  const c=cards[i];
  await c.scrollIntoViewIfNeeded();
  await c.evaluate(c=>{c.classList.remove('pending');c.classList.add('mo');});
  await c.evaluate((c,t)=>{c.getAnimations({subtree:true}).forEach(a=>{a.pause();a.currentTime=t*1000;});},t);
  await c.screenshot({path:`${out}/S${i+1}.png`});
 }
 await b.close();
})();
