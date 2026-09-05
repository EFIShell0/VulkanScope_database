#!/usr/bin/env python3
import argparse,json,xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

def supports_vulkan(value):
    if not value:return True
    parts={x.strip() for x in value.split(',')}
    return 'vulkan' in parts and 'disabled' not in parts

def provider_maps(root):
    providers=defaultdict(set)
    for feature in root.findall('./feature'):
        if not supports_vulkan(feature.get('api')): continue
        provider=feature.get('name','')
        for require in feature.findall('require'):
            if not supports_vulkan(require.get('api')): continue
            for tag in ('command','enum','type'):
                for node in require.findall(tag):
                    name=node.get('name')
                    if name:providers[(tag,name)].add(provider)
    for ext in root.findall('./extensions/extension'):
        if not supports_vulkan(ext.get('supported')):continue
        provider=ext.get('name','')
        for require in ext.findall('require'):
            if not supports_vulkan(require.get('api')):continue
            for tag in ('command','enum','type'):
                for node in require.findall(tag):
                    name=node.get('name')
                    if name:providers[(tag,name)].add(provider)
    return providers

def symbols(root):
    providers=provider_maps(root)
    command_names=set()
    for cmd in root.findall('./commands/command'):
        name=cmd.get('name') or cmd.findtext('proto/name')
        if name and name.startswith('vk') and providers.get(('command',name)):command_names.add(name)
    commands=[[n,'Vulkan command',', '.join(sorted(providers[('command',n)]))] for n in sorted(command_names)]
    token_owner={}
    for group in root.findall('./enums'):
        owner=group.get('name') or group.get('type') or 'Vulkan enum/token'
        for enum in group.findall('enum'):
            name=enum.get('name')
            if name and name.startswith('VK_'):token_owner.setdefault(name,owner)
    for enum in root.findall('.//enum'):
        name=enum.get('name')
        if not name or not name.startswith('VK_'):continue
        extends=enum.get('extends')
        if extends:token_owner.setdefault(name,extends)
        elif name.endswith('_EXTENSION_NAME'):token_owner.setdefault(name,'Extension name macro')
        elif name.endswith('_SPEC_VERSION'):token_owner.setdefault(name,'Extension revision macro')
        else:token_owner.setdefault(name,'Vulkan enum/token')
    tokens=[]
    for name in sorted(token_owner):
        prov=providers.get(('enum',name),set())
        if not prov and token_owner[name]=='Vulkan enum/token':continue
        tokens.append([name,token_owner[name],', '.join(sorted(prov)) if prov else 'Core/registry declaration'])
    type_meta={}
    for node in root.findall('./types/type'):
        name=node.get('name') or node.findtext('name')
        if name and name.startswith('Vk') and providers.get(('type',name)):type_meta[name]=node.get('category') or 'type'
    types=[[n,type_meta[n],', '.join(sorted(providers[('type',n)]))] for n in sorted(type_meta)]
    return commands,tokens,types

def extension_rows(root):
    enum_values={}
    for enum in root.findall('.//enum'):
        name=enum.get('name')
        value=enum.get('value')
        if name and value is not None:enum_values.setdefault(name,value.strip('"'))
    rows=[]
    for ext in root.findall('./extensions/extension'):
        if not supports_vulkan(ext.get('supported')):continue
        name=ext.get('name','')
        commands=[];enums=[]
        for req in ext.findall('require'):
            if not supports_vulkan(req.get('api')):continue
            commands.extend(x.get('name') for x in req.findall('command') if x.get('name'))
            enums.extend(x.get('name') for x in req.findall('enum') if x.get('name'))
        spec_name=name.upper()+'_SPEC_VERSION'
        spec=''
        for en in enums:
            if en.endswith('_SPEC_VERSION') and en.startswith(name.upper().replace('VK_','VK_')):
                spec=enum_values.get(en,'');break
        author=name.split('_',2)[1] if name.count('_')>=2 else ''
        rows.append({'name':name,'author':author,'specVersion':spec,'type':ext.get('type',''),'platform':ext.get('platform',''),'promotedTo':ext.get('promotedto',''),'requires':ext.get('requires',''),'deprecatedBy':ext.get('deprecatedby',''),'obsoletedBy':ext.get('obsoletedby',''),'depends':ext.get('depends',''),'provisional':ext.get('provisional')=='true','commands':sorted(set(commands)),'enums':sorted(set(enums))})
    return sorted(rows,key=lambda x:x['name'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--registry',default='registry/upstream/vk.xml');ap.add_argument('--curated',default='registry/encyclopedia_curated.json');ap.add_argument('--output',default='assets/encyclopedia.v03924.js');args=ap.parse_args()
    root=ET.parse(args.registry).getroot();cur=json.loads(Path(args.curated).read_text(encoding='utf-8'))
    commands,tokens,types=symbols(root);extensions=extension_rows(root)
    data={'schemaVersion':1,'appVersion':cur['appVersion'],'registryBaseline':cur['registryBaseline'],'counts':{'commands':len(commands),'tokens':len(tokens),'types':len(types),'extensions':len(extensions),'vkResults':len(cur['vkResults'])},'core':cur['core'],'vkResults':cur['vkResults'],'commonCommands':cur['commonCommands'],'commands':commands,'tokens':tokens,'types':types,'extensions':extensions}
    expected={'commands':842,'tokens':6248,'types':2461,'extensions':476,'vkResults':50}
    if data['counts']!=expected:raise SystemExit(f'encyclopedia census mismatch {data["counts"]} != {expected}')
    payload=json.dumps(data,ensure_ascii=False,separators=(',',':'))
    Path(args.output).write_text('window.VULKANSCOPE_ENCYCLOPEDIA='+payload+';\n',encoding='utf-8')
    print('generated',args.output,data['counts'])
if __name__=='__main__':main()
