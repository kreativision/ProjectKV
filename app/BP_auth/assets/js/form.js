// registers form inputs on page load.
var formFields;
// locks the label in the float if text is entered into it. 
// otherwise restores the label in it's default position.
document.addEventListener("DOMContentLoaded", () => {
  formFields = document.querySelectorAll('.form-group .form-control');
  formFields.forEach((e) => {
    if (e.value != '') {
      e.parentNode.querySelector('label').classList.add('active');
    } else {
      e.parentNode.querySelector('label').classList.remove('active');
    }
    e.onblur = function () {
      if (e.value != '') {
        e.parentNode.querySelector('label').classList.add('active');
      } else {
        e.parentNode.querySelector('label').classList.remove('active');
      }
    }
  });
  // To focus the first input element by default when the page is loaded.
  setTimeout(() => {
    formFields[0].focus();
  }, 400);
});

// registers password fields on page-load. 
var passwords;
// toggles the visibility of password on checking the checkbox "Show Password"
function togglePassword() {
  if (!passwords) {
    passwords = document.querySelectorAll('input[type="password"]');
  }
  passwords.forEach(field => {
    if (field.type == 'text') {
      field.type = 'password';
    } else {
      field.type = 'text';
    }
  });
}