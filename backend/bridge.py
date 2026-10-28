"""Puente del despliegue público. Solo expone las tres rutas API del prototipo."""
import os
import secrets
from starlette.responses import JSONResponse
from main import app
from config import ROOT

class Bridge:
    async def __call__(self,scope,receive,send):
        if scope['type']!='http':
            await app(scope,receive,send); return
        headers=dict(scope['headers'])
        expected=os.environ.get('PUBLIC_BRIDGE_TOKEN','')
        actual=headers.get(b'x-prototype-key',b'').decode('utf-8',errors='replace')
        if not expected or not secrets.compare_digest(actual,expected):
            await JSONResponse({'detail':'No autorizado'},status_code=401)(scope,receive,send);return
        path=scope.get('path','')
        method=scope.get('method')
        if (path,method) not in {('/api/health','GET'),('/api/report','GET'),('/api/chat','POST')}:
            await JSONResponse({'detail':'Ruta no disponible'},status_code=404)(scope,receive,send);return
        # Límite real del cuerpo incluso con Transfer-Encoding chunked.
        body=b''
        while True:
            event=await receive()
            if event['type']=='http.disconnect': return
            body+=event.get('body',b'')
            if len(body)>8192:
                await JSONResponse({'detail':'Solicitud demasiado grande'},status_code=413)(scope,receive,send);return
            if not event.get('more_body'):break
        sent=False
        async def limited_receive():
            nonlocal sent
            if not sent:
                sent=True
                return {'type':'http.request','body':body,'more_body':False}
            return await receive()
        scope={**scope,'headers':[(k,v) for k,v in scope['headers'] if k!=b'host']+[(b'host',b'127.0.0.1')]}
        await app(scope,limited_receive,send)

bridge=Bridge()
