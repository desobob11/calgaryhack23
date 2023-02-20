function toggleDarkMode() {
    //Toggles dark mode on app 
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




function populateDropdown(dict, type) {
    let dropdown = document.getElementById(`${type}-drop`);//select dropdown menu
    
    //populate dropdown menu with values from json file
    for (let code in dict) {
        let entry = document.createElement("option");
        entry.textContent = dict[code];
        entry.value = code;
        dropdown.append(entry);
    }
}

async function loadJson(filename) {
    //Loads Json file contents as dictionary object
    const dict = await fetchJson(filename);
    return dict;
}

async function fetchJson(filename) {
    //fetches local json files
    let filepath = "./jsons/" + filename + ".json";
    let regions = 
    await fetch(filepath)
        .then(response => { return response.json();})
    return regions
}

function addRegion() {
    //adds regions to list of filters
    let region = document.getElementById("region-drop").value;
    
    //skip if region is already in selection
    if (!selected_regions.includes(region)) {
        selected_regions.push(region);
    }    
    console.log(selected_regions);
}

function addData() {
    //adds filter selections to data query
    let series = document.getElementById("series-drop").value; //series code
    selected_filters[series] = selected_regions; //add to filter in the form of {series code : [regions]}
    console.log(selected_filters);
    document.getElementById("series-selection").innerHTML = selected_filters[series] 
}

function pullData() {
    //sends query into working directory as a json file for backend

    let query_data = JSON.stringify(selected_filters);

    let a = document.createElement("a");
    let file = new Blob([query_data], {type: "text/json"});
    a.href = URL.createObjectURL(file);
    a.download = "query.json";
    a.click();

    
}

let regions; //holds objects of regions {code : region}
let series; //holds dictionary of series by {code : series}

let selected_filters = {}; //keeps track of currently selected filters
const selected_regions = []; //keeps track of regions added to current selection

async function main() {
    regions = await loadJson("regions_data"); //load regions dictionary
    series = await loadJson("series_data"); //load series dictionary
    populateDropdown(regions, "region");
    populateDropdown(series, "series");
}

window.addEventListener("DOMContentLoaded", function () {

    //initialize buttons
    document.getElementById("add-button").addEventListener("click", addData);
    document.getElementById("pull-button").addEventListener("click", pullData);
})

main();