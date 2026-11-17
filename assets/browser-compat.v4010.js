(function(){
'use strict';
// Browser brands are informational. The engine version is taken from the
// corresponding engine token; SamsungBrowser/24 is NOT Chromium/24.
var MIN={chromium:84,firefox:86,safari:14.1};
var JXL_PROBE='./assets/jxl-probe.v4010.jxl?v=4010';
function num(v){var n=parseFloat(v);return isFinite(n)?n:0;}
function token(ua,re){var m=ua.match(re);return m?num(m[1]):0;}
function detect(ua){
  ua=String(ua===undefined?(navigator.userAgent||''):ua);
  var android=/\bAndroid\b/i.test(ua),ios=/\b(?:iPhone|iPad|iPod)\b/i.test(ua),
      chromium=token(ua,/(?:Chrome|Chromium)\/(\d+(?:\.\d+)?)/),
      firefox=token(ua,/Firefox\/(\d+(?:\.\d+)?)/),
      safari=token(ua,/Version\/(\d+(?:\.\d+)?)/);
  var brands=[
    [/Edg(?:A|iOS)?\/(\d+(?:\.\d+)?)/i,'Microsoft Edge'],
    [/SamsungBrowser\/(\d+(?:\.\d+)?)/i,'Samsung Internet'],
    [/(?:XiaoMi\/)?MiuiBrowser\/(\d+(?:\.\d+)?)/i,'Mi Browser'],
    [/MiBrowser\/(\d+(?:\.\d+)?)/i,'Mi Browser'],
    [/(?:TapTapBrowser|TapTapBrowserMobile|TapBrowser)\/(\d+(?:\.\d+)?)/i,'TapTap Browser'],
    [/\bTapTap(?:\/|\s)(\d+(?:\.\d+)?)/i,'TapTap Browser'],
    [/OPR\/(\d+(?:\.\d+)?)/i,'Opera'],
    [/Vivaldi\/(\d+(?:\.\d+)?)/i,'Vivaldi'],
    [/Brave\/(\d+(?:\.\d+)?)/i,'Brave'],
    [/YaBrowser\/(\d+(?:\.\d+)?)/i,'Yandex Browser'],
    [/UCBrowser\/(\d+(?:\.\d+)?)/i,'UC Browser'],
    [/QQBrowser\/(\d+(?:\.\d+)?)/i,'QQ Browser'],
    [/DuckDuckGo\/(\d+(?:\.\d+)?)/i,'DuckDuckGo Browser'],
    [/Waterfox\/(\d+(?:\.\d+)?)/i,'Waterfox'],
    [/Floorp\/(\d+(?:\.\d+)?)/i,'Floorp'],
    [/Librewolf\/(\d+(?:\.\d+)?)/i,'LibreWolf'],
    [/Iceraven\/(\d+(?:\.\d+)?)/i,'Iceraven'],
    [/Fennec\/(\d+(?:\.\d+)?)/i,'Fennec'],
    [/FxiOS\/(\d+(?:\.\d+)?)/i,'Firefox for iOS'],
    [/FxFocus\/(\d+(?:\.\d+)?)/i,'Firefox Focus'],
    [/Firefox\/(\d+(?:\.\d+)?)/i,'Firefox'],
    [/CriOS\/(\d+(?:\.\d+)?)/i,'Chrome for iOS'],
    [/Chrome\/(\d+(?:\.\d+)?)/i,'Google Chrome'],
    [/Chromium\/(\d+(?:\.\d+)?)/i,'Chromium']
  ];
  var name='Unknown browser',version=0;
  for(var i=0;i<brands.length;i++){
    var match=ua.match(brands[i][0]);if(match){name=brands[i][1];version=num(match[1]);break;}
  }
  // iOS browser brands run on the platform WebKit engine, not desktop Gecko/Blink.
  var family=ios?'safari':firefox?'firefox':chromium?'chromium':
      /AppleWebKit\//i.test(ua)&&/Safari\//i.test(ua)?'safari':'unknown';
  var engineVersion=family==='chromium'?chromium:family==='firefox'?firefox:safari;
  if(name==='Unknown browser'&&family==='safari')name='Safari / WebKit-based browser';
  return {family:family,name:name,version:version,engineVersion:engineVersion,
          platform:android?'android':ios?'ios':'desktop',isEdge:/^Microsoft Edge$/.test(name)};
}
function features(){return !!(window.Promise&&window.fetch&&window.Map&&window.Set&&window.URL&&window.URLSearchParams&&window.AbortController&&window.ResizeObserver&&window.requestAnimationFrame&&window.matchMedia&&window.Intl&&Intl.DateTimeFormat&&Intl.Collator&&window.Element&&Element.prototype.animate&&Element.prototype.getAnimations);}
var b=detect(),min=MIN[b.family]||0;
// If UA was reduced/spoofed, do not infer an unsupported capability from it.
var versionOK=!b.engineVersion||!min||b.engineVersion>=min;
var baseOK=versionOK&&features();
window.__VULKANSCOPE_COMPATIBLE__=baseOK?null:false;
window.__VULKANSCOPE_BROWSER_INFO__=b;
window.__VULKANSCOPE_JXL_STATUS__='unknown';
window.__VULKANSCOPE_JXL_METHOD__='none';
function element(id){return document.getElementById(id);}
function launchApp(){
  if(window.__VULKANSCOPE_COMPATIBLE__!==true)return;
  var script=document.createElement('script');script.src='./assets/app.v4010.js?v=4010';script.async=false;
  script.onerror=function(){var why=element('browserCompatibilityReason');if(why)why.textContent='The application bundle could not be downloaded. Check your connection and retry.';var gate=element('browserCompatibilityGate');if(gate)gate.hidden=false;};
  document.body.appendChild(script);
}
// JPEG XL must genuinely decode. Native engines update intrinsic dimensions;
// JXL-RS Edge 4.0.1 instead paints a sibling canvas without changing the img.
// See its content.js: createCanvas() -> first onFrame -> release() -> activateOverlay().
// Mere extension presence, a pending marker or an undecoded canvas are NOT success.
function jxlRsEdgePainted(img){
  if(!img||img.getAttribute('data-jxl-rs-edge-060')!=='released')return false;
  var canvas=img.previousElementSibling;
  if(!canvas||canvas.localName!=='canvas'||!canvas.hasAttribute('data-jxl-rs-edge-canvas')||
     canvas.parentElement!==img.parentElement||!canvas.isConnected||!img.isConnected)return false;
  if(!(canvas.width>0&&canvas.height>0))return false;
  var rect=canvas.getBoundingClientRect();
  if(!(rect.width>0&&rect.height>0))return false;
  var computed=getComputedStyle(canvas);
  if(computed.display==='none'||computed.visibility!=='visible'||Number(computed.opacity)===0)return false;
  var imgRect=img.getBoundingClientRect();
  return imgRect.width>0&&imgRect.height>0;
}
function jxlProbe(){return new Promise(function(resolve){
  var host=element('browserJxlProbeHost'),img=document.createElement('img'),settled=false,timer=0,observer=null;
  if(!host){resolve('probe_unavailable');return;}
  function removeProbe(){
    if(observer)observer.disconnect();
    if(img.parentNode)img.parentNode.removeChild(img);
    // The extension places the canvas immediately before the image. Removing
    // its own test container's children is safe; the extension also cleans up.
    while(host.firstChild&&host.firstChild.localName!=='span')host.removeChild(host.firstChild);
  }
  function finish(value,method){
    if(settled)return;settled=true;clearTimeout(timer);
    window.__VULKANSCOPE_JXL_METHOD__=method||'none';
    img.onload=null;img.onerror=null;removeProbe();resolve(value);
  }
  function check(){
    if(settled)return;
    if(img.complete&&img.naturalWidth===2&&img.naturalHeight===2){finish('supported','native');return;}
    if(jxlRsEdgePainted(img)){finish('supported','jxl-rs-edge-canvas');}
  }
  async function inspectFailure(){
    if(settled)return;
    // A fetch/MIME result is diagnostic only; it never establishes decode support.
    var status='decoder_failed';
    try{
      var response=await fetch(JXL_PROBE,{cache:'no-store',credentials:'same-origin'});
      if(!response.ok)status='probe_unavailable';
      else if(!/^image\/jxl(?:\s*;|\s*$)/i.test(response.headers.get('content-type')||''))status='incorrect_mime';
    }catch(e){status='probe_unavailable';}
    if(!settled){check();if(!settled)finish(status);}
  }
  img.alt='';img.setAttribute('aria-hidden','true');
  img.width=48;img.height=48;
  img.style.cssText='display:block;width:48px;height:48px;object-fit:contain';
  // The test is ON SCREEN. The Edge extension cannot align a decoded canvas
  // against an offscreen, transparent, zero-size or hidden image reliably.
  host.insertBefore(img,host.firstChild);
  if(typeof MutationObserver==='function'){
    observer=new MutationObserver(check);
    observer.observe(host,{subtree:true,childList:true,attributes:true,
      attributeFilter:['data-jxl-rs-edge-060','data-jxl-rs-edge-canvas','style','width','height']});
  }
  img.onload=check;
  img.onerror=check; // A native IMG error may precede a successful extension canvas.
  timer=setTimeout(function(){check();if(!settled)void inspectFailure();},22000);
  img.src=JXL_PROBE;
  check();
});}
function showJxlWarning(verdict){
  var title=element('browserCompatibilityTitle'),why=element('browserCompatibilityReason'),req=element('browserRequirement'),
      info=element('browserBasicHelp'),edge=element('browserEdgeHelp'),edgeAndroid=element('browserEdgeAndroidHelp'),chromiumHelp=element('browserChromiumHelp'),firefoxHelp=element('browserFirefoxHelp'),webkitHelp=element('browserWebkitHelp'),retry=element('browserRetry');
  if(title)title.textContent=verdict==='decoder_failed'?'JPEG XL decoder not detected':'JPEG XL could not be verified';
  if(req)req.textContent='A working JPEG XL decoder (native or compatible extension)';
  if(why)why.textContent=verdict==='incorrect_mime'?'The test image was not served with image/jxl. Check the server MIME configuration.':
    verdict==='probe_unavailable'?'The JPEG XL test image could not be loaded. Check connectivity and try again.':
    verdict==='probe_timeout'?'The JPEG XL test did not finish. Try again after checking your browser and network.':
    'The browser could not display the first-party JPEG XL test image. VulkanScope requires working JPEG XL decoding.';
  if(info)info.hidden=false;
  if(edge)edge.hidden=!(b.isEdge&&b.platform==='desktop');
  if(edgeAndroid)edgeAndroid.hidden=!(b.isEdge&&b.platform==='android');
  if(chromiumHelp)chromiumHelp.hidden=!(b.family==='chromium'&&!b.isEdge);
  if(firefoxHelp)firefoxHelp.hidden=!(b.family==='firefox');
  if(webkitHelp)webkitHelp.hidden=!(b.family==='safari');
  if(retry)retry.hidden=false;
  document.title='JPEG XL support needed - VulkanScope Database';
}
async function apply(){
  var gate=element('browserCompatibilityGate'),app=element('appRoot'),det=element('browserDetected'),req=element('browserRequirement'),why=element('browserCompatibilityReason');
  if(det)det.textContent=b.name+(b.version?' '+b.version:'')+(b.engineVersion?' · '+b.family+' '+b.engineVersion:'');
  if(!baseOK){if(why)why.textContent='This browser is missing one or more required Web Platform features, or its rendering engine is too old.';
    if(gate)gate.hidden=false;if(app)app.hidden=true;document.title='Browser not supported - VulkanScope Database';return;}
  if(gate)gate.hidden=false;if(app)app.hidden=true;
  if(req)req.textContent='JPEG XL image decoding';
  if(why)why.textContent='Checking JPEG XL rendering, including first-frame canvas output from JXL-RS Edge…';
  var verdict=await jxlProbe();window.__VULKANSCOPE_JXL_STATUS__=verdict;
  if(verdict!=='supported'){
    window.__VULKANSCOPE_COMPATIBLE__=false;showJxlWarning(verdict);return;
  }
  window.__VULKANSCOPE_COMPATIBLE__=true;
  document.documentElement.classList.add('browser-compatible');
  if(gate)gate.hidden=true;if(app)app.hidden=false;launchApp();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});else apply();
})();
