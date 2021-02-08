/**
 * Auth Page Scripts - manipulation of the form-fields on the page.
 */
var formFields = document.querySelectorAll('.form-group .form-control, .input-group .form-control');
var passwords = document.querySelectorAll('input[type="password"]');
var toggleIcon = document.querySelector('#pwd-toggle i');

/**
 * locks the label in the float position if there is value in it, on page-load.
 * Also sets the onblur method for each field to check if data is entered and lock label
 */
document.addEventListener("DOMContentLoaded", () => {
  formFields.forEach((element) => {
    if (element.value) {
      element.parentNode.querySelector('label').classList.add('active');
    }
    element.onblur = () => {
      if (element.value) {
        element.parentNode.querySelector('label').classList.add('active');
      }
    }
  });
});

/**
 * toggles the visibility of password on checking the checkbox "Show Password".
 * Also toggle the icon on click
 */
function togglePassword() {
  passwords.forEach(field => {
    if (field.type == 'text') {
      toggleIcon.classList.replace('fa-eye', 'fa-eye-slash');
      field.type = 'password';
    } else {
      toggleIcon.classList.replace('fa-eye-slash', 'fa-eye');
      field.type = 'text';
    }
  });
  toggleIcon.parentElement.blur();
}