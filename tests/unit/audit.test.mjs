import {test} from 'node:test';
import assert from 'node:assert/strict';
import {estimateScenario,draftAudit,enrichAudit} from '../../web_publica/audit.mjs';
test('coste supuesto separado; neto cero no divide por cero',()=>{
 const r=estimateScenario({metricas:{ventas_positivas:100,importe_neto:0}},70);
 assert.equal(r.resultado_estimado,-70);assert.equal(r.margen_estimado_porcentaje,null);assert.equal(r.tipo,'SIMULACION_NO_BENEFICIO_REAL');
});
test('rechaza costes no finitos o fuera de rango',()=>{for(const x of [NaN,Infinity,-1,201,'70'])assert.throws(()=>estimateScenario({},x))});
test('borrador sin alertas no inventa incidencias ni envío',()=>{
 const d=draftAudit({desde:'2010-12-01',hasta:'2011-12-09',alertas_activas:0,alertas:[]});
 assert.equal(d.estado,'borrador_no_enviado');assert.match(d.cuerpo,/No se han activado alertas/);
});
test('código contable no es pérdida demostrada',()=>{
 const a=enrichAudit({alertas:[{grupo:'AMAZONFEE',dimension:'producto',regla:'neto_negativo',cancelaciones:200,importe_neto:-100}]}).alertas[0];
 assert.match(a.accion,/ajuste contable/);assert.match(a.hipotesis,/no está demostrada/);
});
