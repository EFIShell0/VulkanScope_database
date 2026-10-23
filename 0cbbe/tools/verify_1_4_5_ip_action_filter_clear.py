from __future__ import annotations
from pathlib import Path
import argparse, json, sys
ap=argparse.ArgumentParser(); ap.add_argument('--root',default=None); a=ap.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
index=text('index.html'); app=text('assets/app.v1405.js'); css=text('assets/site.v1405.css'); worker=text('worker/src/index.js'); rules=text('rules/PROJECT_RULES.md')
try: marker=json.loads(text('data/release.json'))
except Exception as e: marker={}; errors.append(f'invalid release marker: {e}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.4.5','releaseReady':False,'appAsset':'assets/app.v1405.js','cacheKey':'1405'},'1.4.5 release marker mismatch')
for token in ['./assets/site.v1405.css?v=1405','./assets/release-bootstrap.v1405.js?v=1405','./assets/browser-compat.v1405.js?v=1405','./assets/app.v1405.js?v=1405','VulkanScope Database <strong>1.4.5</strong>']:
    need(token in index,f'current frontend identity missing: {token}')
need("const DATABASE_VERSION='1.4.5'" in app,'frontend Database version mismatch')
for token in ["databaseReleaseVersion:'1.4.5'","workerReleaseVersion:'1.4.5'"]:
    need(worker.count(token)>=3,f'Worker 1.4.5 release metadata missing: {token}')

# Address privacy remains independent, but the address surface itself is no longer an action.
need('const networkAddressReveal={active:false,ipv4:false,ipv6:false,pseudo:false};' in app,'independent address reveal slots missing')
need('return`<span class="network-address-toggle ${revealed?' in app,'address privacy shell is not a non-interactive span')
need('<button class="network-address-toggle' not in app,'entire IP address shell is still a clickable button')
need('<button class="network-address-action" type="button" data-network-address-toggle="${esc(key)}"' in app,'dedicated Show/Hide button missing')
need("const shell=button.closest('.network-address-toggle');shell?.classList.toggle('is-revealed',!!revealed)" in app,'Show/Hide action does not update its privacy shell')
need('can be revealed only with the Show/Hide button; the address surface itself is not interactive.' in app,'Internet help text still tells users to click the address surface')
need('.network-address-toggle{cursor:default}' in css,'address shell does not advertise non-interactive cursor state')
need('.network-address-action{appearance:none;-webkit-appearance:none;border:1px solid transparent;cursor:pointer' in css,'Show/Hide button is not the explicit pointer target')
need('.network-address-action:hover{' in css and '.network-address-action:active{' in css and '.network-address-action:focus-visible{' in css,'Show/Hide smooth hover/press/focus treatment missing')
need('@media(prefers-reduced-motion:reduce){.network-address-action,.custom-select-search-clear{transition:none!important}' in css,'reduced-motion action/clear parity missing')

# Every enhanced searchable filter gets the shared local X clear control.
need("clearSearch.className='search-clear-button custom-select-search-clear is-hidden'" in app,'custom-filter search clear button missing')
need("clearSearch.setAttribute('aria-hidden','true');clearSearch.tabIndex=-1" in app,'custom-filter clear starts hidden/non-tabbable')
need("const syncSearchClear=()=>{const hidden=!search.value;clearSearch.classList.toggle('is-hidden',hidden)" in app,'custom-filter clear visibility is not query-driven')
need("clearSearch.onclick=e=>{e.preventDefault();e.stopPropagation();if(!search.value)return;search.value='';syncSearchClear();optionPage=1;renderOptions({resetScroll:true});search.focus({preventScroll:true})}" in app,'custom-filter clear does not atomically clear/reset/focus')
need("search.addEventListener('input',syncSearchClear);syncSearchClear();menu.appendChild(searchShell)" in app,'custom-filter clear is not synchronized while typing')
need("search.dispatchEvent(new Event('input',{bubbles:false}))" in app,'filter reopen/reset does not resynchronize clear visibility')
# Existing row/global/reference searches must keep the same local clear-control language.
need('const textControl=(id,label,value,placeholder=' in app and 'data-search-clear="${esc(id)}"' in app,'row-filter clear controls regressed')
need("bindSearchClear($('#globalSearch'),$('#globalSearchClear'))" in app,'global search clear control regressed')
need("bindSearchClear(search,$('#encyclopediaSearchClear'))" in app,'Encyclopedia search clear control regressed')
need('input[type="search"]::-webkit-search-cancel-button{-webkit-appearance:none;appearance:none;display:none}' in css,'browser-native inconsistent search cancel glyph is not suppressed')
need('.search-clear-button{' in css and 'transition:opacity .18s ease,transform .18s cubic-bezier(.2,.8,.2,1)' in css,'shared clear button smooth transition missing')
need('.custom-select-search-clear{width:30px;flex:0 0 30px' in css and '.custom-select-search-clear.is-hidden{width:0;flex-basis:0' in css,'custom-filter clear enter/exit geometry animation missing')

# Preserve 1.4.4 fixed viewport chrome repair.
need('@keyframes startupShellReveal{from{opacity:0}to{opacity:1}}' in css,'opacity-only startup reveal regressed')
need('.page-progress{position:fixed;inset:0 0 auto 0;height:3px;z-index:230;' in css,'fixed top page progress regressed')
need('.viewport-scrollbar{position:fixed;z-index:220;top:0;right:0;bottom:0;width:18px;' in css,'fixed viewport scrollbar regressed')

# Release boundary / immediate predecessor bridge.
need('## Release 1.4.5 action-only address reveal / filter-search clear requirements' in rules,'1.4.5 project-rules section missing')
need("PREDECESSOR_BRIDGE = {'app.v1404.js','browser-compat.v1404.js','release-bootstrap.v1404.js'}" in text('tools/repair_repository.py'),'1.4.5 predecessor bridge mismatch')
pages=text('tools/build_pages_artifact.py')
need("'assets/app.v1404.js'" in pages and "'assets/app.v1405.js'" in pages and "'assets/app.v1403.js'" not in pages,'Pages predecessor/current app bridge mismatch')
need("'assets/site.v1404.css'" in pages and "'assets/site.v1405.css'" in pages,'Pages current stylesheet assets missing')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); sys.exit(1)
print('PASS Database 1.4.5 action-only IP reveal + filter-search clear contract')
