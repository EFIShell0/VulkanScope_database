import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('../assets/browser-compat.v4009.js',import.meta.url),'utf8');
const UAS={
 samsung:'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/117.0.0.0 Mobile Safari/537.36',
 mi:'Mozilla/5.0 (Linux; Android 15; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36 XiaoMi/MiuiBrowser/14.44.1-gn',
 taptap:'Mozilla/5.0 (Linux; Android 15; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36 TapTapBrowser/4.2.3',
 edge:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36 Edg/157.0.0.0',
 edgeAndroid:'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Mobile Safari/537.36 EdgA/157.0.0.0',
 firefox:'Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0',
 waterfox:'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0 Waterfox/6.5.0',
 oldChrome:'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.0.0 Safari/537.36'
};
async function scenario(ua,mode='native'){
 const ids=new Map(),timers=new Map(),scripts=[];let id=0,observer=null,canvas=null,probeImg=null;
 const el=id=>{if(!ids.has(id))ids.set(id,{id,hidden:false,textContent:''});return ids.get(id);};
 const host={children:[],firstChild:null,insertBefore(e,before){const ix=this.children.indexOf(before);if(ix<0)this.children.push(e);else this.children.splice(ix,0,e);e.parentElement=this;e.parentNode=this;e.isConnected=true;this.firstChild=this.children[0]||null;this._siblings();},
   removeChild(e){const ix=this.children.indexOf(e);if(ix>=0)this.children.splice(ix,1);e.isConnected=false;e.parentElement=null;e.parentNode=null;this.firstChild=this.children[0]||null;this._siblings();},
   _siblings(){for(let i=0;i<this.children.length;i++)this.children[i].previousElementSibling=this.children[i-1]||null;}};
 const span={localName:'span'};host.insertBefore(span,null);
 function make(tag){const e={tagName:tag.toUpperCase(),localName:tag,parentNode:null,parentElement:null,isConnected:false,
    previousElementSibling:null,style:{cssText:''},width:tag==='canvas'?2:0,height:tag==='canvas'?2:0,naturalWidth:0,naturalHeight:0,complete:false,attrs:{},
    setAttribute(k,v){this.attrs[k]=String(v);},getAttribute(k){return this.attrs[k]||null;},hasAttribute(k){return Object.hasOwn(this.attrs,k);},
    getBoundingClientRect(){return {width:tag==='canvas'?48:48,height:tag==='canvas'?48:48};}};
  if(tag==='img'){
   probeImg=e;
   Object.defineProperty(e,'src',{get(){return this._src;},set(v){this._src=v;queueMicrotask(()=>{
    if(mode==='native'){e.complete=true;e.naturalWidth=2;e.naturalHeight=2;e.onload?.();}
    else if(mode==='extension'||mode==='pending'||mode==='hidden-canvas'||mode==='unrelated-canvas'){
     e.complete=true;e.onerror?.();canvas=make('canvas');canvas.setAttribute('data-jxl-rs-edge-canvas','');
     canvas._visible=mode!=='hidden-canvas';host.insertBefore(canvas,e);
     e.setAttribute('data-jxl-rs-edge-060',mode==='pending'?'pending':'released');
     if(mode==='unrelated-canvas')canvas.attrs={};
     observer?.callback();
    }else {e.complete=true;e.onerror?.();}
   });}});
  }
  return e;
 }
 const body={appendChild(e){scripts.push(e);e.parentNode=this;},removeChild(e){scripts.splice(scripts.indexOf(e),1);e.parentNode=null;}};
 class Observer{constructor(callback){this.callback=callback;observer=this;}observe(){}disconnect(){}}
 const doc={readyState:'complete',title:'',baseURI:'https://example.test/index.html',documentElement:{classList:{add(){}}},body,
   getElementById(k){return k==='browserJxlProbeHost'?host:el(k);},createElement:make,addEventListener(){}};
 const browser={Promise,fetch:async()=>({ok:mode!=='http-fail',headers:{get:()=>mode==='mime-fail'?'text/plain':'image/jxl'}}),Map,Set,URL,URLSearchParams,
  AbortController,ResizeObserver:class{},requestAnimationFrame(){},matchMedia(){},Intl,Element:class{}};
 browser.Element.prototype.animate=function(){};browser.Element.prototype.getAnimations=function(){return[];};
 const sandbox={navigator:{userAgent:ua},window:browser,document:doc,MutationObserver:Observer,getComputedStyle:e=>({
  display:'block',visibility:e._visible===false?'hidden':'visible',opacity:'1'}),
  Element:browser.Element,Intl,URL,Promise,Map,Set,Image:class{},fetch:browser.fetch,
  setTimeout(fn,delay){const key=++id;timers.set(key,{fn,delay});return key;},clearTimeout(key){timers.delete(key);},console};
 vm.runInNewContext(source,sandbox,{timeout:3000});
 await new Promise(r=>setImmediate(r));
 for(const [key,t] of [...timers])if(t.delay===22000){timers.delete(key);await t.fn();}
 await new Promise(r=>setImmediate(r));
 return {browser,doc,element:el,host,scripts,canvas,probeImg};
}
for(const [name,ua,expected,engine,platform] of [
 ['samsung',UAS.samsung,'Samsung Internet',117,'android'],
 ['mi',UAS.mi,'Mi Browser',123,'android'],
 ['taptap',UAS.taptap,'TapTap Browser',143,'android'],
 ['firefox',UAS.firefox,'Firefox',158,'desktop'],
 ['waterfox',UAS.waterfox,'Waterfox',140,'desktop'],
 ['edgeAndroid',UAS.edgeAndroid,'Microsoft Edge',157,'android'],
 ['edge',UAS.edge,'Microsoft Edge',157,'desktop']
]){
 const r=await scenario(ua);
 assert.equal(r.browser.__VULKANSCOPE_BROWSER_INFO__.name,expected,name+' browser');
 assert.equal(r.browser.__VULKANSCOPE_BROWSER_INFO__.engineVersion,engine,name+' engine');
 assert.equal(r.browser.__VULKANSCOPE_BROWSER_INFO__.platform,platform,name+' platform');
 assert.equal(r.browser.__VULKANSCOPE_COMPATIBLE__,true,name+' native should pass');
 assert.equal(r.browser.__VULKANSCOPE_JXL_METHOD__,'native',name+' proof path');
 assert.ok(r.scripts.some(e=>e.src==='./assets/app.v4009.js?v=4009'),name+' app script');
}
for(const mode of ['extension']){
 const r=await scenario(UAS.edge,mode);
 assert.equal(r.browser.__VULKANSCOPE_COMPATIBLE__,true,mode+' first frame canvas must pass');
 assert.equal(r.browser.__VULKANSCOPE_JXL_METHOD__,'jxl-rs-edge-canvas');
 assert.ok(r.scripts.some(e=>e.src==='./assets/app.v4009.js?v=4009'),'app started after extension paint');
}
for(const mode of ['pending','hidden-canvas','unrelated-canvas','decoder-fail']){
 const r=await scenario(UAS.edge,mode);
 assert.equal(r.browser.__VULKANSCOPE_COMPATIBLE__,false,mode+' should fail closed');
 assert.equal(r.browser.__VULKANSCOPE_JXL_METHOD__,'none',mode+' must not infer decode');
 assert.equal(r.browser.__VULKANSCOPE_JXL_STATUS__,'decoder_failed');
 assert.equal(r.element('browserEdgeHelp').hidden,false);
 assert.ok(!r.scripts.some(e=>e.localName==='script'));
}
for(const [mode,result] of [['mime-fail','incorrect_mime'],['http-fail','probe_unavailable']]){
 const r=await scenario(UAS.edge,mode);assert.equal(r.browser.__VULKANSCOPE_JXL_STATUS__,result);
}
const old=await scenario(UAS.oldChrome);assert.equal(old.browser.__VULKANSCOPE_COMPATIBLE__,false);assert.equal(old.browser.__VULKANSCOPE_JXL_STATUS__,'unknown');
const html=fs.readFileSync(new URL('../index.html',import.meta.url),'utf8');
assert.ok(html.includes('id="browserJxlProbeHost"'));for(const drive of ['13OnKYgF9xzU4NPGhVDbyRwztIrrUWsfP','1jZYaoQVdDumrlxEgcmaqPfMefDydQW1F'])assert.ok(html.includes(drive));
console.log('PASS 4.0.9 browser JXL: real native IMG; JXL-RS Edge released visible canvas; pending/hidden/false overlays rejected; proper failure diagnostics');
