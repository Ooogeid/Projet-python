<?php

class SeriesService {

    private $db;

    public function __construct($db) {
        $this->db = $db;
    }

    public function findSeries($keyword) {
        $query = "
            SELECT s.titre 
            FROM serie s
            JOIN apparition_vo av ON s.id_serie = av.id_serie
            JOIN mots_vo mv ON av.id_mot_vo = mv.id_mot_vo
            WHERE mv.Libelle = :keyword
            ORDER BY av.poids DESC
            LIMIT 10";

        $stmt = $this->db->prepare($query);
        $stmt->bindParam(':keyword', $keyword, PDO::PARAM_STR);
        $stmt->execute();

        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

}

?>
