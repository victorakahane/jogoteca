
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, FileField
from flask_wtf.file import FileAllowed

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    foto = FileField(
        'Escolha uma imagem',
        validators=[
            FileAllowed(['jpg', 'png', 'jpeg'], 'Somente imagens são permitidas!')
        ]
    )
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')