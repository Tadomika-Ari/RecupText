import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import re

# En-têtes pour simuler un navigateur
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Fonction pour diviser le texte en morceaux
def diviser_texte(texte, taille_max):
    lignes = texte.split('\n')
    morceaux = []
    morceau_actuel = ""
    for ligne in lignes:
        if len(morceau_actuel) + len(ligne) + 1 > taille_max:
            morceaux.append(morceau_actuel)
            morceau_actuel = ligne
        else:
            morceau_actuel += "\n" + ligne
    if morceau_actuel:
        morceaux.append(morceau_actuel)
    return morceaux

# Extraire le numéro du chapitre depuis l'URL
def extraire_numero_chapitre(url):
    match = re.search(r'chapter-(\d+)', url)
    if match:
        return match.group(1)
    return "inconnu"

# Boucle principale pour demander des liens à l'utilisateur
while True:
    # Demande à l'utilisateur d'entrer un lien ou de taper "arret" pour quitter
    url = input("Entrez le lien du chapitre (ou tapez 'arret' pour quitter) : ").strip()
    
    if url.lower() == "arret":
        print("Arrêt du programme.")
        break

    # Récupération du contenu HTML de la page
    response = requests.get(url, headers=headers)

    # Vérifie que la requête a réussi
    if response.status_code == 200:
        # Utilise BeautifulSoup pour parser le HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Récupère tout le texte brut de la page
        texte = soup.get_text(separator='\n', strip=True)
        
        # Extraire le numéro du chapitre
        numero_chapitre = extraire_numero_chapitre(url)
        
        # Sauvegarde le texte brut dans un fichier
        nom_fichier_non_traduit = f"chapitre_{numero_chapitre}_non_traduit.txt"
        with open(nom_fichier_non_traduit, "w", encoding="utf-8") as fichier_non_traduit:
            fichier_non_traduit.write(texte)
        
        # Divise le texte en morceaux de taille raisonnable (par exemple, 5000 caractères)
        morceaux = diviser_texte(texte, 5000)
        
        # Traduit chaque morceau et les combine
        texte_traduit = ""
        traducteur = GoogleTranslator(source='en', target='fr')
        for morceau in morceaux:
            texte_traduit += traducteur.translate(morceau) + "\n"
        
        # Sauvegarde le texte traduit dans un fichier
        nom_fichier_traduit = f"chapitre_{numero_chapitre}_traduit.txt"
        with open(nom_fichier_traduit, "w", encoding="utf-8") as fichier_traduit:
            fichier_traduit.write(texte_traduit)
        
        print(f"Les fichiers '{nom_fichier_non_traduit}' et '{nom_fichier_traduit}' ont été créés.")
    else:
        print("Erreur lors du chargement de la page :", response.status_code)