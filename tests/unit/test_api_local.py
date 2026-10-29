import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'backend'))
from fastapi.testclient import TestClient
import main
client=TestClient(main.app)

def test_periodo_invertido():
    assert client.get('/api/report?desde=2012-01-01&hasta=2011-01-01').status_code==422

def test_coste_fuera_de_rango():
    assert client.post('/api/scenario',json={'coste_porcentaje':-1}).status_code==422

def test_fallo_db_sin_filtrar_secretos(monkeypatch):
    async def failure(*args):raise RuntimeError('PASSWORD_SHOULD_NOT_LEAK')
    monkeypatch.setattr(main,'report',failure)
    r=client.get('/api/report')
    assert r.status_code==503
    assert 'PASSWORD_SHOULD_NOT_LEAK' not in r.text

def test_chat_corto():
    assert client.post('/api/chat',json={'question':'x'}).status_code==422
