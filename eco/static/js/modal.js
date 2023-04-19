
const addProblemButton = document.getElementById('add-problem');
const overlay = document.querySelector('.overlay');
const modal = document.querySelector('.modal');
const closeBtn = document.querySelector('.close-btn');

addProblemButton.addEventListener('click', function() {
  overlay.classList.remove('hidden');
  modal.classList.remove('hidden');
});

overlay.addEventListener('click', function() {
  overlay.classList.add('hidden');
  modal.classList.add('hidden');
});

closeBtn.addEventListener('click', function() {
  overlay.classList.add('hidden');
  modal.classList.add('hidden');
});

modal.addEventListener('click', function(event) {
  event.stopPropagation();
});


$('#slider').owlCarousel({
    items: 1,
    loop: true,
    nav: false,
    dots: true,
    autoplay: true,
    center: true
})
