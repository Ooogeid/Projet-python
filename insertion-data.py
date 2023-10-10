import os
import pandas as pd
from sqlalchemy import create_engine, text

# Configuration de la connexion à la base de données MySQL
db_username = 'root'
db_password = ''
db_host = 'localhost'  # Ou tout autre hôte MySQL
db_port = '3306'  # Port MySQL par défaut
db_name = 'projet_sae'

engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

# Répertoire contenant les fichiers CSV
input_directory = '../csv_clean'

# Parcourir les fichiers CSV dans le répertoire
for file_name in os.listdir(input_directory):
    if 'vo' in file_name and file_name.endswith('.csv'):
        file_path = os.path.join(input_directory, file_name)
        print(f"Traitement du fichier : {file_path}")

        # Extraire le titre du fichier sans l'extension .csv
        titre = file_name.replace('_vo_clusters.csv', '')

        # Insérer le titre dans la table serie et récupérer l'ID de la série insérée
        connection = engine.connect()
        transaction = connection.begin()
        try:
            query = text("INSERT INTO serie (titre) VALUES (:titre)")
            connection.execute(query, {"titre": titre})
            result = connection.execute(text("SELECT LAST_INSERT_ID()"))
            serie_id = result.scalar()
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e
        finally:
            connection.close()

        # Charger le CSV dans un DataFrame
        df = pd.read_csv(file_path, encoding='latin-1', sep=';')

        # Insérer les données de mots_vo_df dans la table mots_vo
        mots_vo_df = df[['Mot_nettoye']].rename(columns={'Mot_nettoye': 'Libelle'})

        connection = engine.connect()
        transaction = connection.begin()
        try:
            # Insérer les données dans la table mots_vo
            mots_vo_df.to_sql('mots_vo', con=engine, if_exists='append', index=False)

            # Récupérer les IDs des mots insérés
            libelles_str = ', '.join(f"'{libelle}'" for libelle in mots_vo_df['Libelle'])
            query = text(f"SELECT id_mot_vo, Libelle FROM mots_vo WHERE Libelle IN ({libelles_str})")
            result = connection.execute(query, {"libelles": tuple(mots_vo_df['Libelle'])})
            mots_vo_ids_df = result.fetchall()
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e
        finally:
            connection.close()

        # Créer une DataFrame pour apparition_vo avec les IDs
        apparition_vo_df = pd.DataFrame(columns=['id_serie', 'id_mot_vo', 'poids'])

        for index, row in df.iterrows():
            libelle_mot = row['Mot_nettoye']
            poids = row['Poids']

            # Recherche de l'ID du mot dans mots_vo_ids_df
            id_mot_vo = next(item for item in mots_vo_ids_df if item[1] == libelle_mot)[0]

            # Ajouter les données à la DataFrame apparition_vo
            apparition_vo_df = apparition_vo_df.append({'id_serie': serie_id, 'id_mot_vo': id_mot_vo, 'poids': poids}, ignore_index=True)

        # Insérer les données dans la table apparition_vo
        connection = engine.connect()
        transaction = connection.begin()
        try:
            apparition_vo_df.to_sql('apparition_vo', con=engine, if_exists='append', index=False)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e
        finally:
            connection.close()

# Fermer le curseur et la connexion à la base de données
engine.dispose()

print("Terminé !")
