document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('searchButton');
    const inputElement = document.getElementById('credentials');
    const resultDiv = document.getElementById('result');

    searchButton.addEventListener('click', function() {
        const credentials = inputElement.value;
        console.log(credentials);
    
        if (credentials) {
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '../backend/controller.php', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
        
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    displayResults(response);
                }
            };

            const data = { credentials: credentials }; // Créez un objet JSON
            xhr.send(JSON.stringify(data)); // Envoyez l'objet JSON

        } else {
            resultDiv.innerHTML = 'Veuillez entrer un mot-clé.';
        }
        
    });
    

    function displayResults(results) {
        let html = '<h2>Résultats :</h2>';
        console.log(results)
        if (results.length > 0) {
            html += '<ul>';
            results.forEach(function(result) {
                html += '<li>' + result.titre + '</li>';
            });
            html += '</ul>';
        } else {
            html += 'Aucun résultat trouvé.';
        }
        resultDiv.innerHTML = html;
    }
});
