// registers form inputs on page load.
var formFields = document.querySelectorAll('.form-group .form-control, .input-group .form-control');

// locks the label in the float position if there is value on page-load.
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
  // Autofocus the first input element on page load => handled in the form class.
  // setTimeout(() => {
  //   formFields[0].focus();
  // }, 400);
});


// registers password fields on page-load. 
var passwords = document.querySelectorAll('input[type="password"]');
var toggleButton = document.querySelector('#pwd-toggle i');

// toggles the visibility of password on checking the checkbox "Show Password".
function togglePassword() {
  passwords.forEach(field => {
    if (field.type == 'text') {
      field.type = 'password';
    } else {
      field.type = 'text';
    }
  });
  // toggle the eye icon
  if (toggleButton.classList.contains('fa-eye')) {
    toggleButton.classList.remove('fa-eye');
    toggleButton.classList.add('fa-eye-slash');
  } else {
    toggleButton.classList.remove('fa-eye-slash');
    toggleButton.classList.add('fa-eye');
  }
  toggleButton.parentElement.blur();
}

// Automatically capitalize the first letter of every word in the username field.
uname = document.querySelector('#username');
if(uname) {
  uname.onkeyup = () => {
    uname.value = (uname.value).split(' ').map((word) => {
      return word.charAt(0).toUpperCase() + word.substr(1).toLowerCase();
    }).join(' ');
  }
}