import spacy
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Charger le modèle SpaCy
nlp = spacy.load("en_core_web_sm")
pos_a_exclure = ['SYM', 'NUM', 'PRON', 'DET', 'CONJ', 'ADP', 'ADJ', 'AUX', 'ADV', 'PRT', 'SPACE']

# Fonction pour nettoyer et lemmatiser les mots
def clean_word(word):
    word = word.lower()
    doc = nlp(word)
    cleaned_word = []

    for token in doc:
        if not token.is_stop and token.is_alpha and not token.is_punct and not token.is_space:
            if token.pos_ not in pos_a_exclure:
                cleaned_word.append(token.lemma_)

    return " ".join(cleaned_word)

# Fonction pour traiter un fichier CSV avec clustering
def clean_with_cluster(input_csv_path, output_csv_path):
    # Charger le fichier CSV d'origine
    data = pd.read_csv(input_csv_path, sep=";", encoding='latin-1')
    data = data[data['Mot'].apply(lambda x: isinstance(x, str))]
    # Nettoyer et lemmatiser les mots
    data['Mot_nettoye'] = data['Mot'].apply(clean_word)

    # Vectorisation des mots nettoyés
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['Mot_nettoye'])

    # Clustering avec K-Means
    kmeans = KMeans(n_clusters=3)  # Spécifiez le nombre de clusters souhaité
    data['Cluster'] = kmeans.fit_predict(tfidf_matrix)
    
    # Obtenez le nom du fichier d'origine sans extension
    base_filename = os.path.splitext(os.path.basename(input_csv_path))[0]

    # Enregistrement du DataFrame avec le nom du fichier de base suivi de "_clusters"
    data.to_csv(output_csv_path, sep=";", index=False, encoding='latin-1')

    # Lire le nouveau fichier avec les clusters
    clustered_data = pd.read_csv(output_csv_path, sep=";", encoding='latin-1')

    # Création d'une nouvelle colonne "Cluster_occurrence" pour stocker la somme des occurrences par mot
    clustered_data['Poids'] = clustered_data.groupby('Mot_nettoye')['Occurrence'].transform('sum')

    # Supprimer les colonnes "Mot", "Occurrence" et "Cluster"
    clustered_data = clustered_data.drop(columns=['Mot', 'Occurrence', 'Cluster'])

    # Remplacer les valeurs non finies (NaN et inf) par des zéros dans la colonne "Cluster_occurrence"
    clustered_data['Poids'].fillna(0, inplace=True)
    clustered_data['Poids'] = clustered_data['Poids'].replace([pd.np.inf, -pd.np.inf], 0) # type: ignore

    # Convertir la colonne "Cluster_occurrence" en int
    clustered_data['Poids'] = clustered_data['Poids'].astype(int)

    # Tri du DataFrame par la colonne "Mot_nettoye" en ordre croissant
    clustered_data = clustered_data.sort_values(by='Mot_nettoye')

    # Supprimer les doublons pour obtenir une seule entrée par mot unique
    clustered_data = clustered_data.drop_duplicates()

    # Enregistrer le DataFrame sans doublons dans le fichier de sortie
    clustered_data.to_csv(output_csv_path, sep=";", index=False, encoding='latin-1')

# Fonction pour traiter une série complète de fichiers
def process_series(series_directory, output_directory):
    # Parcourir tous les fichiers du répertoire de la série
    for filename in os.listdir(series_directory):
        # Vérifier si le fichier est un fichier CSV contenant "_vo" dans son nom
        if filename.endswith('.csv') and '_vo' in filename:
            # Construire le chemin d'accès complet du fichier d'entrée
            input_csv_path = os.path.join(series_directory, filename)
            print("Processing file: " + filename)
            # Construire le nom de fichier de sortie en ajoutant "_clusters" au nom du fichier
            output_filename = os.path.splitext(filename)[0] + "_clusters.csv"
            output_csv_path = os.path.join(output_directory, output_filename)

            # Appeler la fonction de nettoyage avec clustering
            clean_with_cluster(input_csv_path, output_csv_path)

# Exemple d'utilisation
series_directory = '../csv'  # Répertoire contenant les séries CSV
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
