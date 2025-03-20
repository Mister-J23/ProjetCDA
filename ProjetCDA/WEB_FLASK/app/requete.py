from flask import redirect, url_for, session, render_template
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
            text("SELECT * FROM users WHERE name = :username"),
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
            session['id']=utilisateur.id_user
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
        
        try:
            # Récupère le lien de l'audio depuis la base de données
            resultat = self.session_db.execute(
                text("SELECT id_audio, speech_link FROM audios WHERE id_author = :id"),
                {'id': id}
            ).fetchone()
            # Retourne l'ID et le lien audio sous forme de dictionnaire ou tuple
            return {'id_audio': resultat[0], 'speech_link': resultat[1]}  # Retourne un dictionnaire avec l'ID et le lien
        except SQLAlchemyError as e:
            print(f"❌ Erreur SQL : {str(e)}")
            return None

    def obtenir_lien_photo(self, id):
        # Récupère le lien de la photo depuis la base de données
        resultat = self.session_db.execute(
            text("SELECT picture_link FROM authors WHERE id_author = :id"),
            {'id': id}
        ).fetchone()
        return resultat[0] if resultat else None
    
    def obtenir_lien_bio(self, id):
        # Récupère le lien du fichier pdf depuis la base de données
        resultat = self.session_db.execute(
            text("SELECT link_text FROM bios WHERE id_author = :id"),
            {'id': id}
        ).fetchone()
        return resultat[0] if resultat else None
    
    def obtenir_lien_photoOeuvre(self, id):
        # Récupère le lien du fichier pdf depuis la base de données
        resultat = self.session_db.execute(
            text("SELECT link_photo FROM bios WHERE id_author= :id"),
            {'id': id}
        ).fetchone()
        return resultat[0] if resultat else None
    
    def obtenir_personnages(self):
        try:
            # Récupérer toutes les données de la table "authors"
            resultat = db.session.execute(text("SELECT * FROM authors")).fetchall()
            return resultat  # Retourne la liste des personnages
        except SQLAlchemyError as e:
            return f"Erreur lors de la récupération des items : {str(e)}"

                

media = Media(db.session)

class Allimentation:
    def __init__(self, session_db):
        self.session_db = session_db  # Ici on stocke la session DB dans l'attribut self.session_db
    
    def inserer_auteur(self, name, birth, dead, picture_link, id_lead):
        try:
            resultat = self.session_db.execute(
                text("INSERT INTO authors (name, birth, dead, picture_link, id_lead) VALUES (:nom, :naissance, :mort, :photo, :lead)"),
                {'nom': name, 'naissance': birth, 'mort': dead, 'photo': picture_link, 'lead':id_lead}
            )
            return resultat.lastrowid  # Retourne l'ID de la ligne ajoutée 
        except SQLAlchemyError as e:
            print(f"❌ Erreur SQL : {str(e)}")
            return None
    
    def inserer_audio(self, speech_link, _date, id_author):
        try:
            resultat = db.session.execute(
                    text("INSERT INTO audios (speech_link, _date, id_author) VALUES (:audio, :tempo, :auteur_id)"),
                    {'audio': speech_link, 'tempo': _date, 'auteur_id': id_author}
                )
            return resultat.rowcount  # Retourne True
        except SQLAlchemyError as e:
            print(f"❌ Erreur SQL : {str(e)}")
            return None
        
    def inserer_bio(self, link_text, _date, id_author):
        try:
            resultat = db.session.execute(
                    text("INSERT INTO bios (link_text, _date, id_author) VALUES (:audio, :tempo, :auteur_id)"),
                    {'audio': link_text, 'tempo': _date, 'auteur_id': id_author}
                )
            return resultat.rowcount  # Retourne True
        except SQLAlchemyError as e:
            print(f"❌ Erreur SQL : {str(e)}")
            return None
    def inserer_commentaire(self, date_comment, comment, id_user, id_audio):
        try:
            resultat = db.session.execute(
                    text("INSERT INTO comments (date_comment, comment, id_user, id_audio) VALUES (:V1, :V2, :V3, :V4)"),
                    {'V1': date_comment, 'V2': comment, 'V3': id_user, 'V4':id_audio}
                )
            print("Insertion réussie !")
            return resultat.rowcount # Retourne True
        except SQLAlchemyError as e:
            print("!!!!!!!!!Echec!!!!!!!!!!! !")
            print(f"❌ Erreur SQL : {str(e)}")
            return None

    def inserer_courant(self, lead_name, link_text):
        try:
            resultat = db.session.execute(
                    text("INSERT INTO _lead (lead_name, link_text) VALUES (:courant, :lien)"),
                    {'courant': lead_name, 'lien': link_text}
                )
            print("Insertion réussie !")
            return resultat.rowcount # Retourne True
        except SQLAlchemyError as e:
            print("!!!!!!!!!Echec!!!!!!!!!!! !")
            print(f"❌ Erreur SQL : {str(e)}")
            return None


insert = Allimentation(db.session)

class Acquisition:
    def __init__(self, session_db):
        self.session_db = session_db  # Ici on stocke la session DB dans l'attribut self.session_db
    
    def select_courant(self):
        try:
            resultat = db.session.execute(text("SELECT id_lead,lead_name FROM _lead")).fetchall()
            return resultat #Renvoyer la liste des noms de courant philosophique
        except SQLAlchemyError as e:
            return f"Erreur lors de la récupération : {str(e)}"
        
acquis = Acquisition(db.session)

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