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
app=text('assets/app.v1307.js'); compat=text('assets/browser-compat.v1307.js'); boot=text('assets/release-bootstrap.v1307.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); build=text('tools/build_pages_artifact.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); template=text('tools/pages.workflow.yml'); notice=text('licenses/browser-marks.md')
need("const DATABASE_VERSION='1.3.7'" in app,'frontend identity missing')
need("Unsupported browser for VulkanScope Database 1.3.7" in app,'frontend browser-error identity missing')
for token in ['assets/app.v1307.js?v=1307','assets/browser-compat.v1307.js?v=1307','assets/release-bootstrap.v1307.js?v=1307','site.v0390.css?v=1307','config.js?v=1307','VulkanScope Database <strong>1.3.7</strong>']:
    need(token in index,f'index identity/reference missing: {token}')
# All identities the UI can explicitly distinguish have a local same-origin brand mark.
expected={
 'Samsung Browser':'samsung-browser.v1307.svg','Microsoft Edge':'microsoft-edge.v1307.svg','Opera':'opera.v1307.svg','Vivaldi':'vivaldi.v1307.svg','Brave':'brave.v1307.svg','Firefox':'firefox.v1307.svg','Google Chrome':'google-chrome.v1307.svg','Chromium':'chromium.v1307.png','Safari':'safari.v1307.svg'}
need('const BROWSER_LOGO_ASSETS={' in app,'browser logo map missing')
for name,file in expected.items():
    need(f"'{name}':'./assets/browser-logos/{file}'" in app,f'logo map missing {name}')
    p=root/'assets/browser-logos'/file
    need(p.is_file(),f'logo asset missing {file}')
    if p.is_file():
        need(p.stat().st_size>250,f'logo asset suspiciously empty {file}')
        if p.suffix=='.svg':
            raw=p.read_text(encoding='utf-8')
            need('<svg' in raw and '</svg>' in raw,f'invalid svg wrapper {file}')
            need('<script' not in raw.lower() and 'javascript:' not in raw.lower(),f'active content forbidden in logo {file}')
            need(not re.search(r'(?:href|xlink:href)=[\"\']https?://|url\(https?://',raw,re.I),f'external resource forbidden in logo {file}')
# Preserve original-color artwork: images are not CSS-tinted and the wrapper is neutral.
need('.settings-browser-logo{display:block;width:32px;height:32px;max-width:32px;max-height:32px;object-fit:contain;filter:none!important;opacity:1}' in css,'browser logo CSS must preserve intrinsic sizing/color without filtering')
need('.settings-browser-icon{overflow:hidden;background:rgba(255,255,255,.045);color:#aeb2bd}' in css,'neutral browser mark container missing')
need('browserLogoAsset(b.name)' in app and 'class="settings-browser-logo"' in app,'local logo rendering path missing')
need('Browser marks are bundled with VulkanScope Database and are never fetched from a third-party logo service.' in app,'local-only logo disclosure missing')
need("'Chromium-based browser':'./assets/browser-logos/" not in app,'generic Chromium-family fallback must not be assigned a Chromium trademark')
# Detection is best-effort/local only. Brave and Vivaldi are recognized only from exposed browser signals.
need("const braveDetected=!!navigator.brave||brandEntries.some" in app,'Brave exposed-signal detection missing')
need("['Vivaldi',/Vivaldi\\/" in app,'Vivaldi UA token detection missing')
need("['Samsung Browser',/SamsungBrowser\\/" in app,'Samsung Browser current-name detection missing')
need("['Samsung Internet'" not in app[app.find('function browserIdentity'):app.find('function renderBrowserInfo')],'obsolete Samsung display name remains in identity rules')
need('canvas.toDataURL' not in app and 'WEBGL_debug_renderer_info' not in app,'fingerprinting primitive introduced')
need('logo CDN' not in app or 'third-party logo service' in app,'unexpected logo-service behavior')
# Provenance/trademark note is public/local and explicit.
for token in ['Google Chrome: https://about.google/brand-resource-center/products-and-services/','Chromium: https://chromium.googlesource.com/','Mozilla Firefox: https://www.mozilla.org/','Apple Safari: https://support.apple.com/safari','Opera Browser: https://brand.opera.com/','Brave: https://brave.com/brave-branding-assets/','Vivaldi: https://vivaldi.com/press/','Samsung Browser: https://developer.samsung.com/']:
    need(token in notice,f'official brand provenance missing: {token}')
need('does not imply affiliation, sponsorship, endorsement' in notice,'trademark non-affiliation note missing')
need("license_files=['wrangler.md','sharp.md','esbuild.md','workerd.md','nodejs.md','python.md','browser-marks.md']" in build,'browser mark notice is not staged')
for file in expected.values(): need(f"'assets/browser-logos/{file}'" in build,f'Pages staging missing {file}')
# Preserve 1.3.6 redesign/raw-report and 1.3.5/1.3.4 requested fixes.
need('const DETAIL_TAB_META={' in app and 'id="downloadRawReport"' in app and "new Blob([text],{type:'text/plain;charset=utf-8'})" in app,'1.3.6 report-detail/raw download contract regressed')
need('const submittedZoneMarkup=zone=>' in app and '.submitted-stack .submitted-zone-value{white-space:normal' in css,'1.3.5 timezone wrapping regressed')
need("minimized?'M6 9l6 6 6-6':'M6 15l6-6 6 6'" in app,'1.3.4 Compare chevron semantics regressed')
need("scrollable=visible&&max>2" in app,'1.3.4 demand-driven scrollbar regressed')
# Release bridge/current identity.
for token in ["'assets/app.v1306.js'","'assets/browser-compat.v1306.js'","'assets/release-bootstrap.v1306.js'","'assets/app.v1307.js'","'assets/browser-compat.v1307.js'","'assets/release-bootstrap.v1307.js'"]:
    need(token in build,f'Pages predecessor/current bridge missing: {token}')
need("'assets/app.v1305.js'" not in build,'stale 1.3.5 app bridge still staged')
need("PREDECESSOR_BRIDGE = {'app.v1306.js','browser-compat.v1306.js','release-bootstrap.v1306.js'}" in repair,'repository predecessor bridge mismatch')
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floors changed')
need("databaseReleaseVersion:'1.3.7'" in worker and "workerReleaseVersion:'1.3.7'" in worker,'Worker release identity mismatch')
need("const LOCAL='1.3.7'" in boot,'release bootstrap identity mismatch')
need('## Release 1.3.7 browser brand-mark requirements' in rules,'1.3.7 rules section missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',template)]:
    need(wf.count('python tools/verify_1_3_7_browser_brand_marks.py')>=3,f'{name}: current verifier missing from release stages')
    need(wf.count('python tools/test_1_3_7_browser_brand_marks_negative_mutations.py')>=3,f'{name}: negative suite missing from release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.7','releaseReady':False,'appAsset':'assets/app.v1307.js','cacheKey':'1307'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.7 local browser brand-mark contract')
