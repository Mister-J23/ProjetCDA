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

#@app.route('/Oeuvres') # decorators
#@login_required_Admin
#def oeuvres():
#    return render_template('Oeuvres.html')

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

