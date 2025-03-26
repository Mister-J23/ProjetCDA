


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

