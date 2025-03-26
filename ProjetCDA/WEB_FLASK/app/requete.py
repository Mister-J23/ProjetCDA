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

            # Si aucun résultat, renvoie un dictionnaire avec une erreur
            if not resultat:
                return {"error": "Biographie non trouvée"}  # Retourner un message d'erreur sous forme de dictionnaire

            # Retourne l'ID et le lien bio sous forme de dictionnaire
            return {'id_audio': resultat[0], 'speech_link': resultat[1]}
        
        except SQLAlchemyError as e:
            print(f"❌ Erreur SQL : {str(e)}")
            return {"error": f"Erreur lors de la récupération de l'audio : {str(e)}"}  # Retourne une erreur


    def obtenir_lien_photo(self, id):
        # Récupère le lien de la photo depuis la base de données
        resultat = self.session_db.execute(
            text("SELECT picture_link FROM authors WHERE id_author = :id"),
            {'id': id}
        ).fetchone()
        return resultat[0] if resultat else None
    
    def obtenir_lien_bio(self, id):
        try:
            # Récupère le lien de l'audio depuis la base de données
            resultat = self.session_db.execute(
                text("SELECT id_bio, link_text FROM bios WHERE id_author = :id"),
                {'id': id}
            ).fetchone()

            # Si aucun résultat, renvoie un dictionnaire avec une erreur
            if not resultat:
                return {"error": "Biographie non trouvée"}  # Retourner un message d'erreur sous forme de dictionnaire

            # Retourne l'ID et le lien bio sous forme de dictionnaire
            return {'id_bio': resultat[0], 'link_text': resultat[1]}
        
        except SQLAlchemyError as e:
            print(f"❌ Erreur SQL : {str(e)}")
            return {"error": f"Erreur lors de la récupération de la biographie : {str(e)}"}  # Retourne une erreur

    
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
            return f"❌ Erreurlors de la récupération des items : {str(e)}"

                

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
        

    def inserer_commentaire_audio(self, date_comment, comment, id_user, id_audio):
        try:
            resultat = db.session.execute(
                    text("INSERT INTO comments (date_comment, comment, id_user, id_audio) VALUES (:V1, :V2, :V3, :V4)"),
                    {'V1': date_comment, 'V2': comment, 'V3': id_user, 'V4':id_audio}
                )
            print("Insertion réussie !")
            return resultat.rowcount  # Retourne True
        except SQLAlchemyError as e:
            print(f"❌ Erreur SQL : {str(e)}")
            return None
        
    def inserer_commentaire_bio(self, date_comment, comment, id_user, id_bio):
        try:
            resultat = db.session.execute(
                    text("INSERT INTO comments (date_comment, comment, id_user, id_bio) VALUES (:V1, :V2, :V3, :V4)"),
                    {'V1': date_comment, 'V2': comment, 'V3': id_user, 'V4':id_bio}
                )
            print("Insertion réussie !")
            if resultat.rowcount > 0: 
                return "✅ Commentaire inséré avec succès"
        except SQLAlchemyError as e:
            print("!!!!!!!!!Echec!!!!!!!!!!! !")
            print(f"❌ Erreur SQL : {str(e)}")
            return f"❌ Erreurlors de l'insertion du commentaire' : {str(e)}"

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
        
    def inserer_utilisateur(self, name, password, group):
        try:
            resultat = db.session.execute(
                    text("INSERT INTO users (name, password, _group) VALUES (:V1, :V2, :V3)"),
                    {'V1': name, 'V2': password, 'V3': group}
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
            return f"❌ Erreurlors de la récupération des courants: {str(e)}"
        
    def select_utilisateurs(self):
        try:
            resultat = db.session.execute(text("SELECT id_user, name, password, _group FROM users")).fetchall()
            return resultat #Renvoyer la liste des noms de courant philosophique
        except SQLAlchemyError as e:
            return f"❌ Erreur lors de la récupération des utilisateurs : {str(e)}"
    def select_nomutilisateurs(self, id):
        try:
            resultat = db.session.execute(
                text("SELECT name FROM users WHERE id_user = :id"),
                {'id': id}
            ).fetchone()
            
            # Si aucun utilisateur n'est trouvé, on retourne None
            if not resultat:
                return "Utilisateur suprimé"
            
            # On retourne le nom sous forme de chaîne (en supposant que le résultat est une ligne de type Row)
            return resultat[0]  # Nous extrayons juste le nom de l'utilisateur (la première colonne)
        
        except SQLAlchemyError as e:
            return f"❌ Erreur lors de la récupération de l'utilisateur : {str(e)}"

        
    def select_groupe(self):
        try:
            resultat = db.session.execute(text("SELECT DISTINCT _group FROM users")).fetchall()
            return resultat #Renvoyer la liste des noms de courant philosophique
        except SQLAlchemyError as e:
            return f"❌ Erreurlors de la récupération des groupes : {str(e)}"
        
    def select_commentaire_bio(self, id):
        try:
            resultat = db.session.execute(
                text("SELECT id_comment, comment, date_comment, id_user FROM comments WHERE id_bio = :id"),
                {'id': id}
            ).fetchall()
            
            # Vérifie si aucun commentaire n'a été trouvé
            if not resultat:
                return []  # Retourne une liste vide si aucun commentaire n'est trouvé
            
            # Convertit le résultat en une liste de dictionnaires
            commentaires = [
                {"id_comment": row[0], "comment": row[1], "date_comment": row[2], "id_user": row[3]}
                for row in resultat
            ]
            print("👍 Liste des commentaires récupéré")

            return commentaires
        except SQLAlchemyError as e:
            return f"❌ Erreur lors de la récupération des commentaires : {str(e)}"
        
    def select_commentaire_audio(self, id):
        try:
            resultat = db.session.execute(
                text("SELECT id_comment, comment, date_comment, id_user FROM comments WHERE id_audio = :id"),
                {'id': id}
            ).fetchall()
            
            # Vérifie si aucun commentaire n'a été trouvé
            if not resultat:
                return []  # Retourne une liste vide si aucun commentaire n'est trouvé
            
            # Convertit le résultat en une liste de dictionnaires
            commentaires = [
                {"id_comment": row[0], "comment": row[1], "date_comment": row[2], "id_user": row[3]}
                for row in resultat
            ]
            print("👍 Liste des commentaires récupéré")

            return commentaires
        except SQLAlchemyError as e:
            return f"❌ Erreur lors de la récupération des commentaires : {str(e)}"

        
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
            return f"❌ Erreurlors de l'insertion : {str(e)}"
        
class Suppression:
    def __init__(self, session_db):
        self.session_db = session_db  # Ici on stocke la session DB dans l'attribut self.session_db
    
    def supprimer_commentaire(self, id_comment, id_user): #la méthode qui permet de supprimer un commentaire
        try:
            result=db.session.execute(
                    text("""
                        DELETE FROM comments 
                        WHERE id_comment = :id_comment 
                        AND (
                            (SELECT _group FROM users WHERE id_user = :id_user) = 'Admin'
                            OR id_user = :id_user
                        )
                    """),
                    {"id_comment": id_comment, "id_user": id_user}
                )
            db.session.commit()
            if result.rowcount > 0:  # Vérifie si au moins une ligne a été supprimée
                
                print("👍 Suppresion effectuée")
                return "✅ Commentaire supprimé avec succès"
            else:
                return "❌ Aucun commentaire supprimé (ID incorrect ou droits insuffisants)"
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return f"❌ Erreur lors de la suppression du commentaire : {str(e)}"
        
    def supprimer_utilisateur(self, id_user): #la méthode qui permet de supprimer un user
        try:
            result=db.session.execute(
                    text("""
                        DELETE FROM users 
                        WHERE id_user = :id_user 
                    """),
                    {"id_user": id_user}
                )
            db.session.commit()
            if result.rowcount > 0:  # Vérifie si au moins une ligne a été supprimée
                
                print("👍 Suppresion effectuée")
                return "✅ Utilisateur supprimé avec succès"
            else:
                return "❌ Aucun Utilisateur supprimé (ID incorrect ou droits insuffisants)"
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return f"❌ Erreur lors de la suppression de l'Utilisateur : {str(e)}"
        
supp = Suppression(db.session)

