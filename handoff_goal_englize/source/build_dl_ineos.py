import base64,re
src=open('como_slides_download.html',encoding='utf8').read()
css=src[src.index('<style>'):src.index('</style>')+8]
head='<meta name="claude:viewport-fit-sides" content="cover">\n<title>Ineos Slides</title>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&display=swap">\n'
N=9
figs=''.join(f'<figure class="s"><video class="v" id="vid{n}" controls playsinline loop muted preload="auto" width="1080" height="1440" aria-label="INEOS slide {n} with motion"></video><figcaption><b>Slide {n}</b><span>Ineos_Slide_{n}</span></figcaption><div class="row"><button class="btn" type="button" data-kind="mp4" data-n="{n}" hidden>Save video</button><button class="btn alt" type="button" data-kind="png" data-n="{n}" hidden>Save image</button></div></figure>\n' for n in range(1,N+1))
body=f'''<div class="wrap"><h1>INEOS slides</h1>
<p class="lead">Nine finished slides, 1080 x 1440. Each has a video with the motion (about 8 seconds: text rising, photo zooming slowly) and a PNG image of the last frame.</p>
<div class="bar"><button class="btn" id="allV" type="button" hidden>Save all 9 videos</button><button class="btn alt" id="allI" type="button" hidden>Save all 9 images</button></div>
<p class="msg" id="msg" role="status">Loading the slides...</p>
<p class="fallback" id="fb" hidden>If the Save buttons do not appear, open this page in Safari or Chrome. You can also play a video and use the browser's own save option.</p>
<div class="grid">
{figs}</div></div>
'''
data=''
for n in range(1,N+1):
    data+=f'<script type="text/plain" id="v{n}">'+base64.b64encode(open(f'ineos_emb/v{n}.mp4','rb').read()).decode()+'</script>\n'
    data+=f'<script type="text/plain" id="i{n}">'+base64.b64encode(open(f'ineos_emb/i{n}.jpg','rb').read()).decode()+'</script>\n'
js='''<script>
(function(){
var N=9,msg=document.getElementById("msg"),fb=document.getElementById("fb"),dl=null;
var btns=[].slice.call(document.querySelectorAll("button[data-n]")),allV=document.getElementById("allV"),allI=document.getElementById("allI");
function say(t,c){msg.textContent=t;msg.className="msg"+(c?" "+c:"")}
function busy(b){btns.forEach(function(x){x.disabled=b});allV.disabled=b;allI.disabled=b}
function blobOf(id,type){
 var s=document.getElementById(id).textContent.trim(),bin=atob(s),u=new Uint8Array(bin.length);
 for(var i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);
 return new Blob([u],{type:type});
}
function pngOf(n){
 return new Promise(function(res,rej){
  var url=URL.createObjectURL(blobOf("i"+n,"image/jpeg")),im=new Image();
  im.onload=function(){
   var c=document.createElement("canvas");c.width=1080;c.height=1440;
   c.getContext("2d").drawImage(im,0,0,1080,1440);
   c.toBlob(function(b){URL.revokeObjectURL(url);b?res(b):rej(new Error("png"))},"image/png");
  };
  im.onerror=function(){rej(new Error("img"))};
  im.src=url;
 });
}
function one(kind,n){
 if(kind==="mp4")return dl.save({filename:"Ineos_Slide_"+n+".mp4",data:blobOf("v"+n,"video/mp4")});
 return pngOf(n).then(function(b){return dl.save({filename:"Ineos_Slide_"+n+".png",data:b})});
}
function why(e){
 var c=e&&e.code;
 if(c==="declined")return "Not saved. You declined, so I stopped.";
 if(c==="rate_limited")return "Wait a moment, then tap again.";
 return "Saving is not available in this view. Open the page in Safari or Chrome.";
}
for(var n=1;n<=N;n++){(function(n){
 var v=document.getElementById("vid"+n);
 try{
  v.poster=URL.createObjectURL(blobOf("i"+n,"image/jpeg"));
  v.src=URL.createObjectURL(blobOf("v"+n,"video/mp4"));
 }catch(e){}
})(n)}
btns.forEach(function(b){b.addEventListener("click",function(){
 var n=+b.getAttribute("data-n"),k=b.getAttribute("data-kind");busy(true);say("Waiting for your confirmation...");
 var p;try{p=one(k,n)}catch(e){p=Promise.reject(e)}
 p.then(function(){say((k==="mp4"?"Video ":"Image ")+n+" saved.","ok")},function(e){say(why(e),"warn")}).then(function(){busy(false)});
})});
function batch(kind){
 busy(true);var n=1;
 (function next(){
  if(n>N){say("All "+N+" "+(kind==="mp4"?"videos":"images")+" saved.","ok");busy(false);return}
  say("Saving "+n+" of "+N+". Confirm each one.");
  var p;try{p=one(kind,n)}catch(e){p=Promise.reject(e)}
  p.then(function(){n++;next()},function(e){say(why(e),"warn");busy(false)});
 })();
}
allV.addEventListener("click",function(){batch("mp4")});
allI.addEventListener("click",function(){batch("png")});
fb.hidden=false;
if(window.claude&&window.claude.use){
 window.claude.use("downloads").then(function(d){
  if(!d){say("Save buttons are not available in this view.","warn");return}
  dl=d;fb.hidden=true;say("Tap Save under a slide. You confirm each file before it is saved.");
  btns.forEach(function(b){b.hidden=false});allV.hidden=false;allI.hidden=false;
 },function(){say("Save buttons are not available in this view.","warn")});
}else{say("Save buttons are not available in this view.","warn")}
})();
</script>
'''
out=head+css+'\n'+body+data+js
open('ineos_slides_download.html','w',encoding='utf8').write(out)
print(len(out)/1e6,'MB')
