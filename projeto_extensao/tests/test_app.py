import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
import run

def test_index(tmp_path, monkeypatch):
    monkeypatch.setattr(run, 'DB', tmp_path/'test.db')
    run.init_db()
    client=run.app.test_client()
    r=client.get('/')
    assert r.status_code==200
    assert b'Conectando gera' in r.data

def test_participante(tmp_path, monkeypatch):
    monkeypatch.setattr(run, 'DB', tmp_path/'test.db')
    run.init_db(); client=run.app.test_client()
    r=client.post('/participantes/novo', data={'nome':'Maria','idade':'68','contato':'','observacoes':''}, follow_redirects=True)
    assert r.status_code==200
    assert b'Maria' in r.data
