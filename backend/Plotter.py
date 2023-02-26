import sqlite3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as sql3
from Database import Database
import json
import matplotlib.style as style
import pathlib as path
import matplotlib
plt.switch_backend('agg')
matplotlib.use('Agg')

class Plotter:

    def __init__(self, data):
        self._function_map = {"line" : self.line, "stack" : self.stack}
        self._data = data
        self._series_map = None
        with open("jsons/series_data.json", "r") as file:
            self._series_map = json.load(file)

        self._write_path = str("jsons/figure")
    
    def stack(self, series_map: dict[str, list[str]]) -> None:
        plt.style.use('seaborn-v0_8-pastel')
        x_axis = None
        self._figure = plt.figure(1)
        legend = []
        valid_series = []
        for i in series_map:
            table = self._data[i]
            if x_axis is None:
                x_axis = table["year"].astype(int)
            for j in series_map[i]:
                try:
                    t = table[j].dropna()
                    if len(t) > 0 and j != "year":
                        valid_series.append(j)
                        legend.append("%s - %s" % (j, self._series_map[i]))
                except:
                    pass
        plt.legend(legend)
        plt.xlim([np.min(x_axis), np.max(x_axis)])
        plt.stackplot(x_axis, table[valid_series].transpose(), labels=valid_series)
        plt.legend(legend)
        plt.xticks(np.arange(min(x_axis), max(x_axis), 10))
        #plt.show()


    def line(self, series_map: dict[str, list[str]]) -> None:
        if len(self._data.keys()) > 0:
            plt.style.use('seaborn-v0_8-whitegrid')
            x_axis = None
            self._figure = plt.figure(1)
            legend = []
            for i in series_map:
                table = self._data[i]
                print(table)
                if x_axis is None:
                    x_axis = table["year"].astype(int)
                for j in series_map[i]:
                    try:
                        t = table[j].dropna()
                        if len(t) > 0:
                            plt.plot(x_axis, table[j])
                            legend.append("%s - %s" % (j, self._series_map[i]))
                    except:
                        pass
            plt.legend(legend)
            plt.xticks(np.arange(min(x_axis), max(x_axis), 10))
            #plt.show()

    def save_fig(self):
        if len(self._data.keys()) > 0:
            self._figure.savefig(self._write_path + "/img.png", format="png")
        else:
            with open("jsons/figure/img.png", "wb+") as file:
                pass





    def make_plot(self, type: str, series_map: dict[str, list[str]]) -> None:
        self._function_map[type](series_map)




def main():
    sample_data = {}

    graph_data = sample_data

    con = sql3.connect("gen_data.db")

    data = Database.load_data(con, sample_data)
   # data["DT.NFL.PCBO.CD"].to_csv("shts.csv")
    p = Plotter(data)
    p.make_plot("line", graph_data)
    p.save_fig()

if __name__ == "__main__":
    main()