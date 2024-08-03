document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('like-button').addEventListener('click', function() {
        var button = this;
        var postId = button.getAttribute('data-post-id');

        fetch(`/post/${postId}/like/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response:', data);
            if (data.liked) {
                button.textContent = 'Unlike';
            } else {
                button.textContent = 'Like';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});