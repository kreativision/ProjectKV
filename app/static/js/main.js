// Global JavaScript Functions. 
// Used By All Modules.

// method to close the sidebar on clicking outside the sidebar area
document.addEventListener('click', function (e) {
    if (!document.querySelector('#sidebar').contains(e.target) && !document.querySelector('#sidebarToggle').contains(e.target)) {
        closeSidebar()
    }
})

// Sidebar menu controls.
function openSidebar() {
    document.querySelector('#sidebar').classList.add('active');
    document.querySelector('#sidebar button').focus();
}

function closeSidebar() {
    document.querySelector('#sidebar').classList.remove('active');
}

// toast message control
$(document).ready(function() {
    $(".toast").toast('show');
})