let revId = undefined;
let deleteRestoreId = undefined;
let modalAction = "";
let deleteMsg = "Are you sure you want to delete this review?<br>This action cannot be undone!"
let restoreMsg = "The review will be restore to NEW state!<br>You would require to set it as REVIEWED manually."
const DELETE_URL = `http://${window.location.hostname}:6174/a/delete-review/`;
const RESTORE_URL = `http://${window.location.hostname}:6174/a/restore-review/`

function editReview(button) {
    revId = button.getAttribute("id");
    $('#editReviewModal').modal({
        backdrop: "static"
    });
}

function deleteRestoreModal(action, button) {
    deleteRestoreId = button.getAttribute("id");
    modalAction = action;
    $('#deleteRestoreModal').modal({
        backdrop: "static"
    });
}

$('#deleteRestoreModal').on('show.bs.modal', () => {
    if (modalAction == 'delete') {
        $('#actionMessage').html(deleteMsg);
        $('#deleteBtn').attr("href", DELETE_URL + deleteRestoreId);
        $('#deleteBtn').text("Delete");
        $('#deleteRestoreModalLabel').text("Delete Review");
    } else {
        $('#actionMessage').html(restoreMsg);
        $('#deleteBtn').attr("href", RESTORE_URL + deleteRestoreId);
        $('#deleteBtn').text("Restore");
        $('#deleteRestoreModalLabel').text("Restore Review");
    }
});

$('#deleteRestoreModal').on('hidden.bs.modal', () => {
    $('#deleteBtn').attr("href", "");
    deleteRestoreId = undefined;
    modalAction = "";
    $('#actionMessage').html("");
    $('#deleteBtn').text("");
    $('#deleteRestoreModalLabel').text("");
});

$('#editReviewModal').on('shown.bs.modal', () => {
    fetch(`${API_URL}/review-data/${revId}`).then(res => {
        return res.json();
    }).then(reviewData => {
        for (let key in reviewData)
            $(`#review_${key}`).val(reviewData[key]);
        $('#counter').text(reviewData.title.length);
        activateFormBehaviour('#editReviewForm');
    }).catch(err => {
        console.log(err);
    })
});

$('#editReviewModal').on('hidden.bs.modal', () => {
    revId = undefined;
    document.querySelectorAll('#review_title, #review_content').forEach((input) => {
        input.value = "";
    })
    $('#counter').text("0");
});

function activateFormBehaviour(form) {
    let inputs = document.querySelectorAll(`${form} input[type="text"], ${form} textarea`);
    inputs.forEach(field => {
        if (field.value) { field.parentNode.querySelector('label').classList.add('active'); }
        else { field.parentNode.querySelector('label').classList.remove('active'); }
        field.onblur = () => {
            if (field.value) { field.parentNode.querySelector('label').classList.add('active'); }
            else { field.parentNode.querySelector('label').classList.remove('active'); }

        }
    });
    let end = inputs[0].value.length;
    inputs[0].setSelectionRange(end, end);
    inputs[0].focus();
    validateReview();
}

function validateReview() {
    var disable = true;
    $('input[type="submit"]').prop('disabled', disable);
    $('#review_id').val(revId);
    var title = $('#review_title');
    var content = $('#review_content');
    var counter = $('#counter');
    formScope = $(`#editReviewForm input[type="text"], #editReviewForm textarea`);
    const formScopState = formScope.serialize();

    formScope.bind('keyup', () => {
        countTitleLength();
        titleEmpty();
        let errors = document.querySelectorAll(".is-invalid").length;
        let stateChanged = formScopState !== formScope.serialize()
        if (stateChanged && !errors) {
            disable = false;
        } else {
            disable = true;
        }
        $('input[type="submit"]').prop('disabled', disable);
    });

    function titleEmpty() {
        if (!title.val()) {
            title.addClass('is-invalid');
            $('#rTitle_error').text("Title cannot be empty.");
        } else {
            title.removeClass('is-invalid');
        }
    }

    function countTitleLength() {
        let titleLength = title.val() ? title.val().length : 0
        counter.text(titleLength);
    }
}