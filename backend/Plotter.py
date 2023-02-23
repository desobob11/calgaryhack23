import sqlite3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as sql3
from Database import Database
import json
import matplotlib.style as style


class Plotter:

    def __init__(self, data):
        self._function_map = {"line" : self.line, "stack" : self.stack}
        self._data = data
        self._series_map = None
        with open("jsons/series_data.json", "r") as file:
            self._series_map = json.load(file)

    def stack(self, series_map: dict[str, list[str]]) -> None:
        plt.style.use('seaborn-v0_8-pastel')
        x_axis = None
        plt.figure(1)
        legend = []
        latest_obs = 0
        valid_series = []
        for i in series_map:
            table = self._data[i]
            table.to_csv("energy.csv")
            if x_axis is None:
                x_axis = table.index
            for j in series_map[i]:
                try:
                    t = table[j].dropna()
                    if t.index[-1] > latest_obs:
                        latest_obs = t.index[-1]
                    if len(t) > 0 and j != "index":
                        valid_series.append(j)
                        legend.append("%s - %s" % (j, self._series_map[i]))
                except:
                    pass
        plt.legend(legend)
        print(table)
        #plt.xlim([0, latest_obs])
        plt.stackplot(self._data[i]["economy"], table[valid_series].transpose(), labels=valid_series)
        plt.legend(legend)
        plt.show()


    def line(self, series_map: dict[str, list[str]]) -> None:
        plt.style.use('seaborn-v0_8-whitegrid')
        x_axis = None
        plt.figure(1)
        legend = []
        for i in series_map:
            table = self._data[i]
            print(table)
            if x_axis is None:
                x_axis = table.index
            for j in series_map[i]:
                try:
                    t = table[j].dropna()
                    if len(t) > 0:
                        plt.plot(x_axis, table[j])
                        legend.append("%s - %s" % (j, self._series_map[i]))
                except:
                    pass
        plt.legend(legend)
        plt.show()





    def make_plot(self, type: str, series_map: dict[str, list[str]]) -> None:
        self._function_map[type](series_map)




def main():
    sample_data = {"EG.USE.COMM.FO.ZS": ["CAN", "USA"]}

    graph_data = sample_data

    con = sql3.connect("gen_data.db")

    data = Database.load_data(con, sample_data)
   # data["DT.NFL.PCBO.CD"].to_csv("shts.csv")
    p = Plotter(data)
    p.make_plot("stack", graph_data)

if __name__ == "__main__":
    main()