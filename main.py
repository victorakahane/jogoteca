from flask import Flask, render_template, request, redirect, session, flash, url_for
from jogo import Jogo
from usuario import Usuario

app = Flask(__name__)
app.secret_key = 'teste123'
jogo1 = Jogo('Roblox', 2006, ['PC', 'PS4', 'XBOX'], 'Infantil')
jogo2 = Jogo('Minecraft', 2009, ['PC', 'PS4', 'XBOX', 'Android'], 'Sandbox')
jogo3 = Jogo('Outlast', 2016, ['PC'], 'Terror')
lista_jogos = [jogo1, jogo2, jogo3]
usuario1 = Usuario('Teste', 'test', '12345')
usuario2 = Usuario('Victor', 'corinthians', 'depay')
usuario3 = Usuario('Outro', 'outro', 'abcd')
lista_usuarios = [usuario1, usuario2, usuario3]
usuarios = {}
for usuario in lista_usuarios:
    usuarios[usuario.nickname] = usuario


@app.route('/')
def index():
    return render_template('lista.html', titulo='Novos jogos', jogos=lista_jogos)

@app.route('/formulario_cadastro')
def retornar_pagina_cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('fazer_login', proxima=url_for('retornar_pagina_cadastro')))
        # return redirect('/login?proxima=formulario_cadastro')
    plataformas = ['ps4', 'xbox360', 'ps3', 'pc', 'android', 'ios', 'xbox one']
    return render_template('cadastrar.html', titulo='Cadastro de Jogo', plataformas=plataformas)

@app.route('/cadastrar', methods=['POST'])
def cadastrar_jogo():
    nome = request.form.get('nome')
    ano_lancamento = request.form.get('ano_lancamento')
    plataformas = request.form.getlist('plataformas')
    categoria = request.form.get('categoria')
    lista_jogos.append(Jogo(nome, ano_lancamento, plataformas, categoria))
    return redirect('/')

@app.route('/login')
def fazer_login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    input_usuario = request.form.get('usuario')
    input_senha = request.form.get('senha')
    if input_usuario in usuarios:
        usuario: type[Usuario] = usuarios[input_usuario]
        if input_senha == usuario.senha:
            session['usuario_logado'] = input_usuario
            proxima_pagina = request.form.get('proxima')
            flash(f'Usuário logado com sucesso: {session["usuario_logado"]}')
            return redirect(proxima_pagina)
    
    flash(f'Senha incorreta, tente novamente')
    return redirect(url_for('fazer_login'))

@app.route('/logout')
def fazer_logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)