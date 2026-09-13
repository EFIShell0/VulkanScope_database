from __future__ import annotations
from pathlib import Path
import argparse,re,sys

parser=argparse.ArgumentParser()
parser.add_argument('--root',default=None)
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')

app=text('assets/app.v1025.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md')
need("const DATABASE_VERSION='1.0.25',LIVE_SYNC_INTERVAL_MS=3000,RELEASE_CHECK_INTERVAL_MS=10000,NETWORK_INFO_INTERVAL_MS=3000,NETWORK_PROBE_TIMEOUT_MS=2200;" in app,'1.0.25 frontend identity/timers missing')
need('assets/app.v1025.js?v=1025' in index and 'site.v0390.css?v=1025' in index and 'config.js?v=1025' in index,'1.0.25 cache-busted index references missing')
need('VulkanScope Database <strong>1.0.25</strong>' in index,'1.0.25 footer identity missing')

# Connectivity and live Internet observation.
need("restored:{title:'Connection restored',message:'Live report synchronization and Database update checks have resumed.',badge:''}" in app,'restored state must have no Online badge')
need('},5000);renderNetworkInfo()' in app,'restored banner must remain for five seconds')
need("window.addEventListener('offline',()=>{networkInterrupted=true;setNetworkBannerState('offline')" in app,'browser offline event must surface offline state immediately')
need("navigator.connection?.addEventListener?.('change',forceConnectivityRecheck)" in app,'Network Information change listener missing')
need("liveSyncFailures++;markNetworkFailure(true)" in app,'first failed live sync must surface API-unavailable state')
need("fetchJsonBounded(u,{cache:'no-store',timeoutMs:NETWORK_PROBE_TIMEOUT_MS})" in app,'bounded sync-head reachability probe missing')
need('function syncNetworkInfoAutoRefresh()' in app and 'NETWORK_INFO_INTERVAL_MS' in app,'automatic network-info refresh loop missing')
need("settingsActiveCategory!=='internet'" in app and 'stopNetworkInfoAutoRefresh()' in app,'network-info refresh scope/cleanup missing')
need('networkInfoRefresh' not in index and 'networkInfoRefresh' not in app,'manual network-info Refresh control must be removed')

# Local flags: every accepted code must have one same-origin local asset.
m=re.search(r"const COUNTRY_CODES=Object\.freeze\('([^']+)'\.split\(','\)\);",app)
need(bool(m),'country-code allow-list missing')
codes=m.group(1).split(',') if m else []
need(len(codes)==250 and len(set(codes))==250,'country-code allow-list must contain exactly 250 unique codes')
flags=root/'assets/country-flags'
actual=sorted(p.stem.upper() for p in flags.glob('*.png')) if flags.is_dir() else []
need(actual==sorted(codes),f'country flag asset set mismatch expected={len(codes)} actual={len(actual)}')
need('countryFlagAsset' in app and 'assets/country-flags/${cc.toLowerCase()}.png' in app,'same-origin local country flag mapping missing')
need('countryDisplayMarkup' in app and 'class="country-flag"' in app and 'alt="${esc(name)} flag"' in app,'country flag accessible markup missing')
need('flagcdn' not in app.lower() and 'countryflags' not in app.lower(),'runtime third-party flag service reference forbidden')

# Scroll/select visual consistency.
need('scrollbar-color:#684047 #100c0d' in css and '*::-webkit-scrollbar-thumb' in css,'site-wide scrollbar design missing')
need('.custom-select-menu::-webkit-scrollbar' in css and '.custom-select-option:active' in css,'custom dropdown scrollbar/interaction design missing')
need('data-native-select=' not in index,'regional controls must use accessible custom-select presentation')
need("root.querySelectorAll?.('select').forEach(enhanceSelect)" in app,'native select authoritative/custom select enhancement contract missing')

# Encyclopedia/Surface redesign and semantic guidance.
for token in ['encyclopedia-workspace','encyclopedia-stat-strip','encyclopedia-search-zone','encyclopedia-guidance','encyclopedia-results-head']:
    need(token in app and f'.{token}' in css,f'Encyclopedia workspace token missing: {token}')
need('Registry is reference, not evidence' in app and 'VulkanScope states stay authoritative' in app,'Encyclopedia reference/evidence guidance missing')
for token in ['surface-workspace','surface-summary-grid','surface-control-panel','surface-evidence-rule','surface-data-section']:
    need(token in app and f'.{token}' in css,f'Surface workspace token missing: {token}')
need('Unavailable, unsupported, not applicable and unknown are not interchangeable.' in app,'Surface semantic-state guidance missing')
need("surfaceQueryState(r.surface||{})" in app and "surfaceAvailableState(r.surface||{})==='available'" in app and "surfacePresentationState(r.surface||{})==='supported'" in app,'Surface summary must derive from canonical evidence-state helpers')

need('## Release 1.0.25 live network observation / local flags / coherent controls / Surface and Encyclopedia workspace requirements' in rules,'1.0.25 rules section missing')
need('No D1 migration' in rules,'1.0.25 immutability rule missing')

if errors:
    print('\n'.join('FAIL '+x for x in errors)); raise SystemExit(1)
print(f'PASS VulkanScope Database 1.0.25 connectivity/flags/scroll-select/Surface/Encyclopedia contract flags={len(actual)}')
