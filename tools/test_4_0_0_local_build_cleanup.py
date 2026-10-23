from pathlib import Path
import os,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
script=root/'tools/clean_local_build_artifacts.py'
def run(dest,*args):return subprocess.run([sys.executable,str(script),'--root',str(dest),*args],capture_output=True,text=True)
with tempfile.TemporaryDirectory(prefix='vsdb4000-hygiene-') as td:
    dest=Path(td)/'repo';dest.mkdir()
    subprocess.run(['git','init','-q',str(dest)],check=True)
    (dest/'.gitignore').write_text('dist/\nworker/node_modules/\nworker/.wrangler/\n',encoding='utf-8')
    subprocess.run(['git','-C',str(dest),'add','.gitignore'],check=True)
    # A clean tree has no generated build outputs.
    assert run(dest,'--check').returncode==0
    for rel in ('dist/release.zip','worker/node_modules/tool.js','worker/.wrangler/tmp/state'):
        p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('private-local-data',encoding='utf-8')
    assert run(dest,'--check').returncode!=0
    result=run(dest,'--apply');assert result.returncode==0,result.stdout+result.stderr
    assert run(dest,'--check').returncode==0
    assert run(dest,'--apply').returncode==0
    backup=dest.parent/(dest.name+'-local-build-backups')
    for rel in ('dist/release.zip','worker/node_modules/tool.js','worker/.wrangler/tmp/state'):
        hits=list(backup.rglob(Path(rel).name));assert len(hits)==1 and hits[0].read_text(encoding='utf-8')=='private-local-data',rel
    # Symlink is an unsafe file-system topology even when git ignores it.
    marker=dest/'dist'
    try:
        marker.symlink_to(backup,target_is_directory=True)
    except (OSError,NotImplementedError):
        # Windows without Developer Mode/admin permission cannot create test symlinks.
        print('SKIP symlink creation negative: OS permission unavailable')
    else:
        assert run(dest,'--apply').returncode!=0
        marker.unlink()
    # Tracked material must never be silently moved or erased.
    tracked=dest/'dist';tracked.mkdir();(tracked/'important.txt').write_text('tracked',encoding='utf-8')
    subprocess.run(['git','-C',str(dest),'add','-f','dist/important.txt'],check=True)
    assert run(dest,'--apply').returncode!=0
    assert (tracked/'important.txt').read_text(encoding='utf-8')=='tracked'
print('PASS 4.0.0 local-build quarantine: clean, dirty, idempotence, preservation, symlink and tracked-file negatives')
