document.addEventListener('DOMContentLoaded', function() {
    const saveCommentBtn = document.getElementById('save-comment-btn');
    
    saveCommentBtn.addEventListener('click', function() {
        const commentId = this.dataset.commentId;
        const newText = document.getElementById('edit-comment-text').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(`/comment/${commentId}/edit/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `text=${encodeURIComponent(newText)}&csrfmiddlewaretoken=${csrfToken}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                document.getElementById(`comment-text-${commentId}`).textContent = data.text;
                bootstrap.Modal.getInstance(document.getElementById('editCommentModal')).hide();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ошибка при сохранении комментария');
        });
    });
});