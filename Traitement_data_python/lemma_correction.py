import os
import pandas as pd

# Répertoire contenant les fichiers CSV
input_directory = '../csv_clean'

# Liste de mots à modifier
mots_a_modifier = {
    'drogu': 'drogue',
    'vampir': 'vampire',
    'téléphon': 'téléphone',
    'télévis': 'télévision',
    'télécharg': 'télécharger',
    'héroïn'   : 'héroïne',
    'temp': 'temps',
    'detest': 'détester',
    'mangu': 'manger',
    'ressembl': 'ressembler',
    'touch': 'toucher',
    'gueul': 'gueule',
    'battr': 'battre',
    'mensong': 'mensonge',
    'fum': 'fumer',
    'bais': 'baiser',
    'saign': 'saigner',
    'réveill': 'réveiller',
    'sonn': 'sonner',
    'respir': 'respirer',
    'fortun': 'fortune',
    'impliqu': 'impliquer',
    'nanotechnologiqu': 'nanotechnologique',
    'sorcièrer': 'sorcièrerie',
    'rêv': 'rêve',
    'gourmandis': 'gourmandise',
    'couvertur': 'couverture',
}

# Parcourir les fichiers CSV dans le répertoire
for file_name in os.listdir(input_directory):
    if file_name.endswith('.csv') and '_vf' in file_name:
        file_path = os.path.join(input_directory, file_name)
        print(f"Traitement du fichier : {file_path}")

        # Charger le CSV dans un DataFrame
        df = pd.read_csv(file_path, encoding='latin-1', sep=';')

        # Modifier les mots selon la liste spécifiée
        df['Mot_nettoye'] = df['Mot_nettoye'].replace(mots_a_modifier)

        # Enregistrer les modifications dans un nouveau fichier CSV
        output_file_path = os.path.join(input_directory, file_name.replace('_vf', '_vf_modified'))
        df.to_csv(output_file_path, sep=';', index=False, encoding='latin-1')
