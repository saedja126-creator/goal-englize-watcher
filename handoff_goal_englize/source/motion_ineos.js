// usage: node motion_ineos.js 24 7 1 2 3
const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
 const fps=+process.argv[2], secs=+process.argv[3], slides=process.argv.slice(4).map(Number);
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const p=await b.newPage({viewport:{width:1200,height:1600}});
 await p.addInitScript(()=>{delete window.IntersectionObserver;});
 await p.goto('file://'+process.cwd()+'/_ineos_page.html',{waitUntil:'networkidle'});
 await p.addStyleTag({content:'.card{width:1080px!important;max-width:none!important;box-shadow:none!important}.slide{display:block!important}.card.mo .pi{animation-duration:'+secs+'s!important}'});
 await p.evaluate(()=>document.fonts.ready);
 for(const n of slides){
  const card=p.locator('.card').nth(n-1);
  await card.scrollIntoViewIfNeeded();
  const dir=`ineos_frames/s${n}`; fs.rmSync(dir,{recursive:true,force:true}); fs.mkdirSync(dir,{recursive:true});
  await card.evaluate(c=>{c.classList.remove('pending');c.classList.remove('mo');void c.offsetWidth;c.classList.add('mo');});
  const total=Math.round(fps*secs);
  for(let f=0;f<=total;f++){
   const t=Math.min(f/fps,secs);
   await card.evaluate((c,t)=>{c.getAnimations({subtree:true}).forEach(a=>{a.pause();a.currentTime=t*1000;});},t);
   await card.screenshot({path:`${dir}/${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});
  }
  console.log('done',n);
 }
 await b.close();
})();
