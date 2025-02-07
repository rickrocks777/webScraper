import pymysql
import requests
import json
import pandas
from sqlalchemy import create_engine
from urllib.parse import quote

df = pandas.read_json("tutorial\output.json")

db_username = "master"
db_password = "Aspl@345!"
db_host = "1.23.242.234"
db_port = '3306'
db_name = "gurugaon_sm_cid"

encoded_password = quote(db_password)

engine = create_engine(f"mysql+pymysql://{db_username}:{encoded_password}@{db_host}:{db_port}/{db_name}")
df.to_sql("website_data", con=engine, if_exists='replace', index=False)

print(df)