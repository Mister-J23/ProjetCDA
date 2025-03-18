from flask import redirect, url_for, session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app import app, db
from werkzeug.security import check_password_hash
from functools import wraps


def login_required(f):#Nécessite une connexion
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'groupe' not in session:  # Vérifie si l'utilisateur est connecté
            return redirect(url_for('Connexion'))  # Rediriger vers la page de connexion si non connecté
        return f(*args, **kwargs)
    return decorated_function

def login_required_Admin(f):  # Nécessite une connexion
    @wraps(f)
    def decorated_function_Admin(*args, **kwargs):
        # Vérifie si l'utilisateur est connecté et s'il fait partie du groupe Admin
        if 'groupe' not in session or session['groupe'] != 'Admin':
            return redirect(url_for('Erreur', nb=3))  # Redirection vers la page d'erreur
        return f(*args, **kwargs)
    return decorated_function_Admin


#Objet utilisateur
class Connexion:
    def __init__(self, session_db):
        self.session_db = session_db  # Ici on stocke la session DB dans l'attribut self.session_db

    def obtenir_utilisateur(self, nom_utilisateur):
        # Utilisation de la session DB pour récupérer les données
        resultat = self.session_db.execute(
            text("SELECT name, _group, password FROM users WHERE name = :username"),
            {'username': nom_utilisateur}
        ).fetchone()
        return resultat

    def verifier_mot_de_passe(self, mot_de_passe_stocke, mot_de_passe_saisi):
        # Vérification du mot de passe
        return check_password_hash(mot_de_passe_stocke, mot_de_passe_saisi)

    def se_connecter(self, nom_utilisateur, mot_de_passe):
        # Utilisation de la méthode obtenir_utilisateur pour vérifier l'utilisateur
        utilisateur = self.obtenir_utilisateur(nom_utilisateur)
        if utilisateur and self.verifier_mot_de_passe(utilisateur.password, mot_de_passe):
            session['username'] = utilisateur.name
            session['groupe'] = utilisateur._group
            return True
        return False
user = Connexion(db.session)

#
class Media:
    def __init__(self, session_db):
        self.session_db = session_db  # Ici on stocke la session DB dans l'attribut self.session_db

    def obtenir_lien_audio(self, id):
        # Récupère le lien de l'audio depuis la base de données
        resultat = self.session_db.execute(
            text("SELECT speech_link FROM audios WHERE id_author = :id"),
            {'id': id}
        ).fetchone()
        return resultat[0] if resultat else None

    def obtenir_lien_photo(self, id):
        # Récupère le lien de la photo depuis la base de données
        resultat = self.session_db.execute(
            text("SELECT picture_link FROM authors WHERE id_author = :id"),
            {'id': id}
        ).fetchone()
        return resultat[0] if resultat else None

media = Media(db.session)

class Allimentation:
    def __init__(self, session_db):
        self.session_db = session_db  # Ici on stocke la session DB dans l'attribut self.session_db
    
    def inserer_auteur(self, name, birth, dead, picture_link):
        try:
            resultat = self.session_db.execute(
                text("INSERT INTO authors (name, birth, dead, picture_link) VALUES (:nom, :naissance, :mort, :photo)"),
                {'nom': name, 'naissance': birth, 'mort': dead, 'photo': picture_link}
            )
            return resultat.lastrowid  # Retourne True
        except SQLAlchemyError as e:
            return f"Erreur lors de l'insertion : {str(e)}"
    
    def inserer_audio(self, speech_link, _date, id_author):
        try:
            resultat = db.session.execute(
                    text("INSERT INTO audios (speech_link, _date, id_author) VALUES (:audio, :tempo, :auteur_id)"),
                    {'audio': speech_link, 'tempo': _date, 'auteur_id': id_author}
                )
            self.session_db.commit()  # Valider l'insertion dans la base
            return True  # Retourne True
        except SQLAlchemyError as e:
            self.session_db.rollback()  # Annuler la transaction en cas d'erreur
            return f"Erreur lors de l'insertion : {str(e)}"


insert = Allimentation(db.session)

class Modification:
    def __init__(self, session_db):
        self.session_db = session_db  # Ici on stocke la session DB dans l'attribut self.session_db

    def update_image(self, name, birth, dead, picture_link):
        try:
            resultat = self.session_db.execute(
                text("INSERT INTO authors (name, birth, dead, picture_link) VALUES (:nom, :naissance, :mort, :photo)"),
                {'nom': name, 'naissance': birth, 'mort': dead, 'photo': picture_link}
            )
            return resultat.lastrowid  # Retourne True
        except SQLAlchemyError as e:
            return f"Erreur lors de l'insertion : {str(e)}"