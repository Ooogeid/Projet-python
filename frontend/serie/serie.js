const urlParams = new URLSearchParams(window.location.search);
const serieId = urlParams.get('id');

// Faire une requête AJAX pour obtenir les données de la série
const xhr = new XMLHttpRequest();
xhr.open('GET', `../../backend/controller.php?id=${serieId}`, true); 

xhr.onload = function () {
    if (xhr.status === 200) {
        const serie = JSON.parse(xhr.responseText);

        const titre = document.getElementById('serie-title');
        const description = document.getElementById('serie-description');

        titre.textContent = serie.titre;
        description.textContent = serie.description;
    } else {
        console.error('Une erreur s\'est produite lors de la récupération des données de la série.');
    }
};

xhr.send();