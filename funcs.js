
import './jsons'

var output_dict = {}

/*
    async function fetchJson(filename) {
        //fetches local json files
        let filepath = "./json/" + filename + ".json";
        let regions = 
        await fetch(filepath)
            .then(response => { return response.json();})
        return regions
    }
*/

async function select_series(series, region) {
    var series_name = series.value
    var region_name=  region.value

    let series_json = await fetch('series_data.json')
                        .then(response => {return response.json();})
    //return series_json
    alert(series_json)









}


