/**
 * Dismisses the offer block
 */
function dismissOffer() {
    let offer = document.querySelector('#offers');
    offer.classList.replace('show', 'fade');
    setTimeout(function () {
        offer.remove();
    }, 1000);
}

/**
 * Check if user navigated to services page by clicking on a specific service link, and opens that.
 */
document.addEventListener('DOMContentLoaded', () => {
    if (location.href.includes('#')) {
        let section = location.href.substr(location.href.indexOf('#'));
        let collapseParent = document.querySelector(section + 'Parent');
        collapseParent.scrollIntoView();
        let collapseSection = document.querySelector(section);
        setTimeout(() => {
            collapseSection.classList.add('show');
        }, 500);
        this.flipIcon(collapseParent.querySelector('a'));
    }
});

/**
 * Inverts the text and icon for the specific EXPLORE button that's clicked.
 * @param {*} button HTML element which needs to be modified.
 */
function flipIcon(button) {
    icon = button.querySelector('i');
    text = button.querySelector('span');
    if (text.textContent === 'EXPLORE') {
        icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
        text.innerHTML = 'CLOSE';
    } else {
        icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
        text.innerHTML = 'EXPLORE';
    }
}

