L'ordre d'execution des scripts afin d'obtenir les csv finals de chaque série prêt à être utilisé pour insérer les données en base est le suivants : 

1. dezip.py // Premier script pour tout dézipper et n'avoir plus que des fichiers srt 

2. Trie_sous_titres.py // sert à organiser les sous-titres des séries dans un répertoire principal (évite que certains srt se retrouvent dans des sous dossiers)

3. convert.py // extrait les mots des fichiers CSV, les compte et les enregistre dans un fichier CSV séparé pour les sous-titres VO et VF

4. process_vo.py // nettoie et lemmatise les mots des fichiers CSV de sous-titres VO. Il calcule ensuite la matrice de similarité TF-IDF et effectue un clustering des mots avec K-Means. 
Le résultat est un fichier CSV contenant les mots nettoyés, lemmatisés, ainsi que leur valeur TF-IDF et leur cluster.

5. process_vf // pareil mais en français

6. insertion-data.py // script permettant d'insérer les données clean en base

7. insertion-description 

8. insertion-categorie

9.