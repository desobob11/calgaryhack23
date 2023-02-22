import { Component } from "react";
import { useState } from "react";



function Button(props) {

    const [count, setCount] = useState(0);


    return (
        <button className="button" onClick={() => setCount(count + 1)}>{count}</button>
    );
}

export default Button;