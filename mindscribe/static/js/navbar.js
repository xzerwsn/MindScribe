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

document.addEventListener('DOMContentLoaded', function() {
    // Автовоспроизведение видео при наведении в списке
    // const videoContainers = document.querySelectorAll('.video-container');
    
    videoContainers.forEach(container => {
        const video = container.querySelector('video');
        
        container.addEventListener('mouseenter', () => {
            video.play();
        });
        
        container.addEventListener('mouseleave', () => {
            video.pause();
            video.currentTime = 0;
        });
        
        // При клике открываем страницу поста
        container.addEventListener('click', () => {
            const postLink = container.closest('.post').querySelector('h2 a');
            if (postLink) {
                window.location.href = postLink.href;
            }
        });
    });
});

