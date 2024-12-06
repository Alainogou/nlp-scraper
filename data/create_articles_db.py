import sqlite3
from datetime import datetime

conn = sqlite3.connect('./data/articles.db')
cursor = conn.cursor()

# Création de la table
cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    URL TEXT NOT NULL,
    date TEXT NOT NULL,
    headline TEXT NOT NULL,
    body_article TEXT NOT NULL
)
''')

conn.close()






