import Dropdown from './components/Dropdown';
import Button from './components/Button';
import Figure from './components/Figure';
import './App.css';

function App() {  
  //#TODO:  
  //- Add a function to get the data from the backend
  //- Add a function to send data to the backend

  const regions_dictionary = { "AFR": "Africa", "AMR": "Americas", "EMR": "Eastern Mediterranean", "EUR": "Europe", "SEAR": "South-East Asia", "WPR": "Western Pacific"}
  const series_dictionary = {"NY.GDP.MKTP.CD": "GDP (current US$)", "NY.GDP.PCAP.CD": "GDP per capita (current US$)", "SP.POP.TOTL": "Population, total"}

  return (
    <div className="App">
      
      <div id="filter-container">
          <h1 className="container-title">Filter Settings</h1>
          
          <div className="filters">
            <Dropdown name={"series"} dictionary={regions_dictionary}></Dropdown>
            <Dropdown name={"region"} dictionary={series_dictionary}></Dropdown>
            <Button></Button>
          </div>

          <div id="confirm-pull">
            <button id="add-button">Add Data</button>
            <button id="pull-button">Pull Data</button>
          </div>
      </div>

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
        

        <Figure></Figure>

 
      </div>


      </div>


      
    </div>

  );
}

export default App;
