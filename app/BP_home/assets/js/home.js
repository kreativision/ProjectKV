// Function to load the selected project - INCOMPLETE
var projectCards = document.querySelectorAll('#deskShow .card');
function loadProject(projectID) {
    document.querySelector('.active-project').classList.remove('active-project');
    projectCards[projectID].classList.add('active-project');
}