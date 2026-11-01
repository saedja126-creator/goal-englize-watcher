const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const p=await b.newPage({viewport:{width:1200,height:1600}});
 const html=fs.readFileSync('ineos_carousel_plan.html','utf8');
 await p.addInitScript(()=>{delete window.IntersectionObserver;});
 await p.setContent('<!doctype html><html><head><meta charset=utf8></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.addStyleTag({content:'.card{width:1080px!important;max-width:none!important}.slide{display:block!important}'});
 const r=await p.evaluate(()=>[...document.querySelectorAll('.card')].map((c,i)=>{const rs=c.querySelector('.rs');const a=c.getAnimations({subtree:true});return [i+1,c.className,a.length,rs&&getComputedStyle(rs).opacity,c.querySelectorAll('.rs').length, c.querySelector('.wtext')&&c.querySelector('.wtext').innerText.slice(0,20)]}));
 console.log(JSON.stringify(r));
 await b.close();
})();
