
from flask import Flask, render_template, request

from wtforms import StringField, SubmitField
# from .models import Information
from flask_sqlalchemy import SQLAlchemy
# from flask import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost:3306/urbany'
db = SQLAlchemy()
db.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/form', methods=["POST", "GET"])
def show_form():
    return '''
    <form method="POST" action="/form">
      <h1>Information sur le chantier</h1>

  <label for="nom_du_chantier">Nom du chantier :</label>
  <input type="text" id="nom_du_chantier" name="nom_du_chantier"  required>

  <label for="coordonnees">Coordonnées :</label>
  <input type="text" id="coordonnees" name="coordonnees"  required>

  <label for="proprietaire">Propriétaire :</label>
  <input type="text" id="proprietaire" name="proprietaire">

  <label for="type">Type :</label>
  <input type="text" id="type" name="type">

  <label for="commentaire">Commentaire :</label>
  <textarea id="commentaire" name="commentaire" rows="5" style="width:100%"></textarea>

  <label for="permis">Permis de construire :</label>
  <input type="checkbox" id="permis" name="permis" value="oui" checked>

  <label for="statut">Statut :</label>
  <select id="statut" name="statut">
    <option value="vert">Vert</option>
    <option value="rouge">Rouge</option>
    <option value="orange">Orange</option>
  </select>

  <input type="submit" value="Envoyer">
    </form>   
    '''


# Définit le modèle de données Information
class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coordonnees = db.Column(db.String(50), nullable=False)
    nom_du_chantier = db.Column(db.String(50), nullable=False)
    proprietaire = db.Column(db.String(50))
    type = db.Column(db.String(50))
    commentaire = db.Column(db.String(255))
    permis = db.Column(db.Boolean, nullable=False)
    statut = db.Column(db.Enum('vert', 'rouge', 'orange'), nullable=False)


# Crée la base de données
with app.app_context():
    db.create_all()


# Endpoint pour le formulaire
@app.route('/form', methods=['POST', 'GET'])
def save_form():
    # Si la méthode est POST, traite les données du formulaire
    if request.method == 'POST':
        # Récupère les données du formulaire
        coordonnees = request.form['coordonnees']
        nom_du_chantier = request.form['nom_du_chantier']
        proprietaire = request.form['proprietaire']
        type_de_projet = request.form['type_de_projet']
        commentaire = request.form['commentaire']
        permis = True if request.form.get('permis') else False
        statut = request.form['statut']

        # Vérifie que les données sont valides
        if not coordonnees or not nom_du_chantier or not statut:
            return 'Erreur : certaines données sont manquantes.'
        if len(nom_du_chantier) > 50 or len(type_de_projet) > 50:
            return 'Erreur : le nom du chantier et le type de projet ne doivent pas dépasser 50 caractères.'
        if statut not in STATUTS_POSSIBLES:
            return 'Erreur : statut invalide.'

        # Crée un objet Information à partir des données du formulaire
        information = Information(
            coordonnees=coordonnees,
            nom_du_chantier=nom_du_chantier,
            proprietaire=proprietaire,
            type=type,
            commentaire=commentaire,
            permis=permis,
            statut=statut)

        # Ajoute l'objet à la base de données et valide la transaction
        db.session.add(information)
        db.session.commit()
        return 'Information ajoutée à la base de données !'

    # Si la méthode est GET, affiche le formulaire
    return render_template('information.html')


# Définit les constantes pour les choix possibles de statut
STATUT_VERT = 'vert'
STATUT_ROUGE = 'rouge'
STATUT_ORANGE = 'orange'
STATUTS_POSSIBLES = [STATUT_VERT, STATUT_ROUGE, STATUT_ORANGE]

if __name__ == '__main__':
    # Lance l'application Flask
    app.run()