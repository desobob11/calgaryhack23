import Button from "./Button";
import Dropdown from "./Dropdown";
import './Filter.css';

function Filter(props) {
    //builds a dropdown item with a name, a list of items, and a button to add that filter
    
    
    
    return (
        <div className="filter">
            <Dropdown className="filter-dropdowns" name={props.name}></Dropdown>
            <Button className="filter-button" name="Add Filter"></Button>
        </div>
    );

}

export default Filter;