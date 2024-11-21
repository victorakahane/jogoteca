from flask import render_template, request, redirect, session, flash, url_for
from flask_wtf import FlaskForm
from flask_bcrypt import check_password_hash
from main import app
from models import Usuarios
from helpers import FormularioUsuario

@app.route('/login')
def fazer_login():
    proxima = request.args.get('proxima', url_for('index'))
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    form: type[FlaskForm] = FormularioUsuario(request.form)
    input_usuario = form.nickname.data
    input_senha = form.senha.data
    usuario = Usuarios.query.filter_by(nickname=input_usuario).first()

    if usuario and check_password_hash(usuario.senha, input_senha):
        session['usuario_logado'] = input_usuario
        proxima_pagina = request.form.get('proxima')
        flash(f'Usuário logado com sucesso: {session["usuario_logado"]}')
        return redirect(proxima_pagina)
    elif not usuario:
        flash('Usuário não cadastrado, tente novamente')
        return redirect(url_for('fazer_login'))
    flash('Senha incorreta, tente novamente')
    return redirect(url_for('fazer_login'))
