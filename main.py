import csv
import re
import os
from collections import defaultdict
import pandas as pd

def extract_words_from_srt(input_file, output_csv):
    word_count = defaultdict(int)

    with open(input_file, 'r', encoding='latin-1') as file:
        srt_content = file.read()
    
    # Remplacer les caractères de ponctuation par des espaces et diviser en mots
    words = re.findall(r'\b\w+\b', srt_content.lower())  # Utilisez lower() pour tout mettre en minuscules

    for word in words:
        if not word.isdigit():  # Exclure les mots composés uniquement de chiffres
            word_count[word] += 1

    with open(output_csv, 'w', newline='', encoding='latin-1') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Mots', 'Occurrence'])
        for word, count in word_count.items():
            csv_writer.writerow([word, count])
    

# Charger les deux fichiers CSV dans des DataFrames
breakingbadvo = pd.read_csv('breakingbadvo.csv', encoding='latin-1')
breakingbadvf = pd.read_csv('breakingbadvf.csv', encoding='latin-1')

# Concaténer les DataFrames verticalement (ajouter un DataFrame en dessous de l'autre)
concatenated_df = pd.concat([breakingbadvo, breakingbadvf], ignore_index=True)

# Écrire le DataFrame concaténé dans un nouveau fichier CSV
concatenated_df.to_csv('breakingbad.csv', index=False)