document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('searchButton');
    const keywordInput = document.getElementById('keyword');
    const resultDiv = document.getElementById('result');

    searchButton.addEventListener('click', function() {
        const keyword = keywordInput.value;
        console.log(keyword)
        if (keyword) {
            // Effectuer la requête au contrôleur
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '../backend/controller.php', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    displayResults(response);
                }
            };
            xhr.send('keyword=' + encodeURIComponent(keyword));
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
