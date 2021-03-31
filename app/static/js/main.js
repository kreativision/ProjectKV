// Global JavaScript Functions. 
// Used By All Modules.
let sidebar = document.querySelector('#sidebar');
let sidebarToggler = document.querySelector('#sidebarToggle');
const API_URL = `http://${window.location.hostname}:6174/api`;

/**
 * Method to set device specific link for the instagram button.
 */
$(document).ready(() => {
    if ($('.floating-action')) {
        instaBtn = $('.instagram');
        if ((navigator.userAgent.indexOf('Android') !== -1)) {
            instaBtn.attr("href", "instagram://user?username=kreativision.photoarts");
        } else {
            instaBtn.attr({
                href: "https://www.instagram.com/kreativision.photoarts/",
                target: "_blank"
            });
        }
    }
})

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
})
/**
 * Floating Action Button
 */
$('#contactUs, .fab-toggle, .fab-overlay').click(() => {
    $('.floating-action').toggleClass('active');
    $('.fab-overlay').toggleClass('active');
})