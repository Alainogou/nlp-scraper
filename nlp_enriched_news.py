# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy 
from scripts import entity_detection, operations_db
# import pickle
from scripts.preprocessing import preprocessing

# from sentiment_analysis import sentiment_analysis

# import spacy.cli
# spacy.cli.download("en_core_web_lg")

nlp = spacy.load("en_core_web_lg")



df= operations_db.get_articles()

print(df.columns)


df['Org'] = df.apply(lambda x: entities_detection(x['Headline'] + x['Body'], nlp), axis=1)


print(df.head(1)[['Headline', 'Body']])
print(df.head(1)['Org'])


# with open('topic_classifier.pkl', 'rb') as file:
#     model=pickle.load(file)
#     article= preprocessing(text)
    

#     with open("vectorizer.pkl", "rb") as vectorizer_file:
#         vectorizer = pickle.load(vectorizer_file)
    
#         article_vect= vectorizer.transform([article])
#         # 'sport': 1, 'business': 2, 'politics': 3, 'entertainment': 4, 'tech': 5 business
#         print(model.predict(article_vect))
    
#     print(sentiment_analysis(article))

# print(entities_detection(text))