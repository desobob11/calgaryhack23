import { useState } from 'react';

import './CurrentFilter.css'

function CurrentFilter(props) {
    //adds a filter to the list of current filters, displays the name of the filter and a x next to it to remove it

    const [visible, setVisible] = useState("flex");

    function removeFilter() {
        //removes the current filter from the list of current filters
        console.log("remove filter");
        setVisible("none");
    }

    return (
        <div className="current-filter" style={{"display" : visible}}>
            {props.name}
            <button className="remove-filter-button" onClick={removeFilter}>X</button>
        </div>
    );
}

export default CurrentFilter;