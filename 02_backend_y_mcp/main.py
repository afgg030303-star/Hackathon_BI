import asyncio
from datetime import date
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field, ConfigDict
from config import ROOT
from db import Periodo
from agent import run_agent, report, model_status, AgentUnavailable

app=FastAPI(title='Observatorio Retail · Agente BI local',version='0.1.0')
app.add_middleware(TrustedHostMiddleware,allowed_hosts=['127.0.0.1','localhost','testserver'])
app.mount('/assets',StaticFiles(directory=ROOT/'03_frontend'),name='assets')
agent_lock=asyncio.Lock()

class Question(BaseModel):
    model_config=ConfigDict(extra='forbid')
    question: str=Field(min_length=3,max_length=1500)

@app.get('/')
async def index(): return FileResponse(ROOT/'03_frontend/index.html')

@app.get('/api/health')
async def health():
    return {'api':'ok','llm':await model_status(),'dataset':'UCI Online Retail','database':'comprobar mediante informe','version':'0.1.0'}

@app.get('/api/report')
async def analytics(desde: date=date(2010,12,1),hasta: date=date(2011,12,9),pais: str|None=None):
    try: p=Periodo(desde=desde,hasta=hasta,pais=pais)
    except ValueError: raise HTTPException(422,'Periodo o país no válido') from None
    try: return await report(str(p.desde),str(p.hasta),p.pais)
    except Exception: raise HTTPException(503,'No se pudo consultar el dataset UCI a través de MCP. Revisa Supabase y la carga de datos.') from None

@app.post('/api/chat')
async def chat(body: Question):
    if agent_lock.locked(): raise HTTPException(429,'El agente está respondiendo otra consulta. Espera a que termine.')
    async with agent_lock:
        try: return await run_agent(body.question)
        except AgentUnavailable as exc: raise HTTPException(503,str(exc)) from None
