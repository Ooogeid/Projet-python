const urlParams = new URLSearchParams(window.location.search);
const serieId = urlParams.get('id');

// Fonction pour effectuer une requête AJAX
function makeRequest(url, method = 'GET', body = null) {
  return new Promise(function(resolve, reject) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);

    xhr.onload = function() {
      if (xhr.status === 200) {
        resolve(xhr.responseText);
      } else {
        reject(Error(xhr.statusText));
      }
    };

    xhr.onerror = function() {
      reject(Error('Une erreur réseau s\'est produite.'));
    };

    if (method === 'POST') {
      xhr.setRequestHeader('Content-Type', 'application/json');
    }

    xhr.send(body);
  });
}

// Faire une requête AJAX pour obtenir les données de la série
makeRequest(`../../backend/controller.php?id=${serieId}`)
  .then(function(responseText) {
    const serie = JSON.parse(responseText);
    const titre = document.getElementById('serie-title');
    const description = document.getElementById('serie-description');
    titre.textContent = serie.titre;
    description.textContent = serie.description;

    const img_series = document.getElementById('serie-image');
    img_series.setAttribute('src', "../img/img_series/" + serieId + ".jpg");
    
    // Faire une autre requête AJAX pour vérifier si la série est dans la liste
    return makeRequest('../../backend/controller.php?maListe');
  })
  .then(function(responseText) {
    const maListe = JSON.parse(responseText);

    // Comparez la série sélectionnée avec les séries de la liste
    const serieEstDansLaListe = maListe.some(serie => serie.id === serieId);

    // Affichez ou masquez les boutons en fonction du résultat
    const removeButton = document.getElementById('remove');
    if (serieEstDansLaListe) {
      removeButton.style.display = 'block';
      likeButton.style.display = 'none';
    } else {
      removeButton.style.display = 'none';
      likeButton.style.display = 'block';
    }
  })
  .catch(function(error) {
    console.error('Une erreur s\'est produite :', error);
  });

// Gestion des likes (ajout d'un like)
const likeButton = document.getElementById('like');
const likePopup = document.getElementById('like-popup');
const likePopupMessage = document.getElementById('like-popup-message');

likeButton.addEventListener('click', function() {
  makeRequest('../../backend/controller.php', 'POST', JSON.stringify({ like: serieId }))
    .then(function() {
      likePopup.classList.add('show');
      likePopupMessage.textContent = 'Like ajouté avec succès';

      // Supprimez la classe "show" après 2 secondes pour masquer la pop-up
      setTimeout(function() {
        likePopup.classList.remove('show');
      }, 2000);
    })
    .catch(function(error) {
      console.error('Erreur lors de l\'ajout du like :', error);
    });
});

// Gestion du retrait de la série
const removeButton = document.getElementById('remove');
removeButton.addEventListener('click', function() {
  makeRequest('../../backend/controller.php', 'POST', JSON.stringify({ remove: serieId }))
    .then(function() {
      likePopup.classList.add('show');
      likePopupMessage.textContent = 'Série retirée avec succès';

      // Supprimez la classe "show" après 2 secondes pour masquer la pop-up
      setTimeout(function() {
        likePopup.classList.remove('show');
      }, 2000);
    })
    .catch(function(error) {
      console.error('Erreur lors du retrait de la série :', error);
    });
});