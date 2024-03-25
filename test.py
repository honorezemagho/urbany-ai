import os
import csv
import exifread
import folium


# Chemin du dossier contenant les images
chemin_dossier = "valu"

# Chemin du fichier CSV pour sauvegarder les coordonnées GPS
chemin_fichier_csv = "coordonnees_gps.csv"


# Ouverture du fichier CSV en mode d'écriture
with open(chemin_fichier_csv, "w", newline="") as fichier_csv:
    # Création d'un objet writer pour écrire les données dans le fichier CSV
    writer = csv.writer(fichier_csv)

    # Création de la carte
    carte = folium.Map(location=[4.0413, 9.7294], zoom_start = 11)

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

                    # Écriture des coordonnées GPS dans le fichier CSV

                    writer.writerow([fichier, latitude, longitude])
                    # creer un lien vers une page web
                    link = f'<iframe src="http://127.0.0.1:5000/formulaire/{longitude}/{latitude}/{fichier}" height="450px" width="450px"></iframe>'
                    # Ajout d'un marqueur sur la carte
                    iframe = folium.IFrame(html=link, width=450, height=500)
                    popup = folium.Popup(iframe, max_width=2650)
                    # form = folium.Popup(
                    #     '<form><input type = "text" name = "name"><br><input type = "submit" value = "soumettre"></form>')
                    marker = folium.Marker([latitude, longitude], popup=fichier)
                    marker.add_child(popup)
                    marker.add_to(carte)



                    # Affichage des coordonnées GPS
                    print(f"Coordonnées GPS de {fichier} : {latitude}, {longitude}")

                else:
                    print(f"Aucune donnée GPS trouvée pour {fichier}.")

# Affichage de la carte
carte.save("carte.html")
