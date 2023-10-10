import os
import pandas as pd
import re

def process_csv_file(file_path):

    regex = re.compile(r'\b\w{2,}\b')

    # Charger le CSV dans un DataFrame
    df = pd.read_csv(file_path, encoding='latin-1', sep=';')

    # Filtrer les lignes avec moins de 10 occurrences
    df = df[df['Poids'] >= 10]

    df = df[df['Mot_nettoye'].str.match(regex)]
    
    # Trier le DataFrame par ordre décroissant d'occurrence 
    df = df.sort_values(by='Poids', ascending=False)
    
    # Sauvegarder le DataFrame dans le même fichier CSV (en écrasant l'original)
    df.to_csv(file_path, index=False, encoding='latin-1', sep=';')

def process_csv_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print(f"Traitement du fichier : {file_path}")
                process_csv_file(file_path)

if __name__ == "__main__":
    input_directory = '../csv_clean'
    process_csv_directory(input_directory)

