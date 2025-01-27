from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from data import insert_articles
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


def is_today(time_string: str):
    now = datetime.now()

    if time_string.lower() == "just now":
        return True
    
    if "hrs ago" in time_string or "hr ago" in time_string:
        hours= time_string.split()[0]
        try : 
           hrs=int(hours)
        except ValueError:
           return False
        
        diff= now-timedelta(hours=int(hours))
        return diff.date()==now.date()
    
    elif "mins ago" in time_string or "min ago" in time_string:
        try:
            minutes = int(time_string.split()[0])  
        except ValueError:
            return False  
        diff = now - timedelta(minutes=minutes)
        return diff.date() == now.date()

    elif "days ago" in time_string or 'day ago' in time_string:
        return False
    

    return False

def convert_to_date(date_str):
    # On extrait les jours (numéro) à partir de la chaîne de caractères
    days_ago = int(date_str.split()[0])  # "1 day ago" -> "1"
    
    # Date d'aujourd'hui
    today = pd.Timestamp.today()
    
    # Calcul de la date en soustrayant le nombre de jours
    date = today - timedelta(days=days_ago)
    
    return date



def scraper_new(): 
    
    
    domain= 'https://www.bbc.com/'

    counter =0
    # page_id =1
    for page_id in range(0, 10):
        
        # html = requests.get('https://www.bbc.com/news')
        html= requests.get(f'https://www.bbc.com/search?q=news&page={page_id}')

        if html.status_code == 200:
           
            conn = sqlite3.connect('./data/articles.db')
            

            soup= BeautifulSoup(html.text, 'lxml' )
            news= soup.find_all('div', {'data-testid': "anchor-inner-wrapper"})
           
            # news = soup.find_all('div', attrs={'data-testid': "liverpool-card"})
            

            
            for new in news:
                
                
                is_article= new.find('div', {'data-testid':["edinburgh-article", "manchester-article", "chester-article"] })
                print(len(news), is_article)
                if is_article: 
                    time_ago =new.find('span', class_="sc-6fba5bd4-1 efYorw")     
                
                    print(page_id)
                    if time_ago.text in ["1 day ago", "2 days ago", "3 days ago", "4 days ago", "5 days ago"]:
                        

                        date= convert_to_date(time_ago.text).date()

                        link= new.find('a', class_="sc-2e6baa30-0 gILusN")['href']
                        title= new.find('h2', {'data-testid': "card-headline"})
                        url=domain+link
                        body_article= get_description(url)

                        # insert_articles.insert_article(conn, url, date, title.text, body_article )
                        
                        print(counter, date, page_id, '------------------------------')
                        print(title.text, time_ago.text)
                        counter+=1
                        
            # page_id+=1

            conn.close()
        
        else:
            exit()

        



scraper_new()