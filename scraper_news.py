from bs4 import BeautifulSoup
import requests



domain= 'https://www.bbc.com/news'

params=0


counter =0


html_text = requests.get(f'https://www.bbc.com/news')
if html_text.status_code == 200:
    soup= BeautifulSoup(html_text.text, 'lxml' )
    news= soup.find_all('div', {'data-testid': "anchor-inner-wrapper"})
    

    for new in news:
        is_article= new.find('div', {'data-testid':["edinburgh-article", "manchester-article", "chester-article"] })
        if is_article: 
            link= new.find('a', class_="sc-2e6baa30-0 gILusN")['href']
            title= new.find('h2', {'data-testid': "card-headline"})
            print(title.text)
            print(counter, domain+link)
            counter+=1
else:
    exit()


# for i in range(0, 1112):

#     html_text= requests.get(f'https://www.bbc.com/search?q=news&page={i}').text
#     soup= BeautifulSoup(html_text, 'lxml')


#     news = soup.find_all('div', attrs={'data-testid': "liverpool-card"})
   
#     for new in news:
#         is_article= new.find('div', attrs= {'data-testid':"liverpool-article"})
#         date_ago=  new.find('div', class_="sc-6fba5bd4-0 bFzmvn").text

#         if is_article and ('2 days' in date_ago) :

#             link= new.find('a', class_="sc-2e6baa30-0 gILusN")['href']   
#             title= new.find('h2', class_="sc-8ea7699c-3 gRBdkE").text
        
#             article_html= requests.get(domain+link).text

#             soup_article=BeautifulSoup(article_html, 'lxml')

#             main_content= soup_article.find("main", attrs={'id': "main-content"})
          
#             content_paragraphs = [line.get_text() for line in  main_content.find_all("p", attrs={'class': 'sc-eb7bd5f6-0 fYAfXe'})]
#             article_content = ''
#             for paragraph in content_paragraphs:
#                 paragraph = paragraph.replace("�", "'")
#                 article_content += paragraph
#             print({counter}, title)
#             # print(article_content)
#             # print({counter}, date_ago)
#             # print(domain+link)
#             counter+=1


# print(len(news))

#edinburgh-card  anchor-inner-wrapper





# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime

# def scrape_articles(date):
#     # URL de base pour la recherche
#     url = "https://www.bbc.com/search"
    
#     # Paramètres pour la requête
#     params = {
#         "q": f"news",
#         "page": 1,
#         "edgeauth": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJrZXkiOiAiZmFzdGx5LXVyaS10b2tlbi0xIiwiZXhwIjogMTczMzMyNTYzOCwibmJmIjogMTczMzMyNTI3OCwicmVxdWVzdHVyaSI6ICIlMkZzZWFyY2glM0ZxJTNEbmV3cyUyNnBhZ2UlM0Q1In0.0qhyMlc5C7tWH3Xt_eNIZ-uc5IAEm4b0ouSQx1Y6gqE"
#     }
    
#     articles = []
    
#     while True:
#         response = requests.get(url, params=params)
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             article_elements = soup.find_all('article', class_='ss-c-card')
            
#             for element in article_elements:
#                 title = element.find('h3', class_='ss-c-card__title').text.strip()
#                 date_published = element.find('time')['datetime']
                
#                 if datetime.fromisoformat(date) <= datetime.fromisoformat(date_published):
#                     articles.append({
#                         "title": title,
#                         "date_published": date_published
#                     })
            
#             next_page = soup.find('a', class_='gs-u-mb gs-u-mb@l')
            
#             if next_page and next_page['href']:
#                 params['page'] += 1
#                 params['q'] = f"news&page={params['page']}"
#             else:
#                 break
    
#     return articles

# # Exemple d'utilisation
# date_to_scrape = "2024-11-06"
# articles = scrape_articles(date_to_scrape)

# print(f"Articles publiés le {date_to_scrape}:")
# for article in articles:
#     print(f"- {article['title']} (Publié le {article['date_published']})")

# # Contrôle de la date
# scraped_date = datetime.fromisoformat(articles[0]['date_published'])
# if scraped_date.date() == datetime.strptime(date_to_scrape, "%Y-%m-%d").date():
#     print("\nContrôle de la date : OK")
# else:
#     print(f"\nErreur : La date des articles ne correspond pas à la date spécifiée.")
