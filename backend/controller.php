<?php

require 'service.php';
require 'connexion.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    try {
        $pdo = Database::getInstance();
        $service = new SeriesService($pdo);
        $jsonData = file_get_contents("php://input");
        $credentials = json_decode($jsonData, true);
        
        // Gestion de la recherche de mots clés
        if (isset($credentials['keyword'])) {
            $result = $service->findSeries($credentials);
        }
        // Gestion de l'ajout de like 
        elseif (isset($credentials['like'])) {
            $serieId = $credentials['like'];
            $userId = $_SESSION['id_users'];
            $service->addLike($serieId, $userId);
            $result = "Like ajouté avec succès";
        } 
        elseif(isset($credentials['remove'])){
            $serieId = $credentials['remove'];
            $userId = $_SESSION['id_users'];
            $service->removeLike($serieId, $userId);
            $result = "Like supprimé avec succès";
        }
        
        header('Content-Type: application/json');
        echo json_encode($result);
    } catch (PDOException $e) {
        echo 'Erreur de connexion à la base de données : ' . $e->getMessage();
    }
} 

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Gérer les requêtes GET avec un ID spécifié
    try {
        $pdo = Database::getInstance();
        $service = new SeriesService($pdo);
        
        if (isset($_GET['id'])) {
            $serieId = $_GET['id'];
            // récupération des données de la série pour le détail
            $serieData = $service->getSerieData($serieId);
            if ($serieData) {
                $result['description'] = utf8_encode($serieData['description']);
                $result['titre'] = utf8_encode($serieData['titre']);
            } else {
                $result = ['error' => 'Série non trouvée'];
                http_response_code(404);
            }
        } 
        elseif (isset($_GET['maListe'])) {  // Récupération de la liste des séries de l'utilisateur
            $series = $service->getMaliste();
            $result = $series;
        } 
        elseif(isset($_GET['categorie'])){
            $series = $service->getSeriesByCategories();
            $result = $series;
        }
        else {
            // récupération des données de la série pour le détail
            $series = $service->getAllSeries();
            $result = $series;
        }
        
        header('Content-Type: application/json');
        echo json_encode($result);
    } catch (PDOException $e) {
        echo 'Erreur de connexion à la base de données : ' . $e->getMessage();
    }
}


?>