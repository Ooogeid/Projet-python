import os

# Répertoire contenant les fichiers CSV
input_directory = '../csv_clean'

# Parcourir les fichiers CSV dans le répertoire
for file_name in os.listdir(input_directory):
    if file_name.endswith('_modified_tfidf.csv'):
        file_path = os.path.join(input_directory, file_name)
        try:
            os.remove(file_path)
            print(f"Fichier supprimé : {file_path}")
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier {file_path}: {e}")
