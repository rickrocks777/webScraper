import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote

Base = declarative_base()

# Define the WebsiteScraped table (for storing URLs and timestamps)
class WebsiteScraped(Base):
    __tablename__ = 'website_Scraped'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), unique=True)
    timestamp = Column(DateTime, default=datetime.now)

# Database connection
db_username = "master"
db_password = "Aspl@345!"
db_host = "1.23.242.234"
db_port = '3306'
db_name = "gurugaon_sm_cid"
encoded_password = quote(db_password)

engine = create_engine(f"mysql+pymysql://{db_username}:{encoded_password}@{db_host}:{db_port}/{db_name}") # Adjust database URL if needed
Base.metadata.create_all(engine)  # Create the table if not exists

Session = sessionmaker(bind=engine)
session = Session()

def update_or_insert_url(url):
    # Check if URL exists in the database
    existing_record = session.query(WebsiteScraped).filter(WebsiteScraped.url == url).first()
    
    if existing_record:
        # If it exists, update the timestamp
        existing_record.timestamp = datetime.now()
        session.commit()
        print(f"Timestamp for URL '{url}' updated.")
    else:
        # If it doesn't exist, insert the new URL with current timestamp
        new_record = WebsiteScraped(url=url, timestamp=datetime.now())
        session.add(new_record)
        session.commit()
        print(f"URL '{url}' inserted into the database.")

def scrapUrl(url):
    os.system(f'scrapy crawl dynamicSpider -a start_urls="{url}" -o output.json')

def clear_json_file(file_path):
    with open(file_path,'w') as file:
        pass


if __name__ == "__main__":
    url = sys.argv[1]
    update_or_insert_url(url)
    clear_json_file('tutorial\output.json')
    scrapUrl(url)    

# scrapUrl("https://timesofindia.indiatimes.com/india/haryana")

