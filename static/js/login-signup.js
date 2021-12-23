const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const pass = document.getElementById('password');
const confPass = document.getElementById('confirm-password');
const signUp = document.getElementById('signup-btn');
const signupName = document.getElementById('signup-name');
const signupEmail = document.getElementById('email');
const phone = document.getElementById('phone');
const address = document.getElementById('address');

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});

signUp.addEventListener('click', () => {
    const passValue = pass.value;
    const confPassValue = confPass.value;
    if (passValue != confPassValue) {
        pass.value = '';
        confPass.value = '';
    }
    else {
        signupName.value = '';
        signupEmail.value = '';
        pass.value = '';
        confPass.value = '';
        phone.value = '';
        address.value = '';
    }
})
