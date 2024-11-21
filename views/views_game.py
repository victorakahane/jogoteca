import os
from flask_wtf import FlaskForm
from flask import (
    render_template, request, redirect, session, flash, url_for, send_from_directory, abort
)
from helpers import FormularioJogo
from main import app, db
from models import Jogos

@app.route('/')
def index():
    lista_jogos = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Novos jogos', jogos=lista_jogos)

@app.route('/novo')
def retornar_pagina_cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('fazer_login', proxima=url_for('retornar_pagina_cadastro')))
    form = FormularioJogo()
    return render_template('cadastrar.html', titulo='Novo Jogo', form=form) 

@app.route('/cadastrar', methods=['POST'])
def cadastrar_jogo():
    form: type[FlaskForm] = FormularioJogo(request.form)

    if not form.validate_on_submit():
        flash('Preencha todos os campos obrigatórios.', category='error')
        return redirect(url_for('retornar_pagina_cadastro'))

    nome = form.nome.data
    console = form.console.data
    categoria = form.categoria.data
    arquivo = request.files.get('foto')

    if Jogos.query.filter_by(nome=nome).first():
        flash('Jogo já cadastrado.', category='error')
        return redirect(url_for('retornar_pagina_cadastro'))

    # Criação do objeto do jogo
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    if arquivo and arquivo.filename:
        # Gerar nome único para o arquivo
        nome_arquivo = f'capa_{novo_jogo.id}.jpg'
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)

        # Salvar o arquivo
        arquivo.save(caminho_arquivo)

        # Atribuir o nome do arquivo ao objeto do jogo
        novo_jogo.caminho_capa = nome_arquivo

    db.session.commit()
    flash('Jogo cadastrado com sucesso!', category='success')
    return redirect(url_for('index'))

@app.route('/logout')
def fazer_logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/editar/<int:jogo_id>')
def editar(jogo_id):
    jogo = Jogos.query.filter_by(id=jogo_id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    form.foto.data = jogo.caminho_capa
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('fazer_login', proxima=url_for('editar', id=jogo_id)))
    if jogo:
        return render_template('editar.html', form=form, id=jogo_id)

    flash('Jogo não encontrado!', category='error')
    return redirect(url_for('index'))

@app.route('/atualizar', methods=['POST'])
def atualizar():
    form: type[FlaskForm] = FormularioJogo(request.form)
    jogo_id = request.form.get('id')
    jogo = Jogos.query.filter_by(id=jogo_id).first()

    if not jogo:
        flash('Jogo não encontrado!', category='error')
        return redirect(url_for('index'))
    if not form.validate_on_submit():
        flash('Informações inváidas!', category='error')
        return redirect(url_for('editar', id=jogo_id))

    arquivo = request.files.get('foto')
    jogo.nome = form.nome.data
    jogo.categoria = form.categoria.data
    jogo.console = form.console.data
    if arquivo and arquivo.filename:
        nome_arquivo = f'capa_{jogo.id}.jpg'
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        arquivo.save(caminho_arquivo)
        jogo.caminho_capa = nome_arquivo

    db.session.add(jogo)
    db.session.commit()
    flash('Jogos atualizados!')
    return redirect(url_for('index'))

@app.route('/deletar/<int:jogo_id>')
def deletar(jogo_id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    # Buscar o jogo no banco de dados
    jogo = Jogos.query.get(jogo_id)
    if not jogo:
        flash('Jogo não encontrado!', category='error')
        return redirect(url_for('index'))

    caminho_capa = jogo.caminho_capa

    try:
        # Deletar o jogo do banco de dados
        db.session.delete(jogo)
        db.session.commit()
        # Verificar se há uma capa associada
        if caminho_capa:
            caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], caminho_capa)
            # Checar se o arquivo existe e deletá-lo
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)

        flash('Jogo deletado com sucesso!', category='success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir o jogo: {str(e)}', category='error')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    # Caminho para a pasta de uploads
    upload_folder = app.config['UPLOAD_FOLDER']
    caminho_arquivo = os.path.join(upload_folder, nome_arquivo)
    # Verifica se o arquivo existe
    if not os.path.isfile(caminho_arquivo):
        # Retorna a capa padrão se o arquivo não existir
        capa_padrao = os.path.join(upload_folder, 'capa_padrao.jpg')
        if os.path.isfile(capa_padrao):
            return send_from_directory(upload_folder, 'capa_padrao.jpg', conditional=True)
        else:
            # Caso a capa padrão também não exista, retorna 404
            abort(404)

    # Retorna o arquivo solicitado
    return send_from_directory(upload_folder, nome_arquivo, conditional=True)
