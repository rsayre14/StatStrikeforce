// display the login/sign up div
function display_login()  {
    var loginForm = document.getElementById('loginOrSignup');
    loginForm.style.display = 'block';
}

// hide the login/sign up div
function hide_login()  {
    var loginForm = document.getElementById('loginOrSignup');
    loginForm.style.display = 'none';
}

// Login form submission handler
function login()   {

    var formData = new FormData(document.getElementById('loginForm'))

    $.ajax({
        type: 'POST',
        url: '/login',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            if (response.success === true) {
                alert(response.message); // Display success message

                // hide login-signup dive then redirect if wanted
                hide_login();

            } else {
                alert(response.message); // Display failure message

                // display error message from app.py, clear form, etc if wanted
            }
        },

        // Error code is triggered when 401 status is returned, return 401 when database.py or app.py doesn't execute
        error: function(error) {
            alert('Error running database.py or app.py code');
        }

    });

}

// Signup form submission handler
function signup()   {

    var formData = new FormData(document.getElementById('signupForm'))

    $.ajax({
        type: 'POST',
        url: '/signup',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            if (response.success === true) {
                alert(response.message); // Display success message

                // hide login-signup dive then redirect if wanted
                hide_login();

            } else {
                alert(response.message); // Display failure message

                // display error message from app.py, clear form, etc if wanted
            }
        },

        // Error code is triggered when 401 status is returned, return 401 when database.py or app.py doesn't execute
        error: function(error) {
            alert('Error running database.py or app.py code');
        }
    });
}

function show_tracker()   {
    var tracker = document.getElementById('TrackerSearchContent');
    tracker.style.display = 'block';
}


function track()   {

    var userinput = $('#search-bar').val();
        $.ajax({
            type: 'GET',
            url: '/tracker',
            data: { userinput: userinput },
            success: function(response) {
                // Update the HTML content of the #search-results div
                $('#search-results').html(response);
                // Display the #search-results div
                $('#search-results').show();
            },
            // consider something to remove display of #search-results
            error: function(error) {
                console.log('Error generating HTML:', error);
            }
        });
}

document.addEventListener('DOMContentLoaded', function() {
    // Wait for DOM content to be fully loaded
    var loginButton = document.getElementById('loginButton');
    var loginSubmit = document.getElementById('loginSubmit');
    var signupSubmit = document.getElementById('signupSubmit');
    var trackButton = document.getElementById('trackButton');
    var trackHereButton = document.getElementById('trackHereButton');

    // Add event listener to the Login button
    loginButton.addEventListener('click', function() {
        // This code will run when the Login button is clicked
        // Call your login function or perform login-related actions here
        display_login();
    });

    loginSubmit.addEventListener('click', function() {
        login();
    });

    signupSubmit.addEventListener('click', function() {
        signup();
    });

    trackButton.addEventListener('click', function() {
        show_tracker();
    });

    trackHereButton.addEventListener('click', function() {
        track();
    });


});
