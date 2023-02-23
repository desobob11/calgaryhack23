

import { Component } from "react";
import { useState } from "react";
import figure from './fig.png'


function Figure() {
    return (
      //  <div className="image" id={props.name}>
       //            <img src="/fig.png"  alt=""> </img> 
       // </div>
        <div>
            hello
            <img src={figure} alt={''}>

            </img>
        </div>
    );
}

export default Figure;

