import pandas as pd
import numpy as np
import sqlite3 as sql3
import sqlalchemy as sql
from PullSeries import load_jsons
from SeriesFormatter import *

#pd.DataFrame(final_df).to_sql(con=engine, schema="AESO", name="aeso_csd_t", index=False, if_exists="append")
def update_series_tables(cursor, engine, df_dict: dict) -> None:
    for i in df_dict:
        try:
            cursor.execute("SELECT * from '%s'" % i)
            original = pd.read_sql_table(i, "sqlite:///gen_data.db")
            #original = cursor.execute("SELECT * from '%s'" % i)
            new = df_dict[i]
            #print(original)
            new = pd.DataFrame(new).join(original)
            new.to_sql(con=engine, name=i, index=False, if_exists="replace")
        except sql3.OperationalError:
            df = df_dict[i]
            df.to_sql(con=engine, name=i, index=False)












def main():
    #load_jsons()
    #sp = PullSeries()



    engine = sql.create_engine("sqlite:///gen_data.db")
    con = sql3.connect("gen_data.db")
    c = con.cursor()


    sf = SeriesFormatter()
    sample_data = {"AG.LND.EL5M.UR.K2" : ["AFW", "AFR", "AFE, LDC"],
                   "AG.LND.EL5M.UR.ZS" : ["AFW", "AFR", "LDC"]}







    data_dict = sf.pull_compile_data(sample_data)


    update_series_tables(c, engine, data_dict)


if __name__ == "__main__":
    main()