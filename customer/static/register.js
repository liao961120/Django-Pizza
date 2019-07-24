document.addEventListener('DOMContentLoaded', () => {
    var pssd = document.querySelector('#pssd');
    var pssd_confirm = document.querySelector('#pssd_confirm');
    var username = document.querySelector('#username')

    username.onchange = validatePassword;
    pssd.onchange = validatePassword;
    pssd.onkeyup = validatePassword;
    pssd_confirm.onkeyup = validatePassword;
});

function validatePassword() {
    pssd_confirm.setCustomValidity('');
    pssd.setCustomValidity('');

    if (pssd.value != pssd_confirm.value) 
        pssd_confirm.setCustomValidity("Password don't match.");
    if (pssd.value == username.value) 
        pssd.setCustomValidity("Password same as username.");
};