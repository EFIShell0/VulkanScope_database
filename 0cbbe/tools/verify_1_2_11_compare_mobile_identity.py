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
app=text('assets/app.v1211.js'); compat=text('assets/browser-compat.v1211.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.2.11'" in app,'frontend 1.2.11 identity missing')
need('assets/app.v1211.js?v=1211' in index and 'browser-compat.v1211.js?v=1211' in index and 'site.v0390.css?v=1211' in index,'1.2.11 cache references missing')
need('VulkanScope Database <strong>1.2.11</strong>' in index,'footer identity missing')
need(not (root/'assets/app.v1210.js').exists() and not (root/'assets/browser-compat.v1210.js').exists(),'stale 1.2.10 browser-visible bundles remain')
need("CURRENT_APP = 'app.v1211.js'" in repair and "CURRENT_BROWSER_COMPAT = 'browser-compat.v1211.js'" in repair,'repository repair current bundle identities missing')
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors changed')
# Exact failure mechanism and corrected full/mobile state.
need('.compare-identity-line{max-height:20rem;min-width:0}' in css,'full Compare identity line still lacks a non-clipping animation ceiling')
need('.compare-workspace.is-compact .compare-identity-line{max-height:0}' in css,'compact identity collapse regressed')
need('@media(max-width:760px)' in css,'narrow Compare breakpoint missing')
need('#contentView[data-main-view="compare"] .compare-identity-line{display:grid;grid-template-columns:minmax(0,1fr);gap:5px;align-items:start;min-width:0;max-width:100%}' in css,'mobile Compare identity is not intrinsic single-column')
need('#contentView[data-main-view="compare"] .compare-identity-line span{display:block;min-width:0;max-width:100%;overflow-wrap:anywhere}' in css,'mobile identity text safe wrapping missing')
need('#contentView[data-main-view="compare"] .compare-report-meta{min-width:0;max-width:100%}' in css,'Compare report meta width containment missing')
need('#contentView[data-main-view="compare"] .compare-identity-meta span{max-width:100%;overflow-wrap:anywhere}' in css,'metadata chip safe wrapping missing')
need('#contentView[data-main-view="compare"] .compare-workspace.is-compact .compare-identity-line{max-height:0}' in css,'mobile compact override does not preserve collapse')
# The identity source remains exact report evidence and unchanged in shape.
need("<span>${esc(driver)} ${esc(dv)}</span>" in app,'driver mode/version identity is no longer exact escaped report evidence')
need("compareIdentityMarkup(r,slot)" in app and 'compare-identity-line' in app and 'compare-identity-meta' in app,'Compare identity markup missing')
# 1.2.10 responsive/filter and version-emphasis behavior stays regression-protected.
need('@media(max-width:900px)' in css and '#contentView[data-main-view="compare"] .compare-filter-controls{display:grid!important;grid-template-columns:minmax(0,1fr)!important' in css,'1.2.10 Compare filter containment regressed')
need('.compare-warning .compare-version-token{color:#fff;font-weight:900}' in css,'1.2.10 Compare version emphasis regressed')
# Transport/data invariants.
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("databaseReleaseVersion:'1.2.11'" in worker and "workerReleaseVersion:'1.2.11'" in worker,'Worker release identity missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker producer-floor fixtures missing')
need('## Release 1.2.11 Compare mobile identity-flow requirements' in rules,'1.2.11 rules section missing')
need('"databaseVersion":"1.2.11"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_11_compare_mobile_identity.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_11_compare_mobile_identity_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.11','releaseReady':False,'appAsset':'assets/app.v1211.js','cacheKey':'1211'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.11 Compare mobile identity-flow contract')
