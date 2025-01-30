import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def sentiment_analysis(text): 
    
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
   



#