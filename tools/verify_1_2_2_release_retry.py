from __future__ import annotations
from pathlib import Path
import argparse,json,re
parser=argparse.ArgumentParser(); parser.add_argument('--root',default=None); args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
app=text('assets/app.v1202.js'); css=text('assets/site.v0390.css'); index=text('index.html'); worker=text('worker/src/index.js'); rules=text('rules/PROJECT_RULES.md'); contract=text('worker/tests/contract.mjs')
need("const DATABASE_VERSION='1.2.2',LIVE_SYNC_INTERVAL_MS=3000,RELEASE_CHECK_INTERVAL_MS=10000,NETWORK_INFO_INTERVAL_MS=3000,NETWORK_PROBE_TIMEOUT_MS=2200;" in app,'1.2.2 frontend identity/timers missing')
need('assets/app.v1202.js?v=1202' in index and 'site.v0390.css?v=1202' in index and 'config.js?v=1202' in index,'1.2.2 cache-busted references missing')
need('VulkanScope Database <strong>1.2.2</strong>' in index,'1.2.2 footer identity missing')
# Producer floor and 1.2.0 workspace/privacy behavior are retained.
need('const producerAtLeast1205=p=>' in worker and 'const supportedProducer=p=>producerAtLeast1205(p)' in worker,'1.2.5 submission floor missing')
need('VulkanScope 1.2.5 or newer is required for new submissions' in worker,'1.2.5 floor rejection missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker floor contract fixtures missing')
need('Updating connection observation…' not in app,'silent automatic Internet refresh regressed')
need('WORKSPACE_UI' in app and 'FILTER_FAMILIES' in app,'1.2.0 purpose-specific workspaces/filter families regressed')
# Compare sticky tracking contract.
for token in ['compareStickySentinel','function syncCompareStickyState()','queueCompareStickyState','compare-workspace.is-compact']:
    need(token in app or token in css,f'Compare sticky tracking missing: {token}')
need('.compare-workspace{position:sticky;' in css,'Compare workspace is not sticky')
need("sentinel.getBoundingClientRect().top<top" in app,'Compare natural-top compact transition missing')
need("String(slot||'').toLowerCase()==='a'?'Baseline':'Candidate'" in app,'Compare A/B identity label bug remains')
# Page scrollbar and endpoint controls.
need('html::-webkit-scrollbar,body::-webkit-scrollbar{width:14px;height:14px}' in css,'primary page scrollbar width contract missing')
need("setButton(up,scrollable,y<=2);setButton(down,scrollable,y>=max-2)" in app,'page endpoint arrow disabled-state logic missing')
need('.page-scroll-controls button:disabled' in css,'disabled page-scroll visual state missing')
need('::-webkit-scrollbar-button:single-button:vertical:disabled' in css,'native scrollbar endpoint disabled style missing')
# Network effectiveType semantics.
need("['Browser effective network class',navigator.connection?.effectiveType?" in app,'effective network class label missing')
need('not the physical access technology' in app and 'FTTH, Wi‑Fi or wired Ethernet' in app,'effectiveType non-physical-access explanation missing')
need("['Connection profile'" not in app,'misleading Connection profile label remains')
# Temporal source integrity.
need('const submissionEpoch=value=>' in app,'raw submission epoch parser missing')
need("if(field==='submitted'){const t=submissionEpoch(r.submittedAt)" in app,'submission sort is not bound to raw epoch')
need('submissionAgeFilter:(r,v)=>{const days=Number(v),t=submissionEpoch(r.submittedAt)' in app,'submission age filter is not bound to raw epoch')
need('Sorting, age filters and comparison identity always use the original server-authored timestamp' in index,'regional presentation/source separation explanation missing')
# Destructive confirmation.
for token in ['destructiveConfirmDialog','requestDestructiveConfirmation','Clear saved browser data?','Remove favorite?','requestFavoriteToggle']:
    need(token in app or token in index,f'destructive confirmation contract missing: {token}')
need("const active=await requestFavoriteToggle(button.dataset.favoriteReport||'')" in app,'favorite-button removal does not pass through confirmation')
need('if(clear)clear.onclick=async()=>{const ok=await requestDestructiveConfirmation' in app,'clear-saved-data action does not pass through confirmation')
need('destructive-confirm-dialog' in css and 'destructive-confirm-backdrop' in css,'confirmation visual layer missing')
# Detail interaction regression.
need('function syncDetailTabUi(ensureVisible=false)' in app,'detail tab synchronizer definition missing')
need('syncDetailTabUi(false);renderDetailTab(r)' in app,'detail render does not synchronize/render tab body')
need("tab.setAttribute('aria-selected',active?'true':'false')" in app and 'tab.tabIndex=active?0:-1' in app,'detail tab ARIA/tabindex state missing')
need("const el=$('#detailTabBody'),t=state.detailTab,c=r.capabilities||[];if(!el)return;" in app,'detail body null guard missing')
# Release rules and marker.

workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
for wf_name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need('permissions:\n      contents: write' in wf,f'{wf_name}: release job contents:write missing')
    need('for attempt in 1 2 3 4 5' in wf,f'{wf_name}: bounded release retry loop missing')
    need('HTTP 429|HTTP 5[0-9][0-9]|rate limit|temporarily unavailable' in wf,f'{wf_name}: transient GitHub API classifier missing')
    need('git rev-list -n 1 "$TAG"' in wf,f'{wf_name}: tag ownership verification missing')
    need('bump the Database version instead of retargeting' in wf,f'{wf_name}: fail-closed tag policy missing')
need('## Release 1.2.2 GitHub Release retry hardening / inherited 1.2.1 UI integrity requirements' in rules,'1.2.2 rules section missing')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.2','releaseReady':False,'appAsset':'assets/app.v1202.js','cacheKey':'1202'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.2 release-retry + inherited compare/temporal/detail contract')
