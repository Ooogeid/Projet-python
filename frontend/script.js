document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('searchButton');
    const inputElement = document.getElementById('credentials');
    const resultDiv = document.getElementById('result');
    const languageToggle = document.getElementById('languageToggle');

    let xhr = null;

    // Ajoutez un gestionnaire d'événements pour la soumission du formulaire
    searchButton.addEventListener('click', function(event) {
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
            xhr.open('POST', '../backend/controller.php', true);
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
            console.log(selectedLanguage);

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
