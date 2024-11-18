from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from main import app, db
from models import Jogos, Usuarios
import os

@app.route('/')
def index():
    lista_jogos = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Novos jogos', jogos=lista_jogos)

@app.route('/novo')
def retornar_pagina_cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('fazer_login', proxima=url_for('retornar_pagina_cadastro')))
    return render_template('cadastrar.html', titulo='Cadastro de Jogo')

@app.route('/cadastrar', methods=['POST'])
def cadastrar_jogo():
    nome = request.form.get('nome')
    console = request.form.get('console')
    categoria = request.form.get('categoria')
    arquivo = request.files.get('arquivo')

    if not arquivo:
        flash('Nenhum arquivo foi enviado.', category='error')
        return redirect(url_for('novo'))

    arquivo_extensao = os.path.splitext(arquivo.filename)[1]

    if not arquivo.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        flash('Formato de arquivo inválido. Envie uma imagem.', category='error')
        return redirect(url_for('novo'))

    if Jogos.query.filter_by(nome=nome).first():
        flash('Jogo já cadastrado', category='error')
        return redirect(url_for('novo'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)

    # Salvar no banco de dados
    db.session.add(novo_jogo)
    db.session.commit()

    # Salvar o arquivo
    arquivo.save(os.path.join(app.config.get('UPLOAD_FOLDER'), f'capa{novo_jogo.id}{arquivo_extensao}'))

    flash('Jogo cadastrado com sucesso!', category='success')
    return redirect(url_for('index'))

@app.route('/login')
def fazer_login():
    proxima = request.args.get('proxima', url_for('index'))
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    input_usuario = request.form.get('usuario')
    input_senha = request.form.get('senha')
    usuario = Usuarios.query.filter_by(nickname=input_usuario).first()

    if usuario:
        if usuario.senha == input_senha:
            session['usuario_logado'] = input_usuario
            proxima_pagina = request.form.get('proxima')
            flash(f'Usuário logado com sucesso: {session["usuario_logado"]}')
            return redirect(proxima_pagina)

        flash('Senha incorreta, tente novamente')
        return redirect(url_for('fazer_login'))
    else:
        flash('Usuário não cadastrado, tente novamente')
        return redirect(url_for('fazer_login'))

@app.route('/logout')
def fazer_logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    jogo = Jogos.query.filter_by(id=id).first()

    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('fazer_login', proxima=url_for('editar', id=id)))
    if jogo:
        return render_template('editar.html', jogo=jogo)
    else:
        flash('Jogo não encontrado!', category='error')
        return redirect(url_for('index'))
    
@app.route('/atualizar', methods=['POST'])
def atualizar():
    jogo_id = request.form.get('id')
    jogo = Jogos.query.filter_by(id=jogo_id).first()
    if jogo:
        jogo.nome = request.form.get('nome')
        jogo.categoria = request.form.get('categoria')
        jogo.console = request.form.get('console')
        db.session.add(jogo)
        db.session.commit()
        flash('Jogos atualizados!')
    else:
        flash('Jogo não encontrado!', category='error')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    try:
        Jogos.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Jogo deletado com sucesso!')
    except:
        db.session.rollback()
        flash('Não foi possível excluir o jogo', category='error')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)