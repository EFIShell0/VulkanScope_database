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
app=text('assets/app.v1305.js'); compat=text('assets/browser-compat.v1305.js'); boot=text('assets/release-bootstrap.v1305.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); build=text('tools/build_pages_artifact.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.3.5'" in app,'frontend identity missing')
for token in ['assets/app.v1305.js?v=1305','assets/browser-compat.v1305.js?v=1305','assets/release-bootstrap.v1305.js?v=1305','site.v0390.css?v=1305','config.js?v=1305','VulkanScope Database <strong>1.3.5</strong>']:
    need(token in index,f'index identity/reference missing: {token}')
# Submitted time-zone presentation repair.
need("const submittedZoneMarkup=zone=>" in app,'submittedZoneMarkup helper missing')
need("suffixes=['Daylight / summer offset','Standard / winter offset']" in app,'seasonal descriptor allow-list missing')
need('return `${esc(primary)}<span class="submitted-zone-season">${esc(suffix)}</span>`' in app,'seasonal second-line markup missing')
need('<span class="submitted-value submitted-zone-value">${submittedZoneMarkup(submitted.zone)}</span>' in app,'Reports time-zone row does not use structured wrapping markup')
need('.submitted-stack .submitted-zone-value{white-space:normal;overflow-wrap:anywhere;word-break:normal}' in css,'time-zone nowrap override missing')
need('.submitted-zone-season{display:block;' in css,'seasonal descriptor is not forced to a second line')
need('.submitted-stack>span:nth-child(-n+2) .submitted-value{white-space:nowrap}' in css,'Date/Time single-line contract regressed')
# Do not alter timestamp semantics.
need('const submittedParts=value=>' in app and 'submissionEpoch(value)' in app and 'temporalZoneLabel(ctx)' in app,'server timestamp presentation pipeline changed')
need('sortReports(filteredReports())' in app,'Reports sorting pipeline missing')
# Preserve 1.3.4 filter/Compare behavior.
need("scrollable=visible&&max>2" in app and "rail.classList.toggle('is-scrollable',scrollable)" in app,'1.3.4 demand-driven filter scrollbar regressed')
need("minimized?'M6 9l6 6 6-6':'M6 15l6-6 6 6'" in app,'1.3.4 Compare chevron semantics regressed')
need('.compare-workspace.is-minimized .compare-minimize-toggle svg{transform:rotate(180deg)}' not in css,'Compare state CSS rotation returned')
# Freshness and bridge.
for token in ["cache:'no-store'",'data/release.json','index.html','marker.appAsset','release-bootstrap.v${key}.js','browser-compat.v${key}.js','location.replace']:
    need(token in boot,f'freshness token missing: {token}')
for token in ["'assets/app.v1304.js'","'assets/browser-compat.v1304.js'","'assets/release-bootstrap.v1304.js'","'assets/app.v1305.js'","'assets/browser-compat.v1305.js'","'assets/release-bootstrap.v1305.js'"]:
    need(token in build,f'Pages predecessor/current bridge asset missing: {token}')
need("'assets/app.v1303.js'" not in build,'stale 1.3.3 app bridge still staged')
need("PREDECESSOR_BRIDGE = {'app.v1304.js','browser-compat.v1304.js','release-bootstrap.v1304.js'}" in repair,'repository predecessor bridge mismatch')
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor changed')
need("databaseReleaseVersion:'1.3.5'" in worker and "workerReleaseVersion:'1.3.5'" in worker,'Worker release identity mismatch')
need('## Release 1.3.5 Submitted time-zone wrapping requirements' in rules,'1.3.5 rules section missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',template)]:
    need(wf.count('python tools/verify_1_3_5_submitted_timezone_wrap.py')>=3,f'{name}: current verifier missing from release stages')
    need(wf.count('python tools/test_1_3_5_submitted_timezone_wrap_negative_mutations.py')>=3,f'{name}: negative suite missing from release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.5','releaseReady':False,'appAsset':'assets/app.v1305.js','cacheKey':'1305'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.5 Submitted time-zone wrapping contract')
