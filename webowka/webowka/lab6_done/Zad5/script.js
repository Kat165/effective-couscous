const carouselSlide = document.querySelector(".carousel-slide");
const carouselSlides = document.querySelectorAll(".carousel-slide div");

const prevBtn = document.querySelector("#prevbtn");
const nextBtn = document.querySelector("#nextbtn");
const ranBtn = document.querySelector("#randombtn");

let counter = 1;
const size = carouselSlides[0].clientWidth;

carouselSlide.style.transform = 'translateX(' + (-size * counter) + 'px)';

nextBtn.addEventListener('click', () => {
  if(counter >= carouselSlides.length -1) return;
  carouselSlide.style.transition = 'transform 0.4s ease-in-out';
  counter++;
  carouselSlide.style.transform = 'translateX(' + (-size * counter) + 'px)';
});

prevBtn.addEventListener('click', () => {
  if(counter<=0) return;
  carouselSlide.style.transition = 'transform 0.4s ease-in-out';
  counter--;
  carouselSlide.style.transform = 'translateX(' + (-size * counter) + 'px)';
});

carouselSlide.addEventListener('transitionend',()=>{
  if(carouselSlides[counter].id == 'lastclone'){
    carouselSlide.style.transition = 'none';
    counter = carouselSlides.length - 2;
    carouselSlide.style.transition = 'transform 0.4s ease-in-out';
  }

  if(carouselSlides[counter].id == 'firstclone'){
    carouselSlide.style.transition = 'none';
    counter = carouselSlides.length - counter;
    carouselSlide.style.transition = 'transform 0.4s ease-in-out';
  }
});

ranBtn.addEventListener('click', () => {
  let random_num = Math.floor(Math.random() * 4)

  for (let index = 0; index < random_num; index++) {
    if(counter<=0) return;
    carouselSlide.style.transition = 'transform 0.4s ease-in-out';
    counter--;
    carouselSlide.style.transform = 'translateX(' + (-size * counter) + 'px)';
  }
  
});