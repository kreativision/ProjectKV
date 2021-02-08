// Global JavaScript Functions. 
// Used By All Modules.
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
 * Method to set device specific link for the instagram button.
 */
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.footer')) {
        let instaBtn = document.querySelector('.instagram');
        // let waBtn = document.querySelector('.whatsapp');
        if ((navigator.userAgent.indexOf('Android') !== -1)) {
            instaBtn.setAttribute('href', 'instagram://user?username=kreativision.photoarts');
        } else {
            instaBtn.setAttribute('href', 'https://www.instagram.com/kreativision.photoarts/');
            instaBtn.setAttribute('target', '_blank');
        }
    }
})

/**
 * Toast notification message control - jQuery.
 */
$(document).ready(function () {
    $(".toast").toast('show');
})