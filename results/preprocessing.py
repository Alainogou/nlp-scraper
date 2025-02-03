import nltk
import re
nltk.download('punkt')  # For tokenization
nltk.download('punkt_tab')
nltk.download('stopwords')  # For stopwords corpus
nltk.download('wordnet') # For wordnet
nltk.download('averaged_perceptron_tagger_eng')
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer





def stemming_text(text):
    porter = PorterStemmer()
    words = word_tokenize(text)
    
    stem_array = [porter.stem(word) for word in words]
    stem_sentence = ' '.join(stem_array)
    return  stem_sentence


def preprocessing(text):
    text= text.lower()
    
    text = re.sub('[^a-zA-Z]', ' ', text)

    words= word_tokenize(text)
    
    filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]

    filtered_phrases = ' '.join(filtered_words)
    
    stems =  stemming_text(filtered_phrases)
  
    return  stems
