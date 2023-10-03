'''
import spacy
import pandas as pd
import transformers
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

#from transformers import CamembertForMaskedLM, CamembertTokenizer

#tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
#model = CamembertForMaskedLM.from_pretrained("camembert-base")
#model.eval()

#from spacy_transformers import TransformersLanguage, TransformersWordPiecer, TransformersTok2Vec
# Téléchargez le modèle CamemBERT pré-entraîné
#model_name = "camembert-base"
#tokenizer = transformers.CamembertTokenizer.from_pretrained(model_name)
#model = transformers.CamembertModel.from_pretrained(model_name)

# Vous pouvez ensuite l'utiliser pour le traitement du texte en français

# Créez un objet nlp avec le modèle CamemBERT
#nlp = TransformersLanguage(trf_name="camembert-base")

# Ajoutez les composants de pipeline pour la tokenization et le marquage grammatical
#nlp.add_pipe(TransformersWordPiecer.from_pretrained(nlp.vocab, "camembert-base"))
#nlp.add_pipe(TransformersTok2Vec.from_pretrained(nlp.vocab, "camembert-base"))

# Traitez le texte en utilisant le pipeline SpaCy avec CamemBERT
#doc = nlp("Votre texte en français ici.")

#import torch
#from transformers.modeling_camembert import CamembertForMaskedLM
#from transformers.tokenization_camembert import CamembertTokenizer

#camembert = torch.hub.load('pytorch/fairseq', 'camembert')
#camembert.eval()  # disable dropout (or leave in train mode to finetune)

#Charger le modèle SpaCy
nlp = spacy.load("fr_core_news_sm")

# Charger le fichier CSV d'origine
data = pd.read_csv("../csv/bones/bones_vf.csv", sep=";", encoding='latin-1')

# Nettoyer et lemmatiser les mots
def clean_word(word):
    word = word.lower()
    doc = nlp(word)
    cleaned_word = []

    for token in doc:
        if not token.is_stop and token.is_alpha and not token.is_punct and not token.is_space:
            cleaned_word.append(token.lemma_)

    return " ".join(cleaned_word)

data = data[data['Mot'].apply(lambda x: isinstance(x, str))]
data['Mot_nettoye'] = data['Mot'].apply(clean_word)

# Vectorisation des mots nettoyés
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['Mot_nettoye'])

# Clustering avec K-Means
kmeans = KMeans(n_clusters=3)  # Spécifiez le nombre de clusters souhaité
data['Cluster'] = kmeans.fit_predict(tfidf_matrix)

# Enregistrement du DataFrame avec les clusters dans un nouveau fichier CSV
data.to_csv("nouveau_fichier_clusters.csv", sep=";", index=False, encoding='latin-1')


Dans ce code :

    -Les mots sont nettoyés et lemmatisés, tout comme dans votre code précédent.
    Les mots nettoyés sont vectorisés en utilisant la vectorisation TF-IDF, ce qui permet de représenter chaque mot sous forme de 
    vecteurs numériques.
    -Le clustering K-Means est appliqué aux vecteurs TF-IDF pour regrouper les mots en clusters. Vous devez spécifier le nombre 
    de clusters (dans cet exemple, n_clusters=3).
    -Les mots sont associés à leur cluster respectif dans le DataFrame, et le DataFrame résultant est enregistré dans un nouveau 
    fichier CSV avec les informations de clustering.

Cela permet de regrouper les mots similaires en fonction de leurs vecteurs TF-IDF calculés à partir des données textuelles. Vous pouvez
ensuite explorer et analyser les clusters pour mieux comprendre la structure de vos données. Notez que le nombre de
clusters (n_clusters) doit être ajusté en fonction de vos données et de vos besoins spécifiques.



Le choix du nombre optimal de clusters (n_clusters) dans K-Means peut être une tâche délicate et dépend en grande partie de la 
structure des données. Cependant, il existe des méthodes et des heuristiques pour aider à déterminer une valeur appropriée pour n_clusters.

Pour un fichier CSV contenant entre 6000 et 8000 lignes, voici quelques étapes que vous pouvez suivre pour choisir une valeur de n_clusters :

    Méthode du coude (Elbow Method) : Cette méthode consiste à exécuter K-Means avec différentes valeurs de n_clusters et à calculer la somme des carrés des 
    distances (inertie) entre les points et les centres de cluster. Vous tracez ensuite une courbe de l'inertie en fonction de n_clusters et cherchez le point 
    où l'inertie commence à se stabiliser, ressemblant à un coude. Cela peut indiquer un nombre approprié de clusters.

    Méthode de la silhouette (Silhouette Method) : La silhouette est une mesure de la similarité entre un point et son propre cluster par rapport aux autres
    clusters. Vous pouvez calculer la silhouette moyenne pour différentes valeurs de n_clusters et choisir celle qui donne la meilleure silhouette moyenne.

    Méthode de la variabilité interne/externe : Vous pouvez également examiner la variabilité interne (à l'intérieur des clusters) et externe 
    (entre les clusters) en fonction de différentes valeurs de n_clusters. Vous cherchez un point où la variabilité interne diminue tout en maintenant 
    une variabilité externe significative.

    Connaissance du domaine : Si vous avez une connaissance approfondie du domaine et que vous savez combien de groupes distincts sont attendus,
    cela peut vous guider dans le choix de n_clusters.

Il n'y a pas de réponse unique à la question du nombre optimal de clusters, mais ces méthodes peuvent vous aider à choisir une valeur raisonnable. 
Vous pouvez également essayer plusieurs valeurs de n_clusters et évaluer les résultats en fonction de la cohérence et de l'interprétabilité des clusters obtenus.


'''

from transformers import CamembertTokenizer, CamembertForMaskedLM
#from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders
import spacy
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import torch

# Charger le modèle SpaCy
nlp = spacy.load("fr_core_news_sm")

# Charger le tokenizer et le modèle CamemBERT
model_name = "camembert-base"
tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
model = CamembertForMaskedLM.from_pretrained("camembert-base")
model.eval()

# Fonction pour nettoyer et lemmatiser les mots avec CamemBERT
def clean_word(word):
    word = word.lower()

    # Utiliser CamemBERT pour remplir l'espace réservé masqué
    input_text = f"La phrase contient le mot {tokenizer.mask_token} et d'autres mots."
    #masked_index = input_text.index(tokenizer.mask_token)
    input_text = input_text.replace(tokenizer.mask_token, word)
    
    # Tokenization avec CamemBERT
    inputs = tokenizer(input_text, return_tensors="pt")
    mask_token_index = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)[1]

    # Prédire le mot masqué avec CamemBERT
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_token_ids = torch.argmax(logits, dim=-1)
    predicted_word = tokenizer.decode(predicted_token_ids[0, mask_token_index]).strip()

    return predicted_word

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
    clustered_data['Cluster_occurrence'] = clustered_data.groupby('Mot_nettoye')['Occurrence'].transform('sum')

    # Supprimer les colonnes "Mot", "Occurrence" et "Cluster"
    clustered_data = clustered_data.drop(columns=['Mot', 'Occurrence', 'Cluster'])

    # Remplacer les valeurs non finies (NaN et inf) par des zéros dans la colonne "Cluster_occurrence"
    clustered_data['Cluster_occurrence'].fillna(0, inplace=True)
    #clustered_data['Cluster_occurrence'] = clustered_data['Cluster_occurrence'].replace([pd.np.inf, -pd.np.inf], 0)
    clustered_data['Cluster_occurrence'] = clustered_data['Cluster_occurrence'].replace([np.inf, -np.inf], 0)


    # Convertir la colonne "Cluster_occurrence" en int
    clustered_data['Cluster_occurrence'] = clustered_data['Cluster_occurrence'].astype(int)

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
        # Vérifier si le fichier est un fichier CSV contenant "_vf" dans son nom
        if filename.endswith('.csv') and '_vf' in filename:
            # Construire le chemin d'accès complet du fichier d'entrée
            input_csv_path = os.path.join(series_directory, filename)
            print("Processing file: " + filename)
            # Construire le nom de fichier de sortie en ajoutant "_clusters" au nom du fichier
            output_filename = os.path.splitext(filename)[0] + "_clusters_vf_new.csv"
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
