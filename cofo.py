import folium
import mysql.connector
import pandas as pd

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flaskapp"
)

# Extraction des données géospatiales sous forme de DataFrame Pandas
df = pd.read_sql_query("SELECT * FROM users", conn)

# Conversion des données géospatiales en GeoJSON
geojson_data = df.to_json()

# Création d'une carte Folium centrée sur les coordonnées moyennes des points
map_center = [df['Email'].mean(), df['password'].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Ajout des données géospatiales à la carte
folium.GeoJson(geojson_data).add_to(m)

# Affichage de la carte
m