
document.addEventListener('DOMContentLoaded', function() {

    const xhr = new XMLHttpRequest();
    xhr.open('GET', '../../backend/controller.php?categorie', true);

    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            console.log(xhr.responseText)
            const response = JSON.parse(xhr.responseText);
            displayResults(response);
        } else {
            console.error('Erreur :', xhr.status, xhr.statusText);
        }
    };

    xhr.send();

});

function displayResults(results) {
    const resultDiv = document.getElementById('result');
    let html = '';
  
    const seriesByCategory = {};
  
    if (results.length > 0) {
        // Parcourir les résultats et stocker les séries par catégorie
        results.forEach(function (result) {
        const category = result.nom;
        if (!seriesByCategory[category]) {
            seriesByCategory[category] = [];
        }
        seriesByCategory[category].push(result);
    });
  
    // Trier les catégories dans l'ordre alphabétique
    const sortedCategories = Object.keys(seriesByCategory).sort();

    // Générer le HTML trié par catégorie
    sortedCategories.forEach(function (category) {
    html += '<div class="category-title">' + category + '</div>';
    html += '<div class="series-container">';
    seriesByCategory[category].forEach(function (result) {
    html += '<a href="../serie/serie.html?id=' + result.id + '" class="serie-link">' + result.titre + '</a>';
        html += '<br>';
    });
    html += '</div>';
    });
    } else {
        html += 'Aucun résultat trouvé.';
    }
  
    resultDiv.innerHTML = html;
}