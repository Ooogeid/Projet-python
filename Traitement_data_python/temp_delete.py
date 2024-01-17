import json
from sqlalchemy import create_engine, text

# Configuration de la connexion à la base de données MySQL
db_username = 'root'
db_password = ''
db_host = 'localhost'
db_port = '3306'
db_name = 'projet_sae'

# Chemin vers le fichier JSON contenant les stop words en français
stop_words_file = 'C:/wamp64/www/Projet_sae/src/Traitement_data_python/stop_words_french.json'

# Lire le contenu du fichier JSON
with open(stop_words_file, 'r') as file:
    stop_words = json.load(file)

# Créer un moteur SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}', echo=True)
conn = engine.connect()

# Parcourir les stop words et les supprimer de la base de données
for word in stop_words:
    # Exemple de requête pour supprimer les apparitions des mots de la table apparition_vf
    delete_apparition_vf_query = text("DELETE FROM apparition_vf WHERE id_mot_vf IN (SELECT id_mot_vf FROM mots_vf WHERE Libelle = :word)")
    # Exemple de requête pour supprimer les mots de la table mots_vf
    delete_mots_vf_query = text("DELETE FROM mots_vf WHERE Libelle = :word")

    # Supprimer les apparitions des mots de la table apparition_vf
    conn.execute(delete_apparition_vf_query, {"word": word})
    # Supprimer les mots de la table mots_vf
    conn.execute(delete_mots_vf_query, {"word": word})

print("Les mots du fichier stop_words_french.json ont été supprimés de la base de données.")