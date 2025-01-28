import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def sentiment_analysis(text): 
    
    analyzer = SentimentIntensityAnalyzer()

    scores = analyzer.polarity_scores(text)

    if scores['compound'] >= 0.05:
        return 'Positve'
    elif scores['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'



#