const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 const p=await b.newPage({viewport:{width:420,height:900}});
 const html=require('fs').readFileSync('ineos_slides_download.html','utf8');
 // stand-in for the viewer's downloads capability
 await p.goto('about:blank');
 await p.evaluate(()=>{window.__saved=[];window.claude={use:async n=>n==='downloads'?{save:async r=>{window.__saved.push([r.filename,r.data.size,r.data.type]);window.__last=window.__last||{};window.__last[r.filename]=r.data;return {status:'saved'}}}:null};});
 await p.setContent('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>',{waitUntil:'load'});
 await p.waitForTimeout(1500);
 console.log('msg:',await p.textContent('#msg'));
 await p.click('button[data-kind="mp4"][data-n="3"]'); await p.waitForTimeout(300);
 await p.click('button[data-kind="png"][data-n="7"]'); await p.waitForTimeout(300);
 await p.click('#allV'); await p.waitForTimeout(2500);
 console.log('png7',JSON.stringify(await p.evaluate(async()=>{const b=window.__last['Ineos_Slide_7.png'];const bm=await createImageBitmap(b);return [b.size,bm.width,bm.height]})));
 console.log('mp4 3 size',await p.evaluate(()=>window.__last['Ineos_Slide_3.mp4'].size));
 console.log(JSON.stringify(await p.evaluate(()=>window.__saved)));
 const vid=await p.evaluate(()=>{const v=document.getElementById("vid2");return [v.readyState,v.duration,v.videoWidth,v.videoHeight,!!v.poster]});
 console.log('video2',JSON.stringify(vid));
 await p.screenshot({path:'dl_ineos.png',fullPage:false});
 await b.close();
})();
