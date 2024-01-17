import os
import pandas as pd
from sqlalchemy import create_engine, text

# Configuration de la connexion à la base de données MySQL
db_username = 'root'
db_password = ''
db_host = 'localhost'  # Ou tout autre hôte MySQL
db_port = '3306'  # Port MySQL par défaut
db_name = 'projet_sae2'

engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

# Répertoire contenant les fichiers CSV
input_directory = '../csv_clean'

# Parcourir les fichiers CSV dans le répertoire
for file_name in os.listdir(input_directory):
    if 'vf' in file_name and file_name.endswith('_modified_tfidf.csv'):
        file_path = os.path.join(input_directory, file_name)
        print(f"Traitement du fichier : {file_path}")

        # Extraire le titre du fichier sans l'extension _vf_tfidf.csv
        titre = file_name.replace('_vf_modified_tfidf.csv', '')

        # Insérer le titre dans la table serie et récupérer l'ID de la série insérée
        connection = engine.connect()

        query = text("SELECT id_serie FROM serie WHERE titre = :titre")
        result = connection.execute(query, {"titre": titre})
        existing_serie = result.fetchone()

        if existing_serie:
            # Si la série existe, utilisez l'ID existant
            serie_id = existing_serie[0]
        else:
            # Si la série n'existe pas, insérez-la et récupérez l'ID
            try:
                query = text("INSERT INTO serie (titre) VALUES (:titre)")
                connection.execute(query, {"titre": titre})
                result = connection.execute(text("SELECT LAST_INSERT_ID()"))
                serie_id = result.scalar()
                print(f"ID de la série {titre} : {serie_id}")
            except Exception as e:
                connection.close()
                raise e

        # Charger le CSV dans un DataFrame
        df = pd.read_csv(file_path, encoding='latin-1', sep=';')

        # Filtrer les mots qui ne sont pas déjà dans la table mots_vf
        existing_words_query = text("SELECT Libelle FROM mots_vf")
        existing_words_result = connection.execute(existing_words_query)
        existing_words = {row[0] for row in existing_words_result.fetchall()}

        new_words_df = df[['Mot_nettoye']].rename(columns={'Mot_nettoye': 'Libelle'})
        new_words_df = new_words_df[~new_words_df['Libelle'].isin(existing_words)]

        # Supprimer les doublons dans le DataFrame
        new_words_df = new_words_df.drop_duplicates()

        try:
            # Insérer les données dans la table mots_vf
            new_words_df.to_sql('mots_vf', con=engine, if_exists='append', index=False)
        except Exception as e:
            connection.close()
            raise e
        finally:
            connection.close()

# Fermer le curseur et la connexion à la base de données
engine.dispose()

print("Terminé !")