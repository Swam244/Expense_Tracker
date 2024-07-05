const usernameField = document.getElementById('usernameField');
const passwordField = document.getElementById('passwordField');
const submitBtn = document.querySelector('.submit-btn');

function toggleSubmitButton() {
    if(usernameField.value.trim() !== "" && passwordField.value.trim() !== "") {
        submitBtn.disabled = false;
    } 
    else{
        submitBtn.disabled = true;
    }
}

usernameField.addEventListener('input', toggleSubmitButton);
passwordField.addEventListener('input', toggleSubmitButton);

toggleSubmitButton();
