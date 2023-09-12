import csv
import re
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
    

breakingbad = pd.read_csv('../csv/breakingbad.csv', encoding='latin-1')
extract_words_from_srt('../sous-titres/breakingbad.srt', breakingbad)