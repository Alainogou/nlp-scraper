from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from data import insert_articles
import sqlite3


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





def scraper_new(): 
    domain= 'https://www.bbc.com/'

    # counter =0
    html_text = requests.get('https://www.bbc.com/news')
    if html_text.status_code == 200:
        conn = sqlite3.connect('./data/articles.db')
        

        soup= BeautifulSoup(html_text.text, 'lxml' )
        news= soup.find_all('div', {'data-testid': "anchor-inner-wrapper"})
    
    
        for new in news:
            is_article= new.find('div', {'data-testid':["edinburgh-article", "manchester-article", "chester-article"] })

            if is_article: 
                time_ago =new.find('span', class_="sc-6fba5bd4-1 efYorw")     
                
                if is_today(time_ago.text):
                    
                    date= datetime.now().date()
                    link= new.find('a', class_="sc-2e6baa30-0 gILusN")['href']
                    title= new.find('h2', {'data-testid': "card-headline"})
                    url=domain+link
                    body_article= get_description(url)

                    insert_articles.insert_article(conn, url, date, title.text, body_article )
                    
                    # print(counter, '-------------------------')
                    # print(title.text)
                    # counter+=1

        conn.close()

    else:
        exit()




scraper_new()