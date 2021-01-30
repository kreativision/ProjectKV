function dismissOffer() {
    let offer = document.querySelector('#offers');
    
    offer.classList.remove('show');
    offer.classList.add('fade');
    setTimeout(function () {
        offer.remove();
    }, 1000);
}