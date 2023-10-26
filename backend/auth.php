<?php
require_once('connexion.php'); // fichier pour avoir l'instance de connexion à la bdd


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    $isLogin = (bool)$_POST['isLogin'];

    // Instance pdo de la bdd
    $pdo = Database::getInstance();

    if ($isLogin) {
        // C'est une tentative de connexion
        // Vérification de l'utilisateur dans la base de données
        $query = "SELECT * FROM users WHERE username = :username";
        $statement = $pdo->prepare($query);
        $statement->bindParam(':username', $username);
        $statement->execute();

        $row = $statement->fetch(PDO::FETCH_ASSOC);
        
        if ($row) {
            $storedPassword = $row['password'];
            if (password_verify($password, $storedPassword)) {
                session_start(); // Démarrez la session
                $_SESSION['username'] = $username; // on stock le username en session 
                $response = [
                    'success' => true,
                    'message' => 'Connecté avec succès',
                    'username' => $username // Incluez le nom d'utilisateur dans la réponse
                ];
            } else {
                $response = [
                    'success' => false,
                    'message' => 'Mot de passe incorrect.'
                ];
            }
        } else {
            $response = array('success' => false, 'message' => 'L\'utilisateur n\'existe pas.');
        }
    } else {
        // C'est une tentative d'inscription
        // Vérification si l'utilisateur existe déjà
        $query = "SELECT * FROM users WHERE username = :username";
        $statement = $pdo->prepare($query);
        $statement->bindParam(':username', $username);
        $statement->execute();

        if ($statement->rowCount() > 0) {
            $response = array('success' => false, 'message' => 'Cet utilisateur existe déjà.');
        } else {
            // L'utilisateur n'existe pas, on l'inscrit avec mot de passe haché
            $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
            $query = "INSERT INTO users (username, password) VALUES (:username, :password)";
            $statement = $pdo->prepare($query);
            $statement->bindParam(':username', $username);
            $statement->bindParam(':password', $hashedPassword);

            if ($statement->execute()) {
                $response = array('success' => true, 'message' => 'Inscription réussie !');
            } else {
                $response = array('success' => false, 'message' => 'Erreur lors de l\'inscription.');
            }
        }
    }

    // Envoi de la réponse JSON
    header('Content-Type: application/json');
    echo json_encode($response);
}
?>
