import csv
import re
import os
from collections import defaultdict
import pandas as pd

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

root_directory = '../sous-titres/breakingbad' 

# Dictionnaire pour stocker les occurrences de mots pour chaque épisode
word_counts = defaultdict(int)

# Walk through all directories and subdirectories
for root, _, files in os.walk(root_directory):
    # Print the list of files in the current directory
    for file in files:
        word_count = extract_words_from_srt(os.path.join(root, file))
        for word, count in word_count.items():
            word_counts[word] += count

# Enregistrez les mots et leurs occurrences dans votre fichier CSV de sortie
output_csv = '../csv/breakingbad.csv'
with open(output_csv, 'w', newline='', encoding='latin-1') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Mot', 'Occurrence'])
    for word, count in word_counts.items():
        csv_writer.writerow([word, count])

df = pd.read_csv('../csv/breakingbad.csv', encoding='latin-1')

# Trier le DataFrame par ordre décroissant d'occurrence
df_sorted = df.sort_values(by='Occurrence', ascending=False)

df_sorted.to_csv(output_csv, index=False, encoding='latin-1')