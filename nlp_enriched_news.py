# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy 
# import pickle
# from preprocessing import preprocessing
# from sentiment_analysis import sentiment_analysis

# import spacy.cli
# spacy.cli.download("en_core_web_sm")

def entities_detection(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = []
    for entity in doc.ents:
        if entity.label_ == 'ORG' and entity.text not in  entities:  
            entities.append( entity.text)
            
    return entities



text = ('ABC News has agreed to pay $15m (£12m) to US President-elect Donald Trump to settle a defamation lawsuit after its star anchor falsely said he had been found "liable for rape".'
'George Stephanopoulos made the statements repeatedly during an interview on 10 March this year while challenging a congresswoman about her support for Trump.'
'A jury in a civil case last year determined Trump was liable for "sexual abuse", which has a specific definition under New York law.'
'As part of Saturdays settlement, first reported by Fox News Digital ABC also published an editors note expressing its regret for the statements by Stephanopoulos.'
'According to the settlement, ABC News will pay $15m as a charitable contribution to a Presidential foundation and museum to be established by or for Plaintiff, as Presidents of the United States of America have established in the past'
'The $15m will go towards Trumps future presidential library, US media reported.'
'The network also agreed to pay $1m towards Trumps legal fees.'
'Under the settlement, the network will post an editors note to the bottom of its 10 March 2024 online news article about the story.'
'It will say: ABC News and George Stephanopoulos regret statements regarding President Donald J Trump made during an interview by George Stephanopoulos with Rep. Nancy Mace on ABCs This Week on March 10, 2024.'
'An ABC News spokesperson said in a statement the company was pleased that the parties have reached an agreement to dismiss the lawsuit on the terms in the court filing.'
'In 2023, a New York civil court found Trump sexually abused E Jean Carroll in a dressing room at a department store in 1996. He was also found guilty of defaming the magazine columnist.'
)
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