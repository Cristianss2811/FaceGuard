
document.addEventListener("DOMContentLoaded", function() {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.sidebar-link');

    function setActiveLink(activePage) {
        links.forEach(link => {
            if (link.getAttribute('href') === activePage || 
                (link.getAttribute('href').startsWith('#') && activePage.includes(link.getAttribute('data-page')))) {
                link.classList.add('active');
                localStorage.setItem('activePage', activePage);
            } else {
                link.classList.remove('active');
            }
        });
    }

    // Verificar si hay un estado activo guardado
    const savedActivePage = localStorage.getItem('activePage');
    if (savedActivePage) {
        setActiveLink(savedActivePage);
    } else {
        // Si no hay estado guardado, establecer Dashboard como activo por defecto
        setActiveLink('/'); // Cambia esto si el href de Dashboard es diferente
    }

    links.forEach(link => {
        link.addEventListener('click', function() {
            setActiveLink(link.getAttribute('href'));
        });
    });
});

function logout() {
    localStorage.removeItem('activePage');
}


