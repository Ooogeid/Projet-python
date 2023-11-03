const urlParams = new URLSearchParams(window.location.search);
const serieId = urlParams.get('id');

// Faire une requête AJAX pour obtenir les données de la série
const xhr = new XMLHttpRequest();
xhr.open('GET', `../../backend/controller.php?id=${serieId}`, true); 

xhr.onload = function () {
    if (xhr.status === 200) {
        console.log(xhr.responseText)
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

// Gestion des likes (ajout d'un like)
const likeButton = document.getElementById('like');
likeButton.addEventListener('click', function() {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '../../backend/controller.php', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log('Like ajouté avec succès');
        } else {
            console.error('Erreur lors de l\'ajout du like');
        }
    };

    const credentials = JSON.stringify({ like: serieId });
    xhr.send(credentials);
});
