const hamburger = document.getElementById("check-icon");
const nav = document.querySelector(".menuList");

hamburger.addEventListener("change", () => {
    nav.classList.toggle('active', hamburger.checked);
});