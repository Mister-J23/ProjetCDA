//------------------------------------------------------------------------------------------PAGE OEUVRES-----------------------------------------------------------------
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
    let boutonsOuvrir = document.querySelectorAll(".ouvrir-fenetre-commentaire");

    boutonsOuvrir.forEach(bouton => {
        bouton.addEventListener("click", function (event) {
            event.preventDefault(); // Empêche le rechargement de la page
            
            let authorId = bouton.getAttribute("data-id"); // Récupère l'ID de l'auteur
            let fenetre = document.getElementById("fenetre-commentaire-" + authorId); // Sélectionne la fenêtre modale

            if (!fenetre) {
                console.error("Fenêtre modale introuvable pour l'auteur ID:", authorId);
                return;
            }

            // Affiche la fenêtre modale
            fenetre.classList.add("fenetre-active");

            let commentContainer = fenetre.querySelector(".commentaires-liste");

            if (!commentContainer) {
                console.error("Conteneur des commentaires introuvable !");
                return;
            }

            // Envoie une requête AJAX pour charger les commentaires
            fetch(`/envoyer_commentaires_bio/${authorId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error("Erreur :", data.error);
                        return;
                    }

                    console.log("Commentaires reçus :", data.commentaires);

                    // Efface les anciens commentaires
                    commentContainer.innerHTML = "";

                    // Ajoute les nouveaux commentaires reçus
                    data.commentaires.forEach(commentaire => {
                        let commentHTML = `
                            <div class="commentaire-item" data-id="${commentaire.id_comment}">
                                <span class="commentaire-text">${commentaire.comment}</span>
                                <span class="commentaire-date">${commentaire.date_comment}</span>
                                <span class="commentaire-user">${commentaire.id_user}</span>
                                <img class="delete-comment" src="/static/photo/croix.png" alt="Supprimer" title="Supprimer">
                            </div>`;
                        commentContainer.innerHTML += commentHTML;
                    });

                    // AJOUT DE L'ÉCOUTEUR APRÈS LE CHARGEMENT
                    ajouterEcouteurSuppression(commentContainer);
                })
                .catch(error => console.error("Erreur lors du chargement des commentaires :", error));
        });
    });

    // Fonction pour ajouter l'écouteur d'événement uniquement après le chargement des commentaires
    function ajouterEcouteurSuppression(commentContainer) {
        commentContainer.addEventListener('click', function (event) {
            if (event.target && event.target.classList.contains('delete-comment')) {
                let commentElement = event.target.closest('.commentaire-item');
                let commentId = commentElement.getAttribute('data-id');
                let userId = currentUserId;  

                let requestBody = JSON.stringify({ id_user: currentUserId });

                console.log(`Requête DELETE envoyée avec l'ID du commentaire: ${commentId} et l'ID utilisateur: ${userId}`);

                fetch(`/supprimer_commentaire/${commentId}/${userId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: requestBody
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message.includes("✅")) {
                        commentElement.remove();  
                    } else {
                        alert("Erreur : " + data.message);
                    }
                })
                .catch(error => console.error("Erreur lors de la suppression :", error));
            }
        });
    }

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

//------------------------------------------ECOUTEUR POUR LE CLICK SUR L'IMAGE-------------------------------
document.addEventListener("DOMContentLoaded", function () { 
    // Sélectionne toutes les images des auteurs
    const imagesAuteurs = document.querySelectorAll(".effigie");

    imagesAuteurs.forEach(image => {
        image.addEventListener("click", function (event) {
            event.preventDefault();  // Empêche toute action par défaut

            let authorId = this.getAttribute("data-id"); // Récupère l'ID de l'auteur
            console.log("Clic détecté sur l'image de l'auteur ID :", authorId); // Debugging

            fetch(`/bio/${authorId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        afficherMessageErreur(data.error);
                    } else {
                        window.open(data.link, "_blank"); // Ouvre le PDF dans un nouvel onglet
                    }
                })
                .catch(error => console.error("Erreur lors de la récupération du lien :", error));
        });
    });
});

function afficherMessageErreur(message) {
    let modal = document.createElement("div");
    modal.classList.add("modal-overlay"); // Ajout d'une classe pour le style

    modal.innerHTML = `
        <div class="modal-erreur">
            <p class="black">${message}</p>
        </div>
    `;

    // Fermer la modal si on clique en dehors du message
    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.remove();
        }
    });

    document.body.appendChild(modal);
}


