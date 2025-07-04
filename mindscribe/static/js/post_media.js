document.addEventListener('DOMContentLoaded', function() {
    // Автовоспроизведение видео при наведении в списке
    const videoContainers = document.querySelectorAll('.video-container');
    
    videoContainers.forEach(container => {
        const video = container.querySelector('video');
        
        container.addEventListener('mouseenter', () => {
            video.play();
        });
        
        // container.addEventListener('mouseleave', () => {
        //     video.pause();
        //     video.currentTime = 0;
        // });
        
        // При клике открываем страницу поста
        container.addEventListener('click', () => {
            const postLink = container.closest('.post').querySelector('h2 a');
            if (postLink) {
                window.location.href = postLink.href;
            }
        });
    });
});