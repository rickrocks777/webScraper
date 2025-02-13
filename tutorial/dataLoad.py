import pymysql
import requests
import json
import pandas
from sqlalchemy import create_engine
from urllib.parse import quote

df = pandas.read_json("output.json")

db_username = "master"
db_password = "Aspl@345!"
db_host = "1.23.242.234"
db_port = '3306'
db_name = "gurugaon_sm_cid"

# df = df[~df.isnull().any(axis=1) & (df.apply(lambda x: x.str.strip() != '').all(axis=1))]
df = df[df['url'].str.strip() != "javascript: void(0)"]
df = df[df['text'].str.split().str.len() > 3]

encoded_password = quote(db_password)

engine = create_engine(f"mysql+pymysql://{db_username}:{encoded_password}@{db_host}:{db_port}/{db_name}")
df.to_sql("website_data", con=engine, if_exists='append', index=False)

print(df)