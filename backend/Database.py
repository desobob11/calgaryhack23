import wbgapi.series as wseries
import json
import pandas as pd
import sqlite3 as sql3
import sqlalchemy as sql
import wbgapi
import re


'''
    Function that writes queried series to local sqlite3 database
'''
class Database:
# TODO: ACCOMODATE NEW DATE ROW ENTRIES FOR FUTURE

    @staticmethod
    def write_to_database(con, df_dict: dict[str, pd.DataFrame]) -> None:
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
                new = new.drop([i for i in new.columns if i in original.columns and i != "index"], axis=1)
     
                new = original.join(new)
                new.index = original.index
                con.cursor().execute("drop table %s" % table_name)
                new.to_sql(con=con, name=table_name, index=False)

            except Exception as e:
                # write brand new table to DB
                df_dict[id].to_sql(con=con, name=table_name, index=False)



    '''
        Function to query series from local sqlite3 database if it exists
        instead of querying from world bank again through API
    '''
    @staticmethod
    def pull_from_database(con, input_data: dict[str: list[str]]) -> dict[str, pd.DataFrame]:
        return_dict = {}
        for id in input_data:
            # remove periods in id for SQL safety
            safe_id = id.replace(".", "_")

            # get a list of all existing regions for series in database
            table_info = pd.read_sql("PRAGMA table_info(%s)" % safe_id, con)
            existing_columns = table_info["name"].tolist()

            # format list of existing columns into comma separated list for sql query
            good_columns = "%s" % ",".join([i for i in input_data[id] if i in existing_columns]) + ",year"
            print(good_columns)

            try:
                # query existing columns from database and add to dictionary key
                return_dict[id] =  pd.read_sql("SELECT %s from %s" % (good_columns, safe_id), con)

            except pd.errors.DatabaseError as e:
                pass
        return return_dict


    '''
        Function that takes in a dictionary of series to query.
        
        Returns a dictionary mapping series id to a list of region codes
        
        This function first loads all data that is available in local database first
        before pulling data through WB API.
        
        Any data that is not available locally is then pulled through WB API
    
    '''
    @staticmethod
    def load_data(con, input_data: dict[str, list[str]]) -> dict[str: pd.DataFrame]:
        # try pulling as much data as we can from database
        dataframes = Database.pull_from_database(con, input_data)


        # query rest of data from WB
        for id in input_data:
            # if key for series is in dataframes, ie local data from that series was pulled from sqlite
            try:
                local_data = dataframes[id]
                # only pull series data for regions that have no data stored locally
                series_to_pull = [i for i in input_data[id] if i not in local_data.columns and i !="index"]
                try:
                    pulled_data = Database.pull_from_wb(id, series_to_pull)
                    dataframes[id] = local_data.join(pulled_data)
                except:
                    pass
            # if no local data exists, just create the key value pair in dataframes
            except KeyError:
                try:
                    dataframes[id] = Database.pull_from_wb(id, input_data[id])
                except:
                    pass

        # write any new data to sqlite database
        Database.write_to_database(con, dataframes)
        return dataframes













    '''
        Function for pulling data from WB and formatting index
    '''
    @staticmethod
    def pull_from_wb(series_id:str, regions: list[str]) -> dict[str, pd.DataFrame]:
        # pull the series
        table = wbgapi.data.DataFrame(series_id, regions).transpose()



        # index starts as the format: ["YR2015, YR2016"], etc
        non_dates = table.index

        # new index
        dates = []
        for i in non_dates:
            # for each original index, append only numeric characters to new dates list
            dates.append(re.sub("[^0-9]", "", i))
        # replace the index and return the table
        table["year"] = dates
        return table





    '''
        Function for loading all region and series names from world bank database
        Dictionaries mapping ids to names are written for both regions and series
    '''
    @staticmethod
    def load_jsons() -> None:
        # names and ids from world bank, organized a bit wonky
        series_info = wseries.info().items

        # map each series id to its text name in dictionary d
        series = {}
        for i in series_info:
            series[i["id"]] = i["value"]

        # do the same for regions
        region_info = wbgapi.region.info().items
        country_info = wbgapi.economy.info().items

        regions = {}
        for i in region_info:
            regions[i["code"]] = i["name"]
        for i in country_info:
            regions[i["id"]] = i["value"]

        # write to JSON files
        with open("jsons/series_data.json", "w") as file:
            json.dump(series, file)

        with open("jsons/regions_data.json", "w") as file:
            json.dump(regions, file)





def main():

    engine = sql.create_engine("sqlite:///gen_data.db")
    con = sql3.connect("gen_data.db")
    c = con.cursor()

    #TODO: SOME SERIES DON'T WORK ADDRESS THIS EXAMPLE 'CSA':
    '''
    <wb:error>
    <wb:message id="160" key="Data not found.">
    The provided parameter value is not valid or data not found.
    </wb:message>
    </wb:error>
    '''

    sample_data = {"AG.LND.EL5M.UR.K2" : ["AFW", "LDC", "ECS", "NAC", "EUU", "MNA", "SAS", "CSA", "EAS"],
                  "AG.LND.EL5M.UR.ZS" : ["AFW", "MNA", "LDC", "ECS", "NAC", "EUU", "MNA", "SAS", "CSA", "EAS"]}

    #sample_data = {"AG.LND.EL5M.UR.K2" : ["AFW", "ECS", "LDC"],
     #              "AG.LND.EL5M.UR.ZS" : ["AFW", "ECS", "LDC"]}









   # Database.load_jsons()
    #data_dict = Database.pull_from_wb(sample_data)




   # Database.write_to_database(con, engine, data_dict)

    #dfs = Database.pull_from_database(con, engine, sample_data)
    dataframes = Database.load_data(con,sample_data)
    print(dataframes)


    #Database.load_jsons()

if __name__ == "__main__":
    main()