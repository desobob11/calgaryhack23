import Button from "./Button";
import Dropdown from "./Dropdown";
import './FilterContainer.css';
import Filter  from "./Filter";


function FilterContainer(props) {
    //builds a list of dropdown items from a list prop
    /** */

    let dropdowns = [];
    Object.values(props.list).forEach((value) => {
        console.log(value);
        dropdowns.push(<Filter name = {value}></Filter>)
    }
    );
    
    return (
        <div className="filters">
            <h1 className="container-title">Filters</h1>
                {dropdowns}
            
            <div id="current filters">

            </div>

            <div id="confirm-pull">
                <Button name={"Add Data"} />
                <Button name={"Show Graphs"} id="add-button" />
            </div>
        </div>
    );
}

export default FilterContainer;