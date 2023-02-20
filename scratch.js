import './jsons'
var dict = {}


l = [1,2,3,4]

l.push(5)

async function select_series(series, region) {
    var series_name = series.value
    var region_name=  region.value

    let series_json = await fetch('./jsons/series_data.json')
                        .then(response => {return response.json();})
    return series_json

}

var data = select_series('a', 'b')


console.log(data)


