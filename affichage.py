import requests as request
import mysql.connector

# Connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="urbany"
)


# Récupération des données du formulaire
coordonnees = request.form['coordonnees']
nom_du_chantier = request.form['nom_du_chantier']
proprietaire = request.form['proprietaire']
type = request.form['type']
commentaire = request.form['commentaire']
permis = request.form['permis']
statut = request.form['statut']

# Insertion des données dans la base
cursor = db.cursor()
sql = "INSERT INTO information (coordonnees, nom_du_chantier, proprietaire, type, commentaire, permis, statut) VALUES (%s, %s, %s, %s, %s, %s, %s)"
values = (coordonnees, nom_du_chantier, proprietaire, type, commentaire, permis, statut)
cursor.execute(sql, values)

db.commit()
