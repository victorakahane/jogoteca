from main import db

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)
    caminho_capa = db.Column(db.String(130), nullable=True, default='capa_padrao.jpg')

    def __repr__(self):
        return '<Name %r>' % self.name