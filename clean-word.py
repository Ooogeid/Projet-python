import spacy
import pandas as pd
from collections import defaultdict

# Créer un dictionnaire pour stocker les occurrences de chaque forme à l'infinitif
verb_occurrences = defaultdict(int)

nlp = spacy.load("en_core_web_sm")

# Fonction pour nettoyer un mot en utilisant spaCy
def clean_word(word):
    word = word.lower()
    doc = nlp(word)
    cleaned_word = []

    for token in doc:
        if not token.is_stop and token.is_alpha:
            if token.pos_ in ["NOUN", "PROPN"]:
                # Conserver le mot tel quel s'il est un nom ou un nom propre
                cleaned_word.append(token.text)
            elif token.pos_ == "VERB":
                infinitive = token.lemma_
                # Ajouter l'occurrence au dictionnaire en utilisant l'infinitif comme clé
                verb_occurrences[infinitive] += 1
                # Ajouter l'infinitif au mot nettoyé
                cleaned_word.append(infinitive)

    return " ".join(cleaned_word)

# Charger le fichier CSV d'origine
data = pd.read_csv("../csv/90210/90210_vo_test.csv", sep=";", encoding='latin-1')

# Initialiser un dictionnaire pour stocker les occurrences agrégées des mots nettoyés
word_counts = defaultdict(int)

# Parcourir les lignes du DataFrame
for index, row in data.iterrows():
    word = row["Mot"]
    count = row["Occurrence"]

    # Nettoyer le mot
    cleaned_word = clean_word(word)

    # Ignorer les mots uniques (une seule lettre)
    if len(cleaned_word) > 1:
        # Ajouter le mot nettoyé et ses occurrences au dictionnaire
        word_counts[cleaned_word] += count

# Créer un nouveau DataFrame à partir du dictionnaire
cleaned_data = pd.DataFrame({"Mot": list(word_counts.keys()), "Occurrence": list(word_counts.values())})
    
# Enregistrer le DataFrame nettoyé dans un nouveau fichier CSV
cleaned_data.to_csv("nouveau_fichier.csv", sep=";", index=False, encoding='latin-1')
