//registeration page
const loginBtn = document.querySelector("#loginBtn");
const signUpBtn = document.querySelector("#signUpBtn");
const loginPage = document.querySelector("#Login");
const signUpPage = document.querySelector("#Register");

const pwrd = document.querySelectorAll("#pwrdHASHED");
const reveal = document.querySelectorAll(".ri-eye-line");

const pwrdReveal = function () {
  for (let j = 0; j < pwrd.length; j++) {
    if (pwrd[j].type === "password") {
      pwrd[j].type = "text";

      reveal[j].classList.add("ri-eye-off-line");
      reveal[j].classList.remove("ri-eye-line");
    } else {
      pwrd[j].type = "password";
      reveal[j].classList.add("ri-eye-line");
      reveal[j].classList.remove("ri-eye-off-line");
    }
  }
};

for (let i = 0; i < reveal.length; i++) {
  reveal[i].addEventListener("click", pwrdReveal);
}

// reveal.addEventListener("click", pwrdReveal);

setTimeout(() => {
  loginBtn.addEventListener("click", () => {
    loginPage.classList.add("d-show");
    signUpPage.classList.remove("d-show");
    signUpPage.classList.add("d-none");
    loginBtn.classList.add("active");
    signUpBtn.classList.remove("active");
  });
}, 2000);

setTimeout(() => {
  signUpBtn.addEventListener("click", () => {
    signUpPage.classList.remove("d-none");
    signUpPage.classList.add("d-show");
    loginPage.classList.remove("d-show");
    loginPage.classList.add("d-none");
    loginBtn.classList.remove("active");
    signUpBtn.classList.add("active");
  });
}, 2000);

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
