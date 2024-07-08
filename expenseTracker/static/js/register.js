const usernameField = document.querySelector('#usernameField')
const feedbackField = document.querySelector('.invalid-feedback')
const emailField = document.querySelector('#emailField');
const emailfeedbackField = document.querySelector('.emailfeedbackField');
const usernameSuccessOuput = document.querySelector('.usernameSuccessOutput');
const submitDisable = document.querySelector('.submit-btn')


usernameField.addEventListener("keyup", (e) =>{
    const usernameVal = e.target.value;
    usernameSuccessOuput.style.display = "block";
    usernameSuccessOuput.textContent = `Checking ${usernameVal}!!!`;
    usernameField.classList.remove("is-invalid");
    feedbackField.style.display = "none";
    if( usernameVal.length > 0){
        fetch("/validate-username",{
            body: JSON.stringify({username:usernameVal}),
            method:"POST",
        }).then(res=>res.json()).then(data=>{
            console.log("data", data);
            usernameSuccessOuput.style.display = "none";
            if(data.username_error){
                submitDisable.setAttribute('disabled','disabled');
                submitDisable.disabled  = true;
                usernameField.classList.add("is-invalid");
                feedbackField.style.display = "block";
                feedbackField.innerHTML = `<p>${data.username_error}</p>`;
            }
            else{
                submitDisable.removeAttribute('disabled');
            }
        });
    }

        
});

emailField.addEventListener("keyup", (e) =>{
    const emailVal = e.target.value;
    emailField.classList.remove("is-invalid");
    emailfeedbackField.style.display = "none";
    if( emailVal.length > 0){
        fetch("/validate-email",{
            body: JSON.stringify({email:emailVal}),
            method:"POST",
        }).then(res=>res.json()).then(data=>{
            console.log("data", data);
            if(data.email_error){
                submitDisable.setAttribute('disabled','disabled');
                submitDisable.disabled  = true;
                emailField.classList.add("is-invalid");
                emailfeedbackField.style.display = "block";
                emailfeedbackField.innerHTML = `<p>${data.email_error}</p>`;
            }
            else{
                submitDisable.removeAttribute('disabled');
            }
        });
    }
        
});

