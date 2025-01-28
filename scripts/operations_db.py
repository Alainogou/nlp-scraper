
import sqlite3
import pandas as pd


# Insert article
def insert_article(conn, url, date, headline, body_article):
   
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO articles (URL, 'Date scraped', Headline, Body)
    VALUES (?, ?, ?, ?)
    ''', (url, date, headline, body_article))
    
    conn.commit()


# Unique ID 
# URL 
# Date scraped 
# Headline 
# Body 

# Get articles

def get_articles():

    cnx = sqlite3.connect('./data/articles.db')

    df = pd.read_sql_query("SELECT * FROM articles", cnx)

    return df
