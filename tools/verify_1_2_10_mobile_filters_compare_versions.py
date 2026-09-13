from pathlib import Path
import argparse,json
parser=argparse.ArgumentParser(); parser.add_argument('--root',default=None); args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
app=text('assets/app.v1210.js'); compat=text('assets/browser-compat.v1210.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py')
workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml'); repair=text('tools/repair_repository.py')
# Release/cache identity and stale-asset prevention.
need("const DATABASE_VERSION='1.2.10'" in app,'frontend 1.2.10 identity missing')
need('assets/app.v1210.js?v=1210' in index and 'browser-compat.v1210.js?v=1210' in index and 'site.v0390.css?v=1210' in index,'1.2.10 cache references missing')
need('VulkanScope Database <strong>1.2.10</strong>' in index,'footer identity missing')
need(not (root/'assets/app.v1209.js').exists() and not (root/'assets/browser-compat.v1209.js').exists(),'stale predecessor browser assets remain in successor tree')
need("CURRENT_APP = 'app.v1210.js'" in repair and "CURRENT_BROWSER_COMPAT = 'browser-compat.v1210.js'" in repair,'repository repair current bundle identities missing')
need('def stale_apps()' in repair and 'for p in stale_apps():' in repair,'repository repair does not clean stale app bundles')
need('def stale_browser_compats()' in repair and 'for p in stale_browser_compats():' in repair,'repository repair does not clean stale browser bundles')
need('"databaseVersion":"1.2.10"' in text('data/release.json').replace(' ',''),'release marker version missing')
need('"databaseVersion":"1.2.10"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_10_mobile_filters_compare_versions.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_10_mobile_filters_compare_versions_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
# Browser compatibility floors remain unchanged.
need('<section id="browserCompatibilityGate" class="browser-compatibility-gate" role="main" hidden>' in index,'compatibility gate is not parse-time hidden')
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors changed')
# Reports path remains, while all non-Reports filter workspaces gain earlier intrinsic containment.
need('#contentView[data-main-view="reports"] #filters{display:grid;grid-template-columns:minmax(0,1fr)' in css,'Reports 1.2.9 mobile containment regressed')
nonreports='#contentView[data-main-view]:not([data-main-view="reports"]):not([data-main-view="encyclopedia"]) #filters{display:grid!important;grid-template-columns:minmax(0,1fr)!important'
need('.compare-warning .compare-version-token{color:#fff;font-weight:900}\n@media(max-width:900px){\n  '+nonreports in css,'non-Reports <=900px single-column global-filter containment missing')
need('#filters>.filter-family' in css and 'min-width:0!important;width:100%!important;max-width:100%!important' in css,'non-Reports filter-family width containment missing')
need('.filter-family-controls{display:grid!important;grid-template-columns:minmax(0,1fr)!important' in css,'non-Reports family control single-column layout missing')
need('.filter-family-controls>.custom-select' in css and '.filter-family-controls>select' in css and 'flex:none!important' in css,'enhanced/native filter control width containment missing')
need('#contentView[data-main-view]:not([data-main-view="reports"]) .subfilters{display:grid!important;grid-template-columns:minmax(0,1fr)!important' in css,'non-Reports view-specific subfilter containment missing')
need('#contentView[data-main-view="compare"] .compare-filter-controls{display:grid!important;grid-template-columns:minmax(0,1fr)!important' in css,'Compare evidence-filter mobile containment missing')
# Cross-producer version values are escaped and highlighted without changing comparison identity logic.
need('crossProducer=producerA!==producerB||codeA!==codeB' in app,'cross-producer identity comparison changed')
need(app.count('class="compare-version-token"')==2,'both compared producer versions are not wrapped exactly once')
need('<strong class="compare-version-token">${esc(producerA)}${codeA?' in app and '<strong class="compare-version-token">${esc(producerB)}${codeB?' in app,'Compare version emphasis is not applied to escaped producer values')
need('.compare-warning .compare-version-token{color:#fff;font-weight:900}' in css,'bold white Compare version style missing')
# Immutable transport/data semantics.
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker producer-floor fixtures missing')
need("databaseReleaseVersion:'1.2.10'" in worker and "workerReleaseVersion:'1.2.10'" in worker,'Worker release identity missing')
need('## Release 1.2.10 non-Reports mobile filters / Compare version-emphasis requirements' in rules,'1.2.10 rules section missing')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.10','releaseReady':False,'appAsset':'assets/app.v1210.js','cacheKey':'1210'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.10 mobile-filter / Compare-version contract')
