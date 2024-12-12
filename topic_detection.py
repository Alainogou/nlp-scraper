import pandas as pd
import re
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

train_data=pd.read_csv('./data/bbc_news_train.txt', sep=',')
test_data=pd.read_csv('./data/bbc_news_tests.txt', sep=',')


# download nltk



lemmatizer = WordNetLemmatizer()


# nltk.download('all')
# nltk.download('punkt')  # For tokenization
# nltk.download('stopwords')  # For stopwords corpus
# nltk.download('wordnet') # For wordnet

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



def preprocessing(text):
    text= text.lower()
    
    text = re.sub('[^a-zA-Z]', ' ', text)

    words= word_tokenize(text)
    
    filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]

    filtered_phrases=' '.join(filtered_words)
    
    lemmatizer = lemmatize_passage(filtered_phrases)
  
    return  lemmatizer

# count_vecotrized_df = pd.DataFrame.sparse.from_spmatrix(train_data['Text'], columns=train_data['Text'].get_feature_names_out())
# print(count_vecotrized_df.iloc[:3,400:403])

train_data['Text']= [preprocessing(text) for text in train_data['Text'] ]
# words = word_tokenize(text)
# pos_tags = pos_tag(words)
# print(pos_tags)
print(train_data.head())



cv = CountVectorizer()

X = cv.fit_transform(train_data['Text'])

print(X.shape)

print()

# print(preprocessing(text))

