import pandas as pd


train_data=pd.read_csv('./data/bbc_news_train.txt', sep=',')
test_data=pd.read_csv('./data/bbc_news_tests.txt', sep=',')


# download nltk

import nltk
# from nltk.tokenize import word_tokenize
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

lemmatizer = WordNetLemmatizer()
import re

#nltk.download('all')

 
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:         
        return wordnet.NOUN
    
def lemmatize_passage(text):
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in pos_tags]
    lemmatized_sentence = ' '.join(lemmatized_words)
    return lemmatized_sentence


text="It is better. 01 Edu System presents an innovative curriculum in software engineering and programming. With a renowned industry-leading reputation, the curriculum has been rigorously designed for learning skills of the digital world and technology industry. Taking a different approach than the classic teaching methods today, learning is facilitated through a collective and co-creative process in a professional environment."

def preprocessing(text):
    text= text.lower()
    
    text = re.sub('[^a-zA-Z]', ' ', text)

    words= word_tokenize(text)
    
    filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]

    filtered_phrases=' '.join(filtered_words)
    
    lemmatizer = lemmatize_passage(filtered_phrases)
    # r = ' '.join(lemmatizer_words)
    # # print(r)

    # porter_stemmer = PorterStemmer()
    # stemming_words= [ porter_stemmer.stem(word) for word in filtered_words]
    return  lemmatizer



train_data['Text']= [preprocessing(text) for text in train_data['Text'] ]
# words = word_tokenize(text)
# pos_tags = pos_tag(words)
# print(pos_tags)
print(train_data.head())



cv = CountVectorizer()

X = cv.fit_transform(train_data['Text'])

print(X.shape)

# count_vecotrized_df = pd.DataFrame.sparse.from_spmatrix(train_data['Text'], columns=train_data['Text'].get_feature_names_out())
# print(count_vecotrized_df.iloc[:3,400:403].to_markdown())
# print(preprocessing(text))
import matplotlib.pyplot as plt

# Calculer les proportions (normalisées) des catégories
category_proportions = train_data['Category'].value_counts(normalize=True)

# Tracer un graphique à barres
category_proportions.plot(kind='bar')

# Ajouter un titre et des labels aux axes
plt.title('Distribution des catégories')
plt.xlabel('Catégories')
plt.ylabel('Proportion')

# Afficher le graphique
plt.show()
