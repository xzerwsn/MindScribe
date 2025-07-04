// comments.js
document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.edit-comment-btn');
    const saveButton = document.getElementById('save-comment-btn');
    let currentCommentId = null;

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            currentCommentId = this.dataset.commentId;
            const commentText = document.getElementById(`comment-text-${currentCommentId}`).textContent;
            document.getElementById('edit-comment-text').value = commentText.trim();
            
            // Инициализация модального окна через Bootstrap
            const modal = new bootstrap.Modal(document.getElementById('editCommentModal'));
            modal.show();
        });
    });

    saveButton.addEventListener('click', function() {
        const newText = document.getElementById('edit-comment-text').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/comment/${currentCommentId}/edit/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({text: newText})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById(`comment-text-${currentCommentId}`).textContent = data.text;
                document.querySelector(`#comment-${currentCommentId} .comment-date`).textContent = 
                    data.updated_date + ' (ред.)';
                
                const modal = bootstrap.Modal.getInstance(document.getElementById('editCommentModal'));
                modal.hide();
            }
        });
    });
});