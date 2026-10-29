// Recomendaciones trazables; las causas se investigan, no se inventan.
export function enrichAudit(data){
 return {...data,alertas:data.alertas.map(a=>({...a,
  dato_critico:`${a.dimension}: ${a.grupo}; cancelaciones ${a.cancelaciones} GBP; neto ${a.importe_neto} GBP.`,
  hipotesis:'La causa no está demostrada. Puede haber anulaciones, correcciones o asientos contables; contrastar facturas originales.',
  accion:a.regla==='neto_negativo'?'Conciliar abonos y ventas del periodo; clasificar el código como mercancía o ajuste contable antes de modificar precios.':'Revisar las facturas canceladas y sus ventas relacionadas; contrastar motivos con operaciones y atención al cliente.',
  responsable:'Responsable comercial y administración',
  validacion:'Documentar el motivo de cada incidencia, repetir la auditoría y comparar periodos completos equivalentes.'}))};
}
export function draftAudit(data){
 const first=data.alertas.slice(0,3);
 return {estado:'borrador_no_enviado',destinatario:'Responsable comercial y administración (revisar destinatario)',
 asunto:`Revisión de ventas y cancelaciones · ${data.desde} a ${data.hasta}`,
 cuerpo:`Hola equipo:\n\nLa auditoría de UCI Online Retail del ${data.desde} al ${data.hasta}${data.pais?' para '+data.pais:''} ha identificado ${data.alertas_activas} señales con umbrales heurísticos.\n\n${first.length?first.map(a=>a.dato_critico+'\nAcción propuesta: '+a.accion).join('\n\n'):'No se han activado alertas con estas reglas. Esto no demuestra ausencia de otros riesgos.'}\n\nSolicitamos conciliar las facturas y documentar los motivos antes de decidir cambios comerciales. No hay evidencia de costes, descuentos o causas; estos importes no son beneficios. Los grupos pueden solaparse y no deben sumarse.\n\nPropuesta: revisar en la próxima reunión comercial y repetir el análisis tras validar las incidencias.\n\nBorrador para revisión humana; no se ha enviado ningún correo.`};
}
export function estimateScenario(summary,cost){
 if(typeof cost!=='number'||!Number.isFinite(cost)||cost<0||cost>200)throw Error('Coste inválido');
 const m=summary.metricas,net=Number(m.importe_neto),sales=Number(m.ventas_positivas),estimatedCost=sales*cost/100;
 return {tipo:'SIMULACION_NO_BENEFICIO_REAL',supuesto_coste_porcentaje:cost,base_coste:'Ventas positivas; se supone que el coste no se recupera en cancelaciones',ventas_positivas:sales,importe_neto:net,coste_estimado:estimatedCost,resultado_estimado:net-estimatedCost,margen_estimado_porcentaje:net>0?100*(net-estimatedCost)/net:null,moneda:'GBP',limites:'Supuesto aportado por el usuario, no dato UCI. Excluye impuestos, gastos fijos y recuperación de costes. No es beneficio contable.'};
}
export function groundedAnswer(evidence,fallback){
 const draft=[...evidence].reverse().find(e=>e.tool==='redactar_borrador');
 if(draft)return `BORRADOR NO ENVIADO\nPara: ${draft.result.destinatario}\nAsunto: ${draft.result.asunto}\n\n${draft.result.cuerpo}`;
 const audit=[...evidence].reverse().find(e=>e.tool==='auditar_anomalias');
 if(!audit)return fallback;
 const a=audit.result;
 return `AUDITORÍA · ${a.desde} a ${a.hasta}${a.pais?' · '+a.pais:''}\n${a.alertas_activas} señales en ${a.grupos_analizados} grupos. Se muestran ${a.alertas.length}.\n\n`+a.alertas.map(x=>`DATO CRÍTICO: ${x.dato_critico}\nSEÑAL: ${x.regla}; cancelaciones/ventas ${x.tasa_cancelacion===null?'no calculable':x.tasa_cancelacion+'%'}.\nHIPÓTESIS: ${x.hipotesis}\nACCIÓN PROPUESTA: ${x.accion}\nRESPONSABLE: ${x.responsable}\nVALIDACIÓN: ${x.validacion}`).join('\n\n')+`\n\nREGLAS: ${a.reglas}\nLÍMITES: ${a.limites}`;
}
