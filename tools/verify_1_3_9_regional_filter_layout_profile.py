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
app=text('assets/app.v1309.js'); compat=text('assets/browser-compat.v1309.js'); boot=text('assets/release-bootstrap.v1309.js'); css=text('assets/site.v1309.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); build=text('tools/build_pages_artifact.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.3.9'" in app,'frontend release identity missing')
need("Unsupported browser for VulkanScope Database 1.3.9" in app,'frontend browser-error identity missing')
for token in ['assets/app.v1309.js?v=1309','assets/browser-compat.v1309.js?v=1309','assets/release-bootstrap.v1309.js?v=1309','site.v1309.css?v=1309','config.js?v=1309','VulkanScope Database <strong>1.3.9</strong>']:
    need(token in index,f'index identity/reference missing: {token}')
# Regional lock matrix and locale ownership.
need("const enabled=mode==='country'?id==='settingsRegionalCountry':mode==='manual'?id!=='settingsRegionalCountry':false" in app,'Automatic/Country/Manual lock matrix mismatch')
need("else if(state.regionalMode==='manual')state.regionalCountry='auto'" in app,'Manual mode does not clear country override')
need("if(mode==='auto'||mode==='manual')return browserLanguage()" in app,'Manual locale is still country-derived')
need('Manual keeps Country / region locked' in index and 'Automatic and Manual use the browser/system region' in index,'regional settings explanatory copy mismatch')
# Country profile is explicit and separate.
for token in ['const countryRegionalProfile=','const regionalDatePattern=','const regionalClockProfile=',"regionalProfileRow('Date format'","regionalProfileRow('Clock format'","regionalProfileRow('Representative IANA zone'","regionalProfileRow('Current UTC offset'","regionalProfileRow('Standard / winter offset'","regionalProfileRow('Daylight / summer offset'","regionalProfileRow('Seasonal clock change'","regionalProfileRow('Current offset state'"]:
    need(token in app,f'country profile field/helper missing: {token}')
need('new Intl.DateTimeFormat(locale,{year:\'numeric\',month:\'2-digit\',day:\'2-digit\'' in app,'date pattern is not derived through Intl')
need("new Intl.DateTimeFormat(locale,{hour:'numeric'}).resolvedOptions()" in app,'clock convention is not derived through Intl')
# Country coverage map must cover every declared country code.
cm=re.search(r"const COUNTRY_CODES=Object\.freeze\('([^']+)'\.split\(','\)\);",app)
zm=re.search(r'const COUNTRY_PRIMARY_TIME_ZONES=Object\.freeze\((\{.*?\})\);',app)
if cm and zm:
    codes=set(cm.group(1).split(','))
    try: zones=json.loads(zm.group(1))
    except Exception as exc: zones={}; errors.append(f'country timezone map is not JSON-compatible: {exc}')
    need(len(codes)==250,f'expected 250 country/region codes, found {len(codes)}')
    need(codes==set(zones),f'representative timezone map coverage mismatch missing={sorted(codes-set(zones))[:8]} extra={sorted(set(zones)-codes)[:8]}')
else:
    errors.append('country code/timezone map declarations missing')
# Layout: no permanent gutter, complete wrapped labels, full-width regional controls.
need("host.classList.toggle('has-surface-scrollbar',scrollable)" in app and "parent.classList.toggle('has-surface-scrollbar',scrollable)" in app,'surface scrollbar does not expose real-overflow class')
need('.custom-select-scroll{padding-right:0!important}' in css,'short custom selects still reserve scrollbar gutter')
need('.custom-select-scroll.has-surface-scrollbar{padding-right:23px!important}' in css,'overflowing custom-select rail gutter missing')
need('.settings-regional-group .settings-select-row{grid-template-columns:minmax(0,1fr)!important' in css,'regional settings are still split into narrow columns')
need('.settings-regional-choice .filter-choice-label' in css and 'overflow-wrap:normal!important' in css,'regional labels may still split normal words')
need('.custom-select-option .filter-choice-label' in css and 'white-space:normal!important' in css and 'overflow-wrap:anywhere!important' in css,'filter option labels are still clipped')
need("regional=String(sel?.id||'').startsWith('settingsRegional')" in app and "${regional?'':filterIconSvg(filterIconKey(sel,opt))}" in app,'regional selects still waste width on generic filter icons')
# Presentation-only timestamp integrity and release wiring.
need('const submissionEpoch=value=>' in app and "Date.parse(String(value||''))" in app,'server timestamp epoch path regressed')
need('## Release 1.3.9 regional-control fit / country-profile / filter-gutter requirements' in rules,'1.3.9 rules section missing')
need("databaseReleaseVersion:'1.3.9'" in worker and "workerReleaseVersion:'1.3.9'" in worker,'Worker release identity mismatch')
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor changed')
need("PREDECESSOR_BRIDGE = {'app.v1308.js','browser-compat.v1308.js','release-bootstrap.v1308.js'}" in repair,'repository predecessor bridge mismatch')
need("'assets/app.v1308.js'" in build and "'assets/app.v1309.js'" in build and "'assets/app.v1307.js'" not in build,'Pages immediate predecessor/current app bridge mismatch')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',template)]:
    need(wf.count('python tools/verify_1_3_9_regional_filter_layout_profile.py')>=3,f'{name}: current verifier missing from release stages')
    need(wf.count('python tools/test_1_3_9_regional_filter_layout_profile_negative_mutations.py')>=3,f'{name}: negative suite missing from release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.9','releaseReady':False,'appAsset':'assets/app.v1309.js','cacheKey':'1309'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.9 regional/filter layout profile contract')
