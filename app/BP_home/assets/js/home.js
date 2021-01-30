function dismissOffer() {
    let offer = document.querySelector('#offers');
    offer.classList.replace('show', 'fade');
    setTimeout(function () {
        offer.remove();
    }, 1000);
}

function flipIcon(button) {
    icon = button.querySelector('i');
    text = button.querySelector('span');
    if (text.textContent === 'EXPLORE') {
        icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
        text.innerHTML = 'CLOSE';
    }
    else {
        icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
        text.innerHTML = 'EXPLORE';
    }
}