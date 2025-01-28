# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy 
from scripts import entity_detection, operations_db
import pickle
from scripts.preprocessing import preprocessing

from sentiment_analysis import sentiment_analysis

# import spacy.cli
# spacy.cli.download("en_core_web_lg")

nlp = spacy.load("en_core_web_lg")


#load articles

df= operations_db.get_articles()


print("\n\n---------- Detect entities ----------")

df['Org'] = entity_detection.entities_detection(df, nlp)


#---------------------------------- Topic detection ----------------------------------
print('\n\n---------- Topic detection ----------')
print('Text preprocessing ...')

df['Text'] = df['Body'].apply(preprocessing)

topics=[]

with open('topic_classifier.pkl', 'rb') as file:
    
    model=pickle.load(file)

    with open("vectorizer.pkl", "rb") as vectorizer_file:

        vectorizer = pickle.load(vectorizer_file)

        for _, row in  df.iterrows():

            id= row['Unique ID']
            text= row['Text']
           
        
            article_vect= vectorizer.transform([text])

            dict_topic = {1:'sport' ,  2: 'business',  3: 'politics', 4: 'entertainment' ,  5: 'tech'}

            pred= model.predict(article_vect)[0]

            print(f"The topic of the article {id}  is: {dict_topic.get(pred)}")

            topics.append([pred])


df['Topics'] = topics



#---------------------------------- Sentiment analysis ----------------------------------
print('\n\n---------- Sentiment analysis ----------')
sentiments=[]
for _, row in df.iterrows():

    title= row['Headline']
    body=row['Body']
    sentiment= sentiment_analysis(body)
    sentiments.append(sentiment)
    print(f'The article **{title}** has a {sentiment} sentiment')

df['']


df.head(5)
# print(df.head(1)[['Headline', 'Body']])
# print(df.head(1)['Org'])




# print(entities_detection(text))