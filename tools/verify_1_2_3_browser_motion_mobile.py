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
app=text('assets/app.v1203.js'); compat=text('assets/browser-compat.v1203.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md')
need("const DATABASE_VERSION='1.2.3'" in app,'frontend 1.2.3 identity missing')
need('assets/app.v1203.js?v=1203' in index and 'browser-compat.v1203.js?v=1203' in index,'1.2.3 cache/browser references missing')
need('VulkanScope Database <strong>1.2.3</strong>' in index,'footer identity missing')
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors missing')
for token in ['window.ResizeObserver','Element.prototype.animate','Element.prototype.getAnimations','window.AbortController']:
    need(token in compat,f'compatibility feature probe missing {token}')
need('browserCompatibilityGate' in index and 'This browser is not supported' in index,'incompatible-browser page missing')
need("const browserLanguage=()=> 'en-US'" in app,'browser locale can still leak into UI')
need("new Intl.DisplayNames(['en'],{type:'region'})" in app,'country names not forced to English')
need("if(!cc||cc==='auto')return'en-US'" in app,'automatic regional locale not English')
need("classList.toggle('at-page-top',atTop)" in app and "classList.toggle('at-page-bottom',atBottom)" in app,'page endpoint classes missing')
need('html.at-page-top::-webkit-scrollbar-button:single-button:vertical:decrement' in css,'top scrollbar arrow inactive style missing')
need('html.at-page-bottom::-webkit-scrollbar-button:single-button:vertical:increment' in css,'bottom scrollbar arrow inactive style missing')
need('transition-property:background-color,border-color,color,box-shadow,opacity,transform,filter' in css,'shared interaction motion contract missing')
need('@media(prefers-reduced-motion:reduce)' in css,'reduced-motion fallback missing')
for token in ['html,body{max-width:100%;overflow-x:hidden}','@media(max-width:760px)','@media(max-width:430px)','.table-wrap{overflow-x:auto}']:
    need(token in css,f'mobile overflow containment missing {token}')
need('## Release 1.2.3 browser compatibility / English presentation / endpoint motion / mobile overflow requirements' in rules,'1.2.3 rules section missing')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.3','releaseReady':False,'appAsset':'assets/app.v1203.js','cacheKey':'1203'},'release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.3 browser/motion/mobile contract')
