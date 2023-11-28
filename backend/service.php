<?php

use writecrow\Lemmatizer\Lemmatizer;
require 'Lemmatizer.php';

class SeriesService {

    private $db;

    public function __construct($db) {
        $this->db = $db;
    }

    // Première fonction de l'api permettant de traiter les mots-clés reçus en les séparant, 
    // en les filtrant, en les convertissant en minuscules, en les lemmatisant 
    // puis en recherchant d'abord si il y a des correspondances de titre 
    // (afin de ressortir en premier les correspondances directs de titres)
    private function preprocessKeywords($keywords) {

        // On sépare chaque mot reçu par un espace
        $keywordsArray = explode(' ', $keywords);
    
        // Filtrer les mots-clés pour exclure les éléments vides
        $keywordsArray = array_filter($keywordsArray, 'strlen');
    
        // Rejoindre les mots-clés pour former une chaîne
        $cleanedKeywords = implode(' ', $keywordsArray);
    
        // On convertit tous les mots en minuscules
        $keywordsArrayMinuscule = array_map('strtolower', $keywordsArray);
    
        // On récupère les mots sans caractères spéciaux (sauf les chiffres)
        $keywordsArrayMinuscule = array_map(function($word) {
            return preg_replace('/[^a-z0-9]/', '', $word);
        }, $keywordsArrayMinuscule);
    
        // Lemmatisation des mots-clés
        $keywordsLemma = array_map([$this, 'lemmatize'], $keywordsArrayMinuscule);

        // Recherche de séries dont le titre correspond au mot-clé (on ne lemmatise pas celui-ci)
        $titleMatches = $this->searchSeriesByTitle($keywordsArrayMinuscule);


        return [
            'cleanedKeywords' => $cleanedKeywords,
            'keywordsArrayMinuscule' => $keywordsArrayMinuscule,
            'keywordsLemma' => $keywordsLemma,
            'titleMatches' => $titleMatches
        ];
    }
    

    // Fonction de comparaison des séries, utilisée pour le tri des séries
    private function compareSeries($a, $b, $seriesWeights, $commonKeywordsCount) {
        $countA = $commonKeywordsCount[$a['titre']];
        $countB = $commonKeywordsCount[$b['titre']];
        
        if ($countA === $countB) {
            $sumA = array_sum($seriesWeights[$a['titre']]);
            $sumB = array_sum($seriesWeights[$b['titre']]);
    
            if ($sumA === $sumB) {
                return 0;
            }
    
            return ($sumA > $sumB) ? -1 : 1;
        }
    
        return ($countA > $countB) ? -1 : 1;
    }

    // Fonction majeur de l'api qui va ressortir les séries avec le plus grand poids
    // mais aussi celles qui ont le plus de mots clés commun avec la recherche
    public function findSeries($credentials) {
        
        $series = [];
        $addedSeries = [];
        $processedKeywords = $this->preprocessKeywords($credentials['keyword']); // appel de la première fonction pour récupérer les données propre

        // Créez un tableau pour stocker les mots-clés de chaque série
        $seriesKeywords = [];
        // Créez un tableau pour stocker les poids des mots-clés de chaque série
        $seriesWeights = [];
    
        // Si des correspondances de titre sont trouvées, les ajouter en premier
        foreach ($processedKeywords['titleMatches'] as $titleMatch) {
            $seriesTitle = $titleMatch['titre'];
            if (!isset($addedSeries[$seriesTitle])) {
                $series[] = $titleMatch;
                $addedSeries[$seriesTitle] = true;
    
                // Ajoutez les mots-clés de cette série au tableau des mots-clés
                $seriesKeywords[$seriesTitle] = $processedKeywords['keywordsArrayMinuscule'];
    
                // Ajoutez les poids des mots-clés de cette série au tableau des poids
                $seriesWeights[$seriesTitle] = [$titleMatch['poids']];
            }
        }
        
        $keywordsToSearch = array_diff($processedKeywords['keywordsLemma'], array_column($processedKeywords['titleMatches'], 'titre'));
    
        // Pour chaque mot-clé restant, on recherche les séries correspondantes
        foreach ($processedKeywords['keywordsArrayMinuscule'] as $keyword) {

            // On détecte la langue du mot-clé
            $language = $credentials['language'];

            // Langue française ou anglaise
            $table = ($language == 'fr') ? 'vf' : 'vo';
            $query = "
                SELECT s.id_serie as id, s.titre, av.poids AS poids
                FROM serie s
                JOIN apparition_$table av ON s.id_serie = av.id_serie
                WHERE 1
                AND av.id_mot_$table = 
                (SELECT mv.id_mot_$table 
                FROM mots_$table mv
                WHERE mv.Libelle LIKE :keyword LIMIT 1) 
                ORDER BY poids DESC
                LIMIT 20";
    
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':keyword', $keyword, PDO::PARAM_STR);
            $stmt->execute();
    
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
            foreach ($result as $seriesResult) {
                $seriesTitle = $seriesResult['titre'];
                if (!isset($addedSeries[$seriesTitle])) {
                    $series[] = $seriesResult;
                    $addedSeries[$seriesTitle] = true;
            
                    // Ajoutez les mots-clés de cette série au tableau des mots-clés
                    $seriesKeywords[$seriesTitle] = [$keyword];
                    // Ajoutez les poids des mots-clés de cette série sous forme de tableau
                    $seriesWeights[$seriesTitle] = [$seriesResult['poids']];
                    

                } else {
                    // Si la série existe déjà, ajoutez le poids du mot-clé à son tableau de poids
                    $seriesWeights[$seriesTitle] = [$seriesResult['poids']];
                }
            }
        }
    
        // Créez un tableau pour stocker le nombre de mots-clés en commun avec la recherche pour chaque série
        $commonKeywordsCount = [];
    
        // Pour chaque série, calculez le nombre de mots-clés en commun avec la recherche
        foreach ($series as $seriesResult) {
            $seriesTitle = $seriesResult['titre'];
            $commonKeywordsCount[$seriesTitle] = count(array_intersect($seriesKeywords[$seriesTitle], $processedKeywords['keywordsArrayMinuscule']));
        }

        // Triez les séries par le nombre de mots-clés en commun avec la recherche
        // puis par la somme du poids des mots-clés dans chaque série
        uasort($series, function ($a, $b) use ($seriesWeights, $commonKeywordsCount) {
            return $this->compareSeries($a, $b, $seriesWeights, $commonKeywordsCount);
        });

        // Obtenir les clés triées
        $sortedSeriesKeys = array_keys($series);

        // Créer un tableau pour stocker les séries triées
        $sortedSeries = [];

        // Remplir le tableau des séries triées avec les données complètes
        foreach ($sortedSeriesKeys as $key) {
            $sortedSeries[] = $series[$key];
        }

        // On ne garde que les 20 premiers résultats
        $top20Series = array_slice($sortedSeries, 0, 20);

        // Retournez le tableau des 20 premières séries triées
        return $top20Series;
    }

    // Recherche de séries dont le titre correspond au mot-clé
    private function searchSeriesByTitle($keywords) {
        // Recherche de séries dont le titre correspond au mot-clé
        $query = "
            SELECT s.id_serie as id, s.titre, av.poids AS poids
            FROM serie s
            JOIN apparition_vo av ON s.id_serie = av.id_serie
            WHERE LOWER(s.titre) LIKE LOWER(:keyword)
            ORDER BY poids DESC
            LIMIT 20";
    
        $matches = [];
    
        foreach ($keywords as $keyword) {
            $searchKeyword = "%" . $keyword . "%";
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':keyword', $searchKeyword, PDO::PARAM_STR);
            $stmt->execute();
            
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
            if (!empty($result)) {
                $matches = array_merge($matches, $result);
            }
        }

        return $matches;
    }
    
    // Fonction pour lemmatiser les mots grâce à une librairie externe (que en anglais pour l'instant)
    private static function lemmatize($word) {
        if (empty($word)) {
            return $word; 
        }
        else{
            $lemmatizedWord = Lemmatizer::getLemma($word);
            return $lemmatizedWord;    
        }
    }

    // Fonction pour récup les infos d'une série lorsque l'utilisateur clique sur une série en particulière
    public function getSerieData($serieId) {
        
        $sql = "SELECT titre, description FROM serie WHERE id_serie = :id";
        $stmt = $this->db->prepare($sql);
        $stmt->bindParam(':id', $serieId, PDO::PARAM_INT);
        $stmt->execute();
        $serieData = $stmt->fetch(PDO::FETCH_ASSOC);
        return $serieData;
    }
    
    // Fonction pour vérifier si un like existe déjà pour une série et un user donnée
    public function getLike($serieId, $userId) {
        $sql = "SELECT * FROM likes WHERE id_serie = :id_serie AND id_users = :id_users";
        $stmt = $this->db->prepare($sql);
        $stmt->bindParam(':id_serie', $serieId, PDO::PARAM_INT);
        $stmt->bindParam(':id_users', $userId, PDO::PARAM_INT);
        $stmt->execute();
        $like = $stmt->fetch(PDO::FETCH_ASSOC);
        return $like;
    }

    // Fonction pour ajouter un like à une série pour un user donnée
    public function addLike($serieId, $userId) {
        $existingLike = $this->getLike($serieId, $userId); // On vérifie si le like existe déjà
        if ($existingLike) {
            return; // on ignore l'ajout du like si il existe déjà
        }
        else{
            $sql = "INSERT INTO likes (id_serie, id_users, date_liked) VALUES (:id, :id_users, NOW())";
            $stmt = $this->db->prepare($sql);
            $stmt->bindParam(':id', $serieId, PDO::PARAM_INT);
            $stmt->bindParam(':id_users', $userId, PDO::PARAM_INT);
            $stmt->execute();
        }
    }

    // Fonction pour supprimer un like à une série pour un user donnée
    public function removeLike($serieId, $userId){
        $existingLike = $this->getLike($serieId, $userId); 
        if(!$existingLike){
            return; // on ignore la suppression du like si il n'existe pas
        }
        $sql = "DELETE FROM likes WHERE id_serie = :id_serie AND id_users = :id_users";
        $stmt = $this->db->prepare($sql);
        $stmt->bindParam(':id_serie', $serieId, PDO::PARAM_INT);
        $stmt->bindParam(':id_users', $userId, PDO::PARAM_INT);
        $stmt->execute();
    }

    public function getAllSeries($page, $seriesPerPage){
        $offset = ($page - 1) * $seriesPerPage;
    
        $sql = "SELECT id_serie as id, titre FROM serie ORDER BY titre ASC LIMIT :limit OFFSET :offset";
        $stmt = $this->db->prepare($sql);
        $stmt->bindValue(':limit', $seriesPerPage, PDO::PARAM_INT);
        $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
        $stmt->execute();
        $series = $stmt->fetchAll(PDO::FETCH_ASSOC);
        return $series;
    }

    public function getMaliste(){
        $sql = "SELECT s.id_serie as id, s.titre
                FROM serie s
                JOIN likes l ON s.id_serie = l.id_serie
                WHERE l.id_users = :user_id 
                ORDER BY s.titre ASC";
        $stmt = $this->db->prepare($sql);
        $stmt->bindParam(':user_id', $_SESSION['id_users'], PDO::PARAM_INT);
        $stmt->execute();
        $series = $stmt->fetchAll(PDO::FETCH_ASSOC);
        return $series;
    }

    public function getSeriesByCategories(){
        $query = "SELECT s.id_serie as id, s.titre, c.nom 
        FROM serie s
        JOIN categorie c ON s.id_categorie = c.id_categorie
        ORDER BY s.id_categorie";
        $stmt = $this->db->prepare($query);
        $stmt->execute();
        $series = $stmt->fetchAll(PDO::FETCH_ASSOC);
        return $series;
    }

    public function getSerieKeywords($serieId){
        $sql = "
            SELECT mv.Libelle AS keyword
            FROM serie s
            JOIN apparition_vo av ON s.id_serie = av.id_serie
            JOIN mots_vo mv ON av.id_mot_vo = mv.id_mot_vo
            JOIN likes l ON s.id_serie = l.id_serie
            WHERE l.id_users = :user_id
            AND s.id_serie = :serie_id
            GROUP BY mv.Libelle
            ORDER BY av.poids DESC
            LIMIT 40";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bindParam(':user_id', $_SESSION['id_users'], PDO::PARAM_INT);
        $stmt->bindParam(':serie_id', $serieId, PDO::PARAM_INT);
        $stmt->execute();
        $keywords = $stmt->fetchAll(PDO::FETCH_COLUMN);
        
        return $keywords;
    }

    public function recommandation(){
        $series = $this->getMaliste();
    
        // Tableau pour stocker tous les mots clés
        $allKeywords = [];
        
        foreach($series as $serie){
            $id = $serie['id'];
    
            // Récupérer les mots clés des séries likées par l'utilisateur
            $keywords = $this->getSerieKeywords($id);
    
            // Ajouter les mots clés à $allKeywords
            $allKeywords = array_merge($allKeywords, $keywords);
        }
        // foreach($allKeywords as $i){
        //     echo $i, " ";
        // }
        
        // Tableau pour stocker les séries recommandées
        $recommendedSeries = [];
    
        // Pour chaque mot clé, trouver la série avec le poids le plus important
        foreach($allKeywords as $keyword){
            $query = "
                SELECT s.id_serie AS id, s.titre, av.poids AS poids
                FROM serie s
                JOIN apparition_vo av ON s.id_serie = av.id_serie
                JOIN mots_vo mv ON av.id_mot_vo = mv.id_mot_vo
                LEFT JOIN (
                    SELECT id_serie
                    FROM likes
                    WHERE id_users = :user_id
                ) l ON s.id_serie = l.id_serie
                WHERE mv.Libelle = :keyword
                AND l.id_serie IS NULL
                ORDER BY poids DESC
                LIMIT 1";
    
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':user_id', $_SESSION['id_users'], PDO::PARAM_INT);
            $stmt->bindParam(':keyword', $keyword, PDO::PARAM_STR);
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
    
            if($result){
                $recommendedSeries[$result['id']] = $result;
            }
        }
        // foreach($recommendedSeries as $i){
        //     foreach($i as $x){
        //         echo $x, " ";
        //     }
        // }
        // Trier les séries recommandées par poids décroissant
        usort($recommendedSeries, function($a, $b) {
            return $b['poids'] - $a['poids'];
        });
    
        // Limiter le nombre de séries recommandées à 20
        $recommendedSeries = array_slice($recommendedSeries, 0, 20);
    
        return array_values($recommendedSeries);
    }


}
?>

