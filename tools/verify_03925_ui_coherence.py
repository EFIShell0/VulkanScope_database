from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(p): return (root/p).read_text(encoding='utf-8')
index=text('index.html'); app=text('assets/app.v03926.js'); css=text('assets/site.v0390.css')
need('role="status" aria-live="polite" aria-atomic="true"' in index,'loading live-region contract missing')
need('database-loading-label">DATABASE STATUS<' in index,'loading Database status label missing')
need('site.v0390.css?v=03926' in index and 'app.v03926.js?v=03926' in index,'main-page UI cache-busting key missing')
for token in ['setDatabaseLoading(true,\'Loading report index…\'','setDatabaseLoading(true,\'Loading reports…\'','completedLoads','failedReportLoads']:
    need(token in app,f'loading progress contract missing: {token}')
for token in ['class="encyclopedia-panel"','class="encyclopedia-stats"','notice encyclopedia-evidence-note','badge info','Registry/reference presence is not runtime capability evidence.']:
    need(token in app,f'Encyclopedia Database-design/evidence token missing: {token}')
need("query.trim().length<2" in app,'large-family two-character search floor missing')
need("entries.length>=24?'Showing the first 24 matches." in app and 'first 24 registered extensions' in app,'24-result Encyclopedia bound missing')
need('overflow-y:auto' not in css[css.find('/* 0.39.25 UI-coherence release'):], 'release introduced nested vertical Encyclopedia scrolling')
for token in ['background:var(--panel)','border:1px solid var(--line)','border-radius:var(--radius)','background:var(--panel2)']:
    need(token in css[css.find('/* 0.39.25 UI-coherence release'):],f'Database design token missing from UI release: {token}')
need('842 commands' not in app,'hard-coded Encyclopedia command census duplicated in presentation')
if errors:
    raise SystemExit('FAIL Database 0.39.25 UI coherence release\n- '+'\n- '.join(errors))
print('PASS Database 0.39.25 loading / Encyclopedia UI coherence release')
