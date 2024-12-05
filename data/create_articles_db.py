import sqlite3
from datetime import datetime

# Connexion à la base de données (création si elle n'existe pas)
conn = sqlite3.connect('./data/artices.db')
cursor = conn.cursor()

# Création de la table
cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    date_publication TEXT NOT NULL,
    titre TEXT NOT NULL,
    corps_article TEXT NOT NULL
)
''')



# Fonction pour insérer un article
def insert_article(url, date_publication, titre, corps_article):
    # Insertion de l'article dans la table
    cursor.execute('''
    INSERT INTO articles (url, date_publication, titre, corps_article)
    VALUES (?, ?, ?, ?)
    ''', (url, date_publication, titre, corps_article))
    
    # Sauvegarder les modifications
    conn.commit()

# # Exemple d'insertion avec une date de publication spécifique
# insert_article(
#     url="https://exemple.com/article1",
#     date_publication="2024-12-01 09:00:00",  # Date de publication
#     titre="Titre de l'article 1",
#     corps_article="Ceci est le corps de l'article 1."
# )

# insert_article(
#     url="https://exemple.com/article2",
#     date_publication="2024-12-02 10:30:00",  # Date de publication
#     titre="Titre de l'article 2",
#     corps_article="Ceci est le corps de l'article 2."
# )

# # Fonction pour récupérer et afficher tous les articles
# def get_articles():
#     cursor.execute('SELECT * FROM articles')
#     articles = cursor.fetchall()
#     for article in articles:
#         print(f"ID: {article[0]}")
#         print(f"URL: {article[1]}")
#         print(f"Date de publication: {article[2]}")
#         print(f"Titre: {article[3]}")
#         print(f"Corps de l'article: {article[4]}")
#         print("-" * 50)

# # Récupérer les articles
# get_articles()

# Fermer la connexion
conn.close()
