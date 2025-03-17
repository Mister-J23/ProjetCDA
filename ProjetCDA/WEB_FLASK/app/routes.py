from flask import Flask, render_template, abort, redirect, url_for, request, session, flash
from sqlalchemy import text
from app import app, db
from app.requete import login_required, login_required_Admin, media, user, insert
from datetime import datetime





#Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    lien = user.se_connecter(username, password)
    if lien :
        return redirect(url_for('Home'))  # Rediriger vers la page d'accueil
    return render_template('connexion.html', message="Identifiants incorrects")





@app.context_processor
def inject_user():
    return dict(
        username=session.get('username'), 
        groupe=session.get('groupe')
    )


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





@app.route('/Home') # decorators
@login_required
def Home():
    return render_template('Home.html')



@app.route('/Personnage')
@login_required
def personnages():
    # Récupérer toutes les images et fichiers audio
    all_items = db.session.execute(text("SELECT * FROM authors")).fetchall()
    # Afficher le contenu pour débogage
    return render_template('Personnages.html', items=all_items)


@app.route('/Oeuvres')
@login_required
def Oeuvres():
    # Récupérer toutes les images et fichiers audio
    all_fig = db.session.execute(text("SELECT * FROM bios")).fetchall()
    return render_template('Oeuvres.html', figs=all_fig)



@app.route('/Chargement') # Charger des éléments dans la base
@login_required_Admin
def Page_chargement():
    return render_template('charger.html')



# Get Audio
@app.route('/audio/<int:id>')
@login_required
def get_audio(id):
    lien = media.obtenir_lien_audio(id)
    if lien:
        return redirect(lien)  # Redirection vers le lien du fichier audio
    return "Audio introuvable", 404


#Get photo extrait-audio
@app.route('/photo/<int:id>')
@login_required
def get_photo(id):
    lien = media.obtenir_lien_photo(id)
    if lien:
        return redirect(lien)  # Redirection vers le lien du fichier audio
    return "Photo introuvable", 404
        

#Get photo Oeuvres
@app.route('/photoOeuvres/<int:id>')
@login_required
def get_photoOeuvres(id):
    try:
        result = db.session.execute(
            text("SELECT link_photo FROM bios WHERE id_bio= :id"),
            {'id': id}
        ).fetchone()

        if result is None or result[0] is None:
            abort(404, description="Image non trouvée.")

        # Rediriger vers l'URL de l'image
        return redirect(result[0])

    except Exception as e:
        abort(500, description=str(e))
    

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

        # Récupérer l'heure actuelle
        tempo = datetime.now()

        # Insérer l'auteur et récupérer l'ID retourné
        id_auteur = insert.inserer_auteur(nom, naissance, mort, photo)

        # Vérifier si l'insertion de l'auteur a réussi
        if isinstance(id_auteur, int):  # Vérifie que l'ID retourné est bien un entier
            if insert.inserer_audio(audio, tempo, id_auteur): #insérer l'audio
                db.session.commit()  # Valider l'insertion dans la base
                return render_template('charger.html', message=f"Auteur {nom}, ID: {id_auteur} ajouté avec succès ")
            else:
                db.session.rollback()  # Annuler la transaction en cas d'erreur
                return render_template('charger.html', message="Erreur lors de l'ajout de l'audio")
            
        else:
            db.session.rollback()  # Annuler la transaction en cas d'erreur
            return render_template('charger.html', message="Erreur lors de l'ajout de l'auteur")






       
    
    


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

