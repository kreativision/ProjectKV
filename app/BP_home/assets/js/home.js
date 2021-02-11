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
 * page load events.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Services page navigation behaviours
    if (location.href.includes('services#')) {
        let section = location.href.substr(location.href.indexOf('#'));
        let collapseParent = document.querySelector(section + 'Parent');
        let collapseSection = document.querySelector(section);
        setTimeout(() => {
            collapseSection.classList.add('show');
            this.flipIcon(collapseParent.querySelector('a'));
            collapseParent.scrollIntoView();
        }, 500);
    }
});

/**
 * Inverts the text and icon for the specific EXPLORE button that's clicked on a catalog item.
 * @param button HTML element which needs to be modified.
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
