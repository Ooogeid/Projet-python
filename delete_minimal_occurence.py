import os
import pandas as pd

def process_csv_file(file_path):
    # Charger le CSV dans un DataFrame
    df = pd.read_csv(file_path, encoding='latin-1', sep=';')

    # Filtrer les lignes avec moins de 10 occurrences
    df = df[df['Cluster_occurrence'] >= 10]
    
    # Trier le DataFrame par ordre décroissant d'occurrence
    df = df.sort_values(by='Cluster_occurrence', ascending=False)
    
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
