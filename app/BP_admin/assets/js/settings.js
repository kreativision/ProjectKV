$('#locationForm').on('shown.bs.collapse', () => {
    $('#loc-city').focus();
    $('#locFormToggler').html("CANCEL <i class='fas fa-chevron-up ml-2'></i>");
    activateFormBehaviour('#locationForm form');
    validateLocation();
});

$('#locationForm').on('hidden.bs.collapse', () => {
    $('#locFormToggler').html("CHANGE <i class='fas fa-chevron-down ml-2'></i>");
});

function validateLocation() {
    const city = $('#loc-city');
    const link = $('#loc-map_link');
    $("#loc-update").prop('disabled', true);
    $('#loc-city, #loc-map_link').bind('keyup', () => {
        let isLinkValid = validateMapLink();
        if(city.val() && link.val() && isLinkValid) {
            $("#loc-update").prop('disabled', false);
        } else {
            $("#loc-update").prop('disabled', true);
        }
    });
    function validateMapLink() {
        if(link.val() && !link.val().startsWith('https://www.google.com/maps/embed?pb=')) {
            link.addClass("is-invalid");
            link.parent().find('#link_error').text("Google Maps embed link invalid.");
            return false;
        } else {
            link.removeClass("is-invalid");
            return true;
        }
    }
}
