import spacy
import pandas as pd
import os
import numpy as np

# Charger le modèle SpaCy
nlp = spacy.load("en_core_web_sm")
pos_a_exclure = ['SYM', 'NUM', 'PRON', 'DET', 'CONJ', 'ADP', 'ADJ', 'AUX', 'ADV', 'PRT', 'SPACE']

# Fonction pour nettoyer et lemmatiser les mots
def clean_word(word):
    if isinstance(word, str):
        word = word.lower()
        doc = nlp(word)
        cleaned_word = []

        for token in doc:
            if not token.is_stop and token.is_alpha and not token.is_punct and not token.is_space:
                if token.pos_ not in pos_a_exclure:
                    cleaned_word.append(token.lemma_)

        return " ".join(cleaned_word)
    else:
        return ""

# Fonction pour calculer le TF-IDF manuellement et remplacer la colonne 'Occurrence'
def calculate_replace_tfidf(data):
    # Calcule TF-IDF values manuellement
    total_documents = len(data)
    term_frequency = data['Occurrence']
    document_frequency = data.groupby('Mot_nettoye')['Mot'].nunique()  # Utiliser nunique() pour compter le nombre de documents

    # Calculer IDF (inverse document frequency)
    inverse_document_frequency = np.log(total_documents / (1 + document_frequency))

    # Créer un dictionnaire pour stocker l'IDF de chaque mot
    idf_dict = dict(zip(document_frequency.index, inverse_document_frequency))

    # Appliquer l'IDF à chaque ligne du DataFrame
    data['TF-IDF'] = term_frequency * data['Mot_nettoye'].map(idf_dict)

    # Supprimer la colonne 'Occurrence'
    data = data.drop(columns=['Occurrence'])

    return data

# Fonction pour traiter un fichier CSV avec TF-IDF
def clean_with_tfidf(input_csv_path, output_csv_path):
    # Charger le fichier CSV d'origine
    data = pd.read_csv(input_csv_path, sep=";", encoding='latin-1')

    # Vérifier si le csv contient les colonnes 'Mot' et 'Occurrence'
    if list(data.columns) != ["Mot", "Occurrence"] or len(data.columns) != 2 or len(data) < 1:
        print(f"Le fichier {input_csv_path} ne contient pas les en-têtes attendus. Aucun traitement n'est effectué.")
        return

    # Nettoyer et lemmatiser les mots
    data['Mot_nettoye'] = data['Mot'].apply(clean_word)

    # Calculer et remplacer le TF-IDF
    data = calculate_replace_tfidf(data)

    # Supprimer les lignes où le mot nettoyé est vide
    data = data[data['Mot_nettoye'] != '']

    # Conserver uniquement les colonnes 'Mot_nettoye' et 'TF-IDF'
    data = data[['Mot_nettoye', 'TF-IDF']]

    # Arrondir le TF-IDF à quatres chiffres après la virgule
    data['TF-IDF'] = data['TF-IDF'].round(4)

    # Trier par TF-IDF décroissant
    data = data.sort_values(by='TF-IDF', ascending=False)

    # Enregistrement du DataFrame final
    data.to_csv(output_csv_path, sep=";", index=False, encoding='latin-1')

# Fonction pour traiter une série complète de fichiers
def process_series(series_directory, output_directory):
    # Parcourir tous les fichiers du répertoire de la série
    for filename in os.listdir(series_directory):
        # Vérifier si le fichier est un fichier CSV contenant "_vo" dans son nom
        if filename.endswith('.csv') and '_vf' in filename:
            # Construire le chemin d'accès complet du fichier d'entrée
            input_csv_path = os.path.join(series_directory, filename)
            print("Processing file: " + filename)
            # Construire le nom de fichier de sortie en ajoutant "_clusters" au nom du fichier
            output_filename = os.path.splitext(filename)[0] + "_tfidf.csv"
            output_csv_path = os.path.join(output_directory, output_filename)

            # Appeler la fonction de nettoyage avec TF-IDF
            clean_with_tfidf(input_csv_path, output_csv_path)

# Exemple d'utilisation
series_directory = r"C:/wamp64/www/Projet_sae/data/csv" # Répertoire contenant les séries CSV
output_directory = '../csv_clean'  # Répertoire de sortie pour les CSV traités

# Créer le répertoire de sortie s'il n'existe pas
os.makedirs(output_directory, exist_ok=True)

# Traiter toutes les séries du répertoire
for series_folder in os.listdir(series_directory):
    if os.path.isdir(os.path.join(series_directory, series_folder)):
        # Construire le chemin d'accès pour le dossier de la série
        series_path = os.path.join(series_directory, series_folder)
        # Traiter la série
        process_series(series_path, output_directory)
