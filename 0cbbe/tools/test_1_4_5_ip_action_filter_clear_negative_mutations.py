from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
required=['index.html','assets/app.v1405.js','assets/site.v1405.css','worker/src/index.js','rules/PROJECT_RULES.md','data/release.json','tools/repair_repository.py','tools/build_pages_artifact.py']
cases=[
 ('whole-address-clickable','assets/app.v1405.js','return`<span class="network-address-toggle ${revealed?', 'return`<button class="network-address-toggle ${revealed?'),
 ('action-button-missing','assets/app.v1405.js','<button class="network-address-action" type="button" data-network-address-toggle="${esc(key)}"','<span class="network-address-action" data-network-address-toggle="${esc(key)}"'),
 ('shell-state-owner','assets/app.v1405.js',"const shell=button.closest('.network-address-toggle');shell?.classList.toggle('is-revealed',!!revealed)","button.classList.toggle('is-revealed',!!revealed)"),
 ('action-pointer','assets/site.v1405.css','cursor:pointer;font:inherit;font-size:9px','cursor:default;font:inherit;font-size:9px'),
 ('clear-control-class','assets/app.v1405.js',"clearSearch.className='search-clear-button custom-select-search-clear is-hidden'","clearSearch.className='custom-select-search-clear is-hidden'"),
 ('clear-visibility','assets/app.v1405.js','const syncSearchClear=()=>{const hidden=!search.value;','const syncSearchClear=()=>{const hidden=false;'),
 ('clear-value','assets/app.v1405.js',"if(!search.value)return;search.value='';syncSearchClear();","if(!search.value)return;syncSearchClear();"),
 ('clear-input-sync','assets/app.v1405.js',"search.addEventListener('input',syncSearchClear);syncSearchClear();menu.appendChild(searchShell)","syncSearchClear();menu.appendChild(searchShell)"),
 ('clear-motion','assets/site.v1405.css','.custom-select-search-clear.is-hidden{width:0;flex-basis:0','.custom-select-search-clear.is-hidden{width:30px;flex-basis:30px'),
 ('release-marker','data/release.json','"databaseVersion":"1.4.5"','"databaseVersion":"1.4.4"'),
]
temps=[]
try:
    for name,rel,needle,repl in cases:
        td=tempfile.TemporaryDirectory(prefix=f'vsdb-145-neg-{name}-'); temps.append(td); dst=Path(td.name)/'src'; dst.mkdir()
        for f in required:
            out=dst/f; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,out)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if needle not in s: raise SystemExit(f'negative fixture needle missing for {name}: {needle}')
        p.write_text(s.replace(needle,repl,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(root/'tools/verify_1_4_5_ip_action_filter_clear.py'),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}\n{r.stdout}')
    print(f'PASS Database 1.4.5 negative mutations: {len(cases)} expected failures')
finally:
    for td in temps: td.cleanup()
