import { Component } from "react";
import { useState } from "react";
import './Dropdown.css';


// function DropdownItem(props) {
//     return (
//         <option value={props.value}>{props.name}</option>
//     );
// }

export default function Dropdown (props) {
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