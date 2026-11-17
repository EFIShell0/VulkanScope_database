import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('../assets/browser-compat.v4008.js',import.meta.url),'utf8');
const UAS={
 samsung:'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/117.0.0.0 Mobile Safari/537.36',
 samsungDesktop:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/117.0.0.0 Safari/537.36',
 mi:'Mozilla/5.0 (Linux; Android 15; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36 XiaoMi/MiuiBrowser/14.44.1-gn',
 taptap:'Mozilla/5.0 (Linux; Android 15; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36 TapTapBrowser/4.2.3',
 edge:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36 Edg/157.0.0.0',
 edgeAndroid:'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Mobile Safari/537.36 EdgA/156.0.0.0',
 firefox:'Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0',
 floorp:'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0 Floorp/12.1.0',
 waterfox:'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0 Waterfox/6.5.0',
 oldChrome:'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.0.0 Safari/537.36',
 unknown:'CustomBrowser NotSpecified'
};
async function scenario(ua,mode='supported'){
 const ids=new Map(),timers=new Map(),children=[];let id=0;
 const el=id=>{if(!ids.has(id))ids.set(id,{id,hidden:false,textContent:''});return ids.get(id);};
 function createElement(tag){
   const e={tagName:tag.toUpperCase(),parentNode:null,style:{},naturalWidth:0,naturalHeight:0,complete:false,src:'',setAttribute(){},removeChild(c){const pos=children.indexOf(c);if(pos>=0)children.splice(pos,1);c.parentNode=null;}};
   if(tag==='img')Object.defineProperty(e,'src',{set(value){this._src=value;queueMicrotask(()=>{
     if(mode==='supported'){this.complete=true;this.naturalWidth=2;this.naturalHeight=2;this.onload?.();}
     else if(mode==='extension'){this.complete=true;this.onerror?.();queueMicrotask(()=>{this.naturalWidth=2;this.naturalHeight=2;this.onload?.();});}
     else {this.complete=true;this.onerror?.();}
   });},get(){return this._src;}});
   return e;
 }
 const doc={readyState:'complete',title:'',documentElement:{classList:{add(){}}},
   body:{appendChild(e){e.parentNode=this;children.push(e);},removeChild(e){const i=children.indexOf(e);if(i>=0)children.splice(i,1);e.parentNode=null;}},
   getElementById:el,createElement,addEventListener(){}};
 const browser={Promise,fetch:async()=>({ok:mode!=='http-fail',headers:{get:()=>mode==='mime-fail'?'text/plain':'image/jxl'}}),Map,Set,URL,URLSearchParams,AbortController,ResizeObserver:class{},requestAnimationFrame:()=>{},matchMedia:()=>{},Intl,Element:class{}};
 browser.Element.prototype.animate=function(){};browser.Element.prototype.getAnimations=function(){return[];};
 const sandbox={navigator:{userAgent:ua},window:browser,document:doc,Image:class{},Intl,Element:browser.Element,URL,Map,Set,Promise,
   fetch:browser.fetch,setTimeout(fn,delay){const key=++id;timers.set(key,{fn,delay});return key;},clearTimeout(key){timers.delete(key);},console};
 vm.runInNewContext(source,sandbox,{timeout:2000});
 await new Promise(r=>setImmediate(r));
 for(const [key,entry] of [...timers])if(entry.delay===3500||entry.delay===3000){timers.delete(key);await entry.fn();}
 await new Promise(r=>setImmediate(r));
 return {browser,doc,get:el,children};
}
for(const [name,ua,expected,engine,platform] of [
 ['samsung',UAS.samsung,'Samsung Internet',117,'android'],
 ['samsungDesktop',UAS.samsungDesktop,'Samsung Internet',117,'desktop'],
 ['mi',UAS.mi,'Mi Browser',123,'android'],
 ['taptap',UAS.taptap,'TapTap Browser',143,'android'],
 ['firefox',UAS.firefox,'Firefox',158,'desktop'],
 ['floorp',UAS.floorp,'Floorp',128,'desktop'],
 ['waterfox',UAS.waterfox,'Waterfox',140,'desktop'],
 ['edgeAndroid',UAS.edgeAndroid,'Microsoft Edge',156,'android'],
 ['edge',UAS.edge,'Microsoft Edge',157,'desktop'],
 ['unknown',UAS.unknown,'Unknown browser',0,'desktop']
 ]){
  const res=await scenario(ua);
  assert.equal(res.browser.__VULKANSCOPE_BROWSER_INFO__.name,expected,name+' browser identity');
  assert.equal(res.browser.__VULKANSCOPE_BROWSER_INFO__.engineVersion,engine,name+' engine version');
  assert.equal(res.browser.__VULKANSCOPE_BROWSER_INFO__.platform,platform,name+' platform');
  assert.equal(res.browser.__VULKANSCOPE_COMPATIBLE__,true,name+' JXL successful');
  assert.equal(res.browser.__VULKANSCOPE_JXL_STATUS__,'supported');
  assert.ok(res.children.some(e=>e.src==='./assets/app.v4008.js?v=4008'),name+' app not started');
}
const old=await scenario(UAS.oldChrome);assert.equal(old.browser.__VULKANSCOPE_COMPATIBLE__,false);assert.equal(old.browser.__VULKANSCOPE_JXL_STATUS__,'unknown');
const absent=await scenario(UAS.edge,'decode-fail');
assert.equal(absent.browser.__VULKANSCOPE_COMPATIBLE__,false);
assert.equal(absent.browser.__VULKANSCOPE_JXL_STATUS__,'decoder_failed');
assert.equal(absent.get('browserEdgeHelp').hidden,false);
assert.match(absent.get('browserCompatibilityTitle').textContent,/decoder not detected/);
assert.ok(!absent.children.some(e=>e.tagName==='SCRIPT'),'no app script on failure');
const viaExtension=await scenario(UAS.edge,'extension');
assert.equal(viaExtension.browser.__VULKANSCOPE_COMPATIBLE__,true,'Edge extension DOM image conversion should pass');
const badMime=await scenario(UAS.mi,'mime-fail');
assert.equal(badMime.browser.__VULKANSCOPE_JXL_STATUS__,'incorrect_mime');
assert.equal(badMime.get('browserEdgeHelp').hidden,true);
const badNetwork=await scenario(UAS.firefox,'http-fail');
assert.equal(badNetwork.browser.__VULKANSCOPE_JXL_STATUS__,'probe_unavailable');
const html=fs.readFileSync(new URL('../index.html',import.meta.url),'utf8');
for(const id of ['browserBasicHelp','browserEdgeHelp','browserRetry','browserCompatibilityTitle'])assert.ok(html.includes(`id="${id}"`),id);
for(const drive of ['13OnKYgF9xzU4NPGhVDbyRwztIrrUWsfP','1jZYaoQVdDumrlxEgcmaqPfMefDydQW1F'])assert.ok(html.includes(drive),drive);
console.log('PASS Browser compatibility 4.0.8: brands, engine-vs-brand, Edge DOM decoder, error states, links');
