<?php

use writecrow\Lemmatizer\Lemmatizer;
require 'Lemmatizer.php';

require_once("../detectlanguage-php-master/lib/detectlanguage.php");
use \DetectLanguage\DetectLanguage;
DetectLanguage::setApiKey("9e448e369dc91f43bc8a6e737ed2b70d");

class SeriesService {

    private $db;

    public function __construct($db) {
        $this->db = $db;
    }

    public function findSeries($keywords) {

        $series = [];
        $keywordsArray = explode(' ', $keywords);

        // On converti tous les mots en minuscules
        $keywordsArray = array_map('strtolower', $keywordsArray);
        $keywordsArray = array_map(function($word) {
            return preg_replace('/[^a-z0-9]/', '', $word);
        }, $keywordsArray);

        // Lemmatisation des mots-clés
        $keywords = array_map(['self', 'lemmatize'], $keywordsArray);

        // Recherche de séries dont le titre correspond au mot-clé
        $titleMatches = $this->searchSeriesByTitle($keywordsArray);
        
        // Si des correspondances de titre sont trouvées, les ajouter en premier
        if (!empty($titleMatches)) {
            $series = $this->mergeResults($series, $titleMatches);
        }
        
        $keywordsToSearch = array_diff($keywordsArray, array_column($titleMatches, 'titre'));

        foreach ($keywordsToSearch as $keyword) {

            $language = DetectLanguage::simpleDetect($keyword);

            // Choisissez la table appropriée en fonction de la langue
            $table = ($language == 'fr') ? 'vf' : 'vo';

            $query = "
                SELECT s.titre, SUM(av.poids) AS total_poids
                FROM serie s
                JOIN apparition_$table av ON s.id_serie = av.id_serie
                JOIN mots_$table mv ON av.id_mot_$table = mv.id_mot_$table
                WHERE mv.Libelle = :keyword
                GROUP BY s.titre
                ORDER BY total_poids DESC
                LIMIT 20";
    
            
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':keyword', $keyword, PDO::PARAM_STR);
            $stmt->execute();
    
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
            $series = $this->mergeResults($series, $result);
        }
    
        // On trie les séries par le poids total décroissant
        usort($series, function ($a, $b) {
            return $b['total_poids'] - $a['total_poids'];
        });
    
        // On limite les résultats à 20 séries
        $series = array_slice($series, 0, 20);
    
        return $series;
    }
    
    private function searchSeriesByTitle($keywords) {
        // Recherche de séries dont le titre correspond au mot-clé
        $query = "
            SELECT s.titre, SUM(av.poids) AS total_poids
            FROM serie s
            JOIN apparition_vo av ON s.id_serie = av.id_serie
            WHERE s.titre LIKE :keyword
            GROUP BY s.titre
            ORDER BY total_poids DESC
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

    private function mergeResults($series, $newResults) {
        // On fusionne les résultats en maintenant le total de poids par série
        foreach ($newResults as $result) {
            $title = $result['titre'];
            $totalWeight = $result['total_poids'];
            if (isset($series[$title])) {
                $series[$title]['total_poids'] += $totalWeight;
            } else {
                $series[$title] = $result;
            }
        }
        return $series;
    }
    
    private static function lemmatize($word) {
        $lemmatizedWord = Lemmatizer::getLemma($word);
        return $lemmatizedWord;
    }
    
}
?>

