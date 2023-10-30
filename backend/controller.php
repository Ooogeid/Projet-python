<?php

require 'service.php';
require 'connexion.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Gérer les requêtes POST
    try {
        $pdo = Database::getInstance();
        $service = new SeriesService($pdo);
        $jsonData = file_get_contents("php://input");
        $credentials = json_decode($jsonData, true);

        if (isset($credentials['keyword'])) {
            $result = $service->findSeries($credentials);
        } else {
            $result = "Pas de credentials";
        }

        header('Content-Type: application/json');
        echo json_encode($result);
    } catch (PDOException $e) {
        echo 'Erreur de connexion à la base de données : ' . $e->getMessage();
    }
} elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Gérer les requêtes GET avec un ID spécifié
    try {
        $pdo = Database::getInstance();
        $service = new SeriesService($pdo);

        $serieId = $_GET['id'];
        $serieData = $service->getSerieData($serieId);
        if ($serieData) {
            $result = $serieData;
        } else {
            $result = ['error' => 'Série non trouvée'];
            http_response_code(404);
        }

        header('Content-Type: application/json');
        echo json_encode($result);
    } catch (PDOException $e) {
        echo 'Erreur de connexion à la base de données : ' . $e->getMessage();
    }
} else {
    // Gérer d'autres cas de requêtes non autorisées
    http_response_code(405);
    echo 'Méthode non autorisée.';
}


?>