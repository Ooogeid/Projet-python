import os
import zipfile

def extraire_fichiers_zip(repertoire):
    for dossier in os.listdir(repertoire):
        chemin_dossier = os.path.join(repertoire, dossier)
        if os.path.isdir(chemin_dossier):
            fichiers_zip = [fichier for fichier in os.listdir(chemin_dossier) if fichier.endswith('.zip')]
            if fichiers_zip:
                print(f"Extraction des fichiers ZIP dans le dossier '{dossier}'...")
                for fichier_zip in fichiers_zip:
                    chemin_fichier_zip = os.path.join(chemin_dossier, fichier_zip)
                    try:
                        with zipfile.ZipFile(chemin_fichier_zip, 'r') as zip_ref:
                            zip_ref.extractall(chemin_dossier)
                        os.remove(chemin_fichier_zip)
                        print(f"Extraction réussie pour le fichier '{fichier_zip}'")
                    except Exception as e:
                        print(f"Erreur lors de l'extraction du fichier '{fichier_zip}': {str(e)}")
                print()

def supprimer_fichiers_zip(repertoire):
    for dossier, sous_dossiers, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            if fichier.endswith('.zip'):
                chemin_fichier_zip = os.path.join(dossier, fichier)
                try:
                    os.remove(chemin_fichier_zip)
                    print(f"Fichier ZIP supprimé : '{chemin_fichier_zip}'")
                except Exception as e:
                    print(f"Erreur lors de la suppression du fichier ZIP '{chemin_fichier_zip}': {str(e)}")

# Chemin d'accès au répertoire
chemin_repertoire = r"C:\Users\diego\Documents\IUT\S5\SAE\sous-titres"

# Extraire les fichiers ZIP et supprimer les fichiers ZIP correspondants
extraire_fichiers_zip(chemin_repertoire)

# Reparcourir les fichiers pour supprimer les fichiers ZIP restants
supprimer_fichiers_zip(chemin_repertoire)