import requests
import time

timestamp = time.time()
date_hour_recup = time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))
date_hour_recup = date_hour_recup.replace('-', '_').replace(' ', '_').replace(':', '_')

url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/csv"
nom_fichier_local = f"prix-des-carburants-en-france-flux-instantane-v2_{date_hour_recup}.csv"

response = requests.get(url)

if response.status_code == 200:
    with open("data/"+ nom_fichier_local, 'wb') as file:
        file.write(response.content)
        print(f"Le fichier a été téléchargé avec succès sous le nom : {nom_fichier_local}")
else:
    print("Échec du téléchargement. Code de statut :", response.status_code)