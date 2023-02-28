import { useEffect } from "react";
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

        const [dictionary, setItems] = useState([]);

        useEffect(() => {
            fetch('/jsons')
            .then(res => res.json())
            .then(data => {console.log(data); setItems(data[props.name])})}, []);

    function dropdownItems(){
        //builds a list of dropdown items from a dictionarys
        let items = [];
        for (const [key, value] of Object.entries(dictionary)) {
            items.push(<option value={key}>{value}</option>);
        }
        return items;
    }

    function handleChange(event) {
        props.storeCurrentSelection(event.target.value);
    }

    return (
        <div className="dropdown-menu" id={props.name}>
            <h4>{props.name}</h4>
            <select name={props.name} id={props.name + '-drop'} onChange={handleChange}>
                {dropdownItems()}
            </select>
        </div>

    );
}