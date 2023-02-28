import { useState, useCallback } from "react";

import Button from "./Button";
import Dropdown from "./Dropdown";
import CurrentFilter from "./CurrentFilter";


import './Filter.css';

function Filter(props) {
    //builds a dropdown item with a name, a list of items, and a button to add that filter
    
    const [data, setData] = useState(null);
    
    const [, updateState] = useState();
    const forceUpdate = useCallback(() => updateState({}), []);

    function addFilters() {
        //adds the current filter to the list of current filters
        props.current_filters.push(<CurrentFilter name={"Hi"}></CurrentFilter>);
        forceUpdate();
        
    }
    
    function storeCurrentSelection(dropdown_value) {
        //is passed into the dropdown component
        //stores the value of the current selection in the dropdown
        setData(dropdown_value);
        console.log(data);

    }

    return (
        <div className="filter">
            <div className="current-filters">
            {props.current_filters}
            </div>
            <Dropdown className="filter-dropdowns" name={props.name} storeCurrentSelection={storeCurrentSelection}></Dropdown>
            <Button className="filter-button" name="Add Filter" onClick={addFilters} ></Button>
        </div>
    );

}

Filter.defaultProps = {
        name: "Filter",
        current_filters: [],
}

export default Filter;