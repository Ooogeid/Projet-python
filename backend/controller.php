<?php

require 'service.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {   

    $dsn = 'mysql:host=localhost;dbname=projet_sae';
    $username = 'root';
    $password = '';

    try {
        $pdo = new PDO($dsn, $username, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $service = new SeriesService($pdo);
        $jsonData = file_get_contents("php://input");
        $data = json_decode($jsonData, true);

        if (isset($data['credentials'])) {
            $credentials = $data['credentials'];
            $result = $service->findSeries($credentials);
        }
        else{
            $result = "Pas de credentials";
        }

        // Vous pouvez maintenant renvoyer $result en tant que réponse JSON, par exemple
        header('Content-Type: application/json');
        echo json_encode($result);
        
    } catch (PDOException $e) {
        // Gérer les erreurs de connexion à la base de données
        echo 'Erreur de connexion à la base de données : ' . $e->getMessage();
    }
} else {

    http_response_code(405); // Méthode non autorisée
    echo 'Méthode non autorisée.';
}

?>