
document.addEventListener('DOMContentLoaded', function() {

    const xhr = new XMLHttpRequest();
    xhr.open('GET', '../../backend/controller.php?maListe', true);

    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
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
    if (results.length > 0) {
        html += '<ul class="ul-result">';
        results.forEach(function(result) {;
            html += '<li><a href="../serie/serie.html?id=' + result.id + '" class="lien-serie">' +
            '<img src="../img/img_series/' + result.id + '.jpg" alt="' + result.titre + '" class="img-series">' +
            '<p style="margin-top: 20px;">' + result.titre + '</p>' + '</a></li>';
        });
        html += '</ul>';
    } else {
        html += 'C\'est un peu vide ici...';
    }
    resultDiv.innerHTML = html;
}