from flask import Flask, render_template,jsonify, send_file, abort, redirect, url_for, request
from sqlalchemy import text
from app import app, db
import io



@app.route('/')
def Connexion():
    return render_template('connexion.html')


@app.route('/Erreur/<int:nb>')
def Erreur(nb):
    if nb==0:
        mes= ""
    if nb==1:
        mes= "Problème de connexion"
    if nb==2:
        mes= "Nom d'utilisateur ou Mot de passe non valide"
    return mes



@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Vérifier les informations d'identification dans la base de données
    user = db.session.execute(
        text("SELECT * FROM users WHERE username = :username AND password = :password"),
        {'username': username, 'password': password}
    ).fetchone()

    if user:
        return redirect(url_for('Home'))  # Rediriger vers la page d'accueil après connexion
    
    else :
        
        return render_template('connexion.html',message=Erreur(2))


@app.route('/Home') # decorators
def Home():
    return render_template('Test.html')

@app.route('/audio/<int:id>')
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

@app.route('/images') # decorators
def Personnages():
    return render_template('Personnages.html')

@app.route('/Vidéos') # decorators
def Vidéos():
    return render_template('Vidéos.html')

@app.route('/Contact') # decorators
def Contact():
    return render_template('Contact.html')

@app.route('/index')
def index():
    strResult = 'Hello Bruz!'
    return strResult