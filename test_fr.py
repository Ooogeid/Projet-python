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

'''
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
'''

'''
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