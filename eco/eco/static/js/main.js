//script for nav dropdown
const navToggle = document.querySelector(".menu");
const navLinks = document.querySelector(".right-side__nav");

const navbarReveal = function () {
  navLinks.classList.toggle("hidden");
};

navToggle.addEventListener("click", navbarReveal);

//nav-dropdown
const dropBtn = document.querySelector(".dropbtn");
const dropContent = document.querySelector(".dropdown-content");

dropBtn.addEventListener("click", (e) => {
  if (e.target === dropBtn) {
    dropContent.classList.remove("d-none");
    dropContent.classList.add("d-show");
  } else {
    dropContent.add("d-none");
  }

  console.log("clicked dropdown");
});
// window.onclick = (function (e) {
//   if (
//     !e.target.matches(".dropbtn") &&
//     dropContent.classList.contains("d-show")
//   ) {
//     dropContent.classList.remove("d-show");
//     dropContent.classList.add("d-none");
//   }
// })

("use strict");

const heading4 = document.querySelector(".abbreviation");
const customUnderline = document.querySelector(".custom-underline");

const headWidth = heading4.offsetWidth;
const headLeft = heading4.offsetLeft;

customUnderline.style.width = headWidth + "px";
customUnderline.style.left = headLeft + "px";

//SCRIPT FOR MODAL
const projectModal = document.querySelector(".project-modal");
const problemModal = document.querySelector(".problem-modal");
const overlay = document.querySelector(".overlay");
const btnCloseModal = document.querySelectorAll(".close-btn");
const btnOpenProjectModal = document.querySelector("#add-project");
const btnOpenProblemModal = document.querySelector("#add-problem");

const openModal = function () {
  projectModal.classList.remove("hidden");
  overlay.classList.remove("hidden");
};

const openProblemModal = function () {
  problemModal.classList.remove("hidden");
  overlay.classList.remove("hidden");
};

const closeModal = function () {
  projectModal.classList.add("hidden");
  overlay.classList.add("hidden");
  problemModal.classList.add("hidden");
};

btnOpenProjectModal.addEventListener("click", openModal);
btnOpenProblemModal.addEventListener("click", openProblemModal);

for (let i = 0; i < btnCloseModal.length; i++) {
  btnCloseModal[i].addEventListener("click", closeModal);
}
overlay.addEventListener("click", closeModal);


//alert message
const alertMessage = document.querySelectorAll('.status-message');

const messageDisappear = function(){
  for (let i = 0; i<alertMessage.length; i++){
    alertMessage[i].style.display = "none";
  }
}

setTimeout(messageDisappear, 3500);