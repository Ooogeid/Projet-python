
// Vérifier si une session est active
const xhr = new XMLHttpRequest();
xhr.open('GET', '../../backend/check_session.php', true);

xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
        const response = JSON.parse(xhr.responseText);
        if (response.success && response.username) {
            // Une session est active, l'utilisateur est connecté
            document.getElementById('usernameDisplay').textContent = response.username;
        } else {
            // Pas de session active, redirigez vers la page de connexion
            window.location.href = '../login/login.html';
        }
    } else {
        // Gestion des erreurs ici
        console.error('Erreur :', xhr.status, xhr.statusText);
    }
};

xhr.send();

document.addEventListener('DOMContentLoaded', function() {

    const searchButton = document.getElementById('searchButton');
    const inputElement = document.getElementById('credentials');
    const resultDiv = document.getElementById('result');
    const languageToggle = document.getElementById('languageToggle');

    let xhr = null;

    searchIcon.addEventListener('click', function(event) {
        performSearch(event);
    });

    inputElement.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Empêche le comportement par défaut du formulaire
            performSearch(event);
        }
    });

    languageToggle.addEventListener('change', function() {
        if (languageToggle.checked) {
            saveLanguageSelection('en');
        } else {
            saveLanguageSelection('fr'); // Par défaut la recherche est en français
        }
    });

    const logoutLink = document.getElementById('logoutLink'); // lien pour se déconnecter

    logoutLink.addEventListener('click', function(event) {
        event.preventDefault();

        const xhr = new XMLHttpRequest();
        xhr.open('GET', '../../backend/logout.php', true);

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                // Rediriger vers la page de connexion une fois déconnecté
                window.location.href = '../login/login.html';
            } else {
                console.error('Erreur :', xhr.status, xhr.statusText);
            }
        };

        xhr.send();
    });
    
    function saveLanguageSelection(language) { // On sauvegarde la sélection de la langue 
        localStorage.setItem('selectedLanguage', language);
        updateLanguageLabel(language);
    }

    function updateLanguageLabel(language) {
        const languageLabel = document.getElementById('language-span');
        if (language === 'en') {
            languageLabel.textContent = 'Anglais';
        } else {
            languageLabel.textContent = 'Français';
        }
    }


    function performSearch(event) {
        event.preventDefault();
        const keyword = inputElement.value;

        // Annulez la requête précédente si elle est en cours
        if (xhr && xhr.readyState !== 4) {
            xhr.abort();
        }

        if (keyword) {
            // Affichez le spinner pendant le chargement
            const spinner = document.querySelector('.loading-spinner');
            spinner.style.display = 'block';

            xhr = new XMLHttpRequest();
            xhr.open('POST', '../../backend/controller.php', true);
            xhr.setRequestHeader('Content-Type', 'application/json');

            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    displayResults(response);

                    // Masquez le spinner et réactivez le bouton de recherche
                    spinner.style.display = 'none';
                    searchButton.disabled = false;
                }
            };
            const selectedLanguage = localStorage.getItem("selectedLanguage");

            const credentials = {
                keyword: keyword,
                language: selectedLanguage 
            };
            xhr.send(JSON.stringify(credentials)); // Envoyez l'objet JSON
        } else {
            resultDiv.innerHTML = 'Veuillez entrer un mot-clé.';
        }
    }

    function displayResults(results) {
        let html = '';
        if (results.length > 0) {
            html += '<ul class="ul-result">';
            results.forEach(function(result) {;
                html += '<li><a href="../serie/serie.html?id=' + result.id + '" class="lien-serie">' + result.titre + '</a></li>';
            });
            html += '</ul>';
        } else {
            html += 'Aucun résultat trouvé.';
        }
        resultDiv.innerHTML = html;
    }

    function getSeriesData() {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '../../backend/controller.php', true);
    
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                const response = JSON.parse(xhr.responseText);
                displayResults(response); // Affichez les résultats en utilisant la fonction displayResults()
            } else {
                console.error('Erreur :', xhr.status, xhr.statusText);
            }
        };
    
        xhr.send();
    }

    // Appel à la fonction pour récupérer les données des séries lors du chargement de la page
    getSeriesData();
});
