
--- Diego Mas-Bouvry et Thomas Robin -- 
Non alternant et alternant

Le projet est construit de la manière suivante : 

- Le répertoire Traitement_data_python contient tout les scripts python que nous avons développés pour traiter les données de l'archive téléchargé sur moodle jusqu'à
avoir une base de données contenant toutes les données. Nous avons laissé certains scripts développés qui nous ont été utiles dans le déroulement du processus, mais pas forcément obligatoire.

- Le répertoire backend contient tout les scripts PHP, en commançant par le service qui s'occupe de requêter la base, puis ensuite passe l'information au controller qui 
lui s'occupe de relayer en fonction du type de requête, puis renvoi au front en JSON.
Nous avons également les scripts auth, check_session, logout ou encore connexion qui sont chargés de la connexion à la bdd ou de la gestion des users sur le site.
Le script Lemmatizer est un script externe que nous avons récupérer sur github, il permet de lemmatiser les mots rentrés par l'utilisateur (uniquement en anglais malheuresment), il utilise le répertoire data_lemma pour effectuer sa lemmatisation.

- Le répertoire frontend contient toutes les pages du sites, avec pour chacune leur JS, HTML et CSS. Nous avons également le répertoire img qui contient les images / logos du site.

- Pour finir, le répertoire BDD qui contient le script SQL de la base de données.

Lien pour télécharger la VM : https://drive.google.com/file/d/1hop5kLlW3f-eab5HlLvXDR8wHHShbiVa/view?usp=drive_link