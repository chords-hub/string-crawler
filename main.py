import re
import os
from db import DatabaseHandler
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
import importlib


def fetch_sites():
   
    db = DatabaseHandler()
    if not db.connect():
        return []
    sites = db.execute_query("SELECT * FROM sites")
    db.close()
    return sites

def start():
    sites = fetch_sites()
    for site in sites:
        print(f"Name: {site['name']}, URL: {site['url']}, Code: {site['code']}")
        module = importlib.import_module(site['code'])
        module.start(site['url'])


if __name__ == "__main__":
    load_dotenv(override=True)
    start()