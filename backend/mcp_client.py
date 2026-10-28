import json
import os
import sys
from contextlib import asynccontextmanager
from datetime import timedelta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from config import ROOT

@asynccontextmanager
async def connect_mcp():
    env={k:v for k,v in os.environ.items() if k in ('PATH','HOME','DATABASE_URL','SYSTEMROOT')}
    env['PYTHONUNBUFFERED']='1'
    params=StdioServerParameters(command=sys.executable,args=[str(ROOT/'backend/mcp_server.py')],env=env)
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write,read_timeout_seconds=timedelta(seconds=30)) as session:
            await session.initialize()
            yield session

async def call_tool(session,name,args):
    result=await session.call_tool(name,args)
    if result.isError:
        raise RuntimeError('La herramienta MCP no pudo completar la consulta. Revisa parámetros y base de datos.')
    if result.structuredContent is not None:
        return result.structuredContent
    for block in result.content:
        if block.type=='text':
            return json.loads(block.text)
    raise RuntimeError('MCP no devolvió un resultado válido')
