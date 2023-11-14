import json
from sqlalchemy import create_engine, text

# Configuration de la connexion à la base de données MySQL
db_username = 'root'
db_password = ''
db_host = 'localhost'
db_port = '3306'
db_name = 'projet_sae'

# Créez un moteur SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}', echo=True)

# Chargement des stop words depuis le fichier JSON
with open('stop_words_english.json', 'r') as file:
    stop_words = json.load(file)

# Suppression des mots de la table mots_vo
delete_query = text("DELETE FROM mots_vo WHERE Libelle IN :stop_words")

with engine.connect() as conn:
    conn.execute(delete_query, stop_words=stop_words) # type: ignore

# Suppression des occurrences dans la table apparition_vo
delete_occurrences_query = text("""
    DELETE FROM apparition_vo
    WHERE id_mot_vo IN (
        SELECT id_mot_vo FROM mots_vo WHERE Libelle IN :stop_words
    )
""")

with engine.connect() as conn:
    conn.execute(delete_occurrences_query, stop_words=stop_words) # type: ignore