document.getElementById("changePasswordForm").onsubmit = function () {
    if (document.getElementById("new_password").value !== document.getElementById("confirm_password").value) {
        alert("New passwords do not match!");
        return false;
    }
};
