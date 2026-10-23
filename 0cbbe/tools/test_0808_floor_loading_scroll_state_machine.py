#!/usr/bin/env python3

def accepted(v):
    m,p=map(int,v.split('.')[1:]);return m>80 or (m==80 and p>=3)
def dtype(x):
    return {'Integrated GPU':'VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU','Discrete GPU':'VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU','Virtual GPU':'VK_PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU','CPU':'VK_PHYSICAL_DEVICE_TYPE_CPU','Other':'VK_PHYSICAL_DEVICE_TYPE_OTHER'}.get(x,x)
def arrows(y,h,total):
    scrollable=total>h+1;return scrollable and y>1,scrollable and y+h<total-1
for v,want in [('0.80.0',False),('0.80.1',False),('0.80.2',False),('0.80.3',True),('0.80.9',True),('0.81.0',True),('0.41.46',False)]:
    if accepted(v)!=want:raise SystemExit('FAIL floor '+v)
for src,want in [('Integrated GPU','VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU'),('Discrete GPU','VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU'),('VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU','VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU')]:
    if dtype(src)!=want:raise SystemExit('FAIL dtype '+src)
for case,want in [((0,600,1600),(False,True)),((500,600,1600),(True,True)),((1000,600,1600),(True,False)),((0,600,500),(False,False))]:
    if arrows(*case)!=want:raise SystemExit(f'FAIL arrows {case}')
print('PASS Database 0.39.23 floor/canonical-type/scroll state machine')
