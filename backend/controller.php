<?php

require 'service.php';
require 'connexion.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    try {
        $pdo = Database::getInstance();
        $service = new SeriesService($pdo);
        $jsonData = file_get_contents("php://input");
        $data = json_decode($jsonData, true);

        if (isset($data['credentials'])) {
            $credentials = $data['credentials'];
            $result = $service->findSeries($credentials);
        } else {
            $result = "Pas de credentials";
        }
        header('Content-Type: application/json');
        echo json_encode($result);
    } catch (PDOException $e) {
        echo 'Erreur de connexion à la base de données : ' . $e->getMessage();
    }
} else {
    http_response_code(405); 
    echo 'Méthode non autorisée.';
}
?>