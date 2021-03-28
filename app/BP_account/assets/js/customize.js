document.addEventListener("DOMContentLoaded", () => {
    let formFields = document.querySelectorAll('.form-group .form-control, .input-group .form-control');
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