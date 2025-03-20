// Ajoute un écouteur d'événements pour détecter les clics sur toute la page
document.addEventListener('click', function(event) {
    // Vérifie si l'élément cliqué est à l'intérieur d'un menu déroulant ou d'un bouton checkbox du menu
    const isClickInsideMenu = event.target.closest('.dropdown') || event.target.closest('.menu-toggle');

    // Si l'utilisateur clique en dehors des menus déroulants
    if (!isClickInsideMenu) {
        // Sélectionne toutes les cases à cocher utilisées pour afficher les menus déroulants
        const checkboxes = document.querySelectorAll('.menu-toggle');

        // Parcourt toutes les checkboxes et les décoche
        checkboxes.forEach(checkbox => {
            checkbox.checked = false; // Décoche le menu déroulant
        });
    }
});

// Attend que la page soit entièrement chargée avant d'exécuter le script
document.addEventListener("DOMContentLoaded", function () {
    // Sélectionne l'élément de la fenêtre de commentaire
    let fenetre = document.getElementById("fenetre-commentaire"); 

    // Sélectionne le bouton de fermeture de la fenêtre
    let boutonFermer = document.querySelector(".fermer"); 

    // Sélectionne tous les boutons qui ouvrent la fenêtre de commentaire
    let boutonsOuvrir = document.querySelectorAll(".ouvrir-fenetre-commentaire"); 

    // Ajoute un écouteur d'événements sur chaque bouton "Commenter"
    boutonsOuvrir.forEach(bouton => {
        bouton.addEventListener("click", function (event) {
            event.preventDefault(); // Empêche le comportement par défaut du lien
            fenetre.classList.add("fenetre-active"); // Ajoute la classe pour afficher la fenêtre
        });
    });

    // Ajoute un écouteur sur le bouton de fermeture
    boutonFermer.addEventListener("click", function () {
        fenetre.classList.remove("fenetre-active"); // Supprime la classe pour cacher la fenêtre
    });

    // Ajoute un écouteur sur la fenêtre entière pour détecter les clics en dehors de la boîte de dialogue
    window.addEventListener("click", function (event) {
        // Si l'utilisateur clique sur l'arrière-plan sombre de la fenêtre modale
        if (event.target === fenetre) {
            fenetre.classList.remove("fenetre-active"); // Ferme la fenêtre modale
        }
    });
});

