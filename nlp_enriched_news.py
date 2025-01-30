# pip install -U spacy
# python -m spacy download en_core_web_lg

import spacy 
from scripts import entities_detection, operations_db
import pickle
from scripts.preprocessing import preprocessing
from sentiment_analysis import sentiment_analysis
from scandal_detection import scandal_detection

# import spacy.cli
# spacy.cli.download("en_core_web_lg")


nlp = spacy.load("en_core_web_lg")


#load articles
df= operations_db.get_articles()

keywords=['pollution', 'deforestation', 'climate change', 'oil spill', 'desertification']
dict_topic = {1:'sport' ,  2: 'business',  3: 'politics', 4: 'entertainment' ,  5: 'tech'}


orgs=[]
topics=[]
sentiments=[]
scandal_distances=  []

#load model
with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

with open('topic_classifier.pkl', 'rb') as mdl:
    model=pickle.load(mdl)


def enriched_sentence(row, nlp, model, vectorizer, dict_topic ):

    title= row['Headline']
    body=row['Body']
    artcle_id= row['Unique ID']
    
    print(f"\n\nEnriching {row['URL']}:")
     
    #---------------------------------- entity detection ----------------------------------

    print("\n--------- Detect entities ----------")
    text= title + ' ' +  body
    org=entities_detection.entities_detection(text,  nlp )
    print(f'Detected {len(org)} companies which are {', '.join(org)}')

    #---------------------------------- Topic detection ----------------------------------

    print('\n\n---------- Topic detection ----------')

    print('Text preprocessing ...')
    body_preprocess = preprocessing(body)

    article_vect= vectorizer.transform([body_preprocess])

    topic_cat= model.predict(article_vect)[0]

    topic= dict_topic.get(topic_cat)

    print(f"The topic of the article {artcle_id}  is: {topic}")


    # #---------------------------------- Sentiment analysis ----------------------------------
    
    score_sentiment, sentiment= sentiment_analysis(body)
    print(f'The article **{title}** has a {sentiment} sentiment')


    # #---------------------------------- Scandal detection ------------------------------------

    print('\n\n---------- Scandal detection ----------')
    print('Computing embeddings and distance ...')
    print(f'Environmental scandal detected for {', '.join(org)}')

    scandal_dist= scandal_detection(row, keywords, org, nlp)


    return org, topic, score_sentiment, scandal_dist



    


for _, row in df.iterrows():
    org, topic, score_sentiment, scandal_dist =  enriched_sentence(row, nlp, model, vectorizer, dict_topic )
   
    orgs.append(org)
    topics.append(org)
    sentiments.append(score_sentiment)
    scandal_distances.append(scandal_dist)



df['Org']=orgs
df['Topics']=topics
df['Sentiment']= sentiments
df['Scandal_distance']= scandal_distances


top10_article = df.nlargest(10, 'Scandal_distance')

df['Top_10'] = df['Scandal_distance'].apply(lambda x: x in top10_article['Scandal_distance'].values)

df.to_csv('./results/enhanced_news.csv')

print(df.head(5))

