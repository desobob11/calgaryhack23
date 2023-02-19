import wbgapi
import wbgapi.series as wseries
import wbgapi.series_metadata as wsm
import wbgapi.time as wtime
import wbgapi.source as sources
import wbgapi.data as wdata
import numpy as np
import pandas as pd
import json

def load_jsons():
    winfo = wseries.info().items



    d = {}
    # TODO: Get series name matched to id, region, begin date, end date, frequency
    '''
        winfo is a list of key-value pairs of series name to id
        
        loop adds each key value pair to single dictionary and writes to json file
    '''

    for i in winfo:
        d[i["value"]] = i["id"]

    '''
        Save key-value pair dictionary of region id to name as dictionary

    '''
    regions = wbgapi.region.info().items
    r = {}
    for i in regions:
        r[i["code"]] = i["name"]

    # write to JSON files
    with open("series_data.json", "w") as file:
        json.dump(d, file)

    with open("regions_data.json", "w") as file:
        json.dump(r, file)







