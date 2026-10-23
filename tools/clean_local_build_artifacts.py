from __future__ import annotations
"""Quarantine only narrowly allowlisted local build outputs outside the source checkout.

No git-clean, force reset, or recursive deletion of user data occurs here.
"""
import argparse, datetime, os, pathlib, shutil, subprocess, sys

DEFAULT_ROOT=pathlib.Path(__file__).resolve().parents[1]
CANDIDATES=('dist','_site','build','node_modules','worker/node_modules','worker/.wrangler',
            '.wrangler','__pycache__','tools/__pycache__','worker/__pycache__')


def contains_symlinks(directory:pathlib.Path)->bool:
    if directory.is_symlink():return True
    for base,dirs,files in os.walk(directory,followlinks=False):
        for name in dirs+files:
            if (pathlib.Path(base)/name).is_symlink():return True
    return False


def tracked(root:pathlib.Path,relative:str)->bool:
    if not (root/'.git').exists():return False
    result=subprocess.run(['git','-C',str(root),'ls-files','--',relative],capture_output=True,text=True)
    if result.returncode:raise RuntimeError('Cannot verify tracked files: '+relative+' '+result.stderr.strip())
    return bool(result.stdout.strip())


def execute(root:pathlib.Path,apply:bool)->list[str]:
    root=root.resolve(strict=True)
    pending=[]
    for relative in CANDIDATES:
        target=root/relative
        if target.exists() or target.is_symlink():
            if not target.is_dir() or target.is_symlink():
                raise RuntimeError('Unexpected file/symlink at generated directory '+relative+'; manual review required')
            if tracked(root,relative):
                raise RuntimeError('Tracked source exists inside generated directory '+relative+'; refusing to relocate')
            if contains_symlinks(target):
                raise RuntimeError('Generated directory contains symlinks '+relative+'; refusing to relocate')
            pending.append((relative,target))
    if not apply:
        for relative,_ in pending:print('GENERATED BUILD OUTPUT '+relative)
        return [relative for relative,_ in pending]
    if not pending:
        print('PASS local build output hygiene: nothing to quarantine')
        return []
    backup_base=root.parent/(root.name+'-local-build-backups')
    timestamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    destination=backup_base/timestamp
    attempt=0
    while destination.exists():
        attempt+=1;destination=backup_base/(timestamp+f'-{attempt}')
    moved=[]
    try:
        for relative,target in pending:
            to=destination/relative
            to.parent.mkdir(parents=True,exist_ok=True)
            # rename on the same parent volume is atomic for each directory.
            target.rename(to)
            moved.append((relative,target,to))
            print('QUARANTINED '+relative+' -> '+str(to))
    except Exception:
        for relative,target,to in reversed(moved):
            if to.exists() and not target.exists():
                target.parent.mkdir(parents=True,exist_ok=True)
                to.rename(target)
        raise
    print('PASS local build output hygiene: generated state preserved outside Git checkout')
    return [relative for relative,_ in pending]

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=pathlib.Path,default=DEFAULT_ROOT)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.apply==args.check:parser.error('choose exactly one: --check or --apply')
    try:
        dirty=execute(args.root,args.apply)
    except Exception as error:
        raise SystemExit('FAIL local build output hygiene: '+str(error))
    if args.check and dirty:
        raise SystemExit('FAIL local generated paths would fail strict source audit; run --apply')
    if args.check:print('PASS local build output hygiene: clean')
