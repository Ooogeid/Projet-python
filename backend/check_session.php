<?php
session_start();
$response = [];

if (isset($_SESSION['username'])) {
    $response['success'] = true;
    $response['username'] = $_SESSION['username'];
} else {
    $response['success'] = false;
}

header('Content-Type: application/json');
echo json_encode($response);

?>