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
                new.to_sql(con=engine, name=table_name, index=True, if_exists="replace")
                # TODO: Traceback (most recent call last):
                #   File "C:\Users\desmo\calgaryhack23\Database.py", line 172, in <module>
                #     main()
                #   File "C:\Users\desmo\calgaryhack23\Database.py", line 168, in main
                #     Database.load_data(con, engine, sample_data)
                #   File "C:\Users\desmo\calgaryhack23\Database.py", line 87, in load_data
                #     Database.write_to_database(con, engine, dataframes)
                #   File "C:\Users\desmo\calgaryhack23\Database.py", line 43, in write_to_database
                #     df_dict[id].to_sql(con=engine, name=table_name, index=True)
                #   File "C:\Users\desmo\AppData\Local\Programs\Python\Python311\Lib\site-packages\pandas\core\generic.py", line 2987, in to_sql
                #     return sql.to_sql(
                #            ^^^^^^^^^^^
                #   File "C:\Users\desmo\AppData\Local\Programs\Python\Python311\Lib\site-packages\pandas\io\sql.py", line 695, in to_sql
                #     return pandas_sql.to_sql(
                #            ^^^^^^^^^^^^^^^^^^
                #   File "C:\Users\desmo\AppData\Local\Programs\Python\Python311\Lib\site-packages\pandas\io\sql.py", line 1728, in to_sql
                #     table = self.prep_table(
                #             ^^^^^^^^^^^^^^^^
                #   File "C:\Users\desmo\AppData\Local\Programs\Python\Python311\Lib\site-packages\pandas\io\sql.py", line 1631, in prep_table
                #     table.create()
                #   File "C:\Users\desmo\AppData\Local\Programs\Python\Python311\Lib\site-packages\pandas\io\sql.py", line 829, in create
                #     raise ValueError(f"Table '{self.name}' already exists.")
                # ValueError: Table 'AG_LND_EL5M_UR_K2' already exists.
                #
                # Process finished with exit code 1
            except Exception:
                # write brand new table to DB
                df_dict[id].to_sql(con=engine, name=table_name, index=True)


    '''
        Function to query series from local sqlite3 database if it exists
        instead of querying from world bank again through API
    '''
    @staticmethod
    def pull_from_database(con, engine, input_data: dict[str: list[str]]) -> dict[str, pd.DataFrame]:
        return_dict = {}
        for id in input_data:
            # remove periods in id for SQL safety
            safe_id = id.replace(".", "_")

            # get a list of all existing regions for series in database
            table_info = pd.read_sql("PRAGMA table_info(%s)" % safe_id, con)
            existing_columns = table_info["name"].tolist()

            # format list of existing columns into comma separated list for sql query
            good_columns = "'%s'" % ",".join([i for i in input_data[id] if i in existing_columns])

            try:
                # query existing columns from database and add to dictionary key
                return_dict[id] =  pd.read_sql("SELECT %s from %s" % (good_columns, safe_id), con)
            except pd.errors.DatabaseError:
                pass
        return return_dict



    @staticmethod
    def load_data(con, engine, input_data: dict[str, list[str]]) -> dict[str: pd.DataFrame]:
        dataframes = Database.pull_from_database(con, engine, input_data)

        for id in input_data:
            try:
                local_data = dataframes[id]
                series_to_pull = [i for i in input_data[id] if i not in local_data.columns]
                pulled_data = wbgapi.data.DataFrame(id, series_to_pull).transpose()
                print(pulled_data)
                dataframes[id] = local_data.join(pulled_data)
            except KeyError:
                dataframes[id] = wbgapi.data.DataFrame(id, input_data[id]).transpose()

        Database.write_to_database(con, engine, dataframes)
        return dataframes














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
        with open("jsons/series_data.json", "w") as file:
            json.dump(series, file)

        with open("jsons/regions_data.json", "w") as file:
            json.dump(regions, file)

def main():

    engine = sql.create_engine("sqlite:///gen_data.db")
    con = sql3.connect("gen_data.db")
    c = con.cursor()


    sample_data = {"AG.LND.EL5M.UR.K2" : ["AFW", "LDC", "ECS", "NAC", "EUU", "MNA", "SAS"],
                   "AG.LND.EL5M.UR.ZS" : ["AFW", "MNA", "LDC", "ECS", "NAC", "EUU", "MNA", "SAS"]}








   # Database.load_jsons()
    #data_dict = Database.pull_from_wb(sample_data)




   # Database.write_to_database(con, engine, data_dict)

    #dfs = Database.pull_from_database(con, engine, sample_data)
    Database.load_data(con, engine, sample_data)


if __name__ == "__main__":
    main()