import wbgapi
import wbgapi.series as wseries
import wbgapi.series_metadata as wsm
import wbgapi.time as wtime
import wbgapi.source as sources
import wbgapi.data as wdata
import json
import pandas as pd
import numpy as np

'''
    Class that reads in desired series vs JSON, pulls data from WB,
    and formats date into usable form

'''
class SeriesFormatter:

    def __init__(self):
        #TODO: hardcode for now, REMEMBER THIS SHOULD BE INPUT BY JSON AT THE END
       #self._series = None
        #self._series = {"Forest area (% of land area)" : ["AFE", "AFW"]}

        # data frames of data, each "series" has a data frame
        # containing observations for all regions associated with it from
        # 1962 to present
        self._dfs = {}

        # mapping desired series names to series id for querying
        self._series_ids = None



    '''
        Reads series_data.json, creating a dictionary that maps
        each desired series name to its id for querying
    '''
    def get_series_id(self) -> None:
        json_map = {}
        with open("series_data.json", "r") as file:
            json_map = json.load(file)
        self._series_ids = {}
        for i in json_map.keys():
            self._series_ids[i] = json_map[i]




    '''
        Function for querying data and compiling into appropriate data frames
    '''
    # TODO: REMEMBER THIS IS SET FOR A ID - LIST OF COUNTRIES K/V

    # TODO: CHECK TO SEE IF COUNTRY ALREADY EXISTS IN SERIES TABLE,
    # TODO: IF IT DOES NO REASON TO REQUERY IT
    def pull_compile_data(self, df_dict: dict) -> None:
        return_dict = {}
        for id in df_dict:
            return_dict[id] = wbgapi.data.DataFrame(id, df_dict[id]).transpose()
        return return_dict




def main():
    '''
    sf = Seriesormatter()
    sf.get_series_id()
    sf.pull_compile_data()
    df = None
    for i in sf._series:
        df = sf._dfs[i]
    pd.DataFrame(df).to_csv("TestingData.csv")
    '''
    # TODO: FIGURE OUT HOW AND WHEN THIS RUNS


if __name__ == "__main__":
    main()


