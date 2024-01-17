import json
from sqlalchemy import create_engine, text

# Fonction pour échapper les apostrophes dans une liste de mots
def escape_apostrophes(words):
    return [word.replace("'", "''") for word in words]

# Configuration de la connexion à la base de données MySQL
db_username = 'root'
db_password = ''
db_host = 'localhost'
db_port = '3306'
db_name = 'projet_sae'

# Créez un moteur SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}', echo=True)

# Chargement des stop words depuis le fichier JSON
with open('stop_words_english.json', 'r', encoding="utf-8") as file:
    stop_words = json.load(file)

# Échapper les apostrophes dans les stop words
escaped_stop_words = escape_apostrophes(stop_words)

# Convertir la liste des stop words échappés en une chaîne de caractères séparée par des virgules
stop_words_str = ', '.join([f"'{word}'" for word in escaped_stop_words])

# Suppression des mots de la table mots_vo
delete_query = text(f"DELETE FROM mots_vo WHERE Libelle IN ({stop_words_str})")

with engine.connect() as conn:
    print(delete_query)
    conn.execute(delete_query)

# Suppression des occurrences dans la table apparition_vo
delete_occurrences_query = text(f"""
    DELETE FROM apparition_vo
    WHERE id_mot_vo IN (
        SELECT id_mot_vo FROM mots_vo WHERE Libelle IN ({stop_words_str})
    )
""")

with engine.connect() as conn:
    conn.execute(delete_occurrences_query)