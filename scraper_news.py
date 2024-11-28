from bs4 import BeautifulSoup
import requests





html_text= requests.get('https://www.bbc.com').text

soup= BeautifulSoup(html_text, 'lxml')

#articles = soup.find_all('div', attrs={'data-testid': {'edinburgh-card', 'chester-card'}})

articles = soup.find_all('a', class_="sc-2e6baa30-0 gILusN")

counter=0
for article in articles:
    # link= article.find('a', class_="sc-2e6baa30-0 gILusN")['href']
  
    if 'articles' in  article['href'] or 'article' in  article['href'] :
       print(article['href'])
       counter+=1


print(len(articles), counter)

#edinburgh-card  anchor-inner-wrapper