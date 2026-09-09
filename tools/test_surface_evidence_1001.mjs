import assert from 'node:assert/strict';
import {normalizeReport} from '../worker/src/index.js';
function normalized(status, order='status-first'){
  const statusLine=`Query status=${status}`;
  const boolLine='Available=false, presentation=false';
  const body=order==='status-first'?`${statusLine}\n${boolLine}`:`${boolLine}\n${statusLine}`;
  return normalizeReport({reportText:`VulkanScope report\nSURFACE\n${body}\n`});
}
const expected={available:['unavailable','unsupported'],incomplete:['incomplete','incomplete'],unavailable:['unavailable','unavailable'],not_applicable:['not_applicable','not_applicable'],unknown:['unknown','unknown']};
for(const [q,[a,p]] of Object.entries(expected)){
  for(const order of ['status-first','boolean-first']){
    const n=normalized(q,order), by=new Map(n.capabilities.filter(x=>x.section==='SURFACE').map(x=>[x.name,x.status]));
    assert.equal(by.get('Available'),a,`${q}/${order} Available`);
    assert.equal(by.get('Presentation supported'),p,`${q}/${order} Presentation`);
  }
}
console.log('PASS Database 1.0.1 Surface evidence-state and line-order model');
