from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from scripts import operations_db
import sqlite3
import pandas as pd


def get_description(url: str) -> str:

    article_html = requests.get(url)

    if article_html.status_code == 200:
        
        soup_article = BeautifulSoup(article_html.text, 'lxml')
        
        main_content = soup_article.find("main", attrs={'id': "main-content"})
        
        content_paragraphs = [line.get_text() for line in main_content.find_all("p", attrs={'class': ['sc-eb7bd5f6-0 fYAfXe', 'ssrcss-1q0x1qg-Paragraph e1jhz7w10']})]
        
        description = ''
        
        for paragraph in content_paragraphs:
            paragraph = paragraph.replace("�", "'") 
            description += paragraph + "\n" 
        
        return description
    else:
       exit()



def convert_to_date(date_str):

    days_ago = int(date_str.split()[0])

    today = pd.Timestamp.today()
    
    date = today - timedelta(days=days_ago)
    
    return date



def scraper_new(): 
    
    domain= 'https://www.bbc.com'

    counter =1
    page_id =0
    while counter<=350:
        
        html= requests.get(f'https://www.bbc.com/search?q=news&page={page_id}')

        if html.status_code == 200:
           
            conn = sqlite3.connect('./data/articles.db')

            soup= BeautifulSoup(html.text, 'lxml' )
            
            news= soup.find_all('div', {'data-testid': "newport-card"})
           
            
            
            for new in news:
                
                is_article = new.find('div', {'data-testid': "newport-article" } ) 

                if is_article: 

                    link = new.find('a', {'data-testid': "internal-link" })['href']
                    time_ago =new.find('span', class_="sc-6fba5bd4-1 efYorw")     
                
                    if time_ago.text in ["1 day ago", "2 days ago", "3 days ago", "4 days ago", "5 days ago"]:
                        
                        date= convert_to_date(time_ago.text).date()

                        title= new.find('h2', {'data-testid': "card-headline"})
                        url=domain+link
                        body_article= get_description(url)

                        operations_db.insert_article(conn, url, date, title.text, body_article )
                        

                        print(f'{counter} scraping {url}'
                            '\n     requesting ...'
                            '\n     parsing ...'
                            '\n     saved in <./data/articles.db>')
                        print('----------------------------------------------------------')
                        
                        counter+=1
                        
                        
            page_id += 1

            
        else:
            print(f'Error,${page_id}')
            exit()

    conn.close()   
        
        



scraper_new()