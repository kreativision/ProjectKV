var sidebar = document.querySelector('#sidebar');
var sidebarToggler = document.querySelector('#sidebarToggle');
const API_URl = `http://${window.location.hostname}:6174/api`;

/**
 * Sidebar menu control function.
 * Required for mobile devices.
 */
function toggleSidebar(action) {
    if (action === 'open') {
        sidebar.classList.add('active');
    } else {
        sidebar.classList.remove('active');
    }
}
/**
 * Method to close the sidebar on clicking outside the sidebar area.
 * Required for Mobile devices
 */
document.addEventListener('click', function (e) {
    if (!sidebar.contains(e.target) && !sidebarToggler.contains(e.target)) {
        toggleSidebar('close');
    }
})
/**
 * Events to happen on page load.
 */
$(document).ready(function () {
    // enable toasts
    $(".toast").toast('show');
    // disable sidebar controls for desktop devices
    if ((navigator.userAgent.indexOf('Android') === -1)) {
        $('#sidebar').addClass('active');
    }
    // enable tooltips
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });
});