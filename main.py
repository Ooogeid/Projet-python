import csv
import re
import os
from collections import defaultdict
import pandas as pd

# Fonction pour extraire les mots d'un fichier SRT, les compter et les stocker dans un dictionnaire
def extract_words_from_srt(input_file):
    word_count = defaultdict(int)

    with open(input_file, 'r', encoding='latin-1') as file:
        srt_content = file.read()
    
    # Remplacer les caractères de ponctuation par des espaces et diviser en mots
    words = re.findall(r'\b\w+\b', srt_content.lower())  # Utilisez lower() pour tout mettre en minuscules

    for word in words:
        if not word.isdigit():  # Exclure les mots composés uniquement de chiffres
            word_count[word] += 1

    return word_count  # Retournez un dictionnaire de mots et occurrences

# Fonction pour traiter une série
def process_series(root_directory, output_csv):
    # Dictionnaire pour stocker les occurrences de mots pour chaque épisode
    word_counts = defaultdict(int)

    # Se position dans cahqu dossier de saison
    for root, _, files in os.walk(root_directory):
        for file in files:
            word_count = extract_words_from_srt(os.path.join(root, file))
            for word, count in word_count.items():
                word_counts[word] += count

    # Enregistrez les mots et leurs occurrences dans le fichier CSV de sortie
    with open(output_csv, 'w', newline='', encoding='latin-1') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Mot', 'Occurrence'])
        for word, count in word_counts.items():
            csv_writer.writerow([word, count])

    df = pd.read_csv(output_csv, encoding='latin-1')

    # Trier le DataFrame par ordre décroissant d'occurrence
    df_sorted = df.sort_values(by='Occurrence', ascending=False)

    # Enregistrer le DataFrame trié dans le fichier CSV
    df_sorted.to_csv(output_csv, index=False, encoding='utf-8')

def main():
    series_directory = '../sous-titres'
    output_directory = '../csv'

    # Parcourir tous les dossiers de séries dans le répertoire de séries
    for series_folder in os.listdir(series_directory):
        if os.path.isdir(os.path.join(series_directory, series_folder)):
            # Construire le chemin d'accès pour le dossier de la série
            series_path = os.path.join(series_directory, series_folder)
            
            # Construire le chemin de sortie CSV pour la série
            output_csv = os.path.join(output_directory, f'{series_folder}.csv')

            # Traiter la série
            process_series(series_path, output_csv)

if __name__ == "__main__":
    main()