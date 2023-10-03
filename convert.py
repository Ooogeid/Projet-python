import csv
import re
import os
from collections import defaultdict
from langdetect import detect

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
def process_series(root_directory, output_csv_directory):
    # Dictionnaires pour stocker les occurrences de mots pour chaque épisode (VO et VF)
    word_counts_vf = defaultdict(int)
    word_counts_vo = defaultdict(int)
    
    # Se positionner dans chaque dossier de saison
    for root, _, files in os.walk(root_directory):
        for file in files:

            file_path = os.path.join(root, file)
            print(file_path)
            with open(file_path, 'r', encoding='latin-1', errors='ignore') as f:
                contenu = f.read()
            
            if contenu.strip():
                langue = detect(contenu)
            
            if langue == "fr":
                language = 'Français'
            else:
                language = 'Anglais'

            word_count = extract_words_from_srt(os.path.join(root, file))

            if language == 'Anglais':
                for word, count in word_count.items():
                    word_counts_vo[word] += count
            elif language == 'Français':
                for word, count in word_count.items():
                    word_counts_vf[word] += count

        print(len(word_counts_vo.keys()))

    # Enregistrez les mots et leurs occurrences dans le fichier CSV de sortie (VO)
    output_csv_vo = os.path.join(output_csv_directory, f'{os.path.basename(root_directory)}_vo.csv')
    with open(output_csv_vo, 'w', newline='', encoding='latin-1') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(['Mot', 'Occurrence'])
        for word, count in word_counts_vo.items():
            csv_writer.writerow([word, count])

    # Enregistrez les mots et leurs occurrences dans le fichier CSV de sortie (VF)
    output_csv_vf = os.path.join(output_csv_directory, f'{os.path.basename(root_directory)}_vf.csv')
    with open(output_csv_vf, 'w', newline='', encoding='latin-1') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(['Mot', 'Occurrence'])
        for word, count in word_counts_vf.items():
            csv_writer.writerow([word, count])

def main():
    series_directory = '../sous-titres'
    output_directory = '../csv'

    # Parcourir tous les dossiers de séries dans le répertoire de séries
    for series_folder in os.listdir(series_directory):
        if os.path.isdir(os.path.join(series_directory, series_folder)):
            # Construire le chemin d'accès pour le dossier de la série
            series_path = os.path.join(series_directory, series_folder)
            # Construire le chemin de sortie pour le dossier CSV de la série
            output_csv_directory = os.path.join(output_directory, series_folder)

            # Créez le dossier de sortie s'il n'existe pas
            os.makedirs(output_csv_directory, exist_ok=True)

            # Traiter la série
            process_series(series_path, output_csv_directory)
            print(f"Processed series: {series_folder}")

if __name__ == "__main__":
    main()
