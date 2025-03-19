document.addEventListener('click', function(event) {
    // Vérifie si l'élément cliqué est en dehors de l'un des menus déroulants
    const isClickInsideMenu = event.target.closest('.dropdown') || event.target.closest('.menu-toggle');

    if (!isClickInsideMenu) {
        // Si on a cliqué à l'extérieur, décocher toutes les cases
        const checkboxes = document.querySelectorAll('.menu-toggle');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false; // Décocher le checkbox
        });
    }
});
