import { Component } from "react";
import { useState } from "react";



function Button(props) {


    const [count, setCount] = useState(0);


    return (
        <button 
            className={props.className} 
            id={props.id} 
            onClick={props.onClick}>{props.name}
        </button>
    );
}

Button.defaultProps = {
    name: "default button",
    className: "default-button",
    id: null,
}

export default Button;