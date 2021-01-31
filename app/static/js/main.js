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
    isInstaBtnShown = document.querySelector('.instagram');
    if (isInstaBtnShown && (navigator.userAgent.indexOf('Android') !== -1)) {
        isInstaBtnShown.setAttribute('href', 'instagram://user?username=kreativision.photoarts');
    } else {
        isInstaBtnShown.setAttribute('href', 'https://www.instagram.com/kreativision.photoarts/');
        isInstaBtnShown.setAttribute('target', '_blank');
    }
})

/**
 * Toast notification message control - jQuery.
 */
$(document).ready(function () {
    $(".toast").toast('show');
})