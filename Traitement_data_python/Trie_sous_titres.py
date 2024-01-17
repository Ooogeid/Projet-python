import os
import shutil

def organiser_series():
    # Chemin vers le répertoire principal
    repertoire_principal = "C:/wamp64/www/Projet_sae/data"

    # Chemin vers le répertoire "sous-titres"
    repertoire_sous_titres = os.path.join(repertoire_principal, "sous-titres")

    # Liste des dossiers de séries dans le répertoire "sous-titres"
    dossiers_series = [d for d in os.listdir(repertoire_sous_titres) if os.path.isdir(os.path.join(repertoire_sous_titres, d))]

    # Parcours de chaque dossier de séries
    for dossier_serie in dossiers_series:
        chemin_serie = os.path.join(repertoire_sous_titres, dossier_serie)

        # Liste des fichiers srt dans le dossier de la série
        fichiers_serie = [f for f in os.listdir(chemin_serie) if f.lower().endswith(".srt")]

        # Liste des dossiers à l'intérieur du dossier de la série
        dossiers_a_supprimer = [d for d in os.listdir(chemin_serie) if os.path.isdir(os.path.join(chemin_serie, d))]

        # Déplacement des fichiers srt vers le dossier principal
        for fichier in fichiers_serie:
            chemin_source = os.path.join(chemin_serie, fichier)
            chemin_destination = os.path.join(repertoire_sous_titres, dossier_serie, fichier)
            shutil.move(chemin_source, chemin_destination)

        # Suppression des dossiers à l'intérieur du dossier de la série
        for dossier in dossiers_a_supprimer:
            chemin_dossier = os.path.join(chemin_serie, dossier)
            shutil.rmtree(chemin_dossier)

if __name__ == "__main__":
    organiser_series()
