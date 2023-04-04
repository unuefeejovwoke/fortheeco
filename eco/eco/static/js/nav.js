// UI VARIABLES
const allNavToggle = document.querySelectorAll('.nav-toggle');
const navContainer = document.querySelectorAll('.nav-group');

// TOGGLE MENU
for (let toggleIndex = 0; toggleIndex < allNavToggle.length; toggleIndex++) {
	allNavToggle[toggleIndex].addEventListener('click', () =>
		toggleNavbar(toggleIndex)
	);
}

// TOGGLE MENU BAR BASED ON INDEX OF THE MENU GROUP
function toggleNavbar(index) {
	navContainer[index].classList.toggle('hidden');
}
