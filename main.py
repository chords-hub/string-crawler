import re
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
import importlib

def fetch_sites():
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_CHORDS_NAME')
    db_port = os.getenv('DB_PORT', '25059') 
    connect_timeout = 10
    
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            connect_timeout=connect_timeout
        )
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return []

    # Create a cursor object
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Execute the query to fetch feed URLs and news_id
    cursor.execute("SELECT * FROM sites")  # Replace 'your_table_name' with the actual table name
    
    # Fetch all URLs and news_ids
    sites = cursor.fetchall()
    
    # Close the connection
    cursor.close()
    conn.close()
    
    return sites

def start():
    sites = fetch_sites()
    for site in sites:
        print(f"Name: {site['name']}, URL: {site['url']}, Code: {site['code']}")
        module = importlib.import_module('crawlers.' + site['code'])
        module.start(site['url'])


if __name__ == "__main__":
    load_dotenv(override=True)
    start()