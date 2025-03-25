from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.secret_key ='svebberbrb'


# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:uimm@localhost/philo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB


# Initialisation de l'instance SQLAlchemy
db = SQLAlchemy(app)

from app import routes
from app import requete

