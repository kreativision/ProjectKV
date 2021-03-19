let revId = undefined;
let deleteRestoreId = undefined;
let modalAction = "";
let typeTracer = "new";
let reviews = [];
const deleteMsg = "Are you sure you want to delete this review?<br>This action cannot be undone!";
const restoreMsg = "The review will be restore to NEW state!<br>You would require to set it as REVIEWED manually.";
const REVIEW_API = `http://${window.location.hostname}:6174/api/review/`;
const reviewTemplate = document.getElementsByTagName('template')[0];
const reviewsContainer = document.querySelector('.reviews-container');
const loader = $('#loader');
const noResults = document.querySelector('#noResults');
const noResultsMsg = document.querySelector('#noTypeResults');
const reviewTypeToggler = document.querySelector("#reviewTypeToggler");
const markAllAsRead = document.querySelector('#markAllAsRead');

$(document).ready(() => {
    loader.removeClass('hidden');
    fetch(REVIEW_API + typeTracer).then(res => res.json()).then(data => {
        responseToTemplate(data, typeTracer);
    }).catch(err => console.log(err))
})

function fetchReviews(type) {
    typeTracer = type;
    document.querySelectorAll('.review-card').forEach(item => item.remove());
    loader.removeClass('hidden');
    if (!noResults.classList.contains('hidden')) { noResults.classList.add('hidden'); }
    fetch(REVIEW_API + typeTracer).then(res => res.json()).then(data => {
        responseToTemplate(data, typeTracer);
    }).catch(err => console.log(err))
}

function responseToTemplate(data, reviewType) {
    reviewTypeToggler.textContent = reviewType.toUpperCase();
    if (data.length > 0) {
        reviews = data;
        reviews.forEach(item => {
            const revCard = reviewTemplate.content.cloneNode(true);
            revCard.querySelector('div').setAttribute("id", `rev-${item.id}`);
            revCard.querySelector('#title').textContent = item.title;
            revCard.querySelector('#author').textContent = item.author;
            revCard.querySelector('#date').textContent = (new Date(item.date)).toDateString();
            revCard.querySelector('#catalogue').textContent = item.catalogue;
            let contentTarget = revCard.querySelector('#content');
            item.content ? contentTarget.textContent = item.content : contentTarget.classList.add('hidden');
            let statusText = revCard.querySelector('#status');

            if (reviewType === 'all') { statusText.textContent = item.status }

            if (item.status === 'NEW' || item.status === 'REMOVED') {
                revCard.querySelector('#actionMenu').classList.remove('hidden');
                let action1 = revCard.querySelector('#action1');
                let action2 = revCard.querySelector('#action2');
                switch (item.status) {
                    case "NEW":
                        action1.setAttribute("onclick", `editReview(${item.id})`);
                        action1.textContent = "Edit";
                        action2.setAttribute("onclick", `removeReview(${item.id})`);
                        action2.textContent = "Remove";
                        break;
                    case "REMOVED":
                        action1.setAttribute("onclick", `restoreOrDelete(${item.id}, 'Restore')`);
                        action1.textContent = "Restore";
                        action2.setAttribute("onclick", `restoreOrDelete(${item.id}, 'Delete')`);
                        action2.textContent = "Delete";
                        break;
                }
            }
            reviewsContainer.appendChild(revCard);
        });
        loader.addClass('hidden');
        if (reviewType === 'new') {
            markAllAsRead.classList.remove('hidden');
        } else {
            markAllAsRead.classList.add('hidden');
        }
    } else {
        loader.addClass('hidden');
        noResultsMsg.textContent = reviewType;
        noResults.classList.remove('hidden');
    }
}


function markAsReviewed() {
    fetch(REVIEW_API + 'mark-reviewed').then(res => res.json()).then(data => {
        if (data.success) {
            document.querySelectorAll('.review-card').forEach(item => item.remove());
            noResultsMsg.textContent = "new";
            noResults.classList.remove('hidden');
            markAllAsRead.classList.add('hidden');
            toaster('success', 'All NEW reviews are marked as REVIEWED');
        }
    }).catch(err => console.log(err))
}


/**
 * Function flow to edit a review.
 * @param {id} id ID of the review to edit.
 */
function editReview(id) {
    revId = id;
    $('#editReviewModal').modal({
        backdrop: "static"
    });
}

$('#editReviewModal').on('show.bs.modal', () => {
    const selectedReview = reviews.filter(item => { return item.id === revId })[0];
    $("#review_title").val(selectedReview.title);
    $("#review_content").val(selectedReview.content);
    $('#counter').text(selectedReview.title.length);
    let inputs = document.querySelectorAll('input[type="text"], textarea');
    inputs.forEach(field => {
        if (field.value) { field.parentNode.querySelector('label').classList.add('active'); }
        else { field.parentNode.querySelector('label').classList.remove('active'); }
        field.onblur = () => {
            if (field.value) { field.parentNode.querySelector('label').classList.add('active'); }
            else { field.parentNode.querySelector('label').classList.remove('active'); }

        }
    });
});

$('#editReviewModal').on('shown.bs.modal', () => {
    document.querySelector('input[type="text"]').focus();
    validateReview();
})

$('#editReviewModal').on('hidden.bs.modal', () => {
    revId = undefined;
    document.querySelectorAll('#review_title, #review_content').forEach((input) => {
        input.value = "";
    })
    $('#counter').text("0");
});

function validateReview() {
    let disable = true;
    $('input[type="submit"]').prop('disabled', disable);
    $('#review_id').val(revId);
    let title = $('#review_title');
    let counter = $('#counter');
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

document.querySelector('#editReviewModal form').addEventListener('submit', (event) => {
    event.preventDefault();
    const patchData = {
        "id": revId,
        "title": $('#review_title').val(),
        "content": $('#review_content').val(),
        "status": "EDITED"
    }
    fetch(REVIEW_API + 'action', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patchData)
    }).then(res => res.json())
        .then(data => {
            if (data.success) {
                if (typeTracer !== 'all') {
                    document.querySelector(`#rev-${data.id}`).remove();
                    if (document.querySelectorAll(".review-card").length === 0) {
                        noResultsMsg.textContent = "new";
                        noResults.classList.remove('hidden');
                    }
                } else {
                    const updatedRev = document.querySelector(`#rev-${data.id}`);
                    updatedRev.querySelector('#title').textContent = patchData.title;
                    if (patchData.content.length > 0) {
                        updatedRev.querySelector('#content').textContent = patchData.content;
                        updatedRev.querySelector('#content').classList.remove('hidden');
                    } else {
                        updatedRev.querySelector('#content').classList.add('hidden')
                    }
                    updatedRev.querySelector('.review-actions').classList.add('hidden');
                    updatedRev.querySelector('#status').textContent = patchData.status;
                }
                $('#editReviewModal').modal('hide');
                toaster('success', 'Review Edited Successfully');
            }
        })
        .catch(err => console.log(err))
})

/**
 * 
 * @param {*} reviewID the ID of the review to delete.
 */
function removeReview(reviewID) {
    const patchData = {
        "id": reviewID,
        "status": "REMOVED"
    }
    fetch(REVIEW_API + 'action', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patchData)
    }).then(res => res.json())
        .then(data => {
            if (data.success) {
                if (typeTracer !== 'all') {
                    document.querySelector(`#rev-${data.id}`).remove();
                    if (document.querySelectorAll(".review-card").length === 0) {
                        noResultsMsg.textContent = typeTracer;
                        noResults.classList.remove('hidden');
                    }
                } else {
                    document.querySelector(`#rev-${data.id} #status`).textContent = patchData.status;
                    const action1 = document.querySelector(`#rev-${data.id} #action1`);
                    const action2 = document.querySelector(`#rev-${data.id} #action2`);
                    action1.setAttribute("onclick", `restoreOrDelete(${data.id}, 'Restore')`);
                    action1.textContent = "Restore";
                    action2.setAttribute("onclick", `restoreOrDelete(${data.id}, 'Delete')`);
                    action2.textContent = "Delete";
                }
                toaster('success', 'Review REMOVED successfully');
            }
        })
        .catch(err => console.log(err))
}

function restoreOrDelete(reviewID, action) {
    $('#deleteRestoreModalLabel').text(`${action} Review`);
    $('#actionMessage').html(`${action === 'Restore' ? restoreMsg : deleteMsg}`);
    $('#actionPrimaryBtn').text(action);
    $('#actionPrimaryBtn').attr("onclick", `${action === 'Restore' ? 'restoreReview' : 'deleteReview'}(${reviewID})`);
    $('#deleteRestoreModal').modal({
        backdrop: 'static'
    });
}

function restoreReview(reviewId) {
    const patchData = {
        "id": reviewId,
        "status": "NEW"
    }
    fetch(REVIEW_API + 'action', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patchData)
    }).then(res => res.json()).then(data => {
        if (data.success) {
            if (typeTracer !== 'all') {
                document.querySelector(`#rev-${data.id}`).remove();
                if (document.querySelectorAll(".review-card").length === 0) {
                    noResultsMsg.textContent = typeTracer;
                    noResults.classList.remove('hidden');
                }
            } else {
                document.querySelector(`#rev-${data.id} #status`).textContent = patchData.status;
                const action1 = document.querySelector(`#rev-${data.id} #action1`);
                const action2 = document.querySelector(`#rev-${data.id} #action2`);
                action1.setAttribute("onclick", `editReview(${data.id})`);
                action1.textContent = "Edit";
                action2.setAttribute("onclick", `removeReview(${data.id})`);
                action2.textContent = "Remove";
            }
            $('#deleteRestoreModal').modal('hide');
            toaster('success', 'Review RESTORED successfully to NEW state');
        }
    }).catch(err => console.log(err))
}

function deleteReview(reviewID) {
    fetch(REVIEW_API + 'action', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "id": reviewID })
    }).then(res => res.json()).then(data => {
        if (data.success) {
            document.querySelector(`#rev-${data.id}`).remove();
            if (document.querySelectorAll(".review-card").length === 0) {
                noResultsMsg.textContent = typeTracer;
                noResults.classList.remove('hidden');
            }
            $('#deleteRestoreModal').modal('hide');
            toaster('success', 'Review permanently deleted.');
        }
    }).catch(err => console.log(err))
}

/**
 * 
 * @param {*} type message type: success | error
 * @param {*} msg message content
 */
function toaster(type, msg) {
    setTimeout(() => {
        $('#dynamicToastHeader').text(type.toUpperCase())
        $('#dynamicToastHeader').addClass(`text-${type}`);
        $('#dynamicToastBody').text(msg);
        $('.toast').removeClass("hide", "fade");
        $(".toast").toast('show');
    }, 200);
}