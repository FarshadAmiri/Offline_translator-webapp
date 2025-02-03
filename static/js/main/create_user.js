document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("createUserForm").addEventListener("submit", function (event) {
        let username = document.getElementById("username").value.trim();
        let email = document.getElementById("email").value.trim();
        let password = document.getElementById("password").value.trim();

        // Validate Username
        let usernameRegex = /^[a-zA-Z0-9_.-]+$/;
        if (!usernameRegex.test(username)) {
            alert("Invalid username! Only letters, numbers, dots, underscores, and hyphens are allowed.");
            event.preventDefault();
            return;
        }

        // Validate Email
        if (email.length > 0) {
            let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert("Invalid email address!");
                event.preventDefault();
                return;
            }
        }

        // Validate Password
        if (password.length < 6) {
            alert("Password must be at least 6 characters long.");
            event.preventDefault();
            return;
        }
    });
});
