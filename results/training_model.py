import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import LearningCurveDisplay, ShuffleSplit
from preprocessing import preprocessing





train_data=pd.read_csv('../data/bbc_news_train.txt', sep=',')
test_data=pd.read_csv('../data/bbc_news_tests.txt', sep=',')

train_data['Text']= [preprocessing(text) for text in train_data['Text'] ]
test_data['Text']= [preprocessing(text) for text in test_data['Text'] ]
train_data.head()


cv = CountVectorizer()

X_train = cv.fit_transform(train_data['Text'])
X_test= cv.transform(test_data['Text'])

with open("vectorizer.pkl", "wb") as vec_file:
    pickle.dump(cv, vec_file)



dict_topic = {'sport': 1 ,  'business':2,  'politics': 3, 'entertainment':4 ,  'tech':5}
train_data['Category'] = train_data['Category'].apply(lambda x: dict_topic.get(x, 0))
test_data['Category'] = test_data['Category'].apply(lambda x: dict_topic.get(x, 0) )


y_train= train_data['Category']
y_test= test_data['Category']

clf = LogisticRegression(max_iter=10000, random_state=0)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")


with open('topic_classifier.pkl', 'wb') as file:
    pickle.dump(clf, file)


common_params = {
    "X": X_train,
    "y": y_train,
    "train_sizes": np.linspace(0.1, 1.0, 5),  
    "cv": ShuffleSplit(n_splits=50, test_size=0.2, random_state=0),  
    "score_type": "both",  
    "n_jobs": -1,  
    "line_kw": {"marker": "o"},  
    "std_display_style": "fill_between",  
    "score_name": "Accuracy",  
}


fig, ax = plt.subplots(figsize=(8, 6))

LearningCurveDisplay.from_estimator(clf, **common_params, ax=ax)

handles, label = ax.get_legend_handles_labels()
ax.legend(handles[:2], ["Training Score", "Test Score"])
ax.set_title("Learning Curve for Logistic Regression")
plt.grid(True)
plt.tight_layout()
# plt.show()

fig.savefig('learning_curves.png')
