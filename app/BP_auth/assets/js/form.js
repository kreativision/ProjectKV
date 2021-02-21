/**
 * Auth Page Scripts - manipulation of the form-fields on the page.
 */
const API_URl = `http://${window.location.hostname}:6174/api`;
const email_pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

var formFields = document.querySelectorAll('.form-group .form-control, .input-group .form-control');
var passwords = document.querySelectorAll('input[type="password"]');
var toggleIcon = document.querySelector('#pwd-toggle i');
var email_field = document.querySelector('#email');

/**
 * Events on page load
 */
document.addEventListener("DOMContentLoaded", () => {
  // for form pages, check if fields are prefilled, and position label accordingly.
  // register the onblur event of the fields.
  formFields.forEach((element) => {
    if (element.value) {
      element.parentNode.querySelector('label').classList.add('active');
    }
    element.onblur = () => {
      if (element.value) {
        element.parentNode.querySelector('label').classList.add('active');
      } else {
        element.parentNode.querySelector('label').classList.remove('active');
      }
    }
  });
  // for email sent page, register the closk segment and start the timer.
  var clock = document.querySelector('.clock');
  if (clock)
    timer(clock, 600);
});

/**
 * countdown timer
 */
function timer(clockElement, time) {
  let minutes = clockElement.querySelector('.minutes');
  let seconds = clockElement.querySelector('.seconds');
  minutes.textContent = '10m';
  seconds.textContent = '00s';
  let countDown = setInterval(() => {
    'use strict';
    let min = Math.floor(time / 60), remSec = time % 60;
    if (remSec < 10) {
      remSec = '0' + remSec;
    }
    if (min < 10) {
      min = '0' + min;
    }
    minutes.textContent = min + 'm';
    seconds.textContent = remSec + 's';
    if (time > 0) {
      time = time - 1;
    } else {
      clearInterval(countDown);
      document.querySelector('.notice').remove();
      document.querySelector('#resend').classList.add('active');
    }
  }, 1000);
}

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

/**
 * Client-Side Password validation.
 */
function validatePassword() {
  let password = document.querySelector('#password');
  let cnfPassword = document.querySelector('#cnf_password')
  let confirmationError = cnfPassword.parentElement.querySelector('#conf_pwd_error')
  if (cnfPassword.value === '') {
    return;
  }
  if (password.value !== cnfPassword.value) {
    cnfPassword.classList.add("is-invalid");
    confirmationError.textContent = "Passwords don't match";
  } else {
    cnfPassword.classList.remove("is-invalid");
    confirmationError.textContent = "";
  }
}

/**
 * API Call for client-side e-mail verification.
 */
email_field.addEventListener('blur', () => {
  email_id = email_field.value;
  if (email_id === '') { return; }
  // validate e-mail format and make api call for DB validation
  if (email_pattern.test(email_id)) {
    const requestUrl = `${API_URl}/check-email/${email_id.toLowerCase()}`;
    var request = new XMLHttpRequest()
    request.open('GET', requestUrl, true);
    // show appropriate validation errors depending on page and field.
    request.onload = () => {
      let user = JSON.parse(request.response);
      if (window.location.pathname.includes('sign-up') && user.registered) {
        email_field.classList.add("is-invalid");
        if (email_field.parentElement.querySelector('#email_hint')) {
          email_field.parentElement.querySelector('#email_hint').remove();
        }
        email_field.parentElement.querySelector('#email_error').innerHTML = "This e-mail is already registered. You can <a href='/login'>login</a> or <a href='/forgot-password'>reset your password.</a>";
      } else if ((window.location.pathname.includes('login') || window.location.pathname.includes('forgot')) && !user.registered) {
        email_field.classList.add("is-invalid");
        email_field.parentElement.querySelector('#email_error').innerHTML = "This email is not registered. <a href='/sign-up'>Please register.</a>";
      } else if (email_field.classList.contains("is-invalid")) {
        email_field.classList.remove("is-invalid");
        email_field.parentElement.querySelector("#email_error").innerHTML = "";
      }
    }
    request.send();
  }
  // if email is not of valid format
  else {
    email_field.classList.add("is-invalid");
    if (email_field.parentElement.querySelector('#email_hint')) {
      email_field.parentElement.querySelector('#email_hint').remove();
    }
    email_field.parentElement.querySelector('#email_error').innerHTML = "Invalid email address.";
  }
});