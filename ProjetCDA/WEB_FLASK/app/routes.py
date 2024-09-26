from flask import Flask, render_template,jsonify, send_file, abort, redirect, url_for, request, session, flash
from sqlalchemy import text
from app import app, db
from functools import wraps
import io


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




@app.route('/')
def Connexion():
    return render_template('connexion.html')


@app.route('/Déconnexion')
def déconnexion():

    # Supprimer la session
    session.clear()
    print(session)
    return redirect(url_for('Connexion'))  # Redirection vers la page de connexion
    


@app.route('/Erreur/<int:nb>')
def Erreur(nb):
    if nb==0:
        mes= ""
    if nb==1:
        mes= "Problème de connexion"
    if nb==2:
        mes= "Nom d'utilisateur ou Mot de passe non valide"
    if nb==3:
        mes= "Page réservé aux administrateurs"
    if nb==4:
        mes= "Le POST n'a pas marché"
    if nb==5:
        mes= "Le POST a marché mais pas la requête"
    return mes



@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Vérifier les informations d'identification dans la base de données
    user = db.session.execute(
        text("SELECT username, groupe FROM users WHERE username = :username AND password = :password"),
        {'username': username, 'password': password}
    ).fetchone()

    if user:
         # Ajouter l'utilisateur à la session
        session['username'] = user.username  # Assurez-vous que 'user.id' est bien récupéré de la base de données
        session['groupe']=user.groupe
        print(session) 
        return redirect(url_for('Home'))  # Rediriger vers la page d'accueil après connexion
    
    else :
        
        return render_template('connexion.html',message=Erreur(2))


@app.route('/Home') # decorators
@login_required
def Home():
    return render_template('Test.html')



@app.route('/Personnage')
@login_required
def personnages():
    # Récupérer toutes les images et fichiers audio
    all_items = db.session.execute(text("SELECT * FROM extrait_audio")).fetchall()
    return render_template('Personnages.html', items=all_items)

@app.route('/audio/<int:id>')
@login_required
def get_audio(id):
    try:
        # Récupérer l'image depuis la base de données
        result = db.session.execute(text("SELECT audio FROM extrait_audio WHERE Id = :id"), {'id': id}).fetchone()
        
        if result is None or result[0] is None:
            abort(404, description="Image non trouvée.")

        # Convertir le BLOB en un objet d'entrée de fichier
        image_data = result[0]
        return send_file(io.BytesIO(image_data), mimetype='audio/mp3')  # Remplacez 'image/jpeg' par le type MIME approprié si nécessaire

    except Exception as e:
        return f"Erreur lors de la récupération de l'image : {str(e)}"

@app.route('/photo/<int:id>')
@login_required
def get_photo(id):
    try:
        # Récupérer l'image depuis la base de données
        result = db.session.execute(text("SELECT photo FROM extrait_audio WHERE Id = :id"), {'id': id}).fetchone()
        
        if result is None or result[0] is None:
            abort(404, description="Image non trouvée.")

        # Convertir le BLOB en un objet d'entrée de fichier
        image_data = result[0]
        return send_file(io.BytesIO(image_data), mimetype='image/mpeg')  # Remplacez 'image/jpeg' par le type MIME approprié si nécessaire

    except Exception as e:
        return f"Erreur lors de la récupération de l'image : {str(e)}"

@app.route('/charge', methods=['POST','GET'])
@login_required_Admin
def charge():

    print("La méthode charge() a été appelée")
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        naissance = request.form['naissance']
        mort = request.form['mort']

        # Récupérer les fichiers uploadés
        photo = request.files['photo']
        audio = request.files['audio']

        # Lire le contenu des fichiers sous forme binaire
        
        photo_data = photo.read()
        audio_data = audio.read()


        # Insérer les données dans la base de données avec des paramètres sécurisés
        if db.session.execute(
            text("INSERT INTO extrait_audio (nom, naissance, mort, photo, audio) VALUES (:nom, :naissance, :mort, :photo, :audio)"),
            {'nom': nom, 'naissance': naissance, 'mort': mort, 'photo': photo_data, 'audio': audio_data}
        ):
            
            db.session.commit()  # Valide les changements
            return redirect(url_for('personnages'))
        
        return redirect(url_for('Erreur', nb=5))
    elif request.method == 'GET':
        return redirect(url_for('Erreur', nb=4))
    
@app.route('/Chargement') # Charger des éléments dans la base
@login_required_Admin
def Page_chargement():
    return render_template('charger.html')

@app.route('/delete/<int:id>', methods=['POST']) #Supprimer des éléments de la base
def delete_item(id):
    # Supprimer l'élément de la base de données
    db.session.execute(text("DELETE FROM extrait_audio WHERE id = :id"), {'id': id})
    db.session.commit()
    flash('Élément supprimé avec succès.', 'success')
    return redirect(url_for('personnages'))



@app.route('/Oeuvres') # decorators
@login_required_Admin
def oeuvres():
    return render_template('Oeuvres.html')

@app.route('/Contact') # decorators
def Contact():
    return render_template('Contact.html')

# Désactiver le cache pour toutes les pages si l'utilisateur est connecté
@app.after_request
def add_header(response):
    if 'username' in session:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response