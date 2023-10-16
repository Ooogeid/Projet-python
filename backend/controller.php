<?php

require 'service.php';

if (isset($_POST['keyword'])) {
    $keyword = $_POST['keyword']; // Récupérez le mot-clé depuis le front-end

    $dsn = 'mysql:host=localhost;dbname=projet_sae';
    $username = 'root';
    $password = '';

    try {
        $pdo = new PDO($dsn, $username, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $service = new SeriesService($pdo);
        $result = $service->findSeries($keyword);

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