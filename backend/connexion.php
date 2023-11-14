<?php

class Database {
    private static $instance;
    private $pdo;

    private function __construct() {
        $dsn = 'mysql:host=localhost;dbname=projet_sae';
        $username = 'root';
        $password = '';

        $this->pdo = new PDO($dsn, $username, $password);
        $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }

    public static function getInstance() {
        if (!self::$instance) {
            self::$instance = new self();
        }

        return self::$instance->pdo;
    }
}

?>
