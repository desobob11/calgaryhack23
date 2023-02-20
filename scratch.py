import wbgapi.series as wseries
import json
import pandas as pd
import sqlite3 as sql3
import sqlalchemy as sql
import wbgapi

engine = sql.create_engine("sqlite:///gen_data.db")
con = sql3.connect("gen_data.db")

#df = pd.read_csv("test.csv")
#df.to_sql(con=engine, name="testing", index=False)

df = pd.read_sql("SELECT * FROM DT_NFL_PCBO_CD", con, index_col="index")
#df = wbgapi.data.DataFrame("DT.NFL.PCBO.CD", ["IDX", "USA"]).transpose()


df.to_csv("local.csv")
