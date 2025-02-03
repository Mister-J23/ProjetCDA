from flask import Flask, render_template,jsonify, send_file, abort, redirect, url_for, request, session, flash
from sqlalchemy import text
from app import app, db
from werkzeug.security import check_password_hash
from datetime import datetime
import io
from app.routes import login_required, login_required_Admin, Erreur



#Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Récupérer l'utilisateur dans la base de données
    user = db.session.execute(
        text("SELECT name, _group, password FROM users WHERE name = :username"),
        {'username': username}
    ).fetchone()

    if user and check_password_hash(user.password, password):  # Vérifier le hash
        # Ajouter l'utilisateur à la session
        session['username'] = user.name
        session['groupe'] = user._group
        print(session)  
        return redirect(url_for('Home'))  # Rediriger vers la page d'accueil
    
    return render_template('connexion.html', message="Identifiants incorrects")


# Get Audio
@app.route('/audio/<int:id>')
@login_required
def get_audio(id):
    try:
        # Récupérer l'image depuis la base de données
        result = db.session.execute(text("SELECT speech_link FROM audios WHERE id_author = :id"), {'id': id}).fetchone()
        
        if result is None or result[0] is None:
            abort(404, description="Image non trouvée.")

        # Convertir le BLOB en un objet d'entrée de fichier
        return redirect(result[0])


    except Exception as e:
        return f"Erreur lors de la récupération de l'image : {str(e)}"
    

#Get photo extrait-audio
@app.route('/photo/<int:id>')
@login_required
def get_photo(id):
    try:
        result = db.session.execute(
            text("SELECT picture_link FROM authors WHERE id_author = :id"),
            {'id': id}
        ).fetchone()

        if result is None or result[0] is None:
            abort(404, description="Image non trouvée.")

        # Rediriger vers l'URL de l'image
        return redirect(result[0])

    except Exception as e:
        abort(500, description=str(e))
        

#Get photo Oeuvres
@app.route('/photoOeuvres/<int:id>')
@login_required
def get_photoOeuvres(id):
    try:
        # Récupérer l'image depuis la base de données
        result = db.session.execute(text("SELECT photo FROM Oeuvres WHERE Id = :id"), {'id': id}).fetchone()
        
        if result is None or result[0] is None:
            abort(404, description="Image non trouvée.")

        # Convertir le BLOB en un objet d'entrée de fichier
        image_data = result[0]
        return send_file(io.BytesIO(image_data), mimetype='image/mpeg')  # Remplacez 'image/jpeg' par le type MIME approprié si nécessaire

    except Exception as e:
        return f"Erreur lors de la récupération de l'image : {str(e)}"
    

@app.route('/delete/<int:id>', methods=['POST']) #Supprimer des éléments de la base
def delete_item(id):
    # Supprimer l'élément de la base de données
    db.session.execute(text("DELETE FROM authors WHERE id_author = :id"), {'id': id})
    db.session.commit()
    flash('Élément supprimé avec succès.', 'success')
    return redirect(url_for('personnages'))






# Charger
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
        photo = '/static/photo/' + request.form['photo'] + '.jpg'
        audio = '/static/audio/' + request.form['audio'] + '.mp3'


       

        

        # Insérer les données dans la base de données avec des paramètres sécurisés
        if db.session.execute(
            text("INSERT INTO authors (name, birth, dead, picture_link) VALUES (:nom, :naissance, :mort, :photo)"),
            {'nom': nom, 'naissance': naissance, 'mort': mort, 'photo': photo}
        ):
            
            db.session.commit()  # Valide les changements

            # Récupérer l'ID de l'auteur à partir du nom
            result = db.session.execute(
                text("SELECT id_author FROM authors WHERE name = :nom LIMIT 1"),
                {'nom': nom}
            ).fetchone()

            # Vérifier si un auteur a été trouvé
            if result:
                auteur_id = result[0]  # Extraire l'ID de l'auteur depuis la tuple
            else:
                auteur_id = None  # Si aucun auteur n'est trouvé, définir auteur_id sur None

            # Récupérer l'heure actuelle
            tempo = datetime.now()

            # Vérifier que l'ID de l'auteur existe avant d'insérer dans la table audios
            if auteur_id:
                db.session.execute(
                    text("INSERT INTO audios (speech_link, _date, id_author) VALUES (:audio, :tempo, :auteur_id)"),
                    {'audio': audio, 'tempo': tempo, 'auteur_id': auteur_id}
                )
                db.session.commit()  # Commit de la transaction
            else:
                # Gérer le cas où aucun auteur n'a été trouvé
                print("Auteur non trouvé pour le nom :", nom)
            return redirect(url_for('personnages'))
        
        return redirect(url_for('Erreur', nb=5))
    elif request.method == 'GET':
        return redirect(url_for('Erreur', nb=4))
    