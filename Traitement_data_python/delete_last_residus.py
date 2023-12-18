from sqlalchemy import create_engine, text

# Configuration de la connexion à la base de données MySQL
db_username = 'root'
db_password = ''
db_host = 'localhost'
db_port = '3306'
db_name = 'projet_sae2'

# Créez un moteur SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}', echo=True)
conn = engine.connect()

# Exemple de requête pour récupérer le texte de votre base de données
query = text("SELECT Libelle FROM mots_vo")
result = conn.execute(query) 

# Récupérer le texte depuis le résultat de la requête
text_data = [row[0] for row in result]

# Liste des préfixes à vérifier
# Liste de mots pour vérifier s'ils sont mal lemmatisés
words_to_check = [
    "didn", "don", "doesn", "hasn", "haven", "ifit", "ifyou", "ifyour", "ifyours", "ifthe", "ifthis", "ifthat", "ifthey", "iftheir", "ifl", "ifwe", "ifour", "ifours", "ifc", "uh", "hey",
    "isn", "let", "mustn", "shan", "shouldn", "wasn", "weren", "won", "wouldn", "yeah", "you", "your", "yours", "the", "this", "that", "they", "their", "l", "we", "our", "ours", "c", "go to", "ve",
    "ain", "aren", "couldn", "hadn", "hasn", "haven", "isn", "mustn", "shan", "shouldn", "wasn", "weren", "won", "wouldn"
]

unique_words_to_check = list(set(words_to_check))

print(unique_words_to_check)

# Liste pour stocker les mots mal lemmatisés
mal_lemmatized_words = [word for word in unique_words_to_check if word in text_data]

# Exemple de requête pour supprimer les apparitions des mots mal lemmatisés de la table apparition_vo
delete_apparition_vo_query = text("DELETE FROM apparition_vo WHERE id_mot_vo IN (SELECT id_mot_vo FROM mots_vo WHERE Libelle = :word)")

# Exemple de requête pour supprimer les mots mal lemmatisés de la table mots_vo
delete_mots_vo_query = text("DELETE FROM mots_vo WHERE Libelle = :word")

# Parcourir la liste des mots mal lemmatisés et les supprimer de la base de données
for word in mal_lemmatized_words:
    # Supprimer les apparitions des mots mal lemmatisés de la table apparition_vo
    conn.execute(delete_apparition_vo_query, {"word": word})

    # Supprimer les mots mal lemmatisés de la table mots_vo
    conn.execute(delete_mots_vo_query, {"word": word})

