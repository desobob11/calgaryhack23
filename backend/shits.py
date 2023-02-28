
import pandas as pd
import sqlite3 as sql3
import sqlalchemy as sql
import numpy as np
from Database import *

rands = pd.DataFrame(np.random.rand(100, 4))

sample_data = {"AG.LND.EL5M.UR.K2" : ["AFW", "ECS", "LDC"],
                   "AG.LND.EL5M.UR.ZS" : ["AFW", "ECS", "LDC"]}



con = sql3.connect("gen_data.db")

data = Database.load_data(con, sample_data)
print(data)

cursor = con.cursor()

#rands.to_sql("testing2", con)


df = pd.read_sql("SELECT * FROM *", con=con)
df.to_csv("WB_data.csv")

print(df)


