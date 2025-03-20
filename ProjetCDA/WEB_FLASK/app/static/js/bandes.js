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

document.addEventListener("DOMContentLoaded", function () {
    // Sélectionne tous les boutons qui ouvrent une fenêtre de commentaire
    let boutonsOuvrir = document.querySelectorAll(".ouvrir-fenetre-commentaire"); 

    // Ajoute un écouteur d'événements sur chaque bouton "Commenter"
    boutonsOuvrir.forEach(bouton => {
        bouton.addEventListener("click", function (event) {
            event.preventDefault(); // Empêche le comportement par défaut du lien
            
            // Récupère l'ID de l'auteur (passé dans l'attribut data-id)
            let authorId = bouton.getAttribute('data-id'); 

            // Sélectionne la fenêtre modale spécifique à cet auteur
            let fenetre = document.getElementById("fenetre-commentaire-" + authorId); 

            // Affiche la fenêtre modale en ajoutant la classe "fenetre-active"
            fenetre.classList.add("fenetre-active"); 
        });
    });

    // Ajoute un écouteur sur les boutons de fermeture (en utilisant une classe)
    document.querySelectorAll(".fermer").forEach(boutonFermer => {
        boutonFermer.addEventListener("click", function () {
            // Trouve la fenêtre modale parente et enlève la classe "fenetre-active"
            let fenetre = boutonFermer.closest(".fenetre-modale");
            fenetre.classList.remove("fenetre-active");
        });
    });

    // Ajoute un écouteur sur la fenêtre entière pour détecter les clics en dehors de la boîte de dialogue
    window.addEventListener("click", function (event) {
        // Si l'utilisateur clique sur l'arrière-plan sombre de la fenêtre modale
        document.querySelectorAll(".fenetre-modale").forEach(fenetre => {
            if (event.target === fenetre) {
                // Ferme la fenêtre modale en retirant la classe "fenetre-active"
                fenetre.classList.remove("fenetre-active");
            }
        });
    });
});

//-------------------------------------AJOUT UTILISATEUR------------------------
document.addEventListener("DOMContentLoaded", function () {
    // Sélectionner les éléments
    const ajouterBtn = document.getElementById("ajouter-btn");
    const fenetreAjouterUtilisateur = document.getElementById("fenetre-ajouter-utilisateur");

    // Vérifier si les éléments existent
    if (!ajouterBtn || !fenetreAjouterUtilisateur) {
        console.error("Les éléments n'ont pas été trouvés.");
        return;
    }

    // Ajouter un écouteur pour afficher la fenêtre modale
    ajouterBtn.addEventListener("click", function (event) {
        event.preventDefault();
        fenetreAjouterUtilisateur.classList.add("fenetre-activeUtilisateur");
    });

    // Ajouter un écouteur pour fermer la fenêtre si on clique en dehors
    window.addEventListener("click", function (event) {
        // Vérifie si le clic se produit en dehors de la fenêtre modale
        if (!fenetreAjouterUtilisateur.contains(event.target) && event.target !== ajouterBtn) {
            fenetreAjouterUtilisateur.classList.remove("fenetre-activeUtilisateur");
        }
    });
});

