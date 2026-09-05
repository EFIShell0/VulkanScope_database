import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const source=fs.readFileSync(new URL('../assets/app.v03924.js', import.meta.url),'utf8');
const prefix=source.slice(0,source.indexOf('async function shareUrl'));
const location={origin:'https://efishell0.github.io',pathname:'/VulkanScope_database/',hash:'',search:''};
const history={
  pushState(_s,_t,url){applyUrl(url)},
  replaceState(_s,_t,url){applyUrl(url)},
};
function applyUrl(url){
  const u=new URL(url,location.origin+location.pathname);
  location.pathname=u.pathname; location.hash=u.hash; location.search=u.search;
}
const context={location,history,URLSearchParams,decodeURIComponent,setTimeout,clearTimeout,console,document:{querySelector(){return null}}};
vm.createContext(context);
vm.runInContext(prefix+';globalThis.__route={state,applyHashRoute,applyLegacyQueryRoute,stateRouteHash,routeReportHash,routeCompareUrl};',context);
const {state,applyHashRoute,stateRouteHash,routeReportHash,routeCompareUrl}=context.__route;
const A='a'.repeat(64),B='b'.repeat(64);
state.reports.set(A,{}); state.reports.set(B,{});

location.hash='#reports'; assert.equal(applyHashRoute(),true); assert.equal(state.view,'reports'); assert.equal(state.detailId,null);
location.hash='#statistics'; assert.equal(applyHashRoute(),true); assert.equal(state.view,'trends'); assert.equal(stateRouteHash(),'#statistics');
location.hash=`#reports/${A}/Properties`; assert.equal(applyHashRoute(),true); assert.equal(state.detailId,A); assert.equal(state.detailTab,'properties'); assert.equal(stateRouteHash(),`#reports/${A}/Properties`);
location.hash=`#reports/${A}`; assert.equal(applyHashRoute(),true); assert.equal(state.detailTab,'overview');
location.hash=`#reports/${A}/Display-HDR`; assert.equal(applyHashRoute(),true); assert.equal(state.detailTab,'display');
location.hash=`#reports/${A}/NotARealSection`; assert.equal(applyHashRoute(),false,'unknown report section must be rejected');
location.hash=`#reports/${A}/Properties/extra`; assert.equal(applyHashRoute(),false,'extra report route segment must be rejected');
location.hash=`#reports/${A.toUpperCase()}/Properties`; assert.equal(applyHashRoute(),false,'uppercase/non-canonical report id must be rejected');
location.hash=`#compare/${A}/${B}`; assert.equal(applyHashRoute(),true); assert.deepEqual([...state.compareIds],[A,B]);
location.hash=`#compare/${A}`; assert.equal(applyHashRoute(),false,'compare requires exactly two ids');
assert.equal(routeReportHash(A,'queues'),`#reports/${A}/Queues`);
assert.equal(routeCompareUrl([A,B]),`https://efishell0.github.io/VulkanScope_database/#compare/${A}/${B}`);
console.log('VulkanScope Database hash route contract tests: ALL PASS');
