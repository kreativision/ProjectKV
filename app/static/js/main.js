// Global JavaScript Functions. 
// Used By All Modules.


// Sidebar menu controls.
function openSidebar() {
    document.querySelector('#sidebar').classList.add('active');
    document.querySelector('#sidebar button').focus();
}

function closeSidebar() {
    document.querySelector('#sidebar').classList.remove('active');
}