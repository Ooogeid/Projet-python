
// Vérifier si une session est active
const xhr = new XMLHttpRequest();
xhr.open('GET', '../../backend/check_session.php', true);

xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
        const response = JSON.parse(xhr.responseText);
        if (response.success && response.username) {
            // Une session est active, l'utilisateur est connecté
            document.getElementById('usernameDisplay').textContent = response.username;

            const recommenderXhr = new XMLHttpRequest();
            recommenderXhr.open('GET', '../../backend/controller.php?recommandation=true', true);
            
            recommenderXhr.onload = function () {
                if (recommenderXhr.status >= 200 && recommenderXhr.status < 300) {
                    const recommandations = JSON.parse(recommenderXhr.responseText);
                    console.log('Recommandations:', recommandations);
                } else {
                    console.error('Erreur lors de la récupération des recommandations:', recommenderXhr.status, recommenderXhr.statusText);
                }
            };
            
            recommenderXhr.send();

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

function scrollLeft() {
    const container = document.querySelector('.series-container');
    container.classList.add('animated'); // Ajoutez la classe 'animated'
    container.scrollLeft -= 800;
}

function scrollRight() {
    const container = document.querySelector('.series-container');
    container.classList.add('animated'); // Ajoutez la classe 'animated'
    container.scrollLeft += 800;
}


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
                    displayResults(response['series']); 
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
            results.forEach(function (result) {
                html += '<li><a href="../serie/serie.html?id=' + result.id + '" class="lien-serie">';
                html += '<img src="../img/img_series/' + result.id + '.jpg" alt="' + result.titre + '" class="img-series">';
                html += '</a></li>';
            });
        } else {
            html += 'Aucun résultat trouvé.';
        }
    
        const ulResult = document.querySelector('.ul-result');
        ulResult.innerHTML = html;

        const scrollLeftButton = document.querySelector('.scroll-left-button');
        const scrollRightButton = document.querySelector('.scroll-right-button');

        scrollLeftButton.innerHTML = '<i class="fas fa-chevron-left"></i>';
        scrollRightButton.innerHTML = '<i class="fas fa-chevron-right"></i>';

        scrollLeftButton.classList.add('scroll-left-button');
        scrollRightButton.classList.add('scroll-right-button')

        scrollLeftButton.addEventListener('click', scrollLeft);
        scrollRightButton.addEventListener('click', scrollRight);
    }
    
    
    
    function getSeriesData(page) {
        const xhr = new XMLHttpRequest();
        const url = '../../backend/controller.php?page=' + page; // Inclure le paramètre de pagination dans l'URL
    
        xhr.open('GET', url, true);
    
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                const response = JSON.parse(xhr.responseText);
                displayResults(response); // Afficher les résultats en utilisant la fonction displayResults()
            } else {
                console.error('Erreur :', xhr.status, xhr.statusText);
            }
        };
    
        xhr.send();
    }
    
    getSeriesData();

});
