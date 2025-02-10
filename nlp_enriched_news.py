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
    """
    The function takes two parameters as input:
     - `text`: a string containing the text in which entities need to be detected.
     - `nlp`: a pre-trained NLP model  from spaCy used to process the text.
    """
    doc = nlp(text)  # The NLP model is applied to the text, creating a 'doc' object containing all the processed linguistic information.
    
    entities = []  # Initialize an empty list to store detected entities.

    # Loop through all the entities detected in the text
    for entity in doc.ents:
        # Check if the entity is of type 'ORG' (organization) and if it hasn't already been added to the `entities` list.
        if entity.label_ == 'ORG' and entity.text not in entities:
            # If both conditions are met, append the entity's text to the list.
            entities.append(entity.text)
    
    return entities  # Return the list of organization ('ORG') entities detected in the text.



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
   


def similarity(sentence, keyword, nlp):
    """
     The function takes three parameters:
     - `sentence`: a string representing a sentence that will be compared.
     - `keyword`: a string representing a keyword to compare against the sentence.
     - `nlp`: a pre-trained NLP model from spaCy used to process both the sentence and the keyword.
    """
   

    doc1 = nlp(keyword)  # Apply the NLP model to the keyword, creating a 'doc' object for the keyword.
    doc2 = nlp(sentence)  # Apply the NLP model to the sentence, creating a 'doc' object for the sentence.

    similarity = doc1.similarity(doc2)  # Calculate the semantic similarity between the two 'doc' objects (keyword and sentence).
    
    return similarity  # Return the computed similarity score (a value between 0 and 1).


def scandal_detection(row, keywords, org_list, nlp):
    """
    The function takes four parameters:
    - `row`: a single row from the DataFrame containing information about an article (e.g., 'Body' and 'Unique ID').
    - `keywords`: a list of keywords to check against the sentences.
    - `org_list`: a list of organizations to search for within the article.
    - `nlp`: a pre-trained NLP model from spaCy to calculate semantic similarity.
    """
   

    body = row['Body']  # Extract the body text of the article from the row.
    article_id = row['Unique ID']  # Extract the unique article ID from the row.

    # Tokenize the article body into sentences.
    sentences = sent_tokenize(body)

    new_rows = []  # Initialize an empty list to store data for new rows.

    # Loop through each sentence in the article.
    for sentence in sentences:
        sentence = ' '.join(sentence.split())  # Clean up extra spaces in the sentence.
        orgs_in_sentence = []  # Initialize an empty list to store organizations found in the sentence.

        for org in org_list:
            if org in sentence and org not in orgs_in_sentence:
                orgs_in_sentence.append(org)  # Add the organization to the list if it appears in the sentence.

        # If at least one organization was found in the sentence, add the sentence and organizations to new_rows.
        if orgs_in_sentence:
            new_rows.append([article_id, sentence, orgs_in_sentence])

    df = pd.DataFrame(new_rows, columns=['Unique ID', 'sentence', 'Org'])

    key_words_colums = []

    # For each keyword, calculate the semantic similarity between the sentence and the keyword.
    for keyword in keywords:

        df[f'similarity {keyword}'] = df['sentence'].apply(lambda sentence: np.round(similarity(sentence, keyword, nlp), 2))
        key_words_colums.append(f'similarity {keyword}')

    # Group the DataFrame by 'Unique ID' and get the maximum similarity value for each keyword per article.
    article_scandal_df = df.groupby('Unique ID')[key_words_colums].max()

    # Calculate the average similarity across all keywords for each article.
    scandal_distance = np.mean(article_scandal_df[key_words_colums])

    return scandal_distance  # Return the mean similarity score, which can be used as a measure of scandal relevance.

    
    
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
    topics.append(topic)
    sentiments.append(score_sentiment)
    scandal_distances.append(scandal_dist)



df['Org']=orgs
df['Topics']=topics
df['Sentiment']= sentiments
df['Scandal_distance']= scandal_distances


top10_article = df.nlargest(10, 'Scandal_distance')

df['Top_10'] = df['Scandal_distance'].apply(lambda x: x in top10_article['Scandal_distance'].values)

df.to_csv('./results/enhanced_news.csv', index= False)








