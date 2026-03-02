document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navUl = document.querySelector('nav ul');

    if (menuToggle && navUl) {
        menuToggle.addEventListener('click', () => {
            navUl.classList.toggle('active');
            
            // Layout accessibility: toggle aria-expanded
            const isExpanded = navUl.classList.contains('active');
            menuToggle.setAttribute('aria-expanded', isExpanded);
        });
    }

    // Console log for debugging
    console.log('Zunda Quake website scripts loaded.');
});

function toggleMenu() {
    const menu = document.getElementById("menu");
    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
}

document.addEventListener("click", function(event) {
    const menu = document.getElementById("menu");
    const button = document.querySelector(".menu-button");
    if (event.target !== menu && event.target !== button && !menu.contains(event.target)) {
        menu.style.display = "none";
    }
});