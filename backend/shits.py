
import pandas as pd
import sqlite3 as sql3
import sqlalchemy as sql
import numpy as np

rands = pd.DataFrame(np.random.rand(100, 4))



con = sql3.connect("gen_data.db")

cursor = con.cursor()

#rands.to_sql("testing2", con)


df = pd.read_sql("SELECT * FROM testing2", con=con)

print(df)
