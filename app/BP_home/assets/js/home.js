/**
 * Dismisses the offer block
 */
function dismissOffer() {
    let offer = document.querySelector('#offers');
    offer.classList.replace('show', 'fade');
    setTimeout(function () {
        offer.remove();
    }, 1000);
}

/**
 * page load events.
 */
$(document).ready(() => {
    if (location.href.includes('services#')) {
        const section = location.href.substr(location.href.indexOf('#'));
        const collapseBtn = document.querySelector(section).parentElement.querySelector('a');
        scrollCollapseToView(collapseBtn);
    }
});

function scrollCollapseToView(btn) {
    const btnID = btn.getAttribute("id");
    const collapseID = '#' + btnID.substr(btnID.indexOf("-") + 1);
    const collapseParent = document.querySelector(collapseID + 'Parent');
    $(collapseID).collapse('toggle');
    setTimeout(() => {
        collapseParent.scrollIntoView();
        btnIcon = btn.querySelector('i');
        btnText = btn.querySelector('span');
        if (btnText.textContent === 'EXPLORE') {
            btnIcon.classList.replace('fa-chevron-down', 'fa-chevron-up');
            btnText.textContent = 'CLOSE';
        } else {
            btnIcon.classList.replace('fa-chevron-up', 'fa-chevron-down');
            btnText.textContent = 'EXPLORE';
        }
    }, 350);
}

function validatePassword() {
    let newPassword = document.querySelector('#new_password');
    let cnfPassword = document.querySelector('#confirm_new_password')
    let confirmationError = cnfPassword.parentElement.querySelector('#conf_pwd_error')
    if (newPassword.value !== cnfPassword.value) {
        cnfPassword.classList.add("is-invalid");
        confirmationError.textContent = "Passwords Don't Match";
    } else {
        cnfPassword.classList.remove("is-invalid");
        confirmationError.textContent = "";
    }
}