var sidebar = document.querySelector('#sidebar');
var sidebarToggler = document.querySelector('#sidebarToggle');

/**
 * Sidebar menu control function.
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
 */
document.addEventListener('click', function (e) {
    if (!sidebar.contains(e.target) && !sidebarToggler.contains(e.target)) {
        toggleSidebar('close');
    }
})
/**
 * Toast notification message control - jQuery.
 */
$(document).ready(function () {
    $(".toast").toast('show');
    if ((navigator.userAgent.indexOf('Android') === -1)) {
        $('#sidebar').addClass('active');
    }
})