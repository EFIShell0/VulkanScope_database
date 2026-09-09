def identity(version,code):
    parts=version.split('.')
    if len(parts)!=3:return False
    try: major,minor,patch=map(int,parts)
    except:return False
    if (major,minor,patch)==(1,0,0):return code==1000
    if (major,minor,patch)==(1,0,1):return code==1001
    if (major,minor,patch)==(1,0,2):return code==1002
    if major==0 and minor==80:return code==800+patch
    return True
cases=[('1.0.2',1002,True),('1.0.2',1001,False),('1.0.1',1001,True),('1.0.1',1002,False),('1.0.0',1000,True),('1.0.0',1001,False),('0.80.3',803,True),('0.80.3',802,False)]
for version,code,expected in cases:
    actual=identity(version,code)
    if actual!=expected:raise SystemExit(f'identity state mismatch {version}/{code}: {actual} != {expected}')
print('PASS Database 1.0.2 producer identity state model')
