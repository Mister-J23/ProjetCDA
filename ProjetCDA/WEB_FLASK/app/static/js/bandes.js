function toggleMenu() {
    let menu = document.getElementById("menu"); // Récupère l'élément du menu déroulant par son ID
    menu.classList.toggle("visible"); // Ajoute ou retire la classe 'visible'
}

// Ferme le menu si on clique ailleurs que sur l'image ou le menu
document.addEventListener("click", function(event) {
    let menu = document.getElementById("menu"); // Récupère l'élément du menu
    let icon = document.querySelector(".icon"); // Récupère l'image qui sert de bouton

    // Vérifie si l'endroit cliqué n'est ni l'image ni le menu
    if (!icon.contains(event.target) && !menu.contains(event.target)) {
        menu.classList.remove("visible"); // Enlève la classe 'visible' pour masquer le menu
    }
});
