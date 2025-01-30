from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from requete import configuration_base

app = Flask(__name__)

app.secret_key ='svebberbrb'

# Appel de la fonction de configuration de la base
configuration_base()

# Initialisation de l'instance SQLAlchemy
db = SQLAlchemy(app)

from app import routes
from app import requete

