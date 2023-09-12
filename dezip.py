import os
from pyunpack import Archive

def extraire_fichiers_archive(repertoire):
    for dossier in os.listdir(repertoire):
        chemin_dossier = os.path.join(repertoire, dossier)
        if os.path.isdir(chemin_dossier):
            fichiers_archive = [fichier for fichier in os.listdir(chemin_dossier) if fichier.endswith(('.zip', '.rar', '.7z'))]
            if fichiers_archive:
                print(f"Extraction des fichiers d'archive dans le dossier '{dossier}'...")
                for fichier_archive in fichiers_archive:
                    chemin_fichier_archive = os.path.join(chemin_dossier, fichier_archive)
                    try:
                        Archive(chemin_fichier_archive).extractall(chemin_dossier)
                        os.remove(chemin_fichier_archive)
                        print(f"Extraction réussie pour le fichier '{fichier_archive}'")
                    except Exception as e:
                        print(f"Erreur lors de l'extraction du fichier '{fichier_archive}': {str(e)}")
                print()

def supprimer_fichiers_archive(repertoire):
    for dossier, sous_dossiers, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            if fichier.endswith(('.zip', '.rar', '.7z')):
                chemin_fichier_archive = os.path.join(dossier, fichier)
                try:
                    os.remove(chemin_fichier_archive)
                    print(f"Fichier d'archive supprimé : '{chemin_fichier_archive}'")
                except Exception as e:
                    print(f"Erreur lors de la suppression du fichier d'archive '{chemin_fichier_archive}': {str(e)}")

# Chemin d'accès au répertoire
chemin_repertoire = r"C:\Users\diego\Documents\IUT\S5\SAE\sous-titres"

# Extraire les fichiers d'archive et supprimer les fichiers d'archive correspondants
extraire_fichiers_archive(chemin_repertoire)

# Reparcourir les fichiers pour supprimer les fichiers d'archive restants
supprimer_fichiers_archive(chemin_repertoire)
