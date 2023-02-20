import wbgapi.series as wseries
import json
import pandas as pd
import sqlite3 as sql3
import sqlalchemy as sql
import wbgapi


'''
    Function that writes queried series to local sqlite3 database
'''
class Database:
# TODO: ACCOMODATE NEW DATE ROW ENTRIES FOR FUTURE

    @staticmethod
    def write_to_database(con, engine, df_dict: dict[str, pd.DataFrame]) -> None:
        # loop over each dataframe in dictionary
        # remember, key in dictionary is series id
        # so table names in sql database will be series id
        for id in df_dict:

            # format name or else will throw sql error
            table_name = str(id).replace(".", "_")

            # try querying the table
            # if it doesn't exist, catch exception and write table
            # if it does exit, remove duplicate rows from table
            # loaded into memory from df_dict and join with
            # original queried table.
            # write this table to databse, replacing original
            # and essentially just adding new columns
            try:
                original = pd.read_sql("SELECT * FROM %s" % table_name, con)

                new = df_dict[id]

                # drop common columns, join, and write
                new = new.drop([i for i in new.columns if i in original.columns], axis=1)
                new = original.join(new)
                new.to_sql(con=engine, name=table_name, index=False, if_exists="replace")
            except Exception:
                # write brand new table to DB
                df_dict[id].to_sql(con=engine, name=table_name, index=False)



    '''
        Function for querying series from world bank api
    '''
    @staticmethod
    def pull_from_wb(df_dict: dict[str, str]) -> dict[str, pd.DataFrame]:
        # dictionary to be returned, series id mapped to dataframe
        return_dict = {}
        # for each id in source dictionary, pull appropriate series as dataframe through api call
        for id in df_dict:
            return_dict[id] = wbgapi.data.DataFrame(id, df_dict[id]).transpose()
        return return_dict

    '''
        Function for loading all region and series names from world bank database
        Dictionaries mapping ids to names are written for both regions and series
    '''
    @staticmethod
    def load_jsons():
        # names and ids from world bank, organized a bit wonky
        series_info = wseries.info().items

        # map each series id to its text name in dictionary d
        series = {}
        for i in series_info:
            series[i["id"]] = i["value"]

        # do the same for regions
        region_info = wbgapi.region.info().items
        regions = {}
        for i in region_info:
            regions[i["code"]] = i["name"]

        # write to JSON files
        with open("WebApp/jsons/series_data.json", "w") as file:
            json.dump(series, file)

        with open("WebApp/jsons/regions_data.json", "w") as file:
            json.dump(regions, file)

def main():

    engine = sql.create_engine("sqlite:///gen_data.db")
    con = sql3.connect("gen_data.db")
    c = con.cursor()

    sample_data = {"AG.LND.EL5M.UR.K2" : ["AFW", "AFR", "AFE, LDC"],
                   "AG.LND.EL5M.UR.ZS" : ["AFW", "MNA", "LDC", "ECS", "NAC"]}


    Database.load_jsons()
    data_dict = Database.pull_from_wb(sample_data)

    Database.write_to_database(con, engine, data_dict)


if __name__ == "__main__":
    main()