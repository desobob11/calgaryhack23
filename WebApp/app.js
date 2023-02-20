
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


async function loadJson(filename, type) {
    //Loads Json files for dropdown menus
    let dropdown = document.getElementById(`${type}-drop`);
    let dict = await fetchJson(filename);
    

    //populate dropdown menu with values from json file
    if (type == "region") {
        for (let code in dict) {
            let entry = document.createElement("option");
            entry.textContent=dict[code];
            entry.value = code
            dropdown.append(entry);
        }
    }
    else if (type == "series") {
        for (let code in dict) {
            let entry = document.createElement("option");
            entry.textContent=code;
            entry.value = dict[code]
            dropdown.append(entry);
        }
    }
}

async function fetchJson(filename) {
    //fetches local json files
    let filepath = "./json/" + filename + ".json";
    let regions = 
    await fetch(filepath)
        .then(response => { return response.json();})
    return regions
}

function addSeries() {
    let text_box = document.getElementById("series-selection");
    let region = document.getElementById("region-drop");
    let series = document.getElementById("series-drop");
    text_box.textContent = region.value + " * " + series.value;
}

async function main() {
    loadJson("regions_data", "region"); //load regions filter
    loadJson("series_data", "series"); //load series filter
}

main();