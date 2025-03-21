//------------------------------------------------------------------------------------------PAGE OEUVRES-----------------------------------------------------------------
// Ajoute un écouteur d'événements pour détecter les clics sur toute la page
document.addEventListener('click', function(event) {
    // Vérifie si l'élément cliqué est à l'intérieur d'un menu déroulant ou d'un bouton checkbox du menu
    const isClickInsideMenu = event.target.closest('.dropdown') || event.target.closest('.menu-toggleoeuvre');

    // Si l'utilisateur clique en dehors des menus déroulants
    if (!isClickInsideMenu) {
        // Sélectionne toutes les cases à cocher utilisées pour afficher les menus déroulants
        const checkboxes = document.querySelectorAll('.menu-toggleoeuvre');

        // Parcourt toutes les checkboxes et les décoche
        checkboxes.forEach(checkbox => {
            checkbox.checked = false; // Décoche le menu déroulant
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    let boutonsOuvrir = document.querySelectorAll(".ouvrir-fenetre-commentaire");

    boutonsOuvrir.forEach(bouton => {
        bouton.addEventListener("click", function (event) {
            event.preventDefault(); // Empêche le rechargement de la page
            
            let authorId = bouton.getAttribute("data-id"); // Récupère l'ID de l'auteur
            let fenetre = document.getElementById("fenetre-commentaire-" + authorId); // Sélectionne la fenêtre modale

            // Vérifie si la fenêtre existe
            if (!fenetre) {
                console.error("Fenêtre modale introuvable pour l'auteur ID:", authorId);
                return;
            }

            // Affiche la fenêtre modale
            fenetre.classList.add("fenetre-active");

            // Sélectionne le conteneur où les commentaires seront affichés
            let commentContainer = fenetre.querySelector(".commentaires-liste");

            // Vérifie si le conteneur existe
            if (!commentContainer) {
                console.error("Conteneur des commentaires introuvable !");
                return;
            }

            // Envoie une requête AJAX pour charger les commentaires
            fetch(`/envoyer_commentaires/${authorId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error("Erreur :", data.error);
                        return;
                    }

                    console.log("Commentaires reçus :", data.commentaires); // Affiche les commentaires reçus

                    // Efface les anciens commentaires
                    commentContainer.innerHTML = "";

                    // Ajoute les nouveaux commentaires reçus
                    data.commentaires.forEach(commentaire => {
                        let commentHTML = `<div class="commentaire-item">${commentaire.comment} | ${commentaire.date_comment} | ${commentaire.id_user}</div>`;
                        commentContainer.innerHTML += commentHTML;
                    });
                })
                .catch(error => console.error("Erreur lors du chargement des commentaires :", error));
        });
    });

    // Fermer la fenêtre modale
    document.querySelectorAll(".fermer").forEach(boutonFermer => {
        boutonFermer.addEventListener("click", function () {
            let fenetre = boutonFermer.closest(".fenetre-modale");
            fenetre.classList.remove("fenetre-active");
        });
    });

    // Fermer en cliquant à l'extérieur
    window.addEventListener("click", function (event) {
        document.querySelectorAll(".fenetre-modale").forEach(fenetre => {
            if (event.target === fenetre) {
                fenetre.classList.remove("fenetre-active");
            }
        });
    });
});
