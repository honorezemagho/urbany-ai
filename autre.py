import os
import csv
import exifread
import folium

chemin_dossier = "valu"
chemin_fichier_csv = "coordonnees_gps.csv"

with open(chemin_fichier_csv, "w", newline="") as fichier_csv:
    writer = csv.writer(fichier_csv)

# Création de la carte
carte = folium.Map(location=[48.8566, 2.3522], zoom_start=2)

# Itération sur chaque fichier du dossier
for fichier in os.listdir(chemin_dossier):
    if fichier.endswith(".jpg") or fichier.endswith(".jpeg"):
        # Ouverture de la photo
        with open(os.path.join(chemin_dossier, fichier), "rb") as image_file:
            tags = exifread.process_file(image_file)

            # Récupération des coordonnées GPS
            if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
                gps_latitude = tags["GPS GPSLatitude"].values
                gps_latitude_ref = tags["GPS GPSLatitudeRef"].values
                gps_longitude = tags["GPS GPSLongitude"].values
                gps_longitude_ref = tags["GPS GPSLongitudeRef"].values

                # Conversion des minutes et secondes en décimales
                latitude = float(gps_latitude[0].num) / float(gps_latitude[0].den) + \
                           float(gps_latitude[1].num) / (60.0 * float(gps_latitude[1].den)) + \
                           float(gps_latitude[2].num) / (3600.0 * float(gps_latitude[2].den))
                longitude = float(gps_longitude[0].num) / float(gps_longitude[0].den) + \
                            float(gps_longitude[1].num) / (60.0 * float(gps_longitude[1].den)) + \
                            float(gps_longitude[2].num) / (3600.0 * float(gps_longitude[2].den))

                # Ajout d'un marqueur sur la carte x
                folium.Marker([latitude, longitude], popup=fichier).add_to(carte)

                # Écriture des coordonnées GPS dans le fichier CSV
                writer.writerow([fichier, latitude, longitude])

# Affichage de la carte
carte.save("carte.html")