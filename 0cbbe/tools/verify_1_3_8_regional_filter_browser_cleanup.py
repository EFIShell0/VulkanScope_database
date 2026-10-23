from pathlib import Path
import argparse,json,re
parser=argparse.ArgumentParser(); parser.add_argument('--root',default=None); args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
app=text('assets/app.v1308.js'); compat=text('assets/browser-compat.v1308.js'); boot=text('assets/release-bootstrap.v1308.js'); css=text('assets/site.v1308.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); build=text('tools/build_pages_artifact.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.3.8'" in app,'frontend release identity missing')
need("Unsupported browser for VulkanScope Database 1.3.8" in app,'frontend browser-error identity missing')
for token in ['assets/app.v1308.js?v=1308','assets/browser-compat.v1308.js?v=1308','assets/release-bootstrap.v1308.js?v=1308','site.v1308.css?v=1308','config.js?v=1308','VulkanScope Database <strong>1.3.8</strong>']:
    need(token in index,f'index identity/reference missing: {token}')
# Browser information current UI is text-only: no mark map, host, or current-app logo reference.
for token in ['const BROWSER_LOGO_ASSETS=','browserLogoAsset(','class="settings-browser-icon"','class="settings-browser-logo"','assets/browser-logos/']:
    need(token not in app,f'current browser UI still contains logo/icon token: {token}')
need('settings-browser-summary settings-browser-summary-text' in app,'text-only browser summary missing')
need('No browser logo, icon, favicon service or browser-brand image is displayed or loaded.' in app,'browser text-only privacy disclosure missing')
# Immediate predecessor assets may remain as cache bridge but current app/index may not reference them.
need('browser-logos' not in index,'current index unexpectedly references browser-logo assets')
# Long filter/select labels wrap and disabled native selects are authoritative.
for token in ['.custom-select-button .filter-choice-label,.custom-select-option .filter-choice-label','white-space:normal!important','overflow-wrap:anywhere','.custom-select.is-disabled .custom-select-button']:
    need(token in css,f'filter wrapping/disabled CSS missing: {token}')
need("btn.disabled=disabled" in app and "wrap.classList.toggle('is-disabled',disabled)" in app,'custom select does not mirror native disabled state')
need("const open=()=>{if(sel.disabled)return;" in app,'disabled custom select can still open')
# One-page page jump must be wholly inert, not just Go/Previous/Next.
need("single=max<=1" in app,'single-page pagination state missing')
need("jump.classList.toggle('is-single-page',single)" in app,'single-page page-jump state missing')
need('input.disabled=single' in app and 'input.tabIndex=single?-1:0' in app,'one-page jump input is still interactive/focusable')
need("go.tabIndex=single?-1:0" in app and "go.setAttribute('aria-disabled',go.disabled?'true':'false')" in app,'one-page jump Go state incomplete')
need('.page-jump.is-single-page .page-jump-input' in css and 'pointer-events:none!important' in css,'one-page page jump pointer guard missing')
# Regional mode UI/state contract.
need('id="settingsRegionalMode"' in index,'regional mode control missing')
for token in ['Automatic (browser / system)','<option value="country">Country</option>','<option value="manual">Manual</option>']:
    need(token in index,f'regional mode option missing: {token}')
need("REGIONAL_MODES=new Set(['auto','country','manual'])" in app,'regional mode state vocabulary missing')
need("regionalMode:'auto'" in app,'Automatic is not the default regional mode')
need('const browserLanguage=()=>{const raw=String(navigator.languages?.[0]||navigator.language' in app,'Automatic mode does not source browser/system language')
need("const browserTimeZone=()=>{try{return Intl.DateTimeFormat().resolvedOptions().timeZone||'UTC'}" in app,'Automatic mode does not source browser/system time zone')
need('const COUNTRY_PRIMARY_TIME_ZONES=Object.freeze(' in app,'Country representative IANA timezone map missing')
need("if(mode==='country')return countryPrimaryTimeZone(effectiveCountryCode())" in app,'Country mode does not derive its time zone from country')
need("new Intl.Locale(`und-${cc}`).maximize().language" in app,'Country mode does not derive country-local regional conventions')
need("const effectiveRegionalDateFormat=()=>effectiveRegionalMode()==='manual'?state.regionalDateFormat:'auto'" in app,'Date-format override leaks outside Manual mode')
need("const effectiveRegionalClock=()=>effectiveRegionalMode()==='manual'?state.regionalClock:'auto'" in app,'Clock override leaks outside Manual mode')
need("const effectiveRegionalSeason=()=>effectiveRegionalMode()==='manual'?state.regionalSeason:'auto'" in app,'Season override leaks outside Manual mode')
need("const enabled=mode==='manual'||(mode==='country'&&id==='settingsRegionalCountry')" in app,'regional control lock matrix is wrong')
need("if(key==='regionalMode'&&state.regionalMode==='country'&&state.regionalCountry==='auto'&&browserRegion())state.regionalCountry=browserRegion()" in app,'Country mode does not seed detected country when available')
# Presentation-only integrity: stored timestamp parsing/sorting remains epoch-based; no migration added.
need('const submissionEpoch=value=>' in app and 'Date.parse(String(value||\'\'))' in app,'server timestamp epoch path regressed')
need('## Release 1.3.8 filter / regional-mode / browser-cleanup requirements' in rules,'1.3.8 rules section missing')
need("databaseReleaseVersion:'1.3.8'" in worker and "workerReleaseVersion:'1.3.8'" in worker,'Worker release identity mismatch')
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor changed')
need("PREDECESSOR_BRIDGE = {'app.v1307.js','browser-compat.v1307.js','release-bootstrap.v1307.js'}" in repair,'repository predecessor bridge mismatch')
need("'assets/app.v1307.js'" in build and "'assets/app.v1308.js'" in build,'Pages predecessor/current app bridge mismatch')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',template)]:
    need(wf.count('python tools/verify_1_3_8_regional_filter_browser_cleanup.py')>=3,f'{name}: current verifier missing from release stages')
    need(wf.count('python tools/test_1_3_8_regional_filter_browser_cleanup_negative_mutations.py')>=3,f'{name}: negative suite missing from release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.8','releaseReady':False,'appAsset':'assets/app.v1308.js','cacheKey':'1308'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.8 filter / regional-mode / browser-cleanup contract')
