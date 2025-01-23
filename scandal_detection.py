import pandas as pd
from nlp_enriched_news import entities_detection
import nltk
from nltk.tokenize import sent_tokenize
import spacy
# import spacy.cli
# spacy.cli.download("en_core_web_lg")

keywords=['pollution', 'deforestation', 'climate change', 'oil spill', 'desertification']

train_data=pd.read_csv('./data/bbc_news_train.txt', sep=',')

df= train_data.head()
df = df.copy() 

df['Org']= df['Text'].apply(entities_detection)

# Tokenizer des phrases (nltk doit être téléchargé si pas encore fait)
nltk.download('punkt')

def scandal_detection(df):
    print(df)


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


# new_df=create_sentence_df(df)
# print(new_df)


def similarity(sentence, keyword):

    nlp = spacy.load("en_core_web_lg")

    doc1 = nlp(keyword)
    doc2 = nlp(sentence)

    similarity = doc1.similarity(doc2)
    
    return similarity

sentenc='The rapid destruction of forests'
sent2='You are so good'

# new_df['similarity_deforestation']= new_df['sentence'].apply(lambda sentence: similarity(sentence, 'deforestion'))

# print(new_df)

print(similarity(sentence=sentenc, keyword='deforestation'))
print(similarity(sentence=sent2, keyword='deforestation'))