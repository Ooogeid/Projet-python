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
        $addedSeries = [];

        // On sépare chaque mot reçu par un espace
        $keywordsArray = explode(' ', $keywords);

        // On converti tous les mots en minuscules
        $keywordsArrayMinuscule = array_map('strtolower', $keywordsArray);

        //On récupère les mots sans caractères spéciaux (sauf les chiffres)
        $keywordsArrayMinuscule = array_map(function($word) {
            return preg_replace('/[^a-z0-9]/', '', $word);
        }, $keywordsArrayMinuscule); 
        
        // Lemmatisation des mots-clés
        $keywordsLemma = array_map(['self', 'lemmatize'], $keywordsArrayMinuscule);

        // Recherche de séries dont le titre correspond au mot-clé (on ne lemmatise pas celui-ci)
        $titleMatches = $this->searchSeriesByTitle($keywordsArrayMinuscule);

        // Si des correspondances de titre sont trouvées, les ajouter en premier
        foreach ($titleMatches as $titleMatch) {
            $seriesTitle = $titleMatch['titre'];
            if (!isset($addedSeries[$seriesTitle])) {
                $series[] = $titleMatch;
                $addedSeries[$seriesTitle] = true;
            }
        }
        
        $keywordsToSearch = array_diff($keywordsLemma, array_column($titleMatches, 'titre'));

        // Pour chaque mot-clé restant, on recherche les séries correspondantes
        foreach ($keywordsArrayMinuscule as $keyword) {
            // On détecte la langue du mot-clé
            $language = DetectLanguage::simpleDetect($keyword);

            // Langue française ou anglaise
            $table = ($language == 'fr') ? 'vf' : 'vo';
            
            $query = "
                SELECT s.titre, av.poids AS poids
                FROM serie s
                JOIN apparition_$table av ON s.id_serie = av.id_serie
                JOIN mots_$table mv ON av.id_mot_$table = mv.id_mot_$table
                WHERE mv.Libelle = :keyword
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
                }
            }
        }

        // On trie les séries par le poids total décroissant
        usort($series, function ($a, $b) {
            return $b['poids'] - $a['poids'];
        });

        // On ne garde que les 20 premiers résultats
        $series = array_slice($series, 0, 20);
        
        return $series;
    }
    
    // Recherche de séries dont le titre correspond au mot-clé
    private function searchSeriesByTitle($keywords) {
        // Recherche de séries dont le titre correspond au mot-clé
        $query = "
            SELECT s.titre, av.poids AS poids
            FROM serie s
            JOIN apparition_vo av ON s.id_serie = av.id_serie
            WHERE s.titre LIKE :keyword
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
    
    private static function lemmatize($word) {
        $lemmatizedWord = Lemmatizer::getLemma($word);
        return $lemmatizedWord;
    }
    
}
?>

