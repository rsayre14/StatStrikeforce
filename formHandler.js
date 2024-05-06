document.addEventListener('DOMContentLoaded', function() {
    // Login form submission handler
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch('http://127.0.0.1:3000/login', { // Make sure to use the correct URL for your login endpoint
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message); // Display message from server
                if (data.success) {
                    window.location.href = '/dashboard'; // Redirect if login is successful
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Signup form submission handler
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch('http://127.0.0.1:3000/signup', { // STILL HAVE to Make sure to use the correct URL for your signup endpoint
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message); // Display message from server
                if (data.success) {
                    window.location.href = '/login'; // Redirect if signup is successful
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
