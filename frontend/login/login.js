document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const message = document.getElementById('message');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const inscriptionLink = document.getElementById('inscriptionLink');
    const connectButton = document.getElementById('connectButton');

    let isLoginFormVisible = true; // Indique si le formulaire de connexion est actuellement affiché

    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const username = usernameInput.value;
        const password = passwordInput.value;
        const isLogin = isLoginFormVisible ? 1 : 0; // 1 pour connexion, 0 pour inscription

        // Créez un objet FormData pour les données à envoyer
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('isLogin', isLogin);

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '../../backend/auth.php', true);

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                // Réponse réussie
                const response = JSON.parse(xhr.responseText);
                if (response.success) {
                    if (!isLoginFormVisible) {
                        // Si c'était une inscription réussie, basculez vers le formulaire de connexion
                        isLoginFormVisible = true;
                        loginForm.reset(); // Effacez les champs
                        inscriptionLink.style.display = 'inline'; // Réaffiche le lien d'inscription
                        connectButton.textContent = 'S\'inscrire'; // Changez le texte du bouton en "S'inscrire"
                        window.location.href = 'login.html';
                    } else {
                        // Connexion réussie, redirigez vers la page d'accueil
                        window.location.href = '../home/home.html';
                    }
                } else {
                    // Affichez un message d'erreur (vous pouvez personnaliser cela côté serveur)
                    message.textContent = response.message;
                }
            } else {
                // Gestion des erreurs ici
                console.error('Erreur :', xhr.status, xhr.statusText);
            }
        };

        xhr.send(formData);
    });

    // Gestion du basculement entre formulaire de connexion et d'inscription
    inscriptionLink.addEventListener('click', function (e) {
        e.preventDefault();
        if (isLoginFormVisible) {
            // Si le formulaire de connexion est visible, basculez vers le formulaire d'inscription
            document.querySelector('.login-title').textContent = 'Inscrivez-vous';
            isLoginFormVisible = false;
            inscriptionLink.textContent = 'Se connecter'; // Changez le texte du lien en "Se connecter"
            passwordInput.value = ''; // Effacez le champ de mot de passe
            connectButton.textContent = 'S\'inscrire'; // Changez le texte du bouton en "S'inscrire"
        } else {
            // Si le formulaire d'inscription est visible, basculez vers le formulaire de connexion
            document.querySelector('.login-title').textContent = 'Connectez-vous';
            isLoginFormVisible = true;
            inscriptionLink.textContent = 'Inscription'; // Réinitialisez le texte du lien en "Inscription"
            usernameInput.value = ''; // Effacez le champ de nom d'utilisateur
            passwordInput.value = ''; // Effacez le champ de mot de passe
            connectButton.textContent = 'Se connecter'; // Changez le texte du bouton en "Se connecter"
        }
    });
});
