# pip install -U spacy
# python -m spacy download en_core_web_lg


import pandas as pd
import numpy as np
import nltk
nltk.download('vader_lexicon')
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy 

from data import  operations_db
import pickle
from results.preprocessing import preprocessing

# import spacy.cli
# spacy.cli.download("en_core_web_lg")
nlp = spacy.load("en_core_web_lg")


def entities_detection(text, nlp):
    doc = nlp(text)
    entities = []
    for entity in doc.ents:
        if entity.label_ == 'ORG' and entity.text not in  entities:  
            entities.append( entity.text)
            
    return entities


def sentiment_analysis(text): 
    
    """
    Analyzes the sentiment of a text using the VADER tool from NLTK.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    tuple: The overall sentiment score (compound) and the sentiment classification
           ('Positive', 'Negative', or 'Neutral').
    """

    
    analyzer = SentimentIntensityAnalyzer()

    scores = analyzer.polarity_scores(text)

    sentiment=''
    if scores['compound'] >= 0.05:
        sentiment= 'Positve'
    elif scores['compound'] <= -0.05:
        sentiment= 'Negative'
    else:
        sentiment= 'Neutral'

    return scores['compound'], sentiment
   


def create_sentence_df(df):
    new_rows = []
    
    for _, row in df.iterrows():
        articleid = row['ArticleId']
        text = row['Text']
        org_list = row['Org']
        
        sentences = sent_tokenize(text)
          
        for sentence in sentences:
            sentence = ' '.join(sentence.split())
            orgs_in_sentence = []  
            
            for org in org_list:
                if org in sentence and org not in orgs_in_sentence:
                    orgs_in_sentence.append(org)
            
            if orgs_in_sentence:
                new_rows.append([articleid, sentence, orgs_in_sentence])

    
    new_df = pd.DataFrame(new_rows, columns=['articleid', 'sentence', 'Org'])
    
    return new_df




def similarity(sentence, keyword, nlp):
    doc1 = nlp(keyword)
    doc2 = nlp(sentence)

    similarity = doc1.similarity(doc2)
    
    return similarity


def scandal_detection(row, keywords, org_list, nlp):

    body=row['Body']
    article_id= row['Unique ID']
    
        
    sentences = sent_tokenize(body)

    new_rows=[]

    for sentence in sentences:
        sentence = ' '.join(sentence.split())
        orgs_in_sentence = []  
            
        for org in org_list:

            if org in sentence and org not in orgs_in_sentence:
                orgs_in_sentence.append(org)  
        
        if orgs_in_sentence:
            new_rows.append([article_id, sentence, orgs_in_sentence])
                
    df = pd.DataFrame(new_rows, columns=['Unique ID', 'sentence', 'Org'])


    key_words_colums=[]
    for keyword in keywords:
        df[f'similarity {keyword}']= df['sentence'].apply(lambda sentence: np.round(similarity(sentence, keyword, nlp), 2))
        key_words_colums.append(f'similarity {keyword}')

    article_scandal_df= df.groupby('Unique ID')[key_words_colums].max()

    scandal_distance =  np.mean(article_scandal_df[key_words_colums])

    return scandal_distance
    
    
def enriched_sentence(row, nlp, model, vectorizer, dict_topic ):

    title= row['Headline']
    body=row['Body']
    artcle_id= row['Unique ID']
    
    print(f"\n\nEnriching {row['URL']}:")
     
    #---------------------------------- entity detection ----------------------------------

    print("\n--------- Detect entities ----------")
    text= title + ' ' +  body
    org=entities_detection(text,  nlp )
    print(f'Detected {len(org)} companies which are {", ".join(org)}')

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
    print(f'Environmental scandal detected for {", ".join(org)}')

    scandal_dist= scandal_detection(row, keywords, org, nlp)

    return org, topic, score_sentiment, scandal_dist



#load articles
df= operations_db.get_articles()

keywords=['pollution', 'deforestation', 'climate change', 'oil spill', 'desertification']
dict_topic = {1:'sport' ,  2: 'business',  3: 'politics', 4: 'entertainment' ,  5: 'tech'}


orgs=[]
topics=[]
sentiments=[]
scandal_distances=  []

#load model
with open("./results/vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

with open('./results/topic_classifier.pkl', 'rb') as mdl:
    model=pickle.load(mdl)




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

df.to_csv('./results/enhanced_news.csv', index= False)

print(df.head(5))







