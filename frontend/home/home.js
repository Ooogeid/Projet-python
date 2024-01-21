
// Vérifier si une session est active
const xhr = new XMLHttpRequest();
xhr.open('GET', '../../backend/check_session.php', true);

xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
        const response = JSON.parse(xhr.responseText);
        if (response.success && response.username) {
            // Une session est active, l'utilisateur est connecté
            document.getElementById('usernameDisplay').textContent = response.username;
            localStorage.setItem('username', response.username);
            const recommenderXhr = new XMLHttpRequest();
            recommenderXhr.open('GET', '../../backend/controller.php?recommandation=true', true);
            
            recommenderXhr.onload = function () {
                if (recommenderXhr.status >= 200 && recommenderXhr.status < 300) {
                    const recommandations = JSON.parse(recommenderXhr.responseText);
                    if (recommandations.recommandation.length === 0) {
                        noResultR = document.getElementById('noResultR');
                        noResultR.textContent = 'Commencez à ajouter une série en liste pour être recommandé';
                        displayRecommandations(recommandations);
                    } else {
                        displayRecommandations(recommandations);
                    }
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
    const resultContainer = document.querySelector('#result .series-container');
    resultContainer.classList.add('animated');
    resultContainer.scrollLeft -= 800;
}

function scrollRight() {
    const resultContainer = document.querySelector('#result .series-container');
    resultContainer.classList.add('animated');
    resultContainer.scrollLeft += 800;
}

function scrollLeftRecommandations() {
    const recommandationsContainer = document.querySelector('#recommandations .series-container');
    recommandationsContainer.classList.add('animated');
    recommandationsContainer.scrollLeft -= 800;
}

function scrollRightRecommandations() {
    const recommandationsContainer = document.querySelector('#recommandations .series-container');
    recommandationsContainer.classList.add('animated');
    recommandationsContainer.scrollLeft += 800;
}

document.onreadystatechange = function () {
    const spinner = document.getElementById('loading-spinner');
    if (document.readyState === 'loading') {
        // Le DOM n'est pas encore entièrement chargé, afficher le spinner
        spinner.style.display = 'block';
    } else if (document.readyState === 'interactive') {
        // Le DOM est partiellement chargé, masquer le spinner
        spinner.style.display = 'none';
    }
};

document.addEventListener('DOMContentLoaded', function() {
    const inputElement = document.getElementById('credentials');
    const languageToggle = document.getElementById('languageToggle');
    var selectedLanguage = localStorage.getItem('selectedLanguage');
  
    // Restaurer la langue sélectionnée
    if (selectedLanguage === 'en') {
        languageToggle.checked = true;
    } else {
        languageToggle.checked = false;
    }
  
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

    // Réinitialiser la langue à "français" lors du retour sur la page d'accueil
    window.addEventListener('pageshow', function(event) {
        if (localStorage.getItem('selectedLanguage') !== 'fr') {
            saveLanguageSelection('fr'); // Réinitialiser la langue à "français"
            languageToggle.checked = false; // Décocher le bouton de bascule
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

    let resultDiv = document.getElementById('result'); // Déclaration de resultDiv en dehors de la fonction

    function performSearch(event) {
        event.preventDefault();
        const keyword = inputElement.value;

        // Annulez la requête précédente si elle est en cours
        if (xhr && xhr.readyState !== 4) {
            xhr.abort();
        }
        console.log(keyword);
        if (keyword) {
            // Affichez le spinner pendant le chargement
            const spinner = document.querySelector('.loading-spinner');
            spinner.style.display = 'block';

            xhr = new XMLHttpRequest();
            xhr.open('POST', '../../backend/controller.php', true);
            xhr.setRequestHeader('Content-Type', 'application/json');

            xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                displayResults(response['series'], true);
                // Masquez le spinner et réactivez le bouton de recherche
                spinner.style.display = 'none';
            }
            };

            const selectedLanguage = localStorage.getItem('selectedLanguage');

            const credentials = {
            keyword: keyword,
            language: selectedLanguage,
            };
            xhr.send(JSON.stringify(credentials)); // Envoyez l'objet JSON

            resultDiv.style.display = 'block'; // Afficher resultDiv
            const noKeyword = document.getElementById('noKeyword');
            noKeyword.style.display = 'none'; // Masquer noKeyword
        } else {
            resultDiv.style.display = 'none'; // Masquer resultDiv
            const noKeyword = document.getElementById('noKeyword');
            noKeyword.style.display = 'block'; // Afficher noKeyword
        }
    }

    function displayResults(results, isSearch) {
        const ulResult = resultDiv.querySelector('.ul-result');
        let html = '';
        const noResult = document.getElementById('noResult');

        noResult.textContent = ''; // Effacer le contenu du paragraphe
        noResult.style.display = 'none'; // Masquer le message

        if (results.length > 0) {
            results.forEach(function (result) {
            html += '<li><a href="../serie/serie.html?id=' + result.id + '" class="lien-serie">';
            html += '<img src="../img/img_series/' + result.id + '.jpg" alt="' + result.titre + '" class="img-series">';
            html += '<p style="margin-top: 20px;">' + result.titre + '</p>';
            html += '</a></li>';
            });
            noResult.style.display = 'none';
        } else {
            noResult.textContent = 'Aucun résultat trouvé.'; // Modifier le texte du paragraphe
            noResult.style.display = 'flex';
            noResult.style.justifyContent = 'center';
        }

        if (isSearch) {
            resultDiv.classList.remove('container'); // Supprimer la classe 'container'
            resultDiv.classList.add('series-container'); // Ajouter la classe 'series-container'
            resultDiv.querySelector('p').style.display = 'none';
        }

        ulResult.innerHTML = html;

        const scrollLeftButton = resultDiv.querySelector('.scroll-left-button-results');
        const scrollRightButton = resultDiv.querySelector('.scroll-right-button-results');

        scrollLeftButton.innerHTML = '<i class="fas fa-chevron-left"></i>';
        scrollRightButton.innerHTML = '<i class="fas fa-chevron-right"></i>';

        scrollLeftButton.classList.add('scroll-left-button');
        scrollRightButton.classList.add('scroll-right-button');

        scrollLeftButton.addEventListener('click', scrollLeft);
        scrollRightButton.addEventListener('click', scrollRight);
    }
    
    function getSeriesData() {
        const xhr = new XMLHttpRequest();
        const url = '../../backend/controller.php?'; 
    
        xhr.open('GET', url, true);
    
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                const response = JSON.parse(xhr.responseText);
                displayResults(response, false); // Afficher les résultats en utilisant la fonction displayResults()
            } else {
                console.error('Erreur :', xhr.status, xhr.statusText);
            }
        };
    
        xhr.send();
    }

    
    getSeriesData();


});

function displayRecommandations(recommandations) {
    const recommandationsDiv = document.getElementById('recommandations');
    const ulResult = recommandationsDiv.querySelector('.ul-result');

    let recommandationsHTML = '';
    const recommandationsArray = Object.values(recommandations);
    recommandationsArray.forEach(function(recommandationArray) {
        recommandationArray.forEach(function(recommandation) {
            recommandationsHTML += '<li><a href="../serie/serie.html?id=' + recommandation.id + '" class="lien-serie">';
            recommandationsHTML += '<img src="../img/img_series/' + recommandation.id + '.jpg" alt="' + recommandation.titre + '" class="img-series">';
            recommandationsHTML += '<p style="margin-top: 20px;">' + recommandation.titre + '</p>';
            recommandationsHTML += '</a></li>';
        });
    });

    ulResult.innerHTML = recommandationsHTML;

    const scrollLeftButton = recommandationsDiv.querySelector('.scroll-left-button-recommandations');
    const scrollRightButton = recommandationsDiv.querySelector('.scroll-right-button-recommandations');

    scrollLeftButton.innerHTML = '<i class="fas fa-chevron-left"></i>';
    scrollRightButton.innerHTML = '<i class="fas fa-chevron-right"></i>';

    scrollLeftButton.classList.add('scroll-left-button');
    scrollRightButton.classList.add('scroll-right-button');

    scrollLeftButton.addEventListener('click', scrollLeftRecommandations);
    scrollRightButton.addEventListener('click', scrollRightRecommandations);

    if(recommandations.recommandation.length === 0){
        scrollLeftButton.style.display = 'none';
        scrollRightButton.style.display = 'none';
    }
}