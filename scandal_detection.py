import pandas as pd
from nlp_enriched_news import entities_detection
import nltk
from nltk.tokenize import sent_tokenize
import spacy
# import spacy.cli
# spacy.cli.download("en_core_web_lg")

keywords=['pollution', 'deforestation', 'climate change', 'oil spill', 'desertification']

train_data=pd.read_csv('./data/bbc_news_train.txt', sep=',')

df= train_data.head(300)

df = df.copy() 

df['Org']= df['Text'].apply(entities_detection)

# Tokenizer des phrases (nltk doit être téléchargé si pas encore fait)
nltk.download('punkt_tab')


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


new_df=create_sentence_df(df)
# print(new_df)
nlp = spacy.load("en_core_web_lg")


def similarity(sentence, keyword):
    doc1 = nlp(keyword)
    doc2 = nlp(sentence)

    similarity = doc1.similarity(doc2)
    
    return similarity



import numpy as np

def scandal_detection(df, keywords):

    df =df.copy()

    key_words_colums=[]
    for keyword in keywords:
        df[f'similarity {keyword}']= df['sentence'].apply(lambda sentence: np.round(similarity(sentence, keyword), 2))
        key_words_colums.append(f'similarity {keyword}')

    article_scandal= df.groupby('articleid')[key_words_colums].max()


    score=[]

    for _, row in article_scandal.iterrows():
        score.append(np.mean(row[key_words_colums]))

    article_scandal['Scandal_distance'] = score
    
    top10_article = article_scandal.nlargest(10, 'Scandal_distance')

    article_scandal['Top_10'] = article_scandal['Scandal_distance'].apply(lambda x: x in top10_article['Scandal_distance'].values)


    return article_scandal




print(scandal_detection(new_df, keywords))