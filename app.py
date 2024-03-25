import mysql.connector

# Configuration de la connexion à la base de données
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="firstapp"
)

# Création d'un curseur pour exécuter des requêtes SQL
mycursor = mydb.cursor()

# Exécution d'une requête SQL pour récupérer toutes les données de la table "users"
mycursor.execute("SELECT * FROM users")


# Récupération de toutes les données de la table "information"
result = mycursor.fetchall()

# Vérification si le résultat est vide ou non
if len(result) == 0:
  print("Aucun résultat trouvé.")
else:
  # Affichage des données récupérées
  for row in result:
    print(row)