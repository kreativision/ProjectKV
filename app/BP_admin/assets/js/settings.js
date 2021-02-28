const EMAIL_PATTERN = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
let formScopeState;
let stateChanged = false;
let userData;

/**
 * On page load, open the form modal which has errors.
 */
$(document).ready(() => {
    formScopeState = undefined;
    if (document.querySelector("#infoModal .info-invalid")) {
        $('#infoModal').modal('show');
    } else if (document.querySelector("#pwdModal .info-invalid")) {
        $('#pwdModal').modal('show');
    }
});

/**
 * Enable form validation for password form when it is loaded.
 */
$('#pwdModal').on('shown.bs.modal', () => {
    activateFormBehaviour("#pwdModal form");
});

/**
 * Remove errors from password form on closing it.
 */
$('#pwdModal').on('hidden.bs.modal', () => {
    let fields = document.querySelectorAll('#pwdModal .is-invalid');
    fields.forEach((field) => {
        field.classList.remove("is-invalid");
    });
});

/**
 * Enable form validation for details form when it is loaded.
 */
$('#infoModal').on('shown.bs.modal', () => {
    if (!$('#password').hasClass("is-invalid")) {
        autoFillForm($('#adminMail').text());
    } else {
        formScopeState = $('#infoModal form input[type="text"]').serialize();
        stateChanged = true;
        activateFormBehaviour('#infoModal form');
    }
});

/**
 * Remove errors from details form on closing it.
 */
$('#infoModal').on('hidden.bs.modal', () => {
    let fields = document.querySelectorAll('#infoModal .is-invalid');
    fields.forEach((field) => {
        field.classList.remove("is-invalid");
    });
});

/**
 * Function to enable the floating labels bahaviour and focus the first input.
 * @param {*} form the selected form
 */
function activateFormBehaviour(form) {
    let inputs = document.querySelectorAll(`${form} input[type="text"], ${form} input[type="password"]`);
    inputs.forEach(field => {
        if (field.value)
            field.parentNode.querySelector('label').classList.add('active');
        field.onblur = () => {
            if (field.value) { field.parentNode.querySelector('label').classList.add('active'); }
            else { field.parentNode.querySelector('label').classList.remove('active'); }

        }
    });
    if (form.includes("info")) {
        let end = inputs[0].value.length;
        inputs[0].setSelectionRange(end, end);
        inputs[0].focus();
        validateInfo(form);
    } else if (form.includes("pwd")) {
        inputs[0].focus();
        validatePasswords(form);
    }
}

/**
 * Function to fetch user data from the database and pre-fill the details-form values
 * @param {*} email email ID of the user.
 */
function autoFillForm(email) {
    $.ajax({
        url: `${API_URl}/fetch-user/${email}`,
        contentType: 'application/json',
        dataType: 'json',
        success: function (user) {
            userData = user;
            for (let key in user)
                $(`#${key}`).val(user[key]);
            setTimeout(() => {
                activateFormBehaviour('#infoModal form');
            }, 100);
        }
    });
}

/**
 * Password form validation script
 * VALIDATION STRATEGY: Submit button should be disabled unless
 * Old and new password are different + new/confirm passwords match.
 * @param {*} form the password validation form
 */
function validatePasswords(form) {
    var disable = true;
    disableSubmit(form, disable);
    var currentPassword = $(`${form} #current`);
    var newPassword = $(`${form} #new_password`);
    var confirmNewPassword = $(`${form} #confirm_new_password`);
    currentPassword.val("");
    newPassword.val("");
    confirmNewPassword.val("");
    $(`${form} #current, ${form} #new_password, ${form} #confirm_new_password`).bind('keyup', () => {
        var fieldsPopulated = areFieldsPopulated();
        arePasswordsDifferent();
        passwordMatcher();
        clearErrorsOnFill();
        var errors = document.querySelectorAll(".is-invalid").length;
        if (fieldsPopulated && !errors) {
            disable = false;
        } else {
            disable = true;
        }
        disableSubmit(form, disable);
    });
    function arePasswordsDifferent() {
        let current = currentPassword.val();
        let newP = newPassword.val();
        if (current && newP && (current === newP)) {
            newPassword.addClass("is-invalid");
            newPassword.parent().find('#new_password').text("New password cannot be same as old passwword.");
        } else {
            newPassword.removeClass("is-invalid");
        }
    }
    function clearErrorsOnFill() {
        if (currentPassword.val()) {
            currentPassword.removeClass("is-invalid");
        }
    }
    function areFieldsPopulated() {
        if (!currentPassword.val() || !newPassword.val() || !confirmNewPassword.val()) {
            return false;
        } else {
            return true;
        }
    }
    function passwordMatcher() {
        if (confirmNewPassword.val() && (newPassword.val() !== confirmNewPassword.val())) {
            confirmNewPassword.addClass("is-invalid");
            confirmNewPassword.parent().find('#confirm_password').text("Passwords don't match");
        } else {
            confirmNewPassword.removeClass("is-invalid");
        }
    }
}

/**
 * Details form validation script
 * VALIDATION STRATEGY: Submit button should be disables unless
 * some detail is changed and password is entered.
 * @param {*} form the form to validate.
 */
function validateInfo(form) {
    var disable = true;
    disableSubmit(form, disable);
    var username = $(`${form} #username`);
    var email = $(`${form} #email`);
    var contact = $(`${form} #contact`);
    var password = $(`${form} #password`);
    password.val("");
    var formScope = $(`${form} input[type="text"]`);
    if (!formScopeState) { formScopeState = formScope.serialize(); }
    $(`${form} #username, ${form} #email, ${form} #contact, ${form} #password`).bind('keyup', () => {
        nameValidation();
        contactValidation();
        emailVAlidation();
        passwordValidation();
        var formStateChanged = stateChanged ? true : formScopeState !== formScope.serialize();
        var formScopeEmpty = isFormScopeEmpty(form);
        var pwdFieldHasData = $(`${form} #password`).val();
        var errors = document.querySelectorAll(".is-invalid").length;
        if (formStateChanged && !formScopeEmpty && pwdFieldHasData && !errors) {
            disable = false;
        } else {
            disable = true;
        }
        disableSubmit(form, disable);
    });

    function nameValidation() {
        var nameLength = username.val().length;
        if ((nameLength > 0 && nameLength <= 3) || nameLength > 50) {
            username.addClass("is-invalid");
            username.parent().find('#name_error').text("Name should be 3 to 50 characters.");
        } else if (nameLength === 0) {
            username.addClass("is-invalid");
            username.parent().find('#name_error').text("Name cannot be empty");
        } else {
            username.removeClass("is-invalid");
        }
    }

    function contactValidation() {
        var number = parseInt(contact.val());
        if (!number || isNaN(number)) {
            contact.addClass("is-invalid");
            contact.parent().find('#contact_error').text("Contact cannot be empty.");
        } else if (number < 1000000000 || number > 9999999999) {
            contact.addClass("is-invalid");
            contact.parent().find('#contact_error').text("Phone number should be 10 digits.");
        } else {
            contact.removeClass("is-invalid");
        }
    }

    function emailVAlidation() {
        var emailId = email.val();
        if (!emailId) {
            email.addClass("is-invalid");
            email.parent().find('#email_error').text("Email cannot be Empty.");
        } else if (!EMAIL_PATTERN.test(emailId)) {
            email.addClass("is-invalid");
            email.parent().find('#email_error').text("Invalid email address.");
        } else if ($('#adminMail').text() !== email.val()) {
            $.ajax({
                url: `${API_URl}/check-email/${email.val()}`,
                contentType: 'application/json',
                dataType: 'json',
                success: function (user) {
                    if (user.registered) {
                        email.addClass("is-invalid");
                        email.parent().find('#email_error').text("This Email id is already in the system.");
                    } else {
                        email.removeClass("is-invalid");
                    }
                }
            });
        } else {
            email.removeClass("is-invalid");
        }
    }

    function passwordValidation() {
        if (password.val()) {
            password.removeClass("is-invalid");
        }
    }

    function isFormScopeEmpty(form) {
        state = false;
        document.querySelectorAll(`${form} input[type="text"]`).forEach((field) => {
            if (!field.value) {
                state = true;
            }
        })
        return state;
    }
}

/**
 * Function to disable/enable submit button
 * @param {*} form the form whose submit button is targeted.
 * @param {*} state the state of the button to set. [true = disable; false = enable]
 */
function disableSubmit(form, state) {
    $(form).find('input[type="submit"]').prop('disabled', state);
}