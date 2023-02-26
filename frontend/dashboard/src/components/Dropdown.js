import { Component } from "react";
import { useState, useEffect, setState} from "react";
import './Dropdown.css';


// function DropdownItem(props) {
//     return (
//         <option value={props.value}>{props.name}</option>
//     );
// }

export function Dropdown (props) {
    //builds a list of dropdown items from a dictionary
    /*
        props: 
        - name: name of the dropdown
        - dictionary: dictionary of items to be added to the dropdown
    */

    function dropdownItems(dictionary){
        //builds a list of dropdown items from a dictionary
        let items = [];
        for (const [key, value] of Object.entries(dictionary)) {
            items.push(<option value={key}>{value}</option>);
        }
        return items;
    }

    return (
        <div className="dropdown-menu" id={props.name}>
            <h4>{props.name}</h4>
            <select name={props.name} id={props.name + '-drop'}>
                {dropdownItems(props.dictionary)}
            </select>
        </div>

    );
}



export function SeriesSelecter(props) {
    const [seriesJSON, setSeriesJSON] = useState({})
    const [regionsJSON, setRegionJSON] = useState({})
    
    const [activeSeries, setActiveSeries] = useState("")
    const [activeRegion, setActiveRegion] = useState("")

    const [dataToBackend, setDataToBackend] = useState({})

    const [selectSeries, setSelectSeries] = useState([])
    const [selectRegions, setSelectRegions] = useState([])
    const [regionsOptions, setRegionsOptions] = useState([])
    const [seriesOptions, setSeriesOptions] = useState([])



    function flask_getRegionsJSON() {
            const options = {
                method: "POST",
                headers: {"Content-Type" : "application/json"},
                body: JSON.stringify({title: "Testing"})
            };
            fetch('http://127.0.0.1:5000/jsons/regions_data.json/', options)
            .then(response => response.json()).then(data_back => {setRegionJSON(data_back)});
    }

    function flask_getSeriesJSON() {
        const options = {
            method: "POST",
            headers: {"Content-Type" : "application/json"},
            body: JSON.stringify({title: "Testing"})
        };
        fetch('http://127.0.0.1:5000/jsons/series_data.json/', options)
        .then(response => response.json()).then(data_back => {setSeriesJSON(data_back)});
}

    useEffect(() => {
        flask_getSeriesJSON();
        flask_getRegionsJSON();
        loadDropdowns()
    }, []);



    function loadDropdowns() {
        let s_options = []
        let r_options = []

        for (const [key, value] of Object.entries(seriesJSON)) {
            s_options.push(<option> {key} </option>)
        }

        for (const [key, value] of Object.entries(regionsJSON)) {
            r_options.push(<option> {value} - {key} </option>)
        }

        setSeriesOptions(s_options)
        setRegionsOptions(r_options)   
    }
    //onChange={(e) => {setSeriesID(e.target.value)}

    function addSeries() {
        let region_code = activeRegion.split(" - ")[0]
        let series_code = seriesJSON[activeSeries]
        if (dataToBackend[series_code] == undefined) {
            dataToBackend[series_code] = [region_code]
        }
        else {
            if (!(dataToBackend[series_code].includes(region_code))) {
                dataToBackend[series_code].push(region_code)
            }
        }
        alert(dataToBackend[series_code])
    }

    function clearSeries() {
        const options = {
            method: "POST",
            headers: {"Content-Type" : "application/json"},
            body: JSON.stringify(JSON.stringify({}))
        };
        fetch('http://127.0.0.1:5000/jsons/clear/', options)
        .then(response => response.json())
        setDataToBackend({})
    }

    function sendSeries() {
        const options = {
            method: "POST",
            headers: {"Content-Type" : "application/json"},
            body: JSON.stringify(dataToBackend)
        };
        fetch('http://127.0.0.1:5000/jsons/', options)
        .then(response => response.json())
    }

    return (

        <div>
            <select onChange={(e) => {setActiveSeries(e.target.value)}}>
                {seriesOptions}
            </select>
            <select onChange={(e) => {setActiveRegion(e.target.value)}}>
                {regionsOptions}
            </select>
            <button onClick = {() => addSeries()}> Add Series</button>
            <button onClick = {() => sendSeries()}> Select Series</button>
            <button onClick = {() => clearSeries()}> Clear Series </button>
        </div>

    );
}


export function Figure(props) {
    const [figure, setFigure] = useState("")

    function getFigure() {
        const options = {
            method: "POST",
            headers: {"Content-Type" : "imgage/png"},
            body: JSON.stringify({title: "Testing"})
        };
        fetch('http://127.0.0.1:5000/jsons/figure/', options)
        .then(response => response.json()).then(data_back => {setFigure(data_back)});
        //return <img src={`data:image/png;base64,${figure}`} alt={""}> </img>
    }


    return(
        <div>
                <button onClick={() =>getFigure()}> Visualize</button>
            <img src={`data:image/png;base64,${figure.png_string}`} alt="Series selecton invalid or empty..."></img>

        </div>
    );
    
    
    ;
}