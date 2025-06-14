import sqlite3
from datetime import datetime

conn = sqlite3.connect('articles.db')
cursor = conn.cursor()

# create table

cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS articles (
            "Unique ID" INTEGER PRIMARY KEY,
            URL TEXT NOT NULL,
            'Date scraped' TEXT NOT NULL,
            Headline TEXT NOT NULL,
            Body TEXT NOT NULL
        )
    '''
)

conn.close()


