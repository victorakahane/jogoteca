from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
from views.views_user import *
from views.views_game import *
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
