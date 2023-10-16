<?php

use writecrow\Lemmatizer\Lemmatizer;
require 'Lemmatizer.php';

class SeriesService {

    private $db;

    public function __construct($db) {
        $this->db = $db;
    }

    public function findSeries($keywords) {
        // Initialisation de la liste des séries
        $series = [];
        $keywordsArray = explode(' ', $keywords);

        // Lemmatization des mots-clés
        $keywords = array_map(['self', 'lemmatize'], $keywordsArray);

        // Effectuer une requête pour chaque mot-clé
        foreach ($keywords as $keyword) {
            $query = "
                SELECT s.titre, SUM(av.poids) AS total_poids
                FROM serie s
                JOIN apparition_vo av ON s.id_serie = av.id_serie
                JOIN mots_vo mv ON av.id_mot_vo = mv.id_mot_vo
                WHERE mv.Libelle = :keyword
                GROUP BY s.titre
                ORDER BY total_poids DESC
                LIMIT 20";

            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':keyword', $keyword, PDO::PARAM_STR);
            $stmt->execute();

            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
            // Ajouter les résultats à la liste des séries
            $series = $this->mergeResults($series, $result);
        }

        // Trier les séries par le total de poids décroissant
        usort($series, function ($a, $b) {
            return $b['total_poids'] - $a['total_poids'];
        });

        // Limiter les résultats à 10 séries
        $series = array_slice($series, 0, 20);

        return $series;
    }

    private function mergeResults($series, $newResults) {
        // Fusionner les résultats en maintenant le total de poids par série
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

