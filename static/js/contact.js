  // Function to initialize EmailJS
  function initEmailJS() {
    const serviceId = 'YOUR_EMAILJS_SERVICE_ID'; // Replace with your EmailJS service ID
    const templateId = 'YOUR_EMAILJS_TEMPLATE_ID'; // Replace with your EmailJS template ID

    emailjs.init(serviceId);
    
    // Handle form submission
    document.getElementById("contactForm").addEventListener("submit", function(event) {
        event.preventDefault();

        const form = event.target;
        const name = form.elements.name.value;
        const email = form.elements.email.value;
        const message = form.elements.message.value;

        // Prepare parameters for EmailJS
        const params = {
            name: name,
            email: email,
            message: message
        };

        // Send email using EmailJS
        emailjs.send(serviceId, templateId, params)
            .then(function(response) {
                alert('Email sent successfully!');
                form.reset(); // Clear the form after successful submission
            }, function(error) {
                console.error('Failed to send email. Error:', error);
                alert('Failed to send email. Please try again later.');
            });
    });
}

// Initialize EmailJS on window load
window.onload = function() {
    initEmailJS();
};