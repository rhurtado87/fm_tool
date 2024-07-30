document.addEventListener('DOMContentLoaded', function() {
    const likeForms = document.querySelectorAll('.like-form');

    likeForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent default form submission

            const button = this.querySelector('button');
            const icon = button.querySelector('i');
            
            fetch(this.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
                body: new URLSearchParams(new FormData(this)),
            })
            .then(response => response.json())
            .then(data => {
                // Toggle icon and button text
                if (data.liked) {
                    icon.classList.add('liked');
                    button.textContent = ' Unlike';
                } else {
                    icon.classList.remove('liked');
                    button.textContent = ' Like';
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
