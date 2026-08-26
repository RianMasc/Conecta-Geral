from pathlib import Path
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, abort

BASE = Path(__file__).resolve().parent
DB = BASE / 'conecta_geracoes.db'
app = Flask(__name__, template_folder=str(BASE / 'templates'), static_folder=str(BASE / 'static'))
app.secret_key = 'conecta-geracoes-dev-key'

ENCONTROS = [
    (1, 'O Básico para Começar', 'Smartphone/tablet, Wi-Fi, dados móveis e instalação de aplicativos.'),
    (2, 'Dominando o WhatsApp', 'Mensagens, áudios, fotos, vídeos, chamadas, videochamadas e segurança.'),
    (3, 'Entrando no Mundo do Facebook', 'Perfil, amigos, publicações e grupos de interesse.'),
    (4, 'Instagram e Revisão Geral', 'Instagram, revisão das aulas, dúvidas e encerramento.'),
]

MATERIAIS = {
    1: ['Ligar/desligar e desbloquear', 'Ajustar volume e brilho', 'Conectar ao Wi-Fi', 'Ativar/desativar dados móveis', 'Abrir a loja de aplicativos', 'Instalar o WhatsApp'],
    2: ['Enviar texto e áudio', 'Enviar fotos e vídeos', 'Fazer ligações', 'Fazer videochamadas', 'Reconhecer golpes e correntes', 'Revisar privacidade'],
    3: ['Criar ou revisar perfil', 'Adicionar familiares e amigos', 'Curtir, comentar e compartilhar', 'Encontrar grupos de interesse', 'Publicar uma foto'],
    4: ['O que é o Instagram', 'Seguir perfis', 'Interagir com publicações', 'Revisão de WhatsApp e segurança', 'Perguntas e respostas'],
}

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS participantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        contato TEXT,
        observacoes TEXT,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS acompanhamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        participante_id INTEGER NOT NULL,
        encontro INTEGER NOT NULL,
        presenca INTEGER NOT NULL DEFAULT 0,
        aprendizado INTEGER NOT NULL DEFAULT 0,
        observacoes TEXT,
        FOREIGN KEY(participante_id) REFERENCES participantes(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS encontros (
        numero INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL
    );
    ''')
    conn.executemany('INSERT OR IGNORE INTO encontros(numero,titulo,descricao) VALUES (?,?,?)', ENCONTROS)
    conn.commit(); conn.close()

def dashboard_stats(conn):
    total = conn.execute('SELECT COUNT(*) c FROM participantes').fetchone()['c']
    ativos = conn.execute('SELECT COUNT(DISTINCT participante_id) c FROM acompanhamentos').fetchone()['c']
    registros = conn.execute('SELECT COUNT(*) c FROM acompanhamentos').fetchone()['c']
    presentes = conn.execute('SELECT COALESCE(SUM(presenca),0) c FROM acompanhamentos').fetchone()['c']
    media = conn.execute('SELECT AVG(aprendizado) m FROM acompanhamentos').fetchone()['m']
    taxa = round((presentes / registros) * 100) if registros else 0
    return dict(total=total, ativos=ativos, registros=registros, presentes=presentes, media=round(media or 0, 1), taxa=taxa)

@app.context_processor
def inject_globals():
    return {'app_name': 'Conecta Gerações'}

@app.route('/')
def index():
    conn = get_db(); stats = dashboard_stats(conn)
    recentes = conn.execute('''SELECT a.*, p.nome FROM acompanhamentos a JOIN participantes p ON p.id=a.participante_id ORDER BY a.id DESC LIMIT 6''').fetchall()
    por_encontro = []
    for n in range(1, 5):
        row = conn.execute('SELECT COUNT(*) total, COALESCE(SUM(presenca),0) presentes, COALESCE(AVG(aprendizado),0) media FROM acompanhamentos WHERE encontro=?', (n,)).fetchone()
        por_encontro.append({'numero': n, 'total': row['total'], 'presentes': row['presentes'], 'media': round(row['media'], 1)})
    conn.close()
    return render_template('index.html', stats=stats, recentes=recentes, por_encontro=por_encontro)

@app.route('/participantes')
def participantes():
    q = request.args.get('q', '').strip()
    conn = get_db()
    if q:
        rows = conn.execute('SELECT * FROM participantes WHERE nome LIKE ? OR contato LIKE ? ORDER BY nome', (f'%{q}%', f'%{q}%')).fetchall()
    else:
        rows = conn.execute('SELECT * FROM participantes ORDER BY nome').fetchall()
    conn.close()
    return render_template('participantes.html', participantes=rows, q=q)

@app.route('/participantes/novo', methods=['GET','POST'])
def novo_participante():
    if request.method == 'POST':
        nome = request.form['nome'].strip(); idade = int(request.form['idade'])
        contato = request.form.get('contato','').strip(); obs = request.form.get('observacoes','').strip()
        if idade < 60: flash('O público-alvo do projeto é de 60 anos ou mais.', 'warning')
        if not nome: flash('Informe o nome do participante.', 'error'); return render_template('participante_form.html')
        conn=get_db(); cur=conn.execute('INSERT INTO participantes(nome,idade,contato,observacoes) VALUES (?,?,?,?)',(nome,idade,contato,obs)); pid=cur.lastrowid; conn.commit(); conn.close()
        flash('Participante cadastrado com sucesso.', 'success'); return redirect(url_for('participante_detalhe', pid=pid))
    return render_template('participante_form.html')

@app.route('/participantes/<int:pid>')
def participante_detalhe(pid):
    conn=get_db(); p=conn.execute('SELECT * FROM participantes WHERE id=?',(pid,)).fetchone()
    if not p: conn.close(); abort(404)
    registros=conn.execute('''SELECT a.*, e.titulo FROM acompanhamentos a LEFT JOIN encontros e ON e.numero=a.encontro WHERE a.participante_id=? ORDER BY a.encontro''',(pid,)).fetchall()
    total=len(registros); pres=sum(r['presenca'] for r in registros); media=round(sum(r['aprendizado'] for r in registros)/total,1) if total else 0
    conn.close()
    return render_template('participante_detalhe.html', p=p, registros=registros, total=total, pres=pres, media=media)

@app.route('/participantes/<int:pid>/editar', methods=['GET','POST'])
def editar_participante(pid):
    conn=get_db(); p=conn.execute('SELECT * FROM participantes WHERE id=?',(pid,)).fetchone()
    if not p: conn.close(); abort(404)
    if request.method=='POST':
        conn.execute('UPDATE participantes SET nome=?, idade=?, contato=?, observacoes=? WHERE id=?', (request.form['nome'].strip(), int(request.form['idade']), request.form.get('contato','').strip(), request.form.get('observacoes','').strip(), pid)); conn.commit(); conn.close()
        flash('Dados atualizados.', 'success'); return redirect(url_for('participante_detalhe', pid=pid))
    conn.close(); return render_template('participante_form.html', p=p, editing=True)

@app.post('/participantes/<int:pid>/excluir')
def excluir_participante(pid):
    conn=get_db(); conn.execute('DELETE FROM participantes WHERE id=?',(pid,)); conn.commit(); conn.close(); flash('Participante removido.', 'success'); return redirect(url_for('participantes'))

@app.route('/encontros')
def encontros():
    conn=get_db(); rows=conn.execute('SELECT * FROM encontros ORDER BY numero').fetchall(); conn.close()
    return render_template('encontros.html', encontros=rows)

@app.route('/materiais/<int:numero>')
def materiais(numero):
    conn=get_db(); e=conn.execute('SELECT * FROM encontros WHERE numero=?',(numero,)).fetchone(); conn.close()
    if not e: abort(404)
    return render_template('materiais.html', encontro=e, itens=MATERIAIS.get(numero, []))

@app.route('/acompanhamento', methods=['GET','POST'])
def acompanhamento():
    conn=get_db()
    if request.method=='POST':
        pid=int(request.form['participante_id']); encontro=int(request.form['encontro']); presenca=int(request.form.get('presenca',0)); aprendizado=int(request.form['aprendizado']); obs=request.form.get('observacoes','').strip()
        conn.execute('INSERT INTO acompanhamentos(participante_id,encontro,presenca,aprendizado,observacoes) VALUES (?,?,?,?,?)',(pid,encontro,presenca,aprendizado,obs)); conn.commit(); conn.close(); flash('Acompanhamento registrado.', 'success'); return redirect(url_for('acompanhamento'))
    ps=conn.execute('SELECT * FROM participantes ORDER BY nome').fetchall(); es=conn.execute('SELECT * FROM encontros ORDER BY numero').fetchall(); rs=conn.execute('SELECT a.*,p.nome,e.titulo FROM acompanhamentos a JOIN participantes p ON p.id=a.participante_id LEFT JOIN encontros e ON e.numero=a.encontro ORDER BY a.id DESC').fetchall(); conn.close()
    return render_template('acompanhamento.html', participantes=ps, encontros=es, registros=rs)

@app.route('/relatorios')
def relatorios():
    conn=get_db(); stats=dashboard_stats(conn)
    por_encontro=[]
    for n in range(1,5):
        row=conn.execute('SELECT COUNT(*) total, COALESCE(SUM(presenca),0) presentes, COALESCE(AVG(aprendizado),0) media FROM acompanhamentos WHERE encontro=?',(n,)).fetchone()
        por_encontro.append({'numero':n,'total':row['total'],'presentes':row['presentes'],'media':round(row['media'],1)})
    conn.close(); return render_template('relatorios.html', stats=stats, por_encontro=por_encontro)

with app.app_context(): init_db()

if __name__ == '__main__': app.run(debug=True)
