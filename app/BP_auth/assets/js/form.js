// Auth Page Scripts - manipulation of the form-fields on the page.
const email_pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

let formFields = document.querySelectorAll('.form-group .form-control, .input-group .form-control');
let passwords = document.querySelectorAll('input[type="password"]');
let toggleIcon = document.querySelector('#pwd-toggle i');

/**
 * Events on page load  
 */
document.addEventListener("DOMContentLoaded", () => {
  formFields.forEach((field) => {
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
  });
});

/**
 * Runs a 10-minute countdown timer if on the email-sent page.
 */
document.addEventListener("DOMContentLoaded", () => {
  let clock = document.querySelector('.clock');
  if (clock) {
    let minutes = clock.querySelector('.minutes');
    let seconds = clock.querySelector('.seconds');
    minutes.textContent = '10m';
    seconds.textContent = '00s';
    let time = 600;
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
}

/**
 * Client-Side Password validation.
 */
function validatePassword() {
  let password = $('#password');
  let cnfPassword = $('#cnf_password');
  let confirmationError = cnfPassword.parent().find('#conf_pwd_error');
  if (cnfPassword.val() === '') {
    return;
  }
  if (password.val() !== cnfPassword.val()) {
    cnfPassword.addClass("is-invalid");
    confirmationError.text("Passwords don't match");
  } else {
    cnfPassword.removeClass("is-invalid");
    confirmationError.text("");
  }
}

/**
 * API Call for client-side e-mail verification.
 */
let jEmail;
$(document).ready(function () {
  jEmail = $('#email');
  jEmail.bind('blur', function () {
    mailId = jEmail.val();
    if (mailId === "") {
      return;
    } else if (email_pattern.test(mailId)) {
      $.ajax({
        url: `${API_URL}/check-email/${jEmail.val()}`,
        contentType: 'application/json',
        dataType: 'json',
        success: function (user) { EmailErrorHandler(user); }
      })
    } else {
      jEmail.addClass("is-invalid");
      jEmail.parent().find('#email_error').html("Invalid e-mail address");
    }
  });
});

/**
 * UI Manipulation supporting function to show email related errors 
 */
function EmailErrorHandler(user) {
  if (window.location.pathname.includes('sign-up') && user.registered) {
    jEmail.addClass("is-invalid");
    if (jEmail.parent().find('#email_hint')) {
      jEmail.parent().find('#email_hint').remove();
    }
    jEmail.parent().find('#email_error').html("This e-mail is already registered. You can <a href='/login'>login</a> or <a href='/forgot-password'>reset your password.</a>");
  } else if ((window.location.pathname.includes('login') || window.location.pathname.includes('forgot')) && !user.registered) {
    jEmail.addClass("is-invalid");
    jEmail.parent().find('#email_error').html("This email is not registered. <a href='/sign-up'>Please register.</a>");
  } else if (jEmail.hasClass("is-invalid")) {
    jEmail.removeClass("is-invalid");
    jEmail.parent().find('#email_error').html("");
  }
}