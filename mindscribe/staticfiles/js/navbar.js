document.addEventListener('DOMContentLoaded', () => {
    const navbarToggle = document.getElementById('navbarToggle');
    const navbarMenu = document.getElementById('navbarMenu');
    
    navbarToggle.addEventListener('click', () => {
        document.body.classList.toggle('active');
    });
    
    // Закрытие меню при клике вне области
    document.addEventListener('click', (e) => {
        if (!navbarMenu.contains(e.target) && !navbarToggle.contains(e.target)) {
            document.body.classList.remove('active');
        }
    });
});