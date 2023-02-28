import Dropdown from './components/Dropdown';
import Button from './components/Button';
import './App.css';
import { useEffect } from 'react';
import FilterContainer from './components/FilterContainer';


function App() {  
  //#TODO:  
  //- Add a function to get the data from the backend
  //- Add a function to send data to the backend


  return (
    <div className="App">
      
      <FilterContainer list = {["series", "regions"]}></FilterContainer>

      <div id="graph-container">
        <h1 className="container-title">Graph View</h1>
        <div className="graph"></div>

        <div id="output">
        <div>This is simple test to get data from a backend</div>
        
        <div><span>Last update: </span><span id="time-container"></span></div>

        <div>
          <label>Data to send:</label>
          <input type="text" id="data-input"></input>
          <button>Send data</button>
        </div>
      
        <div>
            <div id="sent-data-container"></div>
        </div>
        <hr></hr>

        <div>
          <button>Get user data</button>
          <div id="result-container"></div>
        </div>

      </div>


      </div>


      
    </div>

  );
}

export default App;
