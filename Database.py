import pandas as pd
import numpy as np
import sqlite3 as sql3
import sqlalchemy as sql
from PullSeries import load_jsons
from SeriesFormatter import *


'''
    Function that writes queried series to local sqlite3 database


'''
def update_series_tables(con, engine, df_dict: dict) -> None:
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



def main():
    #load_jsons()
    #sp = PullSeries()



    engine = sql.create_engine("sqlite:///gen_data.db")
    con = sql3.connect("gen_data.db")
    c = con.cursor()


    sf = SeriesFormatter()
    sample_data = {"AG.LND.EL5M.UR.K2" : ["AFW", "AFR", "AFE, LDC"],
                   "AG.LND.EL5M.UR.ZS" : ["AFW", "MNA", "LDC", "ECS"]}







    data_dict = sf.pull_compile_data(sample_data)




    update_series_tables(con, engine, data_dict)


if __name__ == "__main__":
    main()