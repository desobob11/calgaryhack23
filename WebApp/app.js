function toggleDarkMode() {

    document.getElementById("dark-button").blur();

    let html = document.querySelector("html");
    let buttons = document.getElementsByClassName("header-buttons")[0];
    if (html.className != "dark-mode") {
        html.classList.add("dark-mode");
        buttons.children[0].classList.add("dark-mode");
        buttons.children[1].classList.add("dark-mode");
        buttons.children[2].classList.add("dark-mode");
    }
    else {
        html.classList.remove("dark-mode");
        buttons.children[0].classList.remove("dark-mode");
        buttons.children[1].classList.remove("dark-mode");
        buttons.children[2].classList.remove("dark-mode");
    }
}

async function main() {
    
}

main();