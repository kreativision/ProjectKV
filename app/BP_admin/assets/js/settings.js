const EMAIL_PATTERN = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
let formScopeState;

/**
 * On page load
 */
$(document).ready(() => {
    // check if there is already a form rendered with errors.
    if (document.querySelector('.collapse.show')) {
        let errorForm = $('.collapse.show').attr("id");
        formScopeState = $('.collapse.show form input[type="text"]').serialize();
        enableLabelsBehaviour(`#${errorForm}`);
    }
});

/**
 * Function to enable the floating labels bahaviour and focus the first input.
 * @param {*} form the selected form
 */
function enableLabelsBehaviour(form) {
    let inputs = document.querySelectorAll(`${form} input[type="text"], ${form} input[type="password"]`);
    inputs.forEach(field => {
        if (field.value) {
            field.parentNode.querySelector('label').classList.add('active');
        }
        field.onblur = () => {
            if (field.value) {
                field.parentNode.querySelector('label').classList.add('active');
            } else {
                field.parentNode.querySelector('label').classList.remove('active');
            }
        }
    })
    let end = inputs[0].value.length;
    inputs[0].setSelectionRange(end, end);
    inputs[0].focus();
    // Start the corresponding form validations
    if (form.includes('detailsCollapse')) { validateInfo(form); }
}

/**
 * Function to close a particular form; called from HTML
 * @param {*} collapse the section to close
 */
function closeCollapse(collapse) {
    $(collapse).collapse('hide');
}

/**
 * Function to open a form section on the settings page.
 * @param {*} open the section to open
 * @param {*} close the section to close
 */
function triggerForm(open, close) {
    $(open).collapse('show');
    $(close).collapse('hide');
    if (open === '#detailsCollapse') {
        $('#password').removeClass("is-invalid");
        autoFillForm($('#adminEmail').text());
    } else {
        enableLabelsBehaviour(open);
    }
}

/**
 * Function to fetch user data from the database and pre-fill the form values
 * @param {*} email email ID of the user.
 */
function autoFillForm(email) {
    $.ajax({
        url: `${API_URl}/fetch-user/${email}`,
        contentType: 'application/json',
        dataType: 'json',
        success: function (user) {
            $('#username').val(user.username);
            $('#email').val(user.email);
            $('#contact').val(user.contact);
            setTimeout(() => {
                enableLabelsBehaviour('#detailsCollapse form');
            }, 100);
        }
    });
}

/**
 * Function to enable the floating labels bahaviour and focus the first input.
 * @param {*} form the selected form
 */
function enableLabelsBehaviour(form) {
    let inputs = document.querySelectorAll(`${form} input[type="text"], ${form} input[type="password"]`);
    inputs.forEach(field => {
        if (field.value) {
            field.parentNode.querySelector('label').classList.add('active');
        }
        field.onblur = () => {
            if (field.value) {
                field.parentNode.querySelector('label').classList.add('active');
            } else {
                field.parentNode.querySelector('label').classList.remove('active');
            }
        }
    })
    let end = inputs[0].value.length;
    inputs[0].setSelectionRange(end, end);
    inputs[0].focus();
    // Start the corresponding form validations
    if (form.includes('detailsCollapse')) { validateInfo(form); }
}

/**
 * Form validation function for the update account details form.
 * VALIDATION STRATEGY: 
 * Submit button should be disabled if nothing is changed/password is empty/there are explicit errors in the form.
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
    formScopeState = formScope.serialize();
    $(`${form} #username, ${form} #email, ${form} #contact, ${form} #password`).bind('keyup', () => {
        nameValidation();
        contactValidation();
        emailVAlidation();
        passwordValidation();
        var formStateChanged = formScopeState !== formScope.serialize();
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
        } else if ($('#adminEmail').text() !== email.val()) {
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
            })
        }
    }

    function passwordValidation() {
        if (password.val()) {
            password.removeClass("is-invalid");
        }
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

function disableSubmit(form, state) {
    var submitBtn = $(form).find('input[type="submit"]');
    submitBtn.prop('disabled', state);
}
