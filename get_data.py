# ------------------------------------------------------------------------------
# Description : This script gets the data from the API and saves it locally.
# ------------------------------------------------------------------------------

# Import libraries
import requests

# Define the url and the name of the file
url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/csv"
nom_fichier_local = f"prix-des-carburants-en-france-flux-instantane-v2.csv"

response = requests.get(url)

# Check if the request was successful, and if so, write the file and if not, print the error code
if response.status_code == 200:
    with open("data/"+ nom_fichier_local, 'wb') as file:
        file.write(response.content)
        print(f"Le fichier a été téléchargé avec succès sous le nom : {nom_fichier_local}")
else:
    print("Échec du téléchargement. Code de statut :", response.status_code)