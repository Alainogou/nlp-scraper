

# Insert article
def insert_article(conn, url, date, headline, body_article):
   
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO articles (url, date, headline, body_article)
    VALUES (?, ?, ?, ?)
    ''', (url, date, headline, body_article))
    
    conn.commit()
    print("insert", headline)



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
