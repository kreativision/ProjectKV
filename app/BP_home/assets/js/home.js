// Function to load the selected project - INCOMPLETE
var projectCards = document.querySelectorAll('#deskShow .card');
function loadProject(projectID) {
    // document.querySelector('.bg-dark').classList.remove("bg-dark", "text-light");
    projectCards.forEach(card => {
        card.classList.remove("bg-dark", "text-light");
    });
    projectCards[projectID].classList.add("bg-dark", "text-light");
}